# Assembly route and cleanup audit

## Result

The active assembly route is complete and internally consistent:

- one README index;
- one 14-lesson assembly course;
- one concise exam-day guide;
- one generated 78-pattern index split into 12 HIGH, 28 CORE and 38
  SUPPLEMENTARY patterns;
- one generated instruction handbook/PDF;
- buildable recipes and exact historical-exam links.

The structural validator confirms 14 lessons and all 78 unique pattern IDs.
The Markdown validator checks every active link and anchor. Active answer,
learning, recipe and solved-exam sources contain no obsolete public
`exam_api`, `exam_user`, `exam_main` or `exam_asm_solution` names.

## Cleanup completed

- Restored the useful assembly README index in the current path instead of
  telling students to use the superseded index.
- Made `START_HERE.md` point directly to the C course, assembly course and
  separate exam-day routes.
- Separated pattern likelihood: exam-derived HIGH, recurring CORE and broader
  SUPPLEMENTARY reference.
- Generated the assembly pattern index from canonical metadata so counts,
  paths and exam mappings do not drift.
- Labeled one-time migration/recovery helpers in the maintenance README so
  they are not mistaken for normal tools.
- Kept historical wrapper-era material outside active navigation.
- Renamed the current 23-answer evidence directory from `API Migration Builds`
  to `Solved Answer Builds` and updated its script, report and index links.

## Material intentionally retained

- `Original two-file migration snapshot` contains 93 evidence files.
- `Superseded Navigation` contains 9 `.legacy` navigation files.
- One-time `migrate-*`, `repair-*` and practice-refresh scripts remain for
  provenance and recovery.
- The generated handbook Markdown remains beside its PDF because algorithm
  pages link to it as the searchable text version.

These items are isolated and do not appear in the normal study route. Deleting
or moving them now would remove provenance or break useful links without
making the exam route simpler.

## Optional cleanup after the current reorganization is committed

1. Move one-time migration helpers into a dedicated historical-tools directory
   after confirming no external workflow calls them.
2. Review the large Git rename/move picture before staging so old-path
   deletions and new current paths are committed together.

None of these optional items affects study, compilation, pattern lookup or the
exam template. There is no critical active-path cleanup left.

## Verification boundary

Compilation, host tests and simulator execution do not replace a physical
LandTiger-board pass for timing, GPIO, debounce, ADC or DAC behavior. That is a
hardware verification task, not a documentation-cleanup defect.
