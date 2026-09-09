"""Refresh only this paper's pages, raw answers, and catalog records.
The ordinary builder also retains these answers through per-question sources.
"""
from pathlib import Path
import csv, hashlib, io, json, re
import BUILD_STUDENT_PORTAL as b
from portal_presentation import install
from workstation_extensions import install as extensions
from asm_reference import install as asm_install

def main():
    root=b.ROOT
    stage=root/"90_WORKING_PROJECTS/LCG_20250701_UPDATE"
    stage.mkdir(parents=True,exist_ok=True)
    reviewed=b.COURSE/"REVIEWED_EXAM_INDEX.csv"
    exams=b.read_csv(reviewed)
    for row in exams:
        if row["exam_id"]=="E2025-07-01-A1":
            row["source_pdf"]="02_ORIGINAL_MATERIALS/Exams/ARM questions/20250701.pdf"
    questions=b.read_csv(b.GUIDES/"QUESTION_INDEX.csv")
    solutions=b.read_csv(b.GUIDES/"CURRENT_TEMPLATE_SOLUTION_INDEX.csv")
    context=vars(b);install(context);extensions(context);asm_install(context)
    # Capture builder output instead of invoking its destructive full-build entrypoint.
    captured={};before={}
    original_source=b.source_code
    def capture(path,text):
        path=Path(path)
        if path not in before:
            before[path]=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        captured[path]=text
    b.write=capture
    b.source_code=lambda path:captured.get(path,original_source(path))
    original_details = b.details_code
    def details(label, code, raw, destination, language, expanded=False):
        panel = original_details(label, code, raw, destination, language, expanded)
        if raw in captured and not raw.exists():
            panel = panel.replace('<div class="code-actions"></div>',
                '<div class="code-actions">' + b.href(raw, destination, "Open raw " + language + " file", "raw-link") + '</div>')
        return panel
    b.details_code = details
    # Presentation closures may retain the previous write function; build_exams
    # itself uses the overridden b.write and never invokes full-build hooks.
    items=[]
    b.build_exams(exams,questions,solutions,{}, {}, {},items)

    names={"e2025-07-01-a1.html","2025-07-01-arm1-q1.html","2025-07-01-arm1-q2.html","2025-07-01-arm1-q3.html","index.html"}
    raw=b.GENERATED_SOURCES/"exam-solutions"
    def allowed(path):
        return (path.parent==b.PORTAL/"exams" and path.name in names
                or path==raw/"manifest.json"
                or path.parent.parent==raw and path.parent.name in {
                    "2025-07-01-arm1-q1","2025-07-01-arm1-q2","2025-07-01-arm1-q3"})
    selected={p:t for p,t in captured.items() if allowed(p)}
    # Preserve all catalog records except this paper's four matching records.
    data_path=b.ASSETS/"portal-data.js"
    data=json.loads(re.fullmatch(r"\s*window\.ARM_PORTAL_DATA=(.*);\s*",data_path.read_text(encoding="utf-8-sig"),re.S)[1])
    new={i["id"]:i for i in items if i["id"]=="exam-e2025-07-01-a1" or i["id"].startswith("question-2025-07-01-arm1-")}
    assert len(new)==4
    data["items"]=[new.get(i["id"],i) for i in data["items"]]
    selected[data_path]="window.ARM_PORTAL_DATA="+json.dumps(data,ensure_ascii=False,separators=(",",":"))+";\n"
    out=io.StringIO(newline="");w=csv.DictWriter(out,fieldnames=list(exams[0]),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(exams)
    selected[reviewed]=out.getvalue()
    for p in selected:
        if p not in before:before[p]=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
    # Render all outputs into a reviewable mirror first.
    for p,text in selected.items():
        dest=stage/"rendered"/p.relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text,encoding="utf-8",newline="\n")
    manifest=[]
    for p,text in selected.items():
        old=p.read_bytes() if p.exists() else None
        digest=hashlib.sha256(old).hexdigest() if old is not None else None
        assert digest==before[p],f"Changed concurrently: {p}"
        if old is not None and old.decode("utf-8-sig").replace("\r\n","\n")==text.replace("\r\n","\n"):continue
        backup=stage/"before"/p.relative_to(root)
        if old is not None and not backup.exists():
            backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(old)
        p.parent.mkdir(parents=True,exist_ok=True)
        tmp=p.with_name(p.name+".lcg-tmp");tmp.write_text(text,encoding="utf-8",newline="\n");tmp.replace(p)
        manifest.append(p.relative_to(root).as_posix())
    (stage/"published.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps({"published":len(manifest),"paths":manifest},indent=2))
if __name__=="__main__":main()

