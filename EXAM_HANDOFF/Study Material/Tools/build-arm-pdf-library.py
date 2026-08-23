#!/usr/bin/env python3
"""Build the searchable instruction handbook and lossless ordered ARM library."""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


STUDY = Path(__file__).resolve().parents[1]
HANDOFF = STUDY.parent
ARM = HANDOFF / "ARM"
OUT = STUDY / "output" / "pdf"
TMP = STUDY / "tmp" / "pdfs"
OUT.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

GUIDE_PDF = OUT / "ARM_ASSEMBLY_INSTRUCTION_HANDBOOK.pdf"
GUIDE_MD = OUT / "ARM_ASSEMBLY_INSTRUCTION_HANDBOOK.md"
LIBRARY_PDF = OUT / "ARM_COMPLETE_ORDERED_LIBRARY.pdf"


GROUPS = [
    ("Data movement and constants", [
        ("MOV, MOVS", "Copy a register or encodable immediate. MOVS updates N and Z; use MOV when flags must survive. Large constants may need MOVW/MOVT or LDR =constant.", "MOV R4, R0; MOVS R6, #0", "MOV cannot encode every 32-bit immediate. Do not use MOVS accidentally between CMP and a conditional branch."),
        ("MOVW, MOVT", "Build a 32-bit constant without a literal-pool load. MOVW writes the low half; MOVT writes the high half without changing the low half.", "MOVW R0, #0xCDEF; MOVT R0, #0x89AB", "Use when the assembler supports the Thumb-2 forms. Neither is a memory access."),
        ("ADR, ADRL", "Form the address of a nearby label using the current PC. ADRL is an assembler expansion for a wider range.", "ADR R0, table", "Range and alignment are assembler-dependent. LDR R0, =label is more general but uses a literal or relocation."),
        ("LDR Rd, =expression", "Assembler pseudo-instruction for an address or constant. It becomes MOV/MOVW/MOVT when possible or a PC-relative literal load.", "LDR R4, =outputData", "Keep LTORG far enough from executed code and within literal-load range. This is not the same as LDR Rd, [Rn]."),
        ("MRS, MSR", "Move from or to special registers such as APSR, CONTROL, MSP, PSP, PRIMASK, CFSR-related system state.", "MRS R0, APSR; MSR APSR_nzcvq, R1", "Only writable fields may be changed. Privileged registers require privileged execution. Preserve unrelated APSR bits when the paper requires them unchanged."),
    ]),
    ("Loads, stores, arrays and matrices", [
        ("LDR, STR", "Load or store a 32-bit word. Use for uint32_t/int arrays and stacked words.", "LDR R5, [R4, R6, LSL #2]; STR R5, [R0, #8]", "Word index scale is 2. Respect alignment. LDR changes no flags."),
        ("LDRB, STRB", "Load or store one unsigned byte. LDRB zero-extends into the register.", "LDRB R3, [R0], #1; STRB R3, [R1], #1", "Use LDRSB, not LDRB, when a signed int8_t comparison is required."),
        ("LDRSB", "Load a signed byte and sign-extend it to 32 bits.", "LDRSB R7, [R4, R6]", "This is why the insertion-sort answer orders negative bytes correctly."),
        ("LDRH, STRH", "Load or store a 16-bit halfword. LDRH zero-extends.", "LDRH R0, [R1, R2, LSL #1]", "Use LDRSH for signed int16_t data. Halfword index scale is 1."),
        ("LDRD, STRD", "Transfer a pair of consecutive words.", "LDRD R0, R1, [R2]", "Register pairing and address alignment constraints depend on the encoding. Do not assume it updates flags."),
        ("Pre/post indexing", "Combine a transfer with pointer movement. Pre-index changes the address before access; post-index accesses then changes it.", "LDRB R3, [R0], #1; STR R2, [R1, #4]!", "Writeback modifies the base register. Avoid unpredictable combinations where the base is also a transferred register."),
        ("LDM/STM, LDMIA/STMIA", "Transfer multiple registers, useful for blocks and context work.", "LDMIA R0!, {R2-R5}", "Register order follows register number, not textual order. The base writeback must be intentional."),
        ("PUSH, POP", "Stack aliases for storing/loading register lists. Save callee-saved registers and LR in non-leaf routines; return with POP {...,PC}.", "PUSH {R4-R7, LR}; ...; POP {R4-R7, PC}", "AAPCS requires SP to be 8-byte aligned at public call boundaries. Pushing an odd count of 32-bit registers misaligns SP unless compensated."),
    ]),
    ("Arithmetic", [
        ("ADD, ADDS", "Add operands. The S form updates N, Z, C and V.", "ADDS R0, R0, R1", "Use ADDS when the following decision needs flags; use ADD when existing flags must survive."),
        ("ADC, ADCS", "Add with the current carry flag. Combine with ADDS for multiword addition.", "ADDS R0, R0, R2; ADCS R1, R1, R3", "Carry-in must be established deliberately. ADC without S preserves flags."),
        ("SUB, SUBS", "Subtract. SUBS updates flags and is also common for countdown loops.", "SUBS R2, R2, #1; BNE loop", "After CMP/SUBS, unsigned and signed branches interpret the same flags differently."),
        ("SBC, SBCS", "Subtract with borrow using inverted carry semantics. Combine with SUBS for multiword subtraction.", "SUBS R0, R0, R2; SBCS R1, R1, R3", "C=1 means no borrow. This is a frequent source of reversed logic."),
        ("RSB, RSBS", "Reverse subtraction: operand2 minus operand1. With zero it forms two's-complement negation.", "RSBS R0, R0, #0", "Negating 0x80000000 overflows in signed arithmetic; inspect V if required."),
        ("MUL", "Multiply the low 32 bits of two operands.", "MUL R0, R0, R1", "High overflow is discarded. MUL does not replace UMULL/SMULL when the full 64-bit product is required."),
        ("MLA, MLS", "Multiply-accumulate or multiply-subtract. MLS is especially useful for remainder after division.", "UDIV R1, R0, R2; MLS R3, R1, R2, R0", "MLS computes accumulator minus product; verify operand order."),
        ("UDIV, SDIV", "Unsigned or signed 32-bit division.", "UDIV R7, R5, R10; SDIV R6, R0, R1", "They return a quotient only and do not set condition flags. Divide-by-zero behavior depends on CCR trapping. Papers may forbid SDIV and require a manual 64/32 algorithm."),
        ("UMULL, SMULL, UMLAL, SMLAL", "Produce or accumulate a full 64-bit result in a low/high register pair.", "UMULL R0, R1, R2, R3", "Low and high destinations must be distinct and chosen carefully. Signed and unsigned high halves differ."),
    ]),
    ("Bitwise operations and shifts", [
        ("AND, ANDS, TST", "AND masks bits. ANDS stores the result and sets N/Z; TST sets flags but discards the result.", "ANDS R0, R0, #0xFF; TST R1, #1", "TST is preferable when only the branch decision matters."),
        ("ORR, ORRS", "Set or combine bits.", "ORR R0, R0, R1", "Use BIC to clear known bits rather than ORR with an inverted mask."),
        ("EOR, EORS", "Exclusive OR, used for parity, toggling, matrix arithmetic and LCG variants.", "EORS R9, R9, R12", "XORing a bit twice cancels it. The S form overwrites N/Z."),
        ("BIC, BICS", "Clear selected bits: Rd = Rn AND NOT operand2.", "BIC R0, R0, #(3 << 4)", "Useful for read-modify-write register configuration before ORR sets the desired field."),
        ("MVN, MVNS", "Bitwise NOT of the operand.", "MVN R0, R0", "Often combined with ADDS #1 for two's complement when RSB is unsuitable."),
        ("LSL, LSLS", "Logical left shift; fills low bits with zero and can provide an index scale or bit mask.", "LDR R0, [R4, R6, LSL #2]", "Large shifts and flag behavior differ between immediate and register forms. LSL by 2 scales a word index."),
        ("LSR, LSRS", "Logical right shift; fills high bits with zero. Use for unsigned fields.", "LSR R0, R0, #8", "Do not use it to divide a negative signed value; ASR preserves the sign."),
        ("ASR, ASRS", "Arithmetic right shift; replicates the sign bit.", "ASR R0, R0, #1", "Rounding for negative values is toward negative infinity, not C signed division's truncation toward zero."),
        ("ROR, RRX", "Rotate right; RRX rotates through carry by one bit.", "ROR R0, R0, #8", "RRX consumes and replaces carry, so establish C deliberately."),
        ("UXTB, UXTH, SXTB, SXTH", "Explicitly zero- or sign-extend an 8- or 16-bit value already in a register.", "UXTB R5, R1", "Loads may already extend; use these after arithmetic or when documenting a narrow contract."),
        ("REV, REV16, REVSH", "Reverse byte order in a word, each halfword, or a signed halfword.", "REV R0, R0", "Use for endianness conversion, not bit reversal."),
        ("CLZ", "Count leading zero bits.", "CLZ R0, R1", "Useful for normalization and bit length. Define the desired behavior for input zero."),
    ]),
    ("Comparison and conditional control", [
        ("CMP, CMN", "Set flags for subtraction or addition without storing a result.", "CMP R6, R5; BHS done", "CMP feeds both signed and unsigned branch families; choose the family that matches the data type."),
        ("B", "Unconditional branch to a local label.", "B outer_loop", "It does not save a return address. Use BL for a subroutine call."),
        ("BEQ/BNE", "Branch when Z is set/not set, typically after CMP, TST or an S-form arithmetic instruction.", "CMP R0, #0; BEQ empty", "Any intervening flag-setting instruction destroys the comparison result."),
        ("BLO/BHS and BCC/BCS", "Unsigned lower/higher-or-same; aliases based on carry clear/set.", "CMP R6, R5; BHS done", "Use for sizes, addresses and uint values. Do not use BLT/BGE for unsigned lengths."),
        ("BLS/BHI", "Unsigned lower-or-same/higher.", "CMP R5, #1; BLS done", "These include equality differently from BLO/BHS."),
        ("BLT/BGE", "Signed less-than/greater-or-equal using N and V.", "CMP R8, #0; BLT insert", "Required for signed array elements and signed candidates."),
        ("BLE/BGT", "Signed less-or-equal/greater-than.", "CMP R0, R7; BLE insert", "Do not substitute unsigned BLS/BHI when negatives are possible."),
        ("BMI/BPL", "Branch on negative/non-negative according to N.", "CMP R0, #0; BMI negative", "After arithmetic overflow, N alone may not represent signed relational ordering; CMP plus BLT/BGE is safer."),
        ("CBZ/CBNZ", "Compare a low register with zero and branch without changing flags.", "CBZ R0, empty", "Branch range and eligible registers are encoding-dependent. Useful when current flags must survive."),
        ("IT/ITE and conditional suffixes", "Condition one to four following Thumb instructions. ITE selects then/else forms.", "CMP R0, #0; ITE EQ; MOVEQ R1,#1; MOVNE R1,#0", "Instructions in the block need matching condition suffixes. Prefer ordinary branches for long or changing logic."),
    ]),
    ("Calls, returns, exceptions and concurrency", [
        ("BL", "Call a subroutine by writing the return address to LR.", "BL aliquotSum", "A routine that executes BL is non-leaf and must preserve its incoming LR before the first nested call."),
        ("BX, BLX", "Branch to a register; BX LR is the normal leaf return. BLX also writes LR and may change instruction state.", "BX LR", "Cortex-M code must remain in Thumb state; function addresses have bit 0 set."),
        ("SVC", "Enter the supervisor-call exception with an 8-bit immediate service number.", "SVC #50", "The handler normally decodes the immediate from the halfword at stacked PC minus 2. Select MSP or PSP from EXC_RETURN."),
        ("BKPT", "Enter the debugger with an immediate breakpoint number.", "BKPT #0", "Without a debugger, behavior can escalate to a fault. Do not leave test breakpoints in the submitted flow."),
        ("CPSID/CPSIE", "Disable or enable configurable interrupts, usually with operand i.", "CPSID i; ...; CPSIE i", "Do not blindly re-enable interrupts if they were already disabled; saving/restoring PRIMASK is safer."),
        ("DMB, DSB, ISB", "Memory, completion and instruction-stream barriers.", "DMB; MSR CONTROL,R0; ISB", "Use for synchronization and system-control changes, not as a substitute for volatile or correct ownership."),
        ("LDREX/STREX, CLREX", "Exclusive load/store pair for lock-free updates. STREX reports whether the reservation succeeded.", "retry: LDREX R1,[R0]; ADD R1,#1; STREX R2,R1,[R0]; CBNZ R2,retry", "Interrupts or other writes may clear the reservation. Always loop on STREX failure."),
        ("WFI, WFE, SEV, NOP", "Wait for interrupt/event, send event, or execute no operation.", "WFI", "WFI is safe only when an enabled event can wake the processor. It does not configure the peripheral or clear pending flags."),
    ]),
]

DIRECTIVES = [
    ("AREA", "Declare a code or data section and its attributes."), ("THUMB", "Assemble Thumb instructions."),
    ("PRESERVE8", "State that code preserves 8-byte stack alignment."), ("EXPORT / IMPORT", "Publish or reference linker symbols."),
    ("PROC / ENDP", "Mark procedure boundaries for the assembler/debugger."), ("DCD / DCB", "Define word or byte constants."),
    ("SPACE", "Reserve uninitialized bytes; multiply word counts by four."), ("EQU / RN", "Define a constant or register alias."),
    ("ALIGN", "Align the following location."), ("LTORG", "Emit the current literal pool."), ("END", "End the assembly source."),
]


def natural_key(path: Path):
    name = path.name
    match = re.match(r"(\d+)(?:_|\b)", name)
    if match:
        return (0, int(match.group(1)), name.lower())
    support_order = {"guide_to_keil_templates.pdf": 0, "lpc176x_usermanual.pdf": 1, "landtiger schematic.pdf": 2}
    return (1, support_order.get(name.lower(), 99), name.lower())


def footer(canvas, doc):
    canvas.saveState(); canvas.setFont("Helvetica", 8); canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(18*mm, 10*mm, "ARM Assembly Instruction Handbook")
    canvas.drawRightString(192*mm, 10*mm, f"Page {doc.page}"); canvas.restoreState()


def build_guide():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Title2", parent=styles["Title"], fontSize=24, leading=29, textColor=colors.HexColor("#17365D"), alignment=TA_CENTER, spaceAfter=16))
    styles.add(ParagraphStyle(name="Group", parent=styles["Heading1"], fontSize=17, leading=21, textColor=colors.HexColor("#17365D"), spaceBefore=8, spaceAfter=10))
    styles.add(ParagraphStyle(name="Inst", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=colors.HexColor("#8A2D1C"), spaceBefore=9, spaceAfter=4))
    styles.add(ParagraphStyle(name="Body2", parent=styles["BodyText"], fontSize=9.2, leading=12.5, spaceAfter=5))
    styles.add(ParagraphStyle(name="Code2", parent=styles["Code"], fontName="Courier", fontSize=8.3, leading=10.5, leftIndent=8, backColor=colors.HexColor("#F2F4F7"), borderPadding=5, spaceAfter=5))
    story = [Paragraph("ARM Assembly Instruction Handbook", styles["Title2"]), Paragraph("Exam-focused Cortex-M3 / Thumb-2 reference derived from the ARM lecture set, all 23 indexed ARM papers, professor assembly templates and historical answer sources.", styles["Body2"]), Spacer(1, 8*mm)]
    story += [Paragraph("How to use this during an exam", styles["Group"]), Paragraph("Start from the operation you need, then check four things before copying a pattern: element width, signedness, flags, and AAPCS preservation. The examples use Keil assembly syntax. Instruction availability and immediate encoding depend on Thumb-2; when an immediate is rejected, load it into a register or use a literal.", styles["Body2"])]
    story += [Paragraph("AAPCS checkpoint", styles["Group"]), Paragraph("R0-R3 carry the first four arguments and the return begins in R0. Additional arguments are at the caller's stack. R4-R11 and SP are callee-saved. LR must be saved by any non-leaf routine. Keep SP 8-byte aligned whenever control crosses a public function boundary.", styles["Body2"])]
    conditions = [["Suffix", "Meaning", "Use"], ["EQ / NE", "equal / not equal", "zero, sentinel, equality"], ["LO / HS", "unsigned < / >=", "sizes, indexes, addresses"], ["LS / HI", "unsigned <= / >", "inclusive unsigned bounds"], ["LT / GE", "signed < / >=", "signed bytes/words"], ["LE / GT", "signed <= / >", "signed inclusive bounds"], ["MI / PL", "negative / non-negative", "sign test"], ["CS / CC", "carry set / clear", "carry or no-borrow / borrow"], ["VS / VC", "overflow set / clear", "signed overflow contract"]]
    table = Table(conditions, colWidths=[24*mm, 52*mm, 92*mm], repeatRows=1); table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#17365D")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),8.5),("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#AAB2BD")),("VALIGN",(0,0),(-1,-1),"TOP"),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F6F8FA")])]))
    story += [Paragraph("Condition-code selection", styles["Group"]), table, PageBreak()]
    md = ["# ARM Assembly Instruction Handbook", "", "This is the maintained source for the searchable PDF handbook.", "", "## AAPCS checkpoint", "", "R0-R3 carry the first four arguments; R4-R11 and SP are callee-saved; save LR before nested BL; keep SP eight-byte aligned at public call boundaries.", ""]
    for group, entries in GROUPS:
        story.append(Paragraph(group, styles["Group"])); md += [f"## {group}", ""]
        for name, purpose, example, constraint in entries:
            story += [Paragraph(name, styles["Inst"]), Paragraph("<b>Use:</b> " + purpose, styles["Body2"]), Paragraph(example.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"), styles["Code2"]), Paragraph("<b>Constraints:</b> " + constraint, styles["Body2"])]
            md += [f"### {name}", "", f"Use: {purpose}", "", "```asm", example, "```", "", f"Constraints: {constraint}", ""]
        story.append(PageBreak())
    story.append(Paragraph("Assembler directives that appear in the material", styles["Group"])); md += ["## Assembler directives", ""]
    for name, description in DIRECTIVES:
        story += [Paragraph(name, styles["Inst"]), Paragraph(description, styles["Body2"])]
        md += [f"- `{name}` - {description}"]
    story += [Paragraph("High-frequency combinations", styles["Group"]), Paragraph("<b>Bounded byte loop:</b> LDRB/STRB with post-indexing, SUBS counter, BNE. <b>Signed sort:</b> LDRSB, CMP, BLE/BLT. <b>Word array:</b> LDR/STR with index LSL #2. <b>Non-leaf:</b> aligned PUSH, BL, matching POP to PC. <b>Remainder:</b> UDIV then MLS. <b>Peripheral field:</b> LDR register, BIC field mask, ORR desired value, STR back. <b>Event handoff:</b> minimal handler, clear W1C flag, update volatile state, foreground processing.", styles["Body2"])]
    doc = SimpleDocTemplate(str(GUIDE_PDF), pagesize=A4, rightMargin=18*mm,leftMargin=18*mm,topMargin=16*mm,bottomMargin=17*mm, title="ARM Assembly Instruction Handbook", author="")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    GUIDE_MD.write_text("\n".join(md)+"\n", encoding="utf-8")


def build_library():
    pdfs = sorted(ARM.rglob("*.pdf"), key=lambda p: natural_key(p))
    entries=[]; source_pages=0
    for p in pdfs:
        n=len(PdfReader(str(p)).pages); entries.append((p,n)); source_pages+=n
    toc_pdf=TMP/"arm-library-index.pdf"
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name="Small",parent=styles["BodyText"],fontSize=8.5,leading=11))
    story=[Paragraph("Complete Ordered ARM PDF Library",styles["Title"]),Paragraph("Every page of every PDF under the ARM directory is preserved unchanged after this searchable index. Use the PDF bookmarks to jump directly to a lecture, reference manual, schematic or Keil guide.",styles["BodyText"]),Spacer(1,5*mm)]
    rows=[["Order","Source document","Source pages"]]
    for i,(p,n) in enumerate(entries,1): rows.append([str(i),p.relative_to(ARM).as_posix(),str(n)])
    table=Table(rows,colWidths=[14*mm,137*mm,25*mm],repeatRows=1); table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#17365D")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8),("GRID",(0,0),(-1,-1),0.35,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F5F7FA")])]))
    story += [table,Spacer(1,4*mm),Paragraph(f"Source documents: {len(entries)}. Original source pages preserved: {source_pages}.",styles["Small"])]
    SimpleDocTemplate(str(toc_pdf),pagesize=A4,rightMargin=15*mm,leftMargin=15*mm,topMargin=15*mm,bottomMargin=15*mm,title="Complete Ordered ARM PDF Library Index",author="").build(story)
    writer=PdfWriter(); toc_reader=PdfReader(str(toc_pdf)); writer.append(toc_reader); offset=len(toc_reader.pages)
    writer.add_outline_item("Library index",0)
    page=offset
    for p,n in entries:
        writer.append(str(p)); writer.add_outline_item(p.relative_to(ARM).as_posix(),page); page+=n
    writer.add_metadata({"/Title":"Complete Ordered ARM PDF Library","/Author":"","/Subject":"Ordered searchable ARM course library with all original pages preserved"})
    with LIBRARY_PDF.open("wb") as target: writer.write(target)
    toc_pdf.unlink(missing_ok=True)
    print(f"guide={GUIDE_PDF}"); print(f"library={LIBRARY_PDF}"); print(f"documents={len(entries)} source_pages={source_pages} total_pages={len(writer.pages)}")


if __name__ == "__main__":
    build_guide(); build_library()
