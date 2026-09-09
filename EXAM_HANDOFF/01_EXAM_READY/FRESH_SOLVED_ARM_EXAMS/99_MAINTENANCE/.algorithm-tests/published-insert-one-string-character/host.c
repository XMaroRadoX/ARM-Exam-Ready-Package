#include <limits.h>
#include <stddef.h>
#include <stdint.h>
/* Exam prompt: Insert one character at an index
 * Contract: Insert one non-NUL byte before index, where index may equal length. Require
 * a valid current terminator and one spare byte. Invalid input writes nothing. Method:
 * 1. Validate all conditions.
 * 2. Shift the suffix including NUL one byte right.
 * 3. Store the character and increment length.
 */
int string_insert_character(uint8_t *text, uint32_t *length, uint32_t capacity,
                            uint32_t index, uint8_t character) {
  if (!text || !length || character == 0 || index > *length || *length >= capacity ||
      text[*length] != 0 || capacity - *length < 2)
    return 0;
  for (uint32_t i = *length + 1; i > index; --i)
    text[i] = text[i - 1];
  text[index] = character;
  ++*length;
  return 1;
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <limits.h>
#include <stddef.h>

int string_insert_character(uint8_t *text, uint32_t *length, uint32_t capacity,
                            uint32_t index, uint8_t character);
int test_main(void) {
  uint8_t a[6] = "ARM";
  uint32_t n = 3;
  CHECK(string_insert_character(a, &n, 6, 1, 'X'));
  CHECK(n == 4 && a[0] == 'A' && a[1] == 'X' && a[2] == 'R' && a[4] == 0);
  CHECK(!string_insert_character(a, &n, 5, 0, 'Y') && n == 4);
  CHECK(!string_insert_character(a, &n, 6, 5, 'Y') && n == 4);
  return 0;
}

int main(void){return test_main();}
