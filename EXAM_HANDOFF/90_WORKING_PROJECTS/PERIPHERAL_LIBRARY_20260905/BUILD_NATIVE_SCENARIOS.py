"""Compile/link every complete SW_Debug project with the native Arm toolchain.

Identical objects may be reused only for matching source, header and flag hashes.
The flags are those recorded by the unchanged native uVision baseline.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,hashlib,json,subprocess,threading,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
BIN=Path('C:/Users/marwa/AppData/Local/Keil_v5/ARM/ARMCLANG/bin')
DEVICE=Path('C:/Users/marwa/AppData/Local/Arm/Packs/Keil/LPC1700_DFP/2.7.2/Device/Include')
CACHE=HERE/'.native-scenario-cache'
CF=['-xc','-std=c90','--target=arm-arm-none-eabi','-mcpu=cortex-m3','-c','-fno-rtti','-funsigned-char','-fshort-enums','-fshort-wchar','-D__EVAL','-gdwarf-4','-O1','-fno-function-sections','-D__UVISION_VERSION=541','-DLPC175x_6x','-DSIMULATOR']
AF=['--cpu','Cortex-M3','--pd','__EVAL SETA 1','-g','--diag_suppress=A1950W','--pd','__UVISION_VERSION SETA 541','--pd','LPC175x_6x SETA 1']
lock=threading.Lock();locks={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args,cwd):
    p=subprocess.run([str(a) for a in args],cwd=cwd,capture_output=True,text=True,timeout=120)
    if p.returncode:raise RuntimeError(' '.join(str(a) for a in args[:3])+'\n'+p.stdout+p.stderr)
    return p.stdout+p.stderr
def build(record,prior):
    folder=ROOT/record['path'];project=folder/'sample.uvprojx'
    hashes={str(p.relative_to(folder)):sha(p) for p in [project,folder/'sample.sct',*sorted((folder/'Source').rglob('*'))] if p.is_file()}
    if prior.get('status')=='PASS' and prior.get('sources')==hashes:return prior
    output=folder/'Objects';output.mkdir(exist_ok=True);(folder/'Listings').mkdir(exist_ok=True)
    target=next(t for t in ET.parse(project).findall('.//Target') if t.findtext('TargetName')=='SW_Debug')
    paths=[folder/f.findtext('FilePath').replace('\\','/') for f in target.findall('.//Files/File') if f.findtext('FileType') in ('1','2')]
    # Read includes from the actual target; add the resolved genuine device pack.
    include=target.findtext('.//Cads/VariousControls/IncludePath') or ''
    inc=[folder/p.replace('\\','/') for p in include.split(';') if p]
    if not inc:inc=[folder/'Source',*sorted(p for p in (folder/'Source').iterdir() if p.is_dir())]
    inc.append(DEVICE)
    headers=''.join(k+v for k,v in hashes.items() if k.endswith('.h'))
    objects=[];messages=[]
    try:
        for source in paths:
            asm=source.suffix.lower()=='.s';flags=AF if asm else CF
            digest=hashlib.sha256((sha(source)+headers+str(flags)+str(DEVICE)).encode()).hexdigest()
            obj=CACHE/(digest+'.o')
            with lock:guard=locks.setdefault(digest,threading.Lock())
            with guard:
                if not obj.exists():
                    args=[BIN/('armasm.exe' if asm else 'armclang.exe'),*flags]
                    for directory in inc:args+=['-I',directory]
                    args += [source,'-o',obj]
                    messages.append(run(args,folder))
            objects.append(obj)
        args=[BIN/'armlink.exe','--cpu','Cortex-M3',*objects,'--strict','--scatter',folder/'sample.sct','--summary_stderr','--info','summarysizes','--map','--symbols','--list',folder/'Listings/sample.map','-o',output/'sample.axf']
        messages.append(run(args,folder))
        result=dict(status='PASS',sources=hashes,objects=[p.name for p in objects],sourceCount=len(paths),imageSha256=sha(output/'sample.axf'))
    except Exception as e:result=dict(status='FAIL',sources=hashes,reason=str(e));messages.append(str(e))
    log=HERE/'scenario-native-logs'/(record['id']+'.log');log.parent.mkdir(exist_ok=True);log.write_text('\n'.join(messages),encoding='utf-8')
    result['log']=str(log.relative_to(ROOT));return result
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--only');args=ap.parse_args()
    CACHE.mkdir(exist_ok=True)
    records=json.loads((HERE/'SCENARIO_MANIFEST.json').read_text())
    if args.only:records=[r for r in records if r['id']==args.only]
    path=HERE/'SCENARIO_NATIVE_BUILDS.json';prior=json.loads(path.read_text()).get('projects',{}) if path.exists() else {};results=dict(prior)
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures={pool.submit(build,r,prior.get(r['id'],{})):r['id'] for r in records}
        for i,f in enumerate(as_completed(futures),1):
            key=futures[f]
            try:results[key]=f.result()
            except Exception as e:results[key]=dict(status='FAIL',reason=str(e))
            report=dict(nativeToolchain='Arm Compiler 6.22 native compiler, ARMASM and linker; complete SW_Debug project source lists; flags match the unchanged uVision baseline',devicePack=str(DEVICE),projects=results,physicalBoard='Not tested')
            path.write_text(json.dumps(report,indent=2)+'\n')
            print(i,len(records),key,results[key]['status'],flush=True)
    return int(any(results[r['id']]['status']!='PASS' for r in records))
if __name__=='__main__':raise SystemExit(main())
