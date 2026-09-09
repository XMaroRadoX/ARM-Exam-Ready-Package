"""Execute the actual LED helper bodies as Cortex-M3 code with a mock LED driver."""
from pathlib import Path
import json, subprocess, sys
from VERIFY_ALGORITHMS import CLANG, LLD, RUNTIME, emulate

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
API = ROOT / "01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API/Source/exam_api"

MOCK = r"""
#include "exam_api.h"
volatile unsigned char led_value;
static uint32_t irq_mask, writes, enters, exits, errors;
uint32_t exam_critical_enter(void) {
    uint32_t old = irq_mask; irq_mask = 1u; ++enters; return old;
}
void exam_critical_exit(uint32_t old) { ++exits; irq_mask = old; }
void LED_On(unsigned int index) {
    if (irq_mask != 1u || index > 7u) { ++errors; return; }
    ++writes; led_value |= (uint8_t)(1u << index);
}
void LED_Off(unsigned int index) {
    if (irq_mask != 1u || index > 7u) { ++errors; return; }
    ++writes; led_value &= (uint8_t)~(1u << index);
}
void LED_Out(unsigned int value) {
    if (irq_mask != 1u) ++errors;
    ++writes; led_value = (uint8_t)value;
}
"""

TEST = r"""
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
typedef exam_status_t (*led_operation)(uint8_t);
uint32_t test_main(void) {
    const led_operation ops[] = {exam_led_on, exam_led_off, exam_led_toggle, exam_led_one_hot};
    const uint8_t masks[] = {0,0,0,0,0x80,0x40,0x20,0x10,0x08,0x04,0x02,0x01};
    const uint8_t seeds[] = {0x00,0x05,0x81,0xFF};
    uint32_t old_irq, label, op, seed, value;
    for (old_irq=0; old_irq<2; ++old_irq) {
        for (label=0; label<256; ++label) {
            for (seed=0; seed<4; ++seed) {
                for (op=0; op<4; ++op) {
                    uint8_t expected = seeds[seed];
                    uint32_t valid = label>=4 && label<=11;
                    irq_mask=old_irq; led_value=expected;
                    writes=enters=exits=errors=0;
                    exam_status_t status = ops[op]((uint8_t)label);
                    if (valid) {
                        if (op==0) expected |= masks[label];
                        if (op==1) expected &= (uint8_t)~masks[label];
                        if (op==2) expected ^= masks[label];
                        if (op==3) expected = masks[label];
                        CHECK(status==EXAM_OK);
                        CHECK(writes==1 && enters==1 && exits==1);
                    } else {
                        CHECK(status==EXAM_OUT_OF_RANGE);
                        CHECK(writes==0 && enters==0 && exits==0);
                    }
                    CHECK(led_value==expected);
                    CHECK(irq_mask==old_irq && errors==0);
                }
            }
        }
        for (value=0; value<256; ++value) {
            irq_mask=old_irq; writes=enters=exits=errors=0;
            exam_led_write((uint8_t)value);
            CHECK(led_value==value && irq_mask==old_irq && writes==1);
            CHECK(exam_led_read()==value);
            CHECK(exam_led_read()==value && led_value==value);
            exam_led_clear();
            CHECK(led_value==0 && exam_led_read()==0);
            CHECK(irq_mask==old_irq && errors==0 && enters==exits);
        }
    }
    return 0;
}
"""

def run(args):
    result = subprocess.run([str(a) for a in args], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)

def main():
    text = (API / "exam_api.c").read_text(encoding="utf-8")
    start = text.index("exam_status_t exam_led_on(")
    end = text.index("void exam_buttons_init(", start)
    bodies = text[start:end]
    build = HERE / ".led-tests"
    build.mkdir(exist_ok=True)
    (build / "test.c").write_text(MOCK + bodies + TEST, encoding="utf-8")
    (build / "runtime.c").write_text(RUNTIME, encoding="utf-8")
    flags = ["--target=arm-none-eabi", "-mcpu=cortex-m3", "-mthumb", "-std=c11",
             "-O0", "-ffreestanding", "-fno-builtin", "-fno-stack-protector",
             "-Wall", "-Wextra", "-Werror"]
    for name in ("test", "runtime"):
        run([CLANG, *flags, "-I", API, "-c", build / (name+".c"), "-o", build / (name+".o")])
    run([LLD, "-Ttext=0x10000", "--entry=test_main", build/"test.o", build/"runtime.o",
         "-o", build/"test.elf"])
    exports = ["exam_led_"+name for name in ("on", "off", "toggle", "one_hot", "write", "read", "clear")]
    result, called, untested = emulate(build / "test.elf", exports)
    if result or untested:
        raise RuntimeError(f"LED execution failed at fixture line {result}; untested={untested}")
    report = {"status": "PASS", "singleLedScenarios": 8192, "wholeDisplaySequences": 512,
              "labels": "All uint8_t values, including all eight valid labels",
              "initialDisplayMasks": ["0x00", "0x05", "0x81", "0xFF"],
              "interruptState": "Enabled and already masked; original state restored",
              "executedExports": called, "physicalBoard": "Not tested",
              "method": "Actual LED helper bodies compiled for Cortex-M3; mock low-level LED driver"}
    (HERE / "LED_API_VALIDATION.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
