"""Snapshot and integrate only reviewed workstation paths; never delete user files."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
STAGE=Path(__file__).resolve().parents[3]
MAINT="01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/"
PORTAL="01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/"
PROJECTS="01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/course-projects/"
SOURCES={"BUILD_STUDENT_PORTAL.py","VERIFY_STUDENT_PORTAL.py","PORTAL_MAINTENANCE.md",
"course_c.py","course_arm.py","course_board.py","course_projects.py","pattern_teaching.py",
"exam_walkthrough.py","workstation_extensions.py","search_corpus.py","VERIFY_WORKSTATION.py",
"VERIFY_WORKSTATION_CONTROLS.cjs","RELEASE_WORKSTATION.py","COURSE_COVERAGE.json",
"SEARCH_COVERAGE.json","SEARCH_DOCUMENT_CACHE.json","WORKSTATION_VALIDATION.json"}
SOURCES.update({"course_relationships.py","VERIFY_COURSE_EXECUTION.py","COURSE_EXECUTION_RESULTS.json",
"BROWSER_WORKSTATION_QA.cjs","WORKSTATION_CONTROLS_RESULTS.json","WORKSTATION_BROWSER_RESULTS.json"})
DOCS={
"03_ADDITIONAL_STUDY_MATERIAL/01 - Learn/02 - ARM Foundations/ASSEMBLY_EXAM_COURSE.md",
"03_ADDITIONAL_STUDY_MATERIAL/01 - Learn/02 - ARM Foundations/README.md",
"03_ADDITIONAL_STUDY_MATERIAL/01 - Learn/01 - C Foundations/C_EXAM_HANDBOOK.md",
"03_ADDITIONAL_STUDY_MATERIAL/01 - Learn/07 - Interrupts and Events/exceptions-and-svc.md",
}
def allowed(relative):
    return relative=="START_HERE.html" or relative.startswith((PORTAL,PROJECTS,MAINT+"portal_ui/")) or relative in DOCS or (relative.startswith(MAINT) and relative[len(MAINT):] in SOURCES)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def files(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts and ".git" not in p.parts}
def main():
    p=argparse.ArgumentParser();p.add_argument("mode",choices=["snapshot","integrate"]);p.add_argument("target");a=p.parse_args()
    target=Path(a.target).resolve()
    if target==STAGE.resolve() or target.name!="EXAM_HANDOFF":raise SystemExit("Target must be the original EXAM_HANDOFF, separate from staging.")
    baseline=STAGE.parent/"workstation-baseline.json"
    if a.mode=="snapshot":
        if baseline.exists():raise SystemExit("Baseline already exists; do not replace it.")
        baseline.write_text(json.dumps({"target":str(target),"files":files(target)},indent=2),encoding="utf-8")
        print("Saved original content baseline.");return
    prior=json.loads(baseline.read_text(encoding="utf-8"))
    if Path(prior["target"])!=target:raise SystemExit("Baseline target mismatch.")
    changes=[]
    for source in STAGE.rglob("*"):
        if not source.is_file():continue
        relative=source.relative_to(STAGE).as_posix()
        if not allowed(relative):continue
        dest=target/relative
        if dest.exists() and sha(dest)==sha(source):continue
        expected=prior["files"].get(relative)
        actual=sha(dest) if dest.exists() else None
        if actual!=expected:raise SystemExit("Original changed since baseline; not overwriting: "+relative)
        changes.append((source,dest,relative))
    backup=STAGE.parent/"workstation-backup"
    if backup.exists():raise SystemExit("Backup already exists; inspect before integrating again.")
    backup.mkdir()
    for source,dest,relative in changes:
        if dest.exists():
            old=backup/relative;old.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,old)
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
    protected=[relative for relative in prior["files"] if not allowed(relative)]
    changed_protected=[relative for relative in protected if not (target/relative).exists() or sha(target/relative)!=prior["files"][relative]]
    report={"changedFiles":len(changes),"backup":str(backup),"protectedFilesChecked":len(protected),"protectedChanges":changed_protected,"files":[r for _,_,r in changes]}
    (STAGE.parent/"workstation-integration.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="files"},indent=2))
if __name__=="__main__":main()
