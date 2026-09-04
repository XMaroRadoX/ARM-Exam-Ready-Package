"""Handwritten byte strings, bounded parsing and encoding routines."""
from algorithm_catalog import add
S='Strings'
add('byte-string-palindrome','Byte-string palindrome',S,
'int bytes_palindrome(const uint8_t *text, uint32_t length)',
'Compare exactly length bytes, case-sensitive. Empty input is a palindrome; null with nonzero length fails.',
'1. Position indexes at opposite ends.\n2. Reject unequal bytes.\n3. Move toward the center.',
'"radar": compare r/r, a/a; center d needs no comparison.',
'int bytes_palindrome(const uint8_t*s,uint32_t n){if(!s&&n)return 0;for(uint32_t i=0;i<n/2;i++)if(s[i]!=s[n-1-i])return 0;return 1;}',
'''cmp r1,#0 | beq sp_yes | cmp r0,#0 | beq sp_no | push {r4,r5} | movs r2,#0 | subs r1,#1
sp_loop: | cmp r2,r1 | bhs sp_ok | ldrb r3,[r0,r2] | ldrb r4,[r0,r1] | cmp r3,r4 | bne sp_fail | adds r2,#1 | subs r1,#1 | b sp_loop
sp_ok: | pop {r4,r5}
sp_yes: | movs r0,#1 | bx lr
sp_fail: | pop {r4,r5}
sp_no: | movs r0,#0 | bx lr''',
'uint8_t a[]={114,97,100,97,114},b[]={0,255,0};CHECK(bytes_palindrome(a,5));CHECK(bytes_palindrome(b,3));CHECK(!bytes_palindrome(a,4));CHECK(bytes_palindrome(0,0));')
add('byte-string-reversal','In-place byte-string reversal',S,
'int bytes_reverse(uint8_t *text, uint32_t length)',
'Reverse exactly length bytes in place; do not include a terminator unless deliberately part of the span. Return 1, or 0 for null with nonzero length.',
'1. Swap the first and last bytes.\n2. Move inward until indexes meet.',
'"abcd" -> "dbca" -> "dcba".',
'int bytes_reverse(uint8_t*s,uint32_t n){if(!s&&n)return 0;for(uint32_t i=0;i<n/2;i++){uint8_t t=s[i];s[i]=s[n-1-i];s[n-1-i]=t;}return 1;}',
'''cmp r1,#0 | beq sr_yes | cmp r0,#0 | beq sr_no | push {r4,r5} | movs r2,#0 | subs r1,#1
sr_loop: | cmp r2,r1 | bhs sr_done | ldrb r3,[r0,r2] | ldrb r4,[r0,r1] | strb r4,[r0,r2] | strb r3,[r0,r1] | adds r2,#1 | subs r1,#1 | b sr_loop
sr_done: | pop {r4,r5}
sr_yes: | movs r0,#1 | bx lr
sr_no: | movs r0,#0 | bx lr''',
'uint8_t a[]={1,2,3,4,77};CHECK(bytes_reverse(a,4)&&a[0]==4&&a[3]==1&&a[4]==77);CHECK(bytes_reverse(0,0));CHECK(!bytes_reverse(0,1));')
add('byte-character-count','Character count in a byte span',S,
'uint32_t byte_count(const uint8_t *text, uint32_t length, uint8_t key)',
'Count every occurrence, including zero bytes, within the explicit span. Null input returns zero.',
'1. Load unsigned bytes.\n2. Increment for each exact match.',
'[0,255,0,1], key 0 -> count 2.',
'uint32_t byte_count(const uint8_t*s,uint32_t n,uint8_t key){uint32_t c=0;if(s)for(uint32_t i=0;i<n;i++)c+=s[i]==key;return c;}',
'''movs r3,#0 | cmp r0,#0 | beq cc_done | push {r4,r5} | uxtb r2,r2
cc_loop: | cmp r1,#0 | beq cc_pop | ldrb r4,[r0],#1 | cmp r4,r2 | bne cc_next | adds r3,#1
cc_next: | subs r1,#1 | b cc_loop
cc_pop: | pop {r4,r5}
cc_done: | mov r0,r3 | bx lr''',
'uint8_t a[]={0,255,0,1};CHECK(byte_count(a,4,0)==2);CHECK(byte_count(a,4,255)==1);CHECK(byte_count(0,0,0)==0);')
for count in (False,True):
 name='substring_count' if count else 'substring_first'
 ret='uint32_t' if count else 'int32_t'
 fail='UINT32_MAX' if count else '-1'
 found='k++;' if count else 'return (int32_t)i;'
 finish='k' if count else '-1'
 add(name.replace('_','-'),'Overlapping substring count' if count else 'First substring occurrence',S,
 f'{ret} {name}(const uint8_t *text, uint32_t length, const uint8_t *pattern, uint32_t pattern_length)',
 f'Compare explicit byte spans. Require length<=INT32_MAX. Empty pattern {"matches length+1 positions" if count else "returns index zero"}. Invalid pointers return {fail}; absent nonempty pattern returns {"zero" if count else "-1"}.',
 '1. Test each legal start position.\n2. Compare pattern bytes until mismatch or completion.\n3. '+('Advance by one even after a match, retaining overlaps.' if count else 'Return immediately on the first match.'),
 '"aaaa" with "aa": first index 0; overlapping count 3.',
 f'{ret} {name}(const uint8_t*s,uint32_t n,const uint8_t*p,uint32_t m){{if(n>INT32_MAX||(!s&&n)||(!p&&m))return {fail};if(!m)return {"n+1" if count else "0"};if(m>n)return {"0" if count else "-1"};uint32_t k=0;(void)k;for(uint32_t i=0;i<=n-m;i++){{uint32_t j=0;while(j<m&&s[i+j]==p[j])j++;if(j==m){{{found}}}}}return {finish};}}',
 f'''cmp r1,#0 | bmi ss_bad | cmp r1,#0 | beq ss_pcheck | cmp r0,#0 | beq ss_bad
ss_pcheck: | cmp r3,#0 | beq ss_empty | cmp r2,#0 | beq ss_bad | cmp r3,r1 | bhi ss_absent | push {{r4-r10,lr}} | sub r4,r1,r3 | movs r5,#0 | movs r6,#0
ss_outer: | cmp r5,r4 | bhi ss_done | movs r7,#0
ss_inner: | cmp r7,r3 | beq ss_found | add r8,r5,r7 | ldrb r9,[r0,r8] | ldrb r10,[r2,r7] | cmp r9,r10 | bne ss_next | adds r7,#1 | b ss_inner
ss_found: | {"adds r6,#1" if count else "mov r0,r5 | pop {r4-r10,pc}"}
ss_next: | adds r5,#1 | b ss_outer
ss_done: | {"mov r0,r6" if count else "mvn r0,#0"} | pop {{r4-r10,pc}}
ss_empty: | {"add r0,r1,#1" if count else "movs r0,#0"} | bx lr
ss_absent: | {"movs r0,#0" if count else "mvn r0,#0"} | bx lr
ss_bad: | mvn r0,#0 | bx lr''',
 f'uint8_t s[]={{97,97,97,97}},p[]={{97,97}},z[]={{98}};CHECK({name}(s,4,p,2)=={3 if count else 0});CHECK({name}(s,4,z,1)=={0 if count else -1});CHECK({name}(s,4,0,0)=={5 if count else 0});CHECK({name}(0,0,p,2)=={0 if count else -1});',
 complexity='O(length * pattern_length) time, O(1) space')
add('byte-anagram-test','Case-sensitive byte anagram test',S,
'int byte_anagram(const uint8_t *a, uint32_t n, const uint8_t *b, uint32_t m)',
'Return 1 when equal-length byte spans have identical multiplicities. Empty spans match. Uses 256 word counters (1024 stack bytes).',
'1. Require equal lengths.\n2. Count bytes from the first span.\n3. Consume counts with the second span; reject a missing occurrence.',
'"aab" versus "aba": counts a=2,b=1; all counts consumed.',
'int byte_anagram(const uint8_t*a,uint32_t n,const uint8_t*b,uint32_t m){if(n!=m||((!a||!b)&&n))return 0;uint32_t f[256]={0};for(uint32_t i=0;i<n;i++)f[a[i]]++;for(uint32_t i=0;i<n;i++){if(!f[b[i]])return 0;f[b[i]]--;}return 1;}',
'''cmp r1,r3 | bne ag_bad | cmp r1,#0 | beq ag_yes | cmp r0,#0 | beq ag_bad | cmp r2,#0 | beq ag_bad | push {r4-r8,lr} | sub sp,sp,#1024 | movs r3,#0 | movs r4,#0
ag_clear: | str r3,[sp,r4] | adds r4,#4 | cmp r4,#1024 | blo ag_clear | movs r4,#0
ag_count: | cmp r4,r1 | bhs ag_second | ldrb r5,[r0,r4] | lsl r5,r5,#2 | ldr r6,[sp,r5] | adds r6,#1 | str r6,[sp,r5] | adds r4,#1 | b ag_count
ag_second: | movs r4,#0
ag_consume: | cmp r4,r1 | bhs ag_ok | ldrb r5,[r2,r4] | lsl r5,r5,#2 | ldr r6,[sp,r5] | cmp r6,#0 | beq ag_fail | subs r6,#1 | str r6,[sp,r5] | adds r4,#1 | b ag_consume
ag_ok: | movs r0,#1 | b ag_finish
ag_fail: | movs r0,#0
ag_finish: | add sp,sp,#1024 | pop {r4-r8,pc}
ag_yes: | movs r0,#1 | bx lr
ag_bad: | movs r0,#0 | bx lr''',
'uint8_t a[]={97,97,98},b[]={97,98,97},c[]={97,98,98};CHECK(byte_anagram(a,3,b,3));CHECK(!byte_anagram(a,3,c,3));CHECK(byte_anagram(0,0,0,0));CHECK(!byte_anagram(a,3,b,2));',
complexity='O(n+256) time, 1024 bytes of counter storage')
for signed in (False,True):
 name='parse_i32' if signed else 'parse_u32'
 typ='int32_t' if signed else 'uint32_t'
 prefix='int neg=0;if(n&&(s[0]==45||s[0]==43)){neg=s[0]==45;s++;n--;}if(!n)return 0;' if signed else ''
 check='if(v>(neg?2147483648u:2147483647u))return 0;' if signed else ''
 write='*out=neg?(int32_t)(-(int64_t)v):(int32_t)v;' if signed else '*out=v;'
 preasm='''movs r7,#0 | ldrb r4,[r0] | cmp r4,#45 | beq pa_negative | cmp r4,#43 | bne pa_digits | b pa_skip
pa_negative: | movs r7,#1
pa_skip: | adds r0,#1 | subs r1,#1 | beq pa_fail
pa_digits: | ''' if signed else ''
 postasm='''ldr r4,=2147483647 | add r4,r7 | cmp r3,r4 | bhi pa_fail | cmp r7,#0 | beq pa_write | rsb r3,r3,#0
pa_write: | ''' if signed else ''
 add(name.replace('_','-'),'Checked '+('signed' if signed else 'unsigned')+' decimal parsing',S,
 f'int {name}(const uint8_t *text, uint32_t length, {typ} *out)',
 'Parse the entire nonempty span. '+('Allow one leading + or -.' if signed else 'Accept decimal digits only, without a sign.')+' Reject spaces, invalid bytes and overflow. Return 1 on success or 0 without changing output.',
 '1. Check optional sign when supported.\n2. Validate each decimal digit.\n3. Check multiply/add overflow before accepting the result.',
 '"123": accumulated values 1,12,123; "12x" fails without output.',
 f'int {name}(const uint8_t*s,uint32_t n,{typ}*out){{if(!s||!out||!n)return 0;{prefix}uint32_t v=0;for(uint32_t i=0;i<n;i++){{if(s[i]<48||s[i]>57)return 0;uint32_t d=s[i]-48;if(v>429496729u||(v==429496729u&&d>5))return 0;v=v*10+d;}}{check}{write}return 1;}}',
 f'''cmp r0,#0 | beq pa_bad | cmp r1,#0 | beq pa_bad | cmp r2,#0 | beq pa_bad | push {{r4-r8,lr}} | {preasm}movs r3,#0 | movs r6,#10
pa_loop: | ldrb r4,[r0],#1 | subs r4,#48 | cmp r4,#9 | bhi pa_fail | umull r5,r8,r3,r6 | cmp r8,#0 | bne pa_fail | adds r3,r5,r4 | bcs pa_fail | subs r1,#1 | bne pa_loop | {postasm}str r3,[r2] | movs r0,#1 | pop {{r4-r8,pc}}
pa_fail: | movs r0,#0 | pop {{r4-r8,pc}}
pa_bad: | movs r0,#0 | bx lr''',
 f'{typ} v=99;CHECK({name}((const uint8_t*)"123",3,&v)&&v==123);v=99;CHECK(!{name}((const uint8_t*)"12x",3,&v)&&v==99);CHECK(!{name}((const uint8_t*)"",0,&v));'+
 ('CHECK(parse_i32((const uint8_t*)"-2147483648",11,&v)&&v==INT32_MIN);CHECK(!parse_i32((const uint8_t*)"2147483648",10,&v));CHECK(!parse_i32((const uint8_t*)"-",1,&v));' if signed else 'CHECK(parse_u32((const uint8_t*)"4294967295",10,&v)&&v==UINT32_MAX);CHECK(!parse_u32((const uint8_t*)"4294967296",10,&v));'))
add('format-signed-decimal','Signed decimal formatting',S,
'uint32_t format_i32(int32_t value, char *out, uint32_t capacity)',
'Write signed decimal text plus a zero terminator. Return character count excluding the terminator, or 0 before output writes for null or insufficient capacity. INT32_MIN is supported.',
'1. Form the unsigned magnitude without signed negation overflow.\n2. Collect digits backwards in a 12-byte scratch buffer.\n3. Check capacity, then emit sign and reversed digits.',
'-120: scratch digits 0,2,1; output "-120", length 4, capacity at least 5.',
'uint32_t format_i32(int32_t v,char*out,uint32_t cap){char d[12];uint32_t x=v<0?(uint32_t)(-(int64_t)v):(uint32_t)v,n=0,k=0;do{d[n++]=(char)(48+x%10);x/=10;}while(x);uint32_t len=n+(v<0);if(!out||cap<=len)return 0;if(v<0)out[k++]=45;while(n)out[k++]=d[--n];out[k]=0;return k;}',
'''cmp r1,#0 | beq fm_bad | push {r4-r8,lr} | sub sp,sp,#16 | movs r4,#0 | cmp r0,#0 | bge fm_start | movs r4,#1 | rsb r0,r0,#0
fm_start: | movs r5,#0 | movs r6,#10
fm_digits: | udiv r7,r0,r6 | mls r8,r7,r6,r0 | adds r8,#48 | strb r8,[sp,r5] | adds r5,#1 | mov r0,r7 | cmp r0,#0 | bne fm_digits | add r7,r5,r4 | cmp r2,r7 | bls fm_fail | movs r3,#0 | cmp r4,#0 | beq fm_copy | movs r0,#45 | strb r0,[r1],#1 | movs r3,#1
fm_copy: | subs r5,#1 | ldrb r0,[sp,r5] | strb r0,[r1],#1 | adds r3,#1 | cmp r5,#0 | bne fm_copy | movs r0,#0 | strb r0,[r1] | mov r0,r3 | b fm_done
fm_fail: | movs r0,#0
fm_done: | add sp,sp,#16 | pop {r4-r8,pc}
fm_bad: | movs r0,#0 | bx lr''',
'char s[13]={0};s[12]=77;CHECK(format_i32(INT32_MIN,s,12)==11&&s[0]==45&&s[10]==56&&s[11]==0&&s[12]==77);s[0]=88;CHECK(!format_i32(-120,s,4)&&s[0]==88);CHECK(format_i32(0,s,2)==1&&s[0]==48&&s[1]==0);',
complexity='At most 10 digit iterations and 12 scratch bytes')
WS='''trim_space: | cmp r3,#32 | beq tw_true | cmp r3,#9 | blo tw_false | cmp r3,#13 | bhi tw_false
tw_true: | movs r3,#1 | bx lr
tw_false: | movs r3,#0 | bx lr'''
add('trim-ascii-whitespace','Trim leading and trailing ASCII whitespace',S,
'uint32_t trim_ascii(uint8_t *text, uint32_t length)',
'Compact the trimmed byte span in place, without appending a terminator. Whitespace is space or byte 9..13. Return remaining length; null input returns zero.',
'1. Find the first non-whitespace byte.\n2. Find the last non-whitespace byte.\n3. Move the retained span to the beginning.',
'[space,tab,A,B,space,newline] -> [A,B], length 2.',
'static int trim_space_c(uint8_t c){return c==32||(c>=9&&c<=13);}uint32_t trim_ascii(uint8_t*s,uint32_t n){if(!s)return 0;uint32_t l=0;while(l<n&&trim_space_c(s[l]))l++;while(n>l&&trim_space_c(s[n-1]))n--;uint32_t k=n-l;for(uint32_t i=0;i<k;i++)s[i]=s[l+i];return k;}',
'''cmp r0,#0 | beq tr_bad | push {r4-r8,lr} | mov r4,r0 | mov r5,r1 | movs r6,#0
tr_left: | cmp r6,r5 | bhs tr_right | ldrb r3,[r4,r6] | bl trim_space | cmp r3,#0 | beq tr_right | adds r6,#1 | b tr_left
tr_right: | cmp r5,r6 | bls tr_move | sub r7,r5,#1 | ldrb r3,[r4,r7] | bl trim_space | cmp r3,#0 | beq tr_move | subs r5,#1 | b tr_right
tr_move: | sub r0,r5,r6 | movs r7,#0
tr_copy: | cmp r7,r0 | bhs tr_done | add r8,r6,r7 | ldrb r3,[r4,r8] | strb r3,[r4,r7] | adds r7,#1 | b tr_copy
tr_done: | pop {r4-r8,pc}
tr_bad: | movs r0,#0 | bx lr''',
'uint8_t s[]={32,9,65,66,32,10},a[]={9,32,13};CHECK(trim_ascii(s,6)==2&&s[0]==65&&s[1]==66);CHECK(trim_ascii(a,3)==0);CHECK(trim_ascii(0,0)==0);',helpers=WS)
add('bounded-run-length-decoding','Bounded run-length decoding',S,
'uint32_t rle_decode(const uint8_t *pairs, uint32_t pair_count, uint8_t *out, uint32_t capacity)',
'Input consists of pair_count (count,value) byte pairs; zero count is invalid. Preflight total length and capacity before writing. Return decoded length or UINT32_MAX on invalid input; input/output must not overlap.',
'1. Sum all run lengths, rejecting zero counts and overflow.\n2. Check output capacity.\n3. Emit each value exactly count times.',
'[(3,A),(2,B)] -> AAABB, length 5.',
'uint32_t rle_decode(const uint8_t*p,uint32_t n,uint8_t*out,uint32_t cap){if((!p&&n)||n>UINT32_MAX/2)return UINT32_MAX;uint32_t total=0;for(uint32_t i=0;i<n;i++){uint32_t c=p[2*i];if(!c||total>UINT32_MAX-c)return UINT32_MAX;total+=c;}if(total>cap||(!out&&total))return UINT32_MAX;uint32_t k=0;for(uint32_t i=0;i<n;i++)for(uint32_t j=0;j<p[2*i];j++)out[k++]=p[2*i+1];return k;}',
'''cmp r1,#0 | bmi rl_bad | cmp r1,#0 | beq rl_zero | cmp r0,#0 | beq rl_bad | push {r4-r8,lr} | movs r4,#0 | movs r5,#0
rl_scan: | cmp r4,r1 | bhs rl_check | lsl r6,r4,#1 | ldrb r7,[r0,r6] | cmp r7,#0 | beq rl_fail | adds r5,r5,r7 | bcs rl_fail | adds r4,#1 | b rl_scan
rl_check: | cmp r5,r3 | bhi rl_fail | cmp r2,#0 | beq rl_fail | movs r4,#0 | movs r5,#0
rl_outer: | cmp r4,r1 | bhs rl_done | lsl r6,r4,#1 | ldrb r7,[r0,r6] | adds r6,#1 | ldrb r8,[r0,r6]
rl_inner: | strb r8,[r2,r5] | adds r5,#1 | subs r7,#1 | bne rl_inner | adds r4,#1 | b rl_outer
rl_done: | mov r0,r5 | pop {r4-r8,pc}
rl_fail: | pop {r4-r8,lr}
rl_bad: | mvn r0,#0 | bx lr
rl_zero: | movs r0,#0 | bx lr''',
'uint8_t p[]={3,65,2,66},o[6]={0};o[5]=77;CHECK(rle_decode(p,2,o,5)==5&&o[2]==65&&o[3]==66&&o[5]==77);o[0]=88;CHECK(rle_decode(p,2,o,4)==UINT32_MAX&&o[0]==88);uint8_t z[]={0,65};CHECK(rle_decode(z,1,o,5)==UINT32_MAX);CHECK(rle_decode(0,0,0,0)==0);',
complexity='O(pair_count+decoded_length) time, O(1) extra space')
add('eight-digit-packed-bcd','Eight-digit packed BCD encoding',S,
'int packed_bcd(uint32_t value, uint32_t *out)',
'Accept 0..99999999. Write eight decimal nibbles in a 32-bit result, with leading zero nibbles. Return 1, or 0 without writing on invalid input.',
'1. Extract each decimal digit.\n2. Insert it into the next four-bit position.\n3. Repeat eight times.',
'12345678 -> 0x12345678; 42 -> 0x00000042.',
'int packed_bcd(uint32_t v,uint32_t*out){if(!out||v>99999999)return 0;uint32_t r=0;for(uint32_t i=0;i<8;i++){r|=(v%10)<<(4*i);v/=10;}*out=r;return 1;}',
'''cmp r1,#0 | beq bd_bad | ldr r2,=99999999 | cmp r0,r2 | bhi bd_bad | push {r4-r6,lr} | movs r2,#0 | movs r3,#0 | movs r4,#10
bd_loop: | udiv r5,r0,r4 | mls r6,r5,r4,r0 | lsl r6,r6,r3 | orr r2,r2,r6 | mov r0,r5 | adds r3,#4 | cmp r3,#32 | blo bd_loop | str r2,[r1] | movs r0,#1 | pop {r4-r6,pc}
bd_bad: | movs r0,#0 | bx lr''',
'uint32_t v=0;CHECK(packed_bcd(12345678,&v)&&v==0x12345678);CHECK(packed_bcd(42,&v)&&v==0x42);CHECK(packed_bcd(0,&v)&&v==0);v=99;CHECK(!packed_bcd(100000000,&v)&&v==99);',
complexity='Exactly eight iterations')
