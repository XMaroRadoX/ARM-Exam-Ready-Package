#!/usr/bin/env python3
"""Verify page preservation, search text and render visual QA contact sheets."""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw
from pypdf import PdfReader


STUDY = Path(__file__).resolve().parents[1]
HANDOFF = STUDY.parent
ARM = HANDOFF / "ARM"
OUT = STUDY / "output" / "pdf"
TMP = Path(tempfile.gettempdir()) / "arm-exam-pdfs" / "qa"
TMP.mkdir(parents=True, exist_ok=True)


def natural_key(path: Path):
    match = re.match(r"(\d+)(?:_|\b)", path.name)
    if match:
        return (0, int(match.group(1)), path.name.lower())
    support = {"guide_to_keil_templates.pdf": 0, "lpc176x_usermanual.pdf": 1, "landtiger schematic.pdf": 2}
    return (1, support.get(path.name.lower(), 99), path.name.lower())


def contact_sheet(pdf_path: Path, pages: list[int], destination: Path, columns: int = 3) -> None:
    document = pdfium.PdfDocument(str(pdf_path))
    thumbs=[]
    for page_number in pages:
        image=document[page_number].render(scale=0.45).to_pil().convert("RGB")
        image.thumbnail((400,560))
        canvas=Image.new("RGB",(420,600),"white"); canvas.paste(image,((420-image.width)//2,30))
        ImageDraw.Draw(canvas).text((8,8),f"page {page_number+1}",fill="black"); thumbs.append(canvas)
    rows=(len(thumbs)+columns-1)//columns
    sheet=Image.new("RGB",(columns*420,rows*600),"#D9DDE3")
    for index,image in enumerate(thumbs): sheet.paste(image,((index%columns)*420,(index//columns)*600))
    sheet.save(destination,quality=88)


def main() -> None:
    guide_path=OUT/"ARM_ASSEMBLY_INSTRUCTION_HANDBOOK.pdf"
    library_path=OUT/"ARM_COMPLETE_ORDERED_LIBRARY.pdf"
    guide=PdfReader(str(guide_path)); library=PdfReader(str(library_path))
    guide_text="\n".join(page.extract_text() or "" for page in guide.pages)
    required=["MOV, MOVS","LDRB, STRB","LDRSB","ADD, ADDS","UDIV, SDIV","CMP, CMN","BLO/BHS","BL","SVC","MRS, MSR","PUSH, POP","AREA"]
    missing=[term for term in required if term not in guide_text]
    if missing: raise AssertionError(f"Guide search terms missing: {missing}")

    source_pdfs=sorted(ARM.rglob("*.pdf"),key=natural_key)
    combined_index=1
    starts=[]; compared=0
    for source_path in source_pdfs:
        source=PdfReader(str(source_path)); starts.append(combined_index)
        for source_page in source.pages:
            left=(source_page.extract_text() or "").replace("\r\n","\n")
            right=(library.pages[combined_index].extract_text() or "").replace("\r\n","\n")
            if left != right:
                raise AssertionError(f"Text mismatch at {source_path}, source page {compared+1}")
            combined_index+=1; compared+=1
    if combined_index != len(library.pages): raise AssertionError((combined_index,len(library.pages)))
    if len(library.outline) < len(source_pdfs)+1: raise AssertionError("Missing bookmarks")

    contact_sheet(guide_path,list(range(len(guide.pages))),TMP/"instruction-handbook-all-pages.jpg",columns=2)
    sample_pages=[0]+starts+[len(library.pages)-1]
    contact_sheet(library_path,sample_pages,TMP/"combined-library-index-and-boundaries.jpg",columns=3)
    print(f"PASS guide_pages={len(guide.pages)} library_pages={len(library.pages)} source_pages_compared={compared} bookmarks={len(library.outline)}")
    print(TMP/"instruction-handbook-all-pages.jpg")
    print(TMP/"combined-library-index-and-boundaries.jpg")


if __name__ == "__main__":
    main()
