#!/usr/bin/env python3
"""Generate reproducible, file-level inventories used by the exam-readiness audit."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

from pypdf import PdfReader


PACKAGE = Path(__file__).resolve().parents[3]
HANDOFF = PACKAGE / "EXAM_HANDOFF"
STUDY = HANDOFF / "Study Material"
ATLAS = STUDY / "Exam Atlas and Code Patterns" / "ARM_EXAM_ATLAS"
REPORTS = STUDY / "Tests and Reports" / "Repository Audit"
PROJECT = HANDOFF / "ARM_Exam_Project"
SOLUTIONS = STUDY / "Solved Exams"
PROFESSOR_TEMPLATES = PACKAGE.parent / "Keil Templates" / "REVISED_EXTRACTED"

TEXT_SUFFIXES = {
    ".c", ".h", ".s", ".asm", ".inc", ".md", ".txt", ".ini", ".csv",
    ".json", ".uvprojx", ".uvoptx", ".scvd", ".xml", ".map", ".lst",
}
GENERATED_PARTS = {"Objects", "Listings", "RTE", "DebugConfig"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            pass
    return "", "binary"


def classify(path: Path, root: Path) -> str:
    relative = path.relative_to(root)
    if any(part in GENERATED_PARTS for part in relative.parts):
        return "GENERATED_OR_TOOL_STATE"
    if path.suffix.lower() in {".o", ".d", ".axf", ".htm", ".crf", ".dep"}:
        return "GENERATED_BUILD_OUTPUT"
    if path.suffix.lower() in {".c", ".h", ".s", ".asm", ".inc"}:
        return "SOURCE"
    if path.suffix.lower() in {".uvprojx", ".uvoptx", ".ini", ".scvd", ".xml"}:
        return "PROJECT_CONFIGURATION"
    if path.suffix.lower() in {".md", ".txt", ".csv", ".json"}:
        return "DOCUMENTATION_OR_DATA"
    return "BINARY_OR_OTHER"


def inspect_tree(scope: str, root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not root.exists():
        return rows
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda p: str(p).lower()):
        category = classify(path, root)
        text = ""
        encoding = "not_text"
        if path.suffix.lower() in TEXT_SUFFIXES:
            text, encoding = read_text(path)
        exports = sorted(set(re.findall(r"(?im)^\s*EXPORT\s+([A-Za-z_$][\w$]*)", text)))
        imports = sorted(set(re.findall(r"(?im)^\s*IMPORT\s+([A-Za-z_$][\w$]*)", text)))
        c_main = bool(re.search(r"(?m)^\s*(?:int|void)\s+main\s*\(", text))
        reset = bool(re.search(r"(?m)^\s*(?:EXPORT\s+)?Reset_Handler\b", text))
        handlers = sorted(set(re.findall(r"(?m)^\s*(?:void\s+)?([A-Za-z_]\w*(?:IRQHandler|Handler))\s*(?:PROC|\()", text)))
        placeholder = bool(re.search(r"(?i)your\s+(?:code|solution)|insert\s+(?:code|solution)|exam_asm_example", text))
        rows.append({
            "scope": scope,
            "relative_path": path.relative_to(root).as_posix(),
            "category": category,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "text_encoding": encoding,
            "line_count": len(text.splitlines()) if text else 0,
            "defines_c_main": c_main,
            "defines_reset_handler": reset,
            "assembly_exports": ";".join(exports),
            "assembly_imports": ";".join(imports),
            "handlers": ";".join(handlers),
            "placeholder_marker": placeholder,
        })
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else ["scope", "relative_path"]
    with path.open("w", newline="", encoding="utf-8-sig") as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def map_exam_pdfs() -> list[dict[str, object]]:
    with (ATLAS / "indexes" / "exams.csv").open(encoding="utf-8-sig", newline="") as source:
        exams = list(csv.DictReader(source))
    pdfs = list((HANDOFF / "Exams").rglob("*.pdf"))
    hashes: dict[str, list[Path]] = {}
    for pdf in pdfs:
        hashes.setdefault(sha256(pdf).lower(), []).append(pdf)
    rows: list[dict[str, object]] = []
    for exam in exams:
        expected_hash = exam["source_sha256"].strip().lower()
        matches = hashes.get(expected_hash, [])
        # A historical CSV typo omitted the final hex digit from one otherwise
        # unambiguous SHA-256 value. Preserve that fact but still identify it.
        if not matches and len(expected_hash) == 63:
            matches = [pdf for digest, paths in hashes.items() if digest.startswith(expected_hash) for pdf in paths]
        page_count = 0
        extracted_characters = 0
        if matches:
            reader = PdfReader(str(matches[0]))
            page_count = len(reader.pages)
            extracted_characters = sum(len(page.extract_text() or "") for page in reader.pages)
        rows.append({
            "exam_id": exam["exam_id"],
            "variant": exam["variant"],
            "expected_sha256": exam["source_sha256"],
            "matched_pdf_count": len(matches),
            "current_source_pdf": ";".join(path.relative_to(HANDOFF).as_posix() for path in matches),
            "page_count": page_count,
            "extracted_text_characters": extracted_characters,
            "project_directory": next((p.name for p in SOLUTIONS.iterdir() if p.is_dir() and p.name.startswith(exam["date"])), ""),
        })
    return rows


def main() -> None:
    current = inspect_tree("ARM_Exam_Project", PROJECT)
    solutions = inspect_tree("Solved_Exams", SOLUTIONS)
    templates = inspect_tree("Professor_Templates", PROFESSOR_TEMPLATES)
    write_csv(REPORTS / "CURRENT_PROJECT_FILES.csv", current)
    write_csv(REPORTS / "SOLVED_EXAM_FILES.csv", solutions)
    write_csv(REPORTS / "PROFESSOR_TEMPLATE_FILES.csv", templates)
    write_csv(REPORTS / "EXAM_SOURCE_PDF_MAP.csv", map_exam_pdfs())
    summary = [
        {"scope": "ARM_Exam_Project", "files": len(current), "text_files_read": sum(row["text_encoding"] != "not_text" for row in current)},
        {"scope": "Solved_Exams", "files": len(solutions), "text_files_read": sum(row["text_encoding"] != "not_text" for row in solutions)},
        {"scope": "Professor_Templates", "files": len(templates), "text_files_read": sum(row["text_encoding"] != "not_text" for row in templates)},
    ]
    write_csv(REPORTS / "AUDIT_SCOPE_SUMMARY.csv", summary)
    for row in summary:
        print(f"{row['scope']}: {row['files']} files; {row['text_files_read']} text files read")


if __name__ == "__main__":
    main()
