#!/usr/bin/env python3
"""Verify the canonical offline ARM exam workstation."""

from __future__ import annotations

import csv
import html
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from canonical_api_reference import API_DOCS, SCENARIOS, VALUE_GUIDANCE


ROOT = Path(__file__).resolve().parents[3]
LIBRARY = ROOT / "01_EXAM_READY" / "FRESH_SOLVED_ARM_EXAMS"
MAINTENANCE = LIBRARY / '99_MAINTENANCE'
GUIDES = LIBRARY / "01_GUIDES_AND_INDEXES"
COURSE = GUIDES / "EXAM_COURSE"
PORTAL = GUIDES / "PORTAL"
HOME = ROOT / "START_HERE.html"
API_HEADER = ROOT / "01_EXAM_READY" / "02_STARTING_TEMPLATES" / "Official Combined Exam API" / "Source" / "exam_api" / "exam_api.h"
RAW = LIBRARY / "03_COPY_PASTE_LIBRARY" / "CANONICAL_WORKSTATION"
STARTING_TEMPLATES = ROOT / "01_EXAM_READY" / "02_STARTING_TEMPLATES"
EXPECTED_NAV = ["Home", "Courses", "In the Exam", "Past Exams", "Solution Patterns", "API", "ASM Reference", "Algorithms", "Guides"]
EXPECTED_COUNTS = {"exams": 23, "questions": 48, "patterns": 85, "api": len(API_DOCS), "algorithms": 0, "peripheral_lessons": 14}
SAMPLE_QUERIES = ["Mastermind", "fifth argument", "Timer0 ADC", "graph shortest path", "quicksort", "exam_timer_config_ms", "exam_adc_take"]
BANNED_VISIBLE = [
    r"\bPAT-(?:[A-Z0-9]+-)+\d+\b", r"\bpat_(?:alg|data|ds|mem)_[a-z0-9_]+\b",
    r"\bsha-?256\b", r"\bverification code\b", r"\bbuild log\b", r"\bevidence tab\b",
    r"\btemplate[-_ ]generation\b", r"\bphysical_board_not_tested\b", r"\bcompile_only\b",
    r"\bStudy\s*/\s*Library\s*/\s*Board\b", r"\b[a-f0-9]{64}\b",
    r"Declared by the sole Official Combined Exam API",
    r"consult the canonical quick reference for the exact meaning",
]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.iframes = 0
        self.ids: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.controls: list[tuple[str, dict[str, str], bool]] = []
        self.label_depth = 0
        self.nav_depth = 0
        self.nav_link_depth = 0
        self.nav_link_text: list[str] = []
        self.nav_labels: list[str] = []
        self.nav_link_href = ""
        self.nav_links: list[tuple[str, str]] = []
        self.visible: list[str] = []
        self.hidden_depth = 0

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key.lower(): value or "" for key, value in attrs_list}
        tag = tag.lower()
        if tag == "h1": self.h1 += 1
        if tag == "iframe": self.iframes += 1
        if attrs.get("id"): self.ids.append(attrs["id"])
        for name in ("href", "src", "data-src"):
            if attrs.get(name): self.links.append((name, attrs[name]))
        if tag == "label": self.label_depth += 1
        if tag in {"input", "select", "textarea", "button"}: self.controls.append((tag, attrs, self.label_depth > 0))
        if tag == "nav" and attrs.get("aria-label") == "Primary navigation": self.nav_depth = 1
        elif self.nav_depth: self.nav_depth += 1
        if self.nav_depth and tag == "a":
            self.nav_link_depth = 1
            self.nav_link_text = []
            self.nav_link_href = attrs.get("href", "")
        elif self.nav_link_depth: self.nav_link_depth += 1
        if tag in {"script", "style"} or "hidden" in attrs or attrs.get("aria-hidden") == "true": self.hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.nav_link_depth:
            self.nav_link_depth -= 1
            if self.nav_link_depth == 0:
                label = " ".join(self.nav_link_text).strip()
                self.nav_labels.append(label)
                self.nav_links.append((label, self.nav_link_href))
        if self.nav_depth: self.nav_depth -= 1
        if tag == "label" and self.label_depth: self.label_depth -= 1
        if tag in {"script", "style"} and self.hidden_depth: self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.nav_link_depth: self.nav_link_text.append(data)
        if not self.hidden_depth: self.visible.append(data)


def csv_count(path: Path) -> int:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def api_names(text: str) -> set[str]:
    return set(re.findall(r"\b(exam_[A-Za-z0-9_]+)\s*\(", text))


def read_manifest() -> list[dict[str, object]]:
    text = (PORTAL / "assets" / "portal-data.js").read_text(encoding="utf-8")
    match = re.fullmatch(r"\s*window\.ARM_PORTAL_DATA=(.*);\s*", text, re.S)
    if not match: raise ValueError("portal-data.js is not a classic JavaScript global")
    return json.loads(match.group(1))["items"]


def search_matches(items: list[dict[str, object]], query: str) -> list[str]:
    words = str(query).lower().split()
    found = []
    for item in items:
        fields = [item.get("title", ""), item.get("summary", "")]
        for key in ("aliases", "topics", "components"):
            if isinstance(item.get(key), list): fields += item[key]
        haystack = " ".join(map(str, fields)).lower()
        if all(word in haystack for word in words): found.append(str(item.get("title", "")))
    return found


def verify() -> list[str]:
    errors: list[str] = []
    template_directories = sorted(path.name for path in STARTING_TEMPLATES.iterdir() if path.is_dir())
    expected_directories = ["Official Combined Exam API", "Official Combined Exam API Reference"]
    if template_directories != expected_directories:
        errors.append(f"Starting Templates must contain the project and its reference documents; found {template_directories}")
    reference_directory = STARTING_TEMPLATES / "Official Combined Exam API Reference"
    if list(reference_directory.rglob("*.uvproj*")):
        errors.append("API Reference must contain documentation, not another project template")
    for obsolete in (PORTAL / "combinations", RAW / "tool-combinations"):
        if obsolete.exists(): errors.append(f"Obsolete generated section still exists: {obsolete.relative_to(ROOT)}")
    if not HOME.exists() or not PORTAL.exists(): return ["Portal has not been generated"]
    pages = [HOME] + sorted(PORTAL.rglob("*.html"))
    actual_counts = {
        "exams": csv_count(COURSE / "REVIEWED_EXAM_INDEX.csv"),
        "questions": csv_count(GUIDES / "QUESTION_INDEX.csv"),
        "patterns": len(list((PORTAL / "patterns").glob("*.html"))) - 1,
        "api": len(list((PORTAL / "api").glob("*.html"))) - 1,
        "algorithms": len([p for p in (PORTAL / "algorithms").glob("*.html") if p.name not in {"index.html", "basic-exam-algorithms.html"}]),
        "peripheral_lessons": len(list((PORTAL / "guides").glob("peripheral-*.html"))),
    }
    expected_counts=dict(EXPECTED_COUNTS)
    destinations=json.loads((MAINTENANCE / 'SECTION_DESTINATIONS.json').read_text()) if (MAINTENANCE / 'SECTION_DESTINATIONS.json').exists() else {}
    scenarios=json.loads((MAINTENANCE / 'SCENARIO_MANIFEST.json').read_text()) if destinations else []
    inventory=json.loads((MAINTENANCE / 'ALGORITHM_INVENTORY.json').read_text()) if (MAINTENANCE / 'ALGORITHM_INVENTORY.json').exists() else []
    original_algorithms={'algorithms/'+r['slug']+'.html' for r in inventory}
    added_algorithms={r['route'] for r in destinations.values() if r['section']=='Algorithms'}-original_algorithms
    expected_counts['algorithms']=len(inventory)+len(added_algorithms)
    if destinations:
        expected_counts['patterns']=len(destinations)+len(scenarios)+1
    if actual_counts != expected_counts: errors.append(f"Coverage differs: {actual_counts}; expected {expected_counts}")
    expected_pages = {"exams": 72, "patterns": 86, "api": len(API_DOCS) + 1, "algorithms": expected_counts['algorithms'] + 2, "guides": 24, "asm": 1}
    if destinations:
        expected_pages.update(patterns=expected_counts['patterns']+1,algorithms=expected_counts['algorithms']+2,guides=24+sum(r['section']=='Guides' for r in destinations.values()),asm=1+sum(r['section']=='ASM Reference' for r in destinations.values()))
    for section, count in expected_pages.items():
        actual = len(list((PORTAL / section).glob("*.html")))
        if actual != count: errors.append(f"{section} has {actual} pages; expected {count}")

    parser_by_path: dict[Path, PageParser] = {}
    for path in pages:
        text = path.read_text(encoding="utf-8", errors="replace")
        parser = PageParser()
        try: parser.feed(text)
        except Exception as exc: errors.append(f"{path.relative_to(ROOT)} cannot be parsed: {exc}"); continue
        parser_by_path[path.resolve()] = parser
        label = path.relative_to(ROOT)
        if parser.h1 != 1: errors.append(f"{label} has {parser.h1} h1 elements")
        if parser.iframes: errors.append(f"{label} contains {parser.iframes} iframe elements")
        duplicates = [value for value, count in Counter(parser.ids).items() if count > 1]
        if duplicates: errors.append(f"{label} has duplicate IDs: {duplicates[:5]}")
        if parser.nav_labels != EXPECTED_NAV: errors.append(f"{label} navigation differs: {parser.nav_labels}")
        api_href = dict(parser.nav_links).get("API", "")
        api_target = (path.parent / unquote(urlsplit(api_href).path)).resolve() if api_href else None
        if api_target != (PORTAL / "api" / "index.html").resolve():
            errors.append(f"{label} API navigation does not target the portal API page")
        visible = " ".join(parser.visible)
        for pattern in BANNED_VISIBLE:
            if re.search(pattern, visible, re.I): errors.append(f"{label} shows banned text matching {pattern}"); break
        if re.search(r">\s*Open\s*<", text, re.I): errors.append(f"{label} uses vague Open link text")
        for tag, attrs, wrapped in parser.controls:
            if attrs.get("type") == "hidden": continue
            labelled = wrapped or attrs.get("aria-label") or attrs.get("aria-labelledby") or (attrs.get("id") and re.search(rf'<label\b[^>]*for=["\']{re.escape(attrs["id"])}["\']', text, re.I))
            if tag != "button" and not labelled: errors.append(f"{label} has an unlabelled {tag}")

    for source in pages:
        parser = parser_by_path.get(source.resolve())
        if not parser: continue
        for attr, url in parser.links:
            parts = urlsplit(url)
            if parts.scheme or url.startswith(("//", "mailto:", "javascript:", "data:")): continue
            if url.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", unquote(url)):
                errors.append(f"{source.relative_to(ROOT)} has non-relative {attr}: {url}"); continue
            target = (source.parent / unquote(parts.path)).resolve() if parts.path else source.resolve()
            try: target.relative_to(ROOT.resolve())
            except ValueError: errors.append(f"{source.relative_to(ROOT)} links outside package: {url}"); continue
            if not target.exists(): errors.append(f"{source.relative_to(ROOT)} has missing target: {url}"); continue
            if parts.fragment and target.suffix.lower() in {".html", ".htm"}:
                target_parser = parser_by_path.get(target)
                if target_parser is None:
                    target_parser = PageParser(); target_parser.feed(target.read_text(encoding="utf-8", errors="replace")); parser_by_path[target] = target_parser
                if unquote(parts.fragment) not in target_parser.ids: errors.append(f"{source.relative_to(ROOT)} has missing fragment: {url}")

    header_text = API_HEADER.read_text(encoding="utf-8", errors="replace")
    declared = api_names(header_text)
    portal_calls = set()
    for path in pages:
        portal_calls |= api_names(path.read_text(encoding="utf-8", errors="replace"))
    unknown_portal_calls = portal_calls - declared
    if unknown_portal_calls:
        errors.append(f"Student pages use undeclared API calls: {sorted(unknown_portal_calls)}")
    documented = {path.stem.replace("-", "_") for path in (PORTAL / "api").glob("exam-*.html")}
    if declared != documented: errors.append(f"API pages differ from header: missing {sorted(declared-documented)}, extra {sorted(documented-declared)}")
    api_index_text = (PORTAL / "api" / "index.html").read_text(encoding="utf-8", errors="replace")
    for marker in ["Required include and initialization", "Ownership and data flow", "Exam-grounded values and scenarios", "Status values", "Public types", "Public constants", "Public fault globals", "Capabilities not present in the current API", "Function groups"]:
        if marker not in api_index_text: errors.append(f"API index lacks section: {marker}")
    if "id=\"complete-reference\"" in api_index_text or "Complete API documentation</h2>" in api_index_text:
        errors.append("API index still contains the old monolithic documentation dump")
    gap_report = API_HEADER.parents[2].with_name("Official Combined Exam API Reference") / "API_GAP_REPORT.md"
    if not gap_report.exists(): errors.append("Current API gap report is missing")
    if set(VALUE_GUIDANCE) != declared:
        errors.append(f"Value guidance differs from header: missing {sorted(declared-set(VALUE_GUIDANCE))}, extra {sorted(set(VALUE_GUIDANCE)-declared)}")
    scenario_functions = {name for scenario in SCENARIOS for name in scenario["functions"]}
    if scenario_functions != declared:
        errors.append(f"Scenario coverage differs from header: missing {sorted(declared-scenario_functions)}, extra {sorted(scenario_functions-declared)}")
    for scenario in SCENARIOS:
        for exam in scenario["exams"]:
            exam_page = PORTAL / "exams" / f"{exam}.html"
            if not exam_page.exists(): errors.append(f"Scenario {scenario['id']} cites missing exam page: {exam_page.relative_to(ROOT)}")
    for path in (PORTAL / "api").glob("exam-*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        name = path.stem.replace("-", "_")
        required = ["Exact declaration", "Contract", "Preconditions", "Parameters", "Return value", "Side effects", "Timing and call context", "Typical exam values", "Scenario usage", "Minimal example", "Common mistake", "Exam use", "Related functions", "Read the current exam_api.h declaration"]
        missing = [marker for marker in required if marker not in text]
        if missing: errors.append(f"{path.relative_to(ROOT)} lacks API sections: {missing}")
        if text.count("data-api-entry") != len(declared):
            errors.append(f"{path.relative_to(ROOT)} sidebar does not list all {len(declared)} functions")
        doc = API_DOCS.get(name)
        if not doc:
            errors.append(f"{path.relative_to(ROOT)} has no canonical function documentation")
            continue
        visible = html.unescape(re.sub(r"<[^>]+>", " ", text))
        for field in ("summary", "preconditions", "returns", "side_effects", "context", "mistake", "exam_note"):
            if re.sub(r"\s+", " ", str(doc[field])).strip() not in re.sub(r"\s+", " ", visible):
                errors.append(f"{path.relative_to(ROOT)} omits canonical {field}")
        for param_name, param_doc in doc["params"].items():
            if param_name not in visible or str(param_doc["description"]) not in visible:
                errors.append(f"{path.relative_to(ROOT)} omits parameter contract for {param_name}")
        for item in VALUE_GUIDANCE[name]:
            if str(item["value"]) not in visible or str(item["basis"]) not in visible:
                errors.append(f"{path.relative_to(ROOT)} omits canonical value guidance: {item['value']}")
        if not any(str(scenario["title"]) in visible for scenario in SCENARIOS if name in scenario["functions"]):
            errors.append(f"{path.relative_to(ROOT)} omits canonical scenario usage")
    debounce_text = (PORTAL / "api" / "exam-debounce-config.html").read_text(encoding="utf-8", errors="replace")
    for marker in ["10 ms sample, 50 ms confirmation", "Recommended maintained recipe, not a literal past-paper constant", "this exact 10/50 pair is not claimed as a literal paper constant"]:
        if marker not in debounce_text: errors.append(f"Debounce reference lacks evidence-safe marker: {marker}")
    if api_index_text.count("data-api-entry") != len(declared):
        errors.append(f"API index sidebar does not list all {len(declared)} functions")

    solution_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in (ROOT / "03_ADDITIONAL_STUDY_MATERIAL" / "03 - Solved Exams").rglob("*.c"))
    solution_calls = api_names(solution_text)
    unknown_solution_calls = solution_calls - declared
    if unknown_solution_calls: errors.append(f"Exam solutions use undeclared API calls: {sorted(unknown_solution_calls)}")
    quick_reference = (API_HEADER.parents[2].with_name("Official Combined Exam API Reference") / "EXAM_API_QUICK_REFERENCE.md").read_text(encoding="utf-8", errors="replace")
    undocumented = {name for name in declared if not re.search(rf"\b{re.escape(name)}\b", quick_reference)}
    if undocumented: errors.append(f"Quick reference omits public API calls: {sorted(undocumented)}")

    algorithm_sources = sorted((RAW / "algorithms").glob("*/reference.c"))
    if len(algorithm_sources) < 100: errors.append(f"Found {len(algorithm_sources)} algorithm sources; expected at least 100")
    if len(algorithm_sources) != len(inventory): errors.append(f"Expected {len(inventory)} algorithm references; found {len(algorithm_sources)}")
    fundamentals = [row for row in inventory if row.get("fundamentals_group")]
    if len(fundamentals) != 80: errors.append(f"Expected 80 one-prompt fundamentals; found {len(fundamentals)}")
    if len({row.get('slug') for row in fundamentals}) != len(fundamentals): errors.append("Fundamentals inventory contains duplicate slugs")
    basics_path = PORTAL / "algorithms" / "basic-exam-algorithms.html"
    basics_text = basics_path.read_text(encoding="utf-8", errors="replace") if basics_path.exists() else ""
    if not basics_text: errors.append("Basic Exam Algorithms index is missing")
    for row in fundamentals:
        if f'{row["slug"]}.html' not in basics_text: errors.append(f'Basic index omits {row["slug"]}')
    for path in algorithm_sources:
        for artifact in ("implementation.s","test_vectors.c"):
            if not (path.parent/artifact).is_file(): errors.append(f"{path.parent.name}: missing {artifact}")
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"\b(TODO|placeholder|dummy solution)\b", text, re.I): errors.append(f"{path.relative_to(ROOT)} contains placeholder content")

    question_pages = [p for p in (PORTAL / "exams").glob("*.html") if p.name != "index.html" and re.match(r"\d{4}-", p.stem)]
    if len(question_pages) != 48: errors.append(f"Found {len(question_pages)} dedicated question pages; expected 48")
    for path in question_pages:
        text = path.read_text(encoding="utf-8", errors="replace")
        required = ["Bounded solution method", "Common wrong answers", "Source status", "View original exam PDF", "Show complete"]
        if any(marker not in text for marker in required): errors.append(f"{path.relative_to(ROOT)} lacks a complete question answer")
    manifest_path = RAW / "exam-solutions" / "manifest.json"
    if not manifest_path.exists(): errors.append("Canonical question manifest is missing")
    else:
        question_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if len(question_manifest.get("questions", [])) != 48: errors.append("Canonical question manifest does not contain 48 questions")

    try: items = read_manifest()
    except Exception as exc: errors.append(str(exc)); items = []
    required_keys = {"id", "kind", "title", "summary", "route", "examHistory", "languages", "components", "topics", "aliases", "relatedIds"}
    ids = [str(item.get("id", "")) for item in items]
    if len(ids) != len(set(ids)): errors.append("Search manifest contains duplicate IDs")
    for number, item in enumerate(items):
        missing = required_keys - item.keys()
        if missing: errors.append(f"Search item {number} lacks {sorted(missing)}")
        target = ((PORTAL / "search.html").parent / unquote(urlsplit(str(item.get("route", ""))).path)).resolve()
        if not target.exists(): errors.append(f"Search item {item.get('title')} has missing route")
    known_ids = set(ids)
    for item in items:
        unknown = [related for related in item.get("relatedIds", []) if related not in known_ids]
        if unknown: errors.append(f"Search item {item.get('title')} has unknown related IDs: {unknown}")
    for query in SAMPLE_QUERIES:
        if not search_matches(items, query): errors.append(f"Search query has no result: {query}")
    return errors


def main() -> int:
    errors = verify()
    if errors:
        print(f"Student portal verification failed with {len(errors)} issue(s):")
        for error in errors[:250]: print(f"- {error}")
        if len(errors) > 250: print(f"- ...and {len(errors)-250} more")
        return 1
    print("Student portal verification passed")
    algorithm_count=len(json.loads((MAINTENANCE / 'ALGORITHM_INVENTORY.json').read_text()))
    pattern_count = len(list((PORTAL / "patterns").glob("*.html"))) - 1
    print(f"Coverage: 23 exams, 48 questions, {pattern_count} pattern/scenario pages, {len(API_DOCS)} API calls, {algorithm_count} canonical algorithms, 14 peripheral lessons, 9 goal guides")
    print(f"Validated {1 + len(list(PORTAL.rglob('*.html')))} student pages and {len(read_manifest())} search items")
    print("Representative searches passed: " + ", ".join(SAMPLE_QUERIES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
