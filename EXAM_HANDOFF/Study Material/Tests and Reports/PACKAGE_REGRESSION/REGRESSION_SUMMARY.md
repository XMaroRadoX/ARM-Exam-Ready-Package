# Automated regression summary

| Check | Passed | Total |
|---|---:|---:|
| Deterministic peripheral model | 23 | 23 |
| Host reference tests | 23 | 23 |
| LPC1768 hardware build | 12 | 23 |
| Actual ARM instruction execution | 0 | 23 |

The peripheral model tests execute native C simulations. Host tests execute independent C reference calculations. Hardware builds compile and link the actual LPC1768/ARM sources. Actual ARM instruction execution remains COMPILE_ONLY until a Keil simulator target runs the linked assembly harness; it is not inferred from either C test category.

Physical status for every project is PHYSICAL_BOARD_NOT_TESTED.
