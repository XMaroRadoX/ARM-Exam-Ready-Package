#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Concatenate bounded strings
 * Contract: Append source to destination. destination[length] must be NUL, source must terminate within source_capacity, and the final NUL must fit. Validate everything before writing.
 * Method:
 * 1. Validate destination state.
 * 2. Find the bounded source length.
 * 3. Check length+source_length+1 against capacity.
 * 4. Copy source including NUL and update length.
 */
static int string_length_for_concat(const uint8_t *text, uint32_t capacity,
                                    uint32_t *length) {
  if (!text || !length) return 0;
  for (uint32_t i=0;i<capacity;++i)
    if (text[i]==0) { *length=i; return 1; }
  return 0;
}
int string_concatenate_bounded(uint8_t *destination, uint32_t *length,
                               uint32_t capacity, const uint8_t *source,
                               uint32_t source_capacity) {
  if (!destination || !length || *length >= capacity ||
      destination[*length] != 0) return 0;
  uint32_t source_length;
  if (!string_length_for_concat(source,source_capacity,&source_length) ||
      source_length > capacity - *length - 1) return 0;
  for (uint32_t i=0;i<=source_length;++i)
    destination[*length+i]=source[i];
  *length += source_length;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
int string_concatenate_bounded(uint8_t *destination, uint32_t *length,
                               uint32_t capacity, const uint8_t *source,
                               uint32_t source_capacity);
int test_main(void) {
uint8_t a[8]="ARM",b[]="M3",bad[]={'X','Y'};uint32_t n=3;
CHECK(string_concatenate_bounded(a,&n,8,b,3)&&n==5);
CHECK(a[0]=='A'&&a[3]=='M'&&a[4]=='3'&&a[5]==0);
CHECK(!string_concatenate_bounded(a,&n,6,b,3)&&n==5);
CHECK(!string_concatenate_bounded(a,&n,8,bad,2)&&n==5);
return 0;
}

int main(void){return test_main();}
