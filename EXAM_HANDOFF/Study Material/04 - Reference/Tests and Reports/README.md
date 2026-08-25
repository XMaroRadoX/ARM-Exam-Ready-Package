# Tests and reports

This directory contains current verification evidence. Use the linked summaries
below as authoritative; older diagnostic logs may remain for provenance but are
not current pass/fail evidence.

| Evidence | Meaning |
|---|---|
| [Repository readiness audit](Repository%20Audit/EXAM_READINESS_AUDIT.md) | Current file-by-file verdict, entry points, known defects and exam/template coverage |
| [Exam-by-exam matrix](Repository%20Audit/EXAM_BY_EXAM_AUDIT.csv) | All 23 historical answer collections classified individually |
| [Direct-main and 78-pattern report](DIRECT_MAIN_AND_78_PATTERN_REPORT.md) | Current template, 23-answer, 78-pattern, recipe, host, link and PDF verification |
| [Solved-answer builds](Solved%20Answer%20Builds/SUMMARY.csv) | Current 23/23 solved-answer compile/link results and per-answer logs |
| [Algorithm host tests](Algorithm%20Host%20Tests/SUMMARY.csv) | Strict-warning core and edge vectors for all 50 new C references |
| [High-priority ARM simulator](High%20Priority%20ARM%20Simulator/README.md) | Runtime, ABI, SP and canary evidence for the 12 handwritten routines |
| [Practice-lab host fixtures](Practice%20Lab%20Host%20Tests/SUMMARY.csv) | Bulls and Cows, board-contract and peripheral-simulation results |
| [C reference builds](Recipe%20Builds/SUMMARY-C-REFERENCES.csv) | 50 Keil C compile/link results |
| [ARMASM implementation builds](Recipe%20Builds/SUMMARY-ARM-IMPLEMENTATIONS.csv) | 50 Keil ARM compile/link results |
| [Professor-template coverage audit](PROFESSOR_TEMPLATE_COVERAGE_AUDIT.md) | Current requirement-by-requirement audit of all 15 professor templates, the official guide, exam rules and 48 indexed questions |
| [Professor-template machine matrix](PROFESSOR_TEMPLATE_COVERAGE.csv) | Hash, retained-ZIP, recorded-build and maintained-equivalent evidence for all 15 templates |
| [C-course tests](C%20Course%20Tests/SUMMARY.csv) | Strict C11 warning-clean host build and deterministic vectors for the C-course reference fixture |
| [Assembly route and cleanup audit](ASSEMBLY_ROUTE_AND_CLEANUP_AUDIT.md) | Current assembly course/index coverage and remaining optional cleanup |
| [Clean template build](ARM_EXAM_CLEAN_TEMPLATE_BUILD.log) | Fresh copied-template build with zero errors and warnings |
| [Template and exam audit](FINAL_PROJECT_TEMPLATE_AND_EXAM_AUDIT.md) | Current project boundary and 23-answer status |
| [PDF visual QA](PDF%20Visual%20QA/) | Contact sheets covering every page of the three maintained generated PDFs |
| [Markdown link results](MARKDOWN_LINK_TEST.csv) | Broken-link output; an empty data section means zero failures |
| [Archive verification](ARCHIVE_VERIFICATION.csv) | SHA-256 and file-count evidence for the legacy ZIP archives |

Build success proves compilation and linking. It is not a substitute for
physical-board testing or automatic execution of every assembly answer.
