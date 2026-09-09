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
int algorithm_queue_wraparound(queue_t *q, int enqueue, int32_t *value) {
  if (!q || !q->b || !q->cap || !value || q->head >= q->cap || q->tail >= q->cap ||
      q->count > q->cap)
    return 0;
  if (enqueue) {
    if (q->count == q->cap)
      return 0;
    q->b[q->tail] = *value;
    q->tail = (q->tail + 1) % q->cap;
    q->count++;
  } else {
    if (!q->count)
      return 0;
    *value = q->b[q->head];
    q->head = (q->head + 1) % q->cap;
    q->count--;
  }
  return 1;
}
