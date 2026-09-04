#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_transpose(const int *a, size_t r, size_t c, int *out) {
  if (!r || !c)
    return 1;
  if (!a || !out || a == out || r > 0x3fffffffu / c)
    return 0;
  for (size_t i = 0; i < r; i++)
    for (size_t j = 0; j < c; j++)
      out[j * r + i] = a[i * c + j];
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int matrix_transpose(const int *in, size_t rows, size_t cols, int *out);
int test_main(void) {
  int a[] = {1, 2, 3, 4, 5, 6}, o[7] = {0};
  o[6] = 77;
  CHECK(matrix_transpose(a, 2, 3, o) && o[0] == 1 && o[1] == 4 && o[4] == 3 &&
        o[5] == 6 && o[6] == 77);
  CHECK(!matrix_transpose(a, 2, 3, a));
  CHECK(matrix_transpose(0, 0, 4, 0));
  return 0;
}

int main(void){return test_main();}
