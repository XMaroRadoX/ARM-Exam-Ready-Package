"""Fundamental bounded-string prompts with readable C and handwritten ARMASM."""
from algorithm_catalog import add

FAMILY = 'Strings'
LEN_HELPER = '''; Local helper: R0=text, R1=capacity; return length or -1.
sbl_loop: | cmp r1,#0 | beq sbl_bad | ldrb r2,[r0],#1 | cmp r2,#0 | beq sbl_done | subs r1,#1 | adds r3,#1 | b sbl_loop
sbl_done: | mov r0,r3 | bx lr
sbl_bad: | mvn r0,#0 | bx lr'''


def entry(slug, title, group, prototype, contract, method, trace, c_code,
          asm_code, tests, complexity='O(capacity) time; O(1) auxiliary storage',
          helpers='', registers=''):
    teaching_comment = ('/* Exam prompt: ' + title + '\n * Contract: ' + contract +
                        '\n * Method:\n * ' + method.replace('\n', '\n * ') + '\n */\n')
    add(slug, title, FAMILY, prototype, contract, method, trace, teaching_comment + c_code, asm_code,
        tests, complexity=complexity, helpers=helpers, registers=registers,
        fundamentals_group=group)


entry('find-bounded-string-length', 'Find bounded string length', 'Strings',
'int string_length_bounded(const uint8_t *text, uint32_t capacity, uint32_t *length_out)',
'Find NUL within capacity and return its index through length_out. A null pointer, zero capacity, or missing terminator returns 0 without changing the output.',
'1. Validate both pointers.\n2. Scan at most capacity bytes.\n3. Stop at NUL and publish its index only then.',
'For "ARM" stored as [65,82,77,0] with capacity 4, NUL is at index 3.',
'''int string_length_bounded(const uint8_t *text, uint32_t capacity,
                          uint32_t *length_out) {
  if (!text || !length_out) return 0;
  for (uint32_t i = 0; i < capacity; ++i) {
    if (text[i] == 0) {
      *length_out = i;
      return 1;
    }
  }
  return 0;
}''',
'''; R0=text, R1=capacity, R2=length_out. R3 is the current index.
cmp r0,#0 | beq sbl_bad_main | cmp r2,#0 | beq sbl_bad_main | movs r3,#0
sbl_main_loop: | cmp r3,r1 | bhs sbl_bad_main | ldrb r12,[r0,r3] | cmp r12,#0 | beq sbl_found | adds r3,#1 | b sbl_main_loop
sbl_found: | str r3,[r2] | movs r0,#1 | bx lr
sbl_bad_main: | movs r0,#0 | bx lr''',
'''uint8_t a[]="ARM",b[]={'N','O'};uint32_t n=99;
CHECK(string_length_bounded(a,4,&n)&&n==3);
n=99;CHECK(!string_length_bounded(b,2,&n)&&n==99);
CHECK(!string_length_bounded(0,4,&n)&&n==99);''')

entry('compare-bounded-strings-for-equality',
      'Compare bounded strings for equality', 'Compare and test',
'''int32_t strings_equal_bounded(const uint8_t *left, uint32_t left_capacity,
                              const uint8_t *right, uint32_t right_capacity)''',
'Return 1 for equal strings, 0 for unequal strings, and -1 when either input is null or lacks NUL within its capacity. Both strings are fully validated before comparison.',
'1. Find both bounded lengths.\n2. Reject unequal lengths.\n3. Compare exactly the characters before NUL.',
'"ARM" equals "ARM"; "ARM" and "Arm" differ at index 1.',
'''static int string_length_for_equal(const uint8_t *text, uint32_t capacity,
                                   uint32_t *length) {
  if (!text || !length) return 0;
  for (uint32_t i = 0; i < capacity; ++i)
    if (text[i] == 0) { *length = i; return 1; }
  return 0;
}
int32_t strings_equal_bounded(const uint8_t *left, uint32_t left_capacity,
                              const uint8_t *right, uint32_t right_capacity) {
  uint32_t left_length, right_length;
  if (!string_length_for_equal(left,left_capacity,&left_length) ||
      !string_length_for_equal(right,right_capacity,&right_length)) return -1;
  if (left_length != right_length) return 0;
  for (uint32_t i=0;i<left_length;++i) if (left[i]!=right[i]) return 0;
  return 1;
}''',
'''; Save both bases/capacities, validate lengths with the local helper, then compare.
push {r4-r8,lr} | mov r4,r0 | mov r5,r1 | mov r6,r2 | mov r7,r3 | movs r3,#0 | bl sbl_loop | cmp r0,#0 | blt seq_invalid | mov r8,r0 | mov r0,r6 | mov r1,r7 | movs r3,#0 | bl sbl_loop | cmp r0,#0 | blt seq_invalid | cmp r8,r0 | bne seq_no | mov r1,r8
seq_loop: | cmp r1,#0 | beq seq_yes | ldrb r2,[r4],#1 | ldrb r3,[r6],#1 | cmp r2,r3 | bne seq_no | subs r1,#1 | b seq_loop
seq_yes: | movs r0,#1 | pop {r4-r8,pc}
seq_no: | movs r0,#0 | pop {r4-r8,pc}
seq_invalid: | mvn r0,#0 | pop {r4-r8,pc}''',
'''uint8_t a[]="ARM",b[]="ARM",c[]="Arm",bad[]={'A','R','M'};
CHECK(strings_equal_bounded(a,4,b,4)==1);
CHECK(strings_equal_bounded(a,4,c,4)==0);
CHECK(strings_equal_bounded(a,4,bad,3)==-1);''',
helpers=LEN_HELPER)

entry('concatenate-bounded-strings', 'Concatenate bounded strings', 'Strings',
'''int string_concatenate_bounded(uint8_t *destination, uint32_t *length,
                               uint32_t capacity, const uint8_t *source,
                               uint32_t source_capacity)''',
'Append source to destination. destination[length] must be NUL, source must terminate within source_capacity, and the final NUL must fit. Validate everything before writing.',
'1. Validate destination state.\n2. Find the bounded source length.\n3. Check length+source_length+1 against capacity.\n4. Copy source including NUL and update length.',
'Appending "M3" to "ARM" with capacity 8 produces "ARMM3" and length 5.',
'''static int string_length_for_concat(const uint8_t *text, uint32_t capacity,
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
}''',
'''; R0=destination, R1=length, R2=capacity, R3=source; source_capacity is at entry SP.
cmp r0,#0 | beq scb_bad | cmp r1,#0 | beq scb_bad | cmp r3,#0 | beq scb_bad | push {r4-r9,lr} | sub sp,sp,#4 | mov r4,r0 | mov r5,r1 | mov r6,r2 | mov r7,r3 | ldr r9,[sp,#32] | ldr r8,[r5] | cmp r8,r6 | bhs scb_fail | ldrb r0,[r4,r8] | cmp r0,#0 | bne scb_fail | mov r0,r7 | mov r1,r9 | movs r3,#0 | bl sbl_loop | cmp r0,#0 | blt scb_fail | sub r1,r6,r8 | subs r1,#1 | cmp r0,r1 | bhi scb_fail | mov r2,r0 | movs r3,#0
scb_copy: | ldrb r1,[r7,r3] | add r9,r8,r3 | strb r1,[r4,r9] | adds r3,#1 | cmp r3,r2 | bls scb_copy | add r8,r8,r2 | str r8,[r5] | movs r0,#1 | b scb_return
scb_fail: | movs r0,#0
scb_return: | add sp,sp,#4 | pop {r4-r9,pc}
scb_bad: | movs r0,#0 | bx lr''',
'''uint8_t a[8]="ARM",b[]="M3",bad[]={'X','Y'};uint32_t n=3;
CHECK(string_concatenate_bounded(a,&n,8,b,3)&&n==5);
CHECK(a[0]=='A'&&a[3]=='M'&&a[4]=='3'&&a[5]==0);
CHECK(!string_concatenate_bounded(a,&n,6,b,3)&&n==5);
CHECK(!string_concatenate_bounded(a,&n,8,bad,2)&&n==5);''',
helpers=LEN_HELPER)

entry('append-one-string-character', 'Append one character', 'Strings',
'int string_append_character(uint8_t *text, uint32_t *length, uint32_t capacity, uint8_t character)',
'Append one non-NUL byte and preserve NUL termination. Require text[length] to be NUL and space for the character plus the new terminator. Invalid input writes nothing.',
'1. Validate storage, length, character, and current NUL.\n2. Write the character over the old NUL.\n3. Write a new NUL and increment length.',
'Appending ! to "ARM" produces "ARM!" with length 4.',
'''int string_append_character(uint8_t *text, uint32_t *length,
                            uint32_t capacity, uint8_t character) {
  if (!text || !length || character==0 || *length>=capacity ||
      text[*length]!=0 || capacity-*length<2) return 0;
  text[*length]=character;
  text[*length+1]=0;
  ++*length;
  return 1;
}''',
'''; R0=text, R1=length, R2=capacity, R3=character.
cmp r0,#0 | beq sac_bad | cmp r1,#0 | beq sac_bad | cmp r3,#0 | beq sac_bad | push {r4,lr} | mov r4,r2 | ldr r12,[r1] | cmp r12,r4 | bhs sac_fail | add r2,r12,#1 | cmp r2,r4 | bhs sac_fail | ldrb r4,[r0,r12] | cmp r4,#0 | bne sac_fail | strb r3,[r0,r12] | movs r3,#0 | strb r3,[r0,r2] | str r2,[r1] | movs r0,#1 | pop {r4,pc}
sac_fail: | movs r0,#0 | pop {r4,pc}
sac_bad: | movs r0,#0 | bx lr''',
'''uint8_t a[6]="ARM";uint32_t n=3;CHECK(string_append_character(a,&n,6,'!'));
CHECK(n==4&&a[3]=='!'&&a[4]==0);
CHECK(!string_append_character(a,&n,5,'?')&&n==4);
CHECK(!string_append_character(a,&n,6,0)&&n==4);''')

entry('insert-one-string-character', 'Insert one character at an index', 'Strings',
'''int string_insert_character(uint8_t *text, uint32_t *length,
                            uint32_t capacity, uint32_t index,
                            uint8_t character)''',
'Insert one non-NUL byte before index, where index may equal length. Require a valid current terminator and one spare byte. Invalid input writes nothing.',
'1. Validate all conditions.\n2. Shift the suffix including NUL one byte right.\n3. Store the character and increment length.',
'Insert X at index 1 in "ARM" to produce "AXRM".',
'''int string_insert_character(uint8_t *text, uint32_t *length,
                            uint32_t capacity, uint32_t index,
                            uint8_t character) {
  if (!text || !length || character==0 || index>*length ||
      *length>=capacity || text[*length]!=0 || capacity-*length<2) return 0;
  for (uint32_t i=*length+1;i>index;--i) text[i]=text[i-1];
  text[index]=character;
  ++*length;
  return 1;
}''',
'''; R0=text, R1=length, R2=capacity, R3=index; character is at entry SP.
cmp r0,#0 | beq sic_bad | cmp r1,#0 | beq sic_bad | ldr r12,[r1] | cmp r3,r12 | bhi sic_bad | sub r2,r2,r12 | cmp r2,#2 | blo sic_bad | ldrb r2,[r0,r12] | cmp r2,#0 | bne sic_bad | add r2,r12,#1 | push {r4,lr} | ldr r4,[sp,#8] | and r4,r4,#255 | cmp r4,#0 | beq sic_fail
sic_shift: | cmp r2,r3 | beq sic_place | sub r12,r2,#1 | ldrb r12,[r0,r12] | strb r12,[r0,r2] | subs r2,#1 | b sic_shift
sic_place: | strb r4,[r0,r3] | ldr r2,[r1] | adds r2,#1 | str r2,[r1] | movs r0,#1 | pop {r4,pc}
sic_fail: | movs r0,#0 | pop {r4,pc}
sic_bad: | movs r0,#0 | bx lr''',
'''uint8_t a[6]="ARM";uint32_t n=3;CHECK(string_insert_character(a,&n,6,1,'X'));
CHECK(n==4&&a[0]=='A'&&a[1]=='X'&&a[2]=='R'&&a[4]==0);
CHECK(!string_insert_character(a,&n,5,0,'Y')&&n==4);
CHECK(!string_insert_character(a,&n,6,5,'Y')&&n==4);''')

entry('delete-one-string-character', 'Delete one character at an index', 'Strings',
'''int string_delete_character(uint8_t *text, uint32_t *length,
                            uint32_t index, uint8_t *removed_out)''',
'Delete index, return the removed byte, and preserve NUL termination. Require index<length and text[length] to be NUL. Invalid input writes nothing.',
'1. Validate and save the selected byte.\n2. Shift all later bytes including NUL left.\n3. Decrement length and publish the removed byte.',
'Delete index 1 from "AXRM" to return X and restore "ARM".',
'''int string_delete_character(uint8_t *text, uint32_t *length,
                            uint32_t index, uint8_t *removed_out) {
  if (!text || !length || !removed_out || index>=*length ||
      text[*length]!=0) return 0;
  uint8_t removed=text[index];
  for (uint32_t i=index;i<*length;++i) text[i]=text[i+1];
  --*length;
  *removed_out=removed;
  return 1;
}''',
'''; R0=text, R1=length, R2=index, R3=removed_out.
cmp r0,#0 | beq sdc_bad | cmp r1,#0 | beq sdc_bad | cmp r3,#0 | beq sdc_bad | ldr r12,[r1] | cmp r2,r12 | bhs sdc_bad | push {r4,r5} | ldrb r4,[r0,r12] | cmp r4,#0 | bne sdc_fail | ldrb r4,[r0,r2]
sdc_shift: | cmp r2,r12 | bhs sdc_done | add r5,r2,#1 | ldrb r5,[r0,r5] | strb r5,[r0,r2] | adds r2,#1 | b sdc_shift
sdc_done: | subs r12,#1 | str r12,[r1] | strb r4,[r3] | pop {r4,r5} | movs r0,#1 | bx lr
sdc_fail: | pop {r4,r5}
sdc_bad: | movs r0,#0 | bx lr''',
'''uint8_t a[6]="AXRM",removed=0;uint32_t n=4;
CHECK(string_delete_character(a,&n,1,&removed)&&removed=='X'&&n==3);
CHECK(a[0]=='A'&&a[1]=='R'&&a[2]=='M'&&a[3]==0);
removed=9;CHECK(!string_delete_character(a,&n,3,&removed)&&removed==9);''')


def occurrence(last):
    name='string_last_occurrence' if last else 'string_first_occurrence'
    title='Find the '+('last' if last else 'first')+' occurrence of a character'
    update=('found=(int32_t)i;' if last else 'return (int32_t)i;')
    asm_update=('mov r4,r3' if last else 'mov r4,r3 | b soc_done')
    entry(('find-last-character-occurrence' if last else 'find-first-character-occurrence'),
          title, 'Search',
          f'int32_t {name}(const uint8_t *text, uint32_t capacity, uint8_t target)',
          'Return a zero-based index, -1 when absent, or -2 for a null input, NUL target, zero capacity, or missing terminator. The complete bound is validated.',
          '1. Scan no farther than capacity.\n2. Stop only at NUL.\n3. Track the requested matching position.\n4. Distinguish not-found from invalid input.',
          ('For "BANANA" and A, the last index is 5.' if last else
           'For "BANANA" and A, the first index is 1.'),
          f'''int32_t {name}(const uint8_t *text, uint32_t capacity,
                         uint8_t target) {{
  if (!text || !target) return -2;
  uint32_t length=0;
  while (length<capacity && text[length]) ++length;
  if (length==capacity) return -2;
  int32_t found=-1;
  for (uint32_t i=0;i<length;++i)
    if (text[i]==target) {{ {update} }}
  return found;
}}''',
          f'''; R0=text, R1=capacity, R2=target. Validate NUL before searching.
cmp r0,#0 | beq soc_invalid | cmp r2,#0 | beq soc_invalid | push {{r4-r7,lr}} | sub sp,sp,#4 | mov r5,r0 | mov r6,r2 | movs r3,#0 | bl sbl_loop | cmp r0,#0 | blt soc_pop_invalid | mov r7,r0 | mvn r4,#0 | movs r3,#0
soc_loop: | cmp r3,r7 | bhs soc_done | ldrb r12,[r5,r3] | cmp r12,r6 | bne soc_next | {asm_update}
soc_next: | adds r3,#1 | b soc_loop
soc_done: | mov r0,r4 | add sp,sp,#4 | pop {{r4-r7,pc}}
soc_pop_invalid: | add sp,sp,#4 | pop {{r4-r7,lr}}
soc_invalid: | mvn r0,#1 | bx lr''',
          f'''uint8_t a[]="BANANA",bad[]={{'A','A'}};CHECK({name}(a,7,'A')=={5 if last else 1});
CHECK({name}(a,7,'Z')==-1);CHECK({name}(bad,2,'A')==-2);
CHECK({name}(a,7,0)==-2);''', helpers=LEN_HELPER)


occurrence(False)
occurrence(True)

entry('replace-every-character-occurrence',
      'Replace every occurrence of a character', 'Transform',
'''uint32_t string_replace_character(uint8_t *text, uint32_t capacity,
                                  uint8_t old_character, uint8_t new_character)''',
'Replace every old_character before NUL and return the replacement count. Both characters must be non-NUL. Invalid or unterminated input returns UINT32_MAX without modifying text.',
'1. Validate the bounded length first.\n2. Scan exactly the characters before NUL.\n3. Replace matches and count them.',
'Replacing A with X in "BANANA" produces "BXNXNX" and returns 3.',
'''uint32_t string_replace_character(uint8_t *text, uint32_t capacity,
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
}''',
'''; R0=text, R1=capacity, R2=old byte, R3=new byte. Validate before mutation.
cmp r0,#0 | beq src_bad | cmp r2,#0 | beq src_bad | cmp r3,#0 | beq src_bad | push {r4-r7,lr} | mov r4,r0 | mov r5,r2 | mov r6,r3 | movs r2,#0
src_validate: | cmp r2,r1 | bhs src_fail | ldrb r7,[r4,r2] | adds r2,#1 | cmp r7,#0 | bne src_validate | subs r2,#1 | movs r0,#0 | movs r1,#0
src_loop: | cmp r1,r2 | bhs src_done | ldrb r7,[r4,r1] | cmp r7,r5 | bne src_next | strb r6,[r4,r1] | adds r0,#1
src_next: | adds r1,#1 | b src_loop
src_done: | pop {r4-r7,pc}
src_fail: | pop {r4-r7,lr}
src_bad: | mvn r0,#0 | bx lr''',
'''uint8_t a[]="BANANA",bad[]={'A','A'};CHECK(string_replace_character(a,7,'A','X')==3);
CHECK(a[0]=='B'&&a[1]=='X'&&a[5]=='X'&&a[6]==0);
CHECK(string_replace_character(bad,2,'A','X')==UINT32_MAX&&bad[0]=='A');
CHECK(string_replace_character(a,7,0,'X')==UINT32_MAX);''')


def case_convert(lower):
    name='string_to_ascii_lowercase' if lower else 'string_to_ascii_uppercase'
    title='Convert ASCII text to '+('lowercase' if lower else 'uppercase')
    lo,hi,delta=(ord('A'),ord('Z'),32) if lower else (ord('a'),ord('z'),-32)
    entry(('convert-ascii-text-to-lowercase' if lower else
           'convert-ascii-text-to-uppercase'),title,'Transform',
          f'int {name}(uint8_t *text, uint32_t capacity)',
          'Convert ASCII letters in place; digits, punctuation, and non-ASCII bytes remain unchanged. Missing NUL or invalid storage returns 0 before any mutation.',
          '1. Validate that NUL exists within capacity.\n2. Scan characters again.\n3. Add or subtract 32 only inside the relevant ASCII letter range.',
          ('"Arm-M3" becomes "arm-m3".' if lower else '"Arm-m3" becomes "ARM-M3".'),
          f'''int {name}(uint8_t *text, uint32_t capacity) {{
  if (!text) return 0;
  uint32_t length=0;
  while (length<capacity && text[length]) ++length;
  if (length==capacity) return 0;
  for (uint32_t i=0;i<length;++i)
    if (text[i]>={lo} && text[i]<={hi}) text[i]=(uint8_t)(text[i]+({delta}));
  return 1;
}}''',
          f'''; R0=text, R1=capacity. First find NUL, then convert safely.
cmp r0,#0 | beq scc_bad | push {{r4-r6,lr}} | mov r4,r0 | movs r2,#0
scc_validate: | cmp r2,r1 | bhs scc_fail | ldrb r3,[r4,r2] | adds r2,#1 | cmp r3,#0 | bne scc_validate | subs r2,#1 | movs r3,#0
scc_loop: | cmp r3,r2 | bhs scc_done | ldrb r5,[r4,r3] | cmp r5,#{lo} | blo scc_next | cmp r5,#{hi} | bhi scc_next | {'adds r5,#32' if lower else 'subs r5,#32'} | strb r5,[r4,r3]
scc_next: | adds r3,#1 | b scc_loop
scc_done: | movs r0,#1 | pop {{r4-r6,pc}}
scc_fail: | movs r0,#0 | pop {{r4-r6,pc}}
scc_bad: | movs r0,#0 | bx lr''',
          f'''uint8_t a[]="{('Arm-M3' if lower else 'Arm-m3')}",bad[]={{'A','B'}};
CHECK({name}(a,sizeof a));CHECK(a[0]=='{'a' if lower else 'A'}');
CHECK(a[1]=='{'r' if lower else 'R'}'&&a[4]=='{'m' if lower else 'M'}');
CHECK(!{name}(bad,2)&&bad[0]=='A');''')


case_convert(True)
case_convert(False)

entry('compare-ascii-strings-case-insensitively',
      'Compare ASCII strings without case sensitivity', 'Compare and test',
'''int32_t strings_compare_ascii_casefold(const uint8_t *left,
                                       uint32_t left_capacity,
                                       const uint8_t *right,
                                       uint32_t right_capacity)''',
'Return -1, 0, or 1 after folding ASCII A-Z to lowercase. Return 2 if either string is null or lacks NUL within its capacity. Non-ASCII bytes compare unchanged.',
'1. Validate both bounded strings.\n2. Fold one pair of ASCII bytes at a time.\n3. Return at the first difference or at NUL.',
'"Arm" and "aRM" compare equal; "abc" is less than "abd".',
'''static int length_for_casefold(const uint8_t *s,uint32_t cap) {
  if (!s) return 0; for(uint32_t i=0;i<cap;++i) if(!s[i]) return 1; return 0;
}
static uint8_t fold_ascii(uint8_t c) {
  return c>='A'&&c<='Z' ? (uint8_t)(c+32) : c;
}
int32_t strings_compare_ascii_casefold(const uint8_t *left,
                                       uint32_t left_capacity,
                                       const uint8_t *right,
                                       uint32_t right_capacity) {
  if (!length_for_casefold(left,left_capacity) ||
      !length_for_casefold(right,right_capacity)) return 2;
  for (uint32_t i=0;;++i) {
    uint8_t a=fold_ascii(left[i]), b=fold_ascii(right[i]);
    if (a<b) return -1; if (a>b) return 1; if (!a) return 0;
  }
}''',
'''; Validate both bounds, then fold bytes in R2/R3 by adding 32 for A-Z.
push {r4-r8,lr} | mov r4,r0 | mov r5,r1 | mov r6,r2 | mov r7,r3 | movs r3,#0 | bl sbl_loop | cmp r0,#0 | blt scf_bad | mov r0,r6 | mov r1,r7 | movs r3,#0 | bl sbl_loop | cmp r0,#0 | blt scf_bad
scf_loop: | ldrb r2,[r4],#1 | ldrb r3,[r6],#1 | cmp r2,#65 | blo scf_right | cmp r2,#90 | bhi scf_right | adds r2,#32
scf_right: | cmp r3,#65 | blo scf_compare | cmp r3,#90 | bhi scf_compare | adds r3,#32
scf_compare: | cmp r2,r3 | blo scf_less | bhi scf_more | cmp r2,#0 | bne scf_loop | movs r0,#0 | pop {r4-r8,pc}
scf_less: | mvn r0,#0 | pop {r4-r8,pc}
scf_more: | movs r0,#1 | pop {r4-r8,pc}
scf_bad: | movs r0,#2 | pop {r4-r8,pc}''',
'''uint8_t a[]="Arm",b[]="aRM",c[]="abd",bad[]={'x'};
CHECK(strings_compare_ascii_casefold(a,4,b,4)==0);
CHECK(strings_compare_ascii_casefold(a,4,c,4)==1);
CHECK(strings_compare_ascii_casefold(bad,1,b,4)==2);''',
helpers=LEN_HELPER)


def affix(prefix):
    name='string_starts_with' if prefix else 'string_ends_with'
    title='Test whether a string '+('starts with a prefix' if prefix else
                                    'ends with a suffix')
    slug='test-string-prefix' if prefix else 'test-string-suffix'
    offset='0' if prefix else 'text_length-affix_length'
    entry(slug,title,'Compare and test',
          f'''int32_t {name}(const uint8_t *text, uint32_t text_capacity,
                         const uint8_t *affix, uint32_t affix_capacity)''',
          'Return 1 for a match, 0 for no match, and -1 for invalid or unterminated input. The empty affix matches every valid string.',
          '1. Find both bounded lengths.\n2. Reject an affix longer than the text.\n3. Compare the required character range.',
          ('"cortex-m3" starts with "cortex".' if prefix else
           '"cortex-m3" ends with "m3".'),
          f'''static int length_for_affix(const uint8_t *s,uint32_t cap,uint32_t *n) {{
  if(!s||!n)return 0;for(uint32_t i=0;i<cap;++i)if(!s[i]){{*n=i;return 1;}}return 0;
}}
int32_t {name}(const uint8_t *text, uint32_t text_capacity,
                         const uint8_t *affix, uint32_t affix_capacity) {{
  uint32_t text_length,affix_length;
  if(!length_for_affix(text,text_capacity,&text_length) ||
     !length_for_affix(affix,affix_capacity,&affix_length)) return -1;
  if(affix_length>text_length)return 0;
  uint32_t start={offset};
  for(uint32_t i=0;i<affix_length;++i)
    if(text[start+i]!=affix[i])return 0;
  return 1;
}}''',
          f'''; R0=text,R1=text_capacity,R2=affix,R3=affix_capacity.
push {{r4-r9,lr}} | sub sp,sp,#4 | mov r4,r0 | mov r5,r1 | mov r6,r2 | mov r7,r3 | movs r3,#0 | bl sbl_loop | cmp r0,#0 | blt saf_bad | mov r8,r0 | mov r0,r6 | mov r1,r7 | movs r3,#0 | bl sbl_loop | cmp r0,#0 | blt saf_bad | mov r9,r0 | cmp r9,r8 | bhi saf_no | {'movs r5,#0' if prefix else 'sub r5,r8,r9'} | movs r7,#0
saf_loop: | cmp r7,r9 | bhs saf_yes | add r0,r5,r7 | ldrb r1,[r4,r0] | ldrb r2,[r6,r7] | cmp r1,r2 | bne saf_no | adds r7,#1 | b saf_loop
saf_yes: | movs r0,#1 | b saf_return
saf_no: | movs r0,#0 | b saf_return
saf_bad: | mvn r0,#0
saf_return: | add sp,sp,#4 | pop {{r4-r9,pc}}''',
          f'''uint8_t text[]="cortex-m3",yes[]="{('cortex' if prefix else 'm3')}",no[]="arm",bad[]={{'x'}};
CHECK({name}(text,10,yes,sizeof yes)==1);
CHECK({name}(text,10,no,sizeof no)==0);
CHECK({name}(text,10,bad,1)==-1);''',
          helpers=LEN_HELPER)


affix(True)
affix(False)

entry('count-ascii-words', 'Count ASCII words', 'Count and measure',
'int32_t string_count_ascii_words(const uint8_t *text, uint32_t capacity)',
'Count maximal runs of non-whitespace bytes. ASCII space, tab, line feed, vertical tab, form feed, and carriage return are separators. Return -1 for null or unterminated input.',
'1. Validate NUL within capacity.\n2. Track whether the scan is inside a word.\n3. Increment only when a non-space byte begins a new word.',
'For " ARM\\tC  ASM\\n", word starts occur at A, C, and A, so the result is 3.',
'''static int ascii_space(uint8_t c) {
  return c==' ' || (c>='\\t' && c<='\\r');
}
int32_t string_count_ascii_words(const uint8_t *text, uint32_t capacity) {
  if (!text) return -1;
  uint32_t length=0;
  while(length<capacity && text[length]) ++length;
  if(length==capacity || length>INT32_MAX) return -1;
  uint32_t words=0; int inside=0;
  for(uint32_t i=0;i<length;++i) {
    int space=ascii_space(text[i]);
    if(!space && !inside) ++words;
    inside=!space;
  }
  return (int32_t)words;
}''',
'''; R0=text,R1=capacity. Validate first; R3=words,R4=inside-word flag.
cmp r0,#0 | beq scw_bad | cmp r1,#0 | bmi scw_bad | push {r4-r6,lr} | mov r5,r0 | mov r6,r1 | movs r2,#0
scw_validate: | cmp r2,r6 | bhs scw_fail | ldrb r3,[r5,r2] | adds r2,#1 | cmp r3,#0 | bne scw_validate | subs r2,#1 | movs r3,#0 | movs r4,#0 | movs r1,#0
scw_loop: | cmp r1,r2 | bhs scw_done | ldrb r0,[r5,r1] | cmp r0,#32 | beq scw_space | cmp r0,#9 | blo scw_nonspace | cmp r0,#13 | bls scw_space
scw_nonspace: | cmp r4,#0 | bne scw_next | adds r3,#1 | movs r4,#1 | b scw_next
scw_space: | movs r4,#0
scw_next: | adds r1,#1 | b scw_loop
scw_done: | mov r0,r3 | pop {r4-r6,pc}
scw_fail: | pop {r4-r6,lr}
scw_bad: | mvn r0,#0 | bx lr''',
'''uint8_t a[]=" ARM\\tC  ASM\\n",empty[]="",bad[]={'A','B'};
CHECK(string_count_ascii_words(a,sizeof a)==3);
CHECK(string_count_ascii_words(empty,1)==0);
CHECK(string_count_ascii_words(bad,2)==-1);
CHECK(string_count_ascii_words(0,2)==-1);''')
