"""Extend the existing offline generator without changing firmware contracts."""
from __future__ import annotations
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit, unquote
from course_c import C
from course_arm import ARM
from course_board import BOARD
from course_projects import CAPSTONES, PROJECTS
from pattern_teaching import WORKFLOWS, render as render_pattern
from exam_walkthrough import STEPS, HELP
from course_relationships import RELATED

TRACKS=[("c","C from zero",C),("arm","ARM from zero",ARM),("board","Board and integration",BOARD),("projects","Guided projects and exam practice",CAPSTONES)]
LESSONS=[lesson for _,_,track in TRACKS for lesson in track]
LECTURES={
 "1_":["arm-machine","board-start"],"2_":["arm-machine","arm-exceptions"],
 "3_":["arm-file","arm-constants"],"4_":["arm-memory","arm-layout"],"5_":["arm-constants"],
 "6_":["arm-flags","arm-wide"],"7_":["arm-flags","arm-loops"],"8_":["arm-stack","arm-extra"],
 "9_":["arm-contract","arm-stack","arm-recursion"],"10_":["arm-exceptions"],
 "11_":["c-integration","arm-contract","arm-extra"],"12_":["c-program","arm-file"],
 "13_":["board-leds"],"14_":["board-buttons","board-irq"],"15_":["board-power"],
 "16_":["board-timers"],"17_":["board-debounce"],"18_":["board-joystick"],
 "19_":["board-adc","board-dac"],"20_":["board-lcd"],"21_":["practice-exam"],
}
def install(c):
    root,portal,maint=c["ROOT"],c["PORTAL"],c["MAINTENANCE"]
    esc,rel,write=c["esc"],c["rel"],c["write"]
    old_page,old_assets,old_search=c["page"],c["build_assets"],c["build_search"]
    old_home,old_patterns,old_guide=c["build_home"],c["build_patterns"],c["guide_body"]
    c["NAV"][1:1]=[("Courses",portal/"courses/index.html"),("In the Exam",portal/"in-exam/index.html")]
    c["SECTION_META"].update({
        "courses":("Courses","Learn progressively: explanation, trace, attempt, feedback, and exam practice."),
        "in-exam":("In the Exam","Follow an offline checklist from the actual instructions to the submitted project."),
    })
    c["SECTION_META"]["patterns"]=("Solution Patterns","Recognize a problem, check whether a method fits, and adapt it safely.")
    c["SECTION_META"]["algorithms"]=("Algorithms","Inspect implementations, contracts, complexity, and test cases.")
    def page(*args,**kwargs):
        text=old_page(*args,**kwargs)
        source=Path(args[0] if args else kwargs["source"])
        script=f'<script src="{rel(portal/"assets/workstation.js",source)}" defer></script>'
        text=text.replace("</head>", '<link rel="stylesheet" href="'+rel(portal/"assets/workstation.css",source)+'">\n</head>')
        return text.replace("</body>",script+"\n</body>")
    def assets():
        old_assets()
        for name in ("workstation.js","workstation_state.js","workstation.css"):
            write(portal/"assets"/name,(maint/"portal_ui"/name).read_text(encoding="utf-8"))
        # Pure state logic is loaded before the UI module on every page.
    def wrapped_page(*args,**kwargs):
        text=page(*args,**kwargs)
        source=Path(args[0] if args else kwargs["source"])
        return text.replace('<script src="'+rel(portal/"assets/workstation.js",source)+'"',
                            '<script src="'+rel(portal/"assets/workstation_state.js",source)+'" defer></script>\n<script src="'+rel(portal/"assets/workstation.js",source)+'"')
    c.update(page=wrapped_page,build_assets=assets)

    def link(path,dest,label):return f'<a href="{rel(path,dest)}">{esc(label)}</a>'
    def paragraphs(value):return "".join("<p>"+esc(p.strip())+"</p>" for p in value.split("\n\n") if p.strip())
    def ul(values):return "<ul>"+"".join("<li>"+esc(v)+"</li>" for v in values)+"</ul>"
    def code(value,language="c"):
        return f'<pre><code class="language-{language}">{esc(value)}</code></pre>'
    def item(key,title,summary,dest,kind,tags=(),language="Both"):
        return dict(id=key,title=title,summary=summary,route=rel(dest,portal/"search.html"),kind=kind,
                    languages=[language],components=list(tags),topics=list(tags),aliases=[],
                    examHistory="Extra practice",relatedIds=[])
    def patterns(rows,exams,solutions,items):
        c["pattern_guidance"]=lambda family,title,clues:render_pattern(title,esc)
        links=old_patterns(rows,exams,solutions,items)
        index=portal/"patterns/index.html"
        extra=[]
        for title,*_ in WORKFLOWS:
            dest=portal/"patterns"/(c["slug"](title)+".html")
            body='<section class="section-block">'+render_pattern(title,esc)
            body+='<h2>Apply this workflow</h2><p>'+link(portal/"in-exam/index.html",dest,"Follow the exam checklist")+' · '+link(portal/"courses/index.html",dest,"Study the prerequisites")+'</p></section>'
            write(dest,c["page"](dest,title,"An exam workflow, not a claimed past-paper algorithm.",body,[("Home",c["HOME"]),("Solution Patterns",index),(title,dest)],"Solution Patterns"))
            links[title]=dest
            items.append(item("workflow-"+c["slug"](title),title,"; ".join(WORKFLOWS[[x[0] for x in WORKFLOWS].index(title)][1:3]),dest,"Solution Patterns",["Workflow"]))
            extra.append(f'<article class="card" data-filter-item data-family="Workflow" data-language="Both" data-history="Extra practice"><h2>{link(dest,index,title)}</h2><p>{esc(_[0])}.</p></article>')
        text=index.read_text(encoding="utf-8")
        text=text.replace('<option>Timers</option>','<option>Timers</option><option>Workflow</option>')
        marker='<div class="grid">'
        text=text.replace(marker,marker+"".join(extra),1)
        write(index,text)
        return links
    c["build_patterns"]=patterns

    def guide(key,cards,dest):
        body=old_guide(key,cards,dest)
        targets={"learn-c":"c-program","learn-assembly":"arm-machine","start-from-zero":"c-program"}
        if key in targets:
            body='<section class="notice"><h2>Take the complete course</h2><p>'+link(portal/"courses"/(targets[key]+".html"),dest,"Start with the first lesson")+' — concepts, traces, exercises, and answers in order.</p></section>'+body
        if key=="start-a-working-project":
            body+='<h2>Current answer files</h2><p>Edit <code>Source/sample.c</code> and <code>Source/ASM_funct.s</code> in your copied <code>sample.uvprojx</code>. Existing IRQ files retain one owner per vector. Historical answer-file names describe historical sources only.</p>'
        return body
    c["guide_body"]=guide

    def progress_controls():
        return '''<div class="progress-tools js-only"><button type="button" data-progress-export>Export progress</button><label>Import progress<input type="file" data-progress-import accept="application/json,.json"></label></div><p data-storage-status role="status"></p>'''

    def course_pages(items):
        index=portal/"courses/index.html"
        questions=c["read_csv"](c["GUIDES"]/"QUESTION_INDEX.csv")
        all_ids={v["id"] for v in LESSONS}
        question_map={}
        for q in questions:
            hay=" ".join(q.values()).lower()
            selected=["c-integration","arm-contract"]
            if q["question"]=="Q1":selected+=["arm-debug","arm-memory","arm-loops","c-collections"]
            else:selected+=["board-start","board-irq","board-combine","c-state"]
            for token,ids in [("byte",["arm-memory"]),("matrix",["arm-layout"]),("recurr",["arm-wide"]),("dfs",["arm-recursion"]),("svc",["arm-exceptions"]),("timer",["board-timers"]),("systick",["board-systick"]),("rit",["board-rit"]),("button",["board-buttons","board-debounce"]),("joystick",["board-joystick"]),("adc",["board-adc"]),("dac",["board-dac"]),("overflow",["c-bits","arm-wide"]),("stack",["arm-stack","arm-extra"])]:
                if token in hay:selected+=ids
            question_map[q["question_id"]]=list(dict.fromkeys(selected))
        lecture_map={}
        for pdf in sorted((root/"02_ORIGINAL_MATERIALS/ARM").glob("*.pdf")):
            prefix=pdf.name.split("_")[0]+"_"
            if prefix in LECTURES:lecture_map[pdf.relative_to(root).as_posix()]=LECTURES[prefix]
        write(maint/"COURSE_COVERAGE.json",json.dumps({"lessons":[v["id"] for v in LESSONS],"lectures":lecture_map,"questions":question_map},indent=2))
        assert len(question_map)==48
        assert all(x in all_ids for values in question_map.values() for x in values)
        cards=[]
        prev=None
        for track_key,track_title,lessons in TRACKS:
            entries=[]
            for lesson in lessons:
                dest=portal/"courses"/(lesson["id"]+".html")
                position=LESSONS.index(lesson)
                next_lesson=LESSONS[position+1] if position+1<len(LESSONS) else None
                body=f'<section class="section-block" data-course-lesson="{esc(lesson["id"])}"><p class="eyebrow">{esc(track_title)} · {esc(lesson["tier"])}</p>'
                body+='<h2>Before this lesson</h2><p>'+(
                    link(portal/"courses"/(prev["id"]+".html"),dest,prev["title"])+" — finish its checkpoint first." if prev else "No programming knowledge assumed. Start here."
                )+"</p>"
                body+='<h2>Understand the idea</h2>'+paragraphs(lesson["explanation"])
                body+='<h2>Worked example</h2><p class="notice">Illustrative fragment unless explicitly marked as a complete project below. Read the contract and required placement before copying.</p>'+code(lesson["code"],"assembly" if track_key=="arm" else "c")
                body+='<h2>Execution trace</h2>'+paragraphs(lesson["trace"])
                body+='<h2>Try it before the answer</h2>'+paragraphs(lesson["task"])
                for i,hint in enumerate(lesson["hints"],1):body+=f'<details class="lesson-reveal"><summary>Hint {i}</summary><p>{esc(hint)}</p></details>'
                body+='<details class="lesson-reveal"><summary>Reveal the worked answer</summary>'+paragraphs(lesson["answer"])+'</details>'
                body+='<h2>Common mistakes and symptoms</h2>'+paragraphs(lesson["mistakes"])
                body+='<h2>Checkpoint</h2>'+paragraphs(lesson["checkpoint"])
                body+=f'<label class="completion-control js-only"><input type="checkbox" data-lesson-complete="{esc(lesson["id"])}"> I can explain and demonstrate this checkpoint</label>'
                # Reuse the maintained deeper chapters instead of maintaining divergent copies.
                reading=lesson.get("reading")
                if reading:
                    source=(root/"03_ADDITIONAL_STUDY_MATERIAL/01 - Learn/01 - C Foundations/C_EXAM_COURSE.md" if track_key=="c" else root/"03_ADDITIONAL_STUDY_MATERIAL/01 - Learn/02 - ARM Foundations/ASSEMBLY_EXAM_COURSE.md" if track_key=="arm" else c["GUIDES"]/"PERIPHERALS_CANONICAL.md")
                    text=c["extract_markdown_section"](source,"",reading)
                    if text:
                        body+='<h2>Deeper explanation and source examples</h2><details class="lesson-reveal"><summary>Continue into the maintained reference chapter</summary>'+c["markdown_fragment"](text,source,dest)+'</details>'
                if lesson["id"] in PROJECTS:
                    project=c["GENERATED_SOURCES"]/"course-projects"/lesson["id"]
                    shutil.copytree(c["STARTING_TEMPLATE"],project,dirs_exist_ok=True)
                    for filename,value in PROJECTS[lesson["id"]].items():write(project/filename,value)
                    body+='<h2>Complete project solution</h2><p>Compare after your attempt. Copy this whole project into your working area before editing. The other driver/startup files remain the supplied template.</p>'
                    body+=link(project/"sample.uvprojx",dest,"Open the complete teaching project")
                    for filename,value in PROJECTS[lesson["id"]].items():
                        body+='<h3>'+esc(filename)+'</h3><p>Complete replacement file in this teaching project. '+link(project/filename,dest,"Read this source file")+'</p>'+code(value,"assembly" if filename.endswith(".s") else "c")
                body+='<h2>Connect this skill to the exam</h2><ul>'
                for title in RELATED[lesson['id']]:
                    body+='<li>Pattern: '+link(portal/'patterns'/(c['slug'](title)+'.html'),dest,title)+'</li>'
                matches=[q for q in questions if lesson["id"] in question_map[q["question_id"]]][:4]
                if not matches and lesson['tier']!='Extension':
                    matches=[q for q in questions if any(t.lower() in ' '.join(q.values()).lower() for t in lesson['tags'] if len(t)>2)][:2] or questions[:2]
                if lesson['tier']=='Extension':
                    body+='<li>No reviewed question is claimed to require this extension. Follow the linked original lecture and transfer the listed foundational patterns where relevant.</li>'
                for q in matches:
                    qpath=portal/"exams"/(c["slug"](q["question_id"])+".html")
                    body+='<li>'+link(qpath,dest,q["question_id"]+": "+q["requirement_summary"])+'</li>'
                body+='<li>'+link(portal/"search.html",dest,"Search related patterns, implementations, and API calls")+'</li>'
                body+='<li>'+link(portal/"courses/coverage.html",dest,"See all lecture and question mappings")+'</li></ul>'
                names=sorted(set(re.findall(r"\bexam_[a-z0-9_]+(?=\s*\()",lesson["code"]+" "+lesson["explanation"])))
                if names:
                    body+='<p>API: '+" · ".join(link(portal/"api"/(name.replace("_","-")+".html"),dest,name) for name in names)+'</p>'
                sources=[path for path,ids in lecture_map.items() if lesson["id"] in ids]
                if sources:body+='<p>Original lecture: '+" · ".join(link(root/path,dest,Path(path).stem) for path in sources)+'</p>'
                body+='<nav class="lesson-navigation" aria-label="Lesson navigation">'
                if prev:body+=link(portal/"courses"/(prev["id"]+".html"),dest,"← "+prev["title"])
                if next_lesson:body+=link(portal/"courses"/(next_lesson["id"]+".html"),dest,next_lesson["title"]+" →")
                body+='</nav></section>'+progress_controls()
                write(dest,c["page"](dest,lesson["title"],"Read, trace, attempt, check, then progress.",body,[("Home",c["HOME"]),("Courses",index),(lesson["title"],dest)],"Courses"))
                items.append(item("lesson-"+lesson["id"],lesson["title"],lesson["explanation"].split("\n\n")[0],dest,"Courses",lesson["tags"],"Assembly" if track_key=="arm" else "C"))
                entries.append(f'<li data-course-entry="{lesson["id"]}">{link(dest,index,lesson["title"])} <span class="tier">{esc(lesson["tier"])}</span><span data-completion-mark="{lesson["id"]}"></span></li>')
                prev=lesson
            cards.append(f'<section class="section-block" id="{track_key}"><h2>{track_title}</h2><ol class="course-list">{"".join(entries)}</ol></section>')
        body='<section class="section-block"><h2>From your first program to an independent attempt</h2><p>Follow the sequence; every stage remains available. Exam core marks immediate programming preparation. Supporting knowledge explains the environment. Extensions broaden the supplied lecture coverage.</p><p data-course-progress role="status"></p>'+link(portal/"courses/c-program.html",index,"Begin with your first C program")+' · '+link(portal/"courses/coverage.html",index,"Lecture and exam coverage")+'</section>'+"".join(cards)+progress_controls()
        write(index,c["page"](index,"Courses","Start from zero and finish with guided projects and independent exam practice.",body,[("Home",c["HOME"]),("Courses",index)],"Courses"))
        items.append(item("courses", "Courses", "C, ARM, board, integration and independent practice",index,"Courses"))
        coverage=portal/"courses/coverage.html"
        body='<section class="section-block"><h2>Supplied ARM lecture sequence</h2><p>These links map foundations and supporting lessons; they do not claim that every lecture detail appears in every exam.</p><ul>'
        for source,ids in lecture_map.items():
            body+='<li>'+link(root/source,coverage,Path(source).name)+': '+" · ".join(link(portal/"courses"/(key+".html"),coverage,next(x["title"] for x in LESSONS if x["id"]==key)) for key in ids)+'</li>'
        body+='</ul><h2>All 48 reviewed questions</h2><p>Use these prerequisite links alongside the question-specific pattern and algorithm links on each reviewed answer.</p><ul>'
        for q in questions:
            body+='<li>'+link(portal/"exams"/(c["slug"](q["question_id"])+".html"),coverage,q["question_id"])+': '+" · ".join(link(portal/"courses"/(key+".html"),coverage,next(x["title"] for x in LESSONS if x["id"]==key)) for key in question_map[q["question_id"]])+'</li>'
        body+='</ul></section>'
        write(coverage,c["page"](coverage,"Lecture and exam coverage","Find the prerequisites for every supplied ARM lecture and reviewed question.",body,[("Home",c["HOME"]),("Courses",index),("Coverage",coverage)],"Courses"))

    def exam_pages(items):
        dest=portal/"in-exam/index.html"
        body='<section data-exam-guide><details class="section-block exam-sitting" open data-exam-sitting><summary>This sitting: instructions, duration, and destination</summary><p>Use the current instructions. Nothing here assumes permission, duration, or a collection drive.</p><div class="sitting-fields">'
        for key,label,kind in [("materials","Permitted materials","text"),("duration","Actual duration in minutes (optional)","number"),("template","Required template or interface","text"),("destination","Exact collection destination","text")]:
            extra=' min="1" max="1440"' if kind=="number" else ' maxlength="500"'
            body+=f'<label>{label}<input type="{kind}" data-exam-field="{key}"{extra}></label>'
        body+='<label>Implementation order<select data-exam-field="order"><option value="">Choose after reading both questions</option><option value="assembly">Assembly first</option><option value="board">Board first with a temporary stub</option></select></label></div>'
        body+='<p data-time-budget role="status">Optional budgets are suggestions, not course rules.</p><p>Supplied rule references: '+link(root/"02_ORIGINAL_MATERIALS/Exams/Exam rules.pdf",dest,"Exam rules")+' · '+link(root/"02_ORIGINAL_MATERIALS/Exams/Exam rules v3.pdf",dest,"Exam rules v3")+'</p>'
        body+='</details><div class="exam-actions js-only"><button type="button" data-exam-all>Show full checklist</button><button type="button" data-exam-reset>Reset this exam session</button></div><p data-exam-status role="status"></p>'
        body+='<nav class="exam-step-nav" aria-label="Exam steps">'
        for i,(key,title,*_) in enumerate(STEPS):body+=f'<a href="#step-{key}" data-go-step="{i}">{i+1}. {esc(title)}</a>'
        body+='</nav>'
        for i,(key,title,explanation,checks,checkpoint) in enumerate(STEPS):
            body+=f'<section class="section-block exam-step" id="step-{key}" data-exam-step="{i}"><p class="eyebrow">Step {i+1} of {len(STEPS)}</p><h2 tabindex="-1">{esc(title)}</h2><p>{esc(explanation)}</p>'
            for j,check in enumerate(checks):
                body+=f'<label class="exam-check"><input type="checkbox" data-exam-check="{key}-{j}"><span>{esc(check)}</span></label>'
            body+='<h3>Ready to move on when</h3><p>'+esc(checkpoint)+'</p>'
            if key=="order":body+='<p data-order-guidance></p>'
            links_for={"prepare":["board-start"],"read":["c-functions"],"contract":["arm-contract","arm-extra","c-state"],"implement":["board-combine","arm-loops"],"test":["arm-debug","board-debounce"],"order":["project-timed"]}
            for lesson in links_for.get(key,[]):body+='<p>'+link(portal/"courses"/(lesson+".html"),dest,"Review: "+next(x["title"] for x in LESSONS if x["id"]==lesson))+'</p>'
            body+='<p>'+link(portal/"patterns/index.html",dest,"Choose a solution pattern")+' · '+link(portal/"api/index.html",dest,"Check the current API")+'</p>'
            body+='<div class="exam-actions js-only"><button type="button" data-exam-prev>Previous step</button><button type="button" data-exam-next>Next step</button></div></section>'
        body+='<section class="section-block"><h2>I’m stuck</h2>'
        for key,title,checks in HELP:body+=f'<details class="lesson-reveal" id="help-{key}"><summary>{esc(title)}</summary>'+ul(checks)+'</details>'
        body+='</section><section class="section-block"><h2>Session notes</h2><label>Requirements, test cases, and remaining stubs<textarea data-exam-field="notes" rows="6" maxlength="20000"></textarea></label></section></section>'+progress_controls()
        write(dest,c["page"](dest,"In the Exam","One actionable step at a time, fully offline.",body,[("Home",c["HOME"]),("In the Exam",dest)],"In the Exam"))
        items.append(item("in-exam","In the Exam","Offline exam plan, checkpoints, troubleshooting, and submission",dest,"In the Exam"))

    def search(items):
        # Retain compatibility with the legacy algorithms-only refresh: rebuild new routes once.
        items[:]=[x for x in items if not str(x["id"]).startswith(("text-","lesson-")) and x["id"] not in {"courses","in-exam"}]
        course_pages(items);exam_pages(items)
        from search_corpus import build
        report=build(c,items)
        old_search(items)
        path=portal/"search.html"
        text=path.read_text(encoding="utf-8")
        text=text.replace('placeholder="Search by title, alias, topic, component, or summary"','placeholder="Search explanations, code, questions, functions, or symptoms"')
        text=text.replace('<option>Guides</option>','<option>Guides</option><option>Original material</option><option>Source references</option>')
        text=text.replace('<label>Exam history', '<label>Source<select data-search-filter="sourceClass"><option value="">All sources</option><option>Maintained</option><option>Original</option><option>Historical</option></select></label><label>Exam history')
        coverage=portal/"search-coverage.html"
        text=text.replace('<div data-search-results></div>', '<p>'+link(coverage,path,"What is indexed and what is not")+'</p><div data-search-results></div>')
        write(path,text)
        body=f'<section class="section-block"><h2>Coverage</h2><p>{report["indexedFiles"]} source/page files inspected; {report["pdfPages"]} PDF pages with extractable text; {report["sectionRecords"]} full-text records; {report["duplicates"]} duplicate records collapsed.</p><p>Original and historical results retain their labels. Personal working projects, caches, generated build artifacts, and binaries are excluded. Search indexes text, not pictures or audio.</p><h2>Pages needing the original viewer</h2><ul>'
        for r in report["unindexed"]:
            body+='<li>'+link(root/r["path"],coverage,Path(r["path"]).name)+(f' page {r["page"]}' if "page" in r else "")+': '+esc(r["reason"])+'</li>'
        body+='</ul></section>'
        write(coverage,c["page"](coverage,"Search coverage","Transparent limits of the offline index.",body,[("Home",c["HOME"]),("Search",path),("Coverage",coverage)]))
    c["build_search"]=search
    def home():
        old_home()
        path=c["HOME"];text=path.read_text(encoding="utf-8")
        shortcut='<section class="exam-entry"><a class="button" href="'+rel(portal/"in-exam/index.html",path)+'">I’m in the exam — guide me</a><a href="'+rel(portal/"courses/index.html",path)+'">Study from the beginning</a></section>'
        text=text.replace('<section class="study-section">',shortcut+'<section class="study-section">',1)
        text=text.replace('</head>','<link rel="stylesheet" href="'+rel(portal/'assets/workstation.css',path)+'">\n</head>')
        write(path,text)
    c["build_home"]=home
