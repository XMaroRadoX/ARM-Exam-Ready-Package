# Tools

- `audit-repository.py` reads and hashes the clean project, solved-exam
  collection and extracted professor templates, then regenerates the
  machine-readable inventories under `Tests and Reports/Repository Audit`.
- `render-exam-contact-sheets.py` renders every page of all 23 indexed ARM
  papers into temporary contact sheets for visual review.

Only tools that operate on the current directory layout are kept here.

| Tool | Purpose |
|---|---|
| `test-markdown-links.ps1` | Checks every active local Markdown file and anchor |
| `validate-library.py` | Validates the 23 exams, 48 questions, 28 patterns and solution-file layout |
| `generate-pattern-coverage.ps1` | Rebuilds the pattern-coverage documentation from the active indexes |
| `repair-atlas-links.ps1` | Repairs known legacy atlas links after a controlled import |

The previous generators, regression script and Python package environment are
preserved in `Original and Legacy Archives/Previous_Tool_Environment.zip`.
They are not active because they target the superseded `deliverables` layout.
