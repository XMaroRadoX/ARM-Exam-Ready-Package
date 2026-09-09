"""Native project builds and execution checks. No physical-board claim.

Run: python validation/verify.py --compiler-bin PATH --device-include PATH
Optional --test-deps PATH points to installed pyelftools and Unicorn packages.
"""
from pathlib import Path
import argparse
import json
import math
import os
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ap = argparse.ArgumentParser()
local = Path(os.environ.get('LOCALAPPDATA', '.'))
ap.add_argument('--compiler-bin', type=Path, default=local/'Keil_v5/ARM/ARMCLANG/bin')
ap.add_argument('--device-include', type=Path, default=local/'Arm/Packs/Keil/LPC1700_DFP/2.7.2/Device/Include')
ap.add_argument('--test-deps', type=Path)
ap.add_argument('--build-only', action='store_true')
ap.add_argument('--test-only', action='store_true')
args = ap.parse_args()
if args.test_deps:
    sys.path.insert(0, str(args.test_deps.resolve()))

def run(command):
    p = subprocess.run(list(map(str, command)), cwd=ROOT, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stdout + p.stderr)
    return p.stdout + p.stderr

builds = []
for project_name in ([] if args.test_only else ['Q1_Assembly', 'Q2_Timer_LEDs']):
    folder = ROOT/project_name
    tree = ET.parse(folder/'sample.uvprojx')
    for target in tree.findall('.//Target'):
        name = target.findtext('TargetName')
        mode = 'debug' if name == 'SW_Debug' else 'release'
        output = folder/'Objects'/mode
        output.mkdir(exist_ok=True)
        inc = target.findtext('.//Cads/VariousControls/IncludePath')
        includes = [folder/p.replace('\\', '/') for p in inc.split(';') if p]
        includes.append(args.device_include)
        cf = ['-xc', '-std=c90', '--target=arm-arm-none-eabi', '-mcpu=cortex-m3',
              '-c', '-fno-rtti', '-funsigned-char', '-fshort-enums', '-fshort-wchar',
              '-D__EVAL', '-gdwarf-4', '-O1', '-fno-function-sections',
              '-D__UVISION_VERSION=541', '-DLPC175x_6x']
        if mode == 'debug':
            cf.append('-DSIMULATOR')
        af = ['--cpu', 'Cortex-M3', '--pd', '__EVAL SETA 1', '-g',
              '--diag_suppress=A1950W', '--pd', '__UVISION_VERSION SETA 541',
              '--pd', 'LPC175x_6x SETA 1']
        objects, messages = [], []
        for i, entry in enumerate(target.findall('.//Files/File')):
            if entry.findtext('FileType') not in ('1', '2'):
                continue
            source = folder/entry.findtext('FilePath').replace('\\', '/')
            obj = output/(source.stem+'.o')
            assembly = source.suffix.lower() == '.s'
            command = [args.compiler_bin/('armasm.exe' if assembly else 'armclang.exe')]
            command += af if assembly else cf
            for include in includes:
                command += ['-I', include]
            messages.append(run(command+[source, '-o', obj]))
            objects.append(obj)
        image = output/'sample.axf'
        messages.append(run([args.compiler_bin/'armlink.exe', '--cpu', 'Cortex-M3',
            *objects, '--strict', '--scatter', folder/'sample.sct',
            '--summary_stderr', '--info', 'summarysizes', '--map', '--symbols',
            '--list', folder/'Listings'/f'{mode}.map', '-o', image]))
        log = '\n'.join(messages)
        (HERE/f'{project_name}_{mode}.log').write_text(log)
        assert 'warning:' not in log.lower() and 'error:' not in log.lower(), log
        builds.append({'project':project_name, 'target':name, 'result':'PASS',
                       'source_files':len(objects), 'warnings':0})
        print('Native build PASS:', project_name, name, flush=True)

if not args.test_only:
    (HERE/'build_results.json').write_text(json.dumps(builds, indent=2)+'\n')
else:
    builds = json.loads((HERE/'build_results.json').read_text())
if args.build_only:
    raise SystemExit(0)
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_MODE_MCLASS, UC_HOOK_CODE
from unicorn.arm_const import *

def aliquot(n):
    if n < 2:
        return 0
    return 1 + sum(a+(n//a if a != n//a else 0)
                   for a in range(2, math.isqrt(n)+1) if n % a == 0)

def reference(n):
    if n < 2:
        return 0, []
    current, terms = n, []
    for count in range(1, 9):
        current = aliquot(current)
        terms.append(current)
        if current == n:
            return count, terms
        if current <= 1:
            break
    return 0, terms

uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB | UC_MODE_MCLASS)
for base, size in [(0, 0x80000), (0x10000000, 0x10000), (0x2007C000, 0x10000)]:
    uc.mem_map(base, size)
with (ROOT/'Q2_Timer_LEDs/Objects/debug/sample.axf').open('rb') as f:
    elf = ELFFile(f)
    for segment in elf.iter_segments():
        if segment['p_type'] == 'PT_LOAD' and segment['p_memsz']:
            uc.mem_write(segment['p_vaddr'], segment.data())
    symbols = {s.name:s['st_value'] for s in elf.get_section_by_name('.symtab').iter_symbols()}
STOP, STACK = 0x70000, 0x1000F000
saved = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
         UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
def call(name, value=0):
    uc.reg_write(UC_ARM_REG_SP, STACK)
    uc.reg_write(UC_ARM_REG_LR, STOP|1)
    uc.reg_write(UC_ARM_REG_R0, value)
    for i, reg in enumerate(saved):
        uc.reg_write(reg, 0x12340000+i)
    uc.emu_start(symbols[name]|1, STOP, count=150000000)
    assert uc.reg_read(UC_ARM_REG_PC) == STOP, 'Instruction limit reached'
    assert uc.reg_read(UC_ARM_REG_SP) == STACK
    for i, reg in enumerate(saved):
        assert uc.reg_read(reg) == 0x12340000+i, 'Callee-saved register damaged'
    return uc.reg_read(UC_ARM_REG_R0)

for n in range(101):
    assert call('aliquotSum', n) == aliquot(n), n
numbers = [8128, 5564, 5400, 14264, 1305184, 1598470, 4938136]
cases = [0, 1, 2, 3, 4, 6, 12, 16, 25, 28, 97, 100, 220, 284, 496, 12496] + numbers
traces = []
for n in cases:
    expected, terms = reference(n)
    assert call('isSociable', n) == expected, n
    traces.append({'input':n, 'result':expected, 'terms':terms})
print('Native ARM instructions PASS: aliquot sums, sociable cases, register/stack preservation', flush=True)

def hook_return(value):
    uc.reg_write(UC_ARM_REG_R0, value)
    uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

# Test exact boundary precedence with a controlled aliquotSum dependency.
boundary_calls = []
def fake_sum(uc, address, size, data):
    assert uc.reg_read(UC_ARM_REG_SP) % 8 == 0
    boundary_calls.append(uc.reg_read(UC_ARM_REG_R0))
    hook_return(next(fake_values))
addr = symbols['aliquotSum'] & ~1
hook = uc.hook_add(UC_HOOK_CODE, fake_sum, begin=addr, end=addr)
uc.ctl_remove_cache(0, 0x80000)
boundaries = [([11,12,13,14,15,16,17,10], 8),
              ([11,12,13,14,15,16,17,18], 0), ([1], 0)]
for values, expected in boundaries:
    fake_values = iter(values)
    boundary_calls.clear()
    actual = call('isSociable', 10)
    assert actual == expected, (values, actual, expected, boundary_calls)
    assert len(boundary_calls) == len(values)
uc.hook_del(hook)
uc.ctl_remove_cache(0, 0x80000)

state = {'pending':1, 'mask':0, 'acks':0}
def ack(uc, address, size, data):
    assert uc.reg_read(UC_ARM_REG_R0) == 1
    state['acks'] += 1
    hook_return(state['pending'])
def one_hot(uc, address, size, data):
    label = uc.reg_read(UC_ARM_REG_R0)
    assert 4 <= label <= 11
    state['mask'] = 1 << (11-label)
    hook_return(0)
def clear(uc, address, size, data):
    state['mask'] = 0
    hook_return(0)
for name, callback in [('exam_timer_ack', ack), ('exam_led_one_hot', one_hot), ('exam_led_clear', clear)]:
    addr = symbols[name] & ~1
    uc.hook_add(UC_HOOK_CODE, callback, begin=addr, end=addr)
uc.ctl_remove_cache(0, 0x80000)
read_word = lambda name: struct.unpack('<I', uc.mem_read(symbols[name], 4))[0]
irq_rows = []
for i in range(14):
    call('TIMER1_IRQHandler')
    expected, _ = reference(numbers[i % 7])
    mask = (1 << (8-expected)) if expected else 0
    assert read_word('last_input') == numbers[i % 7]
    assert read_word('last_result') == expected
    assert read_word('interrupt_count') == i+1
    assert state['mask'] == mask
    irq_rows.append({'interrupt':i+1, 'input':numbers[i % 7], 'result':expected, 'mask':mask})
state['pending'] = 2
call('TIMER1_IRQHandler')
assert read_word('interrupt_count') == 14
assert state['acks'] == 15
state['pending'] = 1
# Exercise every display value, including labels absent from the exam array.
addr = symbols['isSociable'] & ~1
hook = uc.hook_add(UC_HOOK_CODE, lambda u,a,s,d:hook_return(forced), begin=addr, end=addr)
uc.ctl_remove_cache(0, 0x80000)
for forced in range(9):
    state['mask'] = 255
    call('TIMER1_IRQHandler')
    assert state['mask'] == (1 << (8-forced) if forced else 0)
uc.hook_del(hook)
print('Compiled Timer 1 handler PASS: 14 real inputs, wraparound, MR0 guard, all LED results', flush=True)
report = {'native_builds':builds, 'aliquot_cases':101, 'sociable_cases':traces,
          'boundary_cases':3, 'irq_rows':irq_rows, 'all_display_values':'0..8 PASS',
          'abi':'R4-R11 and SP preserved; nested-call stack aligned',
          'execution':'Native Arm-compiled code executed in Unicorn; peripheral API calls mocked for IRQ tests',
          'limits':'No physical board, real interrupt entry, or wall-clock timing validation'}
(HERE/'results.json').write_text(json.dumps(report, indent=2)+'\n')
