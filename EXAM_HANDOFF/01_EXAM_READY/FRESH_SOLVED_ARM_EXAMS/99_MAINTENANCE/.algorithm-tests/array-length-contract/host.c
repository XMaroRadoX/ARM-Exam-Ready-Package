#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int bounded_word_length(const uint32_t*a,uint32_t capacity,uint32_t sentinel,uint32_t*length){if(!a||!length)return 0;for(uint32_t i=0;i<capacity;i++)if(a[i]==sentinel){*length=i;return 1;}return 0;}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int bounded_word_length(const uint32_t *a, uint32_t capacity, uint32_t sentinel, uint32_t *length);
int test_main(void) {
uint32_t a[]={4,7,0,9},b[]={4,7,9},length=99;size_t count=sizeof a/sizeof a[0];CHECK(count==4);CHECK(bounded_word_length(a,(uint32_t)count,0,&length)&&length==2);length=99;CHECK(!bounded_word_length(b,3,0,&length)&&length==99);CHECK(!bounded_word_length(0,0,0,&length)&&length==99);
return 0;
}

int main(void){return test_main();}
