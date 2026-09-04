#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int matrix_symmetric(const int32_t*a,uint32_t n){if(n>256||(!a&&n))return 0;for(uint32_t r=0;r<n;r++)for(uint32_t c=r+1;c<n;c++)if(a[r*n+c]!=a[c*n+r])return 0;return 1;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int matrix_symmetric(const int32_t *a, uint32_t n);
int test_main(void) {
int32_t a[]={1,2,2,3};CHECK(matrix_symmetric(a,2));a[2]=4;CHECK(!matrix_symmetric(a,2));CHECK(matrix_symmetric(0,0));CHECK(!matrix_symmetric(a,257));
return 0;
}

int main(void){return test_main();}
