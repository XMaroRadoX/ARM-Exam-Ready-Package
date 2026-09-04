# Assembly course index

This is the source assembly index for the current `Source/ASM_funct.s` template.
Use the canonical workstation for the current study route.

## Start here

1. Read the guided [Assembly exam course](ASSEMBLY_EXAM_COURSE.md).
2. Keep the [canonical exam workstation](../../../START_HERE.html)
   open while solving a paper.
3. Choose code through the workstation [Solution Patterns](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/patterns/index.html).
4. Use the workstation [Algorithms section](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/algorithms/index.html)
   when you need a complete implementation and test vectors.

## Ordered chapters

| Step | Topic | Read |
|---|---|---|
| 1 | Registers, values, flags and signedness | [Registers, values and flags](registers-values-flags.md) |
| 2 | Functions, parameters, returns and stack frames | [Functions and AAPCS](../03%20-%20Functions%20and%20AAPCS/functions-and-aapcs.md) |
| 3 | Turn the question into a register plan | [Translate C to assembly](../03%20-%20Functions%20and%20AAPCS/translate-c-to-assembly.md) |
| 4 | Loads, stores, arrays and structures | [Memory addressing](../04%20-%20Memory%20and%20Arrays/memory-addressing.md) |
| 5 | Array and pointer loops | [Arrays and loops](../04%20-%20Memory%20and%20Arrays/arrays-and-loops.md) |
| 6 | Row-major and packed matrices | [Matrices](../04%20-%20Memory%20and%20Arrays/matrices.md) |
| 7 | Conditions, signed branches and loop exits | [Conditions and loops](../05%20-%20Control%20Flow/conditions-and-loops.md) |
| 8 | Search, sort, frequency and recurrences | [Algorithm lessons](../06%20-%20Algorithms/recurrences.md) |
| 9 | Graphs, fixed point and wide arithmetic | [Graph patterns](../06%20-%20Algorithms/graphs.md) |
| 10 | SVC, exception frames and exact handlers | [Exceptions and SVC](../07%20-%20Interrupts%20and%20Events/exceptions-and-svc.md) |
| 11 | C/assembly objects and buffers | [Defining and sharing data](../01%20-%20C%20Foundations/defining-data.md) |
| 12 | Register, stack and memory debugging | [Assembly debugging](../09%20-%20Testing%20and%20Debugging/assembly-debugging.md) |

## Buildable examples

- [C calls assembly](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/combinations/c-assembly-many-arguments.html)
- [C and assembly share data](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/combinations/c-assembly-many-arguments.html)
- [Leaf, non-leaf and stacked-argument functions](../../02%20-%20Code%20Recipes/02%20-%20Assembly%20Building%20Blocks/)
- [Arrays and matrices](../../02%20-%20Code%20Recipes/03%20-%20Arrays%20and%20Matrices/)
- [Interrupt and exception routines](../../02%20-%20Code%20Recipes/07%20-%20Interrupts%20and%20Exceptions/)
- [Maximum 78-pattern reference](../../02%20-%20Code%20Recipes/11%20-%20Maximum%20Algorithm%20Reference/README.md)

## Minimum practice before the exam

1. Write and call one leaf function.
2. Write a non-leaf function with a balanced eight-byte-aligned frame.
3. Read a fifth argument after saving registers.
4. Scan signed bytes and unsigned words correctly.
5. Traverse a row-major matrix and a packed bit matrix.
6. Implement a bounded output routine with a capacity check.
7. Debug one deliberate callee-saved-register or stack-offset fault.
8. Solve one high-priority historical pattern without copying its final code.
