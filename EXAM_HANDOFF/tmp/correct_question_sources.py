from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]/'90_WORKING_PROJECTS/QUESTION_REVIEW_20260908/EXAM_HANDOFF'
solved=root/'03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams'
changes=[]
def folder(prefix):return next(solved.glob(prefix+'*'))/'Answer Source'
def edit(prefix,name,old,new):
    p=folder(prefix)/name;t=p.read_text(encoding='utf-8-sig');assert old in t,(p,old)
    p.write_text(t.replace(old,new),encoding='utf-8');changes.append(str(p.relative_to(root)))
def put(p,t):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');changes.append(str(p.relative_to(root)))

# Preserve the pre-exception R7 before using it as a frame pointer.
edit('2023-02-24','assembly.s','MRS     R7, MSP         ; original hardware frame before software saves\n                PUSH    {R4, R5, R7, LR}', 'MRS     R12, MSP        ; frame address before software saves\n                PUSH    {R4, R5, R7, LR}\n                MOV     R7, R12')
# The paper explicitly uses abs(U), not the high word of abs(U:L).
edit('2023-05-17','assembly.s','MVN     R5, R5\n                MVN     R4, R4\n                ADDS    R5, R5, #1\n                MOVS    R8, #0\n                ADCS    R4, R4, R8','RSB     R4, R4, #0      ; paper test uses absolute upper word')
# Aliquot sum of 1 is zero; the supplied divisor loop otherwise never terminates.
edit('2023-07-04','assembly.s','aliquotSum      PROC\n', 'aliquotSum      PROC\n                CMP     R0, #1\n                BHI     aliquot_nontrivial\n                MOVS    R0, #0\n                BX      LR\naliquot_nontrivial\n')
# Count each stored term's digits exactly once.
edit('2023-09-18','assembly.s','STR     R6, [R4, R8, LSL #2]\n                ADD     R7, R7, R0', 'STR     R6, [R4, R8, LSL #2]\n                MOV     R0, R6\n                BL      digitSum       ; count the NEW term, not its predecessor\n                ADD     R7, R7, R0')
edit('2023-09-18','main.c','formula = series[9] - series[0] + digitSum(series[9]);', '/* A failed generation leaves the tail unwritten. Do not read it. */\n    formula = reported ? series[9] - series[0] + digitSum(series[9]) : UINT32_MAX;')
edit('2024-02-12','main.c','(value * 18u) % 101u','((value % 101u) * 18u) % 101u')
# Terminate disconnected or unrepresentable byte-labelled mazes visibly.
edit('2024-02-28','assembly.s','sp_wave        MOVS    R8, #0','sp_wave        MOVS    R12, #0         ; number of newly labelled passages\n                MOVS    R8, #0')
edit('2024-02-28','assembly.s','STRB    R9, [R5, R8]\n                B       sp_scan_next','STRB    R9, [R5, R8]\n                ADD     R12, R12, #1\n                B       sp_scan_next')
edit('2024-02-28','assembly.s','sp_next_wave    ADDS    R7, R7, #1\n                B       sp_wave','sp_next_wave    CMP     R12, #0\n                BEQ     sp_unreachable\n                ADDS    R7, R7, #1\n                CMP     R7, #32         ; byte 32 is also the passage marker\n                BLO     sp_wave\nsp_unreachable  MVN     R0, #0          ; explicit failure extension: UINT32_MAX\n                POP     {R4-R11, R12, PC}')
edit('2024-02-28','main.c','if(!find_entrance() ||','if(step_value < 0 || !find_entrance() ||')
# Literal pushes 1,2,3,4 leave the last eligible direction at stack index zero.
edit('2024-07-09','assembly.s','LDR     R0, [R4, R6, LSL #2]', 'SUB     R7, R5, #1\n                SUB     R6, R7, R6\n                LDR     R0, [R4, R6, LSL #2]')
edit('2024-07-09','main.c','if(exam_systick_config_ticks(0x100000u)!=EXAM_OK) {\n    leds_fill();\n    for (;;) __WFI();\n  }','/* The Q2 Reset_Handler starts SysTick with TICKINT clear. */')
p=folder('2024-07-09');s=(p/'assembly.s').read_text();reset='''
                EXPORT Reset_Handler
                IMPORT SystemInit
                IMPORT __main
Reset_Handler   PROC
                BL      SystemInit
                LDR     R0, =0xE000E010
                MOVS    R1, #0
                STR     R1, [R0]
                LDR     R2, =0xFFFFF
                STR     R2, [R0, #4]
                STR     R1, [R0, #8]
                MOVS    R1, #5          ; core clock + enable; NO interrupt
                STR     R1, [R0]
                LDR     R0, =__main
                BX      R0
                ENDP
                LTORG
'''
put(p/'Q2/assembly.s',s.replace('                END\n',reset+'                END\n'))
edit('2025-01-29_ARM1','main.c','0xF8u, 0x7Cu, 0x3Eu, 0x1Fu, 0x8Fu, 0xC7u, 0xE3u, 0xF1u','0x8Fu, 0xC7u, 0xE3u, 0xF1u, 0xF8u, 0x7Cu, 0x3Eu, 0x1Fu')
# Keep the prior alias for working copies while exporting the paper's exact name.
edit('2025-01-29_ARM3','assembly.s','EXPORT  transpose','EXPORT  transpose\n                EXPORT  transposition')
edit('2025-01-29_ARM3','assembly.s','transpose       PROC','transposition\ntranspose       PROC')
edit('2025-01-29_ARM3','main.c','transpose(', 'transposition(')
# Publish the requested file ownership for the inspected sine/cosine globals.
for variant,wave,timer in [('ARM1','sine',0),('ARM2','cosine',1)]:
    p=folder('2025-02-12_'+variant);t=(p/'main.c').read_text();a=t.index('int '+wave+'Values[45];');b=t.index('int main(void)')
    irq=t[:a]+t[a:b]
    irq+='\n'+'\n'.join(f'void TIMER{i}_IRQHandler(void) {{ exam_timer_ack(EXAM_TIMER{i}); }}' for i in range(4) if i!=timer)+'\n'
    put(p/'Q2/IRQ_timer.c',irq)
    put(p/'Q2/main.c',t[:a]+t[b:])

# ARM2 Q2 was mapped to assembly only, and the whole-paper game was not a Q2 answer.
# Reuse the already explicit per-question structure of the companion ARM1 paper.
a=folder('2025-07-01_ARM1');b=folder('2025-07-01_ARM2')
for q in ['Q2','Q3']:
    for src in (a/q).glob('*'):
        if src.suffix not in ['.c','.s']:continue
        t=src.read_text().replace('nextElementLCG','LCGsequence')
        t=t.replace('131u, 7u, n, 255u','157u, 3u, 3u, 256u').replace('previous = 1u','previous = 6u')
        t=t.replace('TIMER0','TIMER1').replace('3000u','2500u').replace('three seconds','2.5 seconds').replace('three-second','2.5-second').replace('3-second','2.5-second')
        t=t.replace('11u - remainder','4u + remainder').replace('num_correct','hit').replace('num_wrong','miss')
        if q=='Q3':
            t=t.replace('exam_led_on(4u);','exam_led_on(10u);').replace('exam_led_on(5u);','exam_led_on(11u);')
            t=t.replace('LED 11/10/9/8','LED 4/5/6/7')
        t=t.replace('0->11, 1->10, 2->9, 3->8.','0->4, 1->5, 2->6, 3->7.')
        if src.name=='IRQ_timer.c':t=t.replace('void TIMER1_IRQHandler(void) { exam_timer_ack(EXAM_TIMER1); }','void TIMER0_IRQHandler(void) { exam_timer_ack(EXAM_TIMER0); }')
        if src.suffix=='.s':
            original=(b/'assembly.s').read_text();t=original[:original.index('DIM             EQU')]+original[original.index('; uint32_t LCGsequence'):]
        put(b/q/src.name,t)
# Standalone assembly startup test keeps results visible rather than clearing them via __main.
s=(b/'assembly.s').read_text().replace('                IMPORT  __main\n','')
s=s.replace('LDR     R0, =__main\n                BX      R0','B       lcg_finished\nlcg_finished    B       lcg_finished')
put(b/'Q1/assembly.s',s)
put(b/'main.c',(b/'Q3/main.c').read_text())
put(b/'assembly.s',(b/'Q3/assembly.s').read_text())

# Bound final sequence access even if an already-pending Timer A IRQ is delivered.
for variant in ['ARM1','ARM2']:
    edit('2026-02-18_'+variant,'main.c','if (exam_timer_is_running(EXAM_TIMER1) ||','if (sequence_index >= SEQUENCE_LENGTH ||\n      exam_timer_is_running(EXAM_TIMER1) ||')
    edit('2026-02-18_'+variant,'main.c','sample_index++;','if (!exam_timer_is_running(EXAM_TIMER1)) return;\n  sample_index++;')

# A sampled edge is not debounce. Require three stable 10 ms samples before a transition.
for variant in ['ARM1','ARM2']:
    edit('2026-06-25_'+variant,'main.c','static uint32_t previous_joystick;', 'static uint32_t previous_joystick;\nstatic uint32_t candidate_joystick;\nstatic uint32_t stable_samples;')
    edit('2026-06-25_'+variant,'main.c','pressed=exam_joystick_pressed_edges(previous_joystick,current);\n  previous_joystick=current;', 'if (current != candidate_joystick) {\n    candidate_joystick = current; stable_samples = 1u; return;\n  }\n  if (stable_samples < 3u) ++stable_samples;\n  if (stable_samples < 3u) return;\n  pressed=exam_joystick_pressed_edges(previous_joystick,current);\n  previous_joystick=current;')
    edit('2026-06-25_'+variant,'main.c','previous_joystick=exam_joystick_read();','previous_joystick=exam_joystick_read();\n  candidate_joystick=previous_joystick;\n  stable_samples=3u;')

# Q1 setup is part of the requested answer, not an implicit instruction to edit
# the protected startup file. Strong standalone handlers reuse its vector table.
for prefix,func in [('2026-06-25_ARM1','BullsAndCows'),('2026-06-25_ARM2','Mastermind')]:
    p=folder(prefix);s=(p/'assembly.s').read_text()
    setup=f'''
                AREA    GAME_INPUTS, DATA, READONLY
review_guess    DCD     0,1,2,3
review_secret   DCD     1,2,2,0
                AREA    GAME_SCRATCH, DATA, READWRITE, NOINIT
review_scratch  SPACE   32
                AREA    |.text|, CODE, READONLY
                EXPORT  Reset_Handler
Reset_Handler   PROC
                LDR     R2, =review_scratch
                MOVS    R0, #0
                MOVS    R1, #0
review_clear    STR     R0, [R2, R1]
                ADDS    R1, R1, #4
                CMP     R1, #32
                BLO     review_clear
                ADD     R3, R2, #16
                LDR     R0, =review_guess
                LDR     R1, =review_secret
                BL      {func}
review_finished B       review_finished ; R0=19 for the paper example
                ENDP
                LTORG
'''
    put(p/'Q1/assembly.s',s.replace('                END\n',setup+'                END\n'))
p=folder('2023-09-18');s=(p/'assembly.s').read_text()
setup='''
                AREA    DIGIT_SERIES, DATA, READWRITE, NOINIT
review_series   SPACE   200             ; 50 words, as requested
                AREA    |.text|, CODE, READONLY
                EXPORT  Reset_Handler
Reset_Handler   PROC
                LDR     R0, =review_series
                MOVS    R2, #47
                STR     R2, [R0]
                MOVS    R1, #50
                BL      digitaddition
review_finished B       review_finished
                ENDP
                LTORG
'''
put(p/'Q1/assembly.s',s.replace('                END\n',setup+'                END\n'))
(root.parent/'source_changes.json').write_text(json.dumps(sorted(set(changes)),indent=2))
print('Corrected',len(set(changes)),'maintained source files in staging')
