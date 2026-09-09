#include "LPC17xx.h"
#include "exam_api.h"

extern uint32_t isSociable(uint32_t n);

/* Inspect results and tests_passed in the debugger after tests_done = 1. */
const uint32_t inputs[4] = {28u, 220u, 12496u, 100u};
const uint32_t expected[4] = {1u, 2u, 5u, 0u};
volatile uint32_t results[4];
volatile uint32_t tests_passed = 0u;
volatile uint32_t tests_done = 0u;

int main(void)
{
    uint32_t i;
    exam_init();
    for (i = 0u; i < 4u; ++i) {
        results[i] = isSociable(inputs[i]);
        if (results[i] == expected[i]) {
            ++tests_passed;
        }
    }
    tests_done = 1u;
    while (1) {
        __WFI();
    }
}
