# ARM Assembly Exam Reference

Cortex-M3 / Keil ARMASM. Generated from the same content as [ASM Reference](PORTAL/asm/index.html).

Use Source/ASM_funct.s in your copied project. Examples require the stated inputs and memory.


## Values


### MOV / MOVS

Copy a register or load an encodable constant.


**Syntax**

```asm
MOV R0, R1
MOVS R0, #7
```


**Operands and rules:** Use R0–R12 for ordinary operands. SP/PC forms have extra restrictions; the syntax shown avoids them. Immediates must fit an instruction encoding; use LDR Rd,=constant for arbitrary 32-bit constants.


**Flags:** MOV preserves NZCV; MOVS updates N/Z, may update C for a modified immediate, and preserves V. A small immediate such as #7 preserves C.


**Example**

```asm
        MOVS R0, #7
        MOV R1, R0
```


**Expected result:** R0=7; R1=7. MOV copies the value, not memory at that address.


**Watch for:** Do not assume every 32-bit constant fits MOV.


### MOVW / MOVT

Build a 32-bit constant from two 16-bit pieces.


**Syntax**

```asm
MOVW R0, #0x5678
MOVT R0, #0x1234
```


**Operands and rules:** Immediate range is 0..65535. MOVW clears the top half; MOVT preserves the bottom half. Use general registers, not SP/PC.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVW R0, #0x5678
        MOVT R0, #0x1234
```


**Expected result:** R0=0x12345678.


**Watch for:** MOVT does not initialize the low 16 bits.


### MVN / MVNS

Invert every bit of the second operand.


**Syntax**

```asm
MVN R0, R1
```


**Operands and rules:** Use R0–R12 for ordinary operands. SP/PC forms have extra restrictions; the syntax shown avoids them. Immediates must fit an instruction encoding; use LDR Rd,=constant for arbitrary 32-bit constants.


**Flags:** The S form updates N/Z and the shifter carry C; V is unchanged. With an unshifted register operand C is preserved.


**Example**

```asm
        MOVS R1, #0
        MVN R0, R1
```


**Expected result:** R0=0xFFFFFFFF (unsigned maximum or signed -1).


**Watch for:** Bitwise inversion is not arithmetic negation; use RSB from zero for -x.


### ADR

Compute the address of a nearby label in the same section.


**Syntax**

```asm
ADR R0, local_data
```


**Operands and rules:** PC-relative range depends on encoding; wide forms reach up to 4095 bytes. Label must be in the same area. Use LDR =label for a distant or external symbol.


**Flags:** NZCV unchanged.


**Example**

```asm
        ADR R0, local_data
        B after_data
        ALIGN 4
local_data DCD 27
after_data
```


**Expected result:** R0 points to local_data; no data has been loaded from it.


**Watch for:** An address is not the value stored there.


### ADRL

Compute a wider-range PC-relative address using an ARMASM pseudo-instruction.


**Syntax**

```asm
ADRL R0, nearby
```


**Operands and rules:** On Cortex-M3 Thumb-2, ARMASM expands ADRL into two 32-bit data-processing instructions. A PC-relative label must be in the same section and reachable by the expansion. Set bit 0 when using the address as a Thumb function pointer for BX/BLX.


**Flags:** NZCV unchanged.


**Example**

```asm
        ADRL R0, nearby
        B after_nearby
        ALIGN 4
nearby  DCD 12
after_nearby
```


**Expected result:** R0 receives the address of nearby, not its stored value. The pseudo-instruction needs ARMASM; it is not a hardware opcode.


**Watch for:** A raw even code address passed to BX can attempt an unsupported state switch. Use an appropriate Thumb function symbol or set bit 0.


### MOV32

Load a 32-bit value using ARMASM expansion into MOVW and MOVT.


**Syntax**

```asm
MOV32 R0, #0x12345678
```


**Operands and rules:** ARMASM pseudo-instruction; use a general register and a 32-bit constant or supported relocatable expression. It emits instructions rather than a literal-pool read.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOV32 R0, #0x12345678
```


**Expected result:** R0=0x12345678, equivalent here to MOVW #0x5678 followed by MOVT #0x1234.


**Watch for:** Other assemblers may not recognize MOV32 even when they support MOVW/MOVT.


## Memory


### LDR

Load a 32-bit word, or use the = pseudo-instruction to obtain a constant/address.


**Syntax**

```asm
LDR R0, [R1]
LDR R0, [R1, #4]
LDR R0, [R1, R2, LSL #2]
LDR R0, =0x12345678
```


**Operands and rules:** Square brackets mean a memory access. =constant/=label is assembler syntax that may use a literal pool. Ordinary word data should be 4-byte aligned; access only valid memory. Immediate offsets depend on encoding (a common positive wide offset is 0..4095).


**Flags:** NZCV unchanged.


**Example**

```asm
        LDR R1, =values
        LDR R0, [R1, #4]
        B after_values
        ALIGN 4
values  DCD 11,22
after_values
```


**Expected result:** R1 is the array address; R0=22.


**Watch for:** LDR R0,=values gets the address; LDR R0,[R0] then reads the first word.


### LDRB / LDRH / LDRSB / LDRSH

Read a byte or halfword and extend it to a 32-bit register.


**Syntax**

```asm
LDRB R0, [R1]
LDRH R0, [R1]
LDRSB R0, [R1]
LDRSH R0, [R1]
```


**Operands and rules:** B/SB reads 1 byte; H/SH reads 2 bytes. LDRB/LDRH zero-extend. LDRSB/LDRSH sign-extend. Use aligned halfwords; do not use PC as the destination.


**Flags:** NZCV unchanged.


**Example**

```asm
        LDR R1, =byte_data
        LDRB R0, [R1]
        LDRSB R2, [R1]
        B after_byte
byte_data DCB 0xFE
        ALIGN 2
after_byte
```


**Expected result:** R0=254; R2=0xFFFFFFFE (-2).


**Watch for:** An unsigned load destroys the intended sign of int8_t/int16_t data.


### STR / STRB / STRH

Write the low word, byte, or halfword of a register.


**Syntax**

```asm
STR R0, [R1]
STRB R0, [R1]
STRH R0, [R1]
```


**Operands and rules:** R1 must point to writable storage. STR writes 4 bytes; STRB writes the lowest 8 bits; STRH writes the lowest 16 bits. Use naturally aligned data.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #0xAB
        STRB R0, [R1]
```


**Expected result:** With R1 pointing to writable byte storage, that byte becomes 0xAB. Neighboring bytes are unchanged.


**Watch for:** A store has no signed/unsigned variant. STR can overwrite adjacent bytes if the object is only one byte.


### LDRD / STRD

Transfer two 32-bit words using consecutive memory locations.


**Syntax**

```asm
LDRD R0, R1, [R2]
STRD R0, R1, [R2, #8]
```


**Operands and rules:** Address must be word-aligned even if unaligned ordinary loads are enabled. Registers must be distinct, neither SP nor PC. Immediate offset is a multiple of 4 from -1020 to +1020; avoid writeback overlap with a transferred register.


**Flags:** NZCV unchanged.


**Example**

```asm
        LDRD R0, R1, [R2]
```


**Expected result:** If words at R2 and R2+4 are 10 and 20, R0=10 and R1=20.


**Watch for:** These instructions always fault on an unaligned address.


### LDM / LDMIA / LDMFD / LDMDB / STM / STMIA / STMDB / STMFD

Load or store a register list from consecutive word addresses.


**Syntax**

```asm
STMIA R0!, {R1-R3}
LDMIA R0!, {R1-R3}
STMFD SP!, {R4,LR}
LDMFD SP!, {R4,PC}
```


**Operands and rules:** IA increments after each word; DB decrements before the block. ! writes back the base. Registers transfer in increasing register-number order. Keep base out of a writeback list and addresses word-aligned. Cortex-M3 supports IA/DB, not every ARM-state addressing mode. Multi-register wide forms need at least two registers; PUSH/POP provide useful single-register forms.


**Flags:** NZCV unchanged.


**Example**

```asm
        STMFD SP!, {R4,LR}
        MOVS R4, #9
        LDMFD SP!, {R4,PC}
```


**Expected result:** Saves 8 bytes, uses R4, then restores R4 and returns. STMFD=STMDB; LDMFD=LDMIA for a full descending stack.


**Watch for:** The order written inside braces does not change memory order.


## Arithmetic


### ADD / ADDS / ADDW

Add operands; keep the low 32 bits.


**Syntax**

```asm
ADD R0, R1, R2
ADDS R0, R1, R2
ADDW R0, R1, #1000
```


**Operands and rules:** Use R0–R12 for ordinary operands. SP/PC forms have extra restrictions; the syntax shown avoids them. Immediates must fit an instruction encoding; use LDR Rd,=constant for arbitrary 32-bit constants. ADDW uses an unsigned 12-bit immediate (0..4095) and does not set flags.


**Flags:** The S form updates N/Z/C/V. The non-S form preserves them. C means carry for addition and no borrow for subtraction.


**Example**

```asm
        LDR R1, =0xFFFFFFFF
        ADDS R0, R1, #1
```


**Expected result:** R0=0; N=0 Z=1 C=1 V=0.


**Watch for:** Carry signals unsigned overflow; V signals signed overflow.


### SUB / SUBS / SUBW

Subtract the second operand from the first.


**Syntax**

```asm
SUB R0, R1, R2
SUBS R0, R1, #1
SUBW R0, R1, #1000
```


**Operands and rules:** Use R0–R12 for ordinary operands. SP/PC forms have extra restrictions; the syntax shown avoids them. Immediates must fit an instruction encoding; use LDR Rd,=constant for arbitrary 32-bit constants. SUBW uses an unsigned 12-bit immediate (0..4095), with no flag update.


**Flags:** The S form updates N/Z/C/V. The non-S form preserves them. C means carry for addition and no borrow for subtraction.


**Example**

```asm
        MOVS R1, #0
        SUBS R0, R1, #1
```


**Expected result:** R0=0xFFFFFFFF; N=1 Z=0 C=0 V=0.


**Watch for:** C=0 means a borrow was needed. Do not treat C as a borrow flag.


### ADC / ADCS / SBC / SBCS

Carry or borrow between words of a wide integer.


**Syntax**

```asm
ADCS R0, R0, R2
SBCS R0, R0, R2
```


**Operands and rules:** ADC computes Rn+operand+C. SBC computes Rn-operand-(1-C). Establish C with the low-word ADDS/SUBS immediately before processing the high word.


**Flags:** The S form updates N/Z/C/V. The non-S form preserves them. C means carry for addition and no borrow for subtraction.


**Example**

```asm
        LDR R0, =0xFFFFFFFF
        MOVS R1, #0
        MOVS R2, #1
        MOVS R3, #0
        ADDS R0, R0, R2
        ADC R1, R1, R3
```


**Expected result:** R1:R0 becomes 0x00000001:00000000.


**Watch for:** An unrelated flag-setting instruction between words breaks the carry chain.


### RSB / RSBS / NEG / NEGS

Reverse subtraction; subtract a value from zero to negate it.


**Syntax**

```asm
RSB R0, R1, #0
RSBS R0, R1, #0
```


**Operands and rules:** For the shown negation form, R0=0-R1. NEG/NEGS are aliases for reverse subtraction from zero. Wide RSB also accepts a register or shifted-register second operand, computing Operand2-Rn.


**Flags:** The S form updates N/Z/C/V. The non-S form preserves them. C means carry for addition and no borrow for subtraction.


**Example**

```asm
        MOVS R1, #7
        RSBS R0, R1, #0
```


**Expected result:** R0=0xFFFFFFF9 (-7).


**Watch for:** Negating signed INT_MIN overflows; the result still has bit 31 set.


### MUL / MULS

Multiply and keep the low 32 bits.


**Syntax**

```asm
MUL R0, R1, R2
MULS R0, R1, R0
```


**Operands and rules:** No immediate operands. MULS uses the narrow low-register form with the destination also an input. Use ordinary registers for MUL.


**Flags:** MUL preserves NZCV; MULS updates N/Z only, preserving C/V.


**Example**

```asm
        MOVS R1, #6
        MOVS R2, #7
        MUL R0, R1, R2
```


**Expected result:** R0=42.


**Watch for:** MUL does not report multiplication overflow through C or V.


### MLA / MLS

Multiply and add, or subtract a product.


**Syntax**

```asm
MLA R0, R1, R2, R3
MLS R0, R1, R2, R3
```


**Operands and rules:** Register operands only, no SP/PC. MLA=R1*R2+R3; MLS=R3-R1*R2. Result is truncated to 32 bits.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R1, #4
        MOVS R2, #10
        MOVS R3, #47
        MLS R0, R1, R2, R3
```


**Expected result:** R0=47-4*10=7.


**Watch for:** The last operand in MLS is the value from which the product is subtracted.


### UMULL / SMULL / UMLAL / SMLAL

Produce or accumulate a full 64-bit product.


**Syntax**

```asm
UMULL R0, R1, R2, R3
SMULL R0, R1, R2, R3
UMLAL R0, R1, R2, R3
```


**Operands and rules:** Destination order is low, high. Destinations must differ; no SP/PC. U means unsigned, S means signed. MLAL adds the product to the existing destination pair; initialize both words first.


**Flags:** NZCV unchanged.


**Example**

```asm
        LDR R2, =0xFFFFFFFF
        MOVS R3, #2
        UMULL R0, R1, R2, R3
```


**Expected result:** Unsigned result R1:R0=0x00000001:FFFFFFFE. SMULL with the same inputs gives 0xFFFFFFFF:FFFFFFFE (-2).


**Watch for:** SMULL is signed multiply-long, not MUL with an S flag suffix.


### UDIV / SDIV

Divide integers and return the quotient.


**Syntax**

```asm
UDIV R0, R1, R2
SDIV R0, R1, R2
```


**Operands and rules:** Register divisor only; no SP/PC. UDIV is unsigned. SDIV rounds toward zero. Check divisor is nonzero: divide-by-zero may fault when trapping is enabled, otherwise returns zero. INT_MIN/-1 cannot fit a signed 32-bit result.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R1, #47
        MOVS R2, #10
        UDIV R0, R1, R2
        MLS R3, R0, R2, R1
```


**Expected result:** R0=4; R3=7 (remainder).


**Watch for:** No general MOD instruction exists here; calculate n-q*d.


## Compare and branch


### CMP / CMN

Update flags from subtraction or addition without storing the result.


**Syntax**

```asm
CMP R0, R1
CMP R0, #10
CMN R0, #1
```


**Operands and rules:** Use R0–R12 for ordinary operands. SP/PC forms have extra restrictions; the syntax shown avoids them. Immediates must fit an instruction encoding; use LDR Rd,=constant for arbitrary 32-bit constants. CMP computes R0-operand; CMN computes R0+operand.


**Flags:** Always updates N/Z/C/V.


**Example**

```asm
        MOVS R0, #5
        CMP R0, #7
```


**Expected result:** R0 remains 5; N=1 Z=0 C=0 V=0.


**Watch for:** Branch before another instruction replaces the flags you intended to test.


### TST / TEQ

Test bits with AND or compare bit patterns with XOR, discarding the result.


**Syntax**

```asm
TST R0, #8
TEQ R0, R1
```


**Operands and rules:** Use R0–R12 for ordinary operands. SP/PC forms have extra restrictions; the syntax shown avoids them. Immediates must fit an instruction encoding; use LDR Rd,=constant for arbitrary 32-bit constants.


**Flags:** Updates N/Z and shifter carry C; V unchanged. An unshifted register operand preserves C.


**Example**

```asm
        MOVS R0, #8
        TST R0, #8
```


**Expected result:** Z=0 because bit 3 is set. R0 stays 8.


**Watch for:** For TST, BEQ means none of the tested bits were set.


### B

Jump to a label without saving a return address.


**Syntax**

```asm
B loop
```


**Operands and rules:** Target must be reachable; wide B has a larger range than narrow B. Branch to Thumb code, not a data table.


**Flags:** NZCV unchanged.


**Example**

```asm
        B done
        MOVS R0, #99
done
```


**Expected result:** The MOVS is skipped; R0 is unchanged.


**Watch for:** B does not create a return address. Use BL for a normal function call.


### BEQ

Branch when equal / zero.


**Syntax**

```asm
BEQ matched
```


**Operands and rules:** Tests Z=1. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #5
        CMP R0, #5
        BEQ matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BNE

Branch when not equal / nonzero.


**Syntax**

```asm
BNE matched
```


**Operands and rules:** Tests Z=0. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #5
        CMP R0, #7
        BNE matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BCS

Branch when unsigned higher or same / no borrow.


**Syntax**

```asm
BCS matched
```


**Operands and rules:** Tests C=1. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #7
        CMP R0, #5
        BCS matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BHS

Branch when unsigned higher or same (alias of CS).


**Syntax**

```asm
BHS matched
```


**Operands and rules:** Tests C=1. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #7
        CMP R0, #5
        BHS matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BCC

Branch when unsigned lower / borrow.


**Syntax**

```asm
BCC matched
```


**Operands and rules:** Tests C=0. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #5
        CMP R0, #7
        BCC matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BLO

Branch when unsigned lower (alias of CC).


**Syntax**

```asm
BLO matched
```


**Operands and rules:** Tests C=0. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #5
        CMP R0, #7
        BLO matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BHI

Branch when unsigned higher.


**Syntax**

```asm
BHI matched
```


**Operands and rules:** Tests C=1 and Z=0. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #7
        CMP R0, #5
        BHI matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BLS

Branch when unsigned lower or same.


**Syntax**

```asm
BLS matched
```


**Operands and rules:** Tests C=0 or Z=1. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #5
        CMP R0, #7
        BLS matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BGE

Branch when signed greater or equal.


**Syntax**

```asm
BGE matched
```


**Operands and rules:** Tests N=V. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #7
        CMP R0, #5
        BGE matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BLT

Branch when signed less than.


**Syntax**

```asm
BLT matched
```


**Operands and rules:** Tests N!=V. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #5
        CMP R0, #7
        BLT matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BGT

Branch when signed greater than.


**Syntax**

```asm
BGT matched
```


**Operands and rules:** Tests Z=0 and N=V. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #7
        CMP R0, #5
        BGT matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BLE

Branch when signed less or equal.


**Syntax**

```asm
BLE matched
```


**Operands and rules:** Tests Z=1 or N!=V. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #5
        CMP R0, #7
        BLE matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BMI

Branch when negative result.


**Syntax**

```asm
BMI matched
```


**Operands and rules:** Tests N=1. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #5
        CMP R0, #7
        BMI matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BPL

Branch when nonnegative result.


**Syntax**

```asm
BPL matched
```


**Operands and rules:** Tests N=0. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #7
        CMP R0, #5
        BPL matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BVS

Branch when signed overflow.


**Syntax**

```asm
BVS matched
```


**Operands and rules:** Tests V=1. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        LDR R0, =0x7FFFFFFF
        ADDS R0, R0, #1
        BVS matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### BVC

Branch when no signed overflow.


**Syntax**

```asm
BVC matched
```


**Operands and rules:** Tests V=0. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #7
        CMP R0, #5
        BVC matched
        MOVS R2, #0
        B finished
matched
        MOVS R2, #1
finished
```


**Expected result:** The condition is true here, so R2=1.


**Watch for:** MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.


### CBZ / CBNZ

Branch directly when a low register is zero or nonzero.


**Syntax**

```asm
CBZ R0, empty
CBNZ R0, nonempty
```


**Operands and rules:** R0–R7 only; forward-only target, 0..126 bytes from the architectural PC, even offset. No IT block. Use CMP/Bxx for backward loops or more distant targets.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #0
        CBZ R0, empty
        MOVS R1, #99
empty
```


**Expected result:** The MOVS R1 is skipped.


**Watch for:** CBNZ cannot directly branch backward to the top of a loop.


### IT / ITT / ITE / ITTT / ITTE / ITET / ITEE / ITTTT / ITTTE / ITTET / ITTEE / ITETT / ITETE / ITEET / ITEEE

Condition up to four following Thumb instructions.


**Syntax**

```asm
CMP R0, #0
ITE EQ
MOVEQ R1, #1
MOVNE R1, #0
```


**Operands and rules:** T uses the first condition; E uses its inverse. Following instruction suffixes must match the block. Do not nest IT. A branch or PC write can occur only in the final slot. Prefer ordinary branches if a block becomes hard to follow.


**Flags:** NZCV unchanged. Instructions inside the block may alter flags if explicitly requested; this can affect later slots.


**Example**

```asm
        CMP R0, #0
        ITE EQ
        MOVEQ R1, #1
        MOVNE R1, #0
```


**Expected result:** R1=1 if R0 was zero, otherwise R1=0.


**Watch for:** Conditional non-branch instructions need an IT context; do not rely on assembler auto-IT settings.


## Bits and shifts


### AND / ANDS / ORR / ORRS / EOR / EORS / BIC / BICS / ORN / ORNS

Keep, set, toggle, or clear selected bits.


**Syntax**

```asm
AND R0, R1, R2
ORR R0, R1, #8
EOR R0, R1, #8
BIC R0, R1, #8
ORN R0, R1, R2
```


**Operands and rules:** Use R0–R12 for ordinary operands. SP/PC forms have extra restrictions; the syntax shown avoids them. Immediates must fit an instruction encoding; use LDR Rd,=constant for arbitrary 32-bit constants. AND=a&b; ORR=a|b; EOR=a^b; BIC=a&~b; ORN=a|~b.


**Flags:** The S form updates N/Z and the shifter carry C; V is unchanged. With an unshifted register operand C is preserved.


**Example**

```asm
        MOVS R0, #15
        BIC R0, R0, #8
        EOR R0, R0, #1
```


**Expected result:** R0 goes from 15 to 7 to 6.


**Watch for:** Use a mask (1<<bit), not the bit number itself.


### LSL / LSLS / LSR / LSRS / ASR / ASRS

Shift left, shift right with zeros, or shift right preserving the sign.


**Syntax**

```asm
LSL R0, R1, #2
LSR R0, R1, #1
ASR R0, R1, #1
```


**Operands and rules:** Immediate LSL is 0..31; LSR/ASR are 1..32. Register shifts use the low 8 bits of the count and have defined special behavior at/above 32; do not assume count modulo 32. Use ordinary registers.


**Flags:** S forms update N/Z and C (last bit shifted out); V unchanged. A zero register shift preserves C.


**Example**

```asm
        LDR R1, =0xFFFFFFFC
        LSR R0, R1, #1
        ASR R2, R1, #1
```


**Expected result:** R0=0x7FFFFFFE; R2=0xFFFFFFFE (-2).


**Watch for:** ASR rounds negative values downward; SDIV rounds toward zero. They differ for negative odd values.


### ROR / RORS / RRX / RRXS

Rotate bits, optionally through carry.


**Syntax**

```asm
ROR R0, R1, #8
RRX R0, R1
```


**Operands and rules:** Immediate ROR is 1..31. RRX rotates one bit through C: old C enters bit 31; old bit 0 is the carry output if flags are updated. Use ordinary registers.


**Flags:** S forms update N/Z/C; V unchanged. Non-S RRX reads C but preserves flags.


**Example**

```asm
        LDR R1, =0x12345678
        ROR R0, R1, #8
```


**Expected result:** R0=0x78123456.


**Watch for:** ROR preserves rotated bits; LSR discards them.


### SXTB / SXTH / UXTB / UXTH

Extend the low byte/halfword already in a register.


**Syntax**

```asm
SXTB R0, R1
SXTH R0, R1
UXTB R0, R1
UXTH R0, R1
```


**Operands and rules:** S variants sign-extend; U variants zero-extend. No memory access. Optional source rotation supports 0,8,16,24 bits in wide forms.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R1, #0xFE
        SXTB R0, R1
        UXTB R2, R1
```


**Expected result:** R0=-2; R2=254.


**Watch for:** SXTB reads a register; LDRSB reads memory.


### REV / REV16 / REVSH / RBIT / CLZ

Reorder bits/bytes or count leading zero bits.


**Syntax**

```asm
REV R0, R1
REV16 R0, R1
REVSH R0, R1
RBIT R0, R1
CLZ R0, R1
```


**Operands and rules:** REV reverses four bytes; REV16 reverses bytes within each halfword; REVSH reverses the low halfword then sign-extends; RBIT reverses all 32 bits. CLZ(0)=32. No SP/PC.


**Flags:** NZCV unchanged.


**Example**

```asm
        LDR R1, =0x12345678
        REV R0, R1
        MOVS R2, #16
        CLZ R3, R2
```


**Expected result:** R0=0x78563412; R3=27.


**Watch for:** REV does not reverse bit order; use RBIT.


### UBFX / SBFX / BFI / BFC

Extract, insert, or clear a contiguous bit field.


**Syntax**

```asm
UBFX R0, R1, #4, #3
SBFX R0, R1, #4, #3
BFI R0, R1, #4, #3
BFC R0, #4, #3
```


**Operands and rules:** lsb=0..31; width=1..(32-lsb). UBFX zero-extends; SBFX sign-extends. BFI copies the source low width bits into the destination field; BFC clears that field.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R1, #0x70
        UBFX R0, R1, #4, #3
        SBFX R2, R1, #4, #3
```


**Expected result:** R0=7; R2=0xFFFFFFFF (-1).


**Watch for:** The last operand is field width, not the highest bit number.


### SSAT / USAT

Clamp an integer to a signed or unsigned range.


**Syntax**

```asm
SSAT R0, #8, R1
USAT R0, #8, R1
```


**Operands and rules:** SSAT width 1..32; USAT width 0..31. Input is interpreted as a signed 32-bit value. SSAT #8 clamps to -128..127; USAT #8 clamps to 0..255. Optional LSL/ASR can precede saturation.


**Flags:** NZCV unchanged; Q is set if saturation occurs and remains sticky until explicitly cleared.


**Example**

```asm
        MOVW R1, #300
        USAT R0, #8, R1
```


**Expected result:** R0=255; Q=1.


**Watch for:** UXTB truncates; USAT clamps. They are not interchangeable.


## Calls and stack


### BL / BLX

Call a function and save a return address in LR.


**Syntax**

```asm
BL helper
BLX R3
```


**Operands and rules:** BL uses a label. Cortex-M3 BLX supports the register form; the function pointer must have bit 0 set for Thumb. Save your incoming LR if you will return after another call.


**Flags:** NZCV unchanged. The called routine may change NZCV and caller-saved registers.


**Example**

```asm
        PUSH {R4,LR}
        BL helper
        POP {R4,PC}
helper
        ADDS R0, R0, #1
        BX LR
```


**Expected result:** Returns the original R0 plus 1, with the caller’s R4 restored and SP balanced.


**Watch for:** BL overwrites LR, and the callee may overwrite R0–R3/R12. Save live values.


### BX

Branch to a register, usually returning with BX LR.


**Syntax**

```asm
BX LR
```


**Operands and rules:** For normal calls the target must have bit 0 set (Thumb). In an exception handler, LR can instead hold EXC_RETURN; that uses the hardware exception-return mechanism.


**Flags:** NZCV unchanged.


**Example**

```asm
        MOVS R0, #42
        BX LR
```


**Expected result:** Returns 42 to a normal caller.


**Watch for:** A nested BL destroys the original LR unless you saved it.


### PUSH / POP

Save/restore registers on the descending stack.


**Syntax**

```asm
PUSH {R4-R6,LR}
POP {R4-R6,PC}
```


**Operands and rules:** PUSH decrements SP; POP increments SP. Registers transfer in numerical order, 4 bytes each. POP {PC} returns via the saved LR slot. Keep stack word-aligned at all times and 8-byte aligned at public calls. Do not put SP in the list.


**Flags:** NZCV unchanged.


**Example**

```asm
        PUSH {R4,LR}
        MOVS R4, #3
        MOV R0, R4
        POP {R4,PC}
```


**Expected result:** Returns 3; restores the caller’s R4 and the original SP.


**Watch for:** PUSH {R4-R7,LR} consumes 20 bytes; add 4 bytes of padding before calling another public function.


### Fifth-argument

Locate stack arguments after saving registers.


**Syntax**

```asm
; uint32_t fifth(uint32_t a,uint32_t b,uint32_t c,uint32_t d,uint32_t e);
fifth PROC
        PUSH {R4,LR}
        LDR R0, [SP, #8]
        POP {R4,PC}
        ENDP
```


**Operands and rules:** For five 32-bit arguments, a..d use R0..R3; e is at entry SP. After this 8-byte push, e is at current SP+8. Include every push and local/padding allocation when calculating an offset. The caller puts the first stacked argument at its current SP, with any padding after the arguments.


**Flags:** NZCV unchanged.


**Example**

```asm
fifth PROC
        PUSH {R4,LR}
        LDR R0, [SP, #8]
        POP {R4,PC}
        ENDP
```


**Expected result:** fifth(1,2,3,4,99) returns 99 and restores R4/SP.


**Watch for:** A fifth parameter is not always the fifth word; 64-bit types can introduce alignment gaps earlier.


## Exceptions and system


### MRS / MSR

Read or write a special register.


**Syntax**

```asm
MRS R0, APSR
MRS R1, MSP
MSR APSR_nzcvq, R0
MSR PRIMASK, R1
```


**Operands and rules:** Available registers depend on privilege and access direction. APSR exposes status flags; MSP/PSP are stack pointers; PRIMASK/BASEPRI/FAULTMASK affect exception masking. CONTROL changes execution control. Use ISB after a CONTROL change.


**Flags:** MRS preserves flags. MSR APSR_nzcvq writes N/Z/C/V/Q; other special-register writes do not directly change NZCV.


**Example**

```asm
        MRS R0, APSR
```


**Expected result:** R0 holds a status snapshot; NZCV occupy bits 31..28.


**Watch for:** Cortex-M3 uses APSR/xPSR and special registers, not the ARM-state CPSR/SPSR programming model.


### CPSID / CPSIE

Mask or unmask configurable interrupts using PRIMASK.


**Syntax**

```asm
CPSID i
CPSIE i
```


**Operands and rules:** Privileged use. i changes PRIMASK. Masking does not disable NMI or HardFault. In reusable code, save and restore the previous mask instead of blindly enabling interrupts.


**Flags:** NZCV unchanged.


**Example**

```asm
        MRS R0, PRIMASK
        CPSID i
        ; short critical section, keep R0 intact
        MSR PRIMASK, R0
```


**Expected result:** Restores exactly the previous interrupt mask.


**Watch for:** CPSIE i may enable interrupts that your caller intentionally disabled.


### SVC

Request a supervisor-call exception.


**Syntax**

```asm
SVC #7
```


**Operands and rules:** Immediate is 0..255. The installed SVC_Handler must implement the intended service. Normal C function-call argument rules alone do not define an SVC service.


**Flags:** NZCV are saved in the exception frame and restored on return unless the frame is deliberately changed.


**Example**

```asm
        SVC #7
```


**Expected result:** Requests service number 7; the result depends on SVC_Handler.


**Watch for:** Use the stacked return PC minus 2 to locate the SVC instruction; the immediate is its low byte.


### DMB / DSB / ISB

Order memory accesses, wait for completion, or refresh the instruction pipeline.


**Syntax**

```asm
DMB
DSB
ISB
```


**Operands and rules:** Use the full-system form shown. DMB orders explicit memory accesses; DSB also waits for required completion; ISB makes following instructions observe updated execution context. These are not delays.


**Flags:** NZCV unchanged.


**Example**

```asm
        DSB
        ISB
```


**Expected result:** Required prior work completes; subsequent instructions use the updated execution context.


**Watch for:** A memory barrier does not replace interrupt masking or an atomic update.


### WFI / WFE / SEV / NOP / YIELD

Wait for an interrupt/event, signal an event, or issue an execution hint.


**Syntax**

```asm
WFI
WFE
SEV
NOP
YIELD
```


**Operands and rules:** WFI waits for a qualifying wake event; WFE uses the event mechanism and may return immediately if an event is pending. SEV signals an event. NOP has no data effect. YIELD is a scheduling hint. Wakeup is not a guarantee that a particular handler ran.


**Flags:** NZCV unchanged.


**Example**

```asm
        NOP
```


**Expected result:** No register or memory result changes.


**Watch for:** Do not use instruction counts as a reliable time delay; use a timer.


### BKPT / UDF

Stop under a debugger or deliberately execute an undefined instruction.


**Syntax**

```asm
BKPT #0
UDF #0
```


**Operands and rules:** BKPT immediate 0..255. UDF has narrow/wide immediate encodings. These are debugging/fault paths, not normal returns; behavior depends on debugger and fault configuration.


**Flags:** No ordinary computed NZCV result; exception/debug entry may follow.


**Example**

```asm
        BKPT #0
```


**Expected result:** Debugger stops here when configured to handle the breakpoint.


**Watch for:** BKPT without an attached debugger can cause a fault.


### LDREX / LDREXB / LDREXH / STREX / STREXB / STREXH / CLREX

Use an exclusive monitor to attempt an atomic memory update.


**Syntax**

```asm
LDREX R1, [R0]
STREX R2, R1, [R0]
CLREX
```


**Operands and rules:** Pair load/store widths and addresses; align to transfer size. STREX status must not overlap source/base. Use supported normal memory, not arbitrary device registers. STREX returns 0 on success, 1 on failure; retry as required. Add barriers when ordering other memory is part of the contract.


**Flags:** NZCV unchanged.


**Example**

```asm
retry
        LDREX R1, [R0]
        ADD R1, R1, #1
        STREX R2, R1, [R0]
        CMP R2, #0
        BNE retry
```


**Expected result:** For an aligned writable counter at R0, retries until its increment succeeds.


**Watch for:** Interrupts and other events can invalidate the exclusive monitor. A single attempt is not guaranteed to succeed.


### Exception-frame

Read a Cortex-M3 exception’s saved context.


**Syntax**

```asm
TST LR, #4
ITE EQ
MRSEQ R0, MSP
MRSNE R0, PSP
```


**Operands and rules:** At handler entry LR is EXC_RETURN. Bit 2 chooses MSP (0) or PSP (1). The basic saved frame is R0,R1,R2,R3,R12,LR,PC,xPSR at offsets 0,4,8,12,16,20,24,28. Capture the frame before changing the relevant SP. An alignment padding word can follow the basic frame; stacked xPSR bit 9 records it.


**Flags:** TST updates flags. Returning through EXC_RETURN restores the saved context.


**Example**

```asm
        TST LR, #4
        ITE EQ
        MRSEQ R0, MSP
        MRSNE R0, PSP
        LDR R1, [R0, #24]
        LDRB R2, [R1, #-2]
```


**Expected result:** In an SVC handler at entry, R2 receives the SVC immediate from the instruction before the saved return PC.


**Watch for:** This is handler-only code, not a normal C-callable function. Keep one owner of each vector and save EXC_RETURN before a nested BL.


## ARMASM directives


### AREA

Select a named code/data section.


**Syntax**

```asm
AREA asm_functions, CODE, READONLY
AREA scratch, DATA, READWRITE, ALIGN=2
```


**Operands and rules:** Use CODE for instructions, DATA for objects. READONLY data belongs in non-writable storage; READWRITE allows modification. AREA ALIGN=n uses 2^n bytes.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
        AREA scratch, DATA, READWRITE, ALIGN=2
values  SPACE 16
```


**Expected result:** Defines 16 bytes of writable storage in a 4-byte-aligned section.


**Watch for:** AREA ALIGN=2 means four-byte section alignment, unlike the standalone ALIGN 2 directive.


### THUMB / CODE16

Select Thumb assembly for this target.


**Syntax**

```asm
THUMB
```


**Operands and rules:** Cortex-M3 executes Thumb/Thumb-2, not ARM state. THUMB selects Unified syntax; CODE16 selects legacy pre-UAL Thumb syntax with different implicit flag-setting rules. Use THUMB for these examples and the project’s Cortex-M3 CPU setting.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
        THUMB
```


**Expected result:** Subsequent instructions are assembled as Thumb code.


**Watch for:** ARM/CODE32 code is not supported by Cortex-M3.


### PRESERVE8 / REQUIRE8

Declare stack alignment attributes.


**Syntax**

```asm
PRESERVE8
REQUIRE8
```


**Operands and rules:** PRESERVE8 asserts that code preserves 8-byte stack alignment; REQUIRE8 declares a requirement for it. Neither inserts padding or repairs SP.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
        PRESERVE8
```


**Expected result:** Adds alignment metadata for the object/linker.


**Watch for:** You must still balance pushes, local storage, and padding yourself.


### EXPORT / GLOBAL / IMPORT / EXTERN

Expose a symbol or reference one defined elsewhere.


**Syntax**

```asm
EXPORT sum_words
IMPORT helper
```


**Operands and rules:** Names are case-sensitive and must agree with C declarations. GLOBAL is an EXPORT synonym; EXTERN is an IMPORT synonym. [WEAK] marks a weak import/export when used by startup code.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
        EXPORT sum_words
        IMPORT helper
```


**Expected result:** sum_words becomes available to other objects; helper must be resolved according to its import contract.


**Watch for:** EXPORT does not implement a function and IMPORT does not call one.


### PROC / ENDP / FUNCTION / ENDFUNC

Mark a function’s boundaries for assembler/debug metadata.


**Syntax**

```asm
sum_words PROC
        BX LR
        ENDP
```


**Operands and rules:** PROC pairs with ENDP; FUNCTION/ENDFUNC are synonyms. The label is the entry address.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
identity PROC
        BX LR
        ENDP
```


**Expected result:** Defines a callable identity routine when exported and linked.


**Watch for:** ENDP is not a return instruction; you still need BX LR or an appropriate POP.


### DCD / DCW / DCB / DCDU / DCWU

Define words, halfwords, or bytes in the current section.


**Syntax**

```asm
words DCD 10,20
halves DCW 1,2
text DCB "Hi",0
```


**Operands and rules:** DCD: 4-byte objects with word alignment; DCW: 2-byte objects with halfword alignment; DCB: bytes. U forms omit automatic alignment. A string needs an explicit zero if C expects a terminator.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
words   DCD 10,20
text    DCB "Hi",0
```


**Expected result:** words occupies 8 bytes; text contains 0x48,0x69,0x00.


**Watch for:** Data inside a code section must be skipped or placed after a return; the CPU must not execute it.


### SPACE / FILL

Reserve/fill bytes in a section.


**Syntax**

```asm
buffer SPACE 40
FILL 8, 0xFF, 1
```


**Operands and rules:** SPACE size is in bytes, not elements. FILL accepts byte count, value, and optional value size. Use a writable section for a mutable buffer. Runtime initialization depends on image loading/startup, particularly NOINIT sections.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
        AREA buffers, DATA, READWRITE
buffer  SPACE 40
```


**Expected result:** Reserves room for ten 32-bit words.


**Watch for:** SPACE 10 reserves ten bytes, not ten words.


### EQU / RN

Give a name to a constant or register.


**Syntax**

```asm
COUNT EQU 10
index RN 4
```


**Operands and rules:** EQU defines an assembly-time value. RN defines a register alias. These allocate no RAM and are not C variables.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
COUNT   EQU 10
index   RN 4
        MOV index, #COUNT
```


**Expected result:** Assembles a move of 10 into R4.


**Watch for:** Changing a register at runtime does not change an EQU constant.


### ALIGN

Pad to an alignment boundary.


**Syntax**

```asm
ALIGN 4
```


**Operands and rules:** Standalone ALIGN takes a power-of-two byte alignment; default is 4. An optional offset shifts the alignment boundary. AREA ALIGN=n instead uses a power-of-two exponent.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
bytes   DCB 1,2,3
        ALIGN 4
word    DCD 7
```


**Expected result:** Pads as necessary so word begins at a 4-byte boundary.


**Watch for:** ALIGN 4 means 4-byte alignment, not 16-byte alignment.


### LTORG

Emit the current literal pool here.


**Syntax**

```asm
LTORG
```


**Operands and rules:** Use when LDR =constant needs a nearby pool. Place pools after a return/unconditional branch so execution cannot fall into them. Literal-load range depends on the emitted instruction.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
        LDR R0, =0x12345678
        BX LR
        LTORG
```


**Expected result:** The assembler can place the constant near the load without executing it.


**Watch for:** END emits remaining literals, but a long function may need an earlier safe pool.


### END / ENTRY

End the assembly source or identify an image entry point.


**Syntax**

```asm
END
ENTRY
```


**Operands and rules:** END terminates the source; text after it is not assembled. ENTRY identifies an entry point for linking/debug use. Ordinary C-callable routines do not need their own reset entry.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
        END
```


**Expected result:** Finishes assembly of this source file.


**Watch for:** Do not replace startup_LPC17xx.s or add Reset_Handler to an ordinary C-callable solution.


### IF / ELSE / ELIF / ENDIF

Choose source at assembly time.


**Syntax**

```asm
IF :DEF:DEBUG
        NOP
ELSE
        NOP
ENDIF
```


**Operands and rules:** Conditions use assembler expressions; symbols must be known as required. ARMASM also has bracket aliases [ | ] for IF/ELSE/ENDIF.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
        IF :DEF:DEBUG
        NOP
        ENDIF
```


**Expected result:** Includes NOP only when DEBUG is defined.


**Watch for:** This does not test a register at runtime; use CMP and branches for runtime decisions.


### GET / INCLUDE

Include another assembly source file.


**Syntax**

```asm
GET constants.inc
```


**Operands and rules:** GET and INCLUDE are synonyms. Use a relative path resolvable by project include settings.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
        GET constants.inc
```


**Expected result:** Assembles the contents of constants.inc at this position.


**Watch for:** The included file must exist; C headers are not automatically valid ARMASM.


### MACRO / MEND / MEXIT

Define or exit an assembly-time macro.


**Syntax**

```asm
MACRO
$name INC $reg
        ADD $reg, $reg, #1
MEND
```


**Operands and rules:** A macro expands instructions inline. Parameters use $. MEND ends the definition; MEXIT leaves a macro expansion early.


**Flags:** Assembler directive: no instruction executes and no runtime flags change.


**Example**

```asm
        MACRO
$name   INC $reg
        ADD $reg, $reg, #1
        MEND
        INC R0
```


**Expected result:** Expands INC R0 to ADD R0,R0,#1.


**Watch for:** Macros do not have function-call register saving or a runtime return address.


## Essentials


### Syntax

Read an ARMASM line and distinguish names, values, addresses, and metadata.


**Syntax**

```asm
label   opcode operand1, operand2 ; comment
        MOV R0, #10
        LDR R1, =array
        LDR R2, [R1]
```


**Operands and rules:** Put labels in the label field (start of line) and indent instructions/directives. ; starts a comment. # introduces an immediate; 0x prefixes hex. Register names are not variables in RAM. Examples use Rd=destination, Rn/Rm=source registers. Optional syntax in manuals uses braces; do not type those braces except real register lists.


**Flags:** Check the particular instruction and encoding. In Unified syntax, explicitly request S when you need flags; .W/.N request wide/narrow encodings where supported. Not every narrow spelling or IT context has identical flag behavior.


**Example**

```asm
        CMP R0, #0
        IT NE
        ADDNE.W R1, R1, #1
```


**Expected result:** Increments R1 only if R0 is nonzero; ADDNE.W does not replace the comparison flags.


**Watch for:** A condition suffix (NE) and an S flag suffix are different. ADDSNE means flag-setting ADD under NE; .W controls encoding width, not word-sized data.


### Addressing

Choose the location to read/write and whether to advance a pointer.


**Syntax**

```asm
LDR R0, [R1, #4]
LDR R0, [R1, #4]!
LDR R0, [R1], #4
LDR R0, [R1, R2, LSL #2]
```


**Operands and rules:** Offset form leaves R1 unchanged. Pre-index ! adjusts R1 before access; post-index adjusts after access. A scaled register index is limited by the instruction encoding (common wide word load: LSL 0..3). Pre/post-index immediate forms use a different, smaller range than plain positive offset loads. Do not overlap destination/base with load writeback.


**Flags:** NZCV unchanged.


**Example**

```asm
        LDR R0, [R1], #4
```


**Expected result:** If R1 initially points to word 11, loads 11 and moves R1 to the next word.


**Watch for:** Array indexes count elements; memory offsets count bytes. int32_t index uses *4, int16_t *2, int8_t *1.


### Registers

Assign inputs, temporary values, and preserved values before writing the function.


**Syntax**

```asm
R0-R3  arguments / caller-saved
R4-R8, R10-R11  callee-saved
R9  platform role; preserve in this project
R12  caller-saved scratch
SP=R13  LR=R14  PC=R15
```


**Operands and rules:** For ordinary 32-bit integer/pointer arguments, the first four go to R0–R3. Return a 32-bit scalar in R0; a 64-bit integer in R1:R0 (low word R0). Wider arguments, doubleword alignment, and structure returns need the exact AAPCS contract; do not generalize the four-word recipe to every C type.


**Flags:** NZCV are caller-clobbered across public calls. Do not rely on a comparison surviving BL.


**Example**

```asm
        PUSH {R4,LR}
        MOV R4, R0
        BL helper
        ADD R0, R0, R4
        POP {R4,PC}
```


**Expected result:** Keeps the original input in preserved R4 while helper is allowed to overwrite R0–R3/R12.


**Watch for:** R12 is convenient for an entry-SP snapshot only while no call or linker veneer can clobber it.


### Flags

Choose branch conditions from the meaning of the numbers.


**Syntax**

```asm
CMP R0, R1
BLO unsigned_lower
; For signed comparison use BLT instead.
```


**Operands and rules:** N is result bit 31; Z means zero; C means carry/no borrow; V means signed overflow. After CMP use EQ/NE for equality, LO/HS/HI/LS for unsigned, LT/GE/GT/LE for signed. Arithmetic flags describe the truncated result, with C/V carrying different extra information.


**Flags:** The condition table below gives exact formulas. Check flags at the branch, not only at the earlier CMP.


**Example**

```asm
        LDR R0, =0xFFFFFFFF
        MOVS R1, #1
        CMP R0, R1
```


**Expected result:** Unsigned R0>R1, so BHI is true. Signed R0=-1<1, so BLT is also true. N=1 Z=0 C=1 V=0.


**Watch for:** BMI tests the sign bit of the result and is not a substitute for BLT after an overflowing subtraction.


### Standalone-startup

Keep a standalone assembly test separate from the C project.


**Syntax**

```asm
; Only in a separate assembly-only project with its own vector table:
Reset_Handler
        MOVS R0, #41
        BL plus_one
stop
        B stop
```


**Operands and rules:** An assembly-only image needs a valid initial SP, reset vector, linker layout, and its required data initialization. Follow the supplied standalone template. In the normal combined C project, startup enters the C runtime; callable examples must not replace it.


**Flags:** Startup and calls may change flags.


**Example**

```asm
        ; A stop loop for a standalone debugger test:
stop
        B stop
```


**Expected result:** Execution stays at stop for debugger inspection.


**Watch for:** Pasting a custom Reset_Handler into the combined project can bypass C runtime initialization.


## Exam patterns


### Function-template

Use a small exported routine in the existing C project.


**Syntax**

```asm
; C: extern unsigned int plus_one(unsigned int value);
```


**Operands and rules:** In a copied Official Combined Exam API project, edit Source/ASM_funct.s and declare/call the exact export in Source/sample.c. Keep the existing startup_LPC17xx.s. Replace a demo routine only when its old call sites are also adjusted.


**Flags:** This example updates NZCV; callers must not depend on flags surviving a function call.


**Example**

```asm
        AREA asm_functions, CODE, READONLY
        PRESERVE8
        THUMB
        EXPORT plus_one
plus_one PROC
        ADDS R0, R0, #1
        BX LR
        ENDP
        END
```


**Expected result:** plus_one(41) returns 42 in R0. It uses no callee-saved registers and makes no nested call.


**Watch for:** EXPORT name, function label, and C declaration must match exactly, including letter case.


### Array-loop

Sum a word array using a bounded pointer loop.


**Syntax**

```asm
; uint32_t sum_words(const uint32_t *values, uint32_t count);
```


**Operands and rules:** R0 points to count readable 4-byte words; R1 is an unsigned count. A zero count performs no memory access. The sum wraps modulo 2^32; add an explicit carry/overflow exit if the paper requires it.


**Flags:** The loop changes flags and uses BNE immediately after SUBS.


**Example**

```asm
sum_words PROC
        MOVS R2, #0
        CBZ R1, sum_done
sum_loop
        LDR R3, [R0], #4
        ADD R2, R2, R3
        SUBS R1, R1, #1
        BNE sum_loop
sum_done
        MOV R0, R2
        BX LR
        ENDP
```


**Expected result:** For [3,5,7] and count=3, returns 15. For count=0, returns 0.


**Watch for:** Check zero before a decrement-and-branch loop; otherwise count=0 can wrap to a very large value.


### If-else

Implement a signed selection with explicit branches.


**Syntax**

```asm
; int32_t max_signed(int32_t a, int32_t b);
```


**Operands and rules:** R0=a, R1=b. Use BGE for signed inputs; use BHS for unsigned inputs.


**Flags:** NZCV unchanged. CMP sets NZCV.


**Example**

```asm
max_signed PROC
        CMP R0, R1
        BGE max_done
        MOV R0, R1
max_done
        BX LR
        ENDP
```


**Expected result:** max_signed(-1,2) returns 2.


**Watch for:** Selecting an unsigned branch changes the meaning of negative bit patterns.


### Remainder

Compute quotient and remainder together.


**Syntax**

```asm
; R0=n, R1=d (unsigned, nonzero); R2=q, R0=remainder
```


**Operands and rules:** For signed arithmetic substitute SDIV and preserve the numerator; the signed remainder follows the numerator’s sign. Check zero divisors separately.


**Flags:** NZCV unchanged.


**Example**

```asm
        UDIV R2, R0, R1
        MLS R0, R2, R1, R0
```


**Expected result:** For n=47,d=10: R2=4 and R0=7.


**Watch for:** The quotient is not the remainder; keep the original numerator until MLS.


## Target boundaries


### ARM / CODE32 / LDC

Recognize examples that are deliberately unsupported on Cortex-M3.


**Syntax**

```asm
; Other targets only: ARM / CODE32
; Deliberate fault example: LDC p1, c0, [R1]
```


**Operands and rules:** ARM/CODE32 request ARM-state assembly, which this processor cannot execute. LDC accesses a coprocessor unavailable on LPC1768. The supplied exceptions lecture shows these concepts as fault demonstrations, not normal solution instructions.


**Flags:** No normal result is defined for these examples on this target; a fault path is expected.


**Example**

```asm
        ; For normal Cortex-M3 code use:
        THUMB
        LDR R0, [R1]
```


**Expected result:** With R1 pointing to a readable word, LDR performs a normal memory load. It is not a replacement implementation of a coprocessor operation.


**Watch for:** Do not copy the lecture’s deliberate fault experiments into an ordinary callable function.


## Condition codes

| Suffix | Test | Meaning |

|---|---|---|

| EQ | Z=1 | equal / zero |

| NE | Z=0 | not equal / nonzero |

| CS | C=1 | unsigned higher or same / no borrow |

| HS | C=1 | unsigned higher or same (alias of CS) |

| CC | C=0 | unsigned lower / borrow |

| LO | C=0 | unsigned lower (alias of CC) |

| HI | C=1 and Z=0 | unsigned higher |

| LS | C=0 or Z=1 | unsigned lower or same |

| GE | N=V | signed greater or equal |

| LT | N!=V | signed less than |

| GT | Z=0 and N=V | signed greater than |

| LE | Z=1 or N!=V | signed less or equal |

| MI | N=1 | negative result |

| PL | N=0 | nonnegative result |

| VS | V=1 | signed overflow |

| VC | V=0 | no signed overflow |


## Before you run

- Write the exact prototype: argument order, widths, signedness, pointers, and return contract.

- Match the C name, EXPORT, and assembly label; use the project-listed Source/ASM_funct.s.

- Distinguish a register value, an address, and memory at that address.

- Use byte/halfword/word access matching the object, and scale indexes by element size.

- Check every branch against signed or unsigned intent and the last instruction that set flags.

- Handle zero count before reading an array; check limits, output capacity, and divisor zero.

- Preserve modified callee-saved registers and incoming LR across nested calls.

- Keep SP word-aligned throughout and 8-byte aligned at public calls; restore it on every exit.

- Recalculate stack-argument offsets after all pushes, local storage, and padding.

- Confirm literal pools/data cannot be executed; keep writable objects out of read-only code.

- Use one handler definition per vector and retain the correct startup path.

- Trace zero, one element, negative inputs, maximum values, duplicates, and the required overflow behavior.


## Sources and target

Cortex-M3 only. Broader ARM-state and floating-point instructions are outside this target. External manuals require internet.

- [Arm Cortex-M3 instruction and exception reference](https://www.keil.com/dd/docs/datashts/arm/cortex_m3/r2p1/dui0552a_cortex_m3_dgug.pdf)

- [Keil ARMASM syntax and directives](https://www.keil.com/support/man/docs/armasm/default.htm)

- [Arm procedure call standard (AAPCS32)](https://github.com/ARM-software/abi-aa/blob/main/aapcs32/aapcs32.rst)
