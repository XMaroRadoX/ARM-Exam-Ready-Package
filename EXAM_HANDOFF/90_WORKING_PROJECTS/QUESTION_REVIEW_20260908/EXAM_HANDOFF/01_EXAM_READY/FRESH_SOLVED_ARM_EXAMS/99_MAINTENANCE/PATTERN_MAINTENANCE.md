# Maintaining complete Solution Patterns

For the section split and expanded peripheral library, use
[SCENARIO_MAINTENANCE.md](SCENARIO_MAINTENANCE.md). The original technique/project
records below remain maintained; their current destinations are recorded in
`SECTION_DESTINATIONS.json` rather than assumed to be under `patterns/`.

The authoritative content is in `pattern_teaching.py`, `pattern_runnable.py`,
`pattern_foundations.py` and `pattern_board_projects.py`. Existing algorithm
implementations and fixtures remain in their maintained library and
`legacy_algorithm_tests.py`. Do not edit generated pattern projects by hand.

`PATTERN_COVERAGE.json` records each pattern or workflow, its exact project,
functions, replacement files, source hashes, resources, expected result and
verification reports. Related exams are supporting references; the explicit
mapping chooses the implementation. A workflow must end with its complete
project even when its teaching sequence starts with a temporary stub.

## Rebuild and verify

Use a fresh isolated copy of the latest combined package. Run from this
maintenance directory. Python for the portal build needs `pypdf`; the algorithm
checks use the existing LLVM/GCC and Unicorn dependencies. Native builds need
Keil uVision, Arm Compiler 6 and the genuine LPC1700 device pack selected by the
project. Confirm an unchanged template builds before changing project content.

1. Edit authoritative sources and run `BUILD_STUDENT_PORTAL.py`. It rebuilds the
   portal and generated project area. Never run it concurrently with another
   generator or against an older shared snapshot.
2. Run `VERIFY_PATTERN_ALGORITHMS.py` and `VERIFY_PERIPHERAL_HELPERS.py` with the
   installed device/runtime include directories. The latter compiles production
   API and driver code and models W1C and NVIC set/clear semantics.
3. Run `VERIFY_PATTERN_PROJECTS.py --uv4 <installed-UV4.exe>`. Every baseline,
   variant and the three course projects must build as a complete native
   `SW_Debug` target. `--resume` accepts only matching source hashes from a
   successful prior native build; a new source requires a new build.
4. Run `BUILD_PATTERN_FLOW_IMAGES.py --compiler-bin <native-bin-directory>
   --device-include <LPC1700-device-include-directory>`, then
   `VERIFY_PATTERN_FLOWS.py`. The separate test images compile the same C at O0,
   retain the native assembly/startup objects, and substitute SystemInit with a
   known 100 MHz clock. They are not substitutes for normal project builds.
5. Run `VERIFY_PATTERN_COVERAGE.py`, `VERIFY_COMBINED_SOLUTIONS.py`,
   `VERIFY_STUDENT_PORTAL.py`, `VERIFY_WORKSTATION.py`,
   `VERIFY_COURSE_EXECUTION.py` and `VERIFY_PORTAL_PRESENTATION.py`.
6. Run the existing portal/workstation control and browser checks. Inspect
   pattern baselines, long listings, variant links, project links, API contracts,
   desktop and narrow layouts. Check search after adding new source listings.

`--reuse-pattern-projects` is a page-only rebuild option. It verifies every
replacement source and shared template source before reusing a project. It is
useful during a native-build sweep; it is not a way to accept stale examples.

## Interpret the reports

- `PATTERN_NATIVE_BUILDS.json`: real native compiler/linker outcome, warnings,
  complete project source hashes and individual build logs.
- `PATTERN_ALGORITHM_RESULTS.json`: C reference and actual Thumb execution,
  including existing ABI and boundary fixtures.
- `PERIPHERAL_HELPER_VALIDATION.json`: production API register-model checks.
- `PATTERN_FLOW_RESULTS.json`: complete peripheral scenarios with explicit
  input and IRQ invocation. It does not model electrical bounce, real passage
  of time, PLL behaviour, automatic NVIC dispatch or physical output quality.
  SVC verifies wrapper frame selection and the decoder/dispatcher separately
  from hardware exception entry/return.
- `PATTERN_COVERAGE_VALIDATION.json`: declarations, docs, page listings,
  downloadable sources, projects and tested implementations agree.

The O0 simulation images avoid a Unicorn 2.1.4 interaction between memory hooks
and optimized conditional MMIO instructions. Their source hashes are recorded
in `PATTERN_FLOW_IMAGE_SOURCES.json`; native project verification uses the
unchanged normal optimization and device settings. Never label simulated
observations as board tests.

## Integration with other worktrees

Snapshot hashes before work. Compare both the shared checkout and other active
worktrees before integration: unchanged shared files can still have pending
edits elsewhere. Merge authoritative source changes into the newest combined
sources, preserving routes, LED changes and unrelated edits. Rebuild generated
material under one writer from those sources; do not overlay an old generated
site or restore a whole snapshot. Recheck the shared hashes immediately before
copying only the reviewed paths, keep recoverable copies of replaced files,
and verify copied hashes afterward. Original papers, personal projects,
backups and other worktrees are never release targets.
