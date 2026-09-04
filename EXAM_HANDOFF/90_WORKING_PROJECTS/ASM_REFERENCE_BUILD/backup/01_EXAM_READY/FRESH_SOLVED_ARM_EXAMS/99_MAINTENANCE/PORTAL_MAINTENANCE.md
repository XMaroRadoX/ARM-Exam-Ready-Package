# Maintaining the offline portal

## Courses, search, and exam guidance

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
