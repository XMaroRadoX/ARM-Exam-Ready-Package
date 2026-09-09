"""Authored paper-specific content; execution writes only to the review staging copy."""
from pathlib import Path
import json,csv,re
work=Path(__file__).resolve().parents[1]/'90_WORKING_PROJECTS/QUESTION_REVIEW_20260908'
root=work/'EXAM_HANDOFF'
reviews={}
def add(qid,pages,contract,method,trace,why,mistakes,complexity,limits=''):
    reviews[qid]=dict(pages=pages,contract=contract,method=method.split('|'),trace=trace.split('|'),explanation=why.split('|'),mistakes=mistakes.split('|'),complexity=complexity,limitations=limits.split('|') if limits else [],reviewStatus='Reviewed against the original paper and maintained source')

add('2023-02-07-Q1',[1],
'void copyData(const int8_t *source, int8_t *destination, uint32_t length): R0=source, R1=destination, R2=byte count. void insertionSort(int8_t *values, uint32_t length): R0=array, R1=count. Both return void. Destination has at least length bytes; sorting changes only that destination.',
'Copy each byte without changing its bit pattern.|For each index i starting at 1, retain the signed key, shift larger predecessors right, and insert the key into the gap.',
'Copy [3,-14,15,-92,65,35,-89]. The bytes are unchanged.|Insert -14 before 3: [-14,3,15,-92,65,35,-89].|Final signed order: [-92,-89,-14,3,15,35,65]. Empty and single-byte arrays need no shifts.',
'LDRB/STRB suffice for copying; LDRSB is essential for signed comparisons during sorting.|R4 holds the base, R6 the outer index, R7 the key, and R8 the signed predecessor index. Test j<0 before loading A[j].',
'LDRB in the comparison treats -14 as 242.|Scaling an index by four corrupts byte storage.|Moving equal keys is unnecessary; BLE stops at the right position.',
'Copy O(n); insertion sort O(n²) worst case, O(n) when sorted; constant extra space.',
'Separate source and destination regions are assumed; this is not a general overlapping-memory move.')
add('2023-02-07-Q2',[2],
'Timer1 resets at MR0=0xFF with no match interrupt. Each accepted INT0 interrupt stores its low byte as signed data, up to MAX_VALUES=20. KEY1 sorts the initialized prefix and then lights physical LED11.',
'Keep a count independent of array capacity.|Alternate LED6 and LED7 only after a successful capture.|On KEY1, clear LEDs6/7, call insertionSort(values,count), then signal completion.',
'Capture 0xFE: values[0]=-2, LED6 on.|Capture 0x03: values[1]=3, LED7 on.|KEY1 sorts [-2,3] and lights LED11. Capture 21 is ignored once 20 slots are filled.',
'The cast to int8_t supplies the signed interpretation required by Q1.|The paper places sorting in the button handler; the generic advice to move all computation out of IRQs would change this answer.',
'Sorting all 20 slots includes uninitialized samples.|Passing 2 to the single-LED helper does not mean physical LED6.',
'O(1) capture; O(k²) sort for k<=20; 20 bytes of sample storage.',
'One raw external interrupt is treated as one press. Mechanical bounce and the 2-second-free handler runtime require board checks; no debounce period is prescribed in this paper.')
add('2023-02-24-Q1',[1],
'uint32_t KaprekarRoutine(uint32_t a): R0=a on entry, R0=descending_digits(a)-ascending_digits(a) on return. The paper starts with a four-digit unsigned value 1000..9999. This function performs ONE transformation, not the entire sequence.',
'Extract exactly four digits, including any zero digits.|Count the occurrences of digits 0..9.|Rebuild one number from 9 down to 0 and one from 0 up to 9; return their difference.',
'3075 has digits 3,0,7,5.|Descending=7530; ascending=0357=357.|Return 7173. For 1111, both rebuilt numbers are 1111, so return 0.',
'UDIV gives the quotient and MLS obtains the remainder without altering the digit order model.|The 40-byte frequency table is local. The saved-register frame plus local padding totals 80 bytes.',
'Returning 5 for input 3075 implements Q2 instead of Q1.|Dropping zero digits changes intermediate Kaprekar values.',
'Fixed four-digit work and a ten-word local table; constant time and space.')
add('2023-02-24-Q2',[2],
'SVC_Handler handles SVC #50. The caller uses MSP. Read its stacked R0, repeatedly call KaprekarRoutine, and leave the number of calls in LIVE R6. The basic hardware frame does not contain R6.',
'Save the original frame address without overwriting a callee-saved register.|Find the SVC immediate at stacked_PC-2; ignore other service numbers.|Count calls until the result equals 6174. Update stacked R0 to expose that final value on exception return.',
'3075 ->7173 ->6354 ->3087 ->8352 ->6174: R6=5.|Starting at 6174 still makes one call and returns R6=1.|Service 49 returns without running the loop.',
'R12 captures MSP before the software push; R7 becomes the frame pointer only after its original value has been saved.|BL replaces LR, so the handler saves and restores EXC_RETURN. KaprekarRoutine preserves the live R6 counter.',
'[frame+24] contains the saved PC, not the SVC opcode itself.|Writing the count into stacked R0 does not satisfy the required R6 output.|Saving R7 after replacing it with MSP loses the interrupted program’s R7.',
'At most seven transformations for the paper’s valid four-digit inputs with at least two distinct digits.',
'Equal-digit inputs such as 1111 never reach 6174; they are excluded by the convergence condition stated in Q2. This handler follows the specified MSP assumption.')
add('2023-05-17-Q1',[1,2],
'int32_t SDIV64(int32_t U, uint32_t L, int32_t D): R0=upper word, R1=lower word, R2=divisor; return quotient in R0. Treat U:L as one signed 64-bit dividend. No multiplication is used.',
'Remember the XOR of operand signs.|Take two’s-complement magnitudes, carrying the low-word increment into U.|Repeat 32 shifts: shift L into U, shift the quotient, subtract D when unsigned U>=D, and set the new quotient bit.|Restore the quotient sign.',
'Dividend -38 is U=0xFFFFFFFF,L=0xFFFFFFDA; D=-5.|Magnitude division gives 38/5=7 with remainder 3.|Both signs match, so R0=7. For D=5, R0=-7: division truncates toward zero.',
'LSLS on L exports its old bit31 as carry; ADC shifts U and includes that bit.|Unsigned BLO compares magnitudes after sign removal. Register saves protect R4-R8.',
'Negating only L fails whenever a borrow/carry crosses the word boundary.|Using ASR or signed magnitude comparisons breaks long division.|Multiplying by -1 violates the paper’s constraint.',
'Exactly 32 division iterations; constant extra space.',
'D must be nonzero. The returned signed quotient is meaningful when representable in 32 bits; the paper gives no division-by-zero result or out-of-range quotient policy.')
add('2023-05-17-Q2',[3],
'SDIV64S takes the same U,L,D arguments and returns R0 plus APSR flags: N=result bit31, Z=(result==0), C=0. This answer follows the paper’s explicit V test: V=0 iff floor(abs(D)/2)>abs(U). Preserve Q and non-NZCV state.',
'Compute the paper’s overflow test from the original upper word U, separately from taking the magnitude of the full dividend.|Call SDIV64.|Read APSR, replace only NZCV, and write APSR_nzcvq while retaining its original Q bit.',
'U=0,L=38,D=5: quotient7, N0 Z0 C0 V0.|U=-1,L=0xFFFFFFDA,D=2: quotient-19, N1 Z0 C0 V1 under the printed upper-word rule.|U=0,L=0,D=1: quotient0 but V1 under that same rule.',
'R7 holds the chosen V flag across BL; SDIV64 preserves it.|The final MSR is followed by non-flag-setting stack restoration so the requested flags survive the return.',
'The high word of abs(U:L) is not abs(U).|-19 does fit in 32 bits even though the paper’s approximation may set V; do not call this an exact mathematical overflow detector.',
'32 division iterations plus constant flag work.',
'The paper’s V formula conflicts with its statement that V exactly detects signed-32-bit overflow. The implementation deliberately follows the explicit formula; examples on this page expose the discrepancy rather than hiding it.')
add('2023-07-04-Q1',[1],
'uint32_t isSociable(uint32_t n): R0=n; return the first cycle length 1..8 that returns to n, or zero. There is no output-array argument. Natural inputs are treated as positive integers.',
'Compute an aliquot sum using the paper’s paired-divisor scan.|After each term, first check for a return to the starting value, then the terminal value 1, then the eight-term limit.',
'28 ->28: return1.|220 ->284 ->220: return2.|12496 ->14288 ->15472 ->14536 ->14264 ->12496: return5.|100 ->117 ->65 ->19 ->1: return0. Input1 has proper-divisor sum0 and returns0.',
'For a*b=n, add both a and b only when a<b; add a once for a perfect square.|R4 retains the starting value, R5 the current value, and R6 the count across BL aliquotSum.|A guard for n<=1 prevents the divisor loop from running forever on 1.',
'Counting the initial value as an already computed term shifts the returned cycle length.|Adding the square root twice inflates the aliquot sum.',
'At most eight aliquot sums; the required scan can take O(n) divisor attempts for a prime. Constant storage.',
'Intermediate sums must fit uint32_t. This answer retains the specified divisor algorithm, so its runtime is not guaranteed to fit a tight interrupt budget for arbitrary large inputs.')
add('2023-07-04-Q2',[2],
'Timer1 runs every 2000 ms. Its handler cycles through [8128,5564,5400,14264,1305184,1598470,4938136], calls isSociable, and maps results1..8 to physical LEDs4..11; zero means all off.',
'Read the current array element, call the real assembly function, then advance and wrap the seven-element index.|Clear the old display before selecting the result LED.',
'First interrupt: isSociable(8128)=1, so LED4.|An isolated zero result clears every LED.|After the seventh interrupt, the eighth uses 8128 again.',
'result+3 converts a mathematical sequence length to a physical LED label.|The MR0 flag guard prevents an unrelated timer status from advancing the sequence.',
'Writing result as a binary LED mask differs from selecting exactly one physical LED.|Wrapping at eight would read past the seven-element source array.',
'One bounded eight-term search per interrupt; seven constant source words.',
'The paper explicitly calls the algorithm inside Timer1. Physical runtime and 2-second scheduling are not established by a mocked handler test.')
add('2023-09-18-Q1',[1],
'uint32_t digitSum(uint32_t a) returns its decimal digit sum. uint32_t digitaddition(uint32_t *area,uint32_t N) fills N words including area[0], then returns the sum of digits of ALL N stored terms. Return zero immediately if generating a term overflows uint32_t. Q1 also requires a 50-word area and a chosen initial value in Reset_Handler.',
'Compute digitSum of the initial term once.|Generate next=current+digitSum(current); check carry before storing.|After storing, compute and accumulate the NEW term’s digit sum.',
'Seed47,N5 stores [47,58,71,79,95].|Digit sums are [11,13,8,16,14]; total=62.|N1 returns11 and leaves the seed alone. Seed0xFFFFFFFF,N2 returns0 before writing the second term.',
'R6 is the current term and R7 the accumulated digit sum.|ADDS followed immediately by BCS catches unsigned overflow. The corrected loop calls digitSum on the new term before adding to R7.',
'Adding the predecessor’s sum duplicates the seed and omits the final term.|Testing V instead of carry checks signed overflow, which is a different contract.',
'O(N*d) for at most ten decimal digits per word; constant call-frame space in addition to N output words.',
'The standalone Q1 startup example chooses47 and reserves50 words. Empty N returns0 as an explicit safe extension.')
add('2023-09-18-Q2',[2],
'KEY1 appends binary0 to K; KEY2 appends1. INT0 sets series[0]=K and requests10 terms. Compare the reported sum with last-first+digitSum(last). Equal: LED4 on/LED5 off; unequal: the reverse.',
'Maintain K with shift-and-OR operations.|Generate the ten-word series on INT0.|If generation reports overflow, signal failure without reading an unwritten last slot.|Otherwise compare the independent telescoping identity.',
'KEY2,KEY1,KEY1,KEY2,KEY2,KEY1 gives binary100110=38.|For the five-term teaching example, 95-47+14=62 matches the corrected routine.|An overflowing generation lights LED5 and never uses stale series[9].',
'The identity works because each next-current equals digitSum(current); only the final digit sum remains to be added.|K is a number, not the series length: the Q2 length is always10.',
'The old “K up to50” metadata confused the Q1 storage capacity with the input value.|Reading series[9] after an early overflow makes the comparison meaningless.',
'Constant button work; ten generated terms per INT0.',
'Input digits beyond the 32-bit width wrap in the uint32_t accumulator; the paper does not define a wider entry format. Raw-button bounce remains a board limitation.')
add('2024-02-12-Q1',[1,2],
'uint32_t mazeSolver(uint32_t rows,uint32_t columns,uint8_t *maze): R0=rows,R1=columns,R2=flat writable bytes. Walls are *, passages are spaces, border exits are lowercase n/e/s/w. Mutate reachable passages into directions; return the number of productive propagation waves.',
'Scan spaces and select the first lowercase neighbor in north,east,south,west order.|Write uppercase directions during phase1.|Convert uppercase directions to lowercase only in phase2; repeat while anything changed.',
'In a 3x3 maze [*n*,* *,***], the center sees n above and becomes N.|Phase2 changes N to n; the next scan changes nothing, so return1.|A sealed maze with no exit returns0 and leaves its spaces unchanged.',
'Uppercase markers prevent newly discovered cells from influencing later cells in the SAME scan.|Neighbors of a space are safe because the paper guarantees border cells are walls or exits.',
'Using # as the wall or E as the exit applies the wrong encoding.|Writing lowercase immediately makes scan order determine path lengths.',
'O(rows*columns*D), where D is maximum reachable distance; in-place with constant extra space.',
'Dimensions, accessible storage, and the guaranteed border encoding are preconditions. Unreachable interior spaces remain spaces.')
add('2024-02-12-Q2',[3],
'KEY2 samples free-running Timer0, creates a10x8 maze, then calls mazeSolver inside EINT2_IRQHandler. Generate values with (previous*18) mod101. Border threshold90; interior passage threshold60. Corners are always * and consume no random value.',
'Reduce the seed modulo101 before multiplication so a full-width timer value cannot overflow the intended mathematical recurrence.|Visit cells in row-major order and select n/e/s/w according to the border.|Run the two-phase solver after all cells are initialized.',
'Seed300 ->47,38,78,91,22,93 for the six noncorner cells in row0.|The completed first row is ****n*n*.|A zero seed stays zero: every border is a wall and every interior cell starts as a passage.',
'(value%101)*18 has a maximum intermediate of1800 and preserves the mathematical modulus.|The multiplier18 is not a wall threshold. All generation and solving stay in the handler as explicitly requested.',
'Using a 32-bit multiply before the first modulus changes large timer seeds.|Consuming random numbers for corner cells shifts the entire maze.',
'O(rows*columns) generation plus the solver’s propagation cost.',
'Timer sampling supplies a changing seed, not a demonstrated source of statistically true randomness. This is a raw KEY2 handler; no debounce interval is prescribed.')
add('2024-02-28-Q1',[1],
'uint32_t shortestPath(uint32_t rows,uint32_t columns,uint8_t *maze): walls X, spaces unvisited, entrance e, exit numeric byte0. Fill distance bytes and return the distance k of a cell adjacent to the entrance; the final entrance-to-exit route has k+1 moves.',
'Start with wave0 at the exit.|Only spaces neighboring the CURRENT wave receive wave+1.|When e neighbors the current wave, return that wave value.|Stop with UINT32_MAX if no frontier remains or byte labels would collide with the space marker.',
'A corridor X,0,space,e,X receives distance1 in its space; return1, with two moves to the exit.|The supplied9x8 maze returns8 and needs nine LED directions.|An entrance separated from the exit by walls returns UINT32_MAX instead of looping indefinitely.',
'Comparing neighbors to R7 avoids propagating more than one distance in a scan.|R12 counts new labels and detects a disconnected frontier.|The output deliberately leaves e in place for the C playback code.',
'Numeric0 is the exit; character 0 is byte48 and is wrong.|Returning9 for the supplied example confuses moves with the requested iteration count.',
'O(rows*columns*D); constant extra storage.',
'This byte encoding cannot safely distinguish distance32 from a space. The implementation reports UINT32_MAX for disconnected mazes or unsupported wave depth32 rather than claiming arbitrary-size maze support. The paper’s supplied maze is within the supported range.')
add('2024-02-28-Q2',[2],
'Solve the exact9x8 C maze, then use Timer0 at500 ms per phase. Right/down/left/up map to LEDs4/5/6/7. Show each move for500 ms, then blank for500 ms. Include the final move into numeric0.',
'Locate e and keep the returned neighboring distance as a signed step counter.|On an on-phase choose a neighbor equal to step_value.|On the next phase clear LEDs and decrement the distance. Stop producing moves after zero has been consumed.',
'Expected physical LED sequence:6,6,7,7,6,6,6,7,7.|Each adjacent pair is separated by an off-phase.|A solver failure leaves the error display on instead of attempting a route.',
'Timer0 publishes a phase event; foreground owns position, showing, and step_value.|The implementation starts its first on-phase at the first500 ms event; the paper does not specify initial delay.',
'Stopping at k>0 omits the exit move.|Leaving the preceding LED lit can show two directions at once.',
'One constant-size neighbor search per half-second event.',
'Event flags coalesce multiple delayed ticks. Exact wall-clock playback requires foreground work to keep up with500 ms intervals and needs a board check.')
add('2024-07-09-Q1',[1,2],
'void depthFirstSearch(uint8_t *maze,uint32_t rows,uint32_t columns,uint32_t start): R0-R3 in that order. Border bytes are0xFF. Interior bit0=visited; bits1/2/3/4=open right/down/left/up. chooseNeighbor receives four visited flags and returns the first unvisited direction1..4, or0.',
'Mark the current cell visited.|Check right,down,left,up and call chooseNeighbor.|Carve reciprocal passage bits and save the parent before descending.|When no neighbor remains, pop a parent; finish when the parent stack is empty.',
'For the paper’s6x5 matrix,start7: first move7->8 opens right and left bits.|Next8->13 opens down and up bits.|The deterministic route visits all12 interior cells and creates11 passages, with all border bytes unchanged.',
'Each saved parent uses8 bytes, retaining alignment at helper calls.|The chooser is deterministic in Q1; SysTick randomness belongs to Q2.',
'Marking only the current side of a passage creates inconsistent walls.|Treating the border as unvisited can cause out-of-bounds neighbor loads.',
'O(V) maze visits with O(V) worst-case parent-stack space; reserve enough stack for8 bytes per saved parent plus call frames.',
'The start must be an interior cell of a correctly initialized maze; no generic malformed-maze validation is supplied.')
add('2024-07-09-Q2',[3],
'chooseRandomNeighbor receives the same four flags as chooseNeighbor. Push eligible direction numbers in right/down/left/up order, index that stack by SysTick_VAL mod count, and return0 if none are eligible. Q2 Reset_Handler sets LOAD=0xFFFFF and starts SysTick without interrupts.',
'Collect eligible directions in stack-local storage.|Reverse the remainder index to match the order produced by literal descending-stack pushes.|Restore the entire local frame on every exit.|Use the Q2 startup override and call depthFirstSearchRandom from C.',
'Flags[0,0,0,1] push1,2,3; stack top-to-bottom is[3,2,1].|VAL=4 gives remainder1 and direction2.|All flags1 returns0 without division. CTRL=5 enables the core-clock counter with TICKINT clear.',
'The existing SysTick helper enables TICKINT, so it cannot express this paper’s startup contract.|The Q2 assembly supplies one strong Reset_Handler over the template’s weak default, then enters the normal C runtime.',
'LOAD=0xFFFFFF adds an extra hex digit; the paper specifies0xFFFFF.|Failing to remove candidate words before returning corrupts SP.',
'At most four candidates and constant helper space; DFS retains its own O(V) parent stack.',
'The timer-based choice is not a proof of statistical randomness. Keep the original startup vector table and use only one strong Reset_Handler.')
add('2024-09-16-Q1',[1,2,3],
'void kruskal(uint8_t *maze,uint8_t *horizontal,uint8_t *vertical,uint32_t rows,uint32_t columns,uint32_t y,uint32_t x). R0-R3 hold the first four; entry[SP], [SP+4], [SP+8] hold columns,y,x. Each array has rows*columns bytes; cells start with distinct labels0..N-1.',
'Add y to x. Select a horizontal wall when x<N; otherwise subtract N once and consider a vertical wall if the resulting x<N.|Wall1 between unequal labels is removed and every occurrence of the larger label is replaced with the smaller.|Wall0 increments y; border marker2 does nothing. Finish once all labels are zero.',
'Paper example3rows,4columns,x2,y4: x becomes6; remove horizontal wall6 and merge label7 into6.|Next x10 merges11 into10.|Then x14 becomes vertical index2, connecting labels2 and6. The printed example finishes after17 iterations.',
'R12 captures entry SP before the40-byte frame, so the three stack arguments remain correctly addressed.|Replacing every occurrence of the larger label merges whole components, not just two cells.',
'The heading calls the example4x3, but its arrays have four columns and three rows.|Using modulo2N instead of the printed single subtraction changes the specified algorithm.|Byte labels require N<=256.',
'O(N) relabelling and completion scans per attempted wall; constant extra space.',
'The paper does not establish termination for arbitrary increments, offsets, and dimensions. Keep its algorithm and test the selected3x4 button configurations; do not promise a general-purpose maze generator.')
add('2024-09-16-Q2',[4],
'Initialize a3x4 maze and wall arrays. The first button chooses increment: INT0=2,KEY1=3,KEY2=4. The second chooses offset with the same mapping and immediately calls kruskal with seven arguments.',
'Use selection_count to distinguish first from second input.|Initialize each cell label from its row-major index and use wall marker2 at the appropriate borders.|Pass rows before columns, then increment before offset.',
'KEY2 then INT0 selects y4,x2 and produces the paper’s17-iteration example.|After the first press alone, kruskal has not run.|The finished maze contains only component label0; border walls retain marker2.',
'C supplies the last three arguments on the stack automatically.|The first parameter is the maze pointer, not the row count used by other maze routines.',
'Swapping the two chosen button values changes the generated maze.|The INT0 handler is required as well as KEY1 and KEY2.',
'O(1) selection plus the Q1 wall-removal work.',
'The original paper defines one two-button generation. The example resets the selection counter for another pair but does not reinitialize an already completed maze. Raw-button bounce must be considered on hardware.')
add('2025-01-29_ARM1-Q1',[1,2],
'uint32_t bitwiseAffineTransformation(const uint8_t *A,uint32_t b,uint32_t c): R0=A,R1=b,R2=c; return d in R0. A contains eight packed row bytes. Row0 produces bit7; vector bits and row columns run most-significant first. Inputs remain unchanged.',
'Start the result with c.|For each row, compute A[row]&b, reduce its eight bits by XOR, and toggle result bit7-row when parity is1.',
'For A=[F8,7C,3E,1F,8F,C7,E3,F1], b=AA,c=63: row0 AND b=A8 has three1-bits, so parity1 sets d7.|Row1 AND b=28 has two1-bits, so parity0 leaves c6 set.|The final byte is C9, matching the paper.',
'R4 keeps the matrix pointer; UXTB limits b and c to bytes.|The inner loop computes parity, not a numerical sum. The row index determines the destination bit.',
'Swapping R0 and R1 treats a byte as an address.|OR reduction gives the wrong result for rows with an even number of matching bits.|Mapping the first row to bit0 reverses the output.',
'Eight rows times eight parity steps;32-byte saved-register frame.',
'The printed matrix has a mislabeled symbolic entry and repeated final d1 label; follow the explicit byte ordering and worked C9 result.')
add('2025-01-29_ARM1-Q2',[3],
'Timer1 resets at0xFFFF without IRQ. INT0 XORs bits15..8 with bits7..0 and displays the byte. KEY1 uses A=[8F,C7,E3,F1,F8,7C,3E,1F], c=63, and that displayed logical byte; Timer0 toggles every250 ms for a500 ms blink cycle.',
'Store the captured byte separately from the LED hardware’s temporary off-phase.|Call the assembly function using the Q2-specific matrix.|Display the transformed byte immediately and restart the250 ms phase timer.',
'Timer1=0x123442AA: mask to42AA, then42 XOR AA=E8.|Q2’s matrix transforms E8 with c63 into F0.|At250 ms clear the LEDs; at500 ms show F0 again.',
'The Q2 constant matrix differs from Q1’s example. The maintained answer previously reused the wrong one.|blink_is_on tracks the phase while displayed_value retains the logical payload.',
'Using500 ms per toggle doubles the full blink period.|Taking the high byte of all32 timer bits violates the low16-bit requirement.',
'Constant capture/phase work plus one fixed affine computation per KEY1.',
'During a blink off-phase, KEY1 transforms the stored logical value. The paper does not define repeated-button timing; this interpretation prevents blanking from replacing the input with zero.')
add('2025-01-29_ARM2-Q1',[1,2,3],
'void bitMatrixMultiplication(const uint8_t *A,const uint8_t *B,uint8_t *C): R0=A,R1=B,R2=C. All are eight row bytes, MSB first. Write C=A*B over GF(2); preserve A and B. Q2’s explicit void prototype governs the return contract.',
'For each output row i and column j, XOR the eight products A[i,k]&B[k,j].|Set bit7-j of the output row from that parity, then store the completed byte.',
'The paper’s A starts with20, selecting row2 of B; therefore C[0]=3E.|Complete expected C=[3E,7B,0B,C5,79,EC,F3,63].|Multiplication by the MSB-first identity matrix returns the other matrix unchanged.',
'R8 retains one A row, R10 selects a B column, and R12 accumulates parity.|C is separate writable storage; no initial C contents are used.',
'XORing matching row bytes is not matrix multiplication.|The phrase “returns C” does not require inventing a scalar return when the supplied C prototype is void.',
'8*8*8 bit products;40-byte saved-register frame.',
'C must not overlap A or B. The source leaves the C pointer in R0 as a convenience, but callers must use the specified output array.')
add('2025-01-29_ARM2-Q2',[3],
'INT0 captures exactly eight pairs of bytes from Timer1: high8 into A, low8 into B. Timer1 resets at0xFFFF with no IRQ. KEY1 before eight captures does nothing; afterward compute C and display its eight rows once for500 ms each, then blank.',
'Track input_rows separately from output_row.|Show C[0] immediately on KEY1 and set the next row index to1.|Each Timer0 match advances one row; the event after C[7] clears the display and stops the timer.',
'First capture42AA stores A[0]=42,B[0]=AA.|With eight identity rows in A and arbitrary B, C=B.|At time0 show row0; at3.5 s show row7; at4 s all LEDs off.',
'The two counters prevent capture progress from being confused with display progress.|The handler returns after the eighth input, so a ninth press cannot write past the arrays.',
'The output is one pass, not an endless row cycle.|Starting with output_row0 after already showing C[0] repeats the first row.',
'Three8-byte matrices and constant state; one matrix product per accepted KEY1.',
'Repeated KEY1 restarts output from row0. The paper does not prescribe a separate reset-to-capture operation.')
add('2025-01-29_ARM3-Q1',[1],
'void transposition(const uint8_t *A,uint8_t *AT): R0=input,R1=output; eight bytes each, MSB-first columns. A is read-only; AT is a distinct writable array. The prior transpose symbol remains an alias for compatibility.',
'Clear all eight output bytes.|For each source bit at row i,column j, set destination row j,bit7-i when the source bit7-j is1.',
'[F8,7C,3E,1F,8F,C7,E3,F1] transposes to[8F,C7,E3,F1,F8,7C,3E,1F].|A single bit in A[0] at mask40 moves to AT[1] at mask80.|Transposing twice recovers the original matrix.',
'Clearing AT is necessary because set bits are accumulated with OR.|Separate loop indices control source row and destination row; reversing a byte alone cannot transpose a matrix.',
'Exporting only transpose misses the exact transposition name in the paper.|Using the same source and destination erases source data during the clear loop.',
'64 bit inspections plus8 clears;32-byte saved-register frame.')
add('2025-01-29_ARM3-Q2',[2],
'Timer2 resets at0xFFFF without IRQ. KEY1 fills A and KEY2 fills B, each with eight low timer bytes; further presses are ignored. INT0 calls transposition three times to compare transpose(A XOR B) with transpose(A) XOR transpose(B). Success lights LED4; failure LED5.',
'Maintain independent capture counts.|Build A XOR B into separate storage.|Transpose the XOR, then A, then B; compare all eight result bytes.',
'A with only row0=80 and B with only row0=40 gives A XOR B row0=C0.|The left transpose contains80 in rows0 and1; the right XOR produces the same bytes.|Eight filled rows in A alone are insufficient; wait for B as well.',
'Temporary arrays prevent one side of the identity from overwriting inputs needed by the other.|The uint8_t cast intentionally keeps only the timer’s low byte.',
'Comparing only the first output byte misses errors in other columns.|A hard-coded success LED does not test the identity.',
'Three fixed64-bit transposes and eight-byte comparison; seven8-byte arrays.',
'INT0 before both arrays are filled is ignored as a safe completion policy; the paper does not specify how partial input should be handled.')

for variant,name,initial,den,example in [
    ('ARM1','Maclaurin','10*y','(2*i)*(2*i+1)*100','y20,n3: terms200,-133,26,-2; sum91'),
    ('ARM2','Maclaurin_cos','100','(2*i-1)*(2*i)*100','y25,n4: terms100,-312,162,-33,3; sum-80')]:
    add('2025-02-12_'+variant+'-Q1',[2],
    f'int32_t {name}(int32_t y,uint32_t n): R0=y,R1=maximum order n; R0=scaled approximation. y represents10*x and the output approximates100*sin(x) or100*cos(x), respectively. Include terms0 through n.',
    f'Start t0={initial} and sum=t0.|For i=1..n, form the entire signed numerator -previous*y*y and denominator {den}; divide once with truncation toward zero.|Accumulate the term before advancing i.',
    example+'|n0 returns the initial term without entering the loop.|y0 gives0 for sine and100 for cosine at every tested order.',
    'R4 retains y,R5 n,R6 the current term,R7 the sum,R8 i.|SDIV performs signed truncation toward zero. Computing powers/factorials independently is unnecessary and can change overflow behavior.',
    'Dividing early loses precision and changes the required recurrence.|n is the maximum order, so n3 means four terms.|Do not interpret the result as100*sin(y) with an unscaled angle.',
    'O(n) recurrence iterations;32-byte frame, no factorial table.',
    ('The sine notation in the paper reuses y inconsistently; follow its y=10*x definition and worked recurrence.' if variant=='ARM1' else 'The cosine example’s last numerator/denominator line has typographical errors. The stated recurrence gives20625/5600=3 and the printed final sum-80.')+
    '|The claimed absence of overflow is not a guarantee for arbitrary int32_t y and order. Tests cover the paper examples and waveform domain y=-31..31,n3; wider inputs require separate bounds analysis.')
    timer=0 if variant=='ARM1' else 1;button='INT0' if timer==0 else 'KEY1';wave='sine' if timer==0 else 'cosine';ticks=1263 if timer==0 else 1592
    add('2025-02-12_'+variant+'-Q2',[3],
    f'{button} starts Timer{timer} once, with match threshold{ticks} timer clock ticks. IRQ_timer.c contains int {wave}Values[45] and the timer handler. Start ticks=0,repeat=0; after ticks22, wrap to-22 and increment repeat. End when repeat reaches200.',
    f'Round1.428*ticks to the nearest signed integer by adding or subtracting0.5.|Compute output=500+{name}(input,3)/2 using signed integer division.|Store at index ticks+22 and write the10-bit DAC value.|Advance the index exactly as the paper does; after completion write zero and stop the timer.',
    f'First sample: ticks0,input0,output{500 if timer==0 else 550}, stored at index22.|After the first23 samples, ticks wraps from22 to-22 and repeat becomes1.|Then199 complete45-sample cycles finish the run:8978 samples total, followed by a zero output.',
    'The initial cycle is a half-cycle because the supplied pseudocode starts at ticks0, not-22.|The array remains present for inspection even though playback computes each sample directly.|The complete IRQ_timer.c replacement preserves unused timer handlers and avoids duplicate vector definitions.',
    'Using milliseconds for a clock-tick threshold gives the wrong note.|Starting at-22 produces9000 samples and changes the requested initial state.|Dropping the inspection array omits a graded deliverable.',
    'One order3 recurrence per sample;45 int values plus constant state.',
    'The cosine pseudocode is missing a closing brace; the answer follows the matching sine structure and its repeat<200 guard.|No repeated-button handling or debounce is required here. Native compilation does not establish that floating-point emulation and the IRQ body meet the actual sample deadline.')

add('2025-07-01_ARM1-Q1',[1],
'uint32_t nextElementLCG(uint32_t previous,uint32_t a,uint32_t c,uint32_t n,uint32_t m): R0-R3=previous,a,c,n; entry[SP]=m. Return ((a*previous+c) XOR n) mod m. The standalone Reset_Handler fills DIM10 bytes from seed1,a131,c7,m255.',
'Multiply and add before XORing with the iteration index.|Read m at SP+8 after saving R4 and LR.|Compute the remainder from unsigned quotient and feed the result into the next startup-loop call.',
'First call:(131*1+7) XOR0=138;138 mod255=138.|Second:(131*138+7) XOR1=18084;mod255=234.|First10 bytes:8A EA 3F 67 EC 47 7E C6 B6 7D.',
'Each caller reserves8 bytes for the fifth argument and alignment padding.|STRB stores one result per slot. The standalone reset handler stops for debugger inspection rather than starting the game.',
'Using the previous value as the XOR mask confuses this variant with ARM2.|Reading[SP] after the push reads a saved register, not m.',
'Constant work per term;DIM bytes of output and a fixed call frame.',
'm must be nonzero. The paper’s parameters keep products in range; the routine otherwise uses32-bit machine arithmetic.')
add('2025-07-01_ARM1-Q2',[1,2],
'Timer0 fires every3000 ms and calls nextElementLCG exactly10 times using the Q1 constants. Map remainder0/1/2/3 to physical LEDs11/10/9/8, with exactly one LED on. Q2 leaves the final LED lit.',
'Retain previous and n across interrupts.|Acknowledge MR0, reject calls after n10, then generate and display the next value.|Clear the old LED before enabling the new one; stop Timer0 after the tenth call.',
'Expected LEDs:9,9,8,8,11,8,9,9,9,10.|The tenth interrupt displays10 and stops generation.|An additional handler call must not generate an eleventh number.',
'Static locals are sequence state, not reset-on-entry temporary variables.|The supplied IRQ_timer.c replacement leaves TIMER0_IRQHandler in main.c as its single owner.',
'Mapping remainder directly to an LED API argument uses invalid physical labels.|Applying the Q3 win/lose display changes Q2’s requested behavior.',
'Ten constant-time generator calls and constant state.')
add('2025-07-01_ARM1-Q3',[2],
'Extend Q2 with one directional joystick answer per round. LEDs11/10/9/8 mean UP/LEFT/RIGHT/DOWN. First movement increments num_correct or num_wrong and immediately clears the LED. After the tenth full response window, win on num_correct>num_wrong: LED4; otherwise LED5.',
'Open a response window only after displaying a generated value.|Poll directional edges every10 ms; update previous input even outside an active window.|The first edge closes the window. After ten values, a final timer event scores without another LCG call.',
'First LED9 expects RIGHT; a new RIGHT increments num_correct and blanks the LED.|A second move in the same window is ignored.|Holding RIGHT across a round boundary is not a new movement.|A tie, including0:0, ends with LED5.',
'Timer0 and RIT share equal priorities so their state updates cannot preempt one another.|The eleventh timer event gives the tenth value a full3-second interval; it is not an eleventh generated value.',
'Testing a held level counts repeated answers.|Leaving RIT active after the result can erase the victory/defeat LED.',
'Constant work per sample and round; ten sequence values generated.',
'The paper does not assign a miss for no movement; unanswered windows leave both counters unchanged. Centre/select is ignored. Simultaneous direction edges are treated as wrong unless exactly the expected direction is present.10 ms polling latency is not instantaneous hardware response.')
add('2025-07-01_ARM2-Q1',[1],
'uint32_t LCGsequence(uint32_t previous,uint32_t a,uint32_t c,uint32_t s,uint32_t m): R0-R3=previous,a,c,s; entry[SP]=m. Return ((a*previous+c) XOR (previous>>s)) mod m, using a logical shift. Reset_Handler fills DIM10 bytes from seed6,a157,c3,s3,m256.',
'Compute the shifted ORIGINAL previous value before overwriting it with the multiply/add.|XOR, take the unsigned remainder, and use it as the next seed.|Keep the standalone startup result array visible in memory.',
'First:157*6+3=945;6>>3=0;945 mod256=177.|Second:157*177+3=27792;177>>3=22;27792 XOR22=27782;mod256=134.|Bytes:B1 86 21 44 BF 31 16 83 4A 6C.',
'This leaf routine reads the fifth argument at entry SP before any frame is created.|The Q1 reset loop reserves aligned stack-argument space. Q2/Q3 use a function-only assembly file so normal C startup remains available.',
'XORing with the loop index implements ARM1 instead.|Arithmetic right shift is incorrect for an unsigned previous value.',
'Constant work per term;DIM output bytes.',
'm must be nonzero and the tested shift is3. The paper parameters avoid intermediate overflow; a wider-input mathematical generator would require a separate arithmetic contract.')
add('2025-07-01_ARM2-Q2',[1,2],
'Timer1 runs every2500 ms. Generate10 values with LCGsequence(seed6,a157,c3,s3,m256). Remainders0..3 map to LEDs4..7. Supply both C and assembly; an assembly-only answer does not implement this question.',
'Keep previous and the call count between interrupts.|Clear the preceding LED, display4+remainder, and stop Timer1 after call10.|Use the function-only LCG assembly with normal C startup.',
'Expected physical LEDs:5,6,5,4,7,5,6,7,6,4.|Call10 leaves LED4 on; later timer-handler calls do not call the generator.',
'The shift argument stays3 on every call; n is only a count for stopping.|This page now has a dedicated Q2 answer instead of reusing either Q1 assembly or the complete Q3 game.',
'ARM1’s3000 ms period and reversed LED mapping do not apply.|Stopping before displaying the tenth value loses a required output.',
'Ten constant-time generator calls; constant state.')
add('2025-07-01_ARM2-Q3',[2],
'LED4/5/6/7 expects UP/LEFT/RIGHT/DOWN. Count the first response per2500 ms window in hit/miss, clear the LED immediately, and keep the tenth window open for its full duration. Final hit>miss lights LED10; otherwise LED11.',
'Reuse Q2’s generator and open one response window per displayed value.|Poll directional edges, ignoring centre and repeated movement after an answer.|Close the last window, stop Timer1 and RIT, and show the final result without another generator call.',
'First value177 displays LED5; LEFT produces hit1.|A wrong first move increments miss, and a later correct move in that window is ignored.|After ten unanswered windows, hit0=miss0 and LED11 signals defeat.',
'The saved waiting flag prevents post-game RIT activity from erasing the result.|Equal Timer1/RIT priorities serialize score and round transitions. The counters use the paper’s hit/miss names.',
'The previous implementation could still accept movement after displaying the final result.|A correct bit inside a diagonal input should not silently count as a uniquely correct direction.',
'Constant work per poll and round.',
'No movement is not counted as a miss because the paper only increments counters on movement. Centre/select is ignored; multiple new directional edges count as wrong. Physical input latency remains unverified.')

for variant,func,button,order,example in [
    ('ARM1','Look_and_Say','INT0','count then digit','3668999 ->13|26|18|39 ->13261839'),
    ('ARM2','run_length_encoding','KEY1','digit then count','2222779 ->24|72|91 ->247291')]:
    add('2026-02-03_'+variant+'-Q1',[2],
    f'uint32_t {func}(uint32_t digits): R0=input unsigned decimal number,R0=encoded next number. Process consecutive runs from left to right and append {order}. Runs have length<=9, and the paper guarantees the output and intermediate computations fit32 bits.',
    'Extract decimal digits right to left into a local byte buffer.|Walk the buffer backward, accumulating the length of each equal-digit run.|Append two decimal components at each run boundary, then append the final run.',
    example.replace('|',' then ')+'|Input0 is one zero digit: Look_and_Say(0)=10; run_length_encoding(0)=1, the numeric representation of01.|Input111 gives31 in look-and-say and13 in RLE.',
    'The16-byte local buffer holds every digit of uint32_t.|R7 is the current digit,R8 its count,R9 the decimal result. The two multiplication-by10 steps encode the specified component order.',
    'Reversing the whole number loses leading zeros created from trailing zeros.|Counting equal digits globally merges distinct runs.|Forgetting the last append drops the final run.',
    'O(d) for d<=10 digits;48-byte frame including the local buffer.',
    'The look-and-say prose varies capitalization; the answer follows the explicit Look_and_Say prototype. Inputs whose encoded output exceeds32 bits are outside the stated assumptions.')
    result='111213' if variant=='ARM1' else '112131'
    low='6D' if variant=='ARM1' else '03'
    add('2026-02-03_'+variant+'-Q2',[1,3],
    f'ADC produces12 bits. Preview sample>>4 on LEDs with LED4=bit7,LED11=bit0. A debounced {button} passes the latest preview byte to {func} and displays only its low result byte.',
    'ADC_IRQHandler captures completed conversion data; foreground takes a fresh sample and starts the next conversion.|RIT samples button debounce every10 ms, requiring50 ms stable input.|On the confirmed event, use latest_value and replace the preview with the computed result.',
    f'ADC0x7B0 ->preview123.|{button} encodes123 to{result}; low byte0x{low} is displayed.|Held input produces one action, and release/repress permits another.|No conversion yet means no algorithm call.',
    'sample>>4 discards exactly the four least-significant ADC bits.|The result remains visible until the high8 potentiometer value changes, preventing repeated identical conversions from immediately overwriting it.',
    'Masking sample&255 selects the wrong ADC bits.|Reading the displayed result back as the next ADC input mixes two different states.|Raw button edges do not satisfy this paper’s debounce requirement.',
    'Constant IRQ capture work and one short decimal encoding per confirmed press.',
    'The paper specifies no result-hold duration. This implementation holds until the next changed ADC high8 value and consumes a sample before a simultaneous button event. These are explicit display-order choices, not quoted exam rules.')
add('2026-02-03_ARM3-Q1',[2],
'void Recaman(uint32_t *area,uint8_t n): R0=output words,R1=length0..255. Write n terms starting a0=0. For index i>0, use previous-i only if positive and absent from all earlier terms; otherwise use previous+i.',
'Return immediately for length0.|For each new index, test the subtraction candidate against zero and scan the previously written prefix.|Only the subtraction branch checks uniqueness; the addition branch may repeat a value.',
'n8 ->[0,1,3,6,2,7,13,20].|At i4,6-4=2 is positive and unseen, so store2.|At i5,2-5 is negative, so store7.|The longer sequence legitimately contains42 more than once.',
'UXTB enforces the uint8_t length and LSL#2 addresses words.|R6 is the mathematical index i; the linear scan never reads beyond the already initialized prefix.',
'Rejecting repeated sums changes Recamán’s definition.|Allowing a zero subtraction result violates the paper’s positive condition.|Reserving255 bytes is insufficient for255 words.',
'O(n²) searches, n output words,32-byte register frame.')
add('2026-02-03_ARM3-Q2',[1,2],
'ADC high8 supplies length0..255. Debounced KEY2 calls Recaman into a255-word array. Show a0=0 immediately, then subsequent low bytes every2000 ms using Timer0. Playback owns the LEDs while active.',
'Stop/reset the old playback timer and discard its pending foreground event before starting again.|For length0, clear LEDs without reading any array element.|For larger lengths, show index0 now and start the timer only if more elements remain.|Stop after showing the last requested element.',
'ADC0x040 gives length4; KEY2 immediately displays0.|At2 s display1; at4 s display3; at6 s display6 and stop.|Length1 displays only0. A new KEY2 starts a fresh sequence instead of advancing the old one.',
'display_index starts at1 because a0 has already been displayed.|sequence_active prevents ADC preview from overwriting the sequence during timed playback.',
'Waiting2 s before showing a0 violates “immediately”.|Using an8-bit array truncates sequence values before the intended display conversion.',
'Up to255-word generation plus constant timer/event work.',
'After playback, hold the final value until a later changed ADC high8 sample. Timer event flags coalesce if foreground misses multiple intervals; real-time delivery requires board verification.')

for variant,func,definition,first,access in [
    ('ARM1','HofstadterQ','Q(n)=Q(n-Q(n-1))+Q(n-Q(n-2))','1,1,2,3,3,4,5,5','v[i-v[i-1]]+v[i-v[i-2]]'),
    ('ARM2','HofstadterConway','a(n)=a(a(n-1))+a(n-a(n-1))','1,1,2,2,3,4,4,4','v[v[i-1]-1]+v[i-v[i-1]]')]:
    add('2026-02-18_'+variant+'-Q1',[2],
    f'unsigned int {func}(unsigned int *v,int dim): R0=output word array,R1=signed dimension; return the maximum in R0. Terms1 and2 are1. For later terms,{definition}. The caller reserves dim words; Q2 uses1000.',
    'Handle dim<=0 without writing and dim1 without accessing a second word.|Store the initial two1s.|For each zero-based array index i>=2, fetch the already computed terms at the translated indices and update a running maximum.',
    f'First eight terms:[{first}].|dim0 returns0 without touching memory;dim1 returns1 with one word written.|The return is the maximum of the entire prefix, not necessarily its final value.',
    f'The one-based definition becomes {access} at array index i.|LSL#2 scales the word index. R7 tracks the maximum independently from the current term.',
    'Copying the other variant’s recurrence can produce plausible early terms but the wrong sequence.|Subtracting an extra1 from every index double-applies the one-based correction.',
    'O(dim) time and dim output words;32-byte frame.',
    'Nonpositive dimensions return0 as a safe extension. The tested board domain is1000 terms; no unbounded sequence/storage guarantee is implied.')
    add('2026-02-18_'+variant+'-Q2',[2,3],
    f'Compute1000 {func} terms and their maximum. Timer0=A runs every50 ms; Timer1=B streams45 DAC samples periodically; Timer2=C stops/resets once to set note duration. A starts a note only while both B and C are stopped.',
    'Map the next sequence value through threshold=(Pmax-value*(Pmax-Pmin)/maximum)/k, evaluating in floating point before the unsigned cast.|B uses5351,1062,k1; C uses40000000,625000,k5.|Advance the sequence once per new note; stop A after scheduling term1000.|B advances and wraps SinTable; C stops/resets B and silences the DAC.',
    'A value equal to the maximum maps to B=1062 and C=125000 ticks.|While B or C is running, another A event leaves the sequence index unchanged.|B samples start410,467,523 and wrap after353 back to410.|After C ends a note, a stale B event must not write another sample.',
    'sample_index begins44 so increment-before-use starts at SinTable[0].|A’s final-index guard prevents an already-pending interrupt from reading sequence[1000].|C stops B as well as itself; stopping only C would leave sound running.',
    'Integer division before converting to float changes the thresholds.|Using the note duration as a millisecond argument confuses clock ticks with time units.',
    '1000 stored words and45 halfword samples; constant work per timer event after sequence generation.',
    'Floating-point rounding can shift a threshold near an integer boundary. Tests use the implemented single-precision evaluation and the paper’s endpoint formula. Sample deadlines, clock accuracy, audio quality, and simultaneous physical interrupt latency require board verification.')

for variant,func,scratch,method in [
    ('ARM1','BullsAndCows','guessFrequency,secretFrequency','For each unequal position, increment the two per-digit frequency arrays. Then sum min(guessFrequency[d],secretFrequency[d]) across digits0..3.'),
    ('ARM2','Mastermind','usedGuess,usedSecret','Mark exact positions first. For each unmatched guess position, search unused secret positions for one equal digit, mark both used, and break after that one match.')]:
    add('2026-06-25_'+variant+'-Q1',[2] if variant=='ARM1' else [2,3],
    f'int {func}(int guess[4],int secret[4],int {scratch.split(",")[0]}[4],int {scratch.split(",")[1]}[4]): R0-R3 are four array addresses. Digits are0..3; initialize both scratch arrays to zero before EVERY call. Return (((1<<exact)-1)<<4)+((1<<partial)-1).',
    'Count exact same-position matches separately from partial matches.|'+method+'|Pack unary bit masks for the two counts into the high and low nibbles.',
    'guess[0,1,2,3],secret[1,2,2,0] gives exact1,partial2 and result0x13=19.|Four exact matches return0xF0; zero matches return0.|Repeated digits must not be reused: guess[0,0,0,0],secret[0,1,1,1] gives one exact and no partial.',
    ('Frequency indices are digit VALUES, not positions; exclude bulls before updating them.' if variant=='ARM1' else 'Used-array indices are POSITIONS, not digit values; marking each match prevents duplicate use.')+
    '|The standalone Q1 Reset_Handler initializes example inputs and clears scratch before calling the routine. Q2 uses the function-only assembly with C startup.',
    'The superscript in the paper means2 raised to the match count, not2*count.|Reusing nonzero scratch arrays accumulates old matches.|Counting exact matches again as partial overstates the score.',
    'Fixed four-element work;40-byte saved-register frame.',
    'The paper’s unparenthesized shift/add notation is resolved by its worked result19 and four-match display0xF0. Array sizes and digit bounds are preconditions.')
    directions='DOWN,LEFT,RIGHT,UP' if variant=='ARM1' else 'UP,RIGHT,DOWN,LEFT'
    add('2026-06-25_'+variant+'-Q2',[3],
    f'Use Timer1 to capture the secret on the initial SELECT. For digit i,secret[i]=(timer>>(4*i))&3. {directions} increment guess positions0,1,2,3 modulo4. SELECT alternates guess editing and result display; retain the secret across guesses; four exact matches finish.',
    'WAIT_START captures the secret once and clears the guess.|EDIT_GUESS accepts directional input and packs pairs into the LED byte.|SELECT clears scratch, evaluates the guess and shows its packed score.|SHOW_RESULT SELECT begins a new zero guess; FINISHED ignores further input.|Require three stable10 ms joystick samples before accepting a transition.',
    'Timer0x00121AB6 gives secret[2,3,2,1].|Two '+directions.split(',')[0]+' presses make guess[0]=2, lighting LED10 and leaving LED11 off.|A wrong guess followed by SELECT clears the guess but preserves[2,3,2,1].|An exact guess displays0xF0 and ends the game.',
    'guess[0] occupies bits1..0 (LED10/11); guess[3] occupies bits7..6 (LED4/5).|RIT publishes debounced edges; an atomic foreground take clears the event data.|Three stable samples filter bounce as well as suppressing a held direction.',
    'The two game variants use different joystick directions.|Resampling the timer for each guess changes the secret.|Edge detection alone is not mechanical debounce.',
    'Four4-word arrays and constant state; constant work per sample and move.',
    'The paper lets you choose the timer and does not prescribe a debounce interval; this answer uses Timer1 and three stable10 ms samples. Simultaneous SELECT and direction gives SELECT priority. The bitmask handoff can coalesce repeated events if foreground is delayed; physical responsiveness still needs testing.')

if __name__=='__main__':
    maintenance=root/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE'
    guides=maintenance.parent/'01_GUIDES_AND_INDEXES'
    mappings=json.loads((work/'mapping.json').read_text())
    assert len(reviews)==48,(len(reviews),set(m['question']['question_id'] for m in mappings)-reviews.keys())
    for m in mappings:
        q=m['question'];qid=q['question_id'];r=reviews[qid]
        r.update(questionId=qid,paper=m['pdf'],examId=m['exam'])
        r['sources']=[]
        # Resolve updated per-question sources using the same explicit project mapping as the builder.
        source_dir=root/m['sources'][0];base=source_dir.parent
        if base.name in ('Q1','Q2','Q3'):base=base.parent
        if qid=='2025-07-01_ARM2-Q2':
            q['answer_file']=q['answer_file'].replace('/assembly.s','/main.c')+'; '+q['answer_file']
        for name in ['main.c','assembly.s']:
            if (name=='main.c' and '.c' not in q['answer_file']) or (name=='assembly.s' and '.s' not in q['answer_file']):continue
            p=base/q['question']/name
            if not p.exists():p=base/name
            assert p.exists(),p
            r['sources'].append(p.relative_to(root).as_posix())
        for p in sorted((base/q['question']).glob('IRQ_*.c')):r['sources'].append(p.relative_to(root).as_posix())
        # Metadata has one paper-grounded source for contracts and summaries.
        q['argument_mapping']=r['contract']
        q['requirement_summary']=r['method'][0]
        q['constants']=r['contract']
        exports=[]
        for name in r['sources']:
            text=(root/name).read_text(encoding='utf-8-sig')
            exports+=re.findall(r'(?m)^\s*EXPORT\s+(\w+)',text) if name.endswith('.s') else re.findall(r'\bvoid\s+((?:EINT\d|TIMER\d|RIT|ADC)_IRQHandler)\s*\(',text)
        q['function_or_handler']='; '.join(dict.fromkeys(exports)) or 'main'
        # Clear only tags contradicted by reviewed implementations.
        if qid in ('2024-02-12-Q2','2025-01-29_ARM1-Q2'):
            q['peripheral_tags']=q['peripheral_tags'].replace('|Debounce','')
        if qid.startswith('2026-06-25_') and q['question']=='Q2':
            q['peripheral_tags']=q['peripheral_tags'].replace('Timer0','Timer1')
        r['verification']={'sourceReview':'Completed; interpretation and limits listed per question.','instructionExecution':'Not yet run for this revision.','nativeBuild':'Not yet run for this revision.','physicalBoard':'Not tested.'}
    with (guides/'QUESTION_INDEX.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(mappings[0]['question']),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(m['question'] for m in mappings)
    (maintenance/'QUESTION_REVIEWS.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Authored',len(reviews),'paper-specific reviews')
