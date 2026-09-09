#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Test one bit
 * Contract: Accept bit indexes 0..31. Return 1 and the requested result, or return 0 without writing for an invalid index or null output.
 * Method:
 * 1. Validate the index and output.
 * 2. Build or select the requested one-bit mask.
 * 3. Store the exact 32-bit result.
 */
int test_bit_u32(uint32_t value, uint32_t index,
                 uint32_t *result_out) {
  if(index>=32 || !result_out) return 0;
  *result_out=(value >> index) & 1u;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int test_bit_u32(uint32_t value, uint32_t index, uint32_t *result_out);
int test_main(void) {
uint32_t out=77;CHECK(test_bit_u32(0x80000008u,31,&out)&&out==1);
out=77;CHECK(!test_bit_u32(8,32,&out)&&out==77);CHECK(!test_bit_u32(8,3,0));
return 0;
}

int main(void){return test_main();}
