# Matrices

## Row-major traversal

```asm
; R0=base, R1=rows, R2=columns; word elements
MOVS    R3, #0                  ; row
row_test
CMP     R3, R1
BHS     matrix_done
MOVS    R4, #0                  ; column
column_test
CMP     R4, R2
BHS     next_row
MUL     R5, R3, R2
ADD     R5, R5, R4
LDR     R6, [R0, R5, LSL #2]
; use element in R6
ADDS    R4, R4, #1
B       column_test
next_row
ADDS    R3, R3, #1
B       row_test
matrix_done
```

## Transpose

Source index is `r * source_columns + c`. Destination index is `c * source_rows + r`. The destination row stride therefore differs from the source stride.

## Graph matrix

An adjacency matrix uses the same address formula. The algorithm decides what a zero or sentinel means: “no edge,” “zero-cost edge,” and “unvisited” are different concepts and must not be mixed.

