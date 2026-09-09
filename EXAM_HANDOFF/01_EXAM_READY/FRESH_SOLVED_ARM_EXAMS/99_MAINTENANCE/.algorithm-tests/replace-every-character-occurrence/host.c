#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Replace every occurrence of a character
 * Contract: Replace every old_character before NUL and return the replacement count. Both characters must be non-NUL. Invalid or unterminated input returns UINT32_MAX without modifying text.
 * Method:
 * 1. Validate the bounded length first.
 * 2. Scan exactly the characters before NUL.
 * 3. Replace matches and count them.
 */
uint32_t string_replace_character(uint8_t *text, uint32_t capacity,
                                  uint8_t old_character,
                                  uint8_t new_character) {
  if (!text || !old_character || !new_character) return UINT32_MAX;
  uint32_t length=0;
  while (length<capacity && text[length]) ++length;
  if (length==capacity) return UINT32_MAX;
  uint32_t replaced=0;
  for (uint32_t i=0;i<length;++i)
    if (text[i]==old_character) { text[i]=new_character; ++replaced; }
  return replaced;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
uint32_t string_replace_character(uint8_t *text, uint32_t capacity,
                                  uint8_t old_character, uint8_t new_character);
int test_main(void) {
uint8_t a[]="BANANA",bad[]={'A','A'};CHECK(string_replace_character(a,7,'A','X')==3);
CHECK(a[0]=='B'&&a[1]=='X'&&a[5]=='X'&&a[6]==0);
CHECK(string_replace_character(bad,2,'A','X')==UINT32_MAX&&bad[0]=='A');
CHECK(string_replace_character(a,7,0,'X')==UINT32_MAX);
return 0;
}

int main(void){return test_main();}
