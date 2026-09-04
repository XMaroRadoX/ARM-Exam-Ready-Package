# Memory and addressing

## Width and signedness

| C value | Load | Store | Index scale |
|---|---|---|---|
| `uint8_t` | `LDRB` | `STRB` | none |
| `int8_t` | `LDRSB` | `STRB` | none |
| `uint16_t` | `LDRH` | `STRH` | `LSL #1` |
| `int16_t` | `LDRSH` | `STRH` | `LSL #1` |
| `uint32_t`/pointer | `LDR` | `STR` | `LSL #2` |
| 64-bit pair | two words or `LDRD` when alignment permits | two words or `STRD` | `LSL #3` |

```asm
; uint32_t x = a[i]
LDR     R3, [R0, R2, LSL #2]

; int8_t x = a[i]
LDRSB   R3, [R0, R2]

; a[i++] = value using post-index pointer traversal
STR     R3, [R0], #4
```

## Matrix address

For `T matrix[rows][columns]` in row-major order:

`address = base + ((row * columns) + column) * sizeof(T)`

```asm
; R0=base, R1=row, R2=column, R3=columns; word elements
MUL     R12, R1, R3
ADD     R12, R12, R2
LDR     R0, [R0, R12, LSL #2]
```

The stride is the number of columns in the allocated matrix, not necessarily the number currently being processed.

