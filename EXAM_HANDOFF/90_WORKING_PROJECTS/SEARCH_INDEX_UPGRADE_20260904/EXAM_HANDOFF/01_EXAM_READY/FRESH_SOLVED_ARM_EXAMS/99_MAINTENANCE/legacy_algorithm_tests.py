"""Load the existing unique sources and their embedded executable vectors."""
import re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
LIB=ROOT/'03_ADDITIONAL_STUDY_MATERIAL'/'02 - Code Recipes'/'11 - Maximum Algorithm Reference'

def declarations(code):
    # Keep complete typedefs; turn function definitions into prototypes.
    pattern=re.compile(r'(?m)^(?:static\s+)?(?:[A-Za-z_]\w*[\s*]+)+[A-Za-z_]\w*\s*\([^;{}]*\)\s*\{')
    while True:
        m=pattern.search(code)
        if not m:
            code=re.sub(r'(?m)^((?:const\s+)?uint32_t\s+pat_data_asm_objects_001_\w+(?:\[[^]]*\])?)\s*=\s*[^;]+;',r'extern \1;',code)
            code=re.sub(r'(?m)^uint32_t\s+(pat_data_asm_objects_001_workspace\[[^]]*\]);',r'extern uint32_t \1;',code)
            return code
        level=1;i=m.end()
        while level:
            if code[i]=='{': level+=1
            if code[i]=='}': level-=1
            i+=1
        proto=code[m.start():m.end()-1].strip()
        code=code[:m.start()]+proto+';'+code[i:]

def entries():
    result=[]
    for folder in sorted(LIB.iterdir()):
        path=folder/'c/reference.c'
        if not path.exists():continue
        raw=path.read_text(encoding='utf-8')
        code,sep,tests=raw.partition('#ifdef PATTERN_HOST_TEST')
        if not sep: raise ValueError('Missing executable tests: '+folder.name)
        tests=tests.rsplit('#endif',1)[0]
        tests=tests.replace('int main(void)', 'int test_main(void)')
        assembly=(folder/'arm/implementation.s').read_text(encoding='utf-8')
        result.append(dict(slug=folder.name.lower(),code=code,assembly=assembly,
            test=declarations(code)+'\n'+tests,source=path.as_posix()))
    return result
