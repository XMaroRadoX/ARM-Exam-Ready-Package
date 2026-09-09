"""Fundamental signed-integer arithmetic prompts."""
from algorithm_catalog import add

FAMILY='Arithmetic and number theory'


def entry(slug,title,prototype,contract,method,trace,c_code,asm_code,tests,
          complexity='O(1) time and O(1) storage',helpers=''):
    teaching_comment=('/* Exam prompt: '+title+'\n * Contract: '+contract+
                      '\n * Method:\n * '+method.replace('\n','\n * ')+'\n */\n')
    add(slug,title,FAMILY,prototype,contract,method,trace,teaching_comment+c_code,asm_code,tests,
        complexity=complexity,helpers=helpers,fundamentals_group='Arithmetic')


def checked_binary(operation):
    names={'add':('checked_add_i32','Add signed integers with overflow detection','+','adds',''),
           'subtract':('checked_subtract_i32','Subtract signed integers with overflow detection','-','subs',''),
           'multiply':('checked_multiply_i32','Multiply signed integers with overflow detection','*','smull','mul')}
    name,title,op,instruction,kind=names[operation]
    if kind=='mul':
        asm='''cmp r2,#0 | beq cbo_bad | smull r3,r12,r0,r1 | asr r1,r3,#31 | cmp r12,r1 | bne cbo_bad | str r3,[r2] | movs r0,#1 | bx lr'''
    else:
        asm=f'''cmp r2,#0 | beq cbo_bad | {instruction} r3,r0,r1 | bvs cbo_bad | str r3,[r2] | movs r0,#1 | bx lr'''
    samples={'add':('INT32_MAX,1','20,-7','13'),
             'subtract':('INT32_MIN,1','20,7','13'),
             'multiply':('INT32_MAX,2','-6,7','-42')}
    bad,good,expected=samples[operation]
    entry('checked-signed-'+operation,title,
          f'int {name}(int32_t left, int32_t right, int32_t *result_out)',
          'Return 1 and the exact signed 32-bit result. Return 0 without writing when result_out is null or the mathematical result is outside INT32_MIN..INT32_MAX.',
          '1. Compute a widened result or inspect the ARM overflow condition.\n2. Reject overflow before storing.\n3. Publish the result only on success.',
          f'The safe example produces {expected}; the boundary example {bad} is rejected.',
          f'''int {name}(int32_t left, int32_t right, int32_t *result_out) {{
  if (!result_out) return 0;
  int64_t wide=(int64_t)left {op} right;
  if (wide<INT32_MIN || wide>INT32_MAX) return 0;
  *result_out=(int32_t)wide;
  return 1;
}}''',
          f'''; R0=left,R1=right,R2=result_out. Store only after overflow is ruled out.
{asm}
cbo_bad: | movs r0,#0 | bx lr''',
          f'''int32_t out=77;CHECK({name}({good},&out)&&out=={expected});
out=77;CHECK(!{name}({bad},&out)&&out==77);
CHECK(!{name}(1,2,0));''')


checked_binary('add')
checked_binary('subtract')
checked_binary('multiply')

entry('average-two-signed-integers-without-overflow',
      'Average two signed integers without overflow',
'int32_t average_two_i32(int32_t left, int32_t right)',
'Return (left+right)/2 with C signed-division semantics: truncate toward zero. The addition is formed as a signed 64-bit value, so opposite and extreme inputs cannot overflow.',
'1. Form the two-word signed sum.\n2. If a negative sum is odd, add one before shifting.\n3. Arithmetic-shift the 64-bit sum right once.',
'INT32_MIN and INT32_MAX sum to -1; truncating -1/2 toward zero returns 0.',
'''int32_t average_two_i32(int32_t left, int32_t right) {
  return (int32_t)(((int64_t)left + right) / 2);
}''',
'''; R0=left,R1=right. R2:R3 is the signed 64-bit sum.
asr r2,r0,#31 | asr r3,r1,#31 | adds r0,r0,r1 | adc r2,r2,r3 | cmp r2,#0 | bge ati_shift | tst r0,#1 | beq ati_shift | adds r0,#1 | adc r2,r2,#0
ati_shift: | lsrs r0,#1 | orr r0,r0,r2,lsl #31 | bx lr''',
'''CHECK(average_two_i32(INT32_MIN,INT32_MAX)==0);
CHECK(average_two_i32(INT32_MAX,INT32_MAX)==INT32_MAX);
CHECK(average_two_i32(-8,-5)==-6);
CHECK(average_two_i32(8,5)==6);''')

entry('normalize-signed-modulo', 'Normalize signed modulo into a nonnegative result',
'int normalized_modulo_i32(int32_t value, int32_t modulus, int32_t *result_out)',
'Require modulus>0. Return the unique result in 0..modulus-1 that is congruent to value. Invalid input returns 0 without writing.',
'1. Calculate the C signed remainder.\n2. Add modulus if the remainder is negative.\n3. Store the normalized result.',
'-17 modulo 5 gives C remainder -2, then -2+5=3.',
'''int normalized_modulo_i32(int32_t value, int32_t modulus,
                          int32_t *result_out) {
  if (!result_out || modulus<=0) return 0;
  int32_t result=value%modulus;
  if(result<0) result+=modulus;
  *result_out=result;
  return 1;
}''',
'''; R0=value,R1=positive modulus,R2=result_out. R3 is quotient, R12 remainder.
cmp r2,#0 | beq nmi_bad | cmp r1,#0 | ble nmi_bad | sdiv r3,r0,r1 | mls r12,r3,r1,r0 | cmp r12,#0 | bge nmi_store | add r12,r12,r1
nmi_store: | str r12,[r2] | movs r0,#1 | bx lr
nmi_bad: | movs r0,#0 | bx lr''',
'''int32_t out=77;CHECK(normalized_modulo_i32(-17,5,&out)&&out==3);
CHECK(normalized_modulo_i32(17,5,&out)&&out==2);
out=77;CHECK(!normalized_modulo_i32(3,0,&out)&&out==77);
CHECK(!normalized_modulo_i32(3,5,0));''')

entry('classify-integer-even-or-odd', 'Classify an integer as even or odd',
'uint32_t integer_is_odd(int32_t value)',
'Return 0 for even and 1 for odd. Testing the low bit works for positive, zero, and negative two-complement values.',
'1. Mask bit zero.\n2. Return that bit directly.',
'-7 has low bit 1, so it is odd; -8 has low bit 0, so it is even.',
'''uint32_t integer_is_odd(int32_t value) {
  return (uint32_t)value & 1u;
}''',
'''; R0=value. Bit zero is the complete result.
and r0,r0,#1 | bx lr''',
'''CHECK(integer_is_odd(0)==0);CHECK(integer_is_odd(7)==1);
CHECK(integer_is_odd(-7)==1);CHECK(integer_is_odd(-8)==0);''')

entry('test-integer-power-of-two', 'Test whether an integer is a power of two',
'int is_power_of_two_u32(uint32_t value)',
'Return 1 only for positive unsigned values containing exactly one set bit. Zero is not a power of two.',
'1. Reject zero.\n2. Clear the lowest set bit with value & (value-1).\n3. A zero remainder means exactly one bit was set.',
'16 is 10000b and passes; 18 is 10010b and leaves a set bit after the clear.',
'''int is_power_of_two_u32(uint32_t value) {
  return value!=0 && (value&(value-1u))==0;
}''',
'''; R0=value. R1 receives value-1.
cmp r0,#0 | beq ipt_no | sub r1,r0,#1 | tst r0,r1 | bne ipt_no | movs r0,#1 | bx lr
ipt_no: | movs r0,#0 | bx lr''',
'''CHECK(is_power_of_two_u32(1));CHECK(is_power_of_two_u32(16));
CHECK(is_power_of_two_u32(0)==0);CHECK(is_power_of_two_u32(18)==0);
CHECK(is_power_of_two_u32(0x80000000u));''')

entry('find-next-power-of-two-with-overflow',
      'Find the next power of two with overflow detection',
'int next_power_of_two_u32(uint32_t value, uint32_t *result_out)',
'Return the smallest power of two greater than or equal to value. Define input zero as result one. Values above 0x80000000 cannot be represented and fail without writing.',
'1. Handle zero and reject the overflow range.\n2. Subtract one.\n3. Spread the highest set bit downward.\n4. Add one.',
'For 13: 12 is 1100b, spreading gives 1111b, and adding one gives 16.',
'''int next_power_of_two_u32(uint32_t value, uint32_t *result_out) {
  if(!result_out || value>0x80000000u) return 0;
  if(value==0) value=1;
  else {
    --value;
    value|=value>>1; value|=value>>2; value|=value>>4;
    value|=value>>8; value|=value>>16;
    ++value;
  }
  *result_out=value;
  return 1;
}''',
'''; R0=value,R1=result_out. R2 is the spreading temporary.
cmp r1,#0 | beq npt_bad | cmp r0,#0 | beq npt_one | cmp r0,#0x80000000 | bhi npt_bad | subs r0,#1 | lsr r2,r0,#1 | orr r0,r0,r2 | lsr r2,r0,#2 | orr r0,r0,r2 | lsr r2,r0,#4 | orr r0,r0,r2 | lsr r2,r0,#8 | orr r0,r0,r2 | lsr r2,r0,#16 | orr r0,r0,r2 | adds r0,#1 | b npt_store
npt_one: | movs r0,#1
npt_store: | str r0,[r1] | movs r0,#1 | bx lr
npt_bad: | movs r0,#0 | bx lr''',
'''uint32_t out=77;CHECK(next_power_of_two_u32(13,&out)&&out==16);
CHECK(next_power_of_two_u32(0,&out)&&out==1);
CHECK(next_power_of_two_u32(0x80000000u,&out)&&out==0x80000000u);
out=77;CHECK(!next_power_of_two_u32(0x80000001u,&out)&&out==77);''')

entry('build-decimal-digit-frequency-table',
      'Build a decimal digit-frequency table',
'int decimal_digit_frequency_i32(int32_t value, uint32_t counts[10])',
'Clear and fill ten counters for the magnitude digits of value. Zero contributes one zero digit. The unsigned-magnitude conversion handles INT32_MIN. A null table fails.',
'1. Clear all ten counters.\n2. Convert the signed value to an unsigned magnitude.\n3. Repeatedly divide by ten and increment the remainder bucket.',
'For -12012, digit counts are: 0->1, 1->2, 2->2, all others zero.',
'''int decimal_digit_frequency_i32(int32_t value, uint32_t counts[10]) {
  if(!counts) return 0;
  for(uint32_t i=0;i<10;++i) counts[i]=0;
  uint32_t magnitude=value<0 ? 0u-(uint32_t)value : (uint32_t)value;
  if(magnitude==0) { counts[0]=1; return 1; }
  while(magnitude) {
    uint32_t quotient=magnitude/10u;
    ++counts[magnitude-quotient*10u];
    magnitude=quotient;
  }
  return 1;
}''',
'''; R0=value,R1=counts. R2=magnitude,R3=quotient,R12=digit.
cmp r1,#0 | beq ddf_bad | push {r4,lr} | movs r2,#0 | movs r3,#0
ddf_clear: | str r3,[r1,r2,lsl #2] | adds r2,#1 | cmp r2,#10 | blo ddf_clear | mov r2,r0 | cmp r0,#0 | bge ddf_ready | rsb r2,r0,#0
ddf_ready: | cmp r2,#0 | bne ddf_loop | movs r3,#1 | str r3,[r1] | b ddf_done
ddf_loop: | movs r4,#10 | udiv r3,r2,r4 | mls r12,r3,r4,r2 | ldr r0,[r1,r12,lsl #2] | adds r0,#1 | str r0,[r1,r12,lsl #2] | mov r2,r3 | cmp r2,#0 | bne ddf_loop
ddf_done: | movs r0,#1 | pop {r4,pc}
ddf_bad: | movs r0,#0 | bx lr''',
'''uint32_t c[11];for(unsigned i=0;i<11;i++)c[i]=77;
CHECK(decimal_digit_frequency_i32(-12012,c));
CHECK(c[0]==1&&c[1]==2&&c[2]==2&&c[3]==0&&c[10]==77);
CHECK(decimal_digit_frequency_i32(0,c)&&c[0]==1&&c[1]==0);
CHECK(decimal_digit_frequency_i32(INT32_MIN,c)&&c[2]==1&&c[8]==2);
CHECK(!decimal_digit_frequency_i32(5,0));''',
complexity='O(number of decimal digits) time; exactly ten output counters')

entry('scale-integer-between-ranges', 'Scale an integer between ranges',
'''int scale_i32_between_ranges(int32_t value, int32_t input_min,
                             int32_t input_max, int32_t output_min,
                             int32_t output_max, int32_t *result_out)''',
'Clamp value to input_min..input_max, then linearly map it to output_min..output_max. Input span must be positive and fit int32_t; output span must fit int32_t. Use a signed 64-bit product and truncate division toward zero. Invalid input writes nothing.',
'1. Validate both spans and the output pointer.\n2. Clamp the input.\n3. Multiply input offset by output span in 64 bits.\n4. Divide by input span and add output_min.',
'Mapping 25 from 0..100 into 0..1000 gives 250; input 120 clamps to 1000.',
'''int scale_i32_between_ranges(int32_t value, int32_t input_min,
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
}''',
'''; R0=value,R1=input_min,R2=input_max,R3=output_min. output_max and result_out are on entry stack.
ldr r12,[sp,#4] | cmp r12,#0 | beq sir_bad | push {r4-r10,lr} | mov r4,r0 | mov r5,r1 | mov r6,r2 | mov r7,r3 | ldr r8,[sp,#32] | ldr r9,[sp,#36] | subs r10,r6,r5 | bvs sir_fail | cmp r10,#0 | ble sir_fail | subs r6,r8,r7 | bvs sir_fail | cmp r4,r5 | bge sir_high | mov r4,r5
sir_high: | cmp r4,r2 | ble sir_product | mov r4,r2
sir_product: | sub r4,r4,r5 | smull r0,r1,r4,r6 | mov r2,r10 | movs r3,#0 | bl __aeabi_ldivmod | adds r0,r0,r7 | bvs sir_fail | str r0,[r9] | movs r0,#1 | pop {r4-r10,pc}
sir_fail: | movs r0,#0 | pop {r4-r10,pc}
sir_bad: | movs r0,#0 | bx lr''',
'''int32_t out=77;CHECK(scale_i32_between_ranges(25,0,100,0,1000,&out)&&out==250);
CHECK(scale_i32_between_ranges(120,0,100,0,1000,&out)&&out==1000);
CHECK(scale_i32_between_ranges(25,0,100,1000,0,&out)&&out==750);
out=77;CHECK(!scale_i32_between_ranges(2,5,5,0,10,&out)&&out==77);
CHECK(!scale_i32_between_ranges(2,0,5,0,10,0));''',
helpers='IMPORT __aeabi_ldivmod')
