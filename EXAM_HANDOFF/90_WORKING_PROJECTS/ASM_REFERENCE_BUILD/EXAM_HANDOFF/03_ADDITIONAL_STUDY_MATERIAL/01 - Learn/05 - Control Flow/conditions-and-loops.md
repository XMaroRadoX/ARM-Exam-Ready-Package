# Conditions and loops

Write every loop in this order: initialize, test, body, update, repeat. Testing before the body naturally handles an empty input.

```asm
; for (i=0; i<n; ++i)
MOVS    R2, #0
for_test
CMP     R2, R1
BHS     for_done
; body
ADDS    R2, R2, #1
B       for_test
for_done
```

## Nested loops

Use different registers for the outer and inner indexes. Reset the inner index inside the outer loop.

```asm
MOVS    R4, #0                  ; i
outer_test
CMP     R4, R1
BHS     loops_done
MOVS    R5, #0                  ; j resets for every i
inner_test
CMP     R5, R2
BHS     outer_next
; body(i,j)
ADDS    R5, R5, #1
B       inner_test
outer_next
ADDS    R4, R4, #1
B       outer_test
loops_done
```

An early break branches to the label immediately after the current loop, not to the function return unless the algorithm really ends there.

