#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Insert an array element at an index
 * Contract: Insert before index, where index may equal the old length. Require length<capacity, index<=length, and valid storage. Invalid input returns 0 without changing the array or length.
 * Method:
 * 1. Validate every condition before writing.
 * 2. Shift the suffix right from the end.
 * 3. Store the new value and increment length.
 */
int array_insert_at(int32_t *values, uint32_t *length,
                    uint32_t capacity, uint32_t index, int32_t value) {
  if (!values || !length || *length >= capacity || index > *length) return 0;
  for (uint32_t i = *length; i > index; --i) values[i] = values[i - 1];
  values[index] = value;
  ++*length;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int array_insert_at(int32_t *values, uint32_t *length,
                    uint32_t capacity, uint32_t index, int32_t value);
int test_main(void) {
int32_t a[]={3,5,7,99,77};uint32_t n=3;
CHECK(array_insert_at(a,&n,4,1,8)&&n==4);
CHECK(a[0]==3&&a[1]==8&&a[2]==5&&a[3]==7&&a[4]==77);
CHECK(!array_insert_at(a,&n,4,0,1)&&n==4);
CHECK(!array_insert_at(a,&n,5,5,1)&&n==4);
return 0;
}

int main(void){return test_main();}
