# Assembly algorithm library repair report

Updated 4 September 2026.

[Open the local algorithm library](../01_GUIDES_AND_INDEXES/PORTAL/algorithms/index.html).

## Delivered coverage

- 169 study pages: all 109 original entries reviewed and 60 additions delivered.
- 129 independent source sets: 50 legacy groups, 19 formerly C-only groups, and 60 new routines. The remaining 40 pages describe variations sharing those sources.
- Every page includes C, callable Cortex-M3 Thumb assembly, the current interface and contract, argument locations, method, worked example, and executable expected-result fixtures.
- All 60 additions and all 19 formerly C-only entries have directly authored assembly. Existing correct assembly was retained; compiler-derived legacy listings affected by C repairs were refreshed from their repaired sources.
- Shared variations name their focus function. Exported sorting helpers are documented and tested directly, even where a compiler also inlines their bodies.
- New routines are marked **Possible variation**. Historical technique relationships are not represented as exact exam signatures. Generic Kruskal MST is distinguished from maze generation; the existing component-replacement helper is correctly described as five arguments while its old URL is retained.

The [per-page inventory](ALGORITHM_INVENTORY.json) records source groups, interfaces, exports, history labels and relative download paths. Each of the ten approved addition groups contains six routines.

## Confirmed repairs

| Area | Defect and correction |
|---|---|
| Decimal palindrome | Compared against a truncated packed reversal. The palindrome routine now compares the full widened reversed number; regressions include 123321 and 4000000004. The original packed-summary interface remains available. |
| A* | Missing neighbor exploration prevented general pathfinding. Added four-neighbor relaxation and Manhattan-priority selection; fixtures cover reachable, blocked and unreachable grids and identical start/goal. |
| Graph traversal | Duplicate pending DFS vertices could exhaust its stack and lose reachable vertices. Marking on push bounds pending storage. Graph dimensions and directly callable recursive-helper inputs are validated. |
| Graph arithmetic | Added endpoint, distance/weight overflow, disconnection and negative-cycle checks as applicable to the individual graph interfaces. |
| Numeric arithmetic | Fixed signed minimum-value negation in wide division, defined legacy Horner wraparound and added a separately named checked Horner routine. Checked recurrence indexes and additions, including Recaman fallback addition. |
| Missing assembly interfaces | Added the existing unsigned reduction and Hofstadter-Q entry points. Corrected data-object exports while retaining earlier aliases. |
| Bounds and state | Fixed exhausted counting-sort counters, corrupt queue/ring/stack state access, linked-list self-insertion, DP dimension overflow, matrix dimension checks and relevant scratch-buffer alias cases. |
| Index arithmetic | Guarded wrapped count-plus-one expressions, oversized word offsets, substring bounds, array-rotation addition and look-and-say remaining-capacity checks. |

[Detailed legacy repair notes](LEGACY_REPAIR_NOTES.json) accompany the maintained repair script. Correct existing interfaces remain available. Failure returns, partial output, scratch requirements and supported arithmetic/recursion limits are documented per routine; low-level helpers retain their explicit caller preconditions.

## Validation

| Layer | Result |
|---|---|
| 60 new source suites | C and emulated Thumb execution passed, with fixed expected vectors and independent mathematical/property cases. |
| 19 completed source suites | C and emulated Thumb execution passed. |
| 50 legacy source suites | C and emulated Thumb execution passed, including named variants and regression cases. |
| Public-function execution and ABI | All 129 source suites passed; 163 exported function entries executed, with no untested function exports. Callee-saved registers and stack restoration are checked at function returns. |
| Published downloads | All 169 downloaded C/assembly pairs passed execution; every published function export was exercised. Current download hashes match the recorded test artifacts. |
| Portal structure | 400 student pages and 393 search entries validated, including all 169 algorithm pages and their C, assembly and fixture downloads. Representative search checks passed. |
| Native Keil ARMASM | **Blocked: toolchain not located.** No native ARMASM build is claimed. |
| Physical LPC1768 execution | **Not run.** |
| Browser visual inspection | **Blocked by browser local-file URL policy.** No web server or alternate preview was used to bypass it. |

Assembly execution uses LLVM after converting ARMASM section/export/data directives to GNU syntax; the delivered instruction stream is retained. Unicorn executes Cortex-M3 Thumb code. The harness supplies standard memory routines and explicit 64-bit division ABI hooks; those runtime helpers are not a native Keil runtime test.

Fixtures exercise applicable empty/single-element cases, ties and duplicates, signed extremes, arithmetic limits, insufficient/exact capacities, disconnected graphs and recursion limits. Selected buffer canaries and unmapped-memory faults detect boundary errors; this is not exhaustive instrumentation of every memory access or a proof over all inputs. Passing source assembly through the compatible toolchain does not replace the blocked native-assembler gate.

Machine-readable evidence: [new sources](ALGORITHM_TEST_RESULTS.json), [completed sources](EXISTING_ALGORITHM_TEST_RESULTS.json), [legacy sources](LEGACY_ALGORITHM_TEST_RESULTS.json), [ABI and export coverage](ALGORITHM_ABI_COVERAGE.json), and [published downloads](PUBLISHED_ALGORITHM_TEST_RESULTS.json).

## Maintenance and reproduction

Canonical new routines live in the four `exam_algorithms_*.py` modules. The 19 completed routines live in `existing_algorithm_repairs.py`; legacy code remains in the existing additional-study source library. `algorithm_review.py` and `algorithm_pages.py` supply reviewed contracts and teaching-page content. Generated downloads are not the source of truth.

From this maintenance directory:

```text
python VERIFY_ALGORITHMS.py
python VERIFY_ALGORITHMS.py --existing
python VERIFY_ALGORITHMS.py --legacy
python VERIFY_ALGORITHM_ABI.py
python REFRESH_ALGORITHM_NOTES.py
python BUILD_STUDENT_PORTAL.py --algorithms-only
python VERIFY_ALGORITHMS.py --published
python VERIFY_STUDENT_PORTAL.py
```

The behavioral runner requires GCC, LLVM, Unicorn and pyelftools. `--reuse-build` reruns existing executable artifacts only when their C, assembly and fixture contents match; otherwise it rebuilds them. Omit it for a full compilation pass.

Algorithm files do not install startup code. Test fixtures expose `test_main`, returning zero on success and a nonzero failure location; a separate test driver supplies `main`. Use the published fixture with either its C reference or its assembly implementation, not both at once. Original papers, starting templates and personal practice files are preserved. Internal portal and download links remain relative for copying the package.
