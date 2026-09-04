#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Circular ring buffer.
 * Recognition cue: bounded FIFO head tail insertion removal.
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
} ring_t;
int algorithm_isr_to_main_ring_buffer(ring_t *q, int put, int32_t *value) {
  if (!q || !q->b || !q->cap || !value || q->head >= q->cap || q->tail >= q->cap ||
      q->count > q->cap)
    return 0;
  if (put) {
    if (q->count == q->cap)
      return 0;
    q->b[q->head] = *value;
    q->head = (q->head + 1) % q->cap;
    q->count++;
  } else {
    if (!q->count)
      return 0;
    *value = q->b[q->tail];
    q->tail = (q->tail + 1) % q->cap;
    q->count--;
  }
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>


/*
 * Exam-study reference: Circular ring buffer.
 * Recognition cue: bounded FIFO head tail insertion removal.
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
} ring_t;
int algorithm_isr_to_main_ring_buffer(ring_t *q, int put, int32_t *value);

static int pattern_core_vector(void) {
  int32_t b[2], v = 7, o = 0;
  ring_t q = {b, 2, 0, 0, 0};
  return algorithm_isr_to_main_ring_buffer(&q, 1, &v) &&
         algorithm_isr_to_main_ring_buffer(&q, 0, &o) && o == 7;
}
static int pattern_edge_vectors(void) {
  int32_t guard_data[2] = {7, 8}, guard_value = 9;
  ring_t badq = {guard_data, 2, 2, 0, 0};
  if (algorithm_isr_to_main_ring_buffer(&badq, 1, &guard_value) || guard_data[0] != 7)
    return 0;
  int32_t b[1], v = 1, o = 0;
  ring_t q = {b, 1, 0, 0, 0};
  return !algorithm_isr_to_main_ring_buffer(&q, 0, &o) &&
         algorithm_isr_to_main_ring_buffer(&q, 1, &v) &&
         !algorithm_isr_to_main_ring_buffer(&q, 1, &v) &&
         algorithm_isr_to_main_ring_buffer(&q, 0, &o) && o == 1;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }

int main(void){return test_main();}
