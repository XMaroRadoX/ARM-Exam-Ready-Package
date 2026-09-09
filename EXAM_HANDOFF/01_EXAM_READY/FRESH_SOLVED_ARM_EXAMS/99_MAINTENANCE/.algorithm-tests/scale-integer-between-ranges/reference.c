#include <stdint.h>
#include <stddef.h>
#include <limits.h>
/* Exam prompt: Scale an integer between ranges
 * Contract: Clamp value to input_min..input_max, then linearly map it to output_min..output_max. Input span must be positive and fit int32_t; output span must fit int32_t. Use a signed 64-bit product and truncate division toward zero. Invalid input writes nothing.
 * Method:
 * 1. Validate both spans and the output pointer.
 * 2. Clamp the input.
 * 3. Multiply input offset by output span in 64 bits.
 * 4. Divide by input span and add output_min.
 */
int scale_i32_between_ranges(int32_t value, int32_t input_min,
                             int32_t input_max, int32_t output_min,
                             int32_t output_max, int32_t *result_out) {
  if(!result_out) return 0;
  int64_t input_span=(int64_t)input_max-input_min;
  int64_t output_span=(int64_t)output_max-output_min;
  if(input_span<=0 || input_span>INT32_MAX ||
     output_span<INT32_MIN || output_span>INT32_MAX) return 0;
  if(value<input_min) value=input_min;
  if(value>input_max) value=input_max;
  int64_t scaled=((int64_t)(value-input_min)*output_span)/input_span;
  *result_out=(int32_t)(output_min+scaled);
  return 1;
}
