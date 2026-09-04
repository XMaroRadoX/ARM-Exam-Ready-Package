# Adaptation map

Change the smallest applicable item first:

| Correction type | Primary change point | Expected change |
|---|---|---|
| Array length, seed, period, pin, or threshold | `platform/exam_config.h` or the constants block in `Answer/main.c` | One definition |
| Input/output encoding | Small policy/helper in `exam/main.c` | One localized function |
| Algorithm recurrence or match rule | Named rule block in `exam/assembly.s` | One localized assembly block |
| Peripheral ownership | Configuration macros and one initialization call | Configuration plus owner hook |
| Test data | `Tests/expected_results.json` and test vectors | Data only |

Do not edit startup, CMSIS, or the common platform layer for an ordinary paper variation. Keep C prototypes and the R0-R3 assembly contract stable.
