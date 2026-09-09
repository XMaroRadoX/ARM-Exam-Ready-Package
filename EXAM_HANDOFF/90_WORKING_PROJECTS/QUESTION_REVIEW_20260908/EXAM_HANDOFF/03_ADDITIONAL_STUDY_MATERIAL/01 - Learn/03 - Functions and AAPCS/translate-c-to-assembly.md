# Translate a question into assembly

Do not translate syntax line by line. Translate data and control flow.

1. Write a C-like reference model.
2. Mark arguments, return value, local state, array widths, and signedness.
3. Turn each `for`/`while` into test-body-update labels.
4. Turn array access into a base plus scaled index.
5. Turn helper calls into AAPCS boundaries; preserve live values across `BL`.
6. Only then choose exact instructions.

Example requirement: “return the number of negative signed bytes.”

```asm
; uint32_t CountNegative(const int8_t *a, uint32_t n)
CountNegative PROC
        MOVS    R2, #0          ; i
        MOVS    R3, #0          ; count
test
        CMP     R2, R1
        BHS     done
        LDRSB   R12, [R0, R2]   ; signed byte is essential
        CMP     R12, #0
        IT      LT
        ADDLT   R3, R3, #1
        ADDS    R2, R2, #1
        B       test
done
        MOV     R0, R3
        BX      LR
        ENDP
```

Adaptation points are only the predicate and element width. The loop skeleton remains stable.

