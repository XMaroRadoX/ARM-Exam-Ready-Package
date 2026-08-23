# Tests and reports

This directory contains current verification evidence. Superseded build logs
have been removed so a stale result cannot be mistaken for the current build.

| Evidence | Meaning |
|---|---|
| [Repository readiness audit](Repository%20Audit/EXAM_READINESS_AUDIT.md) | Current file-by-file verdict, entry points, known defects and exam/template coverage |
| [Exam-by-exam matrix](Repository%20Audit/EXAM_BY_EXAM_AUDIT.csv) | All 23 historical answer collections classified individually |
| [Professor-template matrix](Repository%20Audit/PROFESSOR_TEMPLATE_COVERAGE.csv) | All 15 professor templates compared with the clean project |
| [Clean template build](ARM_EXAM_CLEAN_TEMPLATE_BUILD.log) | Recorded build assembled, compiled and linked with zero errors and warnings; it is not a fresh build from this audit environment |
| [Bulls and Cows build](BULLS_DEBUG_LAB_BUILD.log) | Practice project build evidence |
| [Template and exam audit](FINAL_PROJECT_TEMPLATE_AND_EXAM_AUDIT.md) | Project coverage and known solution limitations |
| [Markdown link results](MARKDOWN_LINK_TEST.csv) | Broken-link output; an empty data section means zero failures |
| [Archive verification](ARCHIVE_VERIFICATION.csv) | SHA-256 and file-count evidence for the legacy ZIP archives |

Build success proves compilation and linking. It is not a substitute for
physical-board testing or automatic execution of every assembly answer.
