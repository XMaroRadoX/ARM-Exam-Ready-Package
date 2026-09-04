#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Integer square root.
 * Recognition cue: floor square root without floating point.
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
uint32_t pat_alg_integer_sqrt_001(uint32_t n);



static int pattern_core_vector(void) {
  return pat_alg_integer_sqrt_001(0) == 0 &&
         pat_alg_integer_sqrt_001(15) == 3 && pat_alg_integer_sqrt_001(16) == 4;
}
static int pattern_edge_vectors(void) {
  return pat_alg_integer_sqrt_001(1) == 1 &&
         pat_alg_integer_sqrt_001(UINT32_MAX) == 65535u;
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
CHECK(pat_alg_integer_sqrt_001(0u)==0u);
CHECK(pat_alg_integer_sqrt_001(1u)==1u);
CHECK(pat_alg_integer_sqrt_001(2u)==1u);
CHECK(pat_alg_integer_sqrt_001(9u)==3u);
CHECK(pat_alg_integer_sqrt_001(10u)==3u);
CHECK(pat_alg_integer_sqrt_001(123321u)==351u);
CHECK(pat_alg_integer_sqrt_001(4000000004u)==63245u);
CHECK(pat_alg_integer_sqrt_001(4294967295u)==65535u);
CHECK(pat_alg_integer_sqrt_001(264951055u)==16277u);
CHECK(pat_alg_integer_sqrt_001(3302568628u)==57467u);
CHECK(pat_alg_integer_sqrt_001(1461547428u)==38230u);
CHECK(pat_alg_integer_sqrt_001(4165108330u)==64537u);
CHECK(pat_alg_integer_sqrt_001(999144594u)==31609u);
CHECK(pat_alg_integer_sqrt_001(4017729701u)==63385u);
CHECK(pat_alg_integer_sqrt_001(969213969u)==31132u);
CHECK(pat_alg_integer_sqrt_001(3989968933u)==63166u);
CHECK(pat_alg_integer_sqrt_001(1681659299u)==41008u);
CHECK(pat_alg_integer_sqrt_001(1137519360u)==33727u);
CHECK(pat_alg_integer_sqrt_001(1940529389u)==44051u);
CHECK(pat_alg_integer_sqrt_001(3538678198u)==59486u);
CHECK(pat_alg_integer_sqrt_001(3395160109u)==58268u);
CHECK(pat_alg_integer_sqrt_001(924203215u)==30400u);
CHECK(pat_alg_integer_sqrt_001(3951801352u)==62863u);
CHECK(pat_alg_integer_sqrt_001(3065865433u)==55370u);
CHECK(pat_alg_integer_sqrt_001(2864782762u)==53523u);
CHECK(pat_alg_integer_sqrt_001(1356993055u)==36837u);
CHECK(pat_alg_integer_sqrt_001(703953597u)==26532u);
CHECK(pat_alg_integer_sqrt_001(361964270u)==19025u);
CHECK(pat_alg_integer_sqrt_001(1958511902u)==44255u);
CHECK(pat_alg_integer_sqrt_001(1968465316u)==44367u);
CHECK(pat_alg_integer_sqrt_001(3810760418u)==61731u);
CHECK(pat_alg_integer_sqrt_001(3773631281u)==61429u);
}
 return pattern_test_suite(); }
