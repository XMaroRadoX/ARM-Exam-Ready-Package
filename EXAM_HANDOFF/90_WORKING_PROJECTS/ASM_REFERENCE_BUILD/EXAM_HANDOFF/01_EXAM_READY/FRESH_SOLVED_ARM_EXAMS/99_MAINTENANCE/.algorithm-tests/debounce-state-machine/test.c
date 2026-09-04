#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
typedef struct{uint8_t stable,candidate;uint16_t ticks;}Debounce;
int debounce_update(Debounce *s, uint8_t sample, uint16_t required, uint8_t *changed);
int test_main(void) {
Debounce s={0,0,0};uint8_t c=9;CHECK(debounce_update(&s,1,2,&c)&&!c);CHECK(debounce_update(&s,0,2,&c)&&!c);CHECK(debounce_update(&s,1,2,&c)&&!c);CHECK(debounce_update(&s,1,2,&c)&&c&&s.stable==1);CHECK(debounce_update(&s,0,1,&c)&&c&&!s.stable);
return 0;
}
