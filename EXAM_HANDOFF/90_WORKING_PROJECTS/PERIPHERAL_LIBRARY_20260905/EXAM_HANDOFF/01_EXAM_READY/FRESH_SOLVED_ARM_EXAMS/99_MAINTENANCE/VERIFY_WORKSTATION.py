"""Additional acceptance checks. Reads generated content; writes only a test report."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json,re,subprocess,shutil,sys
from course_c import C
from course_arm import ARM
from course_board import BOARD
from course_projects import CAPSTONES,PROJECTS
from pattern_teaching import PATTERNS
from course_relationships import RELATED
from search_corpus import plain
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PORTAL=ROOT/"01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL"
def verify():
    checks=0;errors=[]
    def check(ok,message):
        nonlocal checks
        checks+=1
        if not ok:errors.append(message)
    lessons=C+ARM+BOARD+CAPSTONES
    check(len(lessons)==46,"Expected 46 authored lessons")
    check(set(RELATED)=={x['id'] for x in lessons},"Every lesson needs explicit pattern relationships")
    check(all(title in PATTERNS for titles in RELATED.values() for title in titles),"Unknown related pattern")
    for lesson in lessons:
        p=PORTAL/"courses"/(lesson["id"]+".html")
        check(p.exists(),"Missing lesson "+lesson["id"])
        if not p.exists():continue
        raw=p.read_text(encoding="utf-8")
        for marker in ("Before this lesson","Understand the idea","Worked example","Execution trace","Try it before the answer","Hint 1","Hint 2","Reveal the worked answer","Common mistakes and symptoms","Checkpoint","Connect this skill to the exam"):
            check(marker in raw,lesson["id"]+" missing "+marker)
        check(len(lesson["explanation"].split())>=65,lesson["id"]+" explanation too short")
        check(len(lesson["hints"])>=2,lesson["id"]+" needs progressive hints")
    for title,data in PATTERNS.items():
        slug=re.sub(r"[^a-z0-9]+","-",title.lower()).strip("-")
        p=PORTAL/"patterns"/(slug+".html")
        if (HERE/'SECTION_DESTINATIONS.json').exists():
            p=PORTAL/json.loads((HERE/'SECTION_DESTINATIONS.json').read_text())[title]['route']
        check(p.exists(),"Missing pattern "+title)
        if p.exists():
            raw=p.read_text(encoding="utf-8");text=plain(raw)
            for field in ("use","avoid","trace","tests","adapt"):
                check(data[field] in text,title+" missing specific "+field)
    coverage=json.loads((HERE/"COURSE_COVERAGE.json").read_text())
    check(len(coverage["questions"])==48,"Question coverage incomplete")
    check(set(coverage["lessons"])=={x["id"] for x in lessons},"Lesson coverage mismatch")
    check(set(range(1,22)).issubset({int(Path(p).name.split("_")[0]) for p in coverage["lectures"]}),"ARM lecture sequence 1..21 incomplete")
    raw=(PORTAL/"assets/portal-data.js").read_text(encoding="utf-8")
    items=json.loads(raw.removeprefix("window.ARM_PORTAL_DATA=").rstrip(";\n"))["items"]
    for item in items:
        parts=urlsplit(item["route"])
        target=(PORTAL/unquote(parts.path)).resolve()
        check(target.is_relative_to(ROOT.resolve()),"Search target escapes package")
        check(target.exists(),"Search target missing: "+item["route"])
        if parts.fragment and target.suffix.lower() in {".html",".htm"} and target.is_file():
            check(('id="'+unquote(parts.fragment)+'"') in target.read_text(encoding="utf-8",errors="replace"),"Missing search anchor "+item["route"])
        check("90_WORKING_PROJECTS" not in item.get("sourcePath",""),"Personal work indexed")
        check(item.get("sourceClass") in {"Maintained","Original","Historical"},"Source class missing")
    check(any(i.get("sourceClass")=="Original" and "#page=" in i["route"] for i in items),"No page-level PDF search")
    check(any(i.get("alternateSources") for i in items),"No duplicate source grouping")
    exam=(PORTAL/"in-exam/index.html").read_text(encoding="utf-8")
    for marker in ("data-exam-step=","data-progress-export","data-progress-import","data-exam-reset","help-build","help-output","help-fault","help-interrupt","help-bounce","help-time"):
        check(marker in exam,"Exam guide missing "+marker)
    check(exam.count('data-exam-step="')==9,"Exam step count")
    projects=ROOT/"01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/course-projects"
    syntax=[]
    gcc=shutil.which("gcc")
    native=json.loads((HERE/'PATTERN_NATIVE_BUILDS.json').read_text()).get('projects',{})
    reused_native=[]
    for key,files in PROJECTS.items():
        folder=projects/key
        import hashlib
        hashes={str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [folder/'sample.uvprojx',*sorted((folder/'Source').rglob('*'))] if p.is_file()}
        native_match=native.get(key,{}).get('status')=='PASS' and native[key].get('sources')==hashes
        if native_match:reused_native.append(key)
        for name,expected in files.items():
            check((folder/name).read_text()==expected,key+" source differs: "+name)
            if gcc and not native_match and name.endswith(".c"):
                # Relative compiler inputs also work inside a deeply nested staging copy.
                includes=[str(p.relative_to(folder)) for p in (folder/"Source").rglob("*") if p.is_dir()]+["Source"]
                compiler_source=name
                if sys.platform == "win32" and len(str(folder/name)) >= 240:
                    import ctypes
                    short=ctypes.create_unicode_buffer(32768)
                    if ctypes.windll.kernel32.GetShortPathNameW(str(folder/name),short,len(short)):
                        compiler_source=short.value
                # Windows short names can end in uppercase .C; explicitly select C.
                cmd=[gcc,"-x","c","-std=c11","-fsyntax-only","-Werror=implicit-function-declaration",*[v for p in includes for v in ("-I",p)],compiler_source]
                run=subprocess.run(cmd,cwd=folder,capture_output=True,text=True)
                syntax.append({"project":key,"file":name,"status":"PASS" if run.returncode==0 else "FAIL","details":(run.stdout+run.stderr)[-1800:]})
    report={"structuralChecks":checks,"errors":errors,"hostSyntaxWithActualHeaders":syntax,"unchangedNativeProjectsVerifiedBySourceHash":reused_native,
            "nativeKeilBuild":"See PATTERN_NATIVE_BUILDS.json for native target results. This report covers the structural and host syntax checks only.",
            "physicalBoard":"Not performed; board required for input/timing/output claims."}
    (HERE/"WORKSTATION_VALIDATION.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    return bool(errors) or any(x["status"]=="FAIL" for x in syntax)
if __name__=="__main__":sys.exit(verify())
