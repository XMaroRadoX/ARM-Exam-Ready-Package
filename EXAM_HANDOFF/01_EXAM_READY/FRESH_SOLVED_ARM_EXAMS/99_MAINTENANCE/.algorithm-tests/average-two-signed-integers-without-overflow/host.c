#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Average two signed integers without overflow
 * Contract: Return (left+right)/2 with C signed-division semantics: truncate toward zero. The addition is formed as a signed 64-bit value, so opposite and extreme inputs cannot overflow.
 * Method:
 * 1. Form the two-word signed sum.
 * 2. If a negative sum is odd, add one before shifting.
 * 3. Arithmetic-shift the 64-bit sum right once.
 */
int32_t average_two_i32(int32_t left, int32_t right) {
  return (int32_t)(((int64_t)left + right) / 2);
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int32_t average_two_i32(int32_t left, int32_t right);
int test_main(void) {
CHECK(average_two_i32(INT32_MIN,INT32_MAX)==0);
CHECK(average_two_i32(INT32_MAX,INT32_MAX)==INT32_MAX);
CHECK(average_two_i32(-8,-5)==-6);
CHECK(average_two_i32(8,5)==6);
return 0;
}

int main(void){return test_main();}
