from pathlib import Path
import json, shutil
R=Path('90_WORKING_PROJECTS/QUESTION_REVIEW_20260908/EXAM_HANDOFF');M=R/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE'
p=M/'QUESTION_REVIEWS.json';d=json.loads(p.read_text(encoding='utf-8'))
r=d['2023-09-18-Q2'];r['findings'].append('Preserved the valid zero-seed case: a zero return is an overflow failure only for a nonzero seed. Zero generates ten zeroes and satisfies the identity.');r['trace'].append('K=0 generates ten zeroes; both sides of the identity are zero, so LED4 signals success.')
d['2025-01-29_ARM1-Q1']['contract']+=' Both b and c are byte values in 0..255.'
d['2024-09-16-Q1']['limitations'].append('Dimensions and backing arrays must be valid, with rows*columns <= 256 so the distinct initial labels fit in one byte. The reviewed button program uses 3x4.')
# Keep the maintained whole-project copies consistent with their question-specific files.
for q in ['2025-02-12_ARM1-Q2','2025-02-12_ARM2-Q2']:
    main=next(R/s for s in d[q]['sources'] if s.endswith('/main.c'))
    for name in ['main.c','IRQ_timer.c']:shutil.copy2(main.parent/name,main.parent.parent/name)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=M/'VERIFY_EXAM_PERIPHERALS.py';s=p.read_text(encoding='utf-8')
s=s.replace('Binary input100110, identity success, generation failure displays LED5 without using unfinished tail','Binary input 100110, identity success including zero seed, generation failure displays LED5 without using unfinished tail')
s=s.replace('Debounce/held select, nibble secret extraction, variant direction mapping, scratch cleared, next guess retains secret; scorer mocked','Debounce/held select, nibble secret extraction, variant direction mapping, scratch cleared, next guess retains secret, SELECT priority and finished state ignores input; scorer mocked')
p.write_text(s,encoding='utf-8')
# The cases have already passed; align their descriptions with the extended fixtures.
p=M/'QUESTION_PERIPHERAL_RESULTS.json';results=json.loads(p.read_text(encoding='utf-8'))
results['2023-09-18-Q2']['cases']=['Binary input 100110, identity success including zero seed, generation failure displays LED5 without using unfinished tail']
results['2024-02-12-Q2']['cases'].append('Timer seed UINT32_MAX produces border row *nn***** using the paper recurrence without intermediate 32-bit overflow.')
for q in ['2026-06-25_ARM1-Q2','2026-06-25_ARM2-Q2']:results[q]['cases'].append('Exact-result 0xF0 enters FINISHED; simultaneous SELECT/direction gives SELECT priority; later joystick input leaves the final display unchanged.')
p.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
# Whole-project sections retain access to all supplied replacement handlers.
p=M/'BUILD_STUDENT_PORTAL.py';s=p.read_text(encoding='utf-8')
marker='        whole_notes = c_path.parent / "README.md" if c_path else None'
assert marker in s
s=s.replace(marker,'''        if c_path:
            companions = ''.join(details_code('Show whole-project ' + p.name, source_code(p), p, destination, 'C') for p in sorted(c_path.parent.glob('IRQ_*.c')))
            body += '<section class="section-block"><h2>Whole-project companion files</h2>' + companions + '<p>Use each question page for the exact template placement steps and evidence applicable to that answer.</p></section>' if companions else ''
'''+marker)
p.write_text(s,encoding='utf-8')
print('Final contract, zero-seed regression, and maintained-copy corrections recorded.')
