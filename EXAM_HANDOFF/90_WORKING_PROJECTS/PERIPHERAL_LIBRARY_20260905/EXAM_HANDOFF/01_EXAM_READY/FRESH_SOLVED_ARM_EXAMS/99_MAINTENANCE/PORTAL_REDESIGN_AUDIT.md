# ARM portal redesign and audit

## Delivery

Open [START_HERE.html](../../../START_HERE.html) directly. The portal is ordinary
local HTML with local styles, scripts, search data, and relative links. It has no
server, installation, account, or internet requirement. Keep the handoff folder
together when moving it.

The shared presentation covers the study home, search, exam collections, complete
exam and question answers, solution patterns, algorithms, API references, and
guides. Complete code remains on its existing page and is expanded by default.
Raw-source downloads and existing page URLs are retained.

The final catalog contains **400 maintained HTML pages and 393 searchable
entries**, including **169 algorithm pages**. Structural checks cover **15,594
local references** and **1,120 inline listings**, each with a copy control.

## Website findings and repairs

| Priority | Finding | Result |
|---|---|---|
| High | Editing generated HTML or assets would lose changes on regeneration. | A shared presentation module and local asset sources are connected to the canonical builder. |
| High | Concurrent regeneration replaces shared HTML and generated code directories. | Redesign work was isolated. The content task explicitly handed over after its final rebuild; integration checks current source hashes, uses an explicit output list, and backs up every replaced file. |
| Medium | Choosing C or Assembly could exclude entries labeled Both. | Both the global search and collection filters recognize combined-language entries. |
| Medium | The general Timer filter could miss numbered timers. | Timer includes Timer0–Timer3, Timer IRQ, and multi-timer lessons. Other categories use category-aware matching rather than arbitrary substrings. |
| Medium | Filter state was not restored through browser history. | Query/filter state is recorded in relative page URLs, restored on navigation, and cleared through explicit reset controls. |
| Medium | Large result trees were announced as live regions. | A separate status announces the count; result content is ordinary readable HTML. |
| Medium | The home page opened the canonical template without first explaining the working copy. | The project action leads to the existing copying and ownership instructions. |
| Medium | Some complete source panels started collapsed. | Every source panel is expanded initially, with native keyboard-accessible disclosure controls. |
| Medium | Long reading pages lacked consistent section/code shortcuts. | Pages receive stable section anchors, page contents, breadcrumbs, and a jump-to-code link. Existing anchors remain intact. |
| Medium | API navigation began at heading level three after the page title. | A level-two navigation heading now introduces the grouped functions; every page is checked for skipped heading levels. |
| Medium | Copying depends on browser clipboard permissions. | Failure selects the exact source text and supplies a manual keyboard-copy instruction. |
| Low | The theme did not follow the reader's preference. | System theme is the default; an explicit light/dark choice is stored when possible, with storage failure handled. |
| Low | Offline search had no useful JavaScript-disabled route. | Search provides ordinary catalog links when JavaScript is unavailable; all lessons and their code remain present in HTML. |

Affected-page scope and reproducible evidence:

| Scope | Affected pages | Evidence |
|---|---|---|
| Shared presentation, navigation, headings, code controls, themes | `START_HERE.html` and every `PORTAL/**/*.html` page | `VERIFY_PORTAL_PRESENTATION.py`, complete page/link counts in the linked results file |
| Search language/category matching, count announcements, history | [Search](../01_GUIDES_AND_INDEXES/PORTAL/search.html) | `VERIFY_PORTAL_CONTROLS.cjs` and the browser interactions listed below |
| Collection filtering and reset | [Past Exams](../01_GUIDES_AND_INDEXES/PORTAL/exams/index.html), [Patterns](../01_GUIDES_AND_INDEXES/PORTAL/patterns/index.html), [Algorithms](../01_GUIDES_AND_INDEXES/PORTAL/algorithms/index.html), [Guides](../01_GUIDES_AND_INDEXES/PORTAL/guides/index.html) | Shared filtering logic tests, exam-year and algorithm-query browser checks |
| Project preparation route | [Home](../../../START_HERE.html) | Automated rejection of a direct project-file link from home |
| Heading order and starter notice | [API overview](../01_GUIDES_AND_INDEXES/PORTAL/api/index.html) and API function pages | Complete heading-order scan; exact remaining source issue described below |

## Teaching-content review

The earlier package audit was rechecked against current source before adding
notices. Several of its findings had already been repaired: physical LED mapping,
ADC result ownership, button debouncing, DFS register preservation, reset-array
storage, complete-answer interrupt ownership, one-hot status handling, and
signed-byte question metadata. Those source changes were preserved. This redesign
does not claim a new execution or physical-board test of those repairs.

One remaining source inconsistency is identified on the
[API overview](../01_GUIDES_AND_INDEXES/PORTAL/api/index.html): its inline starter
uses `__WFI()` while including only `exam_api.h`. The canonical quick reference
already includes `LPC17xx.h`. A notice on the overview tells the reader to include
that device header. The underlying example is retained for its content owner to
correct; the presentation layer does not silently rewrite teaching code.

Algorithm content, exported interfaces, contracts, tests, and repairs belong to
the separately maintained algorithm library. The final rebuild retains all 169
entries from 129 independent source sets, including 40 shared variations. Its
catalog modules, renderer, inventory generation, coverage assertions, and
`--algorithms-only` mode are preserved. The canonical builder changes only by
adding two lines that install the presentation before its existing entry point.

## Validation evidence

The current machine-readable structural results are in
[PORTAL_PRESENTATION_RESULTS.json](PORTAL_PRESENTATION_RESULTS.json).

- The canonical portal verifier passes, including its content coverage, API
  coverage, navigation, and representative search checks.
- The independent presentation audit checks every maintained page, link, form
  action, local asset, anchor, source panel, and raw-source/code correspondence.
- Canonical and redesigned builds are compared for exact inline code and generated
  source equality: all 400 pages' inline code and all 557 generated raw files match.
- The control regression suite passes 26 assertions, including combined languages,
  exact API ranking, multiword queries, category matching, absent/denied clipboard
  access, exact copying, valid stored themes, and blocked browser storage.
- Fourteen foreground/background token pairs meet at least 4.5:1 contrast across
  light and dark themes. This is a token check, not a blanket accessibility certification.
- Assets remain local and shared between pages. The complete search catalog loads
  only on the search page; results render in batches of 50. Page and asset sizes
  are recorded in the structural evidence without requiring a network benchmark.

Before the temporary preview was stopped, browser checks confirmed:

- Light/dark switching and persistence between pages.
- Exact `exam_timer_config_ms` lookup and a meaningful no-results state.
- C, Assembly, and Both result sets, including restoration through Back.
- Exam-year filtering, reset behavior, and query/filter URLs.
- Copy output equal to the displayed source, with success feedback.
- Native disclosure behavior with both a click and the Enter key.
- Jump-to-code navigation and complete inline source visibility.
- Desktop collection layouts, API and question layouts, and narrow-screen home,
  algorithm, and API layouts. Narrow pages did not overflow horizontally; long
  source listings scroll within their own panels.

## Limits and remaining checks

- Direct `file:` browser navigation was rejected by the browser tool's URL policy.
  No alternate browser or workaround was used to bypass that restriction. Actual
  double-click behavior is therefore not claimed as an observed browser result.
  The portable relative-path and local-asset checks passed in the relocated copy.
- No server is part of the delivery. The temporary visual-testing server and its
  preview tab were stopped and closed at the user's request.
- Browser zoom shortcuts were not supported by the available controls; a literal
  200% zoom interaction was not verified. Responsive layouts were checked at
  desktop and narrow viewport widths.
- A complete keyboard-only traversal and the full page-type, viewport, and theme
  matrix were not completed. Only the specific browser checks listed above are
  claimed; automated checks do not replace that remaining visual review.
- Print and JavaScript-disabled behavior were inspected structurally. An actual
  print preview and browser-level JavaScript-disable session were not exercised.
- The expanded algorithm catalog is integrated after the earlier visual checks.
  Those additions receive structural and source-fidelity checks; a new browser
  pass is not claimed after the user requested stopping the preview server.
- No fresh firmware correctness, hardware timing, electrical, or physical-board
  claim is made by this website audit.

## Maintenance

The integration baseline inventories 6,567 existing files, including untracked
files and the other task's test artifacts. The update is restricted to generated
HTML/assets, the presentation sources and checks, this report, the entry README,
and the two-line builder hook. Generated raw code, original materials, starting
templates, personal practice files, algorithm sources, and content tests are not
copied back from staging. Every replaced file has an external backup; rollback
must check current hashes before replacing anything that could have newer work.

See [PORTAL_MAINTENANCE.md](PORTAL_MAINTENANCE.md) for the authoritative presentation
sources, checks, and the isolated rebuild procedure. Do not run the destructive
canonical builder against a shared directory while another task is editing it.
