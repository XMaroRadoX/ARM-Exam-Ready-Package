#!/usr/bin/env python3
"""Replace stale atlas source/project paths with portable handoff-relative paths."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


STUDY = Path(__file__).resolve().parents[1]
HANDOFF = STUDY.parent
ATLAS = STUDY / "Exam Atlas and Code Patterns" / "ARM_EXAM_ATLAS"
INDEXES = ATLAS / "indexes"
SOLUTIONS = STUDY / "Solved Exams"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def preferred(paths: list[Path]) -> Path:
    return sorted(paths, key=lambda p: ("ARM questions" in p.parts, len(p.parts), str(p).lower()))[0]


def main() -> None:
    exam_path = INDEXES / "exams.csv"
    question_path = INDEXES / "questions.csv"
    exams = list(csv.DictReader(exam_path.open(encoding="utf-8-sig", newline="")))
    questions = list(csv.DictReader(question_path.open(encoding="utf-8-sig", newline="")))
    pdfs = list((HANDOFF / "Exams").rglob("*.pdf"))
    by_hash: dict[str, list[Path]] = {}
    for pdf in pdfs:
        by_hash.setdefault(sha256(pdf), []).append(pdf)

    exam_by_id: dict[str, dict[str, str]] = {}
    for exam in exams:
        matches = by_hash.get(exam["source_sha256"].strip().lower(), [])
        if not matches:
            old_relative = exam["source_pdf"].replace("Material (8)\\", "")
            candidate = HANDOFF / old_relative
            if not candidate.is_file():
                raise FileNotFoundError(f"No current PDF for {exam['exam_id']}")
            matches = [candidate]
        source = preferred(matches)
        actual_hash = sha256(source)
        solution = next(
            (path for path in SOLUTIONS.iterdir() if path.is_dir() and path.name.startswith(exam["date"])),
            None,
        )
        if solution is None:
            raise FileNotFoundError(f"No answer collection for {exam['exam_id']}")
        exam["source_pdf"] = source.relative_to(HANDOFF).as_posix()
        exam["source_sha256"] = actual_hash
        exam["project"] = f"Study Material/Solved Exams/{solution.name}"
        exam_by_id[exam["exam_id"]] = exam

    for question in questions:
        exam = exam_by_id[question["exam_id"]]
        question["source_pdf"] = exam["source_pdf"]
        question["source_sha256"] = exam["source_sha256"]

    write_csv(exam_path, exams)
    write_csv(question_path, questions)

    atlas_json_path = INDEXES / "atlas.json"
    data = json.loads(atlas_json_path.read_text(encoding="utf-8"))
    for exam in data.get("exams", []):
        current = exam_by_id[exam["exam_id"]]
        exam["source_pdf"] = current["source_pdf"]
        exam["source_sha256"] = current["source_sha256"]
        exam["project"] = current["project"]
    for question in data.get("questions", []):
        current = exam_by_id[question["exam_id"]]
        question["source_pdf"] = current["source_pdf"]
        question["source_sha256"] = current["source_sha256"]
    atlas_json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for exam_id, exam in exam_by_id.items():
        card = ATLAS / "exams" / exam["year"] / exam_id[1:] / "EXAM_CARD.md"
        lines = card.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if line.startswith("- Source PDF:"):
                lines[index] = f"- Source PDF: `{exam['source_pdf']}`"
            elif line.startswith("- SHA-256:"):
                lines[index] = f"- SHA-256: `{exam['source_sha256']}`"
            elif line.startswith("- Project:"):
                lines[index] = f"- Answer collection: `{exam['project']}`"
        card.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Updated {len(exams)} exams, {len(questions)} questions and {len(exams)} exam cards")


if __name__ == "__main__":
    main()
