"""Fundamental array prompts with matching C, ARMASM, traces, and tests."""
from algorithm_catalog import add

FAMILY = 'Arrays and matrices'


def entry(slug, title, group, prototype, contract, method, trace, c_code,
          asm_code, tests, complexity='O(count) time; O(1) auxiliary storage',
          helpers='', registers=''):
    teaching_comment = ('/* Exam prompt: ' + title + '\n * Contract: ' + contract +
                        '\n * Method:\n * ' + method.replace('\n', '\n * ') + '\n */\n')
    add(slug, title, FAMILY, prototype, contract, method, trace, teaching_comment + c_code, asm_code,
        tests, complexity=complexity, helpers=helpers, registers=registers,
        fundamentals_group=group)


entry('checked-array-sum', 'Checked array sum', 'Count and measure',
'''int checked_array_sum(const int32_t *values, uint32_t count,
                      int64_t *sum_out)''',
'Sum signed words into a 64-bit result. count must not exceed INT32_MAX, which guarantees that every possible int32_t input sum fits int64_t. A zero-length array sums to zero and may have a null data pointer. Return 0 without writing for an invalid pointer or count.',
'1. Validate the output and count bound.\n2. Start a 64-bit accumulator at zero.\n3. Sign-extend and add each word.\n4. Store only after the complete scan.',
'For [-4,7,9], the accumulator changes 0 -> -4 -> 3 -> 12.',
'''int checked_array_sum(const int32_t *values, uint32_t count,
                      int64_t *sum_out) {
  /* INT32_MAX elements cannot overflow a signed 64-bit sum. */
  if (!sum_out || count > INT32_MAX || (!values && count != 0)) return 0;
  int64_t sum = 0;
  for (uint32_t i = 0; i < count; ++i) sum += values[i];
  *sum_out = sum;
  return 1;
}''',
'''; R0=values, R1=count, R2=sum_out. R3:R4 is the 64-bit sum.
cmp r2,#0 | beq cas_bad | cmp r1,#0 | bmi cas_bad | cmp r1,#0 | beq cas_empty | cmp r0,#0 | beq cas_bad | push {r4-r7,lr} | movs r3,#0 | movs r4,#0
cas_loop: | ldr r5,[r0],#4 | asr r6,r5,#31 | adds r3,r3,r5 | adc r4,r4,r6 | subs r1,#1 | bne cas_loop | str r3,[r2] | str r4,[r2,#4] | movs r0,#1 | pop {r4-r7,pc}
cas_empty: | movs r3,#0 | str r3,[r2] | str r3,[r2,#4] | movs r0,#1 | bx lr
cas_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={-4,7,9};int64_t s=99;
CHECK(checked_array_sum(a,3,&s)&&s==12);
CHECK(checked_array_sum(0,0,&s)&&s==0);
s=99;CHECK(!checked_array_sum(0,1,&s)&&s==99);
CHECK(!checked_array_sum(a,UINT32_MAX,&s)&&s==99);''')

entry('checked-array-product', 'Checked array product', 'Count and measure',
'int checked_array_product(const int32_t *values, uint32_t count, int32_t *product_out)',
'Multiply signed words into an int32_t result. The empty product is one. Return 0 without writing if an input is invalid or any multiplication leaves the signed 32-bit range.',
'1. Validate pointers.\n2. Start the product at one.\n3. Form each product in 64 bits.\n4. Reject it unless the high word is the sign extension of the low word.',
'For [-2,3,4], the product changes 1 -> -2 -> -6 -> -24.',
'''int checked_array_product(const int32_t *values, uint32_t count,
                          int32_t *product_out) {
  if (!product_out || (!values && count != 0)) return 0;
  int32_t product = 1;
  for (uint32_t i = 0; i < count; ++i) {
    int64_t wide = (int64_t)product * values[i];
    if (wide < INT32_MIN || wide > INT32_MAX) return 0;
    product = (int32_t)wide;
  }
  *product_out = product;
  return 1;
}''',
'''; R0=values, R1=count, R2=product_out. R3 holds the tentative product.
cmp r2,#0 | beq cap_bad | cmp r1,#0 | beq cap_empty | cmp r0,#0 | beq cap_bad | push {r4-r7,lr} | movs r3,#1
cap_loop: | ldr r4,[r0],#4 | smull r5,r6,r3,r4 | asr r7,r5,#31 | cmp r6,r7 | bne cap_fail | mov r3,r5 | subs r1,#1 | bne cap_loop | str r3,[r2] | movs r0,#1 | pop {r4-r7,pc}
cap_fail: | movs r0,#0 | pop {r4-r7,pc}
cap_empty: | movs r3,#1 | str r3,[r2] | movs r0,#1 | bx lr
cap_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={-2,3,4},b[]={INT32_MAX,2},p=77;
CHECK(checked_array_product(a,3,&p)&&p==-24);
CHECK(checked_array_product(0,0,&p)&&p==1);
p=77;CHECK(!checked_array_product(b,2,&p)&&p==77);
CHECK(!checked_array_product(0,1,&p)&&p==77);''')

entry('integer-array-mean', 'Integer array mean', 'Count and measure',
'int integer_array_mean(const int32_t *values, uint32_t count, int32_t *mean_out)',
'Return the arithmetic mean truncated toward zero. Require 1..INT32_MAX elements and valid pointers. The 64-bit sum prevents intermediate 32-bit overflow; invalid input returns 0 without writing.',
'1. Accumulate an exact signed 64-bit sum.\n2. Divide the signed sum by the positive count.\n3. Store the quotient, which always fits int32_t.',
'For [-8,3,4], sum=-1 and -1/3 truncates toward zero to 0.',
'''int integer_array_mean(const int32_t *values, uint32_t count,
                       int32_t *mean_out) {
  if (!values || !mean_out || count == 0 || count > INT32_MAX) return 0;
  int64_t sum = 0;
  for (uint32_t i = 0; i < count; ++i) sum += values[i];
  *mean_out = (int32_t)(sum / (int64_t)count);
  return 1;
}''',
'''; R0=values, R1=count, R2=mean_out. __aeabi_ldivmod receives R0:R1 / R2:R3.
cmp r0,#0 | beq iam_bad | cmp r2,#0 | beq iam_bad | cmp r1,#0 | beq iam_bad | bmi iam_bad | push {r4-r8,lr} | mov r4,r0 | mov r5,r1 | mov r6,r2 | movs r7,#0 | movs r8,#0 | mov r12,r5
iam_loop: | ldr r0,[r4],#4 | asr r1,r0,#31 | adds r7,r7,r0 | adc r8,r8,r1 | subs r12,#1 | bne iam_loop | mov r0,r7 | mov r1,r8 | mov r2,r5 | movs r3,#0 | bl __aeabi_ldivmod | str r0,[r6] | movs r0,#1 | pop {r4-r8,pc}
iam_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={-8,3,4},b[]={INT32_MAX,INT32_MAX},m=77;
CHECK(integer_array_mean(a,3,&m)&&m==0);
CHECK(integer_array_mean(b,2,&m)&&m==INT32_MAX);
m=77;CHECK(!integer_array_mean(a,0,&m)&&m==77);
CHECK(!integer_array_mean(0,3,&m)&&m==77);''',
helpers='IMPORT __aeabi_ldivmod')


def extreme(which):
    is_min = which == 'minimum'
    name = 'array_minimum' if is_min else 'array_maximum'
    op = '<' if is_min else '>'
    skip = 'bge' if is_min else 'ble'
    expected = -3 if is_min else 9
    entry('find-'+which+'-array-value', 'Find the '+which+' array value',
          'Count and measure',
          f'int {name}(const int32_t *values, uint32_t count, int32_t *value_out)',
          f'Return the {which} signed value. Empty input or a null required pointer returns 0 without writing. Equal values keep the first candidate.',
          '1. Seed the candidate from element zero.\n2. Scan remaining elements with signed comparisons.\n3. Replace it only for a strict improvement.',
          f'For [7,-3,9,-3], the {which} is {expected}.',
          f'''int {name}(const int32_t *values, uint32_t count,
                 int32_t *value_out) {{
  if (!values || !value_out || count == 0) return 0;
  int32_t best = values[0];
  for (uint32_t i = 1; i < count; ++i)
    if (values[i] {op} best) best = values[i];
  *value_out = best;
  return 1;
}}''',
          f'''; R0=values, R1=count, R2=value_out, R3=current best.
cmp r0,#0 | beq axe_bad | cmp r2,#0 | beq axe_bad | cmp r1,#0 | beq axe_bad | push {{r4,lr}} | ldr r3,[r0],#4 | subs r1,#1
axe_loop: | cmp r1,#0 | beq axe_done | ldr r4,[r0],#4 | cmp r4,r3 | {skip} axe_next | mov r3,r4
axe_next: | subs r1,#1 | b axe_loop
axe_done: | str r3,[r2] | movs r0,#1 | pop {{r4,pc}}
axe_bad: | movs r0,#0 | bx lr''',
          f'''int32_t a[]={{7,-3,9,-3}},v=77;
CHECK({name}(a,4,&v)&&v=={expected});
v=77;CHECK(!{name}(a,0,&v)&&v==77);
CHECK(!{name}(0,1,&v)&&v==77);''')


extreme('minimum')
extreme('maximum')


def count_kind(kind, condition, compare, expected):
    target = kind == 'target'
    names = {'target':'count_array_target','negative':'count_array_negative',
             'zero':'count_array_zero','positive':'count_array_positive'}
    titles = {'target':'Count occurrences of a target',
              'negative':'Count negative array values',
              'zero':'Count zero array values',
              'positive':'Count positive array values'}
    slugs = {'target':'count-target-occurrences',
             'negative':'count-negative-array-values',
             'zero':'count-zero-array-values',
             'positive':'count-positive-array-values'}
    name=names[kind]
    prototype=(f'uint32_t {name}(const int32_t *values, uint32_t count, int32_t target)'
               if target else f'uint32_t {name}(const int32_t *values, uint32_t count)')
    entry(slugs[kind], titles[kind], 'Count and measure', prototype,
          'Count matching signed words. A null pointer returns zero; the routine never writes memory.',
          '1. Start the count at zero.\n2. Test each element against the requested condition.\n3. Increment exactly once for each match.',
          f'For [-2,0,5,-7], the result is {expected}.',
          f'''{prototype} {{
  uint32_t matches = 0;
  if (!values) return 0;
  for (uint32_t i = 0; i < count; ++i)
    if ({condition}) ++matches;
  return matches;
}}''',
          f'''; R0=values, R1=count{', R2=target' if target else ''}. R4 is the count.
cmp r0,#0 | beq ack_zero | push {{r4,lr}} | movs r4,#0
ack_loop: | cmp r1,#0 | beq ack_done | ldr r3,[r0],#4 | {compare} | adds r4,#1
ack_next: | subs r1,#1 | b ack_loop
ack_done: | mov r0,r4 | pop {{r4,pc}}
ack_zero: | movs r0,#0 | bx lr''',
          f'''int32_t a[]={{-2,0,5,-7,{5 if target else 0}}};
CHECK({name}(a,{5 if target else 4}{',5' if target else ''})=={2 if target else expected});
CHECK({name}(0,4{',5' if target else ''})==0);
CHECK({name}(a,0{',5' if target else ''})==0);''')


count_kind('target','values[i] == target','cmp r3,r2 | bne ack_next',2)
count_kind('negative','values[i] < 0','cmp r3,#0 | bge ack_next',2)
count_kind('zero','values[i] == 0','cmp r3,#0 | bne ack_next',1)
count_kind('positive','values[i] > 0','cmp r3,#0 | ble ack_next',1)

entry('compare-arrays-for-equality', 'Compare two arrays for equality',
      'Compare and test',
'int arrays_equal(const int32_t *left, const int32_t *right, uint32_t count)',
'Return 1 when all count signed words are equal. Empty arrays are equal even with null pointers. A null pointer with a nonzero count returns 0.',
'1. Accept count zero immediately.\n2. Validate both bases.\n3. Stop on the first unequal pair.',
'[3,-1,8] equals [3,-1,8]; changing the final 8 to 7 makes it false.',
'''int arrays_equal(const int32_t *left, const int32_t *right,
                 uint32_t count) {
  if (count == 0) return 1;
  if (!left || !right) return 0;
  for (uint32_t i = 0; i < count; ++i)
    if (left[i] != right[i]) return 0;
  return 1;
}''',
'''; R0=left, R1=right, R2=count.
cmp r2,#0 | beq aeq_yes | cmp r0,#0 | beq aeq_no | cmp r1,#0 | beq aeq_no
aeq_loop: | ldr r3,[r0],#4 | ldr r12,[r1],#4 | cmp r3,r12 | bne aeq_no | subs r2,#1 | bne aeq_loop
aeq_yes: | movs r0,#1 | bx lr
aeq_no: | movs r0,#0 | bx lr''',
'''int32_t a[]={3,-1,8},b[]={3,-1,8},c[]={3,-1,7};
CHECK(arrays_equal(a,b,3));CHECK(!arrays_equal(a,c,3));
CHECK(arrays_equal(0,0,0));CHECK(!arrays_equal(0,b,3));''')

entry('lexicographic-signed-array-comparison',
      'Lexicographically compare two signed arrays', 'Compare and test',
'''int32_t arrays_compare_lexicographic(const int32_t *left, uint32_t left_count,
                                     const int32_t *right, uint32_t right_count)''',
'Return -1, 0, or 1 using signed element order, then shorter-prefix order. A null pointer is valid only with a zero count; invalid input returns 2.',
'1. Compare corresponding values up to the shorter count.\n2. Return at the first unequal signed pair.\n3. If the common prefix matches, compare lengths.',
'[1,9] is greater than [1,7,100] because 9 is greater than 7.',
'''int32_t arrays_compare_lexicographic(const int32_t *left,
                                     uint32_t left_count,
                                     const int32_t *right,
                                     uint32_t right_count) {
  if ((!left && left_count) || (!right && right_count)) return 2;
  uint32_t n = left_count < right_count ? left_count : right_count;
  for (uint32_t i = 0; i < n; ++i) {
    if (left[i] < right[i]) return -1;
    if (left[i] > right[i]) return 1;
  }
  return left_count < right_count ? -1 : left_count > right_count ? 1 : 0;
}''',
'''; R0=left, R1=left_count, R2=right, R3=right_count.
cmp r1,#0 | beq alc_right | cmp r0,#0 | beq alc_bad
alc_right: | cmp r3,#0 | beq alc_start | cmp r2,#0 | beq alc_bad
alc_start: | push {r4-r6,lr} | cmp r1,r3 | bls alc_left_short | mov r4,r3 | b alc_loop
alc_left_short: | mov r4,r1
alc_loop: | cmp r4,#0 | beq alc_lengths | ldr r5,[r0],#4 | ldr r6,[r2],#4 | cmp r5,r6 | blt alc_less | bgt alc_more | subs r4,#1 | b alc_loop
alc_lengths: | cmp r1,r3 | blt alc_less | bgt alc_more | movs r0,#0 | pop {r4-r6,pc}
alc_less: | mvn r0,#0 | pop {r4-r6,pc}
alc_more: | movs r0,#1 | pop {r4-r6,pc}
alc_bad: | movs r0,#2 | bx lr''',
'''int32_t a[]={1,9},b[]={1,7,100},c[]={1,9,0};
CHECK(arrays_compare_lexicographic(a,2,b,3)==1);
CHECK(arrays_compare_lexicographic(a,2,c,3)==-1);
CHECK(arrays_compare_lexicographic(a,2,a,2)==0);
CHECK(arrays_compare_lexicographic(0,1,a,2)==2);''')

entry('copy-array-safely-with-overlap', 'Copy an array safely with overlap',
      'Copy and move',
'''int array_copy_overlap(int32_t *destination, uint32_t capacity,
                       const int32_t *source, uint32_t count)''',
'Copy count words with memmove semantics. Require capacity>=count and valid nonempty pointers. Exact aliasing succeeds. Direction is chosen before writing so overlapping slices are preserved.',
'1. Validate capacity and pointers.\n2. Copy forward when safe.\n3. Copy backward when destination begins inside the source range.',
'Moving [1,2,3,4] one place right produces [1,1,2,3,4].',
'''int array_copy_overlap(int32_t *destination, uint32_t capacity,
                       const int32_t *source, uint32_t count) {
  if (capacity < count || ((!destination || !source) && count)) return 0;
  if (count == 0 || destination == source) return 1;
  uintptr_t d = (uintptr_t)destination, s = (uintptr_t)source;
  if (d < s || d - s >= (uintptr_t)count * sizeof(*source)) {
    for (uint32_t i = 0; i < count; ++i) destination[i] = source[i];
  } else {
    for (uint32_t i = count; i != 0; --i) destination[i - 1] = source[i - 1];
  }
  return 1;
}''',
'''; R0=destination, R1=capacity, R2=source, R3=count.
cmp r1,r3 | blo aco_bad | cmp r3,#0 | beq aco_yes | cmp r0,#0 | beq aco_bad | cmp r2,#0 | beq aco_bad | cmp r0,r2 | beq aco_yes | blo aco_forward | sub r12,r0,r2 | cmp r12,r3,lsl #2 | bhs aco_forward | add r0,r0,r3,lsl #2 | add r2,r2,r3,lsl #2
aco_backward: | ldr r12,[r2,#-4]! | str r12,[r0,#-4]! | subs r3,#1 | bne aco_backward | b aco_yes
aco_forward: | ldr r12,[r2],#4 | str r12,[r0],#4 | subs r3,#1 | bne aco_forward
aco_yes: | movs r0,#1 | bx lr
aco_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={1,2,3,4,9},b[]={7,8,9};
CHECK(array_copy_overlap(a+1,4,a,4)&&a[0]==1&&a[1]==1&&a[4]==4);
CHECK(array_copy_overlap(b,3,b,3)&&b[2]==9);
CHECK(!array_copy_overlap(b,2,a,3));CHECK(array_copy_overlap(0,0,0,0));''')

entry('fill-array-with-one-value', 'Fill an array with one value', 'Transform',
'int array_fill(int32_t *values, uint32_t count, int32_t fill_value)',
'Store fill_value in every element. Empty input succeeds without dereferencing the pointer; a null pointer with nonzero count fails.',
'1. Validate the base when count is nonzero.\n2. Store the same word and advance.\n3. Stop after exactly count stores.',
'Filling four elements with -3 produces [-3,-3,-3,-3].',
'''int array_fill(int32_t *values, uint32_t count, int32_t fill_value) {
  if (!values && count) return 0;
  for (uint32_t i = 0; i < count; ++i) values[i] = fill_value;
  return 1;
}''',
'''; R0=values, R1=count, R2=fill_value.
cmp r1,#0 | beq afl_yes | cmp r0,#0 | beq afl_bad
afl_loop: | str r2,[r0],#4 | subs r1,#1 | bne afl_loop
afl_yes: | movs r0,#1 | bx lr
afl_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={1,2,3,4,77};CHECK(array_fill(a,4,-3));
CHECK(a[0]==-3&&a[3]==-3&&a[4]==77);
CHECK(array_fill(0,0,9));CHECK(!array_fill(0,1,9));''')

entry('swap-two-indexed-elements', 'Swap two indexed elements', 'Transform',
'int array_swap_indexes(int32_t *values, uint32_t count, uint32_t first, uint32_t second)',
'Swap two elements only when both indexes are in range and storage is valid. Equal indexes are a successful no-op. Invalid input returns 0 without writing.',
'1. Validate the pointer and both indexes.\n2. Load both words before storing.\n3. Store each word into the other position.',
'Swapping indexes 1 and 3 of [4,5,6,7] produces [4,7,6,5].',
'''int array_swap_indexes(int32_t *values, uint32_t count,
                       uint32_t first, uint32_t second) {
  if (!values || first >= count || second >= count) return 0;
  int32_t temporary = values[first];
  values[first] = values[second];
  values[second] = temporary;
  return 1;
}''',
'''; R0=values, R1=count, R2=first, R3=second.
cmp r0,#0 | beq asi_bad | cmp r2,r1 | bhs asi_bad | cmp r3,r1 | bhs asi_bad | ldr r1,[r0,r2,lsl #2] | ldr r12,[r0,r3,lsl #2] | str r12,[r0,r2,lsl #2] | str r1,[r0,r3,lsl #2] | movs r0,#1 | bx lr
asi_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={4,5,6,7};CHECK(array_swap_indexes(a,4,1,3));
CHECK(a[0]==4&&a[1]==7&&a[2]==6&&a[3]==5);
CHECK(array_swap_indexes(a,4,2,2));CHECK(!array_swap_indexes(a,4,0,4));''')

entry('concatenate-arrays-within-capacity',
      'Concatenate two arrays within capacity', 'Copy and move',
'''int array_concatenate(const int32_t *left, uint32_t left_count,
                      const int32_t *right, uint32_t right_count,
                      int32_t *output, uint32_t capacity)''',
'Write left followed by right. Reject count overflow, insufficient capacity, or invalid nonempty pointers before writing. The output must not overlap either input. Empty inputs are allowed.',
'1. Validate the total count and pointers.\n2. Copy the left array.\n3. Continue with the right array.',
'[1,2] concatenated with [-3,4,5] becomes [1,2,-3,4,5].',
'''int array_concatenate(const int32_t *left, uint32_t left_count,
                      const int32_t *right, uint32_t right_count,
                      int32_t *output, uint32_t capacity) {
  if (left_count > UINT32_MAX - right_count) return 0;
  uint32_t total = left_count + right_count;
  if (capacity < total || (!left && left_count) || (!right && right_count) ||
      (!output && total)) return 0;
  for (uint32_t i = 0; i < left_count; ++i) output[i] = left[i];
  for (uint32_t i = 0; i < right_count; ++i) output[left_count + i] = right[i];
  return 1;
}''',
'''; R0-R3 hold left, left_count, right, right_count. Output and capacity are on the stack.
ldr r12,[sp] | push {r4-r8,lr} | ldr r4,[sp,#28] | adds r5,r1,r3 | bcs acon_bad | cmp r4,r5 | blo acon_bad | cmp r5,#0 | beq acon_yes | cmp r12,#0 | beq acon_bad | cmp r1,#0 | beq acon_right_check | cmp r0,#0 | beq acon_bad
acon_right_check: | cmp r3,#0 | beq acon_copy_left | cmp r2,#0 | beq acon_bad
acon_copy_left: | mov r4,r12 | mov r5,r1
acon_left_loop: | cmp r5,#0 | beq acon_copy_right | ldr r6,[r0],#4 | str r6,[r4],#4 | subs r5,#1 | b acon_left_loop
acon_copy_right: | cmp r3,#0 | beq acon_yes | ldr r6,[r2],#4 | str r6,[r4],#4 | subs r3,#1 | b acon_copy_right
acon_yes: | movs r0,#1 | pop {r4-r8,pc}
acon_bad: | movs r0,#0 | pop {r4-r8,pc}''',
'''int32_t a[]={1,2},b[]={-3,4,5},o[6]={0};o[5]=77;
CHECK(array_concatenate(a,2,b,3,o,5));
CHECK(o[0]==1&&o[1]==2&&o[2]==-3&&o[4]==5&&o[5]==77);
o[0]=99;CHECK(!array_concatenate(a,2,b,3,o,4)&&o[0]==99);
CHECK(array_concatenate(0,0,0,0,0,0));''')

entry('insert-array-element-at-index', 'Insert an array element at an index',
      'Transform',
'''int array_insert_at(int32_t *values, uint32_t *length,
                    uint32_t capacity, uint32_t index, int32_t value)''',
'Insert before index, where index may equal the old length. Require length<capacity, index<=length, and valid storage. Invalid input returns 0 without changing the array or length.',
'1. Validate every condition before writing.\n2. Shift the suffix right from the end.\n3. Store the new value and increment length.',
'Insert 8 at index 1 in [3,5,7] to obtain [3,8,5,7].',
'''int array_insert_at(int32_t *values, uint32_t *length,
                    uint32_t capacity, uint32_t index, int32_t value) {
  if (!values || !length || *length >= capacity || index > *length) return 0;
  for (uint32_t i = *length; i > index; --i) values[i] = values[i - 1];
  values[index] = value;
  ++*length;
  return 1;
}''',
'''; R0=values, R1=length, R2=capacity, R3=index; value is at entry SP.
cmp r0,#0 | beq ains_bad | cmp r1,#0 | beq ains_bad | ldr r12,[r1] | cmp r12,r2 | bhs ains_bad | cmp r3,r12 | bhi ains_bad | push {r4,lr} | ldr r4,[sp,#8] | mov r2,r12
ains_shift: | cmp r2,r3 | beq ains_place | sub r12,r2,#1 | ldr r12,[r0,r12,lsl #2] | str r12,[r0,r2,lsl #2] | subs r2,#1 | b ains_shift
ains_place: | str r4,[r0,r3,lsl #2] | ldr r2,[r1] | adds r2,#1 | str r2,[r1] | movs r0,#1 | pop {r4,pc}
ains_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={3,5,7,99,77};uint32_t n=3;
CHECK(array_insert_at(a,&n,4,1,8)&&n==4);
CHECK(a[0]==3&&a[1]==8&&a[2]==5&&a[3]==7&&a[4]==77);
CHECK(!array_insert_at(a,&n,4,0,1)&&n==4);
CHECK(!array_insert_at(a,&n,5,5,1)&&n==4);''')

entry('delete-array-element-at-index', 'Delete an array element at an index',
      'Transform',
'''int array_delete_at(int32_t *values, uint32_t *length,
                    uint32_t index, int32_t *removed_out)''',
'Delete index and return the removed value. Require a nonempty valid array, index<length, and a valid output. Invalid input returns 0 without writes.',
'1. Validate and save the removed value.\n2. Shift later elements left.\n3. Decrement length and publish the removed value.',
'Deleting index 1 from [3,8,5,7] returns 8 and leaves [3,5,7].',
'''int array_delete_at(int32_t *values, uint32_t *length,
                    uint32_t index, int32_t *removed_out) {
  if (!values || !length || !removed_out || index >= *length) return 0;
  int32_t removed = values[index];
  for (uint32_t i = index + 1; i < *length; ++i) values[i - 1] = values[i];
  --*length;
  *removed_out = removed;
  return 1;
}''',
'''; R0=values, R1=length, R2=index, R3=removed_out.
cmp r0,#0 | beq adel_bad | cmp r1,#0 | beq adel_bad | cmp r3,#0 | beq adel_bad | ldr r12,[r1] | cmp r2,r12 | bhs adel_bad | push {r4-r6,lr} | ldr r4,[r0,r2,lsl #2] | mov r5,r2
adel_shift: | add r6,r5,#1 | cmp r6,r12 | bhs adel_done | ldr r2,[r0,r6,lsl #2] | str r2,[r0,r5,lsl #2] | mov r5,r6 | b adel_shift
adel_done: | subs r12,#1 | str r12,[r1] | str r4,[r3] | movs r0,#1 | pop {r4-r6,pc}
adel_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={3,8,5,7,77};uint32_t n=4;int32_t removed=99;
CHECK(array_delete_at(a,&n,1,&removed)&&n==3&&removed==8);
CHECK(a[0]==3&&a[1]==5&&a[2]==7&&a[4]==77);
removed=99;CHECK(!array_delete_at(a,&n,3,&removed)&&removed==99&&n==3);''')


def shift(direction):
    left=direction=='left'
    name='array_shift_left' if left else 'array_shift_right'
    if left:
        loops='''for (uint32_t i = 0; i < count - amount; ++i)
    values[i] = values[i + amount];
  for (uint32_t i = count - amount; i < count; ++i)
    values[i] = fill_value;'''
        asm='''push {r4,r5} | sub r4,r1,r2 | movs r5,#0
ash_copy: | cmp r5,r4 | bhs ash_fill | add r12,r5,r2 | ldr r12,[r0,r12,lsl #2] | str r12,[r0,r5,lsl #2] | adds r5,#1 | b ash_copy
ash_fill: | cmp r5,r1 | bhs ash_done | str r3,[r0,r5,lsl #2] | adds r5,#1 | b ash_fill
ash_done: | pop {r4,r5} | b ash_yes'''
        expected='a[0]==3&&a[1]==4&&a[2]==-1&&a[3]==-1'
    else:
        loops='''for (uint32_t i = count; i > amount; --i)
    values[i - 1] = values[i - 1 - amount];
  for (uint32_t i = 0; i < amount; ++i)
    values[i] = fill_value;'''
        asm='''push {r4,r5} | sub r4,r1,r2 | mov r5,r4
ash_copy: | cmp r5,#0 | beq ash_fill_start | subs r5,#1 | ldr r12,[r0,r5,lsl #2] | add r4,r5,r2 | str r12,[r0,r4,lsl #2] | b ash_copy
ash_fill_start: | movs r5,#0
ash_fill: | cmp r5,r2 | bhs ash_done | str r3,[r0,r5,lsl #2] | adds r5,#1 | b ash_fill
ash_done: | pop {r4,r5} | b ash_yes'''
        expected='a[0]==-1&&a[1]==-1&&a[2]==1&&a[3]==2'
    entry('shift-array-'+direction+'-with-fill',
          'Shift an array '+direction+' with a fill value', 'Transform',
          f'int {name}(int32_t *values, uint32_t count, uint32_t amount, int32_t fill_value)',
          'Shift by amount positions and fill vacated positions. An amount at least count fills the array. Empty input succeeds; null nonempty input fails.',
          '1. Validate storage.\n2. Clamp amount to count.\n3. Copy in the safe direction.\n4. Fill vacated positions.',
          ('[1,2,3,4] shifted left by 2 with -1 becomes [3,4,-1,-1].' if left
           else '[1,2,3,4] shifted right by 2 with -1 becomes [-1,-1,1,2].'),
          f'''int {name}(int32_t *values, uint32_t count,
                     uint32_t amount, int32_t fill_value) {{
  if (!values && count) return 0;
  if (amount > count) amount = count;
  {loops}
  return 1;
}}''',
          f'''; R0=values, R1=count, R2=amount, R3=fill_value.
cmp r1,#0 | beq ash_yes | cmp r0,#0 | beq ash_bad | cmp r2,r1 | bls ash_amount_ok | mov r2,r1
ash_amount_ok: | {asm}
ash_yes: | movs r0,#1 | bx lr
ash_bad: | movs r0,#0 | bx lr''',
          f'''int32_t a[]={{1,2,3,4,77}};CHECK({name}(a,4,2,-1));
CHECK({expected}&&a[4]==77);
CHECK({name}(a,4,9,5)&&a[0]==5&&a[3]==5);
CHECK({name}(0,0,1,5));CHECK(!{name}(0,1,1,5));''')


shift('left')
shift('right')

entry('move-zeros-to-end-stably', 'Move zeros to the end stably', 'Transform',
'int array_move_zeros_to_end(int32_t *values, uint32_t count)',
'Move every zero after all nonzero values while preserving nonzero order. Empty input succeeds; a null nonempty base fails.',
'1. Compact nonzero values at a write index.\n2. Fill the remaining suffix with zeros.\n3. Never read beyond count.',
'[0,4,0,-2,7] becomes [4,-2,7,0,0].',
'''int array_move_zeros_to_end(int32_t *values, uint32_t count) {
  if (!values && count) return 0;
  uint32_t write = 0;
  for (uint32_t read = 0; read < count; ++read)
    if (values[read] != 0) values[write++] = values[read];
  while (write < count) values[write++] = 0;
  return 1;
}''',
'''; R0=values, R1=count. R2=read pointer, R3=write pointer.
cmp r1,#0 | beq amz_yes | cmp r0,#0 | beq amz_bad | push {r4,lr} | mov r2,r0 | mov r3,r0 | mov r4,r1
amz_read: | ldr r12,[r2],#4 | cmp r12,#0 | beq amz_next | str r12,[r3],#4
amz_next: | subs r4,#1 | bne amz_read
amz_fill: | cmp r3,r2 | bhs amz_done | movs r12,#0 | str r12,[r3],#4 | b amz_fill
amz_done: | pop {r4,lr}
amz_yes: | movs r0,#1 | bx lr
amz_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={0,4,0,-2,7,77};CHECK(array_move_zeros_to_end(a,5));
CHECK(a[0]==4&&a[1]==-2&&a[2]==7&&a[3]==0&&a[4]==0&&a[5]==77);
CHECK(array_move_zeros_to_end(0,0));CHECK(!array_move_zeros_to_end(0,1));''')

entry('stable-even-before-odd-partition',
      'Partition even values before odd values stably', 'Transform',
'int array_stable_even_first(int32_t *values, uint32_t count)',
'Move even values before odd values while preserving order within both groups. The in-place insertion method uses no scratch buffer.',
'1. Scan left to right.\n2. Save an even value that follows odds.\n3. Shift the odd block right.\n4. Insert the saved even value.',
'[3,2,5,4,1] becomes [2,4,3,5,1].',
'''int array_stable_even_first(int32_t *values, uint32_t count) {
  if (!values && count) return 0;
  for (uint32_t i = 1; i < count; ++i) {
    if ((values[i] & 1) == 0) {
      int32_t even = values[i];
      uint32_t j = i;
      while (j && (values[j - 1] & 1)) {
        values[j] = values[j - 1];
        --j;
      }
      values[j] = even;
    }
  }
  return 1;
}''',
'''; R0=values, R1=count. R2 scans; R3 moves through an odd block.
cmp r1,#0 | beq aep_yes | cmp r0,#0 | beq aep_bad | push {r4-r6,lr} | movs r2,#1
aep_outer: | cmp r2,r1 | bhs aep_done | ldr r4,[r0,r2,lsl #2] | tst r4,#1 | bne aep_next | mov r3,r2
aep_shift: | cmp r3,#0 | beq aep_place | sub r5,r3,#1 | ldr r6,[r0,r5,lsl #2] | tst r6,#1 | beq aep_place | str r6,[r0,r3,lsl #2] | mov r3,r5 | b aep_shift
aep_place: | str r4,[r0,r3,lsl #2]
aep_next: | adds r2,#1 | b aep_outer
aep_done: | pop {r4-r6,lr}
aep_yes: | movs r0,#1 | bx lr
aep_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={3,2,5,4,1,77};CHECK(array_stable_even_first(a,5));
CHECK(a[0]==2&&a[1]==4&&a[2]==3&&a[3]==5&&a[4]==1&&a[5]==77);
CHECK(array_stable_even_first(0,0));CHECK(!array_stable_even_first(0,1));''',
complexity='O(count squared) worst-case time; O(1) auxiliary storage')

entry('test-array-ascending', 'Test whether an array is ascending',
      'Compare and test',
'int array_is_ascending(const int32_t *values, uint32_t count)',
'Return 1 when every adjacent pair is in nondecreasing signed order. Empty and one-element arrays are ascending; a null pointer is valid only for count zero.',
'1. Start with the second element.\n2. Compare it with its predecessor.\n3. Reject the first decrease.',
'[-3,-3,4,9] is ascending; [-3,4,2] fails at 2.',
'''int array_is_ascending(const int32_t *values, uint32_t count) {
  if (count == 0) return 1;
  if (!values) return 0;
  for (uint32_t i = 1; i < count; ++i)
    if (values[i] < values[i - 1]) return 0;
  return 1;
}''',
'''; R0=values, R1=count. R2=previous, R3=current.
cmp r1,#0 | beq aia_yes | cmp r0,#0 | beq aia_no | ldr r2,[r0],#4 | subs r1,#1
aia_loop: | cmp r1,#0 | beq aia_yes | ldr r3,[r0],#4 | cmp r3,r2 | blt aia_no | mov r2,r3 | subs r1,#1 | b aia_loop
aia_yes: | movs r0,#1 | bx lr
aia_no: | movs r0,#0 | bx lr''',
'''int32_t a[]={-3,-3,4,9},b[]={-3,4,2};
CHECK(array_is_ascending(a,4));CHECK(!array_is_ascending(b,3));
CHECK(array_is_ascending(0,0));CHECK(!array_is_ascending(0,1));''')

entry('classify-array-monotonic-direction',
      'Classify an array monotonic direction', 'Compare and test',
'int32_t array_monotonic_direction(const int32_t *values, uint32_t count)',
'Return 1 for nondecreasing, -1 for nonincreasing, 0 for constant or fewer than two elements, and 2 for non-monotonic or invalid input.',
'1. Track whether an increase and a decrease appeared.\n2. Return 2 if both appear.\n3. Otherwise return 1, -1, or 0.',
'[5,5,3,1] records a decrease but no increase, so it returns -1.',
'''int32_t array_monotonic_direction(const int32_t *values, uint32_t count) {
  if (!values && count) return 2;
  int increased = 0, decreased = 0;
  for (uint32_t i = 1; i < count; ++i) {
    increased |= values[i] > values[i - 1];
    decreased |= values[i] < values[i - 1];
    if (increased && decreased) return 2;
  }
  return increased ? 1 : decreased ? -1 : 0;
}''',
'''; R0=values, R1=count. R3=increased, R12=decreased.
cmp r1,#0 | beq amd_constant | cmp r0,#0 | beq amd_none | cmp r1,#1 | beq amd_constant | push {r4,lr} | ldr r2,[r0],#4 | movs r3,#0 | movs r12,#0 | subs r1,#1
amd_loop: | ldr r4,[r0],#4 | cmp r4,r2 | bgt amd_mark_up | blt amd_mark_down | b amd_check
amd_mark_up: | movs r3,#1 | b amd_check
amd_mark_down: | movs r12,#1
amd_check: | cmp r3,#0 | beq amd_next | cmp r12,#0 | bne amd_pop_none
amd_next: | mov r2,r4 | subs r1,#1 | bne amd_loop | cmp r3,#0 | bne amd_up | cmp r12,#0 | bne amd_down | pop {r4,lr}
amd_constant: | movs r0,#0 | bx lr
amd_up: | movs r0,#1 | pop {r4,pc}
amd_down: | mvn r0,#0 | pop {r4,pc}
amd_pop_none: | pop {r4,lr}
amd_none: | movs r0,#2 | bx lr''',
'''int32_t a[]={5,5,3,1},b[]={1,4,2},c[]={7,7};
CHECK(array_monotonic_direction(a,4)==-1);
CHECK(array_monotonic_direction(b,3)==2);
CHECK(array_monotonic_direction(c,2)==0);
CHECK(array_monotonic_direction(0,0)==0);''')

entry('produce-adjacent-differences', 'Produce adjacent differences', 'Transform',
'''int array_adjacent_differences(const int32_t *values, uint32_t count,
                               int64_t *output, uint32_t capacity)''',
'Write values[i+1]-values[i] as signed 64-bit results. Output length is count-1 for nonempty input and zero for empty input. Validate all inputs before writing.',
'1. Compute the required output count.\n2. Load neighboring values.\n3. Widen before subtracting.\n4. Store each 64-bit difference.',
'For [INT32_MIN,0,INT32_MAX], differences are 2147483648 and 2147483647.',
'''int array_adjacent_differences(const int32_t *values, uint32_t count,
                               int64_t *output, uint32_t capacity) {
  uint32_t needed = count ? count - 1 : 0;
  if (capacity < needed || (!values && count) || (!output && needed)) return 0;
  for (uint32_t i = 0; i < needed; ++i)
    output[i] = (int64_t)values[i + 1] - values[i];
  return 1;
}''',
'''; R0=values, R1=count, R2=output, R3=capacity.
cmp r1,#0 | beq aad_yes | cmp r0,#0 | beq aad_bad | subs r1,#1 | cmp r3,r1 | blo aad_bad | cmp r1,#0 | beq aad_yes | cmp r2,#0 | beq aad_bad | push {r4-r7,lr} | ldr r4,[r0],#4
aad_loop: | ldr r5,[r0],#4 | mov r7,r5 | asr r6,r5,#31 | subs r5,r5,r4 | sbc r6,r6,r4,asr #31 | str r5,[r2],#4 | str r6,[r2],#4 | mov r4,r7 | subs r1,#1 | bne aad_loop | pop {r4-r7,lr}
aad_yes: | movs r0,#1 | bx lr
aad_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={INT32_MIN,0,INT32_MAX};int64_t o[3]={0};o[2]=77;
CHECK(array_adjacent_differences(a,3,o,2));
CHECK(o[0]==2147483648LL&&o[1]==2147483647LL&&o[2]==77);
CHECK(array_adjacent_differences(0,0,0,0));
o[0]=99;CHECK(!array_adjacent_differences(a,3,o,1)&&o[0]==99);''')


def pair_sum(sorted_input):
    name='array_pair_sum_sorted' if sorted_input else 'array_pair_sum_unsorted'
    order='sorted' if sorted_input else 'unsorted'
    if sorted_input:
        c_body='''uint32_t first = 0, second = count - 1;
  while (first < second) {
    int64_t sum = (int64_t)values[first] + values[second];
    if (sum == target) { *first_out = first; *second_out = second; return 1; }
    if (sum < target) ++first; else --second;
  }'''
        asm='''movs r5,#0 | sub r6,r1,#1
aps_loop: | cmp r5,r6 | bhs aps_fail | ldr r7,[r0,r5,lsl #2] | ldr r8,[r0,r6,lsl #2] | asr r9,r7,#31 | asr r10,r8,#31 | adds r7,r7,r8 | adc r9,r9,r10 | asr r8,r2,#31 | cmp r9,r8 | blt aps_less | bgt aps_more | cmp r7,r2 | beq aps_found | blo aps_less
aps_more: | subs r6,#1 | b aps_loop
aps_less: | adds r5,#1 | b aps_loop'''
        complexity='O(count) time; O(1) auxiliary storage'
        example='For [1,2,4,7,9] and target 11, indexes 1 and 4 contain 2 and 9.'
        data='1,2,4,7,9'; n=5; target=11; first=1; second=4
        method='1. Start at both ends.\n2. Compare the widened sum with target.\n3. Move the left or right index until a pair is found.'
    else:
        c_body='''for (uint32_t first = 0; first < count; ++first)
    for (uint32_t second = first + 1; second < count; ++second)
      if ((int64_t)values[first] + values[second] == target) {
        *first_out = first; *second_out = second; return 1;
      }'''
        asm='''movs r5,#0
aps_outer: | cmp r5,r1 | bhs aps_fail | add r6,r5,#1
aps_loop: | cmp r6,r1 | bhs aps_next_first | ldr r7,[r0,r5,lsl #2] | ldr r8,[r0,r6,lsl #2] | asr r9,r7,#31 | asr r10,r8,#31 | adds r7,r7,r8 | adc r9,r9,r10 | asr r8,r2,#31 | cmp r9,r8 | bne aps_next_second | cmp r7,r2 | beq aps_found
aps_next_second: | adds r6,#1 | b aps_loop
aps_next_first: | adds r5,#1 | b aps_outer'''
        complexity='O(count squared) time; O(1) auxiliary storage'
        example='For [8,3,5,2] and target 10, the first pair is indexes 0 and 3.'
        data='8,3,5,2'; n=4; target=10; first=0; second=3
        method='1. Enumerate first indexes from low to high.\n2. Enumerate each later second index.\n3. Return the lexicographically first matching pair.'
    entry('find-target-sum-pair-in-'+order+'-array',
          'Find a target-sum pair in a '+order+' array', 'Search',
          f'''int {name}(const int32_t *values, uint32_t count, int32_t target,
                    uint32_t *first_out, uint32_t *second_out)''',
          ('Input must be ascending. ' if sorted_input else '')+
          'Find two distinct indexes whose exact 64-bit sum equals target. Output pointers must be valid and distinct; failure writes nothing.',
          method, example,
          f'''int {name}(const int32_t *values, uint32_t count,
                    int32_t target, uint32_t *first_out,
                    uint32_t *second_out) {{
  if (!values || !first_out || !second_out || first_out == second_out) return 0;
  {c_body}
  return 0;
}}''',
          f'''; R0=values, R1=count, R2=target, R3=first_out; second_out is at entry SP.
ldr r12,[sp] | cmp r0,#0 | beq aps_bad | cmp r3,#0 | beq aps_bad | cmp r12,#0 | beq aps_bad | cmp r3,r12 | beq aps_bad | cmp r1,#2 | blo aps_bad | push {{r4-r10,lr}} | mov r4,r12 | {asm}
aps_found: | str r5,[r3] | str r6,[r4] | movs r0,#1 | pop {{r4-r10,pc}}
aps_fail: | movs r0,#0 | pop {{r4-r10,pc}}
aps_bad: | movs r0,#0 | bx lr''',
          f'''int32_t a[]={{{data}}};uint32_t i=99,j=99;
CHECK({name}(a,{n},{target},&i,&j)&&i=={first}&&j=={second});
i=99;j=99;CHECK(!{name}(a,{n},99,&i,&j)&&i==99&&j==99);
CHECK(!{name}(a,{n},10,&i,&i));''', complexity=complexity)


pair_sum(False)
pair_sum(True)
