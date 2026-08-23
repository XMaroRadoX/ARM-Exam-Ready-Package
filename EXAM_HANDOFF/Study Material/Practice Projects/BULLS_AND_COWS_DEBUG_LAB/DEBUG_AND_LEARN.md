# Bulls and Cows debug lab

## Routine contract

```c
uint32_t BullsAndCows(const uint32_t secret[4],
                      const uint32_t guess[4],
                      uint32_t secret_frequency[4],
                      uint32_t guess_frequency[4]);
```

- R0: secret base address.
- R1: guess base address.
- R2: cleared secret-frequency array.
- R3: cleared guess-frequency array.
- Result R0: `(bulls << 16) | cows`.
- Values are limited to 0-3 so they are valid frequency-array indexes.
- R4-R11 are preserved by the assembly routine.

## First debug vector

```text
secret = [0, 1, 2, 3]
guess  = [0, 2, 1, 3]
```

Expected stages:

| Stage | Bulls | Secret frequency | Guess frequency |
|---|---:|---|---|
| Start | 0 | [0,0,0,0] | [0,0,0,0] |
| Index 0 exact | 1 | unchanged | unchanged |
| Index 1 unmatched | 1 | value 1 incremented | value 2 incremented |
| Index 2 unmatched | 1 | value 2 incremented | value 1 incremented |
| Index 3 exact | 2 | [0,1,1,0] | [0,1,1,0] |
| Frequency minimum sum | 2 | unchanged | unchanged |
| Encoded result | `0x00020002` | - | - |

## Useful breakpoints

- Function entry: confirms R0-R3 pointer arguments.
- Exact-match branch: confirms equal positions do not enter frequency arrays.
- Frequency-update block: confirms values are used as indexes only after range validation by the input contract.
- Minimum-selection block: confirms each value contributes `min(secret_frequency[v], guess_frequency[v])`.
- Function epilogue: confirms encoded R0, restored SP, and restored R4-R11.

## Additional vectors

| Secret | Guess | Bulls | Cows | Encoded result |
|---|---|---:|---:|---:|
| [0,1,2,3] | [0,1,2,3] | 4 | 0 | `0x00040000` |
| [0,0,1,1] | [1,1,0,0] | 0 | 4 | `0x00000004` |
| [0,0,0,1] | [0,1,1,1] | 2 | 0 | `0x00020000` |
| [3,3,3,3] | [0,0,0,0] | 0 | 0 | `0x00000000` |

The duplicate-heavy third vector distinguishes frequency-count logic from an incorrect unrestricted nested match.

## Files

- `Source/exam/exam_asm.s`: assembly implementation.
- `Source/exam/exam_user.c`: joystick/timer/LED application.
- `Tests/june_logic_tests.c`: independent C reference vectors.
- `Tests/host_logic_tests.c`: common timing and conversion checks.

