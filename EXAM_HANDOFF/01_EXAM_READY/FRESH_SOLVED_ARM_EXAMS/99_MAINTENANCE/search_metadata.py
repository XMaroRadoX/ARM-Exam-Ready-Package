"""Source-backed relationships shared by global and section search."""
from __future__ import annotations
import calendar
import csv
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlencode

FIELDS = ("examId", "date", "year", "variant", "question", "functions", "algorithms",
          "peripherals", "interrupts", "timing", "architecture", "recognition", "track",
          "materialType", "solutionStatus", "metadataScope", "scopeRoutes", "paperRoute",
          "solutionRoutes", "languages", "components", "topics", "aliases", "examHistory")

def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

def tags(value):
    return list(dict.fromkeys(x.strip() for x in re.split(r"[|;]", value or "") if x.strip()))

def unique(values):
    return list(dict.fromkeys(v for v in values if v))

def date_aliases(value):
    d = date.fromisoformat(value)
    return [value, value.replace("-", ""), f"{d.day:02}/{d.month:02}/{d.year}",
            f"{d.day} {calendar.month_name[d.month]} {d.year}",
            f"{d.day} {calendar.month_abbr[d.month]} {d.year}"]

def read_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))

def enrich(context, items):
    root, portal, guides = (context[k] for k in ("ROOT", "PORTAL", "GUIDES"))
    route = lambda path: context["rel"](path, portal / "search.html")
    exams = read_rows(guides / "EXAM_COURSE/REVIEWED_EXAM_INDEX.csv")
    questions = {q["question_id"]: q for q in read_rows(guides / "QUESTION_INDEX.csv")}
    manifest = json.loads((context["GENERATED_SOURCES"] / "exam-solutions/manifest.json").read_text(encoding="utf-8"))
    catalog = {i["id"]: i for i in items}
    sources = {}
    def source(path, metadata):
        if path:
            key = path.resolve().relative_to(root.resolve()).as_posix()
            sources.setdefault(key, []).append(dict(metadata))
    for exam in exams:
        eid = exam["exam_id"]
        eitem = catalog["exam-" + slug(eid)]
        paper = context["resolve_index_path"](exam["source_pdf"], context["LIBRARY"])
        if not paper or not paper.is_file():
            raise ValueError("Missing original paper: " + eid)
        paper_route = route(paper)
        children = []
        for answer in manifest["questions"]:
            if answer["examId"] != eid:
                continue
            q = questions[answer["questionId"]]
            item = catalog["question-" + slug(q["question_id"])]
            files = [root / name for name in answer["requiredFiles"]]
            if not files or any(not p.is_file() for p in files):
                raise ValueError("Missing answer: " + q["question_id"])
            languages = unique("Assembly" if p.suffix.lower() == ".s" else "C" for p in files)
            groups = {key: tags(q[column]) for key, column in (
                ("algorithms", "algorithm_tags"), ("peripherals", "peripheral_tags"),
                ("interrupts", "interrupt_tags"), ("timing", "timing_tags"),
                ("architecture", "architecture_tags"))}
            item.update(groups)
            item.update(examId=eid, date=exam["date"], year=exam["date"][:4],
                        variant=answer["variant"], question=q["question"],
                        functions=tags(q["function_or_handler"]), recognition=tags(q["keywords"]),
                        track="ARM programming", materialType="Question and solution",
                        solutionStatus="Maintained solution available", metadataScope="Question",
                        languages=languages, paperRoute=paper_route,
                        solutionRoutes=[route(p) for p in files],
                        scopeRoutes=[item["route"], eitem["route"]],
                        components=unique(groups["peripherals"] + groups["interrupts"] + groups["timing"]),
                        topics=unique(groups["algorithms"] + groups["architecture"]),
                        examHistory="Appeared in past exams")
            variant_id = re.search(r"ARM\d+", q["question_id"], re.I)
            item["aliases"] = unique(list(item.get("aliases", [])) + date_aliases(exam["date"]) +
                [eid, q["question_id"], q["question"], "Question " + q["question"].lstrip("Q"), paper.name] +
                ([variant_id[0], variant_id[0].replace("ARM", "ARM ")] if variant_id else []) +
                item["functions"] + item["recognition"])
            item["relatedIds"] = unique([eitem["id"]] + item.get("relatedIds", []))
            children.append(item)
            for path in files:
                source(path, {**{k: item[k] for k in FIELDS if k in item}, "materialType": "Solution code",
                              "kind": "Past Exams", "title": item["title"] + " — " + path.name,
                              "sourceClass": "Maintained"})
        if not children:
            raise ValueError("Exam has no mapped questions: " + eid)
        eitem.update(examId=eid, date=exam["date"], year=exam["date"][:4], variant=children[0]["variant"],
                     question="", track="ARM programming", materialType="Exam overview",
                     solutionStatus="Maintained solution available", metadataScope="Whole paper",
                     scopeRoutes=[eitem["route"]], paperRoute=paper_route,
                     solutionRoutes=unique(r for q in children for r in q["solutionRoutes"]))
        for key in ("functions", "algorithms", "peripherals", "interrupts", "timing", "architecture",
                    "recognition", "languages", "components", "topics", "aliases"):
            eitem[key] = unique(v for q in children for v in q[key])
        # A whole paper must not claim to be any one of its questions.
        eitem["aliases"] = [a for a in eitem["aliases"] if not re.fullmatch(r"Q\d+|Question \d+", a)]
        eitem["relatedIds"] = unique([q["id"] for q in children] + eitem.get("relatedIds", []))
        source(paper, {**{k: eitem[k] for k in FIELDS if k in eitem}, "materialType": "Original paper",
                       "kind": "Past Exams", "title": eitem["title"] + " — original paper"})
        for key in ("main_c", "assembly_s"):
            path = context["resolve_index_path"](exam.get(key, ""), context["LIBRARY"])
            if path and path.is_file():
                source(path, {**{k: eitem[k] for k in FIELDS if k in eitem},
                              "materialType": "Historical solution", "kind": "Past Exams",
                              "title": eitem["title"] + " — " + path.name,
                              "languages": ["Assembly" if path.suffix.lower() == ".s" else "C"]})
    for item in items:
        item.setdefault("scopeRoutes", [item["route"]])
        item.setdefault("materialType", {"API": "API reference", "Algorithms": "Algorithm",
                        "Solution Patterns": "Solution pattern", "Courses": "Lesson"}.get(item["kind"], "Guide"))
        item.setdefault("track", "ARM programming")
    return sources

def simplify_search_markup(text):
    """Keep the section selector visible and secondary controls available on demand."""
    if 'data-search-advanced' in text:
        return text
    match = re.search(r'<div class="filter-bar">(.*?)</div>', text, re.S)
    if not match:
        raise ValueError("Search filter bar is missing")
    labels = re.findall(r'<label>.*?</label>', match[1], re.S)
    section = next(label for label in labels if 'data-search-filter="kind"' in label)
    advanced = ''.join(label for label in labels if label != section)
    tools = ('<div class="search-tools"><div class="filter-bar">' + section + '</div>'
             '<details data-search-advanced><summary>More filters</summary>'
             '<div class="filter-bar">' + advanced + '</div>'
             '<p><a href="search-coverage.html">Search coverage</a></p></details></div>'
             '<p class="search-scope"><button type="button" data-search-scope>'
             'Search all source material</button></p>')
    text = text[:match.start()] + tools + text[match.end():]
    text = re.sub(r'<p><a href="[^"]*search-coverage.html">What is indexed and what is not</a></p>', '', text)
    text = text.replace('Search everything', 'Search')
    return text.replace('Search questions, solutions, code, functions, or topics', 'Search a topic, function, or exam')


def finish(context, items, report):
    """Add section bindings and coverage without changing lesson or answer content."""
    portal, assets = context["PORTAL"], context["ASSETS"]
    esc, rel, write = (context[k] for k in ("esc", "rel", "write"))
    search = portal / "search.html"
    text = search.read_text(encoding="utf-8")
    text = text.replace('placeholder="Search by title, alias, topic, component, or summary"',
                        'placeholder="Search questions, solutions, code, functions, or topics"')
    def select(key, title, values):
        return '<label>' + title + '<select data-search-filter="' + key + '"><option value="">All ' + title.lower() + '</option>' + ''.join('<option>' + esc(v) + '</option>' for v in sorted(set(values)) if v) + '</select></label>'
    for key, title, values in (
        ("year", "Years", [i.get("year", "") for i in items]),
        ("variant", "Variants", [i.get("variant", "") for i in items]),
        ("question", "Questions", [i.get("question", "") for i in items]),
        ("materialType", "Material types", [i.get("materialType", "") for i in items]),
        ("sourceClass", "Sources", ["Maintained", "Original", "Historical"]),
        ("track", "Tracks", ["ARM programming", "Architecture / theory", "General reference"])):
        text = text.replace('<div class="filter-bar">', '<div class="filter-bar">' + select(key, title, values), 1)
    kinds = unique(i["kind"] for i in items)
    text = re.sub(r'(<select data-search-filter="kind">).*?</select>',
                  lambda m: m[1] + '<option value="">All sections</option>' + ''.join('<option>' + esc(v) + '</option>' for v in kinds) + '</select>', text, flags=re.S)
    coverage = portal / "search-coverage.html"
    text = text.replace('<div data-search-results></div>', '<p><a href="' + rel(coverage, search) + '">What is indexed and what is not</a></p><div data-search-results></div>')
    write(search, simplify_search_markup(text))
    catalog_by_route = {i["route"]: i for i in items if not i["id"].startswith("text-")}
    for path in sorted(portal.rglob("*.html")):
        if path == search or path == coverage:
            continue
        raw = path.read_text(encoding="utf-8")
        metadata = catalog_by_route.get(rel(path, search))
        if metadata and not metadata.get("examId"): metadata = None
        if metadata:
            raw = re.sub(r'<section data-exam-search-metadata.*?</section>', '', raw, flags=re.S)
            panel = '<section data-exam-search-metadata class="section-block"><h2 id="exam-topics">Exam topics</h2><p>' + esc(metadata["metadataScope"]) + ' · ' + esc(metadata["date"]) + ' · ' + esc(metadata["variant"]) + '</p>'
            for field, title in (("algorithms", "Algorithms"), ("peripherals", "Hardware"), ("interrupts", "Interrupts"), ("timing", "Timing"), ("architecture", "ABI and memory")):
                if metadata.get(field):
                    panel += '<p><strong>' + title + ':</strong> ' + ' · '.join('<a href="' + rel(search, path) + '?' + esc(urlencode({"q": tag, "kind": "Past Exams"})) + '">' + esc(tag) + '</a>' for tag in metadata[field]) + '</p>'
            panel += '</section>'
            raw = raw.replace('<div class="page-body">', '<div class="page-body">' + panel, 1)
        if 'data-filter-scope' not in raw and 'data-api-nav-search' not in raw and 'data-asm-entry' not in raw:
            if metadata: write(path, raw)
            continue
        # These attributes are the only changes to existing browsing cards.
        def card(match):
            block = match[0]
            links = re.findall(r'<a\b[^>]*href="([^"]+)"', block)
            target = next((link for link in reversed(links) if ".html" in link), "")
            if target:
                resolved = (path.parent / unquote(urlsplit(html.unescape(target)).path)).resolve()
                canonical = rel(resolved, search)
                metadata = catalog_by_route.get(canonical, {})
                if metadata and 'data-component="' in block:
                    block = re.sub(r'data-component="[^"]*"', lambda m: 'data-component="' + esc("|".join(metadata.get("components", []))) + '"', block)
                block = re.sub(r' data-search-route="[^"]*"', '', block)
                block = block.replace('data-filter-item', 'data-filter-item data-search-route="' + esc(canonical) + '"', 1)
            return block
        raw = re.sub(r'<article\b[^>]*data-filter-item[^>]*>.*?</article>', card, raw, flags=re.S)
        if 'data-search-corpus' not in raw:
            raw = raw.replace('</head>', '<script data-search-corpus src="' + rel(assets / "portal-data.js", path) + '" defer></script>\n</head>')
        write(path, raw)
    body = '<section class="section-block"><h2>Search coverage</h2><p>' + str(report["indexedFiles"]) + ' files indexed; ' + str(report["pdfPages"]) + ' PDF pages with text; ' + str(report["sectionRecords"]) + ' content records. ' + str(report["duplicates"]) + ' duplicate contents share storage while retaining their source metadata.</p>'
    body += '<p>Search includes the maintained package and original/historical references. Personal working projects, backups, caches, and build output are excluded. Images, audio, and archives have searchable filenames and labels only; their contents are not transcribed or extracted.</p><p>Exam tags on an original PDF describe the whole paper, unless a question mapping is explicitly available. Original papers without a maintained answer remain labeled as such.</p>'
    for heading, entries in (("Text unavailable", report["unindexed"]), ("Attachments: names only", report["attachments"]), ("Exam sources without a maintained mapping", report["unmappedMaterial"])):
        body += '<h2>' + heading + '</h2><ul>'
        for entry in entries:
            path = context["ROOT"] / entry["path"]
            body += '<li><a href="' + rel(path, coverage) + '">' + esc(entry["path"]) + '</a>' + (' · page ' + str(entry["page"]) if "page" in entry else '') + ': ' + esc(entry.get("reason", "Original reference; no maintained solution mapping")) + '</li>'
        body += '</ul>'
    body += '</section>'
    write(coverage, context["page"](coverage, "Search coverage", "Included material and explicit search limitations.", body, [("Home", context["HOME"]), ("Search", search), ("Coverage", coverage)]))
