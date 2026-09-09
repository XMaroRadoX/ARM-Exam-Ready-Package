"""Fail unless pattern pages, downloadable sources, projects and verification agree."""
from pathlib import Path
import hashlib,html,json,re
import BUILD_STUDENT_PORTAL as b
from pattern_runnable import HERE,ROOT,OUT,all_specs,write_project,algorithm_entries
from pattern_teaching import PATTERNS
from canonical_api_reference import API_DOCS
from VERIFY_COMBINED_SOLUTIONS import BANNED_TOKENS

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 issues=[];checks=0
 def check(ok,message):
  nonlocal checks
  checks+=1
  if not ok:issues.append(message)
 coverage=json.loads((HERE/'PATTERN_COVERAGE.json').read_text())
 check({r['title'] for r in coverage}==set(PATTERNS),'Pattern coverage differs from maintained titles')
 specs=all_specs();projects={p['id']:p for row in coverage for p in row['projects']}
 native=json.loads((HERE/'PATTERN_NATIVE_BUILDS.json').read_text())['projects']
 algorithms={r['slug']:r for r in json.loads((HERE/'PATTERN_ALGORITHM_RESULTS.json').read_text())['results']}
 flows={r['project']:r for r in json.loads((HERE/'PATTERN_FLOW_RESULTS.json').read_text())['results']}
 api={str(r['title']) for r in b.parse_api()}
 check(api==set(API_DOCS),'Header and API documentation disagree')
 pages={p.stem.replace('-','_') for p in (b.PORTAL/'api').glob('exam-*.html')}
 check(pages==api,'Generated API pages differ from declarations')
 used_api=set();source_files=0
 for key,p in projects.items():
  folder=ROOT/p['path']
  try:write_project(key,specs[key],b.clean_algorithm_code,reuse=True)
  except (ValueError,FileNotFoundError) as e:check(False,str(e))
  check((folder/'README.md').exists(),key+': missing replacement instructions')
  for doc in ['EXAM_API_QUICK_REFERENCE.md','API_GAP_REPORT.md']:
   check((folder/doc).read_bytes()==(b.TEMPLATE_REFERENCE/doc).read_bytes(),key+': copied API reference is stale '+doc)
  current={str(f.relative_to(folder)):sha(f) for f in [folder/'sample.uvprojx',*sorted((folder/'Source').rglob('*'))] if f.is_file()}
  n=native.get(key,{})
  check(n.get('status')=='PASS' and n.get('sources')==current,key+': native build absent, failed or stale')
  if specs[key].get('entry'):
   entry=specs[key]['entry'];r=algorithms.get(entry['slug'],{})
   check(r.get('status')=='C_AND_THUMB_EXECUTION_PASS',key+': missing C/Thumb execution')
   check(r.get('c_sha256')==hashlib.sha256(entry['code'].encode()).hexdigest(),key+': tested C reference differs')
   check(r.get('assembly_sha256')==hashlib.sha256(entry['assembly'].encode()).hexdigest(),key+': tested assembly differs')
  else:check(flows.get(key,{}).get('status')=='PASS',key+': missing behavioural scenario')
  for name,expected in p['files'].items():
   f=folder/name;source_files+=1;check(sha(f)==expected,key+': coverage hash differs '+name)
   text=f.read_text(encoding='utf-8')
   used_api.update(re.findall(r'\b(exam_\w+)\s*\(',text))
   for token in BANNED_TOKENS:
    check(not re.search(r'\b'+re.escape(token)+r'\b',text),key+': obsolete interface '+token)
   check(not re.search(r'\b(?:TODO|FIXME|IMPLEMENT_ME)\b',text),key+': unfinished source '+name)
 for folder in (OUT.parent/'course-projects').iterdir():
  if not (folder/'sample.uvprojx').is_file():continue
  current={str(f.relative_to(folder)):sha(f) for f in [folder/'sample.uvprojx',*sorted((folder/'Source').rglob('*'))] if f.is_file()}
  check(native.get(folder.name,{}).get('status')=='PASS' and native[folder.name].get('sources')==current,folder.name+': native course build absent or stale')
 for row in coverage:
  destinations=json.loads((HERE/'SECTION_DESTINATIONS.json').read_text())
  page=b.PORTAL/destinations[row['title']]['route']
  text=page.read_text(encoding='utf-8')
  listings=[html.unescape(re.sub(r'<[^>]+>','',x)).strip() for x in re.findall(r'<code\b[^>]*>(.*?)</code>',text,re.S)]
  check('data-runnable-pattern' in text,row['title']+': missing runnable section')
  for p in row['projects']:
   for name in p['files']:
    code=(ROOT/p['path']/name).read_text(encoding='utf-8').strip()
    check(code in listings,row['title']+': displayed source differs '+p['id']+'/'+name)
 helpers={'exam_timer_config_match','exam_timer_set_prescaler','exam_timer_set_clock_divider','exam_timer_match_happened','exam_timer_capture_happened','exam_joystick_released_edges'}
 check(helpers<=used_api,'A new helper is absent from complete examples')
 check(used_api<=api,'Examples call undeclared API functions: '+str(used_api-api))
 # Scan active recipes as well, including obsolete names without exam_ prefixes.
 recipe=ROOT/'03_ADDITIONAL_STUDY_MATERIAL/02 - Code Recipes'
 for f in recipe.rglob('*'):
  if f.suffix.lower() not in ('.c','.s'):continue
  text=f.read_text(encoding='utf-8')
  for token in BANNED_TOKENS:
   check(not re.search(r'\b'+re.escape(token)+r'\b',text),str(f.relative_to(ROOT))+': obsolete '+token)
 report=dict(status='PASS' if not issues else 'FAIL',patterns=len(coverage),projects=len(projects),sourceFiles=source_files,apiFunctions=len(api),checks=checks,issues=issues,physicalBoard='Not tested')
 (HERE/'PATTERN_COVERAGE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2));return bool(issues)
if __name__=='__main__':raise SystemExit(main())
