"""Compile new C for Cortex-M3 and execute the delivered sum's Thumb instructions.
Keil ARMASM / full firmware linking / physical-board validation remain separate.
"""
import argparse,json,re,subprocess,sys
from pathlib import Path
from course_projects import PROJECTS,SUM_ASM
from VERIFY_ALGORITHMS import CLANG,LLD,gas,RUNTIME,emulate
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def run(args):
    p=subprocess.run([str(x) for x in args],capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
    return p
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--test-deps",type=Path,default=HERE/".test-deps");args=ap.parse_args()
    sys.path.insert(0,str(args.test_deps))
    folder=HERE/".workstation-tests";folder.mkdir(exist_ok=True)
    flags=["--target=arm-none-eabi","-mcpu=cortex-m3","-mthumb","-std=c11","-O0","-ffreestanding","-fno-builtin","-fno-stack-protector","-Wall","-Wextra","-Werror"]
    projects=ROOT/"01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/course-projects"
    compiled=[]
    for name,files in PROJECTS.items():
        for filename in files:
            if not filename.endswith(".c"):continue
            source=projects/name/filename
            output=folder/(name+"-"+source.stem+".o")
            run([CLANG,*flags,"-I",projects/name/"Source/exam_api","-c",source,"-o",output])
            compiled.append(name+"/"+filename)
    fixture="""#include <stdint.h>
extern uint32_t sum_words(const uint32_t*,uint32_t);
#define CHECK(x) do { if(!(x)) return __LINE__; } while(0)
uint32_t test_main(void) {
    uint32_t a[3]={2u,4u,6u};
    uint32_t b[2]={UINT32_MAX,1u};
    CHECK(sum_words((const uint32_t*)0,0u)==0u);
    CHECK(sum_words(a,1u)==2u);
    CHECK(sum_words(a,3u)==12u);
    CHECK(a[0]==2u && a[1]==4u && a[2]==6u);
    CHECK(sum_words(b,2u)==0u);
    CHECK(b[0]==UINT32_MAX && b[1]==1u);
    CHECK(sum_words(a+1,2u)==10u);
    return 0u;
}
"""
    for name,value in [("test.c",fixture),("runtime.c",RUNTIME),("sum.gnu.s",gas(SUM_ASM))]:
        (folder/name).write_text(value,encoding="utf-8")
    for name in ("test","runtime"):
        run([CLANG,*flags,"-c",folder/(name+".c"),"-o",folder/(name+".o")])
    run([CLANG,*flags[:3],"-c",folder/"sum.gnu.s","-o",folder/"sum.o"])
    run([LLD,"-Ttext=0x10000","--entry=test_main",folder/"test.o",folder/"sum.o",folder/"runtime.o","-o",folder/"test.elf"])
    result,called,untested=emulate(folder/"test.elf",["sum_words"])
    if result or untested:raise RuntimeError(f"Thumb test failed: {result}; untested={untested}")
    report={"cortexM3CObjects":"PASS","compiledCFiles":compiled,"thumbExecution":"PASS",
            "assertions":7,"executedExports":called,"ABI":"SP and R4-R11 preservation checked at every public invocation",
            "assemblyConversion":"Only ARMASM directive spelling converted for LLVM; delivered instructions unchanged",
            "nativeKeilBuild":"Not run; compiler/device-pack environment not available","physicalBoard":"Not tested"}
    (HERE/"COURSE_EXECUTION_RESULTS.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__":main()
