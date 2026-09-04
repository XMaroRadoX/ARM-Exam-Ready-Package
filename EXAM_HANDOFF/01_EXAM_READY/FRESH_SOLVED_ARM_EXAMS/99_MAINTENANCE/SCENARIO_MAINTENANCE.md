# Peripheral scenarios and section ownership

`scenario_library.py` owns scenario metadata, complete combination coverage,
historical mappings, section destinations, and page generation.
`scenario_engine.c` supplies the controller and hardware integration expanded
into each practice project. `lcd_scenario.py` adapts the supplied July 2024 LCD
extension without changing its original archive or the maintained template.

Standalone algorithms belong in Algorithms. General calling-convention and
memory techniques belong in ASM Reference; general exam workflows belong in
Guides. Hardware ownership, input handling, scheduling and exception integration
remain in Solution Patterns. `SECTION_DESTINATIONS.json` preserves the explicit
mapping for all 85 original techniques. Old URLs remain compatibility pages.

The new catalog contains 247 exact configurations, 47 worked application
variants, and 23 historical projects. The eight-family matrix includes every
pair, triple and larger subset. LCD is an additional historical extension.
Clock-free configurations make no timing or debounce guarantee. DAC without a
sample timer is a static voltage output, not an audio-frequency example.

## Content and evidence

Each project includes a complete template copy, replacement files, ownership
notes, expected results, and a ZIP containing all source and project files.
Historical main/assembly files come from explicit reviewed-answer mappings.
Separate support files acknowledge enabled unused button vectors and return
from counter-only SysTick interrupts. Never silently replace a reviewed answer
with a nearby exam merely because its peripheral tags match.

`PAPER_INVENTORY.json` inventories all supplied exam PDFs, including alternate
copies, the LCD extension, standalone algorithm/theory material, and
administrative documents. An unclassified board candidate is a failed audit.

## Build and check

Work in an isolated current copy, retaining the complete relative layout.
Do not regenerate the shared package while another writer is active.

1. Run `AUDIT_SCENARIO_PAPERS.py` using Python with `pypdf`.
2. Run `BUILD_STUDENT_PORTAL.py` for a complete build. Use
   `REFRESH_SCENARIOS.py --all` for scenario-only content changes, or pass exact
   scenario IDs for a deliberately scoped refresh. `--historical` rebuilds the
   historical projects. Follow any incremental refresh with `REFRESH_SEARCH.py`.
3. `MIGRATE_SCENARIO_SECTIONS.py` regenerates the original teaching pages and
   reapplies the classification. It preserves complete listings while giving
   merged content unique anchors. It requires the original pattern projects.
4. Establish an unchanged-template uVision `SW_Debug` baseline. Run
   `BUILD_NATIVE_SCENARIOS.py` for complete native compiler/assembler/linker
   checks. Its compiler flags match that baseline. Source/header/flag hashes
   govern object reuse; each complete target is linked separately. Configure
   the installed compiler and genuine device-pack paths in that script.
5. Run `VERIFY_SCENARIOS.py` and `VERIFY_SCENARIO_FLOWS.py`. They execute the
   actual native Thumb images with explicit inputs. They require the existing
   Unicorn and ELF dependencies used by the maintained peripheral tests.
6. Run the original algorithm, helper, pattern-coverage, combined-solution,
   workstation, course, portal, search, and browser checks. Unchanged native
   course builds can be reused only when every recorded source hash matches.
7. Run `BROWSER_SCENARIOS.cjs`; inspect its desktop and narrow screenshots as
   well as its filter, URL restoration, copy, and no-JavaScript assertions.

## Reports and limits

- `SCENARIO_MANIFEST.json`: projects, source hashes, resources, expected behavior,
  historical question IDs, and section routes.
- `PERIPHERAL_COMBINATIONS.json`: all 247 exact combinations and their timing
  qualifications.
- `SCENARIO_NATIVE_BUILDS.json`: native target results and source/image hashes.
- `SCENARIO_VALIDATION.json`: listing/source agreement and native controller
  execution, with historical source/vector checks distinguished explicitly.
- `SCENARIO_FLOW_RESULTS.json`: complete ADC/DAC/input/queue flows and LCD maze
  generation/movement; physical LCD drawing is substituted only in that test.
- `SCENARIO_BROWSER_RESULTS.json`: browser controls and layouts.

Native compilation is not physical-board verification. The execution model
does not establish electrical debounce, analog quality, actual time passage,
automatic interrupt arbitration, or physical LCD output. Reports retain these
limits; do not relabel source-only historical checks as full hardware tests.

Before integration, compare all original source hashes against the starting
snapshot. Back up only replaced files, copy only reviewed paths, and verify the
copied hashes. Keep original papers, starting templates, personal projects,
build caches, and unrelated files outside the integration set.
