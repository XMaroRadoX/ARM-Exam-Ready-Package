#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Selection sort.
 * Recognition cue: select minimum and swap.
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
void pat_alg_selection_sort_001(int32_t *a, uint32_t n);



static int pattern_core_vector(void) {
  int32_t a[] = {3, -1, 2};
  pat_alg_selection_sort_001(a, 3);
  return a[0] == -1 && a[1] == 2 && a[2] == 3;
}
static int pattern_edge_vectors(void) {
  int32_t a[] = {2, 2, 1};
  pat_alg_selection_sort_001(a, 0);
  pat_alg_selection_sort_001(a, 3);
  return a[0] == 1 && a[1] == 2 && a[2] == 2;
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
{ int32_t property_a[]={987654};
pat_alg_selection_sort_001(property_a,0);
CHECK(property_a[0]==(987654LL));
}
{ int32_t property_a[]={7,987654};
pat_alg_selection_sort_001(property_a,1);
CHECK(property_a[0]==(7LL));
CHECK(property_a[1]==(987654LL));
}
{ int32_t property_a[]={3,3,3,987654};
pat_alg_selection_sort_001(property_a,3);
CHECK(property_a[0]==(3LL));
CHECK(property_a[1]==(3LL));
CHECK(property_a[2]==(3LL));
CHECK(property_a[3]==(987654LL));
}
{ int32_t property_a[]={2147483647,-2147483648,0,987654};
pat_alg_selection_sort_001(property_a,3);
CHECK(property_a[0]==(-2147483648LL));
CHECK(property_a[1]==(0LL));
CHECK(property_a[2]==(2147483647LL));
CHECK(property_a[3]==(987654LL));
}
{ int32_t property_a[]={0,1,2,3,4,5,6,7,8,9,10,11,987654};
pat_alg_selection_sort_001(property_a,12);
CHECK(property_a[0]==(0LL));
CHECK(property_a[1]==(1LL));
CHECK(property_a[2]==(2LL));
CHECK(property_a[3]==(3LL));
CHECK(property_a[4]==(4LL));
CHECK(property_a[5]==(5LL));
CHECK(property_a[6]==(6LL));
CHECK(property_a[7]==(7LL));
CHECK(property_a[8]==(8LL));
CHECK(property_a[9]==(9LL));
CHECK(property_a[10]==(10LL));
CHECK(property_a[11]==(11LL));
CHECK(property_a[12]==(987654LL));
}
{ int32_t property_a[]={11,10,9,8,7,6,5,4,3,2,1,0,987654};
pat_alg_selection_sort_001(property_a,12);
CHECK(property_a[0]==(0LL));
CHECK(property_a[1]==(1LL));
CHECK(property_a[2]==(2LL));
CHECK(property_a[3]==(3LL));
CHECK(property_a[4]==(4LL));
CHECK(property_a[5]==(5LL));
CHECK(property_a[6]==(6LL));
CHECK(property_a[7]==(7LL));
CHECK(property_a[8]==(8LL));
CHECK(property_a[9]==(9LL));
CHECK(property_a[10]==(10LL));
CHECK(property_a[11]==(11LL));
CHECK(property_a[12]==(987654LL));
}
{ int32_t property_a[]={-19,1,-1,987654};
pat_alg_selection_sort_001(property_a,3);
CHECK(property_a[0]==(-19LL));
CHECK(property_a[1]==(-1LL));
CHECK(property_a[2]==(1LL));
CHECK(property_a[3]==(987654LL));
}
{ int32_t property_a[]={-16,-8,-10,-19,14,987654};
pat_alg_selection_sort_001(property_a,5);
CHECK(property_a[0]==(-19LL));
CHECK(property_a[1]==(-16LL));
CHECK(property_a[2]==(-10LL));
CHECK(property_a[3]==(-8LL));
CHECK(property_a[4]==(14LL));
CHECK(property_a[5]==(987654LL));
}
{ int32_t property_a[]={-2,-16,-16,20,20,9,6,15,987654};
pat_alg_selection_sort_001(property_a,8);
CHECK(property_a[0]==(-16LL));
CHECK(property_a[1]==(-16LL));
CHECK(property_a[2]==(-2LL));
CHECK(property_a[3]==(6LL));
CHECK(property_a[4]==(9LL));
CHECK(property_a[5]==(15LL));
CHECK(property_a[6]==(20LL));
CHECK(property_a[7]==(20LL));
CHECK(property_a[8]==(987654LL));
}
{ int32_t property_a[]={-18,-6,9,-5,17,-3,3,7,17,17,12,-11,-20,987654};
pat_alg_selection_sort_001(property_a,13);
CHECK(property_a[0]==(-20LL));
CHECK(property_a[1]==(-18LL));
CHECK(property_a[2]==(-11LL));
CHECK(property_a[3]==(-6LL));
CHECK(property_a[4]==(-5LL));
CHECK(property_a[5]==(-3LL));
CHECK(property_a[6]==(3LL));
CHECK(property_a[7]==(7LL));
CHECK(property_a[8]==(9LL));
CHECK(property_a[9]==(12LL));
CHECK(property_a[10]==(17LL));
CHECK(property_a[11]==(17LL));
CHECK(property_a[12]==(17LL));
CHECK(property_a[13]==(987654LL));
}
{ int32_t property_a[]={-1,-8,-10,-5,-14,-14,-7,11,6,-11,2,12,-10,11,-14,16,17,-13,18,-9,987654};
pat_alg_selection_sort_001(property_a,20);
CHECK(property_a[0]==(-14LL));
CHECK(property_a[1]==(-14LL));
CHECK(property_a[2]==(-14LL));
CHECK(property_a[3]==(-13LL));
CHECK(property_a[4]==(-11LL));
CHECK(property_a[5]==(-10LL));
CHECK(property_a[6]==(-10LL));
CHECK(property_a[7]==(-9LL));
CHECK(property_a[8]==(-8LL));
CHECK(property_a[9]==(-7LL));
CHECK(property_a[10]==(-5LL));
CHECK(property_a[11]==(-1LL));
CHECK(property_a[12]==(2LL));
CHECK(property_a[13]==(6LL));
CHECK(property_a[14]==(11LL));
CHECK(property_a[15]==(11LL));
CHECK(property_a[16]==(12LL));
CHECK(property_a[17]==(16LL));
CHECK(property_a[18]==(17LL));
CHECK(property_a[19]==(18LL));
CHECK(property_a[20]==(987654LL));
}
}
 return pattern_test_suite(); }
