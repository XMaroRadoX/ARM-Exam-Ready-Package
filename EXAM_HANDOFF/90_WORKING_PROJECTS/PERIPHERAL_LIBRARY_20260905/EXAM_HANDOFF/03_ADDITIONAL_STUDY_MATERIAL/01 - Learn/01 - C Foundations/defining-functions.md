# Defining functions without linker mistakes

A function needs one definition and may have declarations in every file that
calls it. In the two-file exam project, declarations belong near the top of
`main.c`, while ordinary C
definitions belong in `main.c`, and assembly definitions belong in
`assembly.s` with an `EXPORT` when another file calls them.

Start from the complete paired scenarios:

- [C defines and calls C](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/algorithms/index.html)
- [C calls assembly](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/combinations/c-assembly-many-arguments.html)
- [Assembly calls C](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/combinations/c-assembly-many-arguments.html)

The fastest diagnostic rules are:

- **Undefined symbol:** the name was called or imported but no compiled source
  defined and exported it.
- **Multiply defined symbol:** two compiled sources supplied bodies for the
  same external name.
- **Wrong result without a linker error:** the C prototype and assembly
  register behavior disagree.
- **Return loop or crash after BL:** the caller did not preserve LR or restore
  SP correctly.
