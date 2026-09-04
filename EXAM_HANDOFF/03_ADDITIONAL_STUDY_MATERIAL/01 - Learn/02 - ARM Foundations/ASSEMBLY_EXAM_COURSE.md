# Assembly course for the ARM exam

This course teaches the assembly part of the current LPC1768/Cortex-M3 exam
project. It uses Keil ARMASM syntax and the direct `Source/ASM_funct.s` file.
Start with the mental model, then learn the function contract, memory widths,
loops and AAPCS. Use the pattern library only after those foundations.

## Course map

1. Where values live.
2. The smallest valid answer file.
3. Read the function contract.
4. Registers and AAPCS ownership.
5. Flags and signed versus unsigned branches.
6. Instruction and directive families.
7. Addresses, loads, stores and data definitions.
8. Stack frames, nested calls and extra arguments.
9. Arrays, matrices, structures and packed bits.
10. Loops, early exits and bounded output.
11. Translating an algorithm into assembly.
12. C/assembly calls and shared data.
13. Reset, SVC, exceptions and interrupts.
14. Testing and debugging.

## Lesson 1: where every value lives

Assembly has no hidden local variables. At every line, a value is in one of
four places:

- a register;
- memory at an address;
- the current stack frame;
- an immediate constant encoded in, or loaded by, an instruction.

For every important value, write four facts before coding:

```text
name: count
location: R1
width: 32 bits
meaning: unsigned number of elements
owner/lifetime: needed until the loop finishes
```

Most assembly failures are one of these: wrong location, wrong element width,
wrong signedness, lost register ownership, wrong stack offset or wrong loop
limit.

## Lesson 2: the smallest valid `assembly.s`

```asm
                AREA    |.text.asm_solution|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  asm_solution

; uint32_t asm_solution(uint32_t value)
; R0 = value; returns R0.
asm_solution    PROC
                BX      LR
                ENDP

                LTORG
                ALIGN   4
                END
```

`AREA` selects a section, `THUMB` selects Cortex-M Thumb code, `EXPORT` makes
the symbol visible to C, `PROC/ENDP` marks the function, and `END` finishes the
assembly source. `PRESERVE8` declares the eight-byte stack-alignment contract;
your code must still preserve it in practice.

Build this stub before writing the algorithm. It proves that the symbol name,
project membership and C declaration agree.

## Lesson 3: write the contract before instructions

Turn the question into a C-like prototype even if the paper gives only prose:

```c
uint32_t count_matches(const int8_t *values, uint32_t count, int8_t key);
```

Then write the assembly contract:

```text
R0 = address of signed bytes; read-only
R1 = unsigned element count
R2 = signed key in its low byte
return R0 = unsigned match count
empty input = return zero without loading memory
overflow = result cannot exceed count
```

Also record:

- which pointers may be null;
- whether input may be modified;
- output capacity and partial-output rules;
- element width and signedness;
- maximum count or recursion depth;
- the required behavior for invalid input;
- whether the routine calls another function.

Do not choose registers until this contract is fixed.

## Lesson 4: registers and AAPCS ownership

| Register | Normal exam meaning |
|---|---|
| `R0-R3` | first four argument words, return words and caller-clobbered scratch |
| `R4-R11` | callee-saved values; restore any register you modify |
| `R12` | caller-clobbered scratch |
| `R13` / `SP` | stack pointer |
| `R14` / `LR` | return address after a call; exception-return token in handlers |
| `R15` / `PC` | current instruction address |
| `APSR` | N, Z, C and V condition flags |

A leaf function executes no `BL`. It can often use only `R0-R3` and return
with `BX LR` without a stack frame.

A non-leaf function executes `BL` or `BLX`. It must save LR before the first
nested call. It must also save every modified `R4-R11` register.

```asm
; uint32_t twice_plus_one(uint32_t value)
twice_plus_one PROC
                PUSH    {R4,LR}       ; 8-byte frame
                MOV     R4, R0
                BL      helper
                ADD     R0, R0, R4
                ADDS    R0, R0, #1
                POP     {R4,PC}
                ENDP
```

Caller-clobbered means a value in `R0-R3` or `R12` may disappear across `BL`.
Move any value needed afterward to a saved register or a planned stack slot.

## Lesson 5: flags and correct branches

`CMP a,b` calculates `a-b` only to set flags. `TST a,b` calculates a bitwise
AND only to set flags. Instructions ending in `S`, such as `ADDS`, also update
flags.

| Meaning after `CMP left,right` | Branch |
|---|---|
| equal / not equal | `BEQ` / `BNE` |
| signed less / less or equal | `BLT` / `BLE` |
| signed greater / greater or equal | `BGT` / `BGE` |
| unsigned lower / lower or same | `BLO` / `BLS` |
| unsigned higher / higher or same | `BHI` / `BHS` |

Use signed branches for signed data values. Use unsigned branches for counts,
indexes, addresses and capacities. Equality is the same either way.

`C` represents an unsigned carry or no-borrow condition. `V` represents signed
overflow. They are not interchangeable.

Thumb conditional execution may use `IT`, `ITE` or related blocks, but short
branches are usually clearer in an exam. When using `IT`, keep the block small
and verify the condition suffix on every controlled instruction.

## Lesson 6: instruction and directive families

### File and data directives

| Form | Use |
|---|---|
| `AREA ..., CODE, READONLY` | executable code section |
| `AREA ..., DATA, READONLY` | constant tables |
| `AREA ..., DATA, READWRITE` | writable or zero-filled objects |
| `EQU` | named constant; allocates no bytes |
| `DCB`, `DCW`, `DCD` | initialized 8-, 16- and 32-bit objects |
| `SPACE n` | reserve `n` bytes |
| `ALIGN 2` | align the next object to four bytes in ARMASM |
| `EXPORT`, `IMPORT` | expose or consume a linker symbol |
| `PROC`, `ENDP`, `LTORG`, `END` | function/literal/file structure |

### Move and constant construction

| Instruction | Use |
|---|---|
| `MOV`, `MOVS` | copy a register or small immediate; `S` updates flags |
| `MOVW`, `MOVT` | construct low/high 16-bit halves of a 32-bit constant |
| `MVN`, `MVNS` | bitwise NOT while moving |
| `LDR Rn, =value` | assembler-generated literal or address load |
| `ADR Rn, label` | nearby position-relative address |

### Arithmetic

| Instruction | Use |
|---|---|
| `ADD`, `ADDS`, `SUB`, `SUBS` | counters, addresses and ordinary arithmetic |
| `ADC`, `ADCS`, `SBC`, `SBCS` | carry/borrow propagation across multiple words |
| `RSB`, `RSBS` | reverse subtract; often negation from zero |
| `MUL` | low 32 bits of a product |
| `MLA`, `MLS` | multiply-add or multiply-subtract |
| `UMULL`, `SMULL` | full unsigned or signed 64-bit product |
| `UDIV`, `SDIV` | unsigned or signed division when allowed by the target/question |

Do not assume a multiply or add preserves flags unless its selected encoding
has the `S` behavior you need. Wide addition starts with `ADDS` on the low word
and continues with `ADC` on the high word. Wide subtraction starts with `SUBS`
and continues with `SBC`.

### Logic, shifts and bit operations

| Instruction | Use |
|---|---|
| `AND`, `ORR`, `EOR`, `BIC` | mask, set, toggle and clear bits |
| `TST` | test selected bits without keeping the result |
| `LSL`, `LSR` | unsigned scale/extract |
| `ASR` | signed right shift preserving the sign bit |
| `ROR` | rotate bits |
| `CLZ` | count leading zeroes |
| `UXTB`, `UXTH` | keep and zero-extend 8 or 16 bits |
| `SXTB`, `SXTH` | sign-extend 8 or 16 bits when available/needed |

Always validate a variable shift count. In C, shifting a 32-bit value by 32 is
invalid; in assembly the hardware shift behavior may not match the intended
algorithm contract.

### Compare and control flow

| Instruction | Use |
|---|---|
| `CMP`, `CMN` | subtraction/addition comparison through flags |
| `TST`, `TEQ` | AND/XOR comparison through flags |
| `B`, `B<condition>` | unconditional or conditional branch |
| `CBZ`, `CBNZ` | compact zero/nonzero branch |
| `BL`, `BLX` | call a routine and write LR |
| `BX LR` | return from a normal leaf function |
| `PUSH`, `POP` | save/restore a planned register set |

### Memory access

| C-like object | Load | Store | Index step |
|---|---|---|---|
| `uint8_t` | `LDRB` | `STRB` | 1 byte |
| `int8_t` | `LDRSB` | `STRB` | 1 byte |
| `uint16_t` | `LDRH` | `STRH` | 2 bytes |
| `int16_t` | `LDRSH` | `STRH` | 2 bytes |
| 32-bit word/pointer | `LDR` | `STR` | 4 bytes |
| paired words | `LDRD` | `STRD` | 8 bytes, with alignment care |

`LDR R0, =symbol` loads the address represented by `symbol`. `LDR R1,[R0]`
dereferences that address. Confusing those two operations is a common exam
error.

### System and exception instructions

| Instruction | Use |
|---|---|
| `MRS` / `MSR` | read/write special registers such as MSP, PSP or PRIMASK |
| `SVC #imm` | enter the SVC exception from Thread mode |
| `CPSID i` / `CPSIE i` | disable/enable interrupts for a truly bounded critical section |
| `WFI` | wait for interrupt; used by `board_idle()` behavior where configured |
| `DMB`, `DSB`, `ISB` | memory/instruction ordering when a hardware contract requires it |
| `NOP` | explicit no-operation, normally only for timing/debug structure |

Do not add privileged or barrier instructions merely because they exist. Use
them only when the paper or peripheral contract requires them.

## Lesson 7: addresses, memory and assembly-defined data

```asm
COUNT           EQU     8

                AREA    |.constdata|, DATA, READONLY
table           DCD     10, 20, 30, 40

                AREA    |.data|, DATA, READWRITE
                ALIGN   2
counter         DCD     0
buffer          SPACE   COUNT
```

Use a load/store width that matches the object. A word load from a byte array
reads four bytes and may violate alignment. A byte load from a signed array
needs `LDRSB` when the sign matters.

Addressing forms you should recognize:

```asm
LDR     R2, [R0]            ; current word
LDR     R2, [R0,#8]         ; word at byte offset 8
LDR     R2, [R0,R1,LSL #2]  ; values[index] for 32-bit values
LDRB    R2, [R0],#1         ; load byte, then advance pointer
STR     R2, [R0,#4]!        ; advance address, then store
```

Use post-index and writeback only when the updated pointer is intended. A
separate `ADD` is often easier to debug.

Read the complete [defining-data guide](../01%20-%20C%20Foundations/defining-data.md)
for strings, pointer tables, structures, section placement and C/assembly
symbol sharing.

## Lesson 8: stack frames and extra arguments

At a public C/assembly call boundary, SP must be eight-byte aligned. Calculate
the frame instead of guessing:

```text
saved registers bytes + local bytes + padding bytes = total SP change
total must preserve required alignment before every BL
```

The fifth argument starts at the caller's original `[SP]`. If the callee first
pushes eight bytes, the fifth argument is now at `[SP,#8]`:

```asm
; uint32_t sum5(uint32_t a, uint32_t b, uint32_t c,
;               uint32_t d, uint32_t e)
sum5            PROC
                PUSH    {R4,LR}       ; SP moved by 8
                LDR     R4, [SP,#8]   ; original caller SP + 0
                ADD     R0, R0, R1
                ADD     R0, R0, R2
                ADD     R0, R0, R3
                ADD     R0, R0, R4
                POP     {R4,PC}
                ENDP
```

If you later add saved registers or local storage, recalculate every incoming
stack-argument offset. Do not copy the old offset unchanged.

Every exit must undo the same frame. Prefer one common epilogue for errors and
early termination.

## Lesson 9: arrays, matrices, structures and packed bits

### Array loop

Test the empty case before the first load:

```asm
                MOVS    R2, #0        ; sum
                CMP     R1, #0
                BEQ     array_done
array_loop
                LDR     R3, [R0],#4
                ADD     R2, R2, R3
                SUBS    R1, R1, #1
                BNE     array_loop
array_done
                MOV     R0, R2
```

### Row-major matrix

For `matrix[row][column]` with `columns` columns and element size `size`:

```text
byte address = base + ((row * columns) + column) * size
```

Preserve the outer row state while the inner loop changes column scratch
registers. Check both dimensions before any load.

### Structure

Assembly receives a pointer, not a copy of the structure. Use verified field
offsets and matching signed loads. C padding can move later fields; verify with
`sizeof` and `offsetof` instead of guessing.

### Packed bits

Write down bit order before coding: most-significant-bit first or
least-significant-bit first. Use masks and shifts to extract one bit, and clear
the destination field before inserting a replacement.

## Lesson 10: loops, early exits and bounded output

Four reliable loop shapes:

- Counted loop: keep a remaining count and decrement it.
- Index loop: compare an unsigned index with count.
- Pointer loop: calculate the one-past-end address and advance by element size.
- Nested loop: preserve outer state while rebuilding inner state each pass.

For output buffers, check capacity before every store:

```text
if written == capacity: return required error/partial count
store output[written]
written = written + 1
```

For run grouping, look-and-say or RLE, explicitly emit the final run after the
input loop. For searches inside nested loops, route a successful early exit to
a named cleanup/next-outer-iteration label so saved state remains balanced.

## Lesson 11: translating an algorithm

Use this order:

1. Write the exact contract and a small C oracle.
2. List edge cases and one deterministic vector.
3. Identify outer loops, inner loops and early exits.
4. Assign long-lived values to saved registers.
5. Assign short scratch values to `R0-R3`/`R12`.
6. Mark every memory access with width and signedness.
7. Mark every `BL` and calculate the stack frame.
8. Implement the smallest correct path.
9. Add empty, invalid, capacity and overflow behavior.
10. Compare assembly output with the C oracle.

Choose the method using the workstation [Solution Patterns](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/patterns/index.html).
The 12 high-priority routines are handwritten and simulator-tested. The 38
supplementary implementations are useful matching references but are not all
recommended memorization models.

## Lesson 12: C calls, assembly calls and shared objects

C calling assembly:

```c
extern uint32_t asm_solution(uint32_t value);
uint32_t result = asm_solution(input);
```

Assembly must `EXPORT asm_solution` with the same capitalization and contract.

Assembly calling C must `IMPORT` the C symbol, preserve LR and saved registers,
place arguments according to AAPCS, then use `BL`.

Shared object rule:

- define the object exactly once;
- declare it with `extern` on the other side;
- match width, signedness, array length, mutability and alignment;
- use `EXPORT` for an assembly definition and `IMPORT` for an external symbol.

Use the complete [C and assembly calling recipe](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/combinations/c-assembly-many-arguments.html).

## Lesson 13: reset, SVC, exceptions and interrupts

Cortex-M3 uses Thread mode and Handler mode. It does not behave like older ARM
cores with a set of classic banked CPU modes. An `SVC` instruction taken from
Thread mode enters Handler mode and hardware stacks:

```text
R0, R1, R2, R3, R12, LR, PC, xPSR
```

The exception LR value describes the return and whether the frame is on MSP or
PSP. A typical SVC handler tests bit 2 of LR, selects MSP or PSP, reads the
stacked PC and decodes the immediate byte before that PC.

Exact handlers, reset routines and SVC wrappers own vector-table behavior. Do
not also enable a library handler for the same vector. In `exam_config.h`, set
the corresponding `EXAM_OWN_*_HANDLER` option before defining an exact handler.

In an interrupt handler:

1. read pending flags once;
2. clear the same write-one-to-clear bits;
3. capture the minimum required state;
4. set an event for foreground work;
5. return promptly.

Use the compiled [interrupt and exception recipes](../../02%20-%20Code%20Recipes/07%20-%20Interrupts%20and%20Exceptions/)
rather than inventing a vector wrapper during the exam.

## Lesson 14: testing and debugging

Test at least:

- empty input;
- one element;
- ordinary deterministic input;
- maximum documented count/capacity;
- signed negative values where relevant;
- duplicate values;
- invalid pointer/count combination if the contract permits it;
- overflow or divide-by-zero behavior;
- canaries before and after writable buffers.

In the debugger inspect:

1. `R0-R3` at function entry.
2. Caller stack words for fifth and later arguments.
3. SP before the call, after the prologue and before return.
4. `R4-R11` before and after the routine.
5. Memory addresses and exact element contents.
6. N/Z/C/V before a suspicious conditional branch.
7. LR before every nested `BL` and at the epilogue.

Symptom guide:

| Symptom | First checks |
|---|---|
| Undefined symbol | spelling, case, C declaration, `EXPORT`, project inclusion |
| Wrong negative ordering | `LDRSB/LDRSH` and signed branches |
| Works until nested call | LR and caller-clobbered live values |
| Hard fault on return | PUSH/POP symmetry, SP alignment and overwritten stack |
| Wrong fifth argument | add the callee frame size to the caller-stack offset |
| First/last element corrupted | loop limit, element scale and output capacity |
| Correct result but caller later fails | modified `R4-R11` not restored |

## Exam readiness checklist

- I can write the minimal file and symbol stub from memory.
- I can map an exact prototype to `R0-R3`, stack arguments and return registers.
- I can explain leaf versus non-leaf and calculate the frame.
- I choose load/store width and branch signedness deliberately.
- I test empty input before the first memory access.
- I can address arrays, matrices, structures and packed bits.
- I route all exits through a balanced epilogue.
- I can call in both C-to-assembly and assembly-to-C directions.
- I understand Thread/Handler mode, MSP/PSP and the exception frame.
- I can select a historical pattern without copying unrelated setup.

Continue with the [course index](README.md), then solve a paper using the
[past-exam workstation](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/exams/index.html).
