#!/usr/bin/env python3
"""Render one contact sheet per indexed ARM exam for complete visual review."""

from __future__ import annotations

import csv
import hashlib
import os
import re
import tempfile
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw


PACKAGE = Path(__file__).resolve().parents[3]
HANDOFF = PACKAGE / "EXAM_HANDOFF"
ATLAS = HANDOFF / "Study Material" / "Exam Atlas and Code Patterns" / "ARM_EXAM_ATLAS"
OUTPUT = Path(tempfile.gettempdir()) / "arm-exam-paper-visual-audit"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (ATLAS / "indexes" / "exams.csv").open(encoding="utf-8-sig", newline="") as source:
        exams = list(csv.DictReader(source))
    pdfs = list((HANDOFF / "Exams").rglob("*.pdf"))
    by_hash = {digest(path): path for path in pdfs}

    for exam in exams:
        path = by_hash.get(exam["source_sha256"].strip().lower())
        if path is None:
            candidate = HANDOFF / exam["source_pdf"].replace("Material (8)\\", "")
            path = candidate if candidate.exists() else None
        if path is None:
            print(f"MISSING {exam['exam_id']}")
            continue

        document = pdfium.PdfDocument(str(path))
        rendered = [page.render(scale=1.15).to_pil().convert("RGB") for page in document]
        width = max(image.width for image in rendered)
        label_height = 44
        height = sum(image.height + label_height for image in rendered)
        sheet = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(sheet)
        y = 0
        for index, image in enumerate(rendered, start=1):
            draw.text((8, y + 8), f"{exam['exam_id']} — page {index}/{len(rendered)}", fill="black")
            y += label_height
            sheet.paste(image, (0, y))
            y += image.height
        destination = OUTPUT / f"{safe_name(exam['exam_id'])}.jpg"
        sheet.save(destination, quality=88, optimize=True)
        print(destination)


if __name__ == "__main__":
    main()
