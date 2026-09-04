#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Assembly objects and exported symbols.
 * Recognition cue: define constants initialized reserved aligned exported data.
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

enum { pat_data_asm_objects_001_BUFFER_WORDS = 8 };

extern const uint32_t pat_data_asm_objects_001_magic;
extern uint32_t pat_data_asm_objects_001_initialized_words[4];
extern uint32_t pat_data_asm_objects_001_workspace[pat_data_asm_objects_001_BUFFER_WORDS];
extern const uint32_t pat_data_asm_objects_001_masks[4];

uint32_t pat_data_asm_objects_001(const uint32_t *values, uint32_t count);



static int pattern_core_vector(void) {
  uint32_t a[] = {1, 2, 3};
  return pat_data_asm_objects_001(a, 3) == 6;
}
static int pattern_edge_vectors(void) {
  if(pat_data_asm_objects_001_magic!=0x13579BDFu||pat_data_asm_objects_001_initialized_words[3]!=4||pat_data_asm_objects_001_masks[3]!=8)return 0;
  uint32_t one[] = {UINT32_MAX};
  return pat_data_asm_objects_001(NULL, 0) == 0u &&
         pat_data_asm_objects_001(one, 1) == UINT32_MAX;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) { return pattern_test_suite(); }
