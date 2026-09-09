#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int string_insert_character(uint8_t *text, uint32_t *length,
                            uint32_t capacity, uint32_t index,
                            uint8_t character);
int test_main(void) {
uint8_t a[6]="ARM";uint32_t n=3;CHECK(string_insert_character(a,&n,6,1,'X'));
CHECK(n==4&&a[0]=='A'&&a[1]=='X'&&a[2]=='R'&&a[4]==0);
CHECK(!string_insert_character(a,&n,5,0,'Y')&&n==4);
CHECK(!string_insert_character(a,&n,6,5,'Y')&&n==4);
return 0;
}
