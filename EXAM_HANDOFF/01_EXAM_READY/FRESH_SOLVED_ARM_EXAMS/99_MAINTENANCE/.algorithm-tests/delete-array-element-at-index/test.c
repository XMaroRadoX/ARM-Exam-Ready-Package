#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
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
