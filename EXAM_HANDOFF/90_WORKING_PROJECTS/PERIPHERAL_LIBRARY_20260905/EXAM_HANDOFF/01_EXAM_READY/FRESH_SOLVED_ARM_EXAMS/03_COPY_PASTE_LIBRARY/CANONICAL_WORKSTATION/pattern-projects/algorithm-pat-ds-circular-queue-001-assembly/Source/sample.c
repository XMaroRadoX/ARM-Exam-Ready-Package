#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Circular queue.
 * Recognition cue: bounded FIFO enqueue dequeue.
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
typedef struct {
  int32_t *b;
  uint32_t cap, head, tail, count;
} queue_t;
int algorithm_algorithm_pat_ds_circular_queue_001_assembly(queue_t *q, int enqueue, int32_t *value);



static int pattern_core_vector(void) {
  int32_t b[2], v = 7, o = 0;
  queue_t q = {b, 2, 0, 0, 0};
  return algorithm_algorithm_pat_ds_circular_queue_001_assembly(&q, 1, &v) &&
         algorithm_algorithm_pat_ds_circular_queue_001_assembly(&q, 0, &o) && o == 7;
}
static int pattern_edge_vectors(void) {
  int32_t guard_data[2]={7,8},guard_value=9; queue_t badq={guard_data,2,2,0,0}; if(algorithm_algorithm_pat_ds_circular_queue_001_assembly(&badq,1,&guard_value)||guard_data[0]!=7) return 0;
  int32_t b[1], v = 1, o = 0;
  queue_t q = {b, 1, 0, 0, 0};
  return !algorithm_algorithm_pat_ds_circular_queue_001_assembly(&q, 0, &o) &&
         algorithm_algorithm_pat_ds_circular_queue_001_assembly(&q, 1, &v) &&
         !algorithm_algorithm_pat_ds_circular_queue_001_assembly(&q, 1, &v) &&
         algorithm_algorithm_pat_ds_circular_queue_001_assembly(&q, 0, &o) && o == 1;
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
