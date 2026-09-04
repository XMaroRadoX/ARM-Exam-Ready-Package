from pathlib import Path
import shutil, hashlib, json
work=Path(__file__).resolve().parent
root=work.parents[1]
stage=work/'EXAM_HANDOFF'
assert not stage.exists(), 'Do not replace an existing stage'
baseline={}
def ignore(folder,names):
    return [n for n in names if n in {'.git','90_WORKING_PROJECTS','__pycache__','Objects','Listings','.search-qa','pattern-native-logs'}]
for name in ['START_HERE.html','README.md','01_EXAM_READY','02_ORIGINAL_MATERIALS','03_ADDITIONAL_STUDY_MATERIAL']:
    src=root/name; dst=stage/name
    if src.is_dir(): shutil.copytree(src,dst,ignore=ignore)
    else: dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
for p in stage.rglob('*'):
    if p.is_file(): baseline[p.relative_to(stage).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(work/'baseline.json').write_text(json.dumps(baseline,indent=2))
print('Staged',len(baseline),'files')
