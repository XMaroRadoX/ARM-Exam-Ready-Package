# Functions and AAPCS

## Leaf function

If only R0-R3 and R12 are modified and there is no nested call, `BX LR` is sufficient.

## Non-leaf function

```asm
; R0-R3 are inputs. This routine calls Helper.
Function PROC
        PUSH    {R4-R7, LR}
        SUB     SP, SP, #4      ; total frame 24 bytes: aligned to 8
        MOV     R4, R0          ; value needed after BL lives in preserved R4
        BL      Helper
        ADD     R0, R0, R4
        ADD     SP, SP, #4
        POP     {R4-R7, PC}
        ENDP
```

Five registers in the PUSH occupy 20 bytes, so the extra 4 bytes preserve eight-byte alignment before `BL`.

## Stacked arguments

At function entry, argument 5 is `[SP,#0]`, argument 6 is `[SP,#4]`. After pushing `frame_bytes`, add that amount to the offset.

```asm
; six arguments; PUSH is 24 bytes
PUSH    {R4-R8, LR}
LDR     R4, [SP, #24]           ; original argument 5
LDR     R5, [SP, #28]           ; original argument 6
```

## Checklist

- Save every changed R4-R11 exactly once.
- Save LR before any `BL` and return by restoring it to PC.
- Keep SP eight-byte aligned at public call boundaries.
- Assume R0-R3/R12 and flags are destroyed by a called function.
- Return a 32-bit value in R0; a 64-bit value normally uses R0 low and R1 high.

