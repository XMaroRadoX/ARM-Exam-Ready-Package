#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int matrix_swap_rows_i32(int32_t *matrix, uint32_t rows, uint32_t columns,
                      uint32_t first, uint32_t second);
int test_main(void) {
int32_t a[]={1,2,3,4,5,6};CHECK(matrix_swap_rows_i32(a,2,3,0,1));
CHECK(a[0]==4&&a[1]==5&&a[2]==6&&a[3]==1&&a[5]==3);
int32_t before=a[0];CHECK(!matrix_swap_rows_i32(a,2,3,0,3)&&a[0]==before);
return 0;
}
