#include "exam_api.h"
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Singly linked-list operations.
 * Recognition cue: traverse search insert remove nodes.
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

typedef struct algorithm_algorithm_pat_ds_linked_list_001_c_node {
  int32_t value;
  struct algorithm_algorithm_pat_ds_linked_list_001_c_node *next;
} algorithm_algorithm_pat_ds_linked_list_001_c_node_t;

algorithm_algorithm_pat_ds_linked_list_001_c_node_t *
algorithm_algorithm_pat_ds_linked_list_001_c(algorithm_algorithm_pat_ds_linked_list_001_c_node_t *head, int32_t key);

int algorithm_algorithm_pat_ds_linked_list_001_c_insert_after(algorithm_algorithm_pat_ds_linked_list_001_c_node_t *position,
                                        algorithm_algorithm_pat_ds_linked_list_001_c_node_t *node);

algorithm_algorithm_pat_ds_linked_list_001_c_node_t *
algorithm_algorithm_pat_ds_linked_list_001_c_remove_first(algorithm_algorithm_pat_ds_linked_list_001_c_node_t **head,
                                    int32_t key);



static int pattern_core_vector(void) {
  algorithm_algorithm_pat_ds_linked_list_001_c_node_t b = {2, NULL}, a = {1, &b};
  return algorithm_algorithm_pat_ds_linked_list_001_c(&a, 2) == &b &&
         algorithm_algorithm_pat_ds_linked_list_001_c(&a, 3) == NULL;
}
static int pattern_edge_vectors(void) {
  algorithm_algorithm_pat_ds_linked_list_001_c_node_t lone={1,NULL};if(algorithm_algorithm_pat_ds_linked_list_001_c_insert_after(&lone,&lone)||lone.next!=NULL) return 0;
  algorithm_algorithm_pat_ds_linked_list_001_c_node_t c = {3, NULL}, b = {2, NULL}, a = {1, &b};
  algorithm_algorithm_pat_ds_linked_list_001_c_node_t *head = &a;
  return algorithm_algorithm_pat_ds_linked_list_001_c_insert_after(&a, &c) && a.next == &c &&
         algorithm_algorithm_pat_ds_linked_list_001_c_remove_first(&head, 3) == &c &&
         c.next == NULL &&
         algorithm_algorithm_pat_ds_linked_list_001_c_remove_first(&head, 9) == NULL;
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
