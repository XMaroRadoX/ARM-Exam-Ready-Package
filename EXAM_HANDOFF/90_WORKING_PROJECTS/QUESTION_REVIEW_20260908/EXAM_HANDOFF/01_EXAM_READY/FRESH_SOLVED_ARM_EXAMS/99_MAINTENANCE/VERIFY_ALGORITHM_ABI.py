"""Audit execution coverage and ABI at every public function call."""
import json,re
from concurrent.futures import ThreadPoolExecutor
from VERIFY_ALGORITHMS import HERE,BUILD,emulate
from algorithm_catalog import ENTRIES
import exam_algorithms_numeric,exam_algorithms_arrays,exam_algorithms_strings,exam_algorithms_matrices
import exam_algorithms_fundamentals_arrays
import exam_algorithms_fundamentals_strings,exam_algorithms_fundamentals_arithmetic
import exam_algorithms_fundamentals_bits,exam_algorithms_fundamentals_matrices
import existing_algorithm_repairs
from legacy_algorithm_tests import entries
from algorithm_property_vectors import augment

def verify(entry):
    try:
        entry=augment(entry); folder=BUILD/entry['slug']
        if (folder/'implementation.s').read_text()!=entry['assembly']:raise ValueError('Stale assembly artifact; rerun VERIFY_ALGORITHMS')
        fixture='#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)\n'+entry['test']
        if (folder/'test.c').read_text()!=fixture:raise ValueError('Stale fixture artifact; rerun VERIFY_ALGORITHMS')
        code,called,untested=emulate(folder/'test.elf',re.findall(r'(?m)^\s*EXPORT\s+(\w+)',entry['assembly']))
        if code:raise ValueError('Assertion failed: '+str(code))
        return dict(slug=entry['slug'],status='PASS' if not untested else 'INCOMPLETE',executed_exports=called,untested_exports=untested)
    except Exception as error:return dict(slug=entry['slug'],status='FAIL',reason=str(error))
if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(verify,entries()+existing_algorithm_repairs.EXISTING+ENTRIES))
    (HERE/'ALGORITHM_ABI_COVERAGE.json').write_text(json.dumps(results,indent=2)+'\n')
    for result in results:
        if result['status']!='PASS':print(result)
    print('Suites:',len(results),'Pass:',sum(r['status']=='PASS' for r in results),'Executed exports:',sum(len(r.get('executed_exports',[])) for r in results))
    raise SystemExit(any(r['status']!='PASS' for r in results))
