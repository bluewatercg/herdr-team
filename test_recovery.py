"""Exercise the real menu with a fake Herdr transport; never touch a live session."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
ROLES = 'lfa-start lfa-pm lfa-android lfa-api lfa-ios lfa-test lfa-review lfa-grok-review lfa-claude-review'.split()


def check():
    for live, fault in [(['lfa-pm'], False), ([], False), (ROLES, False), ([], True)]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kit = root / 'herdr-team'
            kit.mkdir()
            for name in ('lfa-team.sh', 'activate.sh', 'config.env'):
                shutil.copy2(ROOT / name, kit / name)
            shutil.copytree(ROOT / 'prompts', kit / 'prompts')
            control = kit / '.agent-control'
            control.mkdir()
            gate = b'RUN_ID: existing-round\nSTATUS: READY\n'
            (control / 'PM_GATE').write_bytes(gate)
            (control / 'TASK_BOARD.md').write_text('existing tasks\n')
            (kit / 'review_dispatch.py').write_text('pass\n')
            state = root / 'state.json'
            state.write_text(json.dumps(live))
            log = root / 'calls.jsonl'
            binary = root / 'herdr'
            binary.write_text('''#!/usr/bin/env python3
import json, os, pathlib, sys
args = sys.argv[1:]
with open(os.environ['CALLS'], 'a') as f: f.write(json.dumps(args) + '\\n')
p = pathlib.Path(os.environ['STATE'])
live = json.loads(p.read_text())
if args[:2] == ['agent', 'get']:
    if os.environ['FAULT'] == '1':
        print(json.dumps({'error': {'code': 'connection_error'}}), file=sys.stderr); sys.exit(1)
    if args[2] not in live:
        print(json.dumps({'error': {'code': 'agent_not_found'}}), file=sys.stderr); sys.exit(1)
elif args[:2] == ['workspace', 'create']:
    print(json.dumps({'result': {'root_pane': {'pane_id': 'w1:p1'}}})); sys.exit(0)
elif args[:2] == ['agent', 'start']:
    assert args[2] not in live
    live.append(args[2]); p.write_text(json.dumps(live))
elif args[:2] == ['agent', 'prompt']:
    assert args[2] in live
print(json.dumps({'result': {}}))
''')
            binary.chmod(0o755)
            env = dict(os.environ, PATH=str(root) + ':' + os.environ['PATH'], STATE=str(state), CALLS=str(log), FAULT=str(int(fault)))
            result = subprocess.run(['bash', str(kit / 'lfa-team.sh')], input='3\n', text=True, capture_output=True, env=env)
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            started = [call[2] for call in calls if call[:2] == ['agent', 'start']]
            assert (control / 'PM_GATE').read_bytes() == gate
            assert (control / 'TASK_BOARD.md').read_text() == 'existing tasks\n'
            if fault:
                assert result.returncode != 0 and not started, result.stderr
            else:
                assert result.returncode == 0, result.stderr
                assert started == [role for role in ROLES if role not in live]
                again = subprocess.run(['bash', str(kit / 'lfa-team.sh')], input='3\n', text=True, capture_output=True, env=env)
                assert again.returncode == 0, again.stderr
                after = [json.loads(line) for line in log.read_text().splitlines()]
                assert sum(call[:2] == ['agent', 'start'] for call in after) == len(started)
            print(f'PASS: live={live}, transport_fault={fault}; Gate and tasks preserved')


if __name__ == '__main__':
    check()
