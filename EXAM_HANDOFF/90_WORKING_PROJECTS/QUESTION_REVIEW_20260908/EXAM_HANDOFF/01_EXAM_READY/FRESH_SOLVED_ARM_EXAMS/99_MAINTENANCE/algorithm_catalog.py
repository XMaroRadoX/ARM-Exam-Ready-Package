"""Handwritten exam routines and their executable example contracts.

Each entry carries C, ARMASM, and an independent C test fixture. Sources are
published by BUILD_STUDENT_PORTAL; this module is the maintained source.
"""
from __future__ import annotations

ENTRIES = []
HEADERS = '#include <stdint.h>\n#include <stddef.h>\n#include <limits.h>\n'

FUNDAMENTAL_MISTAKES = {
    'Count and measure': [
        'Dereferencing the data pointer before handling the documented empty-input case.',
        'Using a result or accumulator width that is too small for the stated range.',
        'Writing the output before every pointer, count and overflow condition has been validated.',
    ],
    'Compare and test': [
        'Using unsigned comparisons where the prompt requires signed ordering.',
        'Returning the last match or difference when the contract requires the first one.',
        'Reading one element beyond the supplied count while checking a neighbour or prefix.',
    ],
    'Copy and move': [
        'Starting to write before capacity, index and overlap rules have been checked.',
        'Copying in the wrong direction when source and destination overlap.',
        'Forgetting that a failed routine must leave the destination unchanged.',
    ],
    'Search': [
        'Returning a later valid answer instead of the deterministic first answer.',
        'Adding signed values in 32 bits when the pair sum can overflow.',
        'Changing output indexes while searching and then returning failure.',
    ],
    'Transform': [
        'Losing the original order when the prompt explicitly requires a stable transform.',
        'Moving one element too far and reading or writing outside the array.',
        'Modifying the array before every fallible precondition has passed.',
    ],
    'Strings': [
        'Scanning beyond capacity when no NUL terminator is present.',
        'Forgetting that required capacity includes the final NUL byte.',
        'Applying ASCII case rules to punctuation or bytes outside A through Z and a through z.',
    ],
    'Arithmetic': [
        'Performing signed overflow first and trying to detect it afterward.',
        'Forgetting that signed division truncates toward zero.',
        'Writing an output before division-by-zero, range or overflow checks are complete.',
    ],
    'Bits and bytes': [
        'Allowing a bit index outside 0 through 31 or shifting by a full word width.',
        'Using signed shifts when the task is defined on a uint32_t bit pattern.',
        'Packing bytes in the opposite order from the stated most-significant-byte-first contract.',
    ],
    'Matrices': [
        'Using row times rows plus column instead of row times columns plus column.',
        'Ignoring zero dimensions, rectangular shapes or a selected row or column bound.',
        'Partially modifying the output before a capacity or arithmetic preflight has passed.',
    ],
}

def add(slug, title, family, prototype, contract, method, trace, c, asm, test,
        complexity='O(n) time; O(1) auxiliary storage', helpers='', registers='',
        fundamentals_group=''):
    name = prototype.split('(')[0].split()[-1].lstrip('*')
    exam_question = ''
    mistakes = []
    if fundamentals_group:
        exam_question = (f'Write a C function and matching ARMASM subroutine named {name} '
                         f'to {title.lower()}. Use the exact interface below, obey the stated '
                         'failure behaviour, and preserve the AAPCS register and stack rules.')
        mistakes = FUNDAMENTAL_MISTAKES[fundamentals_group]
    # Instruction bodies below are authored directly, not compiled from C.
    def layout(body):
        return '\n'.join(part.strip()[:-1] if part.strip().endswith(':') else '        '+part.strip()
                         for line in body.splitlines() for part in line.split(' | ') if part.strip())
    assembly = ('; ' + title + '\n; ' + prototype.replace('\n', '\n; ') + '\n; ' + contract + '\n'
                '        AREA |.text.exam|, CODE, READONLY\n'
                '        THUMB\n        PRESERVE8\n        EXPORT ' + name + '\n'
                + name + '\n' + layout(asm) + '\n' + layout(helpers) + '\n        ALIGN\n        END\n')
    ENTRIES.append(dict(slug=slug,title=title,family=family,summary=contract,
        recognition=method,method=method,procedure=method,complexity=complexity,
        history='Possible variation',questions=[],code=HEADERS+c.strip()+'\n',
        assembly=assembly,prototype=prototype,contract=contract,trace=trace,
        fundamentals_group=fundamentals_group,
        exam_question=exam_question,mistakes=mistakes,
        registers=registers or 'Parameters follow the prototype: R0–R3 hold the first four words; later words arrive on the caller stack. The comments identify saved working registers. R0 returns a word, or R0:R1 a 64-bit integer.',
        test=HEADERS+prototype+';\nint test_main(void) {\n'+test+'\nreturn 0;\n}\n'))

# A test returns its source line on a failed mathematical assertion.
CHECK = '#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)\n'
