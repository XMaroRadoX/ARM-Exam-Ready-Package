
# USB exam package

Start with [exam-navigator.md](exam-navigator.md) for the
step-by-step exam workflow. Use [README.md](README.md)
to locate any other document in the package.

When the exam has begun and you want directions one checkpoint at a time, open
[live-exam-guide.md](live-exam-guide.md).

For the complete 28-pattern audit—C API versus assembly support and every
linked exam question—open
[api-and-pattern-coverage.md](api-and-pattern-coverage.md).

For the single-target Keil view and simulator/board selection, open
[keil-project-guide.md](keil-project-guide.md).

The sibling directory `ARM_Exam_Project` is the only project intended
for copying to the exam working location and for final submission.

## Exam use

1. Copy `ARM_Exam_Project` from the USB drive to the exam working location.
2. Open `ARM_Exam_Template.uvprojx` inside the copied project.
3. Write the requested C answer in `Answer/exam_user.c`.
4. Write the requested assembly answer in `Answer/exam_asm.s`.
5. Change another project file only when the examination paper requires it.
6. Build the `ARM Exam` target and require zero errors and zero warnings.
7. Submit only the copied `ARM_Exam_Project` directory.

Never submit `Study Material` or the surrounding master workspace.

## Private preparation directory

| Directory                      | Contents                                                               |
| ------------------------------ | ---------------------------------------------------------------------- |
| `Exam Atlas and Code Patterns` | Searchable atlas, reusable C/assembly patterns and revision references |
| `Solved Exams`            | Historical answer sources, mappings and adaptation notes               |
| `Tests and Reports`       | Build logs, audits, test evidence and coverage reports                 |
| `Tools`    | Atlas, validation and regression utilities                             |
| `Original and Legacy Archives`        | Backup references and information about preserved originals            |
| `Practice Projects`       | Practice projects used for test and debugging exercises                |

Some older historical answer folders are still identified as incomplete in
`Tests and Reports/FINAL_PROJECT_TEMPLATE_AND_EXAM_AUDIT.md`. A file must
not be treated as a finished solution merely because it exists.
