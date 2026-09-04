"""Review or integrate only the reference's source, generated pages and reports."""
from pathlib import Path
import hashlib,json,shutil,sys,os,tempfile
WORK=Path(__file__).resolve().parent
ROOT=WORK.parents[1]
STAGE=WORK/'EXAM_HANDOFF'
MAINT='01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/'
PORTAL='01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/'
GLOSSARY='01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/ASM_INSTRUCTION_GLOSSARY.md'
SOURCES={'asm_reference.py','VERIFY_ASM_REFERENCE.py','BROWSER_ASM_REFERENCE.cjs','BUILD_STUDENT_PORTAL.py','VERIFY_STUDENT_PORTAL.py','VERIFY_PORTAL_PRESENTATION.py','VERIFY_WORKSTATION.py','PORTAL_MAINTENANCE.md',
 'portal_ui/asm_reference.css','portal_ui/asm_reference.js','ASM_REFERENCE_VALIDATION.json','ASM_REFERENCE_COVERAGE.json','ASM_REFERENCE_BROWSER_RESULTS.json',
 'STUDENT_PORTAL_VALIDATION.json','PORTAL_PRESENTATION_RESULTS.json','WORKSTATION_VALIDATION.json','WORKSTATION_CONTROLS_RESULTS.json','COURSE_COVERAGE.json','SEARCH_COVERAGE.json','SEARCH_DOCUMENT_CACHE.json'}
def allowed(r):return r in ('START_HERE.html',GLOSSARY) or r.startswith(PORTAL) or r.startswith(MAINT) and r[len(MAINT):] in SOURCES
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def guarded_write(source,target,expected):
 """Retain destination ACLs when Windows permits writing but denies replacement.

 An exclusive handle prevents a concurrent editor from writing between the
 content comparison and the update. Failure to obtain it leaves the file alone.
 """
 import ctypes,msvcrt
 api=ctypes.WinDLL('kernel32',use_last_error=True)
 api.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p]
 api.CreateFileW.restype=ctypes.c_void_p
 handle=api.CreateFileW(str(target),0xC0000000,0,None,3,0x80,None)
 if handle==ctypes.c_void_p(-1).value:raise ctypes.WinError(ctypes.get_last_error())
 fd=msvcrt.open_osfhandle(handle,os.O_RDWR|os.O_BINARY)
 with os.fdopen(fd,'r+b') as dest:
  if hashlib.sha256(dest.read()).hexdigest()!=expected:raise SystemExit('Concurrent content change; file left untouched: '+str(target))
  dest.seek(0);dest.write(source.read_bytes());dest.truncate();dest.flush();os.fsync(dest.fileno())
baseline=json.loads((WORK/'baseline.json').read_text())
previous=json.loads((WORK/'integration-review.json').read_text()) if '--resume' in sys.argv else {}
changes=[]
for p in STAGE.rglob('*'):
 if not p.is_file():continue
 r=p.relative_to(STAGE).as_posix()
 if not allowed(r):continue
 target=ROOT/r
 if target.exists() and sha(p)==sha(target):continue
 if (sha(target) if target.exists() else None)!=baseline.get(r):raise SystemExit('File changed since snapshot: '+r)
 changes.append((p,target,r))
# A regenerated firmware file must still match the original sources used in the
# checks; these protected files will never be copied by this integration.
firmware=[r for r in baseline if Path(r).suffix.lower() in ('.c','.h','.s','.uvprojx','.uvoptx') and '/.algorithm-tests/' not in r and '/.test-deps/' not in r]
drift=[r for r in firmware if not (STAGE/r).exists() or sha(STAGE/r)!=baseline[r] or sha(ROOT/r)!=baseline[r]]
if drift:raise SystemExit('Protected source mismatch: '+json.dumps(drift))
report={'changedFiles':len(changes),'protectedFirmwareFiles':len(firmware),'protectedFirmwareChanges':drift,'files':[r for _,_,r in changes]}
if previous:
 report['files']=sorted(set(previous['files'])|set(report['files']));report['changedFiles']=len(report['files'])
(WORK/'integration-review.json').write_text(json.dumps(report,indent=2))
if '--apply' in sys.argv:
 for name in ('ASM_REFERENCE_VALIDATION.json','ASM_REFERENCE_BROWSER_RESULTS.json','PORTAL_PRESENTATION_RESULTS.json','WORKSTATION_VALIDATION.json'):
  data=json.loads((STAGE/MAINT/name).read_text())
  if name.startswith('ASM_REFERENCE_BROWSER'):
   assert data['status']=='PASS'
  elif name=='PORTAL_PRESENTATION_RESULTS.json':assert not data['issues']
  elif name=='WORKSTATION_VALIDATION.json':assert not data['errors'] and all(v['status']=='PASS' for v in data['hostSyntaxWithActualHeaders'])
  else:assert data['execution']=='PASS' and not(data['compilationErrors'] or data['structuralErrors'] or data['coverageUnresolved'])
 backup=WORK/'backup'
 if backup.exists() and '--resume' not in sys.argv:raise SystemExit('Backup already exists; inspect before explicit resume')
 backup.mkdir(exist_ok='--resume' in sys.argv)
 # New routes/assets land before navigation starts referring to them.
 for source,target,r in sorted(changes,key=lambda row:row[1].exists()):
  expected=baseline.get(r)
  if (sha(target) if target.exists() else None)!=expected:
   raise SystemExit('Concurrent edit detected immediately before integration: '+r)
  if target.exists():
   old=backup/r;old.parent.mkdir(parents=True,exist_ok=True)
   if old.exists():assert sha(old)==expected,'Backup does not match starting content: '+r
   else:shutil.copy2(target,old)
  target.parent.mkdir(parents=True,exist_ok=True)
  fd,temporary=tempfile.mkstemp(prefix='.asm-reference-',suffix='.tmp',dir=target.parent);os.close(fd)
  temporary=Path(temporary)
  try:
   shutil.copy2(source,temporary)
   if (sha(target) if target.exists() else None)!=expected:
    raise SystemExit('Concurrent edit detected; preserving latest file: '+r)
   try:os.replace(temporary,target)
   except PermissionError:
    if os.name!='nt' or expected is None:raise
    guarded_write(source,target,expected)
  finally:
   if temporary.exists():temporary.unlink()
 for r in report['files']:assert sha(STAGE/r)==sha(ROOT/r),r
 assert all(sha(ROOT/r)==baseline[r] for r in firmware)
 report['status']='INTEGRATED'
 (WORK/'integration-result.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
