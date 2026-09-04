#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Population count and parity.
 * Recognition cue: count set bits parity.
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

uint32_t pat_alg_popcount_parity_001(uint32_t value);

uint32_t pat_alg_popcount_parity_001_parity(uint32_t value);



static int pattern_core_vector(void) {
  return pat_alg_popcount_parity_001(0xf0f0u) == 8;
}
static int pattern_edge_vectors(void) {
  return pat_alg_popcount_parity_001(0) == 0 &&
         pat_alg_popcount_parity_001(UINT32_MAX) == 32 &&
         pat_alg_popcount_parity_001_parity(7) == 1 &&
         pat_alg_popcount_parity_001_parity(3) == 0;
}
int pattern_test_suite(void) {
  if (!pattern_core_vector())
    return __LINE__;
  if (!pattern_edge_vectors())
    return __LINE__;
  return 0;
}
int test_main(void) {
{
CHECK(pat_alg_popcount_parity_001(0u)==0u);
CHECK(pat_alg_popcount_parity_001(1u)==1u);
CHECK(pat_alg_popcount_parity_001(2u)==1u);
CHECK(pat_alg_popcount_parity_001(9u)==2u);
CHECK(pat_alg_popcount_parity_001(10u)==2u);
CHECK(pat_alg_popcount_parity_001(123321u)==10u);
CHECK(pat_alg_popcount_parity_001(4000000004u)==14u);
CHECK(pat_alg_popcount_parity_001(4294967295u)==32u);
CHECK(pat_alg_popcount_parity_001(264951055u)==17u);
CHECK(pat_alg_popcount_parity_001(3302568628u)==15u);
CHECK(pat_alg_popcount_parity_001(1461547428u)==16u);
CHECK(pat_alg_popcount_parity_001(4165108330u)==13u);
CHECK(pat_alg_popcount_parity_001(999144594u)==17u);
CHECK(pat_alg_popcount_parity_001(4017729701u)==19u);
CHECK(pat_alg_popcount_parity_001(969213969u)==11u);
CHECK(pat_alg_popcount_parity_001(3989968933u)==15u);
CHECK(pat_alg_popcount_parity_001(1681659299u)==14u);
CHECK(pat_alg_popcount_parity_001(1137519360u)==12u);
CHECK(pat_alg_popcount_parity_001(1940529389u)==16u);
CHECK(pat_alg_popcount_parity_001(3538678198u)==20u);
CHECK(pat_alg_popcount_parity_001(3395160109u)==14u);
CHECK(pat_alg_popcount_parity_001(924203215u)==17u);
CHECK(pat_alg_popcount_parity_001(3951801352u)==15u);
CHECK(pat_alg_popcount_parity_001(3065865433u)==19u);
CHECK(pat_alg_popcount_parity_001(2864782762u)==15u);
CHECK(pat_alg_popcount_parity_001(1356993055u)==13u);
CHECK(pat_alg_popcount_parity_001(703953597u)==20u);
CHECK(pat_alg_popcount_parity_001(361964270u)==15u);
CHECK(pat_alg_popcount_parity_001(1958511902u)==16u);
CHECK(pat_alg_popcount_parity_001(1968465316u)==15u);
CHECK(pat_alg_popcount_parity_001(3810760418u)==16u);
CHECK(pat_alg_popcount_parity_001(3773631281u)==15u);
}
 return pattern_test_suite(); }
