# Original and legacy archives

These archives preserve material consolidated from the package directory above
`EXAM_HANDOFF`. They are reference copies and are never part of the submitted
Keil project.

| Archive | Preserved files | Uncompressed bytes | Contents |
|---|---:|---:|---|
| [Original kit backups](Original_Kit_Backups.zip) | 3,298 | 90,309,986 | Complete v1 and v2 kit backups plus their SHA-256 manifests |
| [Professor Keil templates](Professor_Keil_Templates.zip) | 18 | 51,254,180 | Original template ZIPs, emulator material and the template guide PDF |
| [Previous deliverables](Previous_Deliverables.zip) | 1,920 | 33,640,121 | Earlier kit, exam examples, reports and verification output |
| [Previous atlas](Previous_ARM_EXAM_ATLAS.zip) | 138 | 433,105 | Atlas state before relocation into the handoff |
| [Previous tool environment](Previous_Tool_Environment.zip) | 615 | 25,399,051 | Earlier scripts and their local Python package environment |

Every archived file was read back from its ZIP and compared with its source
using SHA-256 before the unpacked duplicate was removed. The machine-readable
archive hashes and verification status are recorded in
[ARCHIVE_VERIFICATION.csv](../Tests%20and%20Reports/ARCHIVE_VERIFICATION.csv).

The active replacements are:

- Atlas and code patterns: `../Exam Atlas and Code Patterns`
- Historical solutions: `../Solved Exams`
- Reports and test evidence: `../Tests and Reports`
- Maintained tools: `../Tools`
- Practice projects: `../Practice Projects`

An archive can be extracted when an untouched historical file is needed. The
active atlas and Keil submission project should not be replaced by legacy files.
