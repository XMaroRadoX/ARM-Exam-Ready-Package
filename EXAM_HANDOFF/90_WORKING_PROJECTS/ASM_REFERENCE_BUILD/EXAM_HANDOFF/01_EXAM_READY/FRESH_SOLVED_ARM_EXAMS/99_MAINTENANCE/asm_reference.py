"""Single source for the offline ARMASM reference and Markdown glossary."""
from __future__ import annotations
import re

ENTRIES = []
def entry(names, category, purpose, syntax, rules, flags, example, result, mistake, aliases=''):
    names=names.split('|')
    ENTRIES.append(dict(id=names[0].lower(), names=names, category=category, purpose=purpose,
        syntax=syntax, rules=rules, flags=flags, example=example, result=result,
        mistake=mistake, aliases=aliases.split('|') if aliases else []))

UNCHANGED='NZCV unchanged.'
ARITH='The S form updates N/Z/C/V. The non-S form preserves them. C means carry for addition and no borrow for subtraction.'
LOGIC='The S form updates N/Z and the shifter carry C; V is unchanged. With an unshifted register operand C is preserved.'
REGS='Use R0–R12 for ordinary operands. SP/PC forms have extra restrictions; the syntax shown avoids them. Immediates must fit an instruction encoding; use LDR Rd,=constant for arbitrary 32-bit constants.'

entry('MOV|MOVS','Values','Copy a register or load an encodable constant.', 'MOV R0, R1\nMOVS R0, #7', REGS,
 'MOV preserves NZCV; MOVS updates N/Z, may update C for a modified immediate, and preserves V. A small immediate such as #7 preserves C.',
 '        MOVS R0, #7\n        MOV R1, R0', 'R0=7; R1=7. MOV copies the value, not memory at that address.', 'Do not assume every 32-bit constant fits MOV.', 'copy|constant|move value')
entry('MOVW|MOVT','Values','Build a 32-bit constant from two 16-bit pieces.', 'MOVW R0, #0x5678\nMOVT R0, #0x1234', 'Immediate range is 0..65535. MOVW clears the top half; MOVT preserves the bottom half. Use general registers, not SP/PC.', UNCHANGED,
 '        MOVW R0, #0x5678\n        MOVT R0, #0x1234', 'R0=0x12345678.', 'MOVT does not initialize the low 16 bits.')
entry('MVN|MVNS','Values','Invert every bit of the second operand.', 'MVN R0, R1', REGS, LOGIC,
 '        MOVS R1, #0\n        MVN R0, R1', 'R0=0xFFFFFFFF (unsigned maximum or signed -1).', 'Bitwise inversion is not arithmetic negation; use RSB from zero for -x.')
entry('ADR','Values','Compute the address of a nearby label in the same section.', 'ADR R0, local_data', 'PC-relative range depends on encoding; wide forms reach up to 4095 bytes. Label must be in the same area. Use LDR =label for a distant or external symbol.', UNCHANGED,
 '        ADR R0, local_data\n        B after_data\n        ALIGN 4\nlocal_data DCD 27\nafter_data', 'R0 points to local_data; no data has been loaded from it.', 'An address is not the value stored there.')
entry('LDR','Memory','Load a 32-bit word, or use the = pseudo-instruction to obtain a constant/address.', 'LDR R0, [R1]\nLDR R0, [R1, #4]\nLDR R0, [R1, R2, LSL #2]\nLDR R0, =0x12345678', 'Square brackets mean a memory access. =constant/=label is assembler syntax that may use a literal pool. Ordinary word data should be 4-byte aligned; access only valid memory. Immediate offsets depend on encoding (a common positive wide offset is 0..4095).', UNCHANGED,
 '        LDR R1, =values\n        LDR R0, [R1, #4]\n        B after_values\n        ALIGN 4\nvalues  DCD 11,22\nafter_values', 'R1 is the array address; R0=22.', 'LDR R0,=values gets the address; LDR R0,[R0] then reads the first word.', 'load|literal pool|pointer|address versus value|LDR=')
entry('LDRB|LDRH|LDRSB|LDRSH','Memory','Read a byte or halfword and extend it to a 32-bit register.', 'LDRB R0, [R1]\nLDRH R0, [R1]\nLDRSB R0, [R1]\nLDRSH R0, [R1]', 'B/SB reads 1 byte; H/SH reads 2 bytes. LDRB/LDRH zero-extend. LDRSB/LDRSH sign-extend. Use aligned halfwords; do not use PC as the destination.', UNCHANGED,
 '        LDR R1, =byte_data\n        LDRB R0, [R1]\n        LDRSB R2, [R1]\n        B after_byte\nbyte_data DCB 0xFE\n        ALIGN 2\nafter_byte', 'R0=254; R2=0xFFFFFFFE (-2).', 'An unsigned load destroys the intended sign of int8_t/int16_t data.', 'signed load|zero extension|sign extension|byte|halfword')
entry('STR|STRB|STRH','Memory','Write the low word, byte, or halfword of a register.', 'STR R0, [R1]\nSTRB R0, [R1]\nSTRH R0, [R1]', 'R1 must point to writable storage. STR writes 4 bytes; STRB writes the lowest 8 bits; STRH writes the lowest 16 bits. Use naturally aligned data.', UNCHANGED,
 '        MOVS R0, #0xAB\n        STRB R0, [R1]', 'With R1 pointing to writable byte storage, that byte becomes 0xAB. Neighboring bytes are unchanged.', 'A store has no signed/unsigned variant. STR can overwrite adjacent bytes if the object is only one byte.', 'store|write memory')
entry('LDRD|STRD','Memory','Transfer two 32-bit words using consecutive memory locations.', 'LDRD R0, R1, [R2]\nSTRD R0, R1, [R2, #8]', 'Address must be word-aligned even if unaligned ordinary loads are enabled. Registers must be distinct, neither SP nor PC. Immediate offset is a multiple of 4 from -1020 to +1020; avoid writeback overlap with a transferred register.', UNCHANGED,
 '        LDRD R0, R1, [R2]', 'If words at R2 and R2+4 are 10 and 20, R0=10 and R1=20.', 'These instructions always fault on an unaligned address.')
entry('LDM|LDMIA|LDMFD|LDMDB|STM|STMIA|STMDB|STMFD','Memory','Load or store a register list from consecutive word addresses.', 'STMIA R0!, {R1-R3}\nLDMIA R0!, {R1-R3}\nSTMFD SP!, {R4,LR}\nLDMFD SP!, {R4,PC}', 'IA increments after each word; DB decrements before the block. ! writes back the base. Registers transfer in increasing register-number order. Keep base out of a writeback list and addresses word-aligned. Cortex-M3 supports IA/DB, not every ARM-state addressing mode. Multi-register wide forms need at least two registers; PUSH/POP provide useful single-register forms.', UNCHANGED,
 '        STMFD SP!, {R4,LR}\n        MOVS R4, #9\n        LDMFD SP!, {R4,PC}', 'Saves 8 bytes, uses R4, then restores R4 and returns. STMFD=STMDB; LDMFD=LDMIA for a full descending stack.', 'The order written inside braces does not change memory order.', 'multiple registers|full descending|STMFD|LDMFD')
entry('ADD|ADDS|ADDW','Arithmetic','Add operands; keep the low 32 bits.', 'ADD R0, R1, R2\nADDS R0, R1, R2\nADDW R0, R1, #1000', REGS+' ADDW uses an unsigned 12-bit immediate (0..4095) and does not set flags.', ARITH,
 '        LDR R1, =0xFFFFFFFF\n        ADDS R0, R1, #1', 'R0=0; N=0 Z=1 C=1 V=0.', 'Carry signals unsigned overflow; V signals signed overflow.', 'addition|unsigned overflow|carry')
entry('SUB|SUBS|SUBW','Arithmetic','Subtract the second operand from the first.', 'SUB R0, R1, R2\nSUBS R0, R1, #1\nSUBW R0, R1, #1000', REGS+' SUBW uses an unsigned 12-bit immediate (0..4095), with no flag update.', ARITH,
 '        MOVS R1, #0\n        SUBS R0, R1, #1', 'R0=0xFFFFFFFF; N=1 Z=0 C=0 V=0.', 'C=0 means a borrow was needed. Do not treat C as a borrow flag.', 'subtract|borrow')
entry('ADC|ADCS|SBC|SBCS','Arithmetic','Carry or borrow between words of a wide integer.', 'ADCS R0, R0, R2\nSBCS R0, R0, R2', 'ADC computes Rn+operand+C. SBC computes Rn-operand-(1-C). Establish C with the low-word ADDS/SUBS immediately before processing the high word.', ARITH,
 '        LDR R0, =0xFFFFFFFF\n        MOVS R1, #0\n        MOVS R2, #1\n        MOVS R3, #0\n        ADDS R0, R0, R2\n        ADC R1, R1, R3', 'R1:R0 becomes 0x00000001:00000000.', 'An unrelated flag-setting instruction between words breaks the carry chain.', '64 bit addition|multiword')
entry('RSB|RSBS|NEG|NEGS','Arithmetic','Reverse subtraction; subtract a value from zero to negate it.', 'RSB R0, R1, #0\nRSBS R0, R1, #0', 'For the shown negation form, R0=0-R1. NEG/NEGS are aliases for reverse subtraction from zero. Wide RSB also accepts a register or shifted-register second operand, computing Operand2-Rn.', ARITH,
 '        MOVS R1, #7\n        RSBS R0, R1, #0', 'R0=0xFFFFFFF9 (-7).', 'Negating signed INT_MIN overflows; the result still has bit 31 set.')
entry('MUL|MULS','Arithmetic','Multiply and keep the low 32 bits.', 'MUL R0, R1, R2\nMULS R0, R1, R0', 'No immediate operands. MULS uses the narrow low-register form with the destination also an input. Use ordinary registers for MUL.', 'MUL preserves NZCV; MULS updates N/Z only, preserving C/V.',
 '        MOVS R1, #6\n        MOVS R2, #7\n        MUL R0, R1, R2', 'R0=42.', 'MUL does not report multiplication overflow through C or V.')
entry('MLA|MLS','Arithmetic','Multiply and add, or subtract a product.', 'MLA R0, R1, R2, R3\nMLS R0, R1, R2, R3', 'Register operands only, no SP/PC. MLA=R1*R2+R3; MLS=R3-R1*R2. Result is truncated to 32 bits.', UNCHANGED,
 '        MOVS R1, #4\n        MOVS R2, #10\n        MOVS R3, #47\n        MLS R0, R1, R2, R3', 'R0=47-4*10=7.', 'The last operand in MLS is the value from which the product is subtracted.', 'remainder|modulo')
entry('UMULL|SMULL|UMLAL|SMLAL','Arithmetic','Produce or accumulate a full 64-bit product.', 'UMULL R0, R1, R2, R3\nSMULL R0, R1, R2, R3\nUMLAL R0, R1, R2, R3', 'Destination order is low, high. Destinations must differ; no SP/PC. U means unsigned, S means signed. MLAL adds the product to the existing destination pair; initialize both words first.', UNCHANGED,
 '        LDR R2, =0xFFFFFFFF\n        MOVS R3, #2\n        UMULL R0, R1, R2, R3', 'Unsigned result R1:R0=0x00000001:FFFFFFFE. SMULL with the same inputs gives 0xFFFFFFFF:FFFFFFFE (-2).', 'SMULL is signed multiply-long, not MUL with an S flag suffix.', '64 bit multiplication|wide product')
entry('UDIV|SDIV','Arithmetic','Divide integers and return the quotient.', 'UDIV R0, R1, R2\nSDIV R0, R1, R2', 'Register divisor only; no SP/PC. UDIV is unsigned. SDIV rounds toward zero. Check divisor is nonzero: divide-by-zero may fault when trapping is enabled, otherwise returns zero. INT_MIN/-1 cannot fit a signed 32-bit result.', UNCHANGED,
 '        MOVS R1, #47\n        MOVS R2, #10\n        UDIV R0, R1, R2\n        MLS R3, R0, R2, R1', 'R0=4; R3=7 (remainder).', 'No general MOD instruction exists here; calculate n-q*d.', 'division|quotient|remainder|modulus')
entry('CMP|CMN','Compare and branch','Update flags from subtraction or addition without storing the result.', 'CMP R0, R1\nCMP R0, #10\nCMN R0, #1', REGS+' CMP computes R0-operand; CMN computes R0+operand.', 'Always updates N/Z/C/V.',
 '        MOVS R0, #5\n        CMP R0, #7', 'R0 remains 5; N=1 Z=0 C=0 V=0.', 'Branch before another instruction replaces the flags you intended to test.', 'compare|comparison|negative constant')
entry('TST|TEQ','Compare and branch','Test bits with AND or compare bit patterns with XOR, discarding the result.', 'TST R0, #8\nTEQ R0, R1', REGS, 'Updates N/Z and shifter carry C; V unchanged. An unshifted register operand preserves C.',
 '        MOVS R0, #8\n        TST R0, #8', 'Z=0 because bit 3 is set. R0 stays 8.', 'For TST, BEQ means none of the tested bits were set.', 'bit test|mask test')
entry('B','Compare and branch','Jump to a label without saving a return address.', 'B loop', 'Target must be reachable; wide B has a larger range than narrow B. Branch to Thumb code, not a data table.', UNCHANGED,
 '        B done\n        MOVS R0, #99\ndone', 'The MOVS is skipped; R0 is unchanged.', 'B does not create a return address. Use BL for a normal function call.', 'jump|goto')

CONDITIONS=[('EQ','Z=1','equal / zero','5,5'),('NE','Z=0','not equal / nonzero','5,7'),
 ('CS','C=1','unsigned higher or same / no borrow','7,5'),('HS','C=1','unsigned higher or same (alias of CS)','7,5'),
 ('CC','C=0','unsigned lower / borrow','5,7'),('LO','C=0','unsigned lower (alias of CC)','5,7'),
 ('HI','C=1 and Z=0','unsigned higher','7,5'),('LS','C=0 or Z=1','unsigned lower or same','5,7'),
 ('GE','N=V','signed greater or equal','7,5'),('LT','N!=V','signed less than','5,7'),
 ('GT','Z=0 and N=V','signed greater than','7,5'),('LE','Z=1 or N!=V','signed less or equal','5,7'),
 ('MI','N=1','negative result','5,7'),('PL','N=0','nonnegative result','7,5'),
 ('VS','V=1','signed overflow',None),('VC','V=0','no signed overflow','7,5')]
for condition,test,meaning,values in CONDITIONS:
    setup=('        LDR R0, =0x7FFFFFFF\n        ADDS R0, R0, #1' if values is None else
           '        MOVS R0, #'+values.split(',')[0]+'\n        CMP R0, #'+values.split(',')[1])
    entry('B'+condition,'Compare and branch','Branch when '+meaning+'.','B'+condition+' matched',
      'Tests '+test+'. Use after the relevant CMP or flag-setting arithmetic; conditional branch range is shorter than unconditional B.',UNCHANGED,
      setup+'\n        B'+condition+' matched\n        MOVS R2, #0\n        B finished\nmatched\n        MOVS R2, #1\nfinished',
      'The condition is true here, so R2=1.',
      'MI/PL alone are not signed less/greater comparisons after subtraction. Use LT/GE/GT/LE; use LO/HS/HI/LS for unsigned values.',
      condition+'|'+meaning)
entry('CBZ|CBNZ','Compare and branch','Branch directly when a low register is zero or nonzero.', 'CBZ R0, empty\nCBNZ R0, nonempty', 'R0–R7 only; forward-only target, 0..126 bytes from the architectural PC, even offset. No IT block. Use CMP/Bxx for backward loops or more distant targets.', UNCHANGED,
 '        MOVS R0, #0\n        CBZ R0, empty\n        MOVS R1, #99\nempty', 'The MOVS R1 is skipped.', 'CBNZ cannot directly branch backward to the top of a loop.', 'zero branch')
entry('IT|ITT|ITE|ITTT|ITTE|ITET|ITEE|ITTTT|ITTTE|ITTET|ITTEE|ITETT|ITETE|ITEET|ITEEE','Compare and branch','Condition up to four following Thumb instructions.', 'CMP R0, #0\nITE EQ\nMOVEQ R1, #1\nMOVNE R1, #0', 'T uses the first condition; E uses its inverse. Following instruction suffixes must match the block. Do not nest IT. A branch or PC write can occur only in the final slot. Prefer ordinary branches if a block becomes hard to follow.', UNCHANGED+' Instructions inside the block may alter flags if explicitly requested; this can affect later slots.',
 '        CMP R0, #0\n        ITE EQ\n        MOVEQ R1, #1\n        MOVNE R1, #0', 'R1=1 if R0 was zero, otherwise R1=0.', 'Conditional non-branch instructions need an IT context; do not rely on assembler auto-IT settings.', 'conditional execution|MOVEQ|ADDNE')
entry('AND|ANDS|ORR|ORRS|EOR|EORS|BIC|BICS|ORN|ORNS','Bits and shifts','Keep, set, toggle, or clear selected bits.', 'AND R0, R1, R2\nORR R0, R1, #8\nEOR R0, R1, #8\nBIC R0, R1, #8\nORN R0, R1, R2', REGS+' AND=a&b; ORR=a|b; EOR=a^b; BIC=a&~b; ORN=a|~b.', LOGIC,
 '        MOVS R0, #15\n        BIC R0, R0, #8\n        EOR R0, R0, #1', 'R0 goes from 15 to 7 to 6.', 'Use a mask (1<<bit), not the bit number itself.', 'mask|bitwise|set bit|clear bit|toggle bit')
entry('LSL|LSLS|LSR|LSRS|ASR|ASRS','Bits and shifts','Shift left, shift right with zeros, or shift right preserving the sign.', 'LSL R0, R1, #2\nLSR R0, R1, #1\nASR R0, R1, #1', 'Immediate LSL is 0..31; LSR/ASR are 1..32. Register shifts use the low 8 bits of the count and have defined special behavior at/above 32; do not assume count modulo 32. Use ordinary registers.', 'S forms update N/Z and C (last bit shifted out); V unchanged. A zero register shift preserves C.',
 '        LDR R1, =0xFFFFFFFC\n        LSR R0, R1, #1\n        ASR R2, R1, #1', 'R0=0x7FFFFFFE; R2=0xFFFFFFFE (-2).', 'ASR rounds negative values downward; SDIV rounds toward zero. They differ for negative odd values.', 'multiply by 4|signed right shift|array offset')
entry('ROR|RORS|RRX|RRXS','Bits and shifts','Rotate bits, optionally through carry.', 'ROR R0, R1, #8\nRRX R0, R1', 'Immediate ROR is 1..31. RRX rotates one bit through C: old C enters bit 31; old bit 0 is the carry output if flags are updated. Use ordinary registers.', 'S forms update N/Z/C; V unchanged. Non-S RRX reads C but preserves flags.',
 '        LDR R1, =0x12345678\n        ROR R0, R1, #8', 'R0=0x78123456.', 'ROR preserves rotated bits; LSR discards them.', 'rotate|carry rotate')
entry('SXTB|SXTH|UXTB|UXTH','Bits and shifts','Extend the low byte/halfword already in a register.', 'SXTB R0, R1\nSXTH R0, R1\nUXTB R0, R1\nUXTH R0, R1', 'S variants sign-extend; U variants zero-extend. No memory access. Optional source rotation supports 0,8,16,24 bits in wide forms.', UNCHANGED,
 '        MOVS R1, #0xFE\n        SXTB R0, R1\n        UXTB R2, R1', 'R0=-2; R2=254.', 'SXTB reads a register; LDRSB reads memory.', 'extension|cast')
entry('REV|REV16|REVSH|RBIT|CLZ','Bits and shifts','Reorder bits/bytes or count leading zero bits.', 'REV R0, R1\nREV16 R0, R1\nREVSH R0, R1\nRBIT R0, R1\nCLZ R0, R1', 'REV reverses four bytes; REV16 reverses bytes within each halfword; REVSH reverses the low halfword then sign-extends; RBIT reverses all 32 bits. CLZ(0)=32. No SP/PC.', UNCHANGED,
 '        LDR R1, =0x12345678\n        REV R0, R1\n        MOVS R2, #16\n        CLZ R3, R2', 'R0=0x78563412; R3=27.', 'REV does not reverse bit order; use RBIT.', 'byte order|endianness|leading zeros')
entry('UBFX|SBFX|BFI|BFC','Bits and shifts','Extract, insert, or clear a contiguous bit field.', 'UBFX R0, R1, #4, #3\nSBFX R0, R1, #4, #3\nBFI R0, R1, #4, #3\nBFC R0, #4, #3', 'lsb=0..31; width=1..(32-lsb). UBFX zero-extends; SBFX sign-extends. BFI copies the source low width bits into the destination field; BFC clears that field.', UNCHANGED,
 '        MOVS R1, #0x70\n        UBFX R0, R1, #4, #3\n        SBFX R2, R1, #4, #3', 'R0=7; R2=0xFFFFFFFF (-1).', 'The last operand is field width, not the highest bit number.', 'packed bits|bitfield')
entry('SSAT|USAT','Bits and shifts','Clamp an integer to a signed or unsigned range.', 'SSAT R0, #8, R1\nUSAT R0, #8, R1', 'SSAT width 1..32; USAT width 0..31. Input is interpreted as a signed 32-bit value. SSAT #8 clamps to -128..127; USAT #8 clamps to 0..255. Optional LSL/ASR can precede saturation.', 'NZCV unchanged; Q is set if saturation occurs and remains sticky until explicitly cleared.',
 '        MOVW R1, #300\n        USAT R0, #8, R1', 'R0=255; Q=1.', 'UXTB truncates; USAT clamps. They are not interchangeable.', 'clamp|saturation')
entry('BL|BLX','Calls and stack','Call a function and save a return address in LR.', 'BL helper\nBLX R3', 'BL uses a label. Cortex-M3 BLX supports the register form; the function pointer must have bit 0 set for Thumb. Save your incoming LR if you will return after another call.', UNCHANGED+' The called routine may change NZCV and caller-saved registers.',
 '        PUSH {R4,LR}\n        BL helper\n        POP {R4,PC}\nhelper\n        ADDS R0, R0, #1\n        BX LR', 'Returns the original R0 plus 1, with the caller’s R4 restored and SP balanced.', 'BL overwrites LR, and the callee may overwrite R0–R3/R12. Save live values.', 'call|nested call|link register')
entry('BX','Calls and stack','Branch to a register, usually returning with BX LR.', 'BX LR', 'For normal calls the target must have bit 0 set (Thumb). In an exception handler, LR can instead hold EXC_RETURN; that uses the hardware exception-return mechanism.', UNCHANGED,
 '        MOVS R0, #42\n        BX LR', 'Returns 42 to a normal caller.', 'A nested BL destroys the original LR unless you saved it.', 'return|function return')
entry('PUSH|POP','Calls and stack','Save/restore registers on the descending stack.', 'PUSH {R4-R6,LR}\nPOP {R4-R6,PC}', 'PUSH decrements SP; POP increments SP. Registers transfer in numerical order, 4 bytes each. POP {PC} returns via the saved LR slot. Keep stack word-aligned at all times and 8-byte aligned at public calls. Do not put SP in the list.', UNCHANGED,
 '        PUSH {R4,LR}\n        MOVS R4, #3\n        MOV R0, R4\n        POP {R4,PC}', 'Returns 3; restores the caller’s R4 and the original SP.', 'PUSH {R4-R7,LR} consumes 20 bytes; add 4 bytes of padding before calling another public function.', 'save registers|restore registers|stack frame')
entry('MRS|MSR','Exceptions and system','Read or write a special register.', 'MRS R0, APSR\nMRS R1, MSP\nMSR APSR_nzcvq, R0\nMSR PRIMASK, R1', 'Available registers depend on privilege and access direction. APSR exposes status flags; MSP/PSP are stack pointers; PRIMASK/BASEPRI/FAULTMASK affect exception masking. CONTROL changes execution control. Use ISB after a CONTROL change.', 'MRS preserves flags. MSR APSR_nzcvq writes N/Z/C/V/Q; other special-register writes do not directly change NZCV.',
 '        MRS R0, APSR', 'R0 holds a status snapshot; NZCV occupy bits 31..28.', 'Cortex-M3 uses APSR/xPSR and special registers, not the ARM-state CPSR/SPSR programming model.', 'status register|flags register|MSP|PSP|PRIMASK')
entry('CPSID|CPSIE','Exceptions and system','Mask or unmask configurable interrupts using PRIMASK.', 'CPSID i\nCPSIE i', 'Privileged use. i changes PRIMASK. Masking does not disable NMI or HardFault. In reusable code, save and restore the previous mask instead of blindly enabling interrupts.', UNCHANGED,
 '        MRS R0, PRIMASK\n        CPSID i\n        ; short critical section, keep R0 intact\n        MSR PRIMASK, R0', 'Restores exactly the previous interrupt mask.', 'CPSIE i may enable interrupts that your caller intentionally disabled.', 'interrupt disable|critical section')
entry('SVC','Exceptions and system','Request a supervisor-call exception.', 'SVC #7', 'Immediate is 0..255. The installed SVC_Handler must implement the intended service. Normal C function-call argument rules alone do not define an SVC service.', 'NZCV are saved in the exception frame and restored on return unless the frame is deliberately changed.',
 '        SVC #7', 'Requests service number 7; the result depends on SVC_Handler.', 'Use the stacked return PC minus 2 to locate the SVC instruction; the immediate is its low byte.', 'supervisor call|exception')
entry('DMB|DSB|ISB','Exceptions and system','Order memory accesses, wait for completion, or refresh the instruction pipeline.', 'DMB\nDSB\nISB', 'Use the full-system form shown. DMB orders explicit memory accesses; DSB also waits for required completion; ISB makes following instructions observe updated execution context. These are not delays.', UNCHANGED,
 '        DSB\n        ISB', 'Required prior work completes; subsequent instructions use the updated execution context.', 'A memory barrier does not replace interrupt masking or an atomic update.', 'barrier|memory ordering')
entry('WFI|WFE|SEV|NOP|YIELD','Exceptions and system','Wait for an interrupt/event, signal an event, or issue an execution hint.', 'WFI\nWFE\nSEV\nNOP\nYIELD', 'WFI waits for a qualifying wake event; WFE uses the event mechanism and may return immediately if an event is pending. SEV signals an event. NOP has no data effect. YIELD is a scheduling hint. Wakeup is not a guarantee that a particular handler ran.', UNCHANGED,
 '        NOP', 'No register or memory result changes.', 'Do not use instruction counts as a reliable time delay; use a timer.', 'sleep|idle|wait')
entry('BKPT|UDF','Exceptions and system','Stop under a debugger or deliberately execute an undefined instruction.', 'BKPT #0\nUDF #0', 'BKPT immediate 0..255. UDF has narrow/wide immediate encodings. These are debugging/fault paths, not normal returns; behavior depends on debugger and fault configuration.', 'No ordinary computed NZCV result; exception/debug entry may follow.',
 '        BKPT #0', 'Debugger stops here when configured to handle the breakpoint.', 'BKPT without an attached debugger can cause a fault.', 'breakpoint|undefined instruction')
entry('LDREX|LDREXB|LDREXH|STREX|STREXB|STREXH|CLREX','Exceptions and system','Use an exclusive monitor to attempt an atomic memory update.', 'LDREX R1, [R0]\nSTREX R2, R1, [R0]\nCLREX', 'Pair load/store widths and addresses; align to transfer size. STREX status must not overlap source/base. Use supported normal memory, not arbitrary device registers. STREX returns 0 on success, 1 on failure; retry as required. Add barriers when ordering other memory is part of the contract.', UNCHANGED,
 'retry\n        LDREX R1, [R0]\n        ADD R1, R1, #1\n        STREX R2, R1, [R0]\n        CMP R2, #0\n        BNE retry', 'For an aligned writable counter at R0, retries until its increment succeeds.', 'Interrupts and other events can invalidate the exclusive monitor. A single attempt is not guaranteed to succeed.', 'atomic|exclusive access')

DIRECTIVE_FLAGS='Assembler directive: no instruction executes and no runtime flags change.'
def directive(names,purpose,syntax,rules,example,result,mistake,aliases=''):
    entry(names,'ARMASM directives',purpose,syntax,rules,DIRECTIVE_FLAGS,example,result,mistake,aliases)
directive('AREA','Select a named code/data section.','AREA asm_functions, CODE, READONLY\nAREA scratch, DATA, READWRITE, ALIGN=2',
 'Use CODE for instructions, DATA for objects. READONLY data belongs in non-writable storage; READWRITE allows modification. AREA ALIGN=n uses 2^n bytes.',
 '        AREA scratch, DATA, READWRITE, ALIGN=2\nvalues  SPACE 16', 'Defines 16 bytes of writable storage in a 4-byte-aligned section.', 'AREA ALIGN=2 means four-byte section alignment, unlike the standalone ALIGN 2 directive.')
directive('THUMB|CODE16','Select Thumb assembly for this target.','THUMB','Cortex-M3 executes Thumb/Thumb-2, not ARM state. THUMB selects Unified syntax; CODE16 selects legacy pre-UAL Thumb syntax with different implicit flag-setting rules. Use THUMB for these examples and the project’s Cortex-M3 CPU setting.',
 '        THUMB', 'Subsequent instructions are assembled as Thumb code.', 'ARM/CODE32 code is not supported by Cortex-M3.')
directive('PRESERVE8|REQUIRE8','Declare stack alignment attributes.','PRESERVE8\nREQUIRE8','PRESERVE8 asserts that code preserves 8-byte stack alignment; REQUIRE8 declares a requirement for it. Neither inserts padding or repairs SP.',
 '        PRESERVE8', 'Adds alignment metadata for the object/linker.', 'You must still balance pushes, local storage, and padding yourself.')
directive('EXPORT|GLOBAL|IMPORT|EXTERN','Expose a symbol or reference one defined elsewhere.','EXPORT sum_words\nIMPORT helper','Names are case-sensitive and must agree with C declarations. GLOBAL is an EXPORT synonym; EXTERN is an IMPORT synonym. [WEAK] marks a weak import/export when used by startup code.',
 '        EXPORT sum_words\n        IMPORT helper', 'sum_words becomes available to other objects; helper must be resolved according to its import contract.', 'EXPORT does not implement a function and IMPORT does not call one.')
directive('PROC|ENDP|FUNCTION|ENDFUNC','Mark a function’s boundaries for assembler/debug metadata.','sum_words PROC\n        BX LR\n        ENDP','PROC pairs with ENDP; FUNCTION/ENDFUNC are synonyms. The label is the entry address.',
 'identity PROC\n        BX LR\n        ENDP', 'Defines a callable identity routine when exported and linked.', 'ENDP is not a return instruction; you still need BX LR or an appropriate POP.')
directive('DCD|DCW|DCB|DCDU|DCWU','Define words, halfwords, or bytes in the current section.','words DCD 10,20\nhalves DCW 1,2\ntext DCB "Hi",0','DCD: 4-byte objects with word alignment; DCW: 2-byte objects with halfword alignment; DCB: bytes. U forms omit automatic alignment. A string needs an explicit zero if C expects a terminator.',
 'words   DCD 10,20\ntext    DCB "Hi",0', 'words occupies 8 bytes; text contains 0x48,0x69,0x00.', 'Data inside a code section must be skipped or placed after a return; the CPU must not execute it.')
directive('SPACE|FILL','Reserve/fill bytes in a section.','buffer SPACE 40\nFILL 8, 0xFF, 1','SPACE size is in bytes, not elements. FILL accepts byte count, value, and optional value size. Use a writable section for a mutable buffer. Runtime initialization depends on image loading/startup, particularly NOINIT sections.',
 '        AREA buffers, DATA, READWRITE\nbuffer  SPACE 40', 'Reserves room for ten 32-bit words.', 'SPACE 10 reserves ten bytes, not ten words.')
directive('EQU|RN','Give a name to a constant or register.','COUNT EQU 10\nindex RN 4','EQU defines an assembly-time value. RN defines a register alias. These allocate no RAM and are not C variables.',
 'COUNT   EQU 10\nindex   RN 4\n        MOV index, #COUNT', 'Assembles a move of 10 into R4.', 'Changing a register at runtime does not change an EQU constant.')
directive('ALIGN','Pad to an alignment boundary.','ALIGN 4','Standalone ALIGN takes a power-of-two byte alignment; default is 4. An optional offset shifts the alignment boundary. AREA ALIGN=n instead uses a power-of-two exponent.',
 'bytes   DCB 1,2,3\n        ALIGN 4\nword    DCD 7', 'Pads as necessary so word begins at a 4-byte boundary.', 'ALIGN 4 means 4-byte alignment, not 16-byte alignment.')
directive('LTORG','Emit the current literal pool here.','LTORG','Use when LDR =constant needs a nearby pool. Place pools after a return/unconditional branch so execution cannot fall into them. Literal-load range depends on the emitted instruction.',
 '        LDR R0, =0x12345678\n        BX LR\n        LTORG', 'The assembler can place the constant near the load without executing it.', 'END emits remaining literals, but a long function may need an earlier safe pool.')
directive('END|ENTRY','End the assembly source or identify an image entry point.','END\nENTRY','END terminates the source; text after it is not assembled. ENTRY identifies an entry point for linking/debug use. Ordinary C-callable routines do not need their own reset entry.',
 '        END', 'Finishes assembly of this source file.', 'Do not replace startup_LPC17xx.s or add Reset_Handler to an ordinary C-callable solution.')
directive('IF|ELSE|ELIF|ENDIF','Choose source at assembly time.','IF :DEF:DEBUG\n        NOP\nELSE\n        NOP\nENDIF','Conditions use assembler expressions; symbols must be known as required. ARMASM also has bracket aliases [ | ] for IF/ELSE/ENDIF.',
 '        IF :DEF:DEBUG\n        NOP\n        ENDIF', 'Includes NOP only when DEBUG is defined.', 'This does not test a register at runtime; use CMP and branches for runtime decisions.')
directive('GET|INCLUDE','Include another assembly source file.','GET constants.inc','GET and INCLUDE are synonyms. Use a relative path resolvable by project include settings.',
 '        GET constants.inc', 'Assembles the contents of constants.inc at this position.', 'The included file must exist; C headers are not automatically valid ARMASM.')
directive('MACRO|MEND|MEXIT','Define or exit an assembly-time macro.','MACRO\n$name INC $reg\n        ADD $reg, $reg, #1\nMEND','A macro expands instructions inline. Parameters use $. MEND ends the definition; MEXIT leaves a macro expansion early.',
 '        MACRO\n$name   INC $reg\n        ADD $reg, $reg, #1\n        MEND\n        INC R0', 'Expands INC R0 to ADD R0,R0,#1.', 'Macros do not have function-call register saving or a runtime return address.')

# Long-form lookup sections share the same visible fields and Markdown source.
entry('Syntax','Essentials','Read an ARMASM line and distinguish names, values, addresses, and metadata.',
 'label   opcode operand1, operand2 ; comment\n        MOV R0, #10\n        LDR R1, =array\n        LDR R2, [R1]',
 'Put labels in the label field (start of line) and indent instructions/directives. ; starts a comment. # introduces an immediate; 0x prefixes hex. Register names are not variables in RAM. Examples use Rd=destination, Rn/Rm=source registers. Optional syntax in manuals uses braces; do not type those braces except real register lists.',
 'Check the particular instruction and encoding. In Unified syntax, explicitly request S when you need flags; .W/.N request wide/narrow encodings where supported. Not every narrow spelling or IT context has identical flag behavior.',
 '        CMP R0, #0\n        IT NE\n        ADDNE.W R1, R1, #1', 'Increments R1 only if R0 is nonzero; ADDNE.W does not replace the comparison flags.',
 'A condition suffix (NE) and an S flag suffix are different. ADDSNE means flag-setting ADD under NE; .W controls encoding width, not word-sized data.',
 'mnemonic|operand|label|comment|.W|.N|suffix|constant')
entry('Addressing','Essentials','Choose the location to read/write and whether to advance a pointer.',
 'LDR R0, [R1, #4]\nLDR R0, [R1, #4]!\nLDR R0, [R1], #4\nLDR R0, [R1, R2, LSL #2]',
 'Offset form leaves R1 unchanged. Pre-index ! adjusts R1 before access; post-index adjusts after access. A scaled register index is limited by the instruction encoding (common wide word load: LSL 0..3). Pre/post-index immediate forms use a different, smaller range than plain positive offset loads. Do not overlap destination/base with load writeback.',
 UNCHANGED,
 '        LDR R0, [R1], #4', 'If R1 initially points to word 11, loads 11 and moves R1 to the next word.',
 'Array indexes count elements; memory offsets count bytes. int32_t index uses *4, int16_t *2, int8_t *1.',
 'pre index|post index|writeback|pointer increment|array')
entry('Registers','Essentials','Assign inputs, temporary values, and preserved values before writing the function.',
 'R0-R3  arguments / caller-saved\nR4-R8, R10-R11  callee-saved\nR9  platform role; preserve in this project\nR12  caller-saved scratch\nSP=R13  LR=R14  PC=R15',
 'For ordinary 32-bit integer/pointer arguments, the first four go to R0–R3. Return a 32-bit scalar in R0; a 64-bit integer in R1:R0 (low word R0). Wider arguments, doubleword alignment, and structure returns need the exact AAPCS contract; do not generalize the four-word recipe to every C type.',
 'NZCV are caller-clobbered across public calls. Do not rely on a comparison surviving BL.',
 '        PUSH {R4,LR}\n        MOV R4, R0\n        BL helper\n        ADD R0, R0, R4\n        POP {R4,PC}', 'Keeps the original input in preserved R4 while helper is allowed to overwrite R0–R3/R12.',
 'R12 is convenient for an entry-SP snapshot only while no call or linker veneer can clobber it.',
 'AAPCS|ABI|callee saved|caller saved|return value|register ownership')
entry('Flags','Essentials','Choose branch conditions from the meaning of the numbers.',
 'CMP R0, R1\nBLO unsigned_lower\n; For signed comparison use BLT instead.',
 'N is result bit 31; Z means zero; C means carry/no borrow; V means signed overflow. After CMP use EQ/NE for equality, LO/HS/HI/LS for unsigned, LT/GE/GT/LE for signed. Arithmetic flags describe the truncated result, with C/V carrying different extra information.',
 'The condition table below gives exact formulas. Check flags at the branch, not only at the earlier CMP.',
 '        LDR R0, =0xFFFFFFFF\n        MOVS R1, #1\n        CMP R0, R1', 'Unsigned R0>R1, so BHI is true. Signed R0=-1<1, so BLT is also true. N=1 Z=0 C=1 V=0.',
 'BMI tests the sign bit of the result and is not a substitute for BLT after an overflowing subtraction.',
 'signed versus unsigned|condition codes|overflow|NZCV')
entry('Fifth-argument','Calls and stack','Locate stack arguments after saving registers.',
 '; uint32_t fifth(uint32_t a,uint32_t b,uint32_t c,uint32_t d,uint32_t e);\nfifth PROC\n        PUSH {R4,LR}\n        LDR R0, [SP, #8]\n        POP {R4,PC}\n        ENDP',
 'For five 32-bit arguments, a..d use R0..R3; e is at entry SP. After this 8-byte push, e is at current SP+8. Include every push and local/padding allocation when calculating an offset. The caller puts the first stacked argument at its current SP, with any padding after the arguments.',
 UNCHANGED,
 'fifth PROC\n        PUSH {R4,LR}\n        LDR R0, [SP, #8]\n        POP {R4,PC}\n        ENDP', 'fifth(1,2,3,4,99) returns 99 and restores R4/SP.',
 'A fifth parameter is not always the fifth word; 64-bit types can introduce alignment gaps earlier.',
 'fifth argument|stack arguments|sixth argument|stack offset')
entry('Function-template','Exam patterns','Use a small exported routine in the existing C project.',
 '; C: extern unsigned int plus_one(unsigned int value);',
 'In a copied Official Combined Exam API project, edit Source/ASM_funct.s and declare/call the exact export in Source/sample.c. Keep the existing startup_LPC17xx.s. Replace a demo routine only when its old call sites are also adjusted.',
 'This example updates NZCV; callers must not depend on flags surviving a function call.',
 '        AREA asm_functions, CODE, READONLY\n        PRESERVE8\n        THUMB\n        EXPORT plus_one\nplus_one PROC\n        ADDS R0, R0, #1\n        BX LR\n        ENDP\n        END',
 'plus_one(41) returns 42 in R0. It uses no callee-saved registers and makes no nested call.',
 'EXPORT name, function label, and C declaration must match exactly, including letter case.',
 'function skeleton|C assembly|extern|Source/ASM_funct.s')
entry('Array-loop','Exam patterns','Sum a word array using a bounded pointer loop.',
 '; uint32_t sum_words(const uint32_t *values, uint32_t count);',
 'R0 points to count readable 4-byte words; R1 is an unsigned count. A zero count performs no memory access. The sum wraps modulo 2^32; add an explicit carry/overflow exit if the paper requires it.',
 'The loop changes flags and uses BNE immediately after SUBS.',
 'sum_words PROC\n        MOVS R2, #0\n        CBZ R1, sum_done\nsum_loop\n        LDR R3, [R0], #4\n        ADD R2, R2, R3\n        SUBS R1, R1, #1\n        BNE sum_loop\nsum_done\n        MOV R0, R2\n        BX LR\n        ENDP',
 'For [3,5,7] and count=3, returns 15. For count=0, returns 0.',
 'Check zero before a decrement-and-branch loop; otherwise count=0 can wrap to a very large value.',
 'sum|loop|array traversal|empty array')
entry('If-else','Exam patterns','Implement a signed selection with explicit branches.',
 '; int32_t max_signed(int32_t a, int32_t b);', 'R0=a, R1=b. Use BGE for signed inputs; use BHS for unsigned inputs.', UNCHANGED+' CMP sets NZCV.',
 'max_signed PROC\n        CMP R0, R1\n        BGE max_done\n        MOV R0, R1\nmax_done\n        BX LR\n        ENDP',
 'max_signed(-1,2) returns 2.', 'Selecting an unsigned branch changes the meaning of negative bit patterns.', 'if else|maximum|selection')
entry('Remainder','Exam patterns','Compute quotient and remainder together.',
 '; R0=n, R1=d (unsigned, nonzero); R2=q, R0=remainder', 'For signed arithmetic substitute SDIV and preserve the numerator; the signed remainder follows the numerator’s sign. Check zero divisors separately.', UNCHANGED,
 '        UDIV R2, R0, R1\n        MLS R0, R2, R1, R0', 'For n=47,d=10: R2=4 and R0=7.', 'The quotient is not the remainder; keep the original numerator until MLS.', 'mod|decimal digits|division by 10')
entry('Exception-frame','Exceptions and system','Read a Cortex-M3 exception’s saved context.',
 'TST LR, #4\nITE EQ\nMRSEQ R0, MSP\nMRSNE R0, PSP',
 'At handler entry LR is EXC_RETURN. Bit 2 chooses MSP (0) or PSP (1). The basic saved frame is R0,R1,R2,R3,R12,LR,PC,xPSR at offsets 0,4,8,12,16,20,24,28. Capture the frame before changing the relevant SP. An alignment padding word can follow the basic frame; stacked xPSR bit 9 records it.',
 'TST updates flags. Returning through EXC_RETURN restores the saved context.',
 '        TST LR, #4\n        ITE EQ\n        MRSEQ R0, MSP\n        MRSNE R0, PSP\n        LDR R1, [R0, #24]\n        LDRB R2, [R1, #-2]',
 'In an SVC handler at entry, R2 receives the SVC immediate from the instruction before the saved return PC.',
 'This is handler-only code, not a normal C-callable function. Keep one owner of each vector and save EXC_RETURN before a nested BL.',
 'SVC handler|stacked PC|exception return|EXC_RETURN')
entry('Standalone-startup','Essentials','Keep a standalone assembly test separate from the C project.',
 '; Only in a separate assembly-only project with its own vector table:\nReset_Handler\n        MOVS R0, #41\n        BL plus_one\nstop\n        B stop',
 'An assembly-only image needs a valid initial SP, reset vector, linker layout, and its required data initialization. Follow the supplied standalone template. In the normal combined C project, startup enters the C runtime; callable examples must not replace it.',
 'Startup and calls may change flags.',
 '        ; A stop loop for a standalone debugger test:\nstop\n        B stop',
 'Execution stays at stop for debugger inspection.',
 'Pasting a custom Reset_Handler into the combined project can bypass C runtime initialization.',
 'reset handler|standalone|startup')

entry('ADRL','Values','Compute a wider-range PC-relative address using an ARMASM pseudo-instruction.',
 'ADRL R0, nearby', 'On Cortex-M3 Thumb-2, ARMASM expands ADRL into two 32-bit data-processing instructions. A PC-relative label must be in the same section and reachable by the expansion. Set bit 0 when using the address as a Thumb function pointer for BX/BLX.', UNCHANGED,
 '        ADRL R0, nearby\n        B after_nearby\n        ALIGN 4\nnearby  DCD 12\nafter_nearby',
 'R0 receives the address of nearby, not its stored value. The pseudo-instruction needs ARMASM; it is not a hardware opcode.',
 'A raw even code address passed to BX can attempt an unsupported state switch. Use an appropriate Thumb function symbol or set bit 0.', 'long address|PC relative')
entry('MOV32','Values','Load a 32-bit value using ARMASM expansion into MOVW and MOVT.',
 'MOV32 R0, #0x12345678', 'ARMASM pseudo-instruction; use a general register and a 32-bit constant or supported relocatable expression. It emits instructions rather than a literal-pool read.', UNCHANGED,
 '        MOV32 R0, #0x12345678', 'R0=0x12345678, equivalent here to MOVW #0x5678 followed by MOVT #0x1234.',
 'Other assemblers may not recognize MOV32 even when they support MOVW/MOVT.', 'wide constant|pseudo instruction')
entry('ARM|CODE32|LDC','Target boundaries','Recognize examples that are deliberately unsupported on Cortex-M3.',
 '; Other targets only: ARM / CODE32\n; Deliberate fault example: LDC p1, c0, [R1]',
 'ARM/CODE32 request ARM-state assembly, which this processor cannot execute. LDC accesses a coprocessor unavailable on LPC1768. The supplied exceptions lecture shows these concepts as fault demonstrations, not normal solution instructions.',
 'No normal result is defined for these examples on this target; a fault path is expected.',
 '        ; For normal Cortex-M3 code use:\n        THUMB\n        LDR R0, [R1]',
 'With R1 pointing to a readable word, LDR performs a normal memory load. It is not a replacement implementation of a coprocessor operation.',
 'Do not copy the lecture’s deliberate fault experiments into an ordinary callable function.', 'unsupported|coprocessor|UsageFault|ARM state')

CHECKLIST=[
 'Write the exact prototype: argument order, widths, signedness, pointers, and return contract.',
 'Match the C name, EXPORT, and assembly label; use the project-listed Source/ASM_funct.s.',
 'Distinguish a register value, an address, and memory at that address.',
 'Use byte/halfword/word access matching the object, and scale indexes by element size.',
 'Check every branch against signed or unsigned intent and the last instruction that set flags.',
 'Handle zero count before reading an array; check limits, output capacity, and divisor zero.',
 'Preserve modified callee-saved registers and incoming LR across nested calls.',
 'Keep SP word-aligned throughout and 8-byte aligned at public calls; restore it on every exit.',
 'Recalculate stack-argument offsets after all pushes, local storage, and padding.',
 'Confirm literal pools/data cannot be executed; keep writable objects out of read-only code.',
 'Use one handler definition per vector and retain the correct startup path.',
 'Trace zero, one element, negative inputs, maximum values, duplicates, and the required overflow behavior.',
]

for e in ENTRIES:
    if e['id'] in ('blo','bcc'):e['aliases']+=['unsigned less than','unsigned comparison']
    if e['id'] in ('bhs','bcs'):e['aliases']+=['unsigned greater than or equal','unsigned comparison']

def lookup_mnemonic(token):
    token=re.sub(r'\.(W|N)$','',token.upper())
    names={n.upper():e['id'] for e in ENTRIES for n in e['names']}
    if token in names:return names[token]
    if token[-2:] in {x[0] for x in CONDITIONS}|{'AL'}:return names.get(token[:-2])
    return None

def install(c):
    portal=c['PORTAL'];dest=portal/'asm/index.html';rel=c['rel'];esc=c['esc'];write=c['write']
    old_search=c['build_search'];old_page=c['page'];old_assets=c['build_assets']
    position=next(i for i,v in enumerate(c['NAV']) if v[0]=='API')+1
    c['NAV'].insert(position,('ASM Reference',dest))
    # Insertion order places the home tile beside API too.
    meta={}
    for key,value in c['SECTION_META'].items():
        meta[key]=value
        if key=='api':meta['asm']=('ASM Reference','Check instructions, syntax, flags, stack arguments, and short exam examples.')
    c['SECTION_META'].clear();c['SECTION_META'].update(meta)
    def page(*args,**kwargs):
        text=old_page(*args,**kwargs)
        source=args[0] if args else kwargs['source']
        if source==dest:
            text=text.replace('</head>','<link rel="stylesheet" href="'+rel(portal/'assets/asm_reference.css',source)+'">\n</head>')
            text=text.replace('</body>','<script src="'+rel(portal/'assets/asm_reference.js',source)+'" defer></script>\n</body>')
        if source==portal/'in-exam/index.html':
            text=text.replace('<div class="page-body">','<div class="page-body"><aside class="notice"><a class="button" href="'+rel(dest,source)+'">Open ASM Reference</a><p>Check an instruction, flags, a stack offset, or a function skeleton.</p></aside>',1)
        return text
    c['page']=page
    def assets():
        old_assets()
        for name in ('asm_reference.css','asm_reference.js'):
            write(portal/'assets'/name,(c['MAINTENANCE']/'portal_ui'/name).read_text(encoding='utf-8'))
    c['build_assets']=assets
    def build(items):
        items[:]=[i for i in items if not i['id'].startswith('asm-')]
        spellings={e['id']:set() for e in ENTRIES}
        from course_arm import ARM
        texts=[lesson['code'] for lesson in ARM]
        paths=[*c['GENERATED_SOURCES'].rglob('*.s'),*c['STARTING_TEMPLATE'].joinpath('Source').glob('*.s')]
        texts.extend(p.read_text(encoding='utf-8',errors='replace') for p in paths)
        for text in texts:
            for token in set(re.findall(r'\b[A-Za-z][A-Za-z0-9]*(?:\.[WNwn])?\b',text)):
                key=lookup_mnemonic(token)
                if key:spellings[key].add(token.upper())
        body='<section class="asm-intro" id="lookup"><p class="eyebrow">CORTEX-M3 · KEIL ARMASM</p><p>Find the exact spelling, see what changes, and check a small example before using it in your answer.</p><p>Examples are instruction snippets unless marked as complete functions. Establish the stated inputs and valid memory first. Use the current <code>Source/ASM_funct.s</code> in your copied project.</p><a href="#checklist">Before you run: exam checklist</a></section>'
        body+='<section class="asm-tools js-only" aria-label="Filter reference"><label for="asm-filter">Find an instruction or task</label><input id="asm-filter" type="search" placeholder="LDR, unsigned less than, fifth argument…"><label for="asm-category">Category</label><select id="asm-category"><option value="">All categories</option>'+''.join('<option>'+esc(cat)+'</option>' for cat in dict.fromkeys(e['category'] for e in ENTRIES))+'</select><button type="button" id="asm-clear">Clear filters</button><button type="button" id="asm-print">Print full reference</button><p id="asm-count" role="status" aria-live="polite"></p></section>'
        body+='<nav class="asm-index" aria-label="Alphabetical instruction index">'+''.join('<a href="#'+e['id']+'">'+esc(name)+'</a>' for name,e in sorted((n,e) for e in ENTRIES for n in e['names']))+'</nav>'
        body+='<nav class="asm-categories" aria-label="Reference categories">'+''.join('<a href="#category-'+c['slug'](cat)+'">'+esc(cat)+'</a>' for cat in dict.fromkeys(e['category'] for e in ENTRIES))+'</nav>'
        md=['# ARM Assembly Exam Reference','Cortex-M3 / Keil ARMASM. Generated from the same content as [ASM Reference](PORTAL/asm/index.html).','Use Source/ASM_funct.s in your copied project. Examples require the stated inputs and memory.']
        for cat in dict.fromkeys(e['category'] for e in ENTRIES):
            body+='<section class="asm-category" data-asm-group><h2 id="category-'+c['slug'](cat)+'">'+esc(cat)+'</h2>'
            md+=['\n## '+cat]
            for e in [v for v in ENTRIES if v['category']==cat]:
                title=' / '.join(e['names']);aliases=e['names']+e['aliases']+sorted(spellings[e['id']]);search=' '.join([title,e['category'],e['purpose'],e['rules'],e['syntax'],*aliases])
                body+='<article class="asm-entry" data-asm-entry data-category="'+esc(cat)+'" data-search="'+esc(search.lower())+'"><h3 id="'+e['id']+'">'+esc(title)+'</h3><p class="asm-purpose">'+esc(e['purpose'])+'</p>'
                md+=['\n### '+title,e['purpose']]
                for key,label in [('syntax','Syntax'),('rules','Operands and rules'),('flags','Flags'),('example','Example'),('result','Expected result'),('mistake','Watch for')]:
                    value=e[key];body+='<h4>'+label+'</h4>'
                    if key in ('syntax','example'):
                        body+='<pre><code class="language-asm">'+esc(value)+'</code></pre>';md+=['\n**'+label+'**\n\n```asm\n'+value+'\n```']
                    else:body+='<p>'+esc(value)+'</p>';md+=['\n**'+label+':** '+value]
                body+='<a class="asm-back" href="#lookup">Back to lookup</a></article>'
                items.append(dict(id='asm-'+e['id'],kind='ASM Reference',title=title,summary=e['purpose']+' '+e['result'],route=rel(dest,portal/'search.html')+'#'+e['id'],languages=['Assembly'],components=[],topics=[cat],aliases=aliases,text=search+' '+e['result']+' '+e['mistake'],relatedIds=[],examHistory='Extra practice',sourceClass='Maintained'))
            body+='</section>'
        body+='<section class="asm-fixed"><h2 id="condition-table">Condition codes at a glance</h2><div class="asm-table"><table><thead><tr><th>Suffix</th><th>Test</th><th>Meaning</th></tr></thead><tbody>'+''.join('<tr><td><a href="#b'+s.lower()+'">'+s+'</a></td><td>'+esc(t)+'</td><td>'+esc(m)+'</td></tr>' for s,t,m,_ in CONDITIONS)+'</tbody></table></div></section>'
        md+=['\n## Condition codes','| Suffix | Test | Meaning |','|---|---|---|']+['| '+s+' | '+t+' | '+m+' |' for s,t,m,_ in CONDITIONS]
        body+='<section class="asm-fixed"><h2 id="checklist">Before you run</h2><ol>'+''.join('<li>'+esc(v)+'</li>' for v in CHECKLIST)+'</ol></section>'
        md+=['\n## Before you run']+['- '+v for v in CHECKLIST]
        sources=[('Arm Cortex-M3 instruction and exception reference','https://www.keil.com/dd/docs/datashts/arm/cortex_m3/r2p1/dui0552a_cortex_m3_dgug.pdf'),('Keil ARMASM syntax and directives','https://www.keil.com/support/man/docs/armasm/default.htm'),('Arm procedure call standard (AAPCS32)','https://github.com/ARM-software/abi-aa/blob/main/aapcs32/aapcs32.rst')]
        body+='<section class="asm-fixed"><h2 id="sources">Sources and target</h2><p>Written for the LPC1768 Cortex-M3 and the package’s ARMASM project. This covers the exam materials and additional useful M3 instructions; it is not an index of every instruction in other ARM architectures. The reference and examples work offline. External manuals below need internet access.</p><ul>'+''.join('<li><a data-external-reference="manual" href="'+url+'">'+label+'</a></li>' for label,url in sources)+'</ul><p><a href="'+rel(c['GUIDES']/'ASM_INSTRUCTION_GLOSSARY.md',dest)+'">Markdown copy</a> · <a href="'+rel(portal/'courses/arm-machine.html',dest)+'">Learn assembly from the beginning</a></p></section>'
        md+=['\n## Sources and target','Cortex-M3 only. Broader ARM-state and floating-point instructions are outside this target. External manuals require internet.']+['- ['+label+']('+url+')' for label,url in sources]
        write(c['GUIDES']/'ASM_INSTRUCTION_GLOSSARY.md','\n\n'.join(md)+'\n')
        write(dest,c['page'](dest,'ASM Reference','Instructions, syntax, flags, and exam checks for Cortex-M3.',body,[('Home',c['HOME']),('ASM Reference',dest)],'ASM Reference'))
        items.append(dict(id='asm-reference',kind='ASM Reference',title='ASM Reference',summary='Instructions, directives, registers, flags, stack arguments, and exam examples.',route=rel(dest,portal/'search.html'),languages=['Assembly'],components=[],topics=['ARMASM'],aliases=['assembly reference','instruction guide'],relatedIds=[],examHistory='Extra practice',sourceClass='Maintained'))
    def search(items):
        build(items)
        # Also refresh assets when using the builder’s existing partial refresh route.
        for name in ('asm_reference.css','asm_reference.js'):
            write(portal/'assets'/name,(c['MAINTENANCE']/'portal_ui'/name).read_text(encoding='utf-8'))
        old_search(items)
    c['build_search']=search
    c['build_asm_reference']=build
