from pathlib import Path
import random
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEMPLATE = ROOT / '01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API'
BIN = Path.home() / 'AppData/Local/Keil_v5/ARM/ARMCLANG/bin'
DEVICE = Path.home() / 'AppData/Local/Arm/Packs/Keil/LPC1700_DFP/2.7.2/Device/Include'
OUT = HERE / 'build'
OUT.mkdir(exist_ok=True)

def run(args):
    result = subprocess.run([str(x) for x in args], capture_output=True, text=True)
    if result.stdout or result.stderr:
        print(result.stdout + result.stderr)
    result.check_returncode()

target = next(t for t in ET.parse(TEMPLATE / 'sample.uvprojx').findall('.//Target')
              if t.findtext('TargetName') == 'SW_Debug')
inc = [TEMPLATE / p.replace('\\', '/') for p in
       target.findtext('.//Cads/VariousControls/IncludePath').split(';') if p]
inc.append(DEVICE)
cf = ['--target=arm-arm-none-eabi', '-mcpu=cortex-m3', '-mthumb', '-std=c90',
      '-O1', '-c', '-DLPC175x_6x', '-DSIMULATOR', '-fshort-enums', '-fshort-wchar', '-funsigned-char']
af = ['--cpu', 'Cortex-M3', '--diag_suppress=A1950W']
for directory in inc:
    cf += ['-I', str(directory)]
    af += ['-I', str(directory)]
common = []
def compile_file(source, name):
    asm = source.suffix.lower() == '.s'
    obj = OUT / (name + '.o')
    run([BIN / ('armasm.exe' if asm else 'armclang.exe'), *(af if asm else cf), source, '-o', obj])
    return obj

for index, f in enumerate(target.findall('.//Files/File')):
    if f.findtext('FileType') not in ('1', '2'):
        continue
    source = TEMPLATE / f.findtext('FilePath').replace('\\', '/')
    if source.name in ('sample.c', 'IRQ_button.c', 'IRQ_systick.c'):
        continue
    common.append(compile_file(source, 'common_' + str(index)))
common.append(compile_file(HERE / 'transpose.s', 'transpose'))
for question in ('Q1', 'Q2'):
    objects = common + [compile_file(HERE / (question + '_main.c'), question)]
    if question == 'Q1':
        objects += [compile_file(TEMPLATE / 'Source/button_EXINT/IRQ_button.c', 'default_buttons'),
                    compile_file(TEMPLATE / 'Source/systick/IRQ_systick.c', 'default_systick')]
    run([BIN / 'armlink.exe', '--cpu', 'Cortex-M3', *objects,
         '--strict', '--scatter', TEMPLATE / 'sample.sct', '--info', 'summarysizes',
         '-o', OUT / (question + '.axf')])
    print(question + ': native compile and link PASS')

# Algorithm checks: an instruction-level model of the assembly loops,
# compared with an independently expressed mathematical transpose.
# This does not execute the assembled machine code or emulate the board.
def model(a):
    out = [0] * 8
    for i in range(8):
        x = a[i]
        for j in range(8):
            if x & (0x80 >> j):
                out[j] |= 0x80 >> i
    return out

def reference(a):
    return [sum(((a[i] >> (7-j)) & 1) << (7-i) for i in range(8)) for j in range(8)]

def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]

sample = [0xF8, 0x7C, 0x3E, 0x1F, 0x8F, 0xC7, 0xE3, 0xF1]
expected = [0x8F, 0xC7, 0xE3, 0xF1, 0xF8, 0x7C, 0x3E, 0x1F]
assert model(sample) == expected
for i in range(8):
    for j in range(8):
        a = [0] * 8
        a[i] = 0x80 >> j
        expected_single = [0] * 8
        expected_single[j] = 0x80 >> i
        assert model(a) == expected_single
rng = random.Random(20250129)
for _ in range(1000):
    a = [rng.randrange(256) for _ in range(8)]
    b = [rng.randrange(256) for _ in range(8)]
    assert model(a) == reference(a)
    assert model(model(a)) == a
    assert model(xor(a, b)) == xor(model(a), model(b))
print('Algorithm model: paper example, 64 one-bit cases, 1000 random pairs PASS')
print('Physical board and machine-code execution: NOT TESTED')
