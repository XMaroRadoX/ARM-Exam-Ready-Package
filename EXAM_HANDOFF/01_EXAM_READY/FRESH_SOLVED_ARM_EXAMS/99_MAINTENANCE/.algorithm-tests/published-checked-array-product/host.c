#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Checked array product
 * Contract: Multiply signed words into an int32_t result. The empty product is one.
 * Return 0 without writing if an input is invalid or any multiplication leaves the
 * signed 32-bit range. Method:
 * 1. Validate pointers.
 * 2. Start the product at one.
 * 3. Form each product in 64 bits.
 * 4. Reject it unless the high word is the sign extension of the low word.
 */
int checked_array_product(const int32_t *values, uint32_t count, int32_t *product_out) {
  if (!product_out || (!values && count != 0))
    return 0;
  int32_t product = 1;
  for (uint32_t i = 0; i < count; ++i) {
    int64_t wide = (int64_t)product * values[i];
    if (wide < INT32_MIN || wide > INT32_MAX)
      return 0;
    product = (int32_t)wide;
  }
  *product_out = product;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int checked_array_product(const int32_t *values, uint32_t count, int32_t *product_out);
int test_main(void) {
  int32_t a[] = {-2, 3, 4}, b[] = {INT32_MAX, 2}, p = 77;
  CHECK(checked_array_product(a, 3, &p) && p == -24);
  CHECK(checked_array_product(0, 0, &p) && p == 1);
  p = 77;
  CHECK(!checked_array_product(b, 2, &p) && p == 77);
  CHECK(!checked_array_product(0, 1, &p) && p == 77);
  return 0;
}

int main(void){return test_main();}
