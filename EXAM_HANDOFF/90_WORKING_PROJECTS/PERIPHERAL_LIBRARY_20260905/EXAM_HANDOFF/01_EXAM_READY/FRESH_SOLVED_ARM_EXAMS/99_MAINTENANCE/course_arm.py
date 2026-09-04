"""ARM lessons use the current Cortex-M3 / Keil ARMASM target."""
from course_c import lesson
ARM = [
lesson("arm-machine", "1. The machine: registers, memory, and execution",
"""A processor executes instructions one at a time along its control-flow path. Registers are small named storage locations inside the processor. Memory is a larger byte-addressed storage space. An address identifies a location; the value stored there is separate. Loading reads memory into a register; storing writes a register value to memory.

R0-R12 are general registers with calling-convention roles. R13 is SP (stack pointer), R14 is LR (link/return register), and R15 is PC (program counter). The same 32 bits can represent an unsigned number, a signed number, or an address; instructions and contracts determine interpretation.

The LPC1768 uses Cortex-M3 and Thumb instructions. Do not paste ARM-state-only code from a different architecture. Trace a value's location after every instruction before tackling algorithms.""",
"        MOV R0, #7\n        MOV R1, R0\n        ADD R1, R1, #2",
"R0 receives 7 → R1 receives a copy of 7 → R1 becomes 9. R0 remains 7; no data-memory object was updated.",
"Predict R0/R1 after adding MOV R0,R1. Explain why that is not a memory load.",
["MOV copies a value between registers.", "A memory read uses an address and a load instruction."],
"Both registers contain 9. MOV copies R1 into R0; no address is dereferenced. LDR R0,[R1] would instead interpret R1 as an address and read memory there.",
"Confusing a value and an address often causes faults. Register names do not imply permanent variable meanings.",
"Trace three instructions and distinguish register, address, and memory value.", "Assembly|Core|Registers", 1),

lesson("arm-file", "2. A valid ARMASM file and the first return",
"""The assembler translates instructions and directives. A directive describes how to assemble or place code; it is not necessarily an executed instruction. AREA names a section; CODE and READONLY describe it. THUMB selects this target's instruction state. EXPORT makes a symbol visible to other files.

PROC/ENDP mark a function; END terminates the source. PRESERVE8 declares a stack-alignment obligation; it does not insert instructions that maintain it. The program must actually keep that promise.

In a working copy, use the project-listed Source/ASM_funct.s. Keep one definition of each exported symbol. Replace the illustrative function only after you have a matching C declaration. Never edit a historical Answer/assembly.s merely because a reference mentions it.""",
'''        AREA |.text.lesson|, CODE, READONLY
        PRESERVE8
        THUMB
        EXPORT identity
identity PROC
        BX LR
        ENDP
        END''',
"C passes a word in R0 → identity makes no change → BX LR returns to the caller → C receives the original word.",
"Call identity with 42. Then change it to return zero. Which directives execute on the processor?",
["R0 carries the ordinary word result.", "Directives instruct the assembler, not the running CPU."],
"identity(42)=42. Insert MOV R0,#0 before BX LR to return zero. AREA, PRESERVE8, THUMB, EXPORT, PROC, ENDP, and END are assembler directives.",
"Duplicate exports or missing project membership cause linker failures. ARMASM syntax is not GNU assembler syntax.",
"Build one exported leaf function and explain every line.", "Assembly|Toolchain|ABI", 2),

lesson("arm-contract", "3. Function contracts and register ownership",
"""Translate the requirement into a prototype before assigning registers. State element width, signedness, count, output capacity, mutation, empty cases, and return meaning. For ordinary 32-bit arguments, R0-R3 carry the first four words. A 64-bit argument has alignment rules; do not treat it as an arbitrary single register.

R0-R3 and R12 are caller-clobbered scratch registers. Any value needed after a nested call must be saved or held in callee-preserved storage. Preserve modified R4-R11 according to this project's calling convention; R9 has platform-specific roles, so preserve it when used. LR contains the return address after BL.

An algorithm contract is stronger than 'it works for this array.' It tells you which inputs are permitted and which output is correct.""",
"""; uint32_t count_equal(const int8_t *a, uint32_t n, int8_t key)
; R0 = readable signed-byte array
; R1 = element count
; R2 = key (signed value)
; result R0 = match count
; n=0: no loads, return 0
; input is unchanged""",
"With a=[-1,2,-1], n=3, key=-1, the required result is 2. The array pointer and eventual result share R0 at different times.",
"Allocate registers for base, count, key, index, and result. Explain what must be saved if you use R4 and R5.",
["Long-lived values should not accidentally be overwritten by return-value assembly.", "Changing a callee-saved register obliges restoration."],
"One choice: keep base R0/count R1/key R2, index R3, result R4, loaded value R5. Save and restore R4/R5, and move the result into R0 before restoring. No BL is needed for a simple scan.",
"Wrong signedness can count the wrong bytes. Forgetting preservation can break the caller even when the returned number is right.",
"Write the contract and a register map before instructions.", "Assembly|ABI|Functions", 3),

lesson("arm-flags", "4. Arithmetic, flags, and signed branches",
"""CMP subtracts conceptually to update flags without storing the subtraction result. Z records zero/equality; N records the result sign bit; C represents carry/no-borrow for relevant operations; V records signed overflow. Not every instruction updates flags. Use the intended flag-setting form when flags are part of the calculation.

Equality uses BEQ/BNE. Signed order uses BLT/BLE/BGT/BGE. Unsigned order uses BLO/BLS/BHI/BHS. The same bits can have different signed and unsigned order. Keep a comparison close to the branch that consumes its flags; a later flag-setting instruction can replace them.

ADDS can detect carry/overflow, but choose the flag matching the contract. ARM flag tests do not justify undefined signed overflow in C reference code.""",
"        CMP R0, R1\n        BLT signed_less\n        ; fall-through: signed R0 >= R1",
"R0=0xFFFFFFFF, R1=1: signed interpretation is -1<1, so BLT branches. Unsigned interpretation is 4294967295>1, so BLO would not.",
"Choose branches for an unsigned index reaching length and a signed sample below zero.",
["Counts normally use unsigned comparisons.", "Negative sample tests require signed semantics."],
"After CMP index,length use BHS for index>=length. After CMP sample,#0 use BLT for sample<0. Test zero, equality, and the high-bit-set case.",
"Using BLT for unsigned addresses/counts gives wrong behavior near the high bit. A CMP overwritten by arithmetic no longer supports the intended branch.",
"Explain C versus V and choose signed/unsigned branches from the data contract.", "Assembly|Flags|Signed|Overflow", 5),

lesson("arm-constants", "5. Constants, literal pools, and data definitions",
"""An immediate constant is encoded in an instruction, but not every 32-bit constant fits every instruction encoding. LDR R0,=constant is an assembler pseudo-instruction: it chooses an appropriate way to obtain that value. LDR R0,=label obtains a label's address; LDR R1,[R0] then reads the object.

Literal pools hold constants in the code layout. LTORG places a pool; execution must not fall into data. Put pools after an unconditional exit/branch as appropriate. Check assembler diagnostics if a literal is out of range.

DCB defines bytes, DCW halfwords, DCD words, and SPACE reserves bytes. Alignment ensures accesses start at required boundaries. Place mutable storage in a writable section, not a read-only constant table.""",
'''        LDR R0, =table
        LDR R1, [R0, #4]
        BX LR
        LTORG
        AREA lesson_data, DATA, READONLY
table   DCD 11, 22, 33''',
"R0 receives table's address, not 11. Loading at address+4 reads the second word, 22.",
"Change the table to bytes 11,22,33. Which load and offset select the second element?",
["DCD creates four-byte elements; DCB creates one-byte elements.", "Choose load width before choosing offset."],
"Use table DCB 11,22,33 and LDRB R1,[R0,#1]. Signed byte data would use LDRSB. Do not keep a four-byte offset after changing element width.",
"Falling through into LTORG data attempts to execute constants. Writing through a pointer to READONLY storage is invalid.",
"Distinguish obtaining a label address from loading its contents.", "Assembly|Memory|Directives", 7),

lesson("arm-memory", "6. Loads, stores, and signed element widths",
"""LDR/STR operate on words. LDRB/STRB operate on bytes; LDRH/STRH on halfwords. A byte load with LDRB zero-extends: 0xFF becomes 255. LDRSB sign-extends: the same byte becomes -1. Signedness affects loading and comparison separately.

A post-indexed load uses the old address and then updates the pointer. A pre-indexed access calculates the changed address first. Writeback changes the base register, so decide whether you still need the original pointer.

The current machine is little-endian: the least significant byte of a word is stored at its lowest address. Byte order and bit numbering are different concepts. Never read beyond a buffer merely because adjacent memory appears accessible.""",
"        LDRSB R2, [R0], #1\n        STRB R2, [R1], #1",
"If source byte is 0xFE: R2 becomes 0xFFFFFFFE (-2). STRB writes low byte 0xFE. Both pointers advance one byte.",
"Copy a signed halfword and then compare its value with zero. Select the access instructions and pointer increment.",
["A signed halfword requires sign extension.", "Halfwords occupy two bytes."],
"Use LDRSH with a two-byte increment, STRH for output, and CMP followed by signed BLT if checking negativity. Ensure alignment and valid source/destination capacity.",
"LDRB followed by signed comparison does not restore sign information. Incrementing a byte pointer by four skips elements.",
"Predict register contents for 0x7F, 0x80, and 0xFF under LDRB and LDRSB.", "Assembly|Memory|Bytes|Signed", 7),

lesson("arm-loops", "7. Arrays, loops, and safe early exits",
"""Translate a loop in four pieces: initialization, entry condition, body, and update. Check an empty count before the first load. Keep the invariant visible: at the top, index i identifies the next element, and the accumulator summarizes only earlier elements.

A nested loop needs independent outer and inner state. Restart the inner index for each outer iteration. An early exit still must restore the same stack/register state as an ordinary return. Prefer one shared return path rather than duplicated epilogues that drift apart.

A word index needs a byte scale of four. Either increment a pointer by four or scale an index; do not accidentally do both.""",
'''        MOV R2, #0
        MOV R3, #0
scan    CMP R2, R1
        BHS done
        LDR R12, [R0, R2, LSL #2]
        ADD R3, R3, R12
        ADD R2, R2, #1
        B scan
done    MOV R0, R3
        BX LR''',
"Input [2,4,6], n=3: indexes 0,1,2 load byte offsets 0,4,8; R3 becomes 2,6,12. n=0 branches directly to done.",
"Modify the method to stop at the first zero word. What result should [2,0,6] produce?",
["Test the loaded value before adding it.", "All exits should share done."],
"After LDR, CMP R12,#0; BEQ done. The result is 2. For [0] return 0. Define this sentinel policy in the contract; it is different from summing all n elements.",
"Loading before checking n breaks empty input. Reusing the outer index in an inner loop corrupts traversal.",
"Trace both normal completion and an early exit without losing stack balance.", "Assembly|Arrays|Loops", 10),

lesson("arm-layout", "8. Matrices, structures, and packed bits",
"""A matrix is a storage layout plus a coordinate rule. For a flat rows-by-cols matrix, element index=r*cols+c. Multiply by element size only once. Test rectangular examples because square ones can hide a wrong stride.

Structures use field offsets determined by the compiler's target ABI, including padding. Shared layouts need verified offsets and widths. A packed bit matrix has eight logical elements per byte and cannot use ordinary word addressing for each cell.

To access bit k, separate container index k/word_bits and bit position k%word_bits. Masking and shifting recover the logical value. State row order and bit order in the contract before translating a packed representation.""",
"""; R0 = base, R1 = row, R2 = column, R3 = columns
        MUL R1, R3, R1
        ADD R1, R1, R2
        LDR R0, [R0, R1, LSL #2]
        BX LR""",
"2-by-3 word matrix, row=1,col=2: index=5 → offset=20 → read the sixth element.",
"Locate logical bit 13 in a flat byte-packed array with least-significant-bit-first order.",
["Each byte contains eight logical bits.", "Remainder selects the position inside the byte."],
"Byte index=13/8=1; bit position=13%8=5. Read byte 1, shift right by 5, AND with 1. This mapping changes if the contract uses another bit order.",
"Assuming tightly packed structures yields wrong offsets. Mixing element count and byte count oversteps buffers.",
"Derive an address from dimensions, element size, and packing convention.", "Assembly|Matrix|Structures|Bits", 9),

lesson("arm-stack", "9. Stack frames, nested calls, and preservation",
"""The stack is memory addressed by SP. Saving registers allocates space and writes values; restoring reads them back and releases exactly that space. The stack grows down on this target. A non-leaf function calls another function, so BL overwrites LR; preserve the original return address first.

R0-R3/R12 may be overwritten by the callee. Move long-lived values into preserved registers or stack slots, while obeying your own preservation obligations. At a public call boundary SP must be eight-byte aligned. Saving an odd number of words can require padding.

An early return is not exempt from restoration. Use one epilogue for all paths and recalculate offsets whenever the prologue changes.""",
'''        PUSH {R4, LR}
        MOV R4, R0
        BL helper
        ADD R0, R0, R4
        POP {R4, PC}''',
"Entry SP=S → PUSH reserves 8 bytes → R4 holds the original input across helper → helper result plus original input returned → POP restores caller R4 and return address; SP=S.",
"Why is PUSH {LR} alone unsafe before a normal BL when entry SP is eight-byte aligned?",
["Each pushed word is four bytes.", "Alignment is required at the call, not just eventual return."],
"It moves SP by four, leaving SP misaligned at BL. Save an even number of words or reserve another four-byte slot, and release exactly the same amount. Never add padding without updating stack-argument offsets.",
"Saving LR after BL is too late. Keeping needed data in R2 across a call assumes a promise the callee did not make.",
"Draw entry SP, local frame, and restored SP for every return path.", "Assembly|Stack|ABI", 8),

lesson("arm-extra", "10. Fifth arguments and multiword ABI rules",
"""For five ordinary 32-bit arguments, the fifth word is at entry SP. A prologue moves SP, so its offset relative to the new SP increases by the frame size. One option is to read it at a known corrected offset. Another is to remember entry SP before changing it, but a caller-clobbered register holding that address cannot be trusted across BL.

64-bit arguments and results introduce alignment and register-pair rules. Under AAPCS a doubleword argument is aligned to an even-numbered register pair; a following argument may consequently move to the stack. Structures and variadic calls require further rules. Do not extrapolate the ordinary four-word shortcut.

The paper's exact prototype is authoritative. Annotate argument words and stack locations before writing loads.""",
"""; Five uint32_t arguments; fifth initially at [SP]
        PUSH {R4, LR}
        LDR R4, [SP, #8]
        ADD R0, R0, R4
        POP {R4, PC}""",
"At entry fifth=S[0]. After saving two words SP=S-8; [SP+8] still addresses fifth. The function returns first+fifth.",
"Change the save set to R4-R7 and LR with an extra four-byte alignment slot. Where is the fifth argument now?",
["Five registers consume 20 bytes.", "Include the padding in the total frame size."],
"After PUSH {R4-R7,LR} and SUB SP,SP,#4, the frame is 24 bytes. Fifth is [SP,#24]. Before returning ADD SP,SP,#4 then POP {R4-R7,PC}. Confirm alignment before any nested call.",
"A stale offset can read saved LR or another argument instead of the fifth. Saving entry SP in R12 is not safe across a callee.",
"Recompute a stack argument offset after a prologue change.", "Assembly|ABI|Stack|fifth argument", 8),

lesson("arm-wide", "11. Wide arithmetic, fixed point, and recurrence state",
"""A 64-bit integer can be represented by a low and high 32-bit word. Addition propagates carry from low to high: ADDS low then ADC high. Multiplication uses the signed or unsigned long form according to operand interpretation.

Fixed point stores a scaled integer. If a value has f fractional bits, real_value=stored/2^f. Multiplying two values doubles the fractional-bit count; rescale deliberately and define rounding, negative behavior, and overflow. A logical right shift is not a signed arithmetic shift.

A recurrence generates each term from earlier terms. Preserve all terms needed before overwriting one. Handle the seed-only cases before entering the general loop, and ensure indirect indexes refer to already initialized elements.""",
'''        ADDS R0, R0, R2
        ADC  R1, R1, R3
; (R1:R0) += (R3:R2)''',
"0x00000000:FFFFFFFF + 0x00000000:00000001 → low=0 with carry=1 → high=1 → total 4294967296.",
"Represent 1.5 in Q8. Compute its square using a wide intermediate, then rescale to Q8 with truncation for this positive example.",
["Q8 means eight fractional bits.", "The product initially has sixteen fractional bits."],
"1.5*256=384. 384*384=147456. Shift right by 8 →576, representing 2.25. Negative inputs require an explicit rounding policy; do not assume this positive example defines it.",
"Using ADD rather than ADDS loses carry. Overwriting a recurrence seed too early changes all subsequent terms.",
"State storage scale, intermediate width, and overflow policy before coding.", "Assembly|Wide|Fixed-point|Recurrence", 11),

lesson("arm-recursion", "12. Recursion and bounded work storage",
"""Recursion means a function calls itself with a smaller or simpler subproblem. The base case must return without another call. Each live invocation needs its own preserved state, so recursion consumes stack proportional to depth.

For DFS, mark a node visited before exploring its neighbors. A depth bound must define what happens when exceeded; it cannot merely be a hopeful estimate. An explicit stack moves that resource limit into a visible array with a capacity check. Cycles require visited state even when recursion terminates on a tree.

On an embedded exam target, stack space is finite and shared with exceptions. Choose a bounded algorithm and explain worst-case storage instead of relying only on a small successful example.""",
"""; Conceptual recursion, not a complete ARM function:
; factorial(n):
;   if n <= 1: return 1
;   preserve n and LR
;   result = factorial(n-1)
;   return n * result, restoring the frame""",
"factorial(3) waits for factorial(2), which waits for factorial(1)=1; unwind gives 2 then 6. Three invocations exist at the deepest point.",
"State a uint32_t factorial input bound and compare an iterative version's storage with recursion.",
["13! exceeds an unsigned 32-bit result.", "An iterative accumulator does not retain one frame per term."],
"Accept 0..12 for exact uint32_t factorial; reject or otherwise explicitly handle larger inputs. Iteration uses constant working storage; recursion uses depth-proportional frames. Test 0,1,12,13 and the error policy.",
"Missing base cases exhaust the stack. A graph cycle requires visited marking, not merely n-1 style reasoning.",
"Bound depth, output range, and every explicit work buffer.", "Assembly|Recursion|DFS|Stack", 8),

lesson("arm-exceptions", "13. Startup, exceptions, SVC, and vector ownership",
"""Reset starts at the vector-defined startup routine, which establishes the runtime before main. An ordinary function return and an exception return are different contracts. On exception entry, hardware stacks R0-R3,R12,LR,PC,xPSR; handler LR receives an EXC_RETURN token, not an ordinary caller address.

EXC_RETURN indicates which stack holds the interrupted frame. A wrapper must select MSP or PSP correctly before interpreting stacked fields. The Thumb SVC instruction is two bytes: its immediate can be decoded from the instruction at stacked PC minus two, because stacked PC points after SVC.

The current API emits optional fault/SVC wrappers only when enabled for the whole target. Otherwise startup/question code owns those vectors. Do not create two handlers or copy a wrapper without matching its ownership settings.""",
"""; Conceptual SVC inspection:
; frame = stack selected from EXC_RETURN
; instruction_address = frame->pc - 2
; immediate = instruction byte at instruction_address
; result, when required, is written to frame->r0""",
"SVC #5 executes → hardware stacks the following PC → handler locates instruction at PC-2 → immediate=5 → exception return resumes the interrupted code.",
"Explain why reading handler R0 is not always equivalent to reading the interrupted call's R0.",
["Handler code may already have changed registers.", "The hardware frame preserves the interrupted state."],
"Handler R0 can be scratch or a wrapper argument. The stacked frame's r0 is the interrupted value. Read/write that field when the exception contract requires returning a result to interrupted code.",
"Wrong MSP/PSP selection reads unrelated memory. Replacing EXC_RETURN with an ordinary return address breaks exception return.",
"Distinguish reset startup, BL/BX calls, and hardware exception entry/return.", "Assembly|SVC|Exceptions|IRQ", 13),

lesson("arm-debug", "14. Debug the contract, not just the final number",
"""A breakpoint pauses execution before a selected instruction. Step over follows a call as a unit; step into enters it. Use the memory window for input/output arrays and register view for argument locations. Compiler optimization can make source-level stepping less intuitive, so inspect actual instructions when needed.

Check entry arguments first, then the first iteration, final iteration, and return path. Record expected SP and preserved registers. A correct return value does not prove ABI correctness if the function damaged a caller register.

Reduce a failure to the smallest distinguishing input. Test empty, one element, repeated values, negatives where allowed, maximum widths, non-square matrices, and bounded output. For faults inspect the failing access and frame; do not randomize changes until the symptom disappears.""",
"""; Debugger checklist for a non-leaf routine:
; entry: note SP, R4-R11, input addresses/counts
; before BL: SP % 8 == 0; live values preserved
; exit: SP and saved registers restored
; memory: only allowed output region changed""",
"Returned result is correct but the caller later fails → compare saved R4 and SP → a changed callee-saved value explains the delayed failure.",
"An array routine passes n=3 but fails n=0. Where should the first breakpoint go?",
["Look for the first data load.", "Empty input must branch around that load."],
"Break before the first LDR and inspect the condition that reaches it. Ensure n=0 exits before dereferencing. Add an empty-input test and a sentinel around output to detect unrelated writes.",
"Changing multiple things at once destroys causal evidence. Simulator success does not establish actual button timing or board output.",
"Demonstrate correct output, unchanged inputs when required, preserved registers, and balanced SP.", "Assembly|Debug|ABI|Bounds", 14),
]
