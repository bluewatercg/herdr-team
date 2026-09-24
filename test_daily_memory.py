import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile

spec = importlib.util.spec_from_file_location('daily_memory', Path(__file__).with_name('daily_memory.py'))
mem = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mem)

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    db = mem.connect(root / 'memory')
    transcript = root / 'pm.jsonl'
    transcript.write_text('\n'.join(json.dumps({'timestamp': stamp, 'type': 'message', 'message': {'role': 'assistant', 'content': [{'type': 'text', 'text': f'PM event {i}'}]}}) for i, stamp in enumerate(('2026-09-22T15:59:59Z', '2026-09-22T16:00:00Z'))) + '\n')
    db.execute('INSERT INTO sources VALUES (?,?)', ('lfa-pm', str(transcript)))
    db.commit()
    assert mem.capture(db)[0] == 2
    assert mem.capture(db)[0] == 0
    assert db.execute('SELECT day,count(*) FROM records GROUP BY day ORDER BY day').fetchall() == [('2026-09-22', 1), ('2026-09-23', 1)]
    mem.export(db, root / 'memory')
    assert json.loads((root / 'memory/2026-09-22/events.jsonl').read_text().splitlines()[0])['agent'] == 'lfa-pm'
    assert '[REDACTED]' in mem.scrub('{"api_key":"sk-' + 'x' * 40 + '"}')
    assert mem.day_of({'timestamp': '2026-09-22T15:59:59Z'}, dt.datetime.now(dt.timezone.utc))[0] == '2026-09-22'
    remote = root / 'grok-chat.jsonl'
    remote.write_text(json.dumps({'type': 'assistant', 'timestamp': '2026-09-23T09:00:00+08:00', 'content': [{'type': 'text', 'text': 'Grok work'}]}) + '\n')
    db.execute('INSERT INTO sources VALUES (?,?)', ('lfa-grok-review', str(remote)))
    db.commit()
    assert mem.capture(db)[0] == 1
    assert db.execute("SELECT agent FROM records WHERE body LIKE '%Grok work%'").fetchone() == ('lfa-grok-review',)
    mem.qwen = lambda prompt: 'derived ' + str(db.execute('SELECT count(*) FROM records').fetchone()[0])
    mem.summarize(db, root / 'memory', '2026-09-23')
    assert (root / 'memory/2026-09-23/summary.md').is_file()
    assert (root / 'memory/CURRENT.md').is_file()
    test_source = root / 'test.jsonl'
    test_source.write_text(json.dumps({'timestamp': '2026-09-23T10:00:00Z', 'type': 'message', 'text': 'TEST PASS TASK-1'}) + '\n')
    db.execute('INSERT INTO sources VALUES (?,?)', ('lfa-test', str(test_source)))
    db.commit()
    assert mem.capture(db)[0] == 1
    assert db.execute("SELECT count(*) FROM report_events WHERE agent='lfa-test'").fetchone() == (1,)
    assert db.execute("SELECT count(*) FROM records WHERE agent='lfa-test'").fetchone() == (0,)
    mem.qwen = lambda prompt, system=mem.SYSTEM: 'derived ' + str(db.execute('SELECT count(*) FROM records').fetchone()[0])
    mem.report(db, root / 'memory', '2026-09-23')
    assert (root / 'memory/2026-09-23/daily-report.md').is_file()
    assert db.execute("SELECT agent FROM records WHERE day='2026-09-23' AND body LIKE '%PM event 1%'").fetchone() == ('lfa-pm',)
