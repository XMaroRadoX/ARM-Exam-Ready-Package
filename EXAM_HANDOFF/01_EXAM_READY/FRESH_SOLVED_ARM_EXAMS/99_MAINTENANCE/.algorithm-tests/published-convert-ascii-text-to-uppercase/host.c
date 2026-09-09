#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Convert ASCII text to uppercase
 * Contract: Convert ASCII letters in place; digits, punctuation, and non-ASCII bytes
 * remain unchanged. Missing NUL or invalid storage returns 0 before any mutation.
 * Method:
 * 1. Validate that NUL exists within capacity.
 * 2. Scan characters again.
 * 3. Add or subtract 32 only inside the relevant ASCII letter range.
 */
int string_to_ascii_uppercase(uint8_t *text, uint32_t capacity) {
  if (!text)
    return 0;
  uint32_t length = 0;
  while (length < capacity && text[length])
    ++length;
  if (length == capacity)
    return 0;
  for (uint32_t i = 0; i < length; ++i)
    if (text[i] >= 97 && text[i] <= 122)
      text[i] = (uint8_t)(text[i] + (-32));
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int string_to_ascii_uppercase(uint8_t *text, uint32_t capacity);
int test_main(void) {
  uint8_t a[] = "Arm-m3", bad[] = {'A', 'B'};
  CHECK(string_to_ascii_uppercase(a, sizeof a));
  CHECK(a[0] == 'A');
  CHECK(a[1] == 'R' && a[4] == 'M');
  CHECK(!string_to_ascii_uppercase(bad, 2) && bad[0] == 'A');
  return 0;
}

int main(void){return test_main();}
