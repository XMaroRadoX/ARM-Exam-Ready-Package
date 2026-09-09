"""Native Keil builds and source-agreement checks for delivered pattern projects."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess, time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--uv4',type=Path,required=True);ap.add_argument('--resume',action='store_true');ap.add_argument('--board-only',action='store_true');args=ap.parse_args()
    coverage=json.loads((HERE/'PATTERN_COVERAGE.json').read_text())
    results_path=HERE/('PATTERN_BOARD_NATIVE_BUILDS.json' if args.board_only else 'PATTERN_NATIVE_BUILDS.json')
    prior=json.loads(results_path.read_text()).get('projects',{}) if args.resume and results_path.exists() else {}
    projects={p['id']:p for row in coverage for p in row['projects'] if not args.board_only or not p['id'].startswith('algorithm-')}
    if not args.board_only:
        course=ROOT/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/course-projects'
        for project in course.glob('*/sample.uvprojx'):
            projects[project.parent.name]=dict(id=project.parent.name,path=str(project.parent.relative_to(ROOT)))
    results={};logs=HERE/'pattern-native-logs';logs.mkdir(exist_ok=True)
    for i,(key,p) in enumerate(sorted(projects.items()),1):
        folder=ROOT/p['path'];project=folder/'sample.uvprojx'
        hashes={str(f.relative_to(folder)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [project,*sorted((folder/'Source').rglob('*'))] if f.is_file()}
        before=prior.get(key,{})
        if before.get('status')=='PASS' and before.get('sources')==hashes:
            results[key]=before;print(i,len(projects),key,'PASS (matching previous native build)',flush=True);continue
        log=logs/(key+'.log');si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
        started=time.monotonic()
        try:
            process=subprocess.run([str(args.uv4),'-b',str(project),'-t','SW_Debug','-o',str(log)],startupinfo=si,timeout=240)
            text=log.read_text(errors='replace') if log.exists() else ''
            match=re.search(r'(\d+) Error\(s\), (\d+) Warning\(s\)',text)
            passed=process.returncode in (0,1) and match is not None and int(match[1])==0 and (folder/'Objects/sample.axf').exists()
            result=dict(status='PASS' if passed else 'FAIL',exitCode=process.returncode,errors=int(match[1]) if match else None,warnings=int(match[2]) if match else None,seconds=round(time.monotonic()-started,1),sources=hashes,log=str(log.relative_to(ROOT)))
        except subprocess.TimeoutExpired:
            result=dict(status='FAIL',reason='Keil exceeded 240 seconds',sources=hashes,log=str(log.relative_to(ROOT)))
        results[key]=result
        results_path.write_text(json.dumps(dict(nativeToolchain='Keil uVision, native Arm Compiler, unchanged device-pack project settings',projects=results,physicalBoard='Not tested'),indent=2)+'\n')
        print(i,len(projects),key,result['status'],result.get('warnings'),flush=True)
        if result['status']=='FAIL':print(text[-2500:] if 'text' in locals() else result,flush=True)
    results_path.write_text(json.dumps(dict(nativeToolchain='Keil uVision, native Arm Compiler, unchanged device-pack project settings',projects=results,physicalBoard='Not tested'),indent=2)+'\n')
    return int(any(r['status']!='PASS' for r in results.values()))
if __name__=='__main__':raise SystemExit(main())
