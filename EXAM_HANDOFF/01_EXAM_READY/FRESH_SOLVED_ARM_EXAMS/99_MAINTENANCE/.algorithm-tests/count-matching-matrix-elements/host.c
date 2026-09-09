#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Count matching matrix elements
 * Contract: Count cells equal to target in a matrix with dimensions at most 256. A zero dimension returns zero and permits a null matrix pointer. Other invalid input returns zero.
 * Method:
 * 1. Validate dimensions.
 * 2. Convert dimensions to a bounded flat count.
 * 3. Scan and increment for exact signed equality.
 */
uint32_t matrix_count_matches_i32(const int32_t *matrix, uint32_t rows,
                                  uint32_t columns, int32_t target) {
  if(rows>256 || columns>256 || (!matrix && rows && columns)) return 0;
  uint32_t matches=0;
  for(uint32_t i=0;i<rows*columns;++i) if(matrix[i]==target) ++matches;
  return matches;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint32_t matrix_count_matches_i32(const int32_t *matrix, uint32_t rows, uint32_t columns, int32_t target);
int test_main(void) {
int32_t a[]={4,7,4,2,4,9};CHECK(matrix_count_matches_i32(a,2,3,4)==3);
CHECK(matrix_count_matches_i32(a,2,3,8)==0);
CHECK(matrix_count_matches_i32(0,0,3,4)==0);
CHECK(matrix_count_matches_i32(a,257,1,4)==0);
return 0;
}

int main(void){return test_main();}
