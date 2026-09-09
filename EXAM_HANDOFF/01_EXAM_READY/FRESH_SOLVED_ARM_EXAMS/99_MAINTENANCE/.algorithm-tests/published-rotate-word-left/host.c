#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Rotate a 32-bit word left
 * Contract: Normalize amount modulo 32 and rotate without losing bits. A zero or
 * multiple-of-32 amount returns the original word. Method:
 * 1. Keep the low five amount bits.
 * 2. Combine opposite logical shifts in C.
 * 3. Use the ARM rotate instruction with the equivalent direction.
 */
uint32_t rotate_left_u32(uint32_t value, uint32_t amount) {
  amount &= 31u;
  return amount ? (value << amount) | (value >> (32u - amount)) : value;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

uint32_t rotate_left_u32(uint32_t value, uint32_t amount);
int test_main(void) {
  CHECK(rotate_left_u32(0x12345678u, 4) == 0x23456781u);
  CHECK(rotate_left_u32(0x12345678u, 0) == 0x12345678u);
  CHECK(rotate_left_u32(0x12345678u, 36) == 0x23456781u);
  return 0;
}

int main(void){return test_main();}
