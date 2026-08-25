# Direct-main and 78-pattern verification report

Date: 2026-08-25

## Result

The maintained `EXAM_HANDOFF` package uses `Answer/main.c` and
`Answer/assembly.s` directly. The removed wrapper API and hidden lifecycle files
are absent from the canonical project and active learning material. The active
atlas contains exactly 23 exams, 48 questions, and 78 patterns.

The 50 expanded algorithm references are no longer minified: they total 3,567
formatted C lines, every file has an explicit contract/method comment, and the
smallest reference is 48 lines. Their 50 recipe pages and 50 atlas pages average
93 lines and include contracts, named variants, pseudocode, AAPCS/register
plans, frame calculations, complexity, structured edge cases, executable
vectors, adaptation points, verification boundaries, and historical links.

The active learning route now starts with a tested exam-focused C course and a
concise direct-template workflow. The question-level past-paper index provides
243 exact tags across language, type, algorithm, peripheral, event, timing,
data shape, ABI and risk, rather than relying on broad date-level labels.

The assembly route now has a README index, a 14-lesson course, a concise
exam-day guide and a generated index covering all 78 patterns as 12 HIGH, 28
CORE and 38 SUPPLEMENTARY entries.

## Keil / Arm Compiler 6.22

| Scope | Result | Evidence |
|---|---|---|
| Fresh direct-`main.c` template | 0 errors, 0 warnings | `ARM_EXAM_CLEAN_TEMPLATE_BUILD.log` |
| 23 solved answers | 23/23 at 0 errors, 0 warnings | `Solved Answer Builds/SUMMARY.csv` |
| 50 formatted C references | 50/50 at 0 errors, 0 warnings | `Recipe Builds/SUMMARY-C-REFERENCES.csv` |
| 50 matching ARMASM implementations | 50/50 at 0 errors, 0 warnings | `Recipe Builds/SUMMARY-ARM-IMPLEMENTATIONS.csv` |
| 28 other active recipes | 28/28 at 0 errors, 0 warnings | `Recipe Builds/SUMMARY-ACTIVE-RECIPES.csv` |

The 12 exam-derived routines are deliberately handwritten ARMASM. The 38
supplementary routines remain compiler-derived matching implementations and are
described honestly as such in their pages.

## Executed tests

| Check | Result | Evidence |
|---|---|---|
| C core and edge vectors | 50/50 `HOST_EDGE_TESTED_C` | `Algorithm Host Tests/SUMMARY.csv` |
| High-priority ARM runtime harness | 35 checks, 0 functional failures, 0 ABI/SP failures | `High Priority ARM Simulator/SUMMARY.csv` |
| Bulls and Cows / board-contract / peripheral host fixtures | 3/3 pass | `Practice Lab Host Tests/SUMMARY.csv` |
| C-course fixture | strict C11 compile and deterministic run pass | `C Course Tests/SUMMARY.csv` |
| Professor-template coverage | 15/15 retained ZIP hashes, 15/15 recorded builds, 48/48 indexed questions covered | `PROFESSOR_TEMPLATE_COVERAGE_AUDIT.md` |
| Direct-main template contract | pass | `test-template-contract.py` |
| Atlas/library structure | 23 exams, 48 questions, 78 patterns, 293 exact question mappings, 243 detailed tags, pass | `validate-library.py` |
| Markdown links and anchors | 395 documents, 1,879 local links, 0 failures | `MARKDOWN_LINK_TEST.csv` |
| Obsolete active public terminology | 0 matches | active-source scan |
| Attribution scan | 0 matches | active-package scan |

The ARM harness executes the linked Cortex-M3 AXF and checks expected results,
`R4`-`R10` preservation, SP restoration, and guard words around writable
buffers. This supports `SIMULATOR_EXECUTED_PASS` for the 12 handwritten
high-priority routines. The other 38 ARM routines remain `COMPILE_ONLY`.

## Historical mappings

All 12 high-priority IDs now point to their exact indexed questions. This
includes two LCG papers, three indirect-recurrence questions, and both 2026
Bulls and Cows/Mastermind variants. Supplementary entries intentionally have no
historical occurrence unless one is later established.

The searchable source of truth is `03 - Solved Exams/PAST_EXAM_SEARCH_INDEX.md`,
with matching `question_search.csv` and `question_search.json` files for exact
filtering. Exam cards and pattern coverage are regenerated from the same
question-level metadata.

## Generated PDFs

Only the three maintained generated PDFs were rebuilt:

- `ARM_ASSEMBLY_INSTRUCTION_HANDBOOK.pdf` — 5 searchable pages, including the
  assembly-course route, exam sequence, AAPCS/branch sheets, data directives,
  instruction families, decision tree, register worksheet and all 78 IDs.
- `ARM_PATTERN_ATLAS_MASTER.pdf` — 13 searchable pages, including the complete
  78-pattern table and 50 expanded study cards.
- `ARM_PATTERN_QUICK_REFERENCE.pdf` — 1 searchable exam-day page containing the
  12 high-priority and 28 established patterns.

All 19 pages were rendered and visually inspected. No clipping, malformed
tables, broken code blocks, missing page content, or stale terminology was
observed. Original exam, lecture, professor, schematic, and reference-manual
PDFs were not rebuilt.

## Verification boundary and worktree

- Physical LPC1768 board behavior is not tested or claimed. Timer cadence,
  interrupt delivery, GPIO wiring, jumpers, ADC/DAC analog behavior, and board
  timing still require hardware.
- The canonical project can open with simulator debugging selected. The final
  exam pass must select `Use Target`, download to the physical LandTiger board,
  and test the real inputs, timing and analogue paths.
- A compile/link pass for the 23 solved answers does not by itself prove their
  physical peripheral behavior.
- The worktree contains a large reorganization. Review the full rename/move
  picture before staging; do not interpret old-path deletions and new
  directories independently.
