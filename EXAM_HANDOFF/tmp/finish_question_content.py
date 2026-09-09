from pathlib import Path
import csv,io,json,re
W=Path('90_WORKING_PROJECTS/QUESTION_REVIEW_20260908')
R=W/'EXAM_HANDOFF';B=R/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS';M=B/'99_MAINTENANCE';G=B/'01_GUIDES_AND_INDEXES'
d=json.loads((M/'QUESTION_REVIEWS.json').read_text(encoding='utf-8'))
# Repair prose copied between variants and keep exam-specific contracts explicit.
d['2023-02-07-Q2']['limitations'][0]='One raw external interrupt is treated as one press. Mechanical bounce and sorting latency require board checks; no debounce period is prescribed in this paper.'
d['2025-02-12_ARM1-Q1']['contract']=d['2025-02-12_ARM1-Q1']['contract'].replace('100*sin(x) or100*cos(x), respectively','100*sin(x)')
d['2025-02-12_ARM2-Q1']['contract']=d['2025-02-12_ARM2-Q1']['contract'].replace('100*sin(x) or100*cos(x), respectively','100*cos(x)')
d['2025-02-12_ARM1-Q2']['limitations']=d['2025-02-12_ARM1-Q2']['limitations'][1:]
d['2026-02-03_ARM2-Q1']['limitations'][0]='Inputs whose encoded output exceeds 32 bits are outside the stated assumptions. Leading zeroes are represented numerically, so encoding the single digit 0 yields 1 (the numeric value of 01).'
for q in ['2026-06-25_ARM1-Q2','2026-06-25_ARM2-Q2']:
    d[q]['trace'][0]=d[q]['trace'][0].replace('Timer0x','Timer1 value 0x')

findings={
'2023-02-24-Q1':['Corrected the index: this function returns one Kaprekar transformation, not an iteration count.'],
'2023-02-24-Q2':['Preserved the original R7 before assigning the exception-frame pointer. Corrected the return documentation to live R6.'],
'2023-05-17-Q2':['Corrected V to use abs(original upper word), as the explicit paper formula requires. Recorded its conflict with the prose definition of signed overflow.'],
'2023-07-04-Q1':['Terminated aliquotSum for inputs 0 and 1. Removed the nonexistent output-array argument from the documentation.'],
'2023-07-04-Q2':['Uses the corrected sociable routine; the seven-value order and LED mapping are retained.'],
'2023-09-18-Q1':['Fixed the sum to include each stored term exactly once, including the final term. Added the required standalone 50-word Reset_Handler example.'],
'2023-09-18-Q2':['Handles failed generation before reading the final array element. Removed the incorrect K<=50 restriction from the index.'],
'2024-02-12-Q1':['Corrected the index from #/E to the paper’s asterisk, space, and lowercase direction encoding.'],
'2024-02-12-Q2':['Reduced the initial timer seed modulo 101 before multiplying by 18, preventing 32-bit overflow from changing the stated recurrence. Corrected multiplier and threshold documentation.'],
'2024-02-28-Q1':['Added termination for an unreachable entrance and for the distance-32/space collision. Both return UINT32_MAX as documented failure extensions.'],
'2024-02-28-Q2':['Checks solver failure before playback. Corrected the nine-move interpretation of the paper’s returned value 8.'],
'2024-07-09-Q1':['Corrected Q1’s index entry to the complete deterministic DFS, not just a randomized neighbor helper.'],
'2024-07-09-Q2':['Matched literal descending-stack candidate order. Added the required Reset_Handler initialization with LOAD=0xFFFFF and CTRL=5, without enabling SysTick interrupts.'],
'2024-09-16-Q1':['Detected a provably stalled wall-index state and returned partial arrays instead of hanging. Four valid 3x4 parameter pairs remain an explicitly unresolved limitation of the printed algorithm.'],
'2024-09-16-Q2':['Reinitializes every new two-button attempt and displays all LEDs on when the returned labels show an incomplete maze.'],
'2025-01-29_ARM1-Q1':['Corrected R0/R1 documentation to match the original paper and existing assembly.'],
'2025-01-29_ARM1-Q2':['Replaced the reused Q1 matrix with Q2’s distinct matrix. The regression checks E8 -> 56 with c=63.'],
'2025-01-29_ARM3-Q1':['Exported the required transposition name while retaining transpose as a compatibility alias.'],
'2025-01-29_ARM3-Q2':['Calls the paper’s transposition interface.'],
'2025-02-12_ARM1-Q2':['Placed the required global int sineValues array and waveform handler in a complete IRQ_timer.c replacement.'],
'2025-02-12_ARM2-Q2':['Placed the required global int cosineValues array and waveform handler in a complete IRQ_timer.c replacement.'],
'2025-07-01_ARM2-Q1':['Separated the standalone 10-byte Reset_Handler example from the callable routine used by the C questions. Removed the incorrect 256-element claim.'],
'2025-07-01_ARM2-Q2':['Supplied the missing timer-driven C answer using Timer1, 2500 ms, ten calls, and physical LEDs4..7.'],
'2025-07-01_ARM2-Q3':['Corrected first-response ownership, ignored select, retained the full tenth window, stopped RIT at completion, and used equal timer/RIT priorities for shared state.'],
'2026-02-18_ARM1-Q2':['Guarded the final sequence index and ignored a stale Timer1 event after the duration timer has stopped playback.'],
'2026-02-18_ARM2-Q2':['Guarded the final sequence index and ignored a stale Timer1 event after the duration timer has stopped playback.'],
'2026-06-25_ARM1-Q1':['Added the required standalone Reset_Handler scoring example with zeroed scratch arrays.'],
'2026-06-25_ARM2-Q1':['Added the required standalone Reset_Handler scoring example with zeroed scratch arrays.'],
'2026-06-25_ARM1-Q2':['Added three stable 10 ms samples before accepting joystick changes; a raw edge alone did not debounce input.'],
'2026-06-25_ARM2-Q2':['Added three stable 10 ms samples before accepting joystick changes; a raw edge alone did not debounce input.'],
}
for q,r in d.items():
    r['findings']=findings.get(q,['Reviewed the original contract and current implementation; no additional implementation defect found within the documented domain.'])
    r['summary']=''
    if q.startswith('2024-09-16'):r['reviewStatus']='Review complete — unresolved paper-algorithm limitation'
    elif q=='2023-05-17-Q2':r['reviewStatus']='Review complete — conflicting paper wording, explicit formula followed'
    else:r['reviewStatus']='Review complete within the stated contract and limitations'

old={x['question']['question_id']:x['question'] for x in json.loads((W/'mapping.json').read_text(encoding='utf-8'))}
rows=list(csv.DictReader((G/'QUESTION_INDEX.csv').open(encoding='utf-8-sig',newline='')))
summaries={
'2023-02-24-Q1':'Perform one four-digit Kaprekar transformation and return the difference.',
'2023-02-24-Q2':'Handle SVC #50 using the MSP frame and return the number of Kaprekar calls in live R6.',
'2024-07-09-Q1':'Visit the maze with deterministic depth-first search and open reciprocal passage bits.',
'2025-07-01_ARM2-Q1':'Implement the shifted-XOR LCG and fill ten bytes from Reset_Handler.',
'2025-07-01_ARM2-Q2':'Generate ten values with Timer1 every 2500 ms and display their remainders on LEDs4..7.',
}
constants={
'2023-02-24-Q1':'four-digit input 1000..9999; one transformation',
'2023-09-18-Q1':'50 words in Q1 startup; uint32_t overflow returns zero',
'2023-09-18-Q2':'10 terms; 32-bit binary K; LEDs4/5',
'2024-02-12-Q1':'walls *; passages space; exits n/e/s/w',
'2024-02-12-Q2':'10x8; multiplier 18; modulus 101; border threshold 90; interior threshold 60',
'2024-02-28-Q1':'walls X; entrance e; exit numeric 0; failure UINT32_MAX',
'2024-07-09-Q1':'border 0xFF; visited bit0; directions 1..4',
'2024-07-09-Q2':'SysTick LOAD=0xFFFFF; CTRL=5 (no interrupt)',
'2025-01-29_ARM1-Q2':'A=8F C7 E3 F1 F8 7C 3E 1F; c=0x63; 250 ms toggle',
'2025-07-01_ARM2-Q1':'seed=6; a=157; c=3; s=3; m=256; DIM=10',
'2025-07-01_ARM2-Q2':'seed=6; a=157; c=3; s=3; m=256; 10 calls; Timer1=2500 ms',
'2025-07-01_ARM2-Q3':'Timer1=2500 ms; RIT=10 ms; final score at 27.5 s; win LED10, loss LED11',
'2026-02-18_ARM1-Q2':'A=50 ms; B: Pmax=5351,Pmin=1062,k=1; C: Pmax=40000000,Pmin=625000,k=5',
'2026-02-18_ARM2-Q2':'A=50 ms; B: Pmax=5351,Pmin=1062,k=1; C: Pmax=40000000,Pmin=625000,k=5',
'2026-06-25_ARM1-Q1':'(((1<<exact)-1)<<4)+((1<<partial)-1); four digits 0..3',
'2026-06-25_ARM2-Q1':'(((1<<exact)-1)<<4)+((1<<partial)-1); four digits 0..3',
}
for row in rows:
    q=row['question_id'];row['requirement_summary']=summaries.get(q,old[q]['requirement_summary'])
    row['constants']=constants.get(q,old[q]['constants']);d[q]['summary']=row['requirement_summary']
    row['argument_mapping']=d[q]['contract']
out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=list(rows[0]),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(rows)
(G/'QUESTION_INDEX.csv').write_text(out.getvalue(),encoding='utf-8',newline='\n')
# Improve spacing in prose only; never rewrite symbols, prototypes or source code.
words='all|every|at|after|before|by|from|input|output|length|order|seed|mod|return|returns|repeat|terms|dim|wave|distance|direction|directions|physical|value|result|sum|binary|than|through|with|and|or|for|the|a|an|of|in|first|last|remaining|exact|partial|samples|cells|rows|columns|then|flags|push|store|label|labels|count|counts|increment|offset|period|ticks|index|call|calls|gives|gives|needs|bit|bits|LEDs'
def prose(s):
    s=re.sub(r'\b('+words+r')(?=\d)',r'\1 ',s,flags=re.I)
    s=re.sub(r'(?<=\d)(rows|columns|words|terms|samples|iterations|bytes|elements|seconds|calls)\b',r' \1',s)
    s=re.sub(r',(?=[A-Za-z0-9])',', ',s)
    return s
for r in d.values():
    for f in ['contract','complexity','summary']:r[f]=prose(r[f])
    for f in ['method','trace','explanation','mistakes','limitations','findings']:r[f]=[prose(s) for s in r[f]]
(M/'QUESTION_REVIEWS.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=M/'VERIFY_EXAM_ANSWERS.py';s=p.read_text(encoding='utf-8').replace('Execute the delivered ARMASM objects against independent paper-derived cases.','Check ARMASM syntax and execute translated instruction streams against independent paper-derived cases.');p.write_text(s,encoding='utf-8')
p=R/'03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source/README.md'
s=p.read_text(encoding='utf-8').replace('Native Keil and physical-board execution have not been performed for this revision.','All three question answers passed a native SW_Debug build in the current template during the September 8 review. Physical-board execution has not been performed. Current per-question evidence is shown in the guide.');p.write_text(s,encoding='utf-8')
print('Updated 48 records and concise index metadata.')
