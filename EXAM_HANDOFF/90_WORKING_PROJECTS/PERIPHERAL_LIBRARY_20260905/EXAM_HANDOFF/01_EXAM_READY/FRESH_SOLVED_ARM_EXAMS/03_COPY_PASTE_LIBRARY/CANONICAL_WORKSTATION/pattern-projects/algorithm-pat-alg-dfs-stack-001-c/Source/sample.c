#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Bounded DFS with an explicit stack.
 * Recognition cue: visit graph without recursion using bounded stack.
 *
 * Contract rules:
 * - Fixed-width types make width and signedness part of the interface.
 * - A pointer never carries its length; count/capacity arguments are explicit.
 * - const input objects are not mutated. Non-const outputs may be changed only
 *   within their documented bounds.
 * - Invalid, empty, duplicate and arithmetic-limit behavior is executable in
 *   pattern_edge_vectors() and described in the adjacent README.
 *
 * Trace the validation step first, then the main loop/recurrence invariant,
 * then the final result or capacity check. Public suffix functions are named
 * variants of the same advertised pattern, not unrelated shortcuts.
 */

/* Primary algorithm and its named variants. */
uint32_t algorithm_algorithm_pat_alg_dfs_stack_001_c(const uint8_t *adj, uint32_t n, uint32_t start,
                               uint8_t *seen, uint32_t *stack);



static int pattern_core_vector(void) {
  uint8_t a[9] = {0, 1, 0, 1, 0, 1, 0, 1, 0}, s[3] = {0};
  uint32_t q[3];
  return algorithm_algorithm_pat_alg_dfs_stack_001_c(a, 3, 0, s, q) == 3;
}
static int pattern_edge_vectors(void) {
  uint8_t dense[36],seen2[6]={0};uint32_t stack2[7]={0};for(unsigned z=0;z<36;z++)dense[z]=1;stack2[6]=77;if(algorithm_algorithm_pat_alg_dfs_stack_001_c(dense,6,0,seen2,stack2)!=6||stack2[6]!=77)return 0;
  uint8_t a[1] = {0}, s[1] = {0};
  uint32_t q[1];
  return algorithm_algorithm_pat_alg_dfs_stack_001_c(a, 1, 0, s, q) == 1 &&
         algorithm_algorithm_pat_alg_dfs_stack_001_c(NULL, 1, 0, s, q) == 0 &&
         algorithm_algorithm_pat_alg_dfs_stack_001_c(a, 1, 1, s, q) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }

volatile int pattern_result;
int main(void){exam_init();pattern_result=test_main();exam_led_write(pattern_result?0xFFu:0x01u);for(;;){}}
