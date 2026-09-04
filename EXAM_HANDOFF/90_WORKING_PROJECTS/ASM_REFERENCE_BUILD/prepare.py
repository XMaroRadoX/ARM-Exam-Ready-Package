from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
STAGE=WORK/'EXAM_HANDOFF'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
if STAGE.exists(): raise SystemExit('Stage already exists')
baseline={}
for name in ('01_EXAM_READY','02_ORIGINAL_MATERIALS','03_ADDITIONAL_STUDY_MATERIAL','START_HERE.html','README.md'):
    source=ROOT/name
    paths=source.rglob('*') if source.is_dir() else [source]
    for p in paths:
        if not p.is_file() or any(x in p.parts for x in ('__pycache__','.git')):continue
        relative=p.relative_to(ROOT)
        baseline[relative.as_posix()]=sha(p)
        dest=STAGE/relative
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,dest)
# Link checks expect the working-project landing page, but personal projects stay out.
(STAGE/'90_WORKING_PROJECTS').mkdir()
shutil.copy2(ROOT/'90_WORKING_PROJECTS/README.md',STAGE/'90_WORKING_PROJECTS/README.md')
(WORK/'baseline.json').write_text(json.dumps(baseline,indent=2))
print('Isolated copy ready:',len(baseline),'files')
