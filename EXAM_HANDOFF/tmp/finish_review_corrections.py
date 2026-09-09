from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]/'90_WORKING_PROJECTS/QUESTION_REVIEW_20260908/EXAM_HANDOFF'
maint=root/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE'
src=root/'03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-09-16_Kruskal_Buttons/Answer Source'
p=src/'assembly.s';t=p.read_text();old='CMP     R6, R10\n                BHS     kr_check_done\n                LDRB    R0, [R9, R6]'
assert old in t
t=t.replace(old,'CMP     R6, R10\n                BLO     kr_vertical_valid\n                CMP     R5, R10         ; no later wall is reachable if x>=N,y>=N\n                BHS     kr_done         ; failure: leave partial labels for caller\n                B       kr_check_done\nkr_vertical_valid\n                LDRB    R0, [R9, R6]')
p.write_text(t)
p=src/'main.c';t=p.read_text();t=t.replace('if(selection_count==0u){increment=value;selection_count=1u;}', 'if(selection_count==0u){initialize_arrays();increment=value;selection_count=1u;}')
t=t.replace('else {selection_count=0u;kruskal(maze,horizontal,vertical,ROWS,COLS,increment,value);}', '''else {
    uint32_t i;
    selection_count=0u;
    kruskal(maze,horizontal,vertical,ROWS,COLS,increment,value);
    /* The printed algorithm can stall for some button pairs. A nonzero
       component label means it returned a partial maze, not success. */
    for(i=0u;i<ROWS*COLS;++i) {
      if(maze[i]!=0u){exam_led_write(0xFFu);break;}
    }
  }''')
p.write_text(t)
p=maint/'VERIFY_EXAM_ANSWERS.py';t=p.read_text();t=t.replace("if xx>=n:xx-=n;wall=vv;offset=4", "if xx>=n:\n                    xx-=n;wall=vv;offset=4\n                    if xx>=n and yy>=n:break")
t=t.replace('all nine button-selected increment/offset pairs on3x4; all three output arrays match independent paper model','all nine3x4 button pairs: five complete and four explicit partial-maze exits when x>=N,y>=N; arrays match the paper model up to its nonconverging state')
p.write_text(t)
p=maint/'QUESTION_REVIEWS.json';d=json.loads(p.read_text(encoding='utf-8'))
r=d['2024-09-16-Q1'];r['limitations']=[
 'Unresolved paper-algorithm limitation: on the3x4 maze, (increment,offset)=(2,2),(3,2),(3,3),(3,4) reach x>=N and y>=N after the vertical subtraction. Subsequent unbounded-arithmetic iterations cannot reach another wall. The other five2..4 button pairs converge.',
 'The answer now detects that stalled state and returns the partial arrays without changing the required void prototype. Nonzero component labels mean failure, not a completed maze. This is a documented safety extension; it does not invent a replacement Kruskal algorithm.'
]
r['method'].append('If a vertical subtraction leaves x>=N while y>=N, return the partial maze: another iteration cannot make progress without arithmetic wraparound.')
r['reviewStatus']='Reviewed; paper algorithm has an unresolved convergence limitation'
r=d['2024-09-16-Q2'];r['limitations']=[
 'Some valid button pairs expose the printed algorithm’s convergence defect; see Q1. The C answer lights all LEDs if any nonzero component labels remain after the call. This error indication is an implementation extension.',
 'Starting another two-button attempt reinitializes the maze. Raw-button bounce and physical response still require hardware checks.'
]
r['reviewStatus']='Reviewed; four button combinations produce a flagged partial maze'
for qid in ['2025-01-29_ARM1-Q2']:
    d[qid]['trace']=[x.replace('into F0','into56').replace('show F0','show56') for x in d[qid]['trace']]
# Readable spacing: add separation at letter-number boundaries in prose only.
# Preserve identifiers, hex values and prototype spellings by avoiding global rewriting.
(maint/'QUESTION_REVIEWS.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added explicit Kruskal stall handling and corrected checked affine trace to0x56')
