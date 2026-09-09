# Review of all 48 published exam questions

Reviewed September 8, 2026. Each record maps the original paper to maintained sources, the published answer, findings, tests and explicit limitations. The JSON teaching source is QUESTION_REVIEWS.json in 99_MAINTENANCE.

Native SW_Debug builds: 48/48 passed. Independent assembly result records: 48 passed; identical source hashes can support dependent questions. C event-sequence fixtures: 23 passed. No physical-board tests were performed.

The original Kruskal procedure has four nonconvergent valid parameter pairs. The corresponding answers detect failure and report partial results; they do not claim a completed maze. The SDIV64S page records the conflict between the printed V formula and the prose description. The shortest-path page documents the distance-32 encoding limit.

## Reproduce the checks

Run VERIFY_EXAM_ANSWERS.py (ARMASM syntax and LLVM/Unicorn instruction checks), VERIFY_EXAM_PERIPHERALS.py (actual C with explicit mocks), and BUILD_EXAM_REVIEW_PROJECTS.py (native SW_Debug compile/link) from 99_MAINTENANCE. The scripts require the installed toolchains and Python dependencies. Then run question_review.py and REFRESH_QUESTION_REVIEWS.py. Use staging and the portal verifiers before publishing.

Native logs are scenario-native-logs/question-<question id>.log. QUESTION_NATIVE_BUILDS.json records installed source hashes; QUESTION_EXECUTION_RESULTS.json and QUESTION_PERIPHERAL_RESULTS.json record cases and source hashes. These are separate kinds of evidence.

## 2023-02-07-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2023-02-07-q1.html)

Original: [20230207 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/22-23/20230207%20arm.pdf#page=1); pages 1.

**Contract:** void copyData(const int8_t *source, int8_t *destination, uint32_t length): R0=source, R1=destination, R2=byte count. void insertionSort(int8_t *values, uint32_t length): R0=array, R1=count. Both return void. Destination has at least length bytes; sorting changes only that destination.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-02-07_Sort_FreeRunning_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-02-07_Sort_FreeRunning_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Signed byte copy/sort: paper vector, empty, one, duplicates, -128/127; output guard intact
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Separate source and destination regions are assumed; this is not a general overlapping-memory move.

## 2023-02-07-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2023-02-07-q2.html)

Original: [20230207 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/22-23/20230207%20arm.pdf#page=2); pages 2.

**Contract:** Timer1 resets at MR0=0xFF with no match interrupt. Each accepted INT0 interrupt stores its low byte as signed data, up to MAX_VALUES=20. KEY1 sorts the initialized prefix and then lights physical LED11.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-02-07_Sort_FreeRunning_Timer/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-02-07_Sort_FreeRunning_Timer/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-02-07_Sort_FreeRunning_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-02-07_Sort_FreeRunning_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Signed byte copy/sort: paper vector, empty, one, duplicates, -128/127; output guard intact
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Capture signed bytes, LED6/7 alternation, initialized-prefix sort, full buffer ignored
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- One raw external interrupt is treated as one press. Mechanical bounce and sorting latency require board checks; no debounce period is prescribed in this paper.

## 2023-02-24-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2023-02-24-q1.html)

Original: [20230224 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/22-23/20230224%20arm.pdf#page=1); pages 1.

**Contract:** uint32_t KaprekarRoutine(uint32_t a): R0=a on entry, R0=descending_digits(a)-ascending_digits(a) on return. The paper starts with a four-digit unsigned value 1000..9999. This function performs ONE transformation, not the entire sequence.

**Findings:**

- Corrected the index: this function returns one Kaprekar transformation, not an iteration count.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-02-24_Kaprekar_SVC/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-02-24_Kaprekar_SVC/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Kaprekar single transform: paper3075->7173, zero digits, equal digits,291 sampled four-digit inputs
  - SVC50 handler body: constructed MSP frame, five calls, liveR6=5, savedR7 restored; other service ignored (not hardware exception entry)
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- No additional ambiguity within the stated contract.

## 2023-02-24-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2023-02-24-q2.html)

Original: [20230224 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/22-23/20230224%20arm.pdf#page=2); pages 2.

**Contract:** SVC_Handler handles SVC #50. The caller uses MSP. Read its stacked R0, repeatedly call KaprekarRoutine, and leave the number of calls in LIVE R6. The basic hardware frame does not contain R6.

**Findings:**

- Preserved the original R7 before assigning the exception-frame pointer. Corrected the return documentation to live R6.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-02-24_Kaprekar_SVC/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-02-24_Kaprekar_SVC/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Kaprekar single transform: paper3075->7173, zero digits, equal digits,291 sampled four-digit inputs
  - SVC50 handler body: constructed MSP frame, five calls, liveR6=5, savedR7 restored; other service ignored (not hardware exception entry)
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Equal-digit inputs such as 1111 never reach 6174; they are excluded by the convergence condition stated in Q2. This handler follows the specified MSP assumption.

## 2023-05-17-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2023-05-17-q1.html)

Original: [20230517 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/22-23/20230517%20arm.pdf#page=1); pages 1, 2.

**Contract:** int32_t SDIV64(int32_t U, uint32_t L, int32_t D): R0=upper word, R1=lower word, R2=divisor; return quotient in R0. Treat U:L as one signed 64-bit dividend. No multiplication is used.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-05-17_Signed_64_Division/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-05-17_Signed_64_Division/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Signed64/32: signs, low-word carry, zero, INT32 boundary,300 deterministic cases; NZCV follows explicit paper rule and Q is preserved
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- D must be nonzero. The returned signed quotient is meaningful when representable in 32 bits; the paper gives no division-by-zero result or out-of-range quotient policy.

## 2023-05-17-Q2

**Review complete — conflicting paper wording, explicit formula followed.** [Open question](PORTAL/exams/2023-05-17-q2.html)

Original: [20230517 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/22-23/20230517%20arm.pdf#page=3); pages 3.

**Contract:** SDIV64S takes the same U, L, D arguments and returns R0 plus APSR flags: N=result bit 31, Z=(result==0), C=0. This answer follows the paper’s explicit V test: V=0 iff floor(abs(D)/2)>abs(U). Preserve Q and non-NZCV state.

**Findings:**

- Corrected V to use abs(original upper word), as the explicit paper formula requires. Recorded its conflict with the prose definition of signed overflow.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-05-17_Signed_64_Division/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-05-17_Signed_64_Division/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Signed64/32: signs, low-word carry, zero, INT32 boundary,300 deterministic cases; NZCV follows explicit paper rule and Q is preserved
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The paper’s V formula conflicts with its statement that V exactly detects signed-32-bit overflow. The implementation deliberately follows the explicit formula; examples on this page expose the discrepancy rather than hiding it.

## 2023-07-04-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2023-07-04-q1.html)

Original: [20230704 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/22-23/20230704%20arm.pdf#page=1); pages 1.

**Contract:** uint32_t isSociable(uint32_t n): R0=n; return the first cycle length 1..8 that returns to n, or zero. There is no output-array argument. Natural inputs are treated as positive integers.

**Findings:**

- Terminated aliquotSum for inputs 0 and 1. Removed the nonexistent output-array argument from the documentation.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-07-04_Sociable_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-07-04_Sociable_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Sociable:1 termination, prime2, perfect28/8128, amicable220, five-cycle12496, terminating100
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Intermediate sums must fit uint32_t. This answer retains the specified divisor algorithm, so its runtime is not guaranteed to fit a tight interrupt budget for arbitrary large inputs.

## 2023-07-04-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2023-07-04-q2.html)

Original: [20230704 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/22-23/20230704%20arm.pdf#page=2); pages 2.

**Contract:** Timer1 runs every 2000 ms. Its handler cycles through [8128, 5564, 5400, 14264, 1305184, 1598470, 4938136], calls isSociable, and maps results1..8 to physical LEDs 4..11; zero means all off.

**Findings:**

- Uses the corrected sociable routine; the seven-value order and LED mapping are retained.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-07-04_Sociable_Timer/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-07-04_Sociable_Timer/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-07-04_Sociable_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-07-04_Sociable_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Sociable:1 termination, prime2, perfect28/8128, amicable220, five-cycle12496, terminating100
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Seven-value wrap, result1/0 LED mapping, unrelated IRQ ignored; computation stubbed
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The paper explicitly calls the algorithm inside Timer1. Physical runtime and 2-second scheduling are not established by a mocked handler test.

## 2023-09-18-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2023-09-18-q1.html)

Original: [20230918 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/22-23/20230918%20arm.pdf#page=1); pages 1.

**Contract:** uint32_t digitSum(uint32_t a) returns its decimal digit sum. uint32_t digitaddition(uint32_t *area, uint32_t N) fills N words including area[0], then returns the sum of digits of ALL N stored terms. Return zero immediately if generating a term overflows uint32_t. Q1 also requires a 50-word area and a chosen initial value in Reset_Handler.

**Findings:**

- Fixed the sum to include each stored term exactly once, including the final term. Added the required standalone 50-word Reset_Handler example.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-09-18_DigitAddition_Buttons/Answer Source/Q1/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-09-18_DigitAddition_Buttons/Answer%20Source/Q1/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Digit addition:47/5 returns62, one/empty,50 terms, zero, overflow does not store invalid term; guards intact
  - Standalone Reset_Handler executed to its inspection loop: expected result/data and balanced stack; game scratch starts dirty and is cleared before scoring (not hardware reset-vector entry).
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The standalone Q1 startup example chooses47 and reserves50 words. Empty N returns 0 as an explicit safe extension.

## 2023-09-18-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2023-09-18-q2.html)

Original: [20230918 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/22-23/20230918%20arm.pdf#page=2); pages 2.

**Contract:** KEY1 appends binary 0 to K; KEY2 appends1. INT0 sets series[0]=K and requests10 terms. Compare the reported sum with last-first+digitSum(last). Equal: LED4 on/LED5 off; unequal: the reverse.

**Findings:**

- Handles failed generation before reading the final array element. Removed the incorrect K<=50 restriction from the index.
- Preserved the valid zero-seed case: a zero return is an overflow failure only for a nonzero seed. Zero generates ten zeroes and satisfies the identity.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-09-18_DigitAddition_Buttons/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-09-18_DigitAddition_Buttons/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-09-18_DigitAddition_Buttons/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2023-09-18_DigitAddition_Buttons/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Digit addition:47/5 returns62, one/empty,50 terms, zero, overflow does not store invalid term; guards intact
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Binary input 100110, identity success including zero seed, generation failure displays LED5 without using unfinished tail
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Input digits beyond the 32-bit width wrap in the uint32_t accumulator; the paper does not define a wider entry format. Raw-button bounce remains a board limitation.

## 2024-02-12-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2024-02-12-q1.html)

Original: [20240212 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/23-24/20240212%20arm.pdf#page=1); pages 1, 2.

**Contract:** uint32_t mazeSolver(uint32_t rows, uint32_t columns, uint8_t *maze): R0=rows, R1=columns, R2=flat writable bytes. Walls are *, passages are spaces, border exits are lowercase n/e/s/w. Mutate reachable passages into directions; return the number of productive propagation waves.

**Findings:**

- Corrected the index from #/E to the paper’s asterisk, space, and lowercase direction encoding.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-02-12_Maze_LCG_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-02-12_Maze_LCG_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Directional maze: one wave, no exit, multiple exits; independent simultaneous-wave model
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Dimensions, accessible storage, and the guaranteed border encoding are preconditions. Unreachable interior spaces remain spaces.

## 2024-02-12-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2024-02-12-q2.html)

Original: [20240212 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/23-24/20240212%20arm.pdf#page=3); pages 3.

**Contract:** KEY2 samples free-running Timer0, creates a 10x8 maze, then calls mazeSolver inside EINT2_IRQHandler. Generate values with (previous*18) mod 101. Border threshold90; interior passage threshold60. Corners are always * and consume no random value.

**Findings:**

- Reduced the initial timer seed modulo 101 before multiplying by 18, preventing 32-bit overflow from changing the stated recurrence. Corrected multiplier and threshold documentation.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-02-12_Maze_LCG_Timer/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-02-12_Maze_LCG_Timer/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-02-12_Maze_LCG_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-02-12_Maze_LCG_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Directional maze: one wave, no exit, multiple exits; independent simultaneous-wave model
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Original seed300 first row and UINT32_MAX seed modulo regression; solver stubbed
  - Timer seed UINT32_MAX produces border row *nn***** using the paper recurrence without intermediate 32-bit overflow.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Timer sampling supplies a changing seed, not a demonstrated source of statistically true randomness. This is a raw KEY2 handler; no debounce interval is prescribed.

## 2024-02-28-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2024-02-28-q1.html)

Original: [20240228 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/23-24/20240228%20arm.pdf#page=1); pages 1.

**Contract:** uint32_t shortestPath(uint32_t rows, uint32_t columns, uint8_t *maze): walls X, spaces unvisited, entrance e, exit numeric byte0. Fill distance bytes and return the distance k of a cell adjacent to the entrance; the final entrance-to-exit route has k+1 moves.

**Findings:**

- Added termination for an unreachable entrance and for the distance-32/space collision. Both return UINT32_MAX as documented failure extensions.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-02-28_ShortestPath_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-02-28_ShortestPath_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Shortest path: original9x8 returns8 and nine specified LED moves; disconnected entrance returnsUINT32_MAX
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- This byte encoding cannot safely distinguish distance 32 from a space. The implementation reports UINT32_MAX for disconnected mazes or unsupported wave depth32 rather than claiming arbitrary-size maze support. The paper’s supplied maze is within the supported range.

## 2024-02-28-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2024-02-28-q2.html)

Original: [20240228 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/23-24/20240228%20arm.pdf#page=2); pages 2.

**Contract:** Solve the exact 9x8 C maze, then use Timer0 at 500 ms per phase. Right/down/left/up map to LEDs 4/5/6/7. Show each move for 500 ms, then blank for 500 ms. Include the final move into numeric0.

**Findings:**

- Checks solver failure before playback. Corrected the nine-move interpretation of the paper’s returned value 8.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-02-28_ShortestPath_Timer/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-02-28_ShortestPath_Timer/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-02-28_ShortestPath_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-02-28_ShortestPath_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Shortest path: original9x8 returns8 and nine specified LED moves; disconnected entrance returnsUINT32_MAX
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Exact nine-direction LED playback with a blank phase between moves; distance labeling supplied by mock
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Event flags coalesce multiple delayed ticks. Exact wall-clock playback requires foreground work to keep up with 500 ms intervals and needs a board check.

## 2024-07-09-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2024-07-09-q1.html)

Original: [20240709 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/23-24/20240709%20arm.pdf#page=1); pages 1, 2.

**Contract:** void depthFirstSearch(uint8_t *maze, uint32_t rows, uint32_t columns, uint32_t start): R0-R3 in that order. Border bytes are0xFF. Interior bit 0=visited; bits 1/2/3/4=open right/down/left/up. chooseNeighbor receives four visited flags and returns the first unvisited direction 1..4, or 0.

**Findings:**

- Corrected Q1’s index entry to the complete deterministic DFS, not just a randomized neighbor helper.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-07-09_DFS_SysTick/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-07-09_DFS_SysTick/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - DFS: paper6x5 final matrix; all16 visited-flag combinations; five SysTick values per random choice and exact stack-push order
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The start must be an interior cell of a correctly initialized maze; no generic malformed-maze validation is supplied.

## 2024-07-09-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2024-07-09-q2.html)

Original: [20240709 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/23-24/20240709%20arm.pdf#page=3); pages 3.

**Contract:** chooseRandomNeighbor receives the same four flags as chooseNeighbor. Push eligible direction numbers in right/down/left/up order, index that stack by SysTick_VAL mod count, and return 0 if none are eligible. Q2 Reset_Handler sets LOAD=0xFFFFF and starts SysTick without interrupts.

**Findings:**

- Matched literal descending-stack candidate order. Added the required Reset_Handler initialization with LOAD=0xFFFFF and CTRL=5, without enabling SysTick interrupts.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-07-09_DFS_SysTick/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-07-09_DFS_SysTick/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-07-09_DFS_SysTick/Answer Source/Q2/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-07-09_DFS_SysTick/Answer%20Source/Q2/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - DFS: paper6x5 final matrix; all16 visited-flag combinations; five SysTick values per random choice and exact stack-push order
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - C initializes6x5 borders and calls random DFS from7; SysTick startup verified separately in assembly
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The timer-based choice is not a proof of statistical randomness. Keep the original startup vector table and use only one strong Reset_Handler.

## 2024-09-16-Q1

**Review complete — unresolved paper-algorithm limitation.** [Open question](PORTAL/exams/2024-09-16-q1.html)

Original: [20240916 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/23-24/20240916%20arm.pdf#page=1); pages 1, 2, 3.

**Contract:** void kruskal(uint8_t *maze, uint8_t *horizontal, uint8_t *vertical, uint32_t rows, uint32_t columns, uint32_t y, uint32_t x). R0-R3 hold the first four; entry[SP], [SP+4], [SP+8] hold columns, y, x. Each array has rows*columns bytes; cells start with distinct labels 0..N-1.

**Findings:**

- Detected a provably stalled wall-index state and returned partial arrays instead of hanging. Four valid 3x4 parameter pairs remain an explicitly unresolved limitation of the printed algorithm.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-09-16_Kruskal_Buttons/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-09-16_Kruskal_Buttons/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Kruskal: all nine3x4 button pairs: five complete and four explicit partial-maze exits when x>=N,y>=N; arrays match the paper model up to its nonconverging state
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Unresolved paper-algorithm limitation: on the 3x4 maze, (increment, offset)=(2, 2),(3, 2),(3, 3),(3, 4) reach x>=N and y>=N after the vertical subtraction. Subsequent unbounded-arithmetic iterations cannot reach another wall. The other five parameter pairs, with both choices in 2..4, converge.
- The answer now detects that stalled state and returns the partial arrays without changing the required void prototype. Nonzero component labels mean failure, not a completed maze. This is a documented safety extension; it does not invent a replacement Kruskal algorithm.
- Dimensions and backing arrays must be valid, with rows*columns <= 256 so the distinct initial labels fit in one byte. The reviewed button program uses 3x4.

## 2024-09-16-Q2

**Review complete — unresolved paper-algorithm limitation.** [Open question](PORTAL/exams/2024-09-16-q2.html)

Original: [20240916 arm.pdf](../../../02_ORIGINAL_MATERIALS/Exams/23-24/20240916%20arm.pdf#page=4); pages 4.

**Contract:** Initialize a 3x4 maze and wall arrays. The first button chooses increment: INT0=2, KEY1=3, KEY2=4. The second chooses offset with the same mapping and immediately calls kruskal with seven arguments.

**Findings:**

- Reinitializes every new two-button attempt and displays all LEDs on when the returned labels show an incomplete maze.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-09-16_Kruskal_Buttons/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-09-16_Kruskal_Buttons/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-09-16_Kruskal_Buttons/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2024-09-16_Kruskal_Buttons/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Kruskal: all nine3x4 button pairs: five complete and four explicit partial-maze exits when x>=N,y>=N; arrays match the paper model up to its nonconverging state
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Two-button argument order, border markers, distinct starting labels; Kruskal stubbed
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Some valid button pairs expose the printed algorithm’s convergence defect; see Q1. The C answer lights all LEDs if any nonzero component labels remain after the call. This error indication is an implementation extension.
- Starting another two-button attempt reinitializes the maze. Raw-button bounce and physical response still require hardware checks.

## 2025-01-29_ARM1-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-01-29-arm1-q1.html)

Original: [20250129_ARM1.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_01_29/20250129_ARM1.pdf#page=1); pages 1, 2.

**Contract:** uint32_t bitwiseAffineTransformation(const uint8_t *A, uint32_t b, uint32_t c): R0=A, R1=b, R2=c; return d in R0. A contains eight packed row bytes. Row0 produces bit 7; vector bits and row columns run most-significant first. Inputs remain unchanged. Both b and c are byte values in 0..255.

**Findings:**

- Corrected R0/R1 documentation to match the original paper and existing assembly.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-01-29_ARM1_Affine_Two_Timers/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-01-29_ARM1_Affine_Two_Timers/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Affine: all256 input bytes across five matrices including both paper matrices; original exampleC9; input unchanged
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The printed matrix has a mislabeled symbolic entry and repeated final d1 label; follow the explicit byte ordering and worked C9 result.

## 2025-01-29_ARM1-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-01-29-arm1-q2.html)

Original: [20250129_ARM1.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_01_29/20250129_ARM1.pdf#page=3); pages 3.

**Contract:** Timer1 resets at 0xFFFF without IRQ. INT0 XORs bits 15..8 with bits 7..0 and displays the byte. KEY1 uses A=[8F, C7, E3, F1, F8, 7C, 3E, 1F], c=63, and that displayed logical byte; Timer0 toggles every 250 ms for a 500 ms blink cycle.

**Findings:**

- Replaced the reused Q1 matrix with Q2’s distinct matrix. The regression checks E8 -> 56 with c=63.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-01-29_ARM1_Affine_Two_Timers/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-01-29_ARM1_Affine_Two_Timers/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-01-29_ARM1_Affine_Two_Timers/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-01-29_ARM1_Affine_Two_Timers/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Affine: all256 input bytes across five matrices including both paper matrices; original exampleC9; input unchanged
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Low16-bit capture, Q2-specific matrix, expected0x56 and250 ms blink phases
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- During a blink off-phase, KEY1 transforms the stored logical value. The paper does not define repeated-button timing; this interpretation prevents blanking from replacing the input with zero.

## 2025-01-29_ARM2-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-01-29-arm2-q1.html)

Original: [20250129_ARM2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_01_29/20250129_ARM2.pdf#page=1); pages 1, 2, 3.

**Contract:** void bitMatrixMultiplication(const uint8_t *A, const uint8_t *B, uint8_t *C): R0=A, R1=B, R2=C. All are eight row bytes, MSB first. Write C=A*B over GF(2); preserve A and B. Q2’s explicit void prototype governs the return contract.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-01-29_ARM2_Matrix_Two_Timers/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-01-29_ARM2_Matrix_Two_Timers/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - GF2 product: original example, identity/zero and64 deterministic matrix pairs; input and output guards preserved
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- C must not overlap A or B. The source leaves the C pointer in R0 as a convenience, but callers must use the specified output array.

## 2025-01-29_ARM2-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-01-29-arm2-q2.html)

Original: [20250129_ARM2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_01_29/20250129_ARM2.pdf#page=3); pages 3.

**Contract:** INT0 captures exactly eight pairs of bytes from Timer1: high8 into A, low8 into B. Timer1 resets at 0xFFFF with no IRQ. KEY1 before eight captures does nothing; afterward compute C and display its eight rows once for 500 ms each, then blank.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-01-29_ARM2_Matrix_Two_Timers/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-01-29_ARM2_Matrix_Two_Timers/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-01-29_ARM2_Matrix_Two_Timers/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-01-29_ARM2_Matrix_Two_Timers/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - GF2 product: original example, identity/zero and64 deterministic matrix pairs; input and output guards preserved
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Early KEY1, exactly eight captures, rows0..7 once, final blank and stop; product stubbed
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Repeated KEY1 restarts output from row0. The paper does not prescribe a separate reset-to-capture operation.

## 2025-01-29_ARM3-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-01-29-arm3-q1.html)

Original: [20250129_ARM3.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_01_29/20250129_ARM3.pdf#page=1); pages 1.

**Contract:** void transposition(const uint8_t *A, uint8_t *AT): R0=input, R1=output; eight bytes each, MSB-first columns. A is read-only; AT is a distinct writable array. The prior transpose symbol remains an alias for compatibility.

**Findings:**

- Exported the required transposition name while retaining transpose as a compatibility alias.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-01-29_ARM3_Transpose_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-01-29_ARM3_Transpose_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Transpose: exact paper export, zero/all-one/identity and64 random matrices; guards and source preserved
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- No additional ambiguity within the stated contract.

## 2025-01-29_ARM3-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-01-29-arm3-q2.html)

Original: [20250129_ARM3.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_01_29/20250129_ARM3.pdf#page=2); pages 2.

**Contract:** Timer2 resets at 0xFFFF without IRQ. KEY1 fills A and KEY2 fills B, each with eight low timer bytes; further presses are ignored. INT0 calls transposition three times to compare transpose(A XOR B) with transpose(A) XOR transpose(B). Success lights LED4; failure LED5.

**Findings:**

- Calls the paper’s transposition interface.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-01-29_ARM3_Transpose_Timer/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-01-29_ARM3_Transpose_Timer/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-01-29_ARM3_Transpose_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-01-29_ARM3_Transpose_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Transpose: exact paper export, zero/all-one/identity and64 random matrices; guards and source preserved
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Independent capture counts, three transposition calls, XOR identity, full-buffer guards
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- INT0 before both arrays are filled is ignored as a safe completion policy; the paper does not specify how partial input should be handled.

## 2025-02-12_ARM1-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-02-12-arm1-q1.html)

Original: [20250212_ARM1.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_02_12/20250212_ARM1.pdf#page=2); pages 2.

**Contract:** int32_t Maclaurin(int32_t y, uint32_t n): R0=y, R1=maximum order n; R0=scaled approximation. y represents10*x and the output approximates100*sin(x). Include terms 0 through n.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-02-12_ARM1_Sine_DAC/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-02-12_ARM1_Sine_DAC/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Maclaurin: signed truncated recurrence, paper example, y=-31..31 at orders0..4
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The sine notation in the paper reuses y inconsistently; follow its y=10*x definition and worked recurrence.
- The claimed absence of overflow is not a guarantee for arbitrary int32_t y and order. Tests cover the paper examples and waveform domain y=-31..31, n3; wider inputs require separate bounds analysis.

## 2025-02-12_ARM1-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-02-12-arm1-q2.html)

Original: [20250212_ARM1.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_02_12/20250212_ARM1.pdf#page=3); pages 3.

**Contract:** INT0 starts Timer0 once, with match threshold1263 timer clock ticks. IRQ_timer.c contains int sineValues[45] and the timer handler. Start ticks=0, repeat=0; after ticks 22, wrap to-22 and increment repeat. End when repeat reaches200.

**Findings:**

- Placed the required global int sineValues array and waveform handler in a complete IRQ_timer.c replacement.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-02-12_ARM1_Sine_DAC/Answer Source/Q2/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-02-12_ARM1_Sine_DAC/Answer%20Source/Q2/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-02-12_ARM1_Sine_DAC/Answer Source/Q2/IRQ_timer.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-02-12_ARM1_Sine_DAC/Answer%20Source/Q2/IRQ_timer.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-02-12_ARM1_Sine_DAC/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-02-12_ARM1_Sine_DAC/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Maclaurin: signed truncated recurrence, paper example, y=-31..31 at orders0..4
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - 8978 samples from initial half-cycle, order3, output array populated, completion silence, repeated button ignored; recurrence stubbed
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- No repeated-button handling or debounce is required here. Native compilation does not establish that floating-point emulation and the IRQ body meet the actual sample deadline.

## 2025-02-12_ARM2-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-02-12-arm2-q1.html)

Original: [20250212_ARM2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_02_12/20250212_ARM2.pdf#page=2); pages 2.

**Contract:** int32_t Maclaurin_cos(int32_t y, uint32_t n): R0=y, R1=maximum order n; R0=scaled approximation. y represents10*x and the output approximates100*cos(x). Include terms 0 through n.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-02-12_ARM2_Cosine_DAC/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-02-12_ARM2_Cosine_DAC/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Maclaurin: signed truncated recurrence, paper example, y=-31..31 at orders0..4
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The cosine example’s last numerator/denominator line has typographical errors. The stated recurrence gives 20625/5600=3 and the printed final sum-80.
- The claimed absence of overflow is not a guarantee for arbitrary int32_t y and order. Tests cover the paper examples and waveform domain y=-31..31, n3; wider inputs require separate bounds analysis.

## 2025-02-12_ARM2-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-02-12-arm2-q2.html)

Original: [20250212_ARM2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_02_12/20250212_ARM2.pdf#page=3); pages 3.

**Contract:** KEY1 starts Timer1 once, with match threshold1592 timer clock ticks. IRQ_timer.c contains int cosineValues[45] and the timer handler. Start ticks=0, repeat=0; after ticks 22, wrap to-22 and increment repeat. End when repeat reaches200.

**Findings:**

- Placed the required global int cosineValues array and waveform handler in a complete IRQ_timer.c replacement.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-02-12_ARM2_Cosine_DAC/Answer Source/Q2/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-02-12_ARM2_Cosine_DAC/Answer%20Source/Q2/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-02-12_ARM2_Cosine_DAC/Answer Source/Q2/IRQ_timer.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-02-12_ARM2_Cosine_DAC/Answer%20Source/Q2/IRQ_timer.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-02-12_ARM2_Cosine_DAC/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-02-12_ARM2_Cosine_DAC/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Maclaurin: signed truncated recurrence, paper example, y=-31..31 at orders0..4
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - 8978 samples from initial half-cycle, order3, output array populated, completion silence, repeated button ignored; recurrence stubbed
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The cosine pseudocode is missing a closing brace; the answer follows the matching sine structure and its repeat<200 guard.
- No repeated-button handling or debounce is required here. Native compilation does not establish that floating-point emulation and the IRQ body meet the actual sample deadline.

## 2025-07-01_ARM1-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-07-01-arm1-q1.html)

Original: [20250701.pdf](../../../02_ORIGINAL_MATERIALS/Exams/ARM%20questions/20250701.pdf#page=1); pages 1.

**Contract:** uint32_t nextElementLCG(uint32_t previous, uint32_t a, uint32_t c, uint32_t n, uint32_t m): R0-R3=previous, a, c, n; entry[SP]=m. Return ((a*previous+c) XOR n) mod m. The standalone Reset_Handler fills DIM 10 bytes from seed 1, a 131, c7, m255.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source/Q1/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM1_LCG_Rhythm/Answer%20Source/Q1/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - LCG: all ten paper sequence values and fifth stack argument
  - Standalone Reset_Handler executed to its inspection loop: expected result/data and balanced stack; game scratch starts dirty and is cleared before scoring (not hardware reset-vector entry).
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- m must be nonzero. The paper’s parameters keep products in range; the routine otherwise uses32-bit machine arithmetic.

## 2025-07-01_ARM1-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-07-01-arm1-q2.html)

Original: [20250701.pdf](../../../02_ORIGINAL_MATERIALS/Exams/ARM%20questions/20250701.pdf#page=1); pages 1, 2.

**Contract:** Timer0 fires every 3000 ms and calls nextElementLCG exactly10 times using the Q1 constants. Map remainder0/1/2/3 to physical LEDs 11/10/9/8, with exactly one LED on. Q2 leaves the final LED lit.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source/Q2/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM1_LCG_Rhythm/Answer%20Source/Q2/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source/Q2/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM1_LCG_Rhythm/Answer%20Source/Q2/assembly.s)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source/Q2/IRQ_timer.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM1_LCG_Rhythm/Answer%20Source/Q2/IRQ_timer.c)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - LCG: all ten paper sequence values and fifth stack argument
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - All ten paper LED values, correct timer period, exact call count and stop
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- No additional ambiguity within the stated contract.

## 2025-07-01_ARM1-Q3

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-07-01-arm1-q3.html)

Original: [20250701.pdf](../../../02_ORIGINAL_MATERIALS/Exams/ARM%20questions/20250701.pdf#page=2); pages 2.

**Contract:** Extend Q2 with one directional joystick answer per round. LEDs 11/10/9/8 mean UP/LEFT/RIGHT/DOWN. First movement increments num_correct or num_wrong and immediately clears the LED. After the tenth full response window, win on num_correct>num_wrong: LED4; otherwise LED5.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source/Q3/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM1_LCG_Rhythm/Answer%20Source/Q3/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source/Q3/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM1_LCG_Rhythm/Answer%20Source/Q3/assembly.s)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source/Q3/IRQ_RIT.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM1_LCG_Rhythm/Answer%20Source/Q3/IRQ_RIT.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source/Q3/IRQ_timer.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM1_LCG_Rhythm/Answer%20Source/Q3/IRQ_timer.c)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - LCG: all ten paper sequence values and fifth stack argument
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - First response only, nine wrong rounds, tenth full window, final score and post-game input ignored
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The paper does not assign a miss for no movement; unanswered windows leave both counters unchanged. Centre/select is ignored. Simultaneous direction edges are treated as wrong unless exactly the expected direction is present.10 ms polling latency is not instantaneous hardware response.

## 2025-07-01_ARM2-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-07-01-arm2-q1.html)

Original: [ARM2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_07_01/ARM2.pdf#page=1); pages 1.

**Contract:** uint32_t LCGsequence(uint32_t previous, uint32_t a, uint32_t c, uint32_t s, uint32_t m): R0-R3=previous, a, c, s; entry[SP]=m. Return ((a*previous+c) XOR (previous>>s)) mod m, using a logical shift. Reset_Handler fills DIM 10 bytes from seed 6, a 157, c3, s3, m256.

**Findings:**

- Separated the standalone 10-byte Reset_Handler example from the callable routine used by the C questions. Removed the incorrect 256-element claim.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM2_LCG_Rhythm/Answer Source/Q1/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM2_LCG_Rhythm/Answer%20Source/Q1/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - LCG: all ten paper sequence values and fifth stack argument
  - Standalone Reset_Handler executed to its inspection loop: expected result/data and balanced stack; game scratch starts dirty and is cleared before scoring (not hardware reset-vector entry).
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- m must be nonzero and the tested shift is3. The paper parameters avoid intermediate overflow; a wider-input mathematical generator would require a separate arithmetic contract.

## 2025-07-01_ARM2-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-07-01-arm2-q2.html)

Original: [ARM2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_07_01/ARM2.pdf#page=1); pages 1, 2.

**Contract:** Timer1 runs every 2500 ms. Generate10 values with LCGsequence(seed 6, a 157, c3, s3, m256). Remainders0..3 map to LEDs 4..7. Supply both C and assembly; an assembly-only answer does not implement this question.

**Findings:**

- Supplied the missing timer-driven C answer using Timer1, 2500 ms, ten calls, and physical LEDs 4..7.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM2_LCG_Rhythm/Answer Source/Q2/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM2_LCG_Rhythm/Answer%20Source/Q2/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM2_LCG_Rhythm/Answer Source/Q2/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM2_LCG_Rhythm/Answer%20Source/Q2/assembly.s)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM2_LCG_Rhythm/Answer Source/Q2/IRQ_timer.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM2_LCG_Rhythm/Answer%20Source/Q2/IRQ_timer.c)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - LCG: all ten paper sequence values and fifth stack argument
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - All ten paper LED values, correct timer period, exact call count and stop
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- No additional ambiguity within the stated contract.

## 2025-07-01_ARM2-Q3

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2025-07-01-arm2-q3.html)

Original: [ARM2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/24-25/2025_07_01/ARM2.pdf#page=2); pages 2.

**Contract:** LED4/5/6/7 expects UP/LEFT/RIGHT/DOWN. Count the first response per2500 ms window in hit/miss, clear the LED immediately, and keep the tenth window open for its full duration. Final hit>miss lights LED10; otherwise LED11.

**Findings:**

- Corrected first-response ownership, ignored select, retained the full tenth window, stopped RIT at completion, and used equal timer/RIT priorities for shared state.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM2_LCG_Rhythm/Answer Source/Q3/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM2_LCG_Rhythm/Answer%20Source/Q3/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM2_LCG_Rhythm/Answer Source/Q3/IRQ_RIT.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM2_LCG_Rhythm/Answer%20Source/Q3/IRQ_RIT.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM2_LCG_Rhythm/Answer Source/Q3/IRQ_timer.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM2_LCG_Rhythm/Answer%20Source/Q3/IRQ_timer.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM2_LCG_Rhythm/Answer Source/Q3/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2025-07-01_ARM2_LCG_Rhythm/Answer%20Source/Q3/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - LCG: all ten paper sequence values and fifth stack argument
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - First response only, nine wrong rounds, tenth full window, final score and post-game input ignored
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- No movement is not counted as a miss because the paper only increments counters on movement. Centre/select is ignored; multiple new directional edges count as wrong. Physical input latency remains unverified.

## 2026-02-03_ARM1-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-02-03-arm1-q1.html)

Original: [20260203_ARM_1.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2003.02.2026/20260203_ARM_1.pdf#page=2); pages 2.

**Contract:** uint32_t Look_and_Say(uint32_t digits): R0=input unsigned decimal number, R0=encoded next number. Process consecutive runs from left to right and append count then digit. Runs have length<=9, and the paper guarantees the output and intermediate computations fit32 bits.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-03_ARM1_LookAndSay_ADC/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-03_ARM1_LookAndSay_ADC/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Decimal runs: paper examples,0, trailing/internal zeros, repeated run and all256 ADC inputs
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The look-and-say prose varies capitalization; the answer follows the explicit Look_and_Say prototype. Inputs whose encoded output exceeds32 bits are outside the stated assumptions.

## 2026-02-03_ARM1-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-02-03-arm1-q2.html)

Original: [20260203_ARM_1.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2003.02.2026/20260203_ARM_1.pdf#page=1); pages 1, 3.

**Contract:** ADC produces12 bits. Preview sample>>4 on LEDs with LED4=bit 7, LED11=bit 0. A debounced INT0 passes the latest preview byte to Look_and_Say and displays only its low result byte.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-03_ARM1_LookAndSay_ADC/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-03_ARM1_LookAndSay_ADC/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-03_ARM1_LookAndSay_ADC/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-03_ARM1_LookAndSay_ADC/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Decimal runs: paper examples,0, trailing/internal zeros, repeated run and all256 ADC inputs
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Fresh ADC high8, no pre-sample call, confirmed-button routing, low-byte result and hold-until-change; debounce API mocked
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The paper specifies no result-hold duration. This implementation holds until the next changed ADC high8 value and consumes a sample before a simultaneous button event. These are explicit display-order choices, not quoted exam rules.

## 2026-02-03_ARM2-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-02-03-arm2-q1.html)

Original: [20260203_ARM_2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2003.02.2026/20260203_ARM_2.pdf#page=2); pages 2.

**Contract:** uint32_t run_length_encoding(uint32_t digits): R0=input unsigned decimal number, R0=encoded next number. Process consecutive runs from left to right and append digit then count. Runs have length<=9, and the paper guarantees the output and intermediate computations fit32 bits.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-03_ARM2_RLE_ADC/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-03_ARM2_RLE_ADC/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Decimal runs: paper examples,0, trailing/internal zeros, repeated run and all256 ADC inputs
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Inputs whose encoded output exceeds 32 bits are outside the stated assumptions. Leading zeroes are represented numerically, so encoding the single digit 0 yields 1 (the numeric value of 01).

## 2026-02-03_ARM2-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-02-03-arm2-q2.html)

Original: [20260203_ARM_2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2003.02.2026/20260203_ARM_2.pdf#page=1); pages 1, 3.

**Contract:** ADC produces12 bits. Preview sample>>4 on LEDs with LED4=bit 7, LED11=bit 0. A debounced KEY1 passes the latest preview byte to run_length_encoding and displays only its low result byte.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-03_ARM2_RLE_ADC/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-03_ARM2_RLE_ADC/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-03_ARM2_RLE_ADC/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-03_ARM2_RLE_ADC/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Decimal runs: paper examples,0, trailing/internal zeros, repeated run and all256 ADC inputs
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Fresh ADC high8, no pre-sample call, confirmed-button routing, low-byte result and hold-until-change; debounce API mocked
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The paper specifies no result-hold duration. This implementation holds until the next changed ADC high8 value and consumes a sample before a simultaneous button event. These are explicit display-order choices, not quoted exam rules.

## 2026-02-03_ARM3-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-02-03-arm3-q1.html)

Original: [20260203_ARM_3.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2003.02.2026/20260203_ARM_3.pdf#page=2); pages 2.

**Contract:** void Recaman(uint32_t *area, uint8_t n): R0=output words, R1=length 0..255. Write n terms starting a 0=0. For index i>0, use previous-i only if positive and absent from all earlier terms; otherwise use previous+i.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-03_ARM3_Recaman_ADC_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-03_ARM3_Recaman_ADC_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Recaman: lengths0,1,2,8,25,255; independent sequence including repeated addition values; output guard intact
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- No additional ambiguity within the stated contract.

## 2026-02-03_ARM3-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-02-03-arm3-q2.html)

Original: [20260203_ARM_3.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2003.02.2026/20260203_ARM_3.pdf#page=1); pages 1, 2.

**Contract:** ADC high8 supplies length 0..255. Debounced KEY2 calls Recaman into a 255-word array. Show a 0=0 immediately, then subsequent low bytes every 2000 ms using Timer0. Playback owns the LEDs while active.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-03_ARM3_Recaman_ADC_Timer/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-03_ARM3_Recaman_ADC_Timer/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-03_ARM3_Recaman_ADC_Timer/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-03_ARM3_Recaman_ADC_Timer/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Recaman: lengths0,1,2,8,25,255; independent sequence including repeated addition values; output guard intact
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Immediate a0,2-second playback through final element, zero-length no read; sequence mocked
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- After playback, hold the final value until a later changed ADC high8 sample. Timer event flags coalesce if foreground misses multiple intervals; real-time delivery requires board verification.

## 2026-02-18_ARM1-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-02-18-arm1-q1.html)

Original: [20260218_ARM_1.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2018.02.2026/20260218_ARM_1.pdf#page=2); pages 2.

**Contract:** unsigned int HofstadterQ(unsigned int *v, int dim): R0=output word array, R1=signed dimension; return the maximum in R0. Terms 1 and 2 are1. For later terms, Q(n)=Q(n-Q(n-1))+Q(n-Q(n-2)). The caller reserves dim words; Q2 uses1000.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-18_ARM1_Three_Timers/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-18_ARM1_Three_Timers/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Hofstadter: signed dimensions-1,0,1,2,8,1000; independent one-based recurrence and prefix maximum; output guard intact
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Nonpositive dimensions return 0 as a safe extension. The tested board domain is1000 terms; no unbounded sequence/storage guarantee is implied.

## 2026-02-18_ARM1-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-02-18-arm1-q2.html)

Original: [20260218_ARM_1.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2018.02.2026/20260218_ARM_1.pdf#page=2); pages 2, 3.

**Contract:** Compute1000 HofstadterQ terms and their maximum. Timer0=A runs every 50 ms; Timer1=B streams45 DAC samples periodically; Timer2=C stops/resets once to set note duration. A starts a note only while both B and C are stopped.

**Findings:**

- Guarded the final sequence index and ignored a stale Timer1 event after the duration timer has stopped playback.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-18_ARM1_Three_Timers/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-18_ARM1_Three_Timers/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-18_ARM1_Three_Timers/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-18_ARM1_Three_Timers/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Hofstadter: signed dimensions-1,0,1,2,8,1000; independent one-based recurrence and prefix maximum; output guard intact
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Threshold endpoints, B/C active guard, sine sample order, stop/silence, stale B and final A interrupts; sequence mocked
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Floating-point rounding can shift a threshold near an integer boundary. Tests use the implemented single-precision evaluation and the paper’s endpoint formula. Sample deadlines, clock accuracy, audio quality, and simultaneous physical interrupt latency require board verification.

## 2026-02-18_ARM2-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-02-18-arm2-q1.html)

Original: [20260218_ARM_2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2018.02.2026/20260218_ARM_2.pdf#page=2); pages 2.

**Contract:** unsigned int HofstadterConway(unsigned int *v, int dim): R0=output word array, R1=signed dimension; return the maximum in R0. Terms 1 and 2 are1. For later terms, a(n)=a(a(n-1))+a(n-a(n-1)). The caller reserves dim words; Q2 uses1000.

**Findings:**

- Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-18_ARM2_Three_Timers/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-18_ARM2_Three_Timers/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Hofstadter: signed dimensions-1,0,1,2,8,1000; independent one-based recurrence and prefix maximum; output guard intact
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Nonpositive dimensions return 0 as a safe extension. The tested board domain is1000 terms; no unbounded sequence/storage guarantee is implied.

## 2026-02-18_ARM2-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-02-18-arm2-q2.html)

Original: [20260218_ARM_2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2018.02.2026/20260218_ARM_2.pdf#page=2); pages 2, 3.

**Contract:** Compute1000 HofstadterConway terms and their maximum. Timer0=A runs every 50 ms; Timer1=B streams45 DAC samples periodically; Timer2=C stops/resets once to set note duration. A starts a note only while both B and C are stopped.

**Findings:**

- Guarded the final sequence index and ignored a stale Timer1 event after the duration timer has stopped playback.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-18_ARM2_Three_Timers/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-18_ARM2_Three_Timers/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-02-18_ARM2_Three_Timers/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-02-18_ARM2_Three_Timers/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Hofstadter: signed dimensions-1,0,1,2,8,1000; independent one-based recurrence and prefix maximum; output guard intact
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Threshold endpoints, B/C active guard, sine sample order, stop/silence, stale B and final A interrupts; sequence mocked
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- Floating-point rounding can shift a threshold near an integer boundary. Tests use the implemented single-precision evaluation and the paper’s endpoint formula. Sample deadlines, clock accuracy, audio quality, and simultaneous physical interrupt latency require board verification.

## 2026-06-25_ARM1-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-06-25-arm1-q1.html)

Original: [20260625_ARM_1.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2025.06.2206/20260625_ARM_1.pdf#page=2); pages 2.

**Contract:** int BullsAndCows(int guess[4], int secret[4], int guessFrequency[4], int secretFrequency[4]): R0-R3 are four array addresses. Digits are0..3; initialize both scratch arrays to zero before EVERY call. Return (((1<<exact)-1)<<4)+((1<<partial)-1).

**Findings:**

- Added the required standalone Reset_Handler scoring example with zeroed scratch arrays.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-06-25_ARM1_BullsAndCows/Answer Source/Q1/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-06-25_ARM1_BullsAndCows/Answer%20Source/Q1/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Game scoring: paper example, all256 exact codes,2048 deterministic duplicate-heavy pairs; scratch effects and unchanged inputs checked
  - Standalone Reset_Handler executed to its inspection loop: expected result/data and balanced stack; game scratch starts dirty and is cleared before scoring (not hardware reset-vector entry).
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The paper’s unparenthesized shift/add notation is resolved by its worked result 19 and four-match display0xF0. Array sizes and digit bounds are preconditions.

## 2026-06-25_ARM1-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-06-25-arm1-q2.html)

Original: [20260625_ARM_1.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2025.06.2206/20260625_ARM_1.pdf#page=3); pages 3.

**Contract:** Use Timer1 to capture the secret on the initial SELECT. For digit i, secret[i]=(timer>>(4*i))&3. DOWN, LEFT, RIGHT, UP increment guess positions0, 1, 2, 3 modulo4. SELECT alternates guess editing and result display; retain the secret across guesses; four exact matches finish.

**Findings:**

- Added three stable 10 ms samples before accepting joystick changes; a raw edge alone did not debounce input.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-06-25_ARM1_BullsAndCows/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-06-25_ARM1_BullsAndCows/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-06-25_ARM1_BullsAndCows/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-06-25_ARM1_BullsAndCows/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Game scoring: paper example, all256 exact codes,2048 deterministic duplicate-heavy pairs; scratch effects and unchanged inputs checked
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Debounce/held select, nibble secret extraction, variant direction mapping, scratch cleared, next guess retains secret; scorer mocked
  - Exact-result 0xF0 enters FINISHED; simultaneous SELECT/direction gives SELECT priority; later joystick input leaves the final display unchanged.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The paper lets you choose the timer and does not prescribe a debounce interval; this answer uses Timer1 and three stable10 ms samples. Simultaneous SELECT and direction gives SELECT priority. The bitmask handoff can coalesce repeated events if foreground is delayed; physical responsiveness still needs testing.

## 2026-06-25_ARM2-Q1

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-06-25-arm2-q1.html)

Original: [20260625_ARM_2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2025.06.2206/20260625_ARM_2.pdf#page=2); pages 2, 3.

**Contract:** int Mastermind(int guess[4], int secret[4], int usedGuess[4], int usedSecret[4]): R0-R3 are four array addresses. Digits are0..3; initialize both scratch arrays to zero before EVERY call. Return (((1<<exact)-1)<<4)+((1<<partial)-1).

**Findings:**

- Added the required standalone Reset_Handler scoring example with zeroed scratch arrays.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-06-25_ARM2_Mastermind/Answer Source/Q1/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-06-25_ARM2_Mastermind/Answer%20Source/Q1/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Game scoring: paper example, all256 exact codes,2048 deterministic duplicate-heavy pairs; scratch effects and unchanged inputs checked
  - Standalone Reset_Handler executed to its inspection loop: expected result/data and balanced stack; game scratch starts dirty and is cleared before scoring (not hardware reset-vector entry).
- peripheralExecution: NOT APPLICABLE. This question has no C peripheral answer.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The paper’s unparenthesized shift/add notation is resolved by its worked result 19 and four-match display0xF0. Array sizes and digit bounds are preconditions.

## 2026-06-25_ARM2-Q2

**Review complete within the stated contract and limitations.** [Open question](PORTAL/exams/2026-06-25-arm2-q2.html)

Original: [20260625_ARM_2.pdf](../../../02_ORIGINAL_MATERIALS/Exams/Exam%2025.06.2206/20260625_ARM_2.pdf#page=3); pages 3.

**Contract:** Use Timer1 to capture the secret on the initial SELECT. For digit i, secret[i]=(timer>>(4*i))&3. UP, RIGHT, DOWN, LEFT increment guess positions0, 1, 2, 3 modulo4. SELECT alternates guess editing and result display; retain the secret across guesses; four exact matches finish.

**Findings:**

- Added three stable 10 ms samples before accepting joystick changes; a raw edge alone did not debounce input.

**Maintained answer files:**

- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-06-25_ARM2_Mastermind/Answer Source/main.c](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-06-25_ARM2_Mastermind/Answer%20Source/main.c)
- [03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2026-06-25_ARM2_Mastermind/Answer Source/assembly.s](../../../03_ADDITIONAL_STUDY_MATERIAL/03%20-%20Solved%20Exams/2026-06-25_ARM2_Mastermind/Answer%20Source/assembly.s)

**Evidence:**

- sourceReview: COMPLETE. Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.
- instructionExecution: PASS. Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.
  - Game scoring: paper example, all256 exact codes,2048 deterministic duplicate-heavy pairs; scratch effects and unchanged inputs checked
- peripheralExecution: PASS. Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim. The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.
  - Debounce/held select, nibble secret extraction, variant direction mapping, scratch cleared, next guess retains secret; scorer mocked
  - Exact-result 0xF0 enters FINISHED; simultaneous SELECT/direction gives SELECT priority; later joystick input leaves the final display unchanged.
- nativeBuild: PASS. Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.
- physicalBoard: UNVERIFIED. No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.

**Limitations:**

- The paper lets you choose the timer and does not prescribe a debounce interval; this answer uses Timer1 and three stable10 ms samples. Simultaneous SELECT and direction gives SELECT priority. The bitmask handoff can coalesce repeated events if foreground is delayed; physical responsiveness still needs testing.
