# Question 1: complete standalone assembly answer

The attached 20250701.pdf is labelled A2. This collection's ARM1 entry matches its actual formula and constants: seed 1, a=131, c=7, XOR with iteration n, m=255. Do not substitute the other July 1 variant (seed 6, multiplier 157).

## Put the complete file here

Copy assembly.s to Source/ASM_funct.s in a working copy of Official Combined Exam API. Keep the original Source/startup_LPC17xx.s: its stack and vector table are still needed. Its weak Reset_Handler is replaced by this answer's strong Reset_Handler. The program fills the byte array and stops at finished; it intentionally does not enter C main.

## Read the code in this order

1. DIM EQU 10 chooses ten results; SPACE DIM reserves ten bytes.
2. Reset_Handler sets previous=1, n=0, and the array address.
3. R0-R3 receive previous, a, c, n; m is stored on the caller's stack.
4. SUB SP,SP,#8 reserves one argument word and one padding word for 8-byte call alignment.
5. PUSH {R4,LR} inside the subroutine moves SP another eight bytes, so m is read from [SP,#8].
6. MUL, ADD, EOR calculate the expression; integer division, multiplication and subtraction calculate the remainder.
7. POP {R4,PC} restores the caller's R4 and returns without overwriting R0.
8. STRB stores exactly one byte. STR would write four bytes, overlap later elements, and overrun this array.
9. MOV R4,R0 feeds the new value into the next call; incrementing n advances the XOR mask.

## Expected array

Decimal: 138, 234, 63, 103, 236, 71, 126, 198, 182, 125.

Hex: 8A EA 3F 67 EC 47 7E C6 B6 7D.

This is the Q1 test only. Replace this assembly file with Q2/Q3's callable-only assembly when running the timed program.
