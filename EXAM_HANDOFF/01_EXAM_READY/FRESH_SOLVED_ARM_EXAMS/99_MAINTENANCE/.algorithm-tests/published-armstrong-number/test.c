#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int armstrong_number(uint32_t n);
int test_main(void) {
  CHECK(armstrong_number(0));
  CHECK(armstrong_number(153));
  CHECK(armstrong_number(9474));
  CHECK(!armstrong_number(154));
  CHECK(!armstrong_number(4294967295u));
  return 0;
}
