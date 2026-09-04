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

typedef struct pat_ds_linked_list_001_node {
  int32_t value;
  struct pat_ds_linked_list_001_node *next;
} pat_ds_linked_list_001_node_t;

pat_ds_linked_list_001_node_t *
pat_ds_linked_list_001(pat_ds_linked_list_001_node_t *head, int32_t key);

int pat_ds_linked_list_001_insert_after(pat_ds_linked_list_001_node_t *position,
                                        pat_ds_linked_list_001_node_t *node);

pat_ds_linked_list_001_node_t *
pat_ds_linked_list_001_remove_first(pat_ds_linked_list_001_node_t **head,
                                    int32_t key);



static int pattern_core_vector(void) {
  pat_ds_linked_list_001_node_t b = {2, NULL}, a = {1, &b};
  return pat_ds_linked_list_001(&a, 2) == &b &&
         pat_ds_linked_list_001(&a, 3) == NULL;
}
static int pattern_edge_vectors(void) {
  pat_ds_linked_list_001_node_t lone={1,NULL};if(pat_ds_linked_list_001_insert_after(&lone,&lone)||lone.next!=NULL) return 0;
  pat_ds_linked_list_001_node_t c = {3, NULL}, b = {2, NULL}, a = {1, &b};
  pat_ds_linked_list_001_node_t *head = &a;
  return pat_ds_linked_list_001_insert_after(&a, &c) && a.next == &c &&
         pat_ds_linked_list_001_remove_first(&head, 3) == &c &&
         c.next == NULL &&
         pat_ds_linked_list_001_remove_first(&head, 9) == NULL;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
