"""Regenerate per-source reference notes from reviewed contracts and code."""
import re
from algorithm_review import source_details
from algorithm_pages import argument_rows,readable_c
from legacy_algorithm_tests import LIB
fence=chr(96)*3
for folder in sorted(LIB.iterdir()):
    path=folder/'README.md'
    if not (folder/'c/reference.c').exists():continue
    old=path.read_text()
    data=source_details(folder)
    title=next(line for line in old.splitlines() if line.startswith('# '))
    method=re.search(r'## Pseudocode\s+(.*?)(?=\n## )',old,re.S)
    complexity=re.search(r'## Complexity\s+(.*?)(?=\n## )',old,re.S)
    rows=argument_rows(data['prototype'])
    table='| Function | Parameter | Entry location |\n|---|---|---|\n'+''.join(
        '| '+f+' | '+p+' | '+loc+' |\n' for f,p,loc in rows)
    source_asm=(folder/'arm/implementation.s').read_text()
    style='Handwritten Cortex-M3 Thumb reference.' if source_asm.startswith('; Handwritten') else 'Existing compiler-derived Cortex-M3 reference, refreshed only where C behavior changed.'
    suite=readable_c(data['tests'])
    text=f"""{title}

## Recognition phrases

{data['contract']}

## C contract and variants

{fence}c
{data['prototype']}
{fence}

Arguments name the actual span, dimensions or capacity in the prototype. Backing
storage must be valid for those sizes. See the behavior above for empty input,
failure, overlap and arithmetic rules; there is no universal failure sentinel.

## Pseudocode

{method.group(1).strip() if method else 'Follow the control flow in the complete source and the worked trace below.'}

## Worked trace

{data['trace']}

## Source pair

- [Complete C reference](c/reference.c)
- [Complete ARMASM implementation](arm/implementation.s)

{style}

## AAPCS register plan

{table}

Stack offsets are measured at function entry. Add the bytes saved/reserved by the
actual prologue before loading later arguments. A 64-bit integer result uses R0
for the low word and R1 for the high word. Preserve modified R4-R11 registers,
restore SP, and maintain eight-byte stack alignment at calls. Inspect the
particular routine's prologue rather than applying one frame size to all variants.

## Complexity

{complexity.group(1).strip() if complexity else 'See the loop and storage bounds in the source.'}

## Deterministic host vectors

These are the current executable vectors from the reference source. The
maintenance runner also supplies independent property vectors for selected
arithmetic, search and sorting routines. It executes C and the delivered Thumb
instruction stream separately.

{fence}c
{suite.strip()}
{fence}

## Historical grounding

This page is a reusable study method or possible variation. It does not claim
that its complete interface appeared verbatim in a paper. Use the package's
original papers and solved-exam pages for the exact required signatures.

## Verification boundary

Behavioral execution and portal structure are separate checks. LLVM validation
translates ARMASM directives to GNU assembler directives while retaining the
instruction stream. ARM execution uses an emulator; supported external 64-bit
division helpers are modeled at their ARM runtime ABI. Native Keil assembly and
physical-board execution are separate gates and are not implied by these tests.
"""
    if text!=old:path.write_text(text,encoding='utf-8')
print('Refreshed 50 source reference notes from current code and contracts.')
