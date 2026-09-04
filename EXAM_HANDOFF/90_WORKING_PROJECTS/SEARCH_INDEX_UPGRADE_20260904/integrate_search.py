"""Integrate the reviewed search change with content checks and exact-file backups."""
from pathlib import Path
import argparse,hashlib,json,shutil
TASK=Path(__file__).resolve().parent; ROOT=TASK.parents[1]; STAGE=TASK/'EXAM_HANDOFF'
MAINT='01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/'
PORTAL='01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/'
NAMES={'search_metadata.py','search_corpus.py','REFRESH_SEARCH.py','workstation_extensions.py','PORTAL_MAINTENANCE.md',
       'portal_ui/portal.js','portal_ui/portal_logic.js','portal_ui/asm_reference.js','VERIFY_SEARCH.cjs','VERIFY_SEARCH_COVERAGE.py',
       'BROWSER_SEARCH_QA.cjs','SEARCH_REGRESSION_RESULTS.json','SEARCH_INTEGRITY_RESULTS.json','SEARCH_BROWSER_RESULTS.json',
       'SEARCH_DOCUMENT_CACHE.json','SEARCH_COVERAGE.json','WORKSTATION_CONTROLS_RESULTS.json','PORTAL_PRESENTATION_RESULTS.json','WORKSTATION_VALIDATION.json'}
ASSETS={'portal-data.js','portal.js','portal_logic.js','asm_reference.js'}
def allowed(r):
 return r in {MAINT+n for n in NAMES} or (r.startswith(PORTAL) and (r.endswith('.html') or r[len(PORTAL):] in {'assets/'+n for n in ASSETS}))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
 baseline=json.loads((TASK/'baseline.json').read_text());changes={}
 for p in STAGE.rglob('*'):
  if p.is_file():
   r=p.relative_to(STAGE).as_posix()
   if allowed(r):
    desired=sha(p)
    if desired!=baseline.get(r):changes[r]=desired
 # Include original input checks, not just the files about to be replaced.
 drift=[]
 for r,expected in baseline.items():
  actual=sha(ROOT/r)
  if actual!=expected and actual!=changes.get(r):drift.append(r)
 for r,desired in changes.items():
  if r not in baseline and sha(ROOT/r) not in {None,desired}:drift.append(r)
 if drift:
  (TASK/'integration-conflicts.json').write_text(json.dumps(sorted(set(drift)),indent=2))
  raise SystemExit('Live changes require reconciliation: '+json.dumps(sorted(set(drift))))
 report={'status':'PREFLIGHT_PASS','files':[{'path':r,'before':baseline.get(r),'after':h} for r,h in sorted(changes.items())]}
 (TASK/'integration-plan.json').write_text(json.dumps(report,indent=2))
 print('Preflight passed:',len(changes),'reviewed files; all original inputs match.')
 if not args.apply:return
 backup=TASK/'backup';backup.mkdir(exist_ok=True);applied=[]
 try:
  for r,desired in sorted(changes.items()):
   dest=ROOT/r;actual=sha(dest)
   if actual==desired:applied.append(r);continue
   if actual!=baseline.get(r):raise RuntimeError('Destination changed during integration: '+r)
   if dest.exists():
    saved=backup/r;saved.parent.mkdir(parents=True,exist_ok=True)
    if saved.exists() and sha(saved)!=actual:raise RuntimeError('Backup does not match destination: '+r)
    if not saved.exists():shutil.copy2(dest,saved)
   # Check again after backup, immediately before replacing this exact file.
   if sha(dest)!=baseline.get(r):raise RuntimeError('Destination changed after backup: '+r)
   dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(STAGE/r,dest)
   if sha(dest)!=desired:raise RuntimeError('Copy verification failed: '+r)
   applied.append(r)
 finally:
  (TASK/'integration-progress.json').write_text(json.dumps({'applied':applied,'planned':len(changes)},indent=2))
 protected=[r for r in baseline if Path(r).suffix.lower() in {'.c','.h','.s','.uvprojx','.uvoptx'}]
 bad=[r for r in protected if sha(ROOT/r)!=baseline[r]]
 if bad:raise RuntimeError('Protected source changed: '+json.dumps(bad))
 report.update(status='PASS',applied=len(applied),protectedSourceFiles=len(protected),protectedSourceChanges=bad,backup='backup')
 (TASK/'integration-result.json').write_text(json.dumps(report,indent=2))
 print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
if __name__=='__main__':main()
