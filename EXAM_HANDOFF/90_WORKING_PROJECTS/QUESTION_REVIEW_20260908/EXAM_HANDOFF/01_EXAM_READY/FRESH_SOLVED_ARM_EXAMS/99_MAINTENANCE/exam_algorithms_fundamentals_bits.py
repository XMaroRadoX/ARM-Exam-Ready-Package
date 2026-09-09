"""Fundamental bit and byte prompts with exact 32-bit contracts."""
from algorithm_catalog import add

FAMILY='Bits and fixed-point work'


def entry(slug,title,prototype,contract,method,trace,c_code,asm_code,tests,
          complexity='O(1) time and O(1) storage'):
    teaching_comment=('/* Exam prompt: '+title+'\n * Contract: '+contract+
                      '\n * Method:\n * '+method.replace('\n','\n * ')+'\n */\n')
    add(slug,title,FAMILY,prototype,contract,method,trace,teaching_comment+c_code,asm_code,tests,
        complexity=complexity,fundamentals_group='Bits and bytes')


def bit_edit(operation):
    names={'test':('test_bit_u32','Test one bit'),
           'set':('set_bit_u32','Set one bit'),
           'clear':('clear_bit_u32','Clear one bit'),
           'toggle':('toggle_bit_u32','Toggle one bit')}
    name,title=names[operation]
    if operation=='test':
        expression='(value >> index) & 1u'
        asm='lsr r0,r0,r1 | and r0,r0,#1 | str r0,[r2]'
        expected='1'
    elif operation=='set':
        expression='value | (1u << index)'
        asm='movs r3,#1 | lsl r3,r3,r1 | orr r0,r0,r3 | str r0,[r2]'
        expected='0x80000008u'
    elif operation=='clear':
        expression='value & ~(1u << index)'
        asm='movs r3,#1 | lsl r3,r3,r1 | bic r0,r0,r3 | str r0,[r2]'
        expected='0x00000008u'
    else:
        expression='value ^ (1u << index)'
        asm='movs r3,#1 | lsl r3,r3,r1 | eor r0,r0,r3 | str r0,[r2]'
        expected='0x80000008u'
    entry(operation+'-one-bit',title,
          f'int {name}(uint32_t value, uint32_t index, uint32_t *result_out)',
          'Accept bit indexes 0..31. Return 1 and the requested result, or return 0 without writing for an invalid index or null output.',
          '1. Validate the index and output.\n2. Build or select the requested one-bit mask.\n3. Store the exact 32-bit result.',
          ('Testing bit 31 of 0x80000008 returns 1.' if operation=='test' else
           f'Applying the operation at bit 31 to 0x00000008 produces {expected}.'),
          f'''int {name}(uint32_t value, uint32_t index,
                 uint32_t *result_out) {{
  if(index>=32 || !result_out) return 0;
  *result_out={expression};
  return 1;
}}''',
          f'''; R0=value,R1=index,R2=result_out. Invalid input performs no store.
cmp r1,#32 | bhs beo_bad | cmp r2,#0 | beq beo_bad | {asm} | movs r0,#1 | bx lr
beo_bad: | movs r0,#0 | bx lr''',
          f'''uint32_t out=77;CHECK({name}({('0x80000008u' if operation=='test' else '8u')},31,&out)&&out=={expected});
out=77;CHECK(!{name}(8,32,&out)&&out==77);CHECK(!{name}(8,3,0));''')


for operation in ('test','set','clear','toggle'):
    bit_edit(operation)


def rotate(left):
    name='rotate_left_u32' if left else 'rotate_right_u32'
    title='Rotate a 32-bit word '+('left' if left else 'right')
    c=('return amount ? (value<<amount)|(value>>(32u-amount)) : value;' if left else
       'return amount ? (value>>amount)|(value<<(32u-amount)) : value;')
    asm=('rsb r1,r1,#32 | and r1,r1,#31 | ror r0,r0,r1' if left else
         'ror r0,r0,r1')
    expected='0x23456781u' if left else '0x81234567u'
    entry('rotate-word-'+('left' if left else 'right'),title,
          f'uint32_t {name}(uint32_t value, uint32_t amount)',
          'Normalize amount modulo 32 and rotate without losing bits. A zero or multiple-of-32 amount returns the original word.',
          '1. Keep the low five amount bits.\n2. Combine opposite logical shifts in C.\n3. Use the ARM rotate instruction with the equivalent direction.',
          f'Rotating 0x12345678 by 4 produces {expected}.',
          f'''uint32_t {name}(uint32_t value, uint32_t amount) {{
  amount&=31u;
  {c}
}}''',
          f'''; R0=value,R1=amount. Register-controlled ROR uses the low five count bits.
and r1,r1,#31 | {asm} | bx lr''',
          f'''CHECK({name}(0x12345678u,4)=={expected});
CHECK({name}(0x12345678u,0)==0x12345678u);
CHECK({name}(0x12345678u,36)=={expected});''')


rotate(True)
rotate(False)

entry('reverse-byte-order-u32', 'Reverse the byte order of a 32-bit word',
'uint32_t reverse_byte_order_u32(uint32_t value)',
'Return the same four bytes in reverse order. This changes logical byte positions and does not access memory.',
'1. Extract or route each byte to the opposite position.\n2. Combine all four non-overlapping fields.',
'0x12345678 becomes 0x78563412.',
'''uint32_t reverse_byte_order_u32(uint32_t value) {
  return ((value&0x000000ffu)<<24) | ((value&0x0000ff00u)<<8) |
         ((value&0x00ff0000u)>>8) | ((value&0xff000000u)>>24);
}''',
'''; Cortex-M3 REV reverses all four byte lanes in R0.
rev r0,r0 | bx lr''',
'''CHECK(reverse_byte_order_u32(0x12345678u)==0x78563412u);
CHECK(reverse_byte_order_u32(0)==0);
CHECK(reverse_byte_order_u32(0xaabbccddu)==0xddccbbaau);''')

entry('swap-byte-nibbles', 'Swap the two nibbles of a byte',
'uint8_t swap_byte_nibbles(uint8_t value)',
'Exchange bits 7..4 with bits 3..0 and return the low eight-bit result.',
'1. Shift the low nibble left four.\n2. Shift the high nibble right four.\n3. OR the two fields.',
'0xAB becomes 0xBA.',
'''uint8_t swap_byte_nibbles(uint8_t value) {
  return (uint8_t)((value<<4)|(value>>4));
}''',
'''; R0=value. UXTB keeps only the byte before and after the swap.
uxtb r0,r0 | lsl r1,r0,#4 | lsr r0,r0,#4 | orr r0,r0,r1 | uxtb r0,r0 | bx lr''',
'''CHECK(swap_byte_nibbles(0xabu)==0xbau);
CHECK(swap_byte_nibbles(0x10u)==0x01u);
CHECK(swap_byte_nibbles(0xffu)==0xffu);''')

entry('pack-four-bytes-into-word', 'Pack four bytes into a 32-bit word',
'''uint32_t pack_four_bytes_be(uint8_t first, uint8_t second,
                            uint8_t third, uint8_t fourth)''',
'Pack first into bits 31..24, second into 23..16, third into 15..8, and fourth into 7..0. The name describes this logical big-endian display order; no memory access occurs.',
'1. Mask each input to eight bits.\n2. Shift it to its declared field.\n3. OR the four disjoint fields.',
'Bytes 12,34,56,78 hex pack into 0x12345678.',
'''uint32_t pack_four_bytes_be(uint8_t first, uint8_t second,
                            uint8_t third, uint8_t fourth) {
  return ((uint32_t)first<<24)|((uint32_t)second<<16)|
         ((uint32_t)third<<8)|fourth;
}''',
'''; R0-R3 contain the four bytes. Mask before shifting and combining.
uxtb r0,r0 | uxtb r1,r1 | uxtb r2,r2 | uxtb r3,r3 | lsl r0,r0,#24 | orr r0,r0,r1,lsl #16 | orr r0,r0,r2,lsl #8 | orr r0,r0,r3 | bx lr''',
'''CHECK(pack_four_bytes_be(0x12,0x34,0x56,0x78)==0x12345678u);
CHECK(pack_four_bytes_be(0,0,0,0)==0);
CHECK(pack_four_bytes_be(0xff,0xff,0xff,0xff)==UINT32_MAX);''')

entry('unpack-word-into-four-bytes', 'Unpack a 32-bit word into four bytes',
'int unpack_four_bytes_be(uint32_t value, uint8_t *output, uint32_t capacity)',
'Write bits 31..24, 23..16, 15..8, and 7..0 into output[0..3]. Require capacity>=4 and a valid output; failure writes nothing.',
'1. Validate all output storage.\n2. Shift each declared field to the low byte.\n3. Store exactly four bytes.',
'0x12345678 unpacks to bytes 12,34,56,78 hex.',
'''int unpack_four_bytes_be(uint32_t value, uint8_t *output,
                         uint32_t capacity) {
  if(!output || capacity<4) return 0;
  output[0]=(uint8_t)(value>>24);
  output[1]=(uint8_t)(value>>16);
  output[2]=(uint8_t)(value>>8);
  output[3]=(uint8_t)value;
  return 1;
}''',
'''; R0=value,R1=output,R2=capacity. Validate before four STRB operations.
cmp r1,#0 | beq ufb_bad | cmp r2,#4 | blo ufb_bad | lsr r3,r0,#24 | strb r3,[r1] | lsr r3,r0,#16 | strb r3,[r1,#1] | lsr r3,r0,#8 | strb r3,[r1,#2] | strb r0,[r1,#3] | movs r0,#1 | bx lr
ufb_bad: | movs r0,#0 | bx lr''',
'''uint8_t o[5]={0};o[4]=77;CHECK(unpack_four_bytes_be(0x12345678u,o,4));
CHECK(o[0]==0x12&&o[1]==0x34&&o[2]==0x56&&o[3]==0x78&&o[4]==77);
o[0]=99;CHECK(!unpack_four_bytes_be(0, o,3)&&o[0]==99);
CHECK(!unpack_four_bytes_be(0,0,4));''')
