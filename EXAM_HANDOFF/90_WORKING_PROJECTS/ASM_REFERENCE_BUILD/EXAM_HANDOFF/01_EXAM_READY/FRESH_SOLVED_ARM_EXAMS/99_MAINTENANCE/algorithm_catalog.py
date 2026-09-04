"""Handwritten exam routines and their executable example contracts.

Each entry carries C, ARMASM, and an independent C test fixture. Sources are
published by BUILD_STUDENT_PORTAL; this module is the maintained source.
"""
from __future__ import annotations

ENTRIES = []
HEADERS = '#include <stdint.h>\n#include <stddef.h>\n#include <limits.h>\n'

def add(slug, title, family, prototype, contract, method, trace, c, asm, test,
        complexity='O(n) time; O(1) auxiliary storage', helpers='', registers=''):
    name = prototype.split('(')[0].split()[-1].lstrip('*')
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
        registers=registers or 'Parameters follow the prototype: R0–R3 hold the first four words; later words arrive on the caller stack. The comments identify saved working registers. R0 returns a word, or R0:R1 a 64-bit integer.',
        test=HEADERS+prototype+';\nint test_main(void) {\n'+test+'\nreturn 0;\n}\n'))

# A test returns its source line on a failed mathematical assertion.
CHECK = '#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)\n'
