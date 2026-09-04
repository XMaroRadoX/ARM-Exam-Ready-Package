"""Execute the C and actual Thumb implementations used by Solution Patterns."""
from concurrent.futures import ThreadPoolExecutor,as_completed
import json
from pattern_runnable import algorithm_entries, HERE
from VERIFY_ALGORITHMS import verify_entry
from algorithm_property_vectors import augment

def main():
    def verify(e):
        try:return verify_entry(dict(augment(e),reuse_build=True))
        except Exception as exc:return dict(slug=e['slug'],status='FAIL',reason=str(exc))
    results=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for task in as_completed([pool.submit(verify,e) for e in algorithm_entries().values()]):
            r=task.result();results.append(r);print(r['slug'],r['status'],r.get('reason',''),flush=True)
    (HERE/'PATTERN_ALGORITHM_RESULTS.json').write_text(json.dumps(dict(method='Independent C fixtures and execution of the delivered Thumb instructions',results=sorted(results,key=lambda r:r['slug']),nativeKeil='See PATTERN_NATIVE_BUILDS.json',physicalBoard='Not tested'),indent=2)+'\n')
    return int(any(r['status']=='FAIL' for r in results))
if __name__=='__main__':raise SystemExit(main())
