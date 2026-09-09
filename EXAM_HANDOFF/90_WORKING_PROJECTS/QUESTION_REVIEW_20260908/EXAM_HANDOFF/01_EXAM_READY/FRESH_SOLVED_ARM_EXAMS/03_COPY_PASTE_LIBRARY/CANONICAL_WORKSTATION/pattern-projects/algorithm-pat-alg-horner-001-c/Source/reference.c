#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Horner polynomial evaluation.
 * Recognition cue: evaluate polynomial with multiply accumulate.
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
int64_t algorithm_algorithm_pat_alg_horner_001_c(const int32_t *c, uint32_t n, int32_t x) {
  uint64_t y=0;
  if(!c)return 0;
  while(n)y=y*(uint64_t)(int64_t)x+(uint64_t)(int64_t)c[--n];
  if(y<=INT64_MAX)return (int64_t)y;
  return INT64_MIN+(int64_t)(y-(UINT64_C(1)<<63));
}

int algorithm_algorithm_pat_alg_horner_001_c_checked(const int32_t *c, uint32_t n, int32_t x, int64_t *out) {
  if(!out||(!c&&n))return 0;
  int64_t y=0;
  while(n){
    if(x==-1){if(y==INT64_MIN)return 0;y=-y;}
    else {
      if(x>0&&(y>INT64_MAX/x||y<INT64_MIN/x))return 0;
      if(x< -1&&((y>0&&y>INT64_MIN/x)||(y<0&&y<INT64_MAX/x)))return 0;
      y*=x;
    }
    int32_t term=c[--n];
    if((term>0&&y>INT64_MAX-term)||(term<0&&y<INT64_MIN-term))return 0;
    y+=term;
  }
  *out=y;return 1;
}

