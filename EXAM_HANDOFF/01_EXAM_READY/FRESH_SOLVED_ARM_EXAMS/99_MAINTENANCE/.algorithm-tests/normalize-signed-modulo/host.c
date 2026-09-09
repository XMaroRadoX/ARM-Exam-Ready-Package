#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Normalize signed modulo into a nonnegative result
 * Contract: Require modulus>0. Return the unique result in 0..modulus-1 that is congruent to value. Invalid input returns 0 without writing.
 * Method:
 * 1. Calculate the C signed remainder.
 * 2. Add modulus if the remainder is negative.
 * 3. Store the normalized result.
 */
int normalized_modulo_i32(int32_t value, int32_t modulus,
                          int32_t *result_out) {
  if (!result_out || modulus<=0) return 0;
  int32_t result=value%modulus;
  if(result<0) result+=modulus;
  *result_out=result;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int normalized_modulo_i32(int32_t value, int32_t modulus, int32_t *result_out);
int test_main(void) {
int32_t out=77;CHECK(normalized_modulo_i32(-17,5,&out)&&out==3);
CHECK(normalized_modulo_i32(17,5,&out)&&out==2);
out=77;CHECK(!normalized_modulo_i32(3,0,&out)&&out==77);
CHECK(!normalized_modulo_i32(3,5,0));
return 0;
}

int main(void){return test_main();}
