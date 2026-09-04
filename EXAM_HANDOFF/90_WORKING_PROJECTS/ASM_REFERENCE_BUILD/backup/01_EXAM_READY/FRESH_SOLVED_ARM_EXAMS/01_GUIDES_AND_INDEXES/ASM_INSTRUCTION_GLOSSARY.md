# ARM Assembly Quick Glossary

Use this page when an instruction is unfamiliar. The answer files focus on what each algorithm is doing instead of repeating these definitions beside every line.

## AAPCS register rule

- `R0-R3`: first four arguments, return value in `R0`, and caller-saved temporary registers.
- Additional arguments: placed by the caller at `[SP]`, `[SP,#4]`, and so on before the callee changes `SP`.
- `R4-R11`: callee-saved. A function must restore any of these registers that it changes.
- `R12`: caller-saved temporary register.
- `LR`: return address. Save it before calling another function.
- `PC`: program counter. Loading `PC` through `POP` returns to the saved address.
- Public function entry and call sites must keep `SP` eight-byte aligned.

## Loads, stores, and extension

| Instruction | Meaning |
|---|---|
| `LDR` / `STR` | Load/store one 32-bit word. |
| `LDRB` / `STRB` | Load/store one unsigned byte. `LDRB` zero-extends into 32 bits. |
| `LDRH` / `STRH` | Load/store one unsigned halfword. |
| `LDRSB` / `LDRSH` | Load a signed byte/halfword and sign-extend it to 32 bits. |
| `[R0],#4` | Use the address in `R0`, then advance it by four bytes. |
| `[R0,R1,LSL #2]` | Address `R0 + R1*4`, commonly `word_array[index]`. |

## Arithmetic and flags

- `ADD`, `SUB`, `MUL`: ordinary arithmetic.
- An `S` suffix, such as `ADDS` or `SUBS`, updates the condition flags.
- `CMP a,b`: updates flags as if it calculated `a-b`, but discards the numeric result.
- `ADC` / `SBC`: add/subtract including the carry flag; useful for multiword arithmetic.
- `UMULL` / `SMULL`: produce a full 64-bit product in two registers.
- `UDIV` / `SDIV`: unsigned/signed integer division.
- `MLA`: multiply then add. `MLS`: subtract a product, often used to calculate a remainder.

Important APSR flags:

- `N`: result is negative.
- `Z`: result is zero.
- `C`: unsigned carry/no-borrow information.
- `V`: signed overflow.

## Conditions and branches

| Condition | Signed/unsigned meaning |
|---|---|
| `BEQ` / `BNE` | Equal/zero, or not equal/nonzero. |
| `BLO` / `BHS` | Unsigned lower / unsigned higher-or-same. |
| `BHI` / `BLS` | Unsigned higher / unsigned lower-or-same. |
| `BLT` / `BGE` | Signed less-than / signed greater-or-equal. |
| `BGT` / `BLE` | Signed greater-than / signed less-or-equal. |
| `BMI` / `BPL` | Negative / non-negative. |
| `BCS` / `BCC` | Carry set / carry clear. |

- `B label`: unconditional branch.
- `BL function`: call a function and place the return address in `LR`.
- `BX LR`: return to the caller.
- `CBZ` / `CBNZ`: branch when a register is zero/nonzero.
- `IT`, `ITE`, etc.: condition the following one or more Thumb instructions.

## Bits, shifts, and masks

- `AND`: keep selected bits.
- `ORR`: set selected bits.
- `EOR`: toggle bits or perform GF(2) addition.
- `BIC`: clear the bits selected by a mask.
- `TST`: update flags from an AND without storing the result.
- `LSL` / `LSR`: logical left/right shift; right shift inserts zeros.
- `ASR`: arithmetic right shift; preserves a signed value's sign bit.
- `ROR`: rotate bits right instead of discarding them.
- `REV`: reverse the byte order of a word.
- `CLZ`: count leading zero bits.

## Stack operations

- `PUSH {R4-R7,LR}`: save registers before using them.
- `POP {R4-R7,PC}`: restore registers and return using the saved `LR` value.
- `SUB SP,SP,#n`: reserve aligned local stack storage.
- `ADD SP,SP,#n`: release that storage before returning.
- If a function pushes an odd number of registers and then calls another function, it normally needs an extra four-byte alignment slot.

## Exceptions and interrupt frames

On exception entry, Cortex-M3 automatically stacks:

`R0, R1, R2, R3, R12, LR, PC, xPSR`

- `LR` bit 2 selects the saved frame: zero means MSP; one means PSP.
- A handler can inspect the stacked `PC` to locate the instruction that caused an `SVC`.
- Writing the stacked `R0` changes the value returned to the interrupted code.
- Standard handler names such as `SVC_Handler`, `SysTick_Handler`, and `TIMER0_IRQHandler` may exist only once in a linked project.
- Peripheral handlers must clear the peripheral interrupt source; SysTick is acknowledged automatically by exception entry.

## Assembler directives—not CPU instructions

- `AREA`: select a code or data section.
- `THUMB`: assemble Thumb/Thumb-2 code.
- `PRESERVE8`: declare that public stack alignment follows the eight-byte AAPCS rule.
- `EXPORT` / `IMPORT`: expose or reference a linker symbol.
- `PROC` / `ENDP`: mark a procedure for assembler metadata.
- `DCD`, `DCB`, `SPACE`: define words, bytes, or reserved storage.
- `END`: end the assembly source file.
