from pathlib import Path
import hashlib, json, shutil, sys

work = Path(__file__).resolve().parent
root = work.parents[1]
stage = work / 'EXAM_HANDOFF'
baseline = json.loads((work / 'baseline.json').read_text())
preserved = json.loads((work / 'preserved-concurrent.json').read_text()) if (work / 'preserved-concurrent.json').exists() else {}
prefix = '01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/'
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
def allowed(rel):
    parts = Path(rel).parts
    if any(p in {'Objects', 'Listings', '__pycache__'} or p.startswith('.') for p in parts):
        return False
    if rel == 'START_HERE.html': return True
    if rel.startswith(prefix + '01_GUIDES_AND_INDEXES/PORTAL/'): return True
    if rel.startswith(prefix + '99_MAINTENANCE/'):
        return Path(rel).suffix in {'.py', '.c', '.cjs', '.js', '.css', '.md', '.json', '.log'} and (Path(rel).suffix != '.log' or '/scenario-native-logs/' in rel)
    project = prefix + '03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/pattern-projects/'
    return rel.startswith(project) and rel[len(project):].split('/')[0].startswith(('mix-', 'task-', 'paper-'))

conflicts = [rel for rel, sha in baseline.items() if digest(root / rel) != preserved.get(rel, sha)]
changes = []
for src in stage.rglob('*'):
    if not src.is_file(): continue
    rel = src.relative_to(stage).as_posix()
    if rel in preserved: continue
    if not allowed(rel): continue
    sha = digest(src)
    if sha == baseline.get(rel): continue
    if digest(root / rel) != baseline.get(rel): conflicts.append(rel)
    changes.append({'path': rel, 'sha256': sha, 'previous': baseline.get(rel)})
if conflicts:
    (work / 'integration-conflicts.json').write_text(json.dumps(sorted(set(conflicts)), indent=2))
    raise SystemExit('Concurrent changes found; integration stopped')
(work / 'integration-preview.json').write_text(json.dumps(changes, indent=2))
print('Reviewed changed/new files:', len(changes), flush=True)
if '--apply' not in sys.argv: raise SystemExit(0)
backup = work / 'integration-backup'
for row in changes:
    rel = row['path']; dst = root / rel
    assert dst.resolve().is_relative_to(root.resolve())
    if dst.exists():
        saved = backup / rel
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dst, saved)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(stage / rel, dst)
    assert digest(dst) == row['sha256'], rel
(work / 'integration-result.json').write_text(json.dumps({'status': 'PASS', 'files': changes, 'backup': str(backup)}, indent=2))
print('Integrated and hash-verified:', len(changes), flush=True)
