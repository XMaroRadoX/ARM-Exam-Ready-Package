#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Delete an array element at an index
 * Contract: Delete index and return the removed value. Require a nonempty valid array, index<length, and a valid output. Invalid input returns 0 without writes.
 * Method:
 * 1. Validate and save the removed value.
 * 2. Shift later elements left.
 * 3. Decrement length and publish the removed value.
 */
int array_delete_at(int32_t *values, uint32_t *length,
                    uint32_t index, int32_t *removed_out) {
  if (!values || !length || !removed_out || index >= *length) return 0;
  int32_t removed = values[index];
  for (uint32_t i = index + 1; i < *length; ++i) values[i - 1] = values[i];
  --*length;
  *removed_out = removed;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int array_delete_at(int32_t *values, uint32_t *length,
                    uint32_t index, int32_t *removed_out);
int test_main(void) {
int32_t a[]={3,8,5,7,77};uint32_t n=4;int32_t removed=99;
CHECK(array_delete_at(a,&n,1,&removed)&&n==3&&removed==8);
CHECK(a[0]==3&&a[1]==5&&a[2]==7&&a[4]==77);
removed=99;CHECK(!array_delete_at(a,&n,3,&removed)&&removed==99&&n==3);
return 0;
}

int main(void){return test_main();}
