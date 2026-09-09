#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Test whether an integer is a power of two
 * Contract: Return 1 only for positive unsigned values containing exactly one set bit. Zero is not a power of two.
 * Method:
 * 1. Reject zero.
 * 2. Clear the lowest set bit with value & (value-1).
 * 3. A zero remainder means exactly one bit was set.
 */
int is_power_of_two_u32(uint32_t value) {
  return value!=0 && (value&(value-1u))==0;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int is_power_of_two_u32(uint32_t value);
int test_main(void) {
CHECK(is_power_of_two_u32(1));CHECK(is_power_of_two_u32(16));
CHECK(is_power_of_two_u32(0)==0);CHECK(is_power_of_two_u32(18)==0);
CHECK(is_power_of_two_u32(0x80000000u));
return 0;
}

int main(void){return test_main();}
