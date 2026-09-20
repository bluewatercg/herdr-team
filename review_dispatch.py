#!/usr/bin/env python3
"""Revision-bound review queue. Only the coordinator writes this state."""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unicodedata
from urllib.parse import unquote

BEGIN = '<!-- review-state -->\n'
END = '\n<!-- /review-state -->'
ROLES = ('lfa-review', 'lfa-pm')
PHASES = ('ACTIVE', 'AUTHOR_COMPLETE', 'REVIEW_PENDING', 'REVIEW_ACCEPTED', 'PM_PENDING', 'PM_ACCEPTED', 'CLOSED')
EVIDENCE_READY = {'IMPLEMENTED_PENDING_REVIEW', 'AUTHOR_COMPLETE', 'REVIEW_PENDING'}
WATCHDOG_SECONDS = 300


def gate_key(task_id, sha256, size, gate_type='REVIEW'):
    return f'{task_id}:{sha256}:{size}:{gate_type}'


def transition(row, phase):
    current = row.get('phase', row.get('status'))
    if current not in PHASES or phase not in PHASES or PHASES.index(phase) != PHASES.index(current) + 1:
        raise ValueError(f'Invalid state transition: {current} -> {phase}')
    row['phase'] = row['status'] = phase
    row['phase_changed'] = time.time()


def task_rows(root):
    text = (root / 'herdr-team/.agent-control/TASK_BOARD.md').read_text()
    headers, rows = [], []
    for line in text.splitlines():
        if line.strip().startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if 'TASK_ID' in cells and 'PLAN_ID' in cells:
                headers = cells
            elif headers and len(cells) == len(headers) and not all(set(c) <= {'-', ':'} for c in cells):
                rows.append(dict(zip(headers, cells)))
            continue
        headers = []
        fields = dict(re.findall(r'\b(PLAN_ID|DELIVERABLE_ID|TASK_ID|REQUIREMENT_IDS|OWNER|STATUS)=([^;\n]+)', line))
        if {'PLAN_ID', 'DELIVERABLE_ID', 'TASK_ID'} <= fields.keys():
            rows.append({key: value.strip() for key, value in fields.items()})
    unique = {}
    for row in rows:
        unique[(row.get('TASK_ID'), row.get('PLAN_ID'), row.get('DELIVERABLE_ID'))] = row
    return list(unique.values())


def legacy_gate_complete(root, task_id, sha256, size):
    text = (root / 'herdr-team/.agent-control/REVIEW_QUEUE.md').read_text()
    token = f'{sha256}/{size}bytes'
    spaced = f'{sha256} / {size} bytes'
    return task_id in text and (token in text or spaced in text) and 'CODE_REVIEW_ACCEPTED' in text and 'PM_ACCEPTED' in text


def discover_evidence(root, state):
    rows = task_rows(root)
    for path in sorted((root / 'herdr-team/.agent-control/EVIDENCE').glob('*.json')):
        try:
            evidence = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        required = ('task_id', 'plan_id', 'deliverable_id', 'status', 'write_owner')
        if any(not evidence.get(name) for name in required) or evidence['status'] not in EVIDENCE_READY:
            continue
        matches = [row for row in rows if row.get('TASK_ID') == evidence['task_id']]
        if len(matches) != 1 or matches[0].get('PLAN_ID') != evidence['plan_id'] or matches[0].get('DELIVERABLE_ID') != evidence['deliverable_id']:
            continue
        content = path.read_bytes()
        sha256, size = hashlib.sha256(content).hexdigest(), len(content)
        key = gate_key(evidence['task_id'], sha256, size)
        if key in state['submissions'] or legacy_gate_complete(root, evidence['task_id'], sha256, size):
            continue
        manifest = {str(path.relative_to(root)): sha256}
        valid = True
        for item in evidence.get('implementation_files', []):
            name, expected = item.get('path'), item.get('sha256')
            try:
                actual = file_hash(root, name)
            except (OSError, ValueError, TypeError):
                valid = False
                break
            if actual != expected:
                valid = False
                break
            manifest[name] = actual
        if not valid:
            continue
        envelope = {'task_id': evidence['task_id'], 'plan_id': evidence['plan_id'],
                    'deliverable_id': evidence['deliverable_id'],
                    'requirement_ids': [v.strip() for v in matches[0].get('REQUIREMENT_IDS', '').split(',') if v.strip()],
                    'source_references': [], 'artifacts': manifest, 'source_hashes': {},
                    'review_role': 'lfa-review', 'author_role': evidence['write_owner'],
                    'evidence_sha256': sha256, 'evidence_bytes': size}
        state['submissions'][key] = {'envelope': envelope, 'phase': 'AUTHOR_COMPLETE',
                                     'status': 'AUTHOR_COMPLETE',
                                     'delivery': {'lfa-review': 'QUEUED', 'lfa-pm': 'WAITING_INDEPENDENT_REVIEW'},
                                     'decisions': {}, 'created': time.time(), 'phase_changed': time.time()}
    return state


def review_roles(envelope):
    role = envelope.get('review_role', 'lfa-review')
    if (not isinstance(role, str) or not re.fullmatch(r'lfa-[a-z0-9_-]+', role)
            or role in ('lfa-pm', 'lfa-start')):
        raise ValueError('Invalid independent review role')
    return role, 'lfa-pm'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def load(root):
    text = (root / 'herdr-team/.agent-control/REVIEW_QUEUE.md').read_text()
    if BEGIN not in text:
        return {'version': 1, 'submissions': {}, 'last_reconcile': None}
    state = json.loads(text.split(BEGIN, 1)[1].split(END, 1)[0])
    if state.get('version') != 1 or not isinstance(state.get('submissions'), dict):
        raise ValueError('Invalid review state')
    return state


def save(root, state):
    path = root / 'herdr-team/.agent-control/REVIEW_QUEUE.md'
    text = path.read_text()
    block = BEGIN + json.dumps(state, ensure_ascii=False, indent=2) + END
    if BEGIN in text:
        before, rest = text.split(BEGIN, 1)
        _, after = rest.split(END, 1)
        text = before + block + after
    else:
        text += '\n' + block + '\n'
    fd, name = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextlib.contextmanager
def locked(root):
    # Directory inode remains stable across atomic queue replacement.
    fd = os.open(root / 'herdr-team/.agent-control', os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def file_hash(root, name):
    path = root / name
    if path.is_absolute() and not path.resolve().is_relative_to(root):
        raise ValueError('Artifact outside repository')
    if '..' in Path(name).parts or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('Unsafe artifact path')
    if not path.resolve().is_relative_to(root) or not path.is_file():
        raise ValueError('Missing or out-of-root artifact: ' + name)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def heading_slug(text):
    return ''.join(c for c in text.lower() if c in '-_' or not unicodedata.category(c).startswith(('P', 'S'))).replace(' ', '-')


def heading_ids(text):
    ids, fence = set(), None
    for line in text.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            continue
        if marker:
            fence = marker[1]
            continue
        match = re.match(r'^ {0,3}#{1,6}(?:[ \t]+(.*)|$)', line)
        if match:
            title = re.sub(r'[ \t]+#+[ \t]*$', '', match[1] or '').strip()
            base = heading_slug(title)
            slug, suffix = base, 0
            while slug in ids:
                suffix += 1
                slug = f'{base}-{suffix}'
            ids.add(slug)
    return ids


def submit(root, spec):
    required = ('task_id', 'plan_id', 'deliverable_id', 'requirement_ids', 'source_references', 'artifacts')
    if any(not spec.get(k) for k in required) or 'UNMAPPED' in str(spec['requirement_ids']):
        raise ValueError('Complete task, requirement, source and artifact binding required')
    roles = review_roles(spec)
    for field in ('artifacts', 'requirement_ids', 'source_references'):
        if not isinstance(spec[field], list) or any(not isinstance(v, str) or not v.strip() for v in spec[field]):
            raise ValueError('Artifacts, requirement IDs and source references must be string lists')
    board = (root / 'herdr-team/.agent-control/TASK_BOARD.md').read_text()
    headers, rows = [], []
    for line in board.splitlines():
        if not line.strip().startswith('|'):
            headers = []
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if 'TASK_ID' in cells and 'PLAN_ID' in cells:
            headers = cells
            continue
        if headers and len(cells) == len(headers):
            row = dict(zip(headers, cells))
            if row.get('TASK_ID') == spec['task_id']:
                rows.append(row)
    if (len(rows) != 1
            or any(rows[0].get(k.upper()) != spec[k] for k in ('plan_id', 'deliverable_id'))
            or {v.strip() for v in rows[0].get('REQUIREMENT_IDS', '').split(',')} != set(spec['requirement_ids'])):
        raise ValueError('Task binding not registered on TASK_BOARD')
    source_hashes = {}
    for ref in spec['source_references']:
        name, separator, fragment = ref.partition('#')
        file_hash(root, name)
        content = (root / name).read_bytes()
        if separator and (not fragment or heading_slug(unquote(fragment)) not in heading_ids(content.decode('utf-8'))):
            raise ValueError('Source fragment is not an ATX heading: ' + ref)
        source_hashes[name] = hashlib.sha256(content).hexdigest()
    manifest = {}
    for name in sorted(set(spec['artifacts'])):
        if Path(name).name in ('TASK_BOARD.md', 'REVIEW_QUEUE.md') or '/ROUNDS/' in name:
            raise ValueError('Mutable control ledger cannot be a submission artifact')
        manifest[name] = file_hash(root, name)
    envelope = {k: spec[k] for k in required if k != 'artifacts'}
    envelope['artifacts'] = manifest
    envelope['source_hashes'] = source_hashes
    envelope['review_role'] = roles[0]
    envelope['evidence_sha256'] = digest(manifest)
    envelope['evidence_bytes'] = sum((root / name).stat().st_size for name in manifest)
    key = gate_key(spec['task_id'], envelope['evidence_sha256'], envelope['evidence_bytes'])
    state = load(root)
    if key not in state['submissions']:
        for row in state['submissions'].values():
            if (row['envelope']['task_id'] == spec['task_id']
                    and review_roles(row['envelope']) == roles and row.get('phase') != 'CLOSED'):
                row['status'] = 'STALE'
        state['submissions'][key] = {'envelope': envelope, 'phase': 'AUTHOR_COMPLETE', 'status': 'AUTHOR_COMPLETE',
                                     'delivery': {roles[0]: 'QUEUED', roles[1]: 'WAITING_INDEPENDENT_REVIEW'},
                                     'decisions': {}, 'created': time.time(), 'phase_changed': time.time()}
        save(root, state)
    return key


def fresh(root, row):
    try:
        envelope = row['envelope']
        return bool(envelope.get('artifacts')) and all(
            file_hash(root, p) == sha
            for manifest in (envelope['artifacts'], envelope.get('source_hashes', {}))
            for p, sha in manifest.items())
    except (ValueError, OSError):
        return False


def accepted(root, key, row):
    envelope = row['envelope']
    expected = gate_key(envelope['task_id'], envelope['evidence_sha256'], envelope['evidence_bytes'])
    return (row.get('phase') in ('PM_ACCEPTED', 'CLOSED')
            and key == expected and bool(envelope.get('artifacts')) and fresh(root, row)
            and set(row['decisions']) == set(review_roles(envelope))
            and all(row['delivery'].get(role) == 'SENT'
                    and row['decisions'][role].get('action') == action
                    and isinstance(row['decisions'][role].get('evidence'), str)
                    and bool(row['decisions'][role]['evidence'].strip())
                    for role, action in zip(review_roles(envelope), ('CODE_REVIEW_ACCEPTED', 'PM_ACCEPTED'))))


def continue_accepted(root, state, key, row, send):
    if not accepted(root, key, row):
        return
    delivery = row.setdefault('continuation', {'status': 'QUEUED'})
    if delivery['status'] == 'DISPATCHING':
        delivery['status'] = 'DELIVERY_UNKNOWN'
    if delivery['status'] != 'QUEUED':
        return
    delivery.update(status='DISPATCHING', attempted=time.time())
    save(root, state)
    try:
        send('lfa-start', 'Accepted submission ' + key + '. Independent Review and PM accepted this exact revision. '
             'Re-read REVIEW_QUEUE.md, MASTER_PLAN.md, TASK_BOARD.md and FILE_OWNERSHIP.md. '
             'Immediately execute the next eligible authorized action with satisfied dependencies and conflict-free exact ownership. '
             'If none is eligible, record the specific blocker. This notification grants no authorization or business Gate unlock. '
             'Use this submission key to deduplicate continuation.')
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        delivery.update(status='DELIVERY_UNKNOWN', error=type(exc).__name__)
    else:
        delivery.update(status='SENT', acknowledged=time.time())
        delivery.pop('error', None)
        transition(row, 'CLOSED')
    save(root, state)


def reconcile(root, send=None):
    if send is None:
        def send(role, message):
            result = subprocess.run(['herdr', 'agent', 'prompt', role, message], capture_output=True, text=True, timeout=30, check=True)
            data = json.loads(result.stdout)
            if not isinstance(data, dict) or data.get('error') or data.get('result') is None:
                raise ValueError('Transport did not acknowledge submission')
    state = discover_evidence(root, load(root))
    now = time.time()
    for key, row in state['submissions'].items():
        if row.get('status') == 'STALE':
            continue
        if not fresh(root, row):
            row['status'] = 'STALE'
            continue
        reviewer, pm = review_roles(row['envelope'])
        phase = row.get('phase')
        if phase == 'AUTHOR_COMPLETE':
            transition(row, 'REVIEW_PENDING')
            phase = 'REVIEW_PENDING'
        role = reviewer if phase == 'REVIEW_PENDING' else pm if phase == 'PM_PENDING' else None
        if role:
            delivery = row['delivery'].get(role)
            if delivery == 'DISPATCHING':
                row['delivery'][role] = 'DELIVERY_UNKNOWN'
            elif delivery == 'QUEUED':
                row['delivery'][role] = 'DISPATCHING'
                row['last_dispatch_attempt'] = now
                save(root, state)
                try:
                    send(role, f'{"Review" if role == reviewer else "PM Gate"} submission {key}. '
                         'Read the exact structured envelope in herdr-team/.agent-control/REVIEW_QUEUE.md. '
                         'Record only a role-attributed disposition for this revision; transport is not acceptance.')
                    row['delivery'][role] = 'SENT'
                except (OSError, ValueError, subprocess.SubprocessError) as exc:
                    row['delivery'][role] = 'DELIVERY_UNKNOWN'
                    row['transport_error'] = type(exc).__name__
                save(root, state)
        continue_accepted(root, state, key, row, send)
    state['last_reconcile'] = now
    save(root, state)
    return state


def decision(root, key, role, action, evidence):
    state = load(root)
    row = state['submissions'].get(key)
    if not row or row.get('status') == 'STALE' or not fresh(root, row):
        raise ValueError('Unknown or stale submission')
    reviewer, pm = review_roles(row['envelope'])
    phase = row.get('phase')
    allowed = {reviewer: ('IN_REVIEW', 'CODE_REVIEW_ACCEPTED', 'CHANGES_REQUESTED'),
               pm: ('PM_ACCEPTED', 'CHANGES_REQUESTED')}
    if action not in allowed.get(role, ()) or not evidence.strip():
        raise ValueError('Invalid role, disposition or evidence')
    expected_phase = 'REVIEW_PENDING' if role == reviewer else 'PM_PENDING'
    if phase != expected_phase or row['delivery'].get(role) != 'SENT':
        raise ValueError(f'{role} decision requires {expected_phase} with confirmed delivery')
    if action == 'IN_REVIEW':
        row.setdefault('acknowledgments', {}).setdefault(role, {'action': action, 'evidence': evidence, 'time': time.time()})
        save(root, state)
        return row
    if role in row['decisions']:
        raise ValueError('Role decision already recorded')
    row['decisions'][role] = {'action': action, 'evidence': evidence, 'time': time.time()}
    if action == 'CHANGES_REQUESTED':
        row['status'] = 'CHANGES_REQUESTED'
    elif role == reviewer:
        transition(row, 'REVIEW_ACCEPTED')
        transition(row, 'PM_PENDING')
        row['delivery'][pm] = 'QUEUED'
    else:
        transition(row, 'PM_ACCEPTED')
    save(root, state)
    return row

def agent_states(root):
    result = subprocess.run(['herdr', 'agent', 'list'], cwd=root, capture_output=True, text=True, timeout=10, check=True)
    data = json.loads(result.stdout)
    agents = data.get('result', {}).get('agents', [])
    return {agent.get('name'): agent.get('agent_status') for agent in agents if agent.get('name')}


def watchdog(root, state, send, statuses=None, now=None, timeout=WATCHDOG_SECONDS):
    statuses = agent_states(root) if statuses is None else statuses
    now = time.time() if now is None else now
    for key, row in state['submissions'].items():
        phase = row.get('phase')
        changed = row.get('phase_changed', row.get('created', now))
        if now - changed < timeout:
            continue
        reviewer, _ = review_roles(row['envelope'])
        role = row['envelope'].get('author_role') if phase == 'ACTIVE' else reviewer if phase == 'REVIEW_PENDING' else None
        if role and statuses.get(role) == 'idle':
            watchdog_key = gate_key(row['envelope']['task_id'], row['envelope']['evidence_sha256'],
                                    row['envelope']['evidence_bytes'], f'WATCHDOG:{phase}')
            previous = row.setdefault('watchdog', {}).get(watchdog_key, 0)
            if now - previous >= timeout:
                send(role, f'Watchdog continuation {watchdog_key}. Structured task phase is {phase} and remains open. '
                     'Resume this exact original task/revision; do not create a replacement Agent. '
                     'Read REVIEW_QUEUE.md and TASK_BOARD.md before acting.')
                row['watchdog'][watchdog_key] = now
    board_age = now - (root / 'herdr-team/.agent-control/TASK_BOARD.md').stat().st_mtime
    if board_age >= timeout:
        for task in task_rows(root):
            if 'ACTIVE' not in task.get('STATUS', ''):
                continue
            role_match = re.search(r'lfa-[a-z0-9_-]+', task.get('OWNER', ''))
            role = role_match.group() if role_match else None
            if not role or statuses.get(role) != 'idle':
                continue
            watchdog_key = gate_key(task['TASK_ID'], 'PENDING_EVIDENCE', 0, 'WATCHDOG:ACTIVE')
            previous = state.setdefault('watchdog', {}).get(watchdog_key, 0)
            if now - previous >= timeout:
                send(role, f'Watchdog continuation {watchdog_key}. TASK_BOARD keeps this original task ACTIVE without fresh structured progress. '
                     'Resume the same task and owner; do not create a replacement Agent.')
                state['watchdog'][watchdog_key] = now
    save(root, state)
    return state


def resolve_delivery(root, key, role, action, evidence):
    state = load(root)
    row = state['submissions'][key]
    if role not in (*review_roles(row['envelope']), 'lfa-start'):
        raise ValueError('Role not bound to this submission')
    continuation = role == 'lfa-start'
    delivery = row.get('continuation', {}) if continuation else row['delivery']
    field = 'status' if continuation else role
    if (row['status'] == 'STALE' or not fresh(root, row)
            or delivery.get(field) not in ('DELIVERY_UNKNOWN', 'DISPATCHING')
            or not evidence.strip() or action not in ('SENT', 'QUEUED')
            or (continuation and not accepted(root, key, row))):
        raise ValueError('Only current ambiguous delivery may be resolved with evidence')
    delivery[field] = action
    if continuation and action == 'SENT':
        delivery['acknowledged'] = time.time()
    row.setdefault('resolutions', []).append({'role': role, 'action': action, 'evidence': evidence, 'time': time.time()})
    save(root, state)
    return row


def watch_address(root):
    if os.environ.get('HERDR_ENV') != '1':
        raise ValueError('watch requires a Herdr-managed environment')
    result = subprocess.run(['herdr', 'status', '--json'], capture_output=True, text=True, timeout=10, check=True)
    server = json.loads(result.stdout).get('server', {})
    session = server.get('socket') if server.get('running') is True else None
    if not session:
        raise ValueError('Cannot identify current Herdr socket')
    session = str(Path(session).resolve())
    os.environ['HERDR_SOCKET_PATH'] = session
    return '\0lfa-review-' + digest([str(root), session])


def watch_ready(address, timeout=1):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.settimeout(timeout)
            client.connect(address)
            data = json.loads(client.recv(4096))
            return data if data.get('ready') else None
    except (OSError, ValueError):
        return None


def ensure_watch(root):
    address = watch_address(root)
    ready = watch_ready(address)
    if ready:
        return ready
    child = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '--root', str(root), 'watch'],
                             cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
    deadline = time.monotonic() + 100
    while time.monotonic() < deadline:
        ready = watch_ready(address)
        if ready:
            return ready
        if child.poll() not in (None, 0):
            raise ValueError('watch startup failed; run watch in foreground for diagnostics')
        time.sleep(.1)
    raise ValueError('watch readiness timed out; existing process was not killed')


def watch_loop(root, interval):
    address = watch_address(root)
    # Linux abstract sockets disappear on exit; bind arbitrates concurrent starters without stale PID files.
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        try:
            server.bind(address)
        except OSError as exc:
            import errno
            if exc.errno != errno.EADDRINUSE:
                raise
            if watch_ready(address, 95):
                return
            raise ValueError('Existing watch is not responsive; refusing duplicate') from exc
        server.listen(16)
        with locked(root):
            load(root)
        ready = json.dumps({'ready': True, 'pid': os.getpid(), 'root': str(root),
                            'socket': os.environ['HERDR_SOCKET_PATH']}).encode()
        def serve_ready():
            while True:
                try:
                    connection, _ = server.accept()
                except OSError:
                    return
                with connection:
                    connection.settimeout(1)
                    try:
                        connection.sendall(ready)
                    except OSError:
                        pass
        threading.Thread(target=serve_ready, daemon=True).start()
        while True:
            with locked(root):
                state = reconcile(root)
                watchdog(root, state, lambda role, message: subprocess.run(
                    ['herdr', 'agent', 'prompt', role, message], capture_output=True,
                    text=True, timeout=30, check=True))
            time.sleep(interval)


def self_test():
    calls = []
    with tempfile.TemporaryDirectory(prefix='review-dispatch-') as directory:
        root = Path(directory)
        control = root / 'herdr-team/.agent-control'
        (control / 'EVIDENCE').mkdir(parents=True)
        (control / 'REVIEW_QUEUE.md').write_text('# Isolated queue\n')
        (control / 'TASK_BOARD.md').write_text(
            '| TASK_ID | PLAN_ID | DELIVERABLE_ID | REQUIREMENT_IDS |\n'
            '| --- | --- | --- | --- |\n| T | P | D | R |\n')
        (root / 'artifact.txt').write_text('revision one')
        artifact_sha = file_hash(root, 'artifact.txt')
        evidence = {'task_id': 'T', 'plan_id': 'P', 'deliverable_id': 'D',
                    'requirement_ids': ['R'], 'write_owner': 'lfa-api',
                    'status': 'IMPLEMENTED_PENDING_REVIEW',
                    'implementation_files': [{'path': 'artifact.txt', 'sha256': artifact_sha}]}
        evidence_path = control / 'EVIDENCE/D.json'
        evidence_path.write_text(json.dumps(evidence))
        send = lambda role, message: calls.append((role, message))
        with locked(root):
            state = reconcile(root, send)
            assert len(state['submissions']) == 1
            key, row = next(iter(state['submissions'].items()))
            envelope = row['envelope']
            assert key == gate_key('T', envelope['evidence_sha256'], envelope['evidence_bytes'], 'REVIEW')
            assert row['phase'] == 'REVIEW_PENDING'
            assert [role for role, _ in calls] == ['lfa-review']
            reconcile(root, send)
            assert [role for role, _ in calls] == ['lfa-review']

            for role, action in (('lfa-pm', 'PM_ACCEPTED'), ('lfa-review', 'CODE_REVIEW_ACCEPTED')):
                if role == 'lfa-review':
                    continue
                try:
                    decision(root, key, role, action, 'premature')
                except ValueError:
                    pass
                else:
                    raise AssertionError('state skip accepted')
            decision(root, key, 'lfa-review', 'IN_REVIEW', 'claimed')
            decision(root, key, 'lfa-review', 'CODE_REVIEW_ACCEPTED', 'review evidence')
            assert load(root)['submissions'][key]['phase'] == 'PM_PENDING'
            reconcile(root, send)
            assert [role for role, _ in calls] == ['lfa-review', 'lfa-pm']
            decision(root, key, 'lfa-pm', 'PM_ACCEPTED', 'PM evidence')
            assert load(root)['submissions'][key]['phase'] == 'PM_ACCEPTED'
            reconcile(root, send)
            assert [role for role, _ in calls] == ['lfa-review', 'lfa-pm', 'lfa-start']
            assert load(root)['submissions'][key]['phase'] == 'CLOSED'
            reconcile(root, send)
            assert len(calls) == 3

            for current, target in (('ACTIVE', 'REVIEW_PENDING'), ('REVIEW_PENDING', 'PM_PENDING'),
                                    ('PM_PENDING', 'CLOSED'), ('CLOSED', 'PM_ACCEPTED')):
                candidate = {'phase': current}
                try:
                    transition(candidate, target)
                except ValueError:
                    pass
                else:
                    raise AssertionError((current, target))

            watchdog_row = {'envelope': dict(envelope, author_role='lfa-api'), 'phase': 'ACTIVE',
                            'status': 'ACTIVE', 'created': 1, 'phase_changed': 1,
                            'delivery': {}, 'decisions': {}}
            watchdog_state = {'version': 1, 'submissions': {'watch': watchdog_row}, 'last_reconcile': None}
            save(root, watchdog_state)
            watchdog(root, watchdog_state, send, {'lfa-api': 'idle'}, now=1000, timeout=10)
            assert calls[-1][0] == 'lfa-api'
            count = len(calls)
            watchdog(root, load(root), send, {'lfa-api': 'idle'}, now=1001, timeout=10)
            assert len(calls) == count

            evidence['task_id'] = 'UNKNOWN'
            evidence_path.write_text(json.dumps(evidence))
            save(root, {'version': 1, 'submissions': {}, 'last_reconcile': None})
            reconcile(root, send)
            assert not load(root)['submissions']
    return {'self_test': 'PASS',
            'scenarios': 'structured Evidence discovery; explicit seven-state lifecycle; sequential Review then PM then START; revision gate key; forbidden skips; restart deduplication; idle original-owner watchdog deduplication; unregistered Evidence rejection'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    commands = parser.add_subparsers(dest='command', required=True)
    sub = commands.add_parser('submit')
    sub.add_argument('spec', type=Path, help='JSON envelope with task/plan/deliverable, IDs, source_references and artifact paths')
    commands.add_parser('reconcile')
    commands.add_parser('ensure-watch')
    commands.add_parser('self-test')
    watch = commands.add_parser('watch')
    watch.add_argument('--interval', type=float, default=10)
    dec = commands.add_parser('decision')
    for arg in ('key', 'role', 'action', 'evidence'):
        dec.add_argument(arg)
    resolve = commands.add_parser('resolve')
    resolve.add_argument('key')
    resolve.add_argument('role')
    resolve.add_argument('action', choices=('SENT', 'QUEUED'))
    resolve.add_argument('evidence')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == 'watch' and args.interval < 1:
        parser.error('interval must be at least one second')
    try:
        if args.command == 'self-test':
            print(json.dumps(self_test()))
            return
        if args.command == 'ensure-watch':
            print(json.dumps(ensure_watch(root)))
            return
        if args.command == 'watch':
            watch_loop(root, args.interval)
            return
        while True:
            with locked(root):
                if args.command == 'submit':
                    result = submit(root, json.loads(args.spec.read_text()))
                    reconcile(root)
                elif args.command == 'decision':
                    result = decision(root, args.key, args.role, args.action, args.evidence)
                elif args.command == 'resolve':
                    resolve_delivery(root, args.key, args.role, args.action, args.evidence)
                    result = reconcile(root)
                else:
                    result = reconcile(root)
            print(json.dumps(result, ensure_ascii=False), flush=True)
            break
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
