#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int64_t dot_i16(const int16_t*a,const int16_t*b,uint32_t n){int64_t s=0;if(a&&b)for(uint32_t i=0;i<n;i++){s+=(int64_t)a[i]*b[i];}return s;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int64_t dot_i16(const int16_t *a, const int16_t *b, uint32_t n);
int test_main(void) {
int16_t a[]={-32768,-32768},b[]={-32768,-32768};CHECK(dot_i16(a,b,2)==2147483648LL);CHECK(dot_i16(0,0,0)==0);
return 0;
}

int main(void){return test_main();}
