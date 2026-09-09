from pathlib import Path
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROJECT = HERE.parent / 'WLAD_ELHALAL_SPEAKER'
BIN = Path.home() / 'AppData/Local/Keil_v5/ARM/ARMCLANG/bin'
DEVICE = Path.home() / 'AppData/Local/Arm/Packs/Keil/LPC1700_DFP/2.7.2/Device/Include'

def run(args, logs):
    result = subprocess.run(list(map(str, args)), cwd=PROJECT, capture_output=True, text=True, timeout=120)
    logs.append(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)

report = {}
for target in ET.parse(PROJECT / 'sample.uvprojx').findall('.//Target'):
    name = target.findtext('TargetName')
    simulator = name == 'SW_Debug'
    label = 'simulator' if simulator else 'board'
    out = PROJECT / 'Objects' / label
    out.mkdir(exist_ok=True)
    logs = []
    cf = ['-xc','-std=c90','--target=arm-arm-none-eabi','-mcpu=cortex-m3','-c',
          '-fno-rtti','-funsigned-char','-fshort-enums','-fshort-wchar','-D__EVAL',
          '-gdwarf-4','-O1','-fno-function-sections','-D__UVISION_VERSION=541','-DLPC175x_6x']
    if simulator:
        cf.append('-DSIMULATOR')
    af = ['--cpu','Cortex-M3','--pd','__EVAL SETA 1','-g','--diag_suppress=A1950W',
          '--pd','__UVISION_VERSION SETA 541','--pd','LPC175x_6x SETA 1']
    includes = [PROJECT / p.replace('\\','/') for p in target.findtext('.//Cads/VariousControls/IncludePath').split(';') if p]
    includes.append(DEVICE)
    objects = []
    try:
        for i, file in enumerate(target.findall('.//Files/File')):
            if file.findtext('FileType') not in ('1','2'):
                continue
            source = PROJECT / file.findtext('FilePath').replace('\\','/')
            obj = out / ('%02d_%s.o' % (i, source.stem))
            asm = source.suffix.lower() == '.s'
            args = [BIN / ('armasm.exe' if asm else 'armclang.exe'), *(af if asm else cf)]
            for inc in includes:
                args += ['-I', inc]
            run(args + [source, '-o', obj], logs)
            objects.append(obj)
        axf = out / 'speaker.axf'
        run([BIN/'armlink.exe','--cpu','Cortex-M3',*objects,'--strict','--scatter',PROJECT/'sample.sct',
             '--summary_stderr','--info','summarysizes','--map','--symbols','--list',
             PROJECT/'Listings'/('speaker_'+label+'.map'),'-o',axf], logs)
        run([BIN/'fromelf.exe','--i32combined','--output',out/'speaker.hex',axf], logs)
        report[label] = dict(status='PASS',source_count=len(objects),
            image_sha256=hashlib.sha256(axf.read_bytes()).hexdigest(),
            image=str(axf.relative_to(PROJECT)))
        print(label + ': compile and link PASS', flush=True)
    except Exception as error:
        report[label] = dict(status='FAIL',error=str(error))
        print(label + ': FAIL: ' + str(error), flush=True)
    (PROJECT/'Listings'/('build_'+label+'.log')).write_text('\n'.join(logs))
(PROJECT/'BUILD_REPORT.json').write_text(json.dumps(dict(
    native_toolchain='Arm Compiler 6.22', targets=report,
    physical_board='Not tested', audio='6 seconds, 8 kHz mono IMA ADPCM',
    validation_scope='Native command-line compilation/linking; no flashing or debugger execution.'
), indent=2)+'\n')
raise SystemExit(0 if all(r['status']=='PASS' for r in report.values()) else 1)
