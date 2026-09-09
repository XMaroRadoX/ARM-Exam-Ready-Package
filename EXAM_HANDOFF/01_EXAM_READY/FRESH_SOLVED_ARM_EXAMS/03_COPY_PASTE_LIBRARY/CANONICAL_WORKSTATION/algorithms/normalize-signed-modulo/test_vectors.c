#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int normalized_modulo_i32(int32_t value, int32_t modulus, int32_t *result_out);
int test_main(void) {
  int32_t out = 77;
  CHECK(normalized_modulo_i32(-17, 5, &out) && out == 3);
  CHECK(normalized_modulo_i32(17, 5, &out) && out == 2);
  out = 77;
  CHECK(!normalized_modulo_i32(3, 0, &out) && out == 77);
  CHECK(!normalized_modulo_i32(3, 5, 0));
  return 0;
}
