#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t format_i32(int32_t v,char*out,uint32_t cap){char d[12];uint32_t x=v<0?(uint32_t)(-(int64_t)v):(uint32_t)v,n=0,k=0;do{d[n++]=(char)(48+x%10);x/=10;}while(x);uint32_t len=n+(v<0);if(!out||cap<=len)return 0;if(v<0)out[k++]=45;while(n)out[k++]=d[--n];out[k]=0;return k;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint32_t format_i32(int32_t value, char *out, uint32_t capacity);
int test_main(void) {
char s[13]={0};s[12]=77;CHECK(format_i32(INT32_MIN,s,12)==11&&s[0]==45&&s[10]==56&&s[11]==0&&s[12]==77);s[0]=88;CHECK(!format_i32(-120,s,4)&&s[0]==88);CHECK(format_i32(0,s,2)==1&&s[0]==48&&s[1]==0);
return 0;
}

int main(void){return test_main();}
