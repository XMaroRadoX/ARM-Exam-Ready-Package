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

typedef struct algorithm_singly_linked_list_operations_node {
  int32_t value;
  struct algorithm_singly_linked_list_operations_node *next;
} algorithm_singly_linked_list_operations_node_t;

algorithm_singly_linked_list_operations_node_t *algorithm_singly_linked_list_operations(
    algorithm_singly_linked_list_operations_node_t *head, int32_t key) {
  while ((head != NULL) && (head->value != key)) {
    head = head->next;
  }
  return head;
}

int algorithm_singly_linked_list_operations_insert_after(
    algorithm_singly_linked_list_operations_node_t *position,
    algorithm_singly_linked_list_operations_node_t *node) {
  if ((position == NULL) || (node == NULL) || (position == node)) {
    return 0;
  }
  node->next = position->next;
  position->next = node;
  return 1;
}

algorithm_singly_linked_list_operations_node_t *
algorithm_singly_linked_list_operations_remove_first(
    algorithm_singly_linked_list_operations_node_t **head, int32_t key) {
  algorithm_singly_linked_list_operations_node_t **link = head;

  if (head == NULL) {
    return NULL;
  }
  while ((*link != NULL) && ((*link)->value != key)) {
    link = &(*link)->next;
  }
  if (*link != NULL) {
    algorithm_singly_linked_list_operations_node_t *removed = *link;
    *link = removed->next;
    removed->next = NULL;
    return removed;
  }
  return NULL;
}
