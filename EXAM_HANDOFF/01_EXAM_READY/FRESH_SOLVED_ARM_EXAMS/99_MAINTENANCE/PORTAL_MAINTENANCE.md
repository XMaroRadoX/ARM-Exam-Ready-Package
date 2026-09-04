# Maintaining the offline portal

The Algorithms/Solution Patterns split and the complete peripheral scenario
library are maintained through [SCENARIO_MAINTENANCE.md](SCENARIO_MAINTENANCE.md).
Preserve its explicit destination mapping when changing navigation or search.

## ASM exam reference

`asm_reference.py` owns the instructions, syntax, examples, and checklist. The
builder installs it after the workstation extension and generates both the
`PORTAL/asm/index.html` page and `ASM_INSTRUCTION_GLOSSARY.md` from that source.
Edit `portal_ui/asm_reference.css` and `portal_ui/asm_reference.js` for its
appearance and optional local filtering. Keep all entries visible without
JavaScript and include filtered-out entries when printing.

After rebuilding in an isolated copy, run `python -B VERIFY_ASM_REFERENCE.py`
and `node BROWSER_ASM_REFERENCE.cjs` along with the standard portal checks.
The coverage report records source spellings, their locations, and unresolved
tokens from assembly, authored lessons, and the twelve core ARM lecture PDFs.
PDF text extraction does not inspect text embedded in images. Execution checks
assemble displayed instruction examples for Cortex-M3 using LLVM directive
translation and exercise key results and ABI invariants with Unicorn. Native
ARMASM pseudo-instructions/directives and physical hardware have separate
validation limits recorded in `ASM_REFERENCE_VALIDATION.json`.

## Courses, search, and exam guidance

### Search-only updates

Use `python -B REFRESH_SEARCH.py` in an isolated current copy when changing
search. It updates the corpus, search page, section bindings, and exam-topic
panels without regenerating lessons, projects, or answer code. Do not use a
full portal rebuild to deliver an indexing-only change.

`search_metadata.py` joins the reviewed exam index, question index, and existing
answer manifest by their explicit IDs. Keep algorithms, peripherals,
interrupts, timing, and ABI/memory tags in their respective question-index
columns. Recognition phrases and exact function names remain separate.
Exam-level tags are the union of the question tags; original PDFs receive
whole-paper metadata, never a guessed question-to-page mapping.

Global, catalog, and API-sidebar searches share `portal_logic.js`. Catalog
cards are matched against their associated full content, with a direct link
to the match and a link carrying the query to global search. Duplicate content
shares storage while each source retains its own class, tags, and route.
Filename-only attachments and supporting warnings have lower ranking than
the question or solution. Exact API names keep first-match priority.

The coverage report inventories included and excluded files, nonextractable
PDF pages, attachments with searchable names only, and exam sources lacking
a maintained answer mapping. A mapping status does not assert whether an
unmapped original contains its own solution. The track filter separates ARM
programming from architecture/theory and general references.

After refresh, run `VERIFY_SEARCH_COVERAGE.py`, `VERIFY_SEARCH.cjs`, and
`BROWSER_SEARCH_QA.cjs` alongside the existing portal checks. Run the refresh
twice after source edits finish and compare corpus/coverage hashes to verify
determinism. Browser QA uses local file URLs and saves desktop/narrow captures;
set its browser/runtime paths to the locally installed tools.

When other tasks use separate worktrees, integrate only this task's reviewed
files into the intended checkout. Compare both changed files and search inputs
with the starting snapshot immediately before integration. If either changed,
reconcile in staging and rebuild; never restore an older whole tree over a
newer checkout. Keep a manifest and backup for the exact replaced files.


`workstation_extensions.py` extends the canonical builder after the presentation
hook. Edit `course_c.py`, `course_arm.py`, `course_board.py`, and
`course_projects.py` for lesson content. `course_relationships.py` holds explicit
lesson-to-pattern links. All 46 lessons have an attempt, progressive hints,
worked answer, checkpoint, and navigation. `COURSE_COVERAGE.json` records links
to the supplied ARM lecture sequence and all 48 reviewed questions.

`pattern_teaching.py` contains the 78 pattern-specific methods and seven
workflow additions. Broader exam sources are linked as references rather than
presented as minimal reusable functions. Keep original IDs and links stable.

`exam_walkthrough.py` owns the nine-step offline playbook. `workstation_state.js`
validates the versioned progress format; `workstation.js` provides optional
storage, import/export, and the step interface. Without JavaScript the full
checklist and native answer disclosures remain readable. No course duration,
permission, or collection drive is inferred from historical rules.

`search_corpus.py` reads generated sections, code, original PDFs, source notes,
and current-template declarations. It excludes personal working projects and
build artifacts. Python with `pypdf` is required to rebuild the corpus, but
neither Python nor a server is required to use the completed package.
`SEARCH_DOCUMENT_CACHE.json` caches extraction by content hash; source changes
invalidate their cached text. `SEARCH_COVERAGE.json` records nonextractable
pages and duplicate grouping. Do not silently remove those limitations.

Preserve exact-name priority, existing filters, all-word matching, and URL
history when changing `portal_logic.js` or `portal.js`. Synonyms are curated;
typo suggestions require an explicit selection. User text is rendered as text,
not inserted as HTML. PDF page fragments must retain `#page=NUMBER` syntax.

After the standard checks below, run `VERIFY_WORKSTATION.py` and
`VERIFY_WORKSTATION_CONTROLS.cjs`. `VERIFY_COURSE_EXECUTION.py` compiles new C
objects for Cortex-M3 and runs the actual sum instruction stream with ABI
checks; it requires LLVM and the same local test dependencies as the existing
algorithm suite. This is not a full Keil build or physical-board test.
`BROWSER_WORKSTATION_QA.cjs` runs against file URLs in a disposable local browser
context; point its external runtime/browser paths at the installed tools.
Run browser checks only after generation finishes, never while the builder is
replacing its output. Inspect saved desktop/narrow screenshots in addition to
automated assertions. Reports distinguish structural, control, compilation,
instruction-execution, browser, and hardware evidence.

`RELEASE_WORKSTATION.py` snapshots an original handoff and integrates only its
explicit allowed paths from a separate staging copy. It rejects overwriting
files changed since the snapshot and creates a recoverable backup. It never
deletes the original template, exam solutions, source papers, or personal work.

The canonical builder owns the teaching content, source copies, catalog, and routes.
The presentation hook in `portal_presentation.py` owns page layout, navigation,
code controls, the study home, and the search interface. Its browser assets live
in `portal_ui/`; edit those files rather than generated files in `PORTAL/assets`.

The presentation layer preserves every code listing and source-file contract.
It expands code panels, adds copy controls, creates section anchors without
replacing existing identifiers, and provides optional browser enhancements.
All dependencies are local. No server is needed to use the delivered package.

## Rebuild safely

For LED API changes, run `python -B VERIFY_LED_API.py` as well. It executes
the actual LED helper bodies as Cortex-M3 code with a mock low-level driver,
checks all board labels and invalid byte values, and verifies display masks
and interrupt-state restoration. Its report is `LED_API_VALIDATION.json`;
it does not establish physical-board behavior.

1. Agree on a single writer before changing a shared generator or rebuilding.
2. Copy the current handoff into an isolated working directory, including
   untracked files. Keep its complete relative folder layout.
3. From the copy's maintenance directory, run `python -B BUILD_STUDENT_PORTAL.py`.
4. Run `python -B VERIFY_STUDENT_PORTAL.py`,
   `python -B VERIFY_PORTAL_PRESENTATION.py`, and
   `node VERIFY_PORTAL_CONTROLS.cjs`.
5. Inspect representative pages in a browser. Compare canonical/generated code
   and current source hashes before copying reviewed outputs back.

The canonical builder replaces its generated portal and code-copy directories.
Do not run it in a shared workspace while another task is editing or rebuilding.
Keep a backup of files replaced during integration. Never restore an old whole
tree over newer work from another task.

## Browser behavior

- The system theme is the default. An explicit light/dark choice is remembered
  when storage is available; storage denial does not prevent browsing.
- Complete code is visible without JavaScript. Copying falls back to selecting
  the code with a manual keyboard-copy instruction if clipboard access fails.
- Search uses the local catalog. C and Assembly filters include entries marked
  Both; Timer includes numbered timers and multi-timer lessons.
- Submitting a search or changing a filter records URL state. Back/forward
  restores it. A browser that restricts History still supports local filtering.
- JavaScript-disabled search provides ordinary links to the catalog sections.
- Print rules remove navigation chrome and wrap long code and tables.

## Validation boundaries

The structural checks do not prove firmware correctness or physical-board
behavior. The controls test exercises search semantics and unavailable browser
facilities in an isolated runtime. Browser checks remain necessary for appearance,
focus, navigation, and rendering. The audit report records the tests actually run.

## Complete Solution Patterns

See [PATTERN_MAINTENANCE.md](PATTERN_MAINTENANCE.md) for the explicit project mappings, native build gate, behavioural verification and source-agreement checks.
