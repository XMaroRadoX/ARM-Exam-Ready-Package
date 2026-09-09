"""Execute the July 1 seed-1 answers with LLVM/Unicorn and mocked peripherals.
No native Keil or physical-board claim. Run with the package Python runtime.
"""
from pathlib import Path
import hashlib, json, re, sys
from VERIFY_ALGORITHMS import CLANG, LLD, gas, emulate, run

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/"03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2025-07-01_ARM1_LCG_Rhythm/Answer Source"
BUILD=ROOT/"90_WORKING_PROJECTS/LCG_20250701_UPDATE/tests"
API=ROOT/"01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API/Source/exam_api"
FLAGS=["--target=arm-none-eabi","-mcpu=cortex-m3","-mthumb","-O0","-ffreestanding","-fno-builtin","-fno-stack-protector","-Wall","-Wextra","-Werror"]
MOCK=r"""
#include "exam_api.h"
static uint32_t joystick, led, clears, timer_stopped, rit_stopped, calls;
static uint32_t pending_flag=1u;
void exam_init(void) {}
void exam_joystick_init(void) {}
uint32_t exam_joystick_read(void) { return joystick; }
uint32_t exam_joystick_pressed_edges(uint32_t p,uint32_t c) {return c & ~p;}
void exam_led_clear(void) {led=0;clears++;}
exam_status_t exam_led_on(uint8_t label) {led=label;return EXAM_OK;}
uint32_t exam_timer_ack(exam_timer_t t) {(void)t;return pending_flag;}
void exam_rit_ack(void) {}
void exam_timer_stop(exam_timer_t t) {(void)t;timer_stopped++;}
void exam_rit_stop(void) {rit_stopped++;}
exam_status_t exam_timer_config_ms(exam_timer_t t,uint32_t ms,exam_timer_mode_t mode) {(void)t;(void)ms;(void)mode;return EXAM_OK;}
exam_status_t exam_rit_config_ms(uint32_t ms) {(void)ms;return EXAM_OK;}
void exam_timer_start(exam_timer_t t) {(void)t;}
void exam_rit_start(void) {}
void NVIC_SetPriority(int irq,uint32_t p) {(void)irq;(void)p;}
void __WFI(void) {}
extern uint32_t nextElementLCG(uint32_t,uint32_t,uint32_t,uint32_t,uint32_t);
uint32_t counted_lcg(uint32_t x,uint32_t a,uint32_t c,uint32_t n,uint32_t m) {
    calls++;return nextElementLCG(x,a,c,n,m);
}
#define CHECK(x) do {if (!(x)) return __LINE__;} while(0)
"""
Q2=r"""
uint32_t test_main(void) {
    const uint32_t expected[]={9,9,8,8,11,8,9,9,9,10};
    uint32_t i;
    pending_flag=0;TIMER0_IRQHandler();CHECK(calls==0);
    pending_flag=1;
    for(i=0;i<10;i++) {
        TIMER0_IRQHandler();CHECK(led==expected[i]);CHECK(calls==i+1);
        CHECK(clears==i+1);
    }
    CHECK(timer_stopped==1);
    TIMER0_IRQHandler();CHECK(calls==10 && led==10);
    return 0;
}
"""
Q3=r"""
static void reset_game(void) {
    previous=1;n=0;waiting_for_move=0;expected_direction=0;
    num_correct=0;num_wrong=0;old_joystick=0;joystick=0;
    led=0;clears=0;timer_stopped=0;rit_stopped=0;calls=0;pending_flag=1;
}
static void input(uint32_t v) {joystick=v;RIT_IRQHandler();}
uint32_t test_main(void) {
    uint32_t i, saved;
    reset_game();
    input(EXAM_JOY_RIGHT);CHECK(num_correct==0 && num_wrong==0);
    TIMER0_IRQHandler();CHECK(led==9 && calls==1);
    input(EXAM_JOY_RIGHT);CHECK(waiting_for_move==1); /* held before round */
    input(0);input(EXAM_JOY_RIGHT);
    CHECK(num_correct==1 && waiting_for_move==0 && led==0);
    input(0);input(EXAM_JOY_LEFT);CHECK(num_wrong==0); /* second ignored */

    TIMER0_IRQHandler();CHECK(led==9);
    input(EXAM_JOY_LEFT);CHECK(waiting_for_move==1); /* still held */
    input(0);input(EXAM_JOY_UP);
    CHECK(num_wrong==1 && led==0);
    input(0);input(EXAM_JOY_RIGHT);CHECK(num_correct==1);

    TIMER0_IRQHandler();CHECK(led==8);
    input(0);input(EXAM_JOY_SELECT);CHECK(waiting_for_move==1);
    input(0);input(EXAM_JOY_DOWN|EXAM_JOY_RIGHT);
    CHECK(num_wrong==2 && waiting_for_move==0);

    /* No response: neither score changes when the next round starts. */
    TIMER0_IRQHandler();saved=num_correct+num_wrong;
    TIMER0_IRQHandler();CHECK(num_correct+num_wrong==saved);

    /* Reach tenth LED without ending its response window early. */
    while(n<10) TIMER0_IRQHandler();
    CHECK(calls==10 && waiting_for_move==1 && timer_stopped==0 && led==10);
    input(0);input(EXAM_JOY_LEFT);CHECK(num_correct==2);
    TIMER0_IRQHandler();
    CHECK(calls==10 && timer_stopped==1 && rit_stopped==1 && led==5);
    input(0);input(EXAM_JOY_LEFT);
    CHECK(led==5 && num_correct==2 && num_wrong==2); /* result stable */

    /* Ten correct answers => win, including a valid final-round answer. */
    reset_game();
    for(i=0;i<10;i++) {
        TIMER0_IRQHandler();input(0);input(expected_direction);
    }
    CHECK(calls==10 && num_correct==10 && timer_stopped==0);
    TIMER0_IRQHandler();CHECK(led==4 && rit_stopped==1);
    input(0);input(EXAM_JOY_UP);CHECK(led==4 && num_correct==10);

    /* Missing every response gives 0-0: a tie is defeat. */
    reset_game();
    for(i=0;i<11;i++) TIMER0_IRQHandler();
    CHECK(calls==10 && num_correct==0 && num_wrong==0 && led==5);
    return 0;
}
"""
def assembly(text):
    out=gas(text)
    return re.sub(r"(?m)^(nextElementLCG|Reset_Handler):",r".thumb_func\n\1:",out)
def check_c(q,fixture):
    folder=BUILD/q;folder.mkdir(parents=True,exist_ok=True)
    (folder/"LPC17xx.h").write_text("#pragma once\n#include <stdint.h>\n#define TIMER0_IRQn 1\n#define RIT_IRQn 29\nvoid NVIC_SetPriority(int,uint32_t);\nvoid __WFI(void);\n")
    # Include the delivered file unchanged except for main/call names in the fixture.
    text='#define main answer_main\n#define nextElementLCG counted_lcg\n#include "'+(SOURCE/q/"main.c").as_posix()+'"\n#undef main\n#undef nextElementLCG\n'+MOCK+fixture
    (folder/"test.c").write_text(text)
    (folder/"answer.s").write_text(assembly((SOURCE/q/"assembly.s").read_text()))
    run([CLANG,*FLAGS,"-I",folder,"-I",API,"-c",folder/"test.c","-o",folder/"test.o"])
    run([CLANG,*FLAGS[:3],"-c",folder/"answer.s","-o",folder/"answer.o"])
    objects=[folder/"test.o",folder/"answer.o"]
    for f in (SOURCE/q).glob("IRQ_*.c"):
        obj=folder/(f.stem+".o")
        run([CLANG,*FLAGS,"-I",folder,"-I",API,"-c",f,"-o",obj]);objects.append(obj)
    elf=folder/"test.elf"
    run([LLD,"-Ttext=0x10000","--entry=test_main",*objects,"-o",elf])
    result,called,untested=emulate(elf,["nextElementLCG"])
    assert result==0,(q,"fixture assertion line",result)
    assert called==["nextElementLCG"] and not untested
    return dict(status="THUMB_EXECUTION_WITH_MOCK_PERIPHERALS_PASS",assertions=fixture.count("CHECK("),abi="R4-R11, SP restoration and 8-byte call alignment checked")
def check_q1():
    from elftools.elf.elffile import ELFFile
    from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_MODE_MCLASS
    from unicorn.arm_const import UC_ARM_REG_SP,UC_ARM_REG_PC
    folder=BUILD/"Q1";folder.mkdir(parents=True,exist_ok=True)
    (folder/"answer.s").write_text(assembly((SOURCE/"Q1/assembly.s").read_text()))
    run([CLANG,*FLAGS[:3],"-c",folder/"answer.s","-o",folder/"answer.o"])
    elf=folder/"test.elf";run([LLD,"-Ttext=0x10000","--entry=Reset_Handler",folder/"answer.o","-o",elf])
    uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB|UC_MODE_MCLASS)
    uc.mem_map(0x10000,0x200000);uc.mem_map(0x20000000,0x200000)
    with elf.open("rb") as f:
        e=ELFFile(f)
        for seg in e.iter_segments():
            if seg["p_type"]=="PT_LOAD":uc.mem_write(seg["p_vaddr"],seg.data())
        syms={s.name:s["st_value"] for s in e.get_section_by_name(".symtab").iter_symbols()}
    start=syms["sequence"];sp=0x20010000
    uc.mem_write(start,bytes([0xCC])*14)
    uc.reg_write(UC_ARM_REG_SP,sp)
    uc.emu_start(syms["Reset_Handler"]|1,syms["finished"]&~1,count=100000)
    assert uc.reg_read(UC_ARM_REG_PC)==syms["finished"]&~1
    expected=[138,234,63,103,236,71,126,198,182,125]
    assert list(uc.mem_read(start,10))==expected
    assert bytes(uc.mem_read(start+10,4))==bytes([0xCC])*4,"array overrun"
    assert uc.reg_read(UC_ARM_REG_SP)==sp
    return dict(status="THUMB_RESET_HANDLER_EXECUTION_PASS",array=expected,stack_restored=True,array_overrun=False)
def main():
    results={"Q1":check_q1(),"Q2":check_c("Q2",Q2),"Q3":check_c("Q3",Q3)}
    results["limits"]=["LLVM directive translation, not native Keil ARMASM","Mock peripherals, not physical board execution","10 ms input polling; no separate mechanical debounce guarantee"]
    results["source_sha256"]={p.relative_to(SOURCE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.glob("Q*/*") if p.suffix in (".c",".s")}
    (HERE/"LCG_20250701_VALIDATION.json").write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps({k:v for k,v in results.items() if k!="source_sha256"},indent=2))
if __name__=="__main__":main()


