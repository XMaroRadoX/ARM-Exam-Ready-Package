#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Delete one character at an index
 * Contract: Delete index, return the removed byte, and preserve NUL termination. Require index<length and text[length] to be NUL. Invalid input writes nothing.
 * Method:
 * 1. Validate and save the selected byte.
 * 2. Shift all later bytes including NUL left.
 * 3. Decrement length and publish the removed byte.
 */
int string_delete_character(uint8_t *text, uint32_t *length,
                            uint32_t index, uint8_t *removed_out) {
  if (!text || !length || !removed_out || index>=*length ||
      text[*length]!=0) return 0;
  uint8_t removed=text[index];
  for (uint32_t i=index;i<*length;++i) text[i]=text[i+1];
  --*length;
  *removed_out=removed;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int string_delete_character(uint8_t *text, uint32_t *length,
                            uint32_t index, uint8_t *removed_out);
int test_main(void) {
uint8_t a[6]="AXRM",removed=0;uint32_t n=4;
CHECK(string_delete_character(a,&n,1,&removed)&&removed=='X'&&n==3);
CHECK(a[0]=='A'&&a[1]=='R'&&a[2]=='M'&&a[3]==0);
removed=9;CHECK(!string_delete_character(a,&n,3,&removed)&&removed==9);
return 0;
}

int main(void){return test_main();}
