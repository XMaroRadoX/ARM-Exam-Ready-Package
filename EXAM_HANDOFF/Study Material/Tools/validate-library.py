import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "Exam Atlas and Code Patterns" / "ARM_EXAM_ATLAS"
PROJECTS = ROOT / "Solved Exams"

def load_csv(name):
    with (ATLAS / "indexes" / name).open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def main():
    exams = load_csv("exams.csv")
    questions = load_csv("questions.csv")
    patterns = load_csv("patterns.csv")
    links = load_csv("exam_pattern_links.csv")
    atlas = json.loads((ATLAS / "indexes" / "atlas.json").read_text(encoding="utf-8"))
    answer_collections = [p for p in PROJECTS.iterdir()
                if p.is_dir() and (p / "Answer Source").is_dir()]
    assert len(exams) == 23, len(exams)
    assert len(questions) == 48, len(questions)
    assert len(patterns) == 28, len(patterns)
    assert len(answer_collections) == 23, len(answer_collections)
    assert atlas["schema_version"] == "1.0"
    assert len({e["exam_id"] for e in exams}) == len(exams)
    assert len({q["question_id"] for q in questions}) == len(questions)
    assert all(re.fullmatch(r"E\d{4}-\d{2}-\d{2}(?:-[A-Z]\d)?", e["exam_id"]) for e in exams)
    assert all(re.fullmatch(r"PAT-[A-Z0-9-]+-\d{3}", p["pattern_id"]) for p in patterns)
    known_patterns = {p["pattern_id"] for p in patterns}
    known_questions = {q["question_id"] for q in questions}
    assert all(x["pattern_id"] in known_patterns and x["question_id"] in known_questions for x in links)
    for e in exams:
        card = ATLAS / "exams" / e["year"] / e["exam_id"][1:] / "EXAM_CARD.md"
        assert card.is_file(), card
    for p in patterns:
        page = ATLAS / "patterns" / p["category"] / f"{p['pattern_id']}.md"
        assert page.is_file(), page
    required = ["EXAM_MAPPING.md", "ADAPTATION_MAP.md", "CHANGE_BUDGET.md",
                "Answer Source/exam_asm.s", "Answer Source/exam_main.c",
                "Answer Source/exam_user.c", "Answer Source/exam_user.h"]
    for project in answer_collections:
        for item in required:
            assert (project / item).is_file(), project / item
    print(json.dumps({"exams":len(exams),"questions":len(questions),"patterns":len(patterns),
                      "links":len(links),"answer_collections":len(answer_collections),
                      "status":"STRUCTURAL_PASS"}, indent=2))

if __name__ == "__main__": main()
