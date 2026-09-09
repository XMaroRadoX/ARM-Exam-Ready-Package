#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int32_t string_count_ascii_words(const uint8_t *text, uint32_t capacity);
int test_main(void) {
uint8_t a[]=" ARM\tC  ASM\n",empty[]="",bad[]={'A','B'};
CHECK(string_count_ascii_words(a,sizeof a)==3);
CHECK(string_count_ascii_words(empty,1)==0);
CHECK(string_count_ascii_words(bad,2)==-1);
CHECK(string_count_ascii_words(0,2)==-1);
return 0;
}
