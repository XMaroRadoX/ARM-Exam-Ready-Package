"""Publish the reviewed manifest with preflight hashes and recoverable backups."""
from pathlib import Path
import hashlib,json,os,shutil
ROOT=Path.cwd().resolve();WORK=ROOT/'90_WORKING_PROJECTS/QUESTION_REVIEW_20260908';STAGE=WORK/'EXAM_HANDOFF'
manifest=json.loads((WORK/'publish-candidates.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rank(x):
    p=x['path']
    return 3 if p.endswith('/assets/portal-data.js') else 2 if '/PORTAL/' in p else 1 if '/exam-solutions/' in p else 0
changes=sorted(manifest['files'],key=lambda x:(rank(x),x['path']))
for x in changes:
    target=(ROOT/x['path']).resolve();source=STAGE/x['path']
    assert target.is_relative_to(ROOT) and not any(t in target.parts for t in ['.git','.agents','.codex']),target
    assert sha(source)==x['after'],('staged file changed after inventory',source)
    assert (sha(target) if target.exists() else None)==x['before'],('original changed concurrently',target)
    assert not target.with_name(target.name+'.question-review-tmp').exists(),target
# Back up every existing destination before replacing the first one.
for x in changes:
    if x['before'] is None:continue
    backup=WORK/'before'/x['path'];backup.parent.mkdir(parents=True,exist_ok=True)
    if backup.exists():assert sha(backup)==x['before'],backup
    else:shutil.copy2(ROOT/x['path'],backup)
log=[]
for x in changes:
    target=ROOT/x['path'];target.parent.mkdir(parents=True,exist_ok=True)
    assert (sha(target) if target.exists() else None)==x['before'],('destination changed during publication',target)
    temp=target.with_name(target.name+'.question-review-tmp')
    shutil.copy2(STAGE/x['path'],temp);os.replace(temp,target)
    assert sha(target)==x['after'],target
    log.append(x)
    (WORK/'published.json').write_text(json.dumps({'files':log,'protectedFilesVerified':manifest['protectedFilesVerified']},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'publishedFiles':len(log),'backedUpFiles':sum(x['before'] is not None for x in changes),'backupDirectory':str(WORK/'before'),'protectedFilesVerified':manifest['protectedFilesVerified']}))
