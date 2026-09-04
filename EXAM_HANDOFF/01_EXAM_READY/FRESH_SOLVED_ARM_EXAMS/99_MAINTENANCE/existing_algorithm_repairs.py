"""Complete handwritten ARM implementations for the former C-only entries."""
from algorithm_catalog import add, ENTRIES
from canonical_portal_content import EXTRA_ALGORITHMS
EXISTING=[]
def old(slug,prototype,contract,method,trace,c,asm,test,complexity='',helpers=''):
    original=next(e for e in EXTRA_ALGORITHMS if e['slug']==slug)
    add(slug,original['title'],original['family'],prototype,contract,method,trace,
        c or original['code'],asm,test,complexity or original['complexity'],helpers)
    item=ENTRIES.pop()
    item['history']='Possible variation'
    item['questions']=[]
    EXISTING.append(item)
    original.update(item)
old('insertion-sort','void insertion_sort(int *a, size_t n)',
'Sort signed words ascending in place, stably. Null input is a no-op; n is the number of accessible words.',
'1. Save the next key.\n2. Shift strictly larger prefix values right.\n3. Insert the key in its gap.',
'[3,1,2] -> [1,3,2] -> [1,2,3].',None,
'''cmp r0,#0 | beq ins_done | push {r4-r8,lr} | movs r4,#1
ins_outer: | cmp r4,r1 | bhs ins_pop | ldr r5,[r0,r4,lsl #2] | mov r6,r4
ins_inner: | cmp r6,#0 | beq ins_store | sub r7,r6,#1 | ldr r8,[r0,r7,lsl #2] | cmp r8,r5 | ble ins_store | str r8,[r0,r6,lsl #2] | subs r6,#1 | b ins_inner
ins_store: | str r5,[r0,r6,lsl #2] | adds r4,#1 | b ins_outer
ins_pop: | pop {r4-r8,lr}
ins_done: | bx lr''',
'int a[]={3,1,2,INT_MIN,INT_MAX,2};insertion_sort(a,6);CHECK(a[0]==INT_MIN&&a[1]==1&&a[2]==2&&a[3]==2&&a[4]==3&&a[5]==INT_MAX);insertion_sort(0,0);')
old('cocktail-sort','void cocktail_sort(int *a, size_t n)',
'Stable ascending adjacent-swap sort. Null input is a no-op; arrays of length below two are unchanged.',
'1. Sweep large values to the right.\n2. Shrink the high bound.\n3. Sweep small values left and shrink the low bound.',
'[3,2,1]: forward sweep gives [2,1,3]; backward sweep gives [1,2,3].',None,
'''cmp r0,#0 | beq ck_done | cmp r1,#2 | blo ck_done | push {r4-r10,lr} | movs r4,#0 | mov r5,r1
ck_outer: | add r6,r4,#1 | cmp r5,r6 | bls ck_pop | movs r7,#0 | add r6,r4,#1
ck_forward: | cmp r6,r5 | bhs ck_reverse | sub r10,r6,#1 | ldr r8,[r0,r10,lsl #2] | ldr r9,[r0,r6,lsl #2] | cmp r8,r9 | ble ck_fn | str r9,[r0,r10,lsl #2] | str r8,[r0,r6,lsl #2] | movs r7,#1
ck_fn: | adds r6,#1 | b ck_forward
ck_reverse: | cmp r7,#0 | beq ck_pop | subs r5,#1 | movs r7,#0 | sub r6,r5,#1
ck_backward: | cmp r6,r4 | bls ck_end | sub r10,r6,#1 | ldr r8,[r0,r10,lsl #2] | ldr r9,[r0,r6,lsl #2] | cmp r8,r9 | ble ck_bn | str r9,[r0,r10,lsl #2] | str r8,[r0,r6,lsl #2] | movs r7,#1
ck_bn: | subs r6,#1 | b ck_backward
ck_end: | adds r4,#1 | cmp r7,#0 | bne ck_outer
ck_pop: | pop {r4-r10,lr}
ck_done: | bx lr''',
'int a[]={3,2,1,INT_MIN,INT_MAX,2};cocktail_sort(a,6);for(int i=1;i<6;i++)CHECK(a[i-1]<=a[i]);CHECK(a[0]==INT_MIN&&a[5]==INT_MAX);cocktail_sort(0,0);')
old('shell-sort','void shell_sort(int *a, size_t n)',
'Ascending signed-word sort using halved gaps. In place and not guaranteed stable; null input is a no-op.',
'1. Choose gap=n/2.\n2. Apply insertion sort to each gap-separated subsequence.\n3. Halve the gap through one.',
'[9,3,7,1]: gap 2 gives [7,1,9,3]; gap 1 finishes [1,3,7,9].',None,
'''cmp r0,#0 | beq sh_done | push {r4-r8,lr} | lsrs r4,r1,#1
sh_gap: | cmp r4,#0 | beq sh_pop | mov r5,r4
sh_outer: | cmp r5,r1 | bhs sh_half | ldr r6,[r0,r5,lsl #2] | mov r7,r5
sh_inner: | cmp r7,r4 | blo sh_store | sub r3,r7,r4 | ldr r8,[r0,r3,lsl #2] | cmp r8,r6 | ble sh_store | str r8,[r0,r7,lsl #2] | mov r7,r3 | b sh_inner
sh_store: | str r6,[r0,r7,lsl #2] | adds r5,#1 | b sh_outer
sh_half: | lsrs r4,#1 | b sh_gap
sh_pop: | pop {r4-r8,lr}
sh_done: | bx lr''',
'int a[]={9,3,7,1,-5,INT_MAX,INT_MIN};shell_sort(a,7);for(int i=1;i<7;i++)CHECK(a[i-1]<=a[i]);CHECK(a[0]==INT_MIN&&a[6]==INT_MAX);shell_sort(0,0);')
old('radix-sort','int radix_sort_u32(uint32_t *a, size_t n, uint32_t *tmp)',
'Stable unsigned sort using four byte passes. a and tmp each hold n words and must not overlap; exact alias is rejected. Empty input succeeds. Uses 256 word counters on the stack.',
'1. Count byte frequencies.\n2. Turn counts into starting offsets.\n3. Scatter stably into scratch and copy back, for shifts 0,8,16,24.',
'[256,1,0xFFFFFFFF,0] -> [0,1,256,0xFFFFFFFF].',
'''#include <stdint.h>
#include <stddef.h>
int radix_sort_u32(uint32_t*a,size_t n,uint32_t*tmp){if(!n)return 1;if(!a||!tmp||a==tmp)return 0;size_t count[256];for(unsigned shift=0;shift<32;shift+=8){for(size_t b=0;b<256;b++)count[b]=0;for(size_t i=0;i<n;i++)count[(a[i]>>shift)&255]++;size_t sum=0;for(size_t b=0;b<256;b++){size_t c=count[b];count[b]=sum;sum+=c;}for(size_t i=0;i<n;i++){unsigned b=(a[i]>>shift)&255;tmp[count[b]++]=a[i];}for(size_t i=0;i<n;i++)a[i]=tmp[i];}return 1;}''',
'''cmp r1,#0 | beq rx_yes | cmp r0,#0 | beq rx_bad | cmp r2,#0 | beq rx_bad | cmp r0,r2 | beq rx_bad | push {r4-r11,lr} | sub sp,sp,#4 | sub sp,sp,#1024 | mov r4,r0 | mov r5,r1 | mov r6,r2 | movs r7,#0
rx_pass: | movs r8,#0 | movs r9,#0
rx_clear: | str r9,[sp,r8] | adds r8,#4 | cmp r8,#1024 | blo rx_clear | movs r8,#0
rx_count: | cmp r8,r5 | bhs rx_prefix_start | ldr r10,[r4,r8,lsl #2] | lsr r9,r10,r7 | and r9,r9,#255 | lsl r9,r9,#2 | ldr r11,[sp,r9] | adds r11,#1 | str r11,[sp,r9] | adds r8,#1 | b rx_count
rx_prefix_start: | movs r8,#0 | movs r10,#0
rx_prefix: | ldr r9,[sp,r8] | str r10,[sp,r8] | add r10,r9 | adds r8,#4 | cmp r8,#1024 | blo rx_prefix | movs r8,#0
rx_scatter: | cmp r8,r5 | bhs rx_copy_start | ldr r10,[r4,r8,lsl #2] | lsr r9,r10,r7 | and r9,r9,#255 | lsl r9,r9,#2 | ldr r11,[sp,r9] | str r10,[r6,r11,lsl #2] | adds r11,#1 | str r11,[sp,r9] | adds r8,#1 | b rx_scatter
rx_copy_start: | movs r8,#0
rx_copy: | cmp r8,r5 | bhs rx_next | ldr r9,[r6,r8,lsl #2] | str r9,[r4,r8,lsl #2] | adds r8,#1 | b rx_copy
rx_next: | adds r7,#8 | cmp r7,#32 | blo rx_pass | add sp,sp,#1024 | add sp,sp,#4 | pop {r4-r11,lr}
rx_yes: | movs r0,#1 | bx lr
rx_bad: | movs r0,#0 | bx lr''',
'uint32_t a[]={256,1,UINT32_MAX,0,1},t[5];CHECK(radix_sort_u32(a,5,t)&&a[0]==0&&a[1]==1&&a[2]==1&&a[3]==256&&a[4]==UINT32_MAX);CHECK(radix_sort_u32(0,0,0));CHECK(!radix_sort_u32(a,5,a));')
old('upper-bound-equal-range','size_t upper_bound_i32(const int *a, size_t n, int key)',
'Ascending signed input; return the first index with value>key, or n. Null returns zero. This entry supplies upper bound; combine with the existing lower-bound routine for an equal range.',
'1. Maintain [lo,hi).\n2. Move lo past values <=key.\n3. Otherwise lower hi.',
'[1,2,2,4], key 2 -> upper bound 3; lower bound 1 gives equal range [1,3).',None,
'''cmp r0,#0 | beq ub_zero | push {r4,r5} | movs r3,#0
ub_loop: | cmp r3,r1 | bhs ub_done | sub r12,r1,r3 | lsr r12,r12,#1 | add r12,r3 | ldr r4,[r0,r12,lsl #2] | cmp r4,r2 | bgt ub_left | add r3,r12,#1 | b ub_loop
ub_left: | mov r1,r12 | b ub_loop
ub_done: | mov r0,r3 | pop {r4,r5} | bx lr
ub_zero: | movs r0,#0 | bx lr''',
'int a[]={1,2,2,4};CHECK(upper_bound_i32(a,4,2)==3);CHECK(upper_bound_i32(a,4,0)==0);CHECK(upper_bound_i32(a,4,INT_MAX)==4);CHECK(upper_bound_i32(0,0,1)==0);')
old('quickselect','int quickselect(int *a, size_t n, size_t k, int *out)',
'Return 1 and the zero-based kth signed value, rearranging the input. Invalid pointers or k>=n return 0 without writing. Not stable.',
'1. Partition around the last value.\n2. Return if its final rank is k.\n3. Continue only on the side containing k.',
'[4,1,3,2], k=1 -> value 2.',None,
'''cmp r0,#0 | beq qs_bad | cmp r3,#0 | beq qs_bad | cmp r2,r1 | bhs qs_bad | push {r4-r10,lr} | movs r4,#0 | sub r5,r1,#1
qs_outer: | mov r6,r4 | mov r7,r4 | ldr r8,[r0,r5,lsl #2]
qs_scan: | cmp r6,r5 | bhs qs_pivot | ldr r9,[r0,r6,lsl #2] | cmp r9,r8 | bge qs_next | ldr r10,[r0,r7,lsl #2] | str r10,[r0,r6,lsl #2] | str r9,[r0,r7,lsl #2] | adds r7,#1
qs_next: | adds r6,#1 | b qs_scan
qs_pivot: | ldr r9,[r0,r7,lsl #2] | str r9,[r0,r5,lsl #2] | str r8,[r0,r7,lsl #2] | cmp r7,r2 | beq qs_found | bhi qs_left | add r4,r7,#1 | b qs_outer
qs_left: | sub r5,r7,#1 | b qs_outer
qs_found: | str r8,[r3] | movs r0,#1 | pop {r4-r10,pc}
qs_bad: | movs r0,#0 | bx lr''',
'int a[]={4,1,3,2},v=0;CHECK(quickselect(a,4,1,&v)&&v==2);int b[]={2,2,2};CHECK(quickselect(b,3,2,&v)&&v==2);CHECK(!quickselect(a,4,4,&v));')
old('rectangular-matrix-transpose','int matrix_transpose(const int *in, size_t rows, size_t cols, int *out)',
'Transpose a row-major signed-word matrix into disjoint output with rows*cols words. Zero dimensions succeed. Reject null nonempty inputs, exact aliasing, and products exceeding the 32-bit word-address range.',
'1. Read input[r*cols+c].\n2. Write output[c*rows+r].',
'[[1,2,3],[4,5,6]] -> [[1,4],[2,5],[3,6]].',
'''#include <stddef.h>
#include <stdint.h>
int matrix_transpose(const int*a,size_t r,size_t c,int*out){if(!r||!c)return 1;if(!a||!out||a==out||r>0x3fffffffu/c)return 0;for(size_t i=0;i<r;i++)for(size_t j=0;j<c;j++)out[j*r+i]=a[i*c+j];return 1;}''',
'''cmp r1,#0 | beq tx_yes | cmp r2,#0 | beq tx_yes | cmp r0,#0 | beq tx_bad | cmp r3,#0 | beq tx_bad | cmp r0,r3 | beq tx_bad | push {r4-r8,lr} | umull r4,r5,r1,r2 | cmp r5,#0 | bne tx_fail | lsr r5,r4,#30 | cmp r5,#0 | bne tx_fail | movs r4,#0
tx_row: | cmp r4,r1 | bhs tx_done | movs r5,#0
tx_col: | cmp r5,r2 | bhs tx_next | mla r6,r4,r2,r5 | mla r7,r5,r1,r4 | ldr r8,[r0,r6,lsl #2] | str r8,[r3,r7,lsl #2] | adds r5,#1 | b tx_col
tx_next: | adds r4,#1 | b tx_row
tx_done: | pop {r4-r8,lr}
tx_yes: | movs r0,#1 | bx lr
tx_fail: | pop {r4-r8,lr}
tx_bad: | movs r0,#0 | bx lr''',
'int a[]={1,2,3,4,5,6},o[7]={0};o[6]=77;CHECK(matrix_transpose(a,2,3,o)&&o[0]==1&&o[1]==4&&o[4]==3&&o[5]==6&&o[6]==77);CHECK(!matrix_transpose(a,2,3,a));CHECK(matrix_transpose(0,0,4,0));')
old('subset-sum','int subset_sum(const unsigned short *a, size_t n, size_t target, unsigned char *reachable)',
'Return whether target can be formed using each item at most once. reachable has target+1 bytes. Null inputs or target==SIZE_MAX return 0; zero-valued items do not change reachability.',
'1. Mark only sum zero reachable.\n2. Process each positive value.\n3. Traverse sums downward to prevent reusing that item.',
'values [3,5], target 6 -> false; target 8 -> true.',
'''#include <stddef.h>
#include <stdint.h>
int subset_sum(const unsigned short*a,size_t n,size_t target,unsigned char*r){if(!a||!r||target==SIZE_MAX)return 0;for(size_t s=0;s<=target;s++)r[s]=0;r[0]=1;for(size_t i=0;i<n;i++)if(a[i])for(size_t s=target+1;s>a[i];){--s;if(r[s-a[i]])r[s]=1;}return r[target]!=0;}''',
'''cmp r0,#0 | beq su_bad | cmp r3,#0 | beq su_bad | cmn r2,#1 | beq su_bad | push {r4-r8,lr} | movs r4,#0 | movs r5,#0
su_init: | strb r5,[r3,r4] | cmp r4,r2 | beq su_start | adds r4,#1 | b su_init
su_start: | movs r5,#1 | strb r5,[r3] | movs r4,#0
su_outer: | cmp r4,r1 | bhs su_done | ldrh r5,[r0,r4,lsl #1] | cmp r5,#0 | beq su_next | add r6,r2,#1
su_inner: | cmp r6,r5 | bls su_next | subs r6,#1 | sub r7,r6,r5 | ldrb r8,[r3,r7] | cmp r8,#0 | beq su_inner | movs r8,#1 | strb r8,[r3,r6] | b su_inner
su_next: | adds r4,#1 | b su_outer
su_done: | ldrb r0,[r3,r2] | pop {r4-r8,pc}
su_bad: | movs r0,#0 | bx lr''',
'unsigned short a[]={3,5};unsigned char r[10];CHECK(!subset_sum(a,2,6,r));CHECK(subset_sum(a,2,8,r));CHECK(subset_sum(a,0,0,r));')
old('base-conversion','size_t u32_to_base(unsigned value, unsigned base, char *out, size_t cap)',
'Convert an unsigned word to base 2..16, uppercase digits, and append a terminator. Return digit count, or 0 before output writes on invalid base, null output or insufficient capacity.',
'1. Collect remainders in a 32-byte scratch buffer.\n2. Check space for digits and terminator.\n3. Reverse the digits into output.',
'31,base16 -> "1F"; 5,base2 -> "101".',
'''#include <stddef.h>
size_t u32_to_base(unsigned v,unsigned b,char*out,size_t cap){if(!out||b<2||b>16)return 0;char d[32];size_t n=0;do{unsigned x=v%b;d[n++]=(char)(x<10?48+x:55+x);v/=b;}while(v);if(cap<=n)return 0;for(size_t i=0;i<n;i++)out[i]=d[n-1-i];out[n]=0;return n;}''',
'''cmp r2,#0 | beq cv_bad | cmp r1,#2 | blo cv_bad | cmp r1,#16 | bhi cv_bad | push {r4-r8,lr} | sub sp,sp,#32 | movs r4,#0
cv_digits: | udiv r5,r0,r1 | mls r6,r5,r1,r0 | cmp r6,#10 | blo cv_decimal | adds r6,#55 | b cv_put
cv_decimal: | adds r6,#48
cv_put: | strb r6,[sp,r4] | adds r4,#1 | mov r0,r5 | cmp r0,#0 | bne cv_digits | cmp r3,r4 | bls cv_fail | mov r5,r4 | movs r6,#0
cv_copy: | subs r5,#1 | ldrb r7,[sp,r5] | strb r7,[r2,r6] | adds r6,#1 | cmp r5,#0 | bne cv_copy | movs r7,#0 | strb r7,[r2,r6] | mov r0,r4 | b cv_done
cv_fail: | movs r0,#0
cv_done: | add sp,sp,#32 | pop {r4-r8,pc}
cv_bad: | movs r0,#0 | bx lr''',
'char o[34]={0};CHECK(u32_to_base(31,16,o,3)==2&&o[0]==49&&o[1]==70&&o[2]==0);o[0]=88;CHECK(!u32_to_base(31,16,o,2)&&o[0]==88);CHECK(u32_to_base(UINT_MAX,2,o,33)==32);')
old('debounce-state-machine','typedef struct{uint8_t stable,candidate;uint16_t ticks;}Debounce;\nint debounce_update(Debounce *s, uint8_t sample, uint16_t required, uint8_t *changed)',
'Caller initializes stable/candidate/ticks. Require required>=1; samples are byte states. Return 1 for a valid update and set changed only when required consecutive samples confirm a new state.',
'1. A new candidate starts at one sample.\n2. Repeated samples increment the counter up to required.\n3. Publish a changed stable state at the threshold.',
'stable=0, required=2, samples 1,0,1,1 -> changed only on the last sample.',None,
'''cmp r0,#0 | beq db_bad | cmp r3,#0 | beq db_bad | uxth r2,r2 | cmp r2,#0 | beq db_bad | push {r4,r5} | uxtb r1,r1 | movs r4,#0 | strb r4,[r3] | ldrb r4,[r0,#1] | cmp r4,r1 | beq db_same | strb r1,[r0,#1] | movs r4,#1 | strh r4,[r0,#2] | b db_check
db_same: | ldrh r4,[r0,#2] | cmp r4,r2 | bhs db_check | adds r4,#1 | strh r4,[r0,#2]
db_check: | cmp r4,r2 | bne db_done | ldrb r5,[r0] | cmp r5,r1 | beq db_done | strb r1,[r0] | movs r4,#1 | strb r4,[r3]
db_done: | movs r0,#1 | pop {r4,r5} | bx lr
db_bad: | movs r0,#0 | bx lr''',
'Debounce s={0,0,0};uint8_t c=9;CHECK(debounce_update(&s,1,2,&c)&&!c);CHECK(debounce_update(&s,0,2,&c)&&!c);CHECK(debounce_update(&s,1,2,&c)&&!c);CHECK(debounce_update(&s,1,2,&c)&&c&&s.stable==1);CHECK(debounce_update(&s,0,1,&c)&&c&&!s.stable);')
old('threshold-hysteresis','int hysteresis_update(uint16_t sample, uint16_t low, uint16_t high, uint8_t *state)',
'Require low<high and a state pointer. While off, turn on at sample>=high; while on, turn off at sample<=low. Retain state inside the band. Return 0 on invalid input, otherwise 1.',
'1. Read the current state.\n2. Apply its corresponding threshold.\n3. Retain state inside the band.',
'low=10,high=20: samples 21,15,9 -> states 1,1,0.',None,
'''cmp r3,#0 | beq hy_bad | uxth r0,r0 | uxth r1,r1 | uxth r2,r2 | cmp r1,r2 | bhs hy_bad | ldrb r12,[r3] | cmp r12,#0 | bne hy_on | cmp r0,r2 | blo hy_done | movs r0,#1 | strb r0,[r3] | b hy_done
hy_on: | cmp r0,r1 | bhi hy_done | movs r0,#0 | strb r0,[r3]
hy_done: | movs r0,#1 | bx lr
hy_bad: | movs r0,#0 | bx lr''',
'uint8_t s=0;CHECK(hysteresis_update(21,10,20,&s)&&s==1);CHECK(hysteresis_update(15,10,20,&s)&&s==1);CHECK(hysteresis_update(9,10,20,&s)&&s==0);CHECK(!hysteresis_update(1,20,10,&s));')

# Graph examples use a documented 256-vertex/dimension teaching bound.
old('topological-sort','size_t topological_sort(const uint8_t *a, size_t n, size_t *degree, size_t *queue, size_t *out)',
'Byte adjacency matrix, n<=256. degree, queue and out each hold n words and do not overlap. Return n for a complete order; return 0 on a cycle or invalid input. A cycle may leave a valid partial order.',
'1. Count incoming edges.\n2. Queue vertices of indegree zero.\n3. Remove them, decrementing outgoing neighbors.',
'Edges 0->1 and 1->2: initial queue [0], then [1], then [2]; order [0,1,2].',
'''#include <stddef.h>
#include <stdint.h>
size_t topological_sort(const uint8_t*a,size_t n,size_t*d,size_t*q,size_t*out){if(!a||!d||!q||!out||n>256)return 0;size_t h=0,t=0;for(size_t i=0;i<n;i++){d[i]=0;for(size_t j=0;j<n;j++)d[i]+=a[j*n+i]!=0;if(!d[i])q[t++]=i;}while(h<t){size_t v=q[h];out[h++]=v;for(size_t j=0;j<n;j++)if(a[v*n+j]&&!--d[j])q[t++]=j;}return h==n?h:0;}''',
'''cmp r0,#0 | beq tp_bad | cmp r2,#0 | beq tp_bad | cmp r3,#0 | beq tp_bad | cmp r1,#256 | bhi tp_bad | push {r4-r11,lr} | sub sp,sp,#4 | ldr r4,[sp,#40] | cmp r4,#0 | beq tp_fail | movs r5,#0 | movs r8,#0
tp_init: | cmp r5,r1 | bhs tp_begin | movs r6,#0 | movs r10,#0
tp_degree: | cmp r6,r1 | bhs tp_ds | mla r11,r6,r1,r5 | ldrb r9,[r0,r11] | cmp r9,#0 | beq tp_dn | adds r10,#1
tp_dn: | adds r6,#1 | b tp_degree
tp_ds: | str r10,[r2,r5,lsl #2] | cmp r10,#0 | bne tp_in | str r5,[r3,r8,lsl #2] | adds r8,#1
tp_in: | adds r5,#1 | b tp_init
tp_begin: | movs r7,#0
tp_loop: | cmp r7,r8 | bhs tp_check | ldr r9,[r3,r7,lsl #2] | str r9,[r4,r7,lsl #2] | adds r7,#1 | movs r6,#0
tp_edges: | cmp r6,r1 | bhs tp_loop | mla r11,r9,r1,r6 | ldrb r10,[r0,r11] | cmp r10,#0 | beq tp_en | ldr r10,[r2,r6,lsl #2] | subs r10,#1 | str r10,[r2,r6,lsl #2] | bne tp_en | str r6,[r3,r8,lsl #2] | adds r8,#1
tp_en: | adds r6,#1 | b tp_edges
tp_check: | cmp r7,r1 | bne tp_fail | mov r0,r7 | b tp_return
tp_fail: | movs r0,#0
tp_return: | add sp,sp,#4 | pop {r4-r11,pc}
tp_bad: | movs r0,#0 | bx lr''',
'uint8_t a[]={0,1,0,0,0,1,0,0,0};size_t d[3],q[3],o[3];CHECK(topological_sort(a,3,d,q,o)==3&&o[0]==0&&o[2]==2);a[6]=1;CHECK(topological_sort(a,3,d,q,o)==0);')
old('bipartite-test','int graph_is_bipartite(const uint8_t *a, size_t n, int8_t *color, size_t *queue)',
'Undirected byte adjacency matrix, n<=256. Supply n color bytes and n queue words. Return 1 for a two-coloring across all components, or 0 on conflict or invalid input.',
'1. Initialize all colors to -1.\n2. BFS each uncolored component.\n3. Assign opposite colors and reject equal-color edges.',
'A three-vertex path is bipartite; adding its closing edge creates an odd cycle.',
'''#include <stddef.h>
#include <stdint.h>
int graph_is_bipartite(const uint8_t*a,size_t n,int8_t*c,size_t*q){if(!a||!c||!q||n>256)return 0;for(size_t i=0;i<n;i++)c[i]=-1;for(size_t s=0;s<n;s++)if(c[s]<0){size_t h=0,t=0;c[s]=0;q[t++]=s;while(h<t){size_t v=q[h++];for(size_t w=0;w<n;w++)if(a[v*n+w]){if(c[w]<0){c[w]=1-c[v];q[t++]=w;}else if(c[w]==c[v])return 0;}}}return 1;}''',
'''cmp r0,#0 | beq bi_bad | cmp r2,#0 | beq bi_bad | cmp r3,#0 | beq bi_bad | cmp r1,#256 | bhi bi_bad | push {r4-r10,lr} | movs r4,#0 | movs r5,#255
bi_init: | cmp r4,r1 | bhs bi_start | strb r5,[r2,r4] | adds r4,#1 | b bi_init
bi_start: | movs r4,#0
bi_component: | cmp r4,r1 | bhs bi_ok | ldrsb r5,[r2,r4] | cmp r5,#0 | bge bi_next_component | movs r5,#0 | strb r5,[r2,r4] | str r4,[r3] | movs r6,#1
bi_queue: | cmp r5,r6 | bhs bi_next_component | ldr r7,[r3,r5,lsl #2] | adds r5,#1 | movs r8,#0
bi_edge: | cmp r8,r1 | bhs bi_queue | mla r10,r7,r1,r8 | ldrb r9,[r0,r10] | cmp r9,#0 | beq bi_next_edge | ldrsb r9,[r2,r8] | ldrb r10,[r2,r7] | cmp r9,#0 | bge bi_compare | eor r10,r10,#1 | strb r10,[r2,r8] | str r8,[r3,r6,lsl #2] | adds r6,#1 | b bi_next_edge
bi_compare: | cmp r9,r10 | beq bi_fail
bi_next_edge: | adds r8,#1 | b bi_edge
bi_next_component: | adds r4,#1 | b bi_component
bi_ok: | movs r0,#1 | pop {r4-r10,pc}
bi_fail: | pop {r4-r10,lr}
bi_bad: | movs r0,#0 | bx lr''',
'uint8_t a[]={0,1,0,1,0,1,0,1,0};int8_t c[3];size_t q[3];CHECK(graph_is_bipartite(a,3,c,q)&&c[0]!=c[1]&&c[1]!=c[2]);a[2]=a[6]=1;CHECK(!graph_is_bipartite(a,3,c,q));uint8_t self[]={1};CHECK(!graph_is_bipartite(self,1,c,q));')
old('directed-cycle-detection','int directed_cycle(const uint8_t *a, size_t n, uint8_t *state)',
'Directed byte adjacency matrix, n<=256, and n state bytes. Return 1 for a cycle, 0 otherwise or for invalid input. Initialize states internally. Recursion uses at most n helper frames.',
'1. Mark a vertex gray on entry.\n2. A gray neighbor proves a back edge.\n3. Recurse into white vertices, then mark the vertex black.',
'0->1->2 is acyclic; 2->0 reaches gray vertex 0 and proves a cycle.',
'''#include <stddef.h>
#include <stdint.h>
static int cycle_visit(const uint8_t*a,size_t n,size_t v,uint8_t*s){s[v]=1;for(size_t w=0;w<n;w++)if(a[v*n+w]){if(s[w]==1)return 1;if(!s[w]&&cycle_visit(a,n,w,s))return 1;}s[v]=2;return 0;}
int directed_cycle(const uint8_t*a,size_t n,uint8_t*s){if(!a||!s||n>256)return 0;for(size_t i=0;i<n;i++)s[i]=0;for(size_t i=0;i<n;i++)if(!s[i]&&cycle_visit(a,n,i,s))return 1;return 0;}''',
'''cmp r0,#0 | beq cy_bad | cmp r2,#0 | beq cy_bad | cmp r1,#256 | bhi cy_bad | push {r4-r8,lr} | mov r4,r0 | mov r5,r1 | mov r6,r2 | movs r7,#0 | movs r8,#0
cy_init: | cmp r7,r5 | bhs cy_start | strb r8,[r6,r7] | adds r7,#1 | b cy_init
cy_start: | movs r7,#0
cy_outer: | cmp r7,r5 | bhs cy_no | ldrb r0,[r6,r7] | cmp r0,#0 | bne cy_next | mov r0,r4 | mov r1,r5 | mov r2,r7 | mov r3,r6 | bl cy_visit | cmp r0,#0 | bne cy_return
cy_next: | adds r7,#1 | b cy_outer
cy_no: | movs r0,#0
cy_return: | pop {r4-r8,pc}
cy_bad: | movs r0,#0 | bx lr''',
'uint8_t a[]={0,1,0,0,0,1,0,0,0},s[3];CHECK(!directed_cycle(a,3,s));a[6]=1;CHECK(directed_cycle(a,3,s));uint8_t self[]={1};CHECK(directed_cycle(self,1,s));',
helpers='''cy_visit: | push {r4-r8,lr} | mov r4,r0 | mov r5,r1 | mov r6,r2 | mov r7,r3 | movs r0,#1 | strb r0,[r7,r6] | movs r8,#0
cy_vloop: | cmp r8,r5 | bhs cy_black | mla r0,r6,r5,r8 | ldrb r0,[r4,r0] | cmp r0,#0 | beq cy_vnext | ldrb r0,[r7,r8] | cmp r0,#1 | beq cy_found | cmp r0,#0 | bne cy_vnext | mov r0,r4 | mov r1,r5 | mov r2,r8 | mov r3,r7 | bl cy_visit | cmp r0,#0 | bne cy_vreturn
cy_vnext: | adds r8,#1 | b cy_vloop
cy_black: | movs r0,#2 | strb r0,[r7,r6] | movs r0,#0 | b cy_vreturn
cy_found: | movs r0,#1
cy_vreturn: | pop {r4-r8,pc}''')
old('prim-mst','unsigned prim_mst(const unsigned *w, size_t n, size_t start, unsigned *best, unsigned char *used)',
'Undirected symmetric weight matrix with zero meaning no edge; n=1..256. Supply n best words and n used bytes. Return MST weight, or UINT_MAX for invalid input, disconnection or unrepresentable total. UINT_MAX is reserved.',
'1. Start one vertex at cost zero.\n2. Add the unused vertex with smallest connection cost.\n3. Update neighbor costs and check the accumulated weight.',
'Triangle weights 0-1=2,1-2=3,0-2=9 -> MST weight 5.',
'''#include <stddef.h>
#include <limits.h>
unsigned prim_mst(const unsigned*w,size_t n,size_t s,unsigned*b,unsigned char*u){if(!w||!b||!u||s>=n||n>256)return UINT_MAX;for(size_t i=0;i<n;i++){b[i]=UINT_MAX;u[i]=0;}b[s]=0;unsigned total=0;for(size_t k=0;k<n;k++){size_t v=n;unsigned low=UINT_MAX;for(size_t i=0;i<n;i++)if(!u[i]&&b[i]<low){low=b[i];v=i;}if(v==n||low>=UINT_MAX-total)return UINT_MAX;u[v]=1;total+=low;for(size_t i=0;i<n;i++)if(!u[i]&&w[v*n+i]&&w[v*n+i]<b[i])b[i]=w[v*n+i];}return total;}''',
'''cmp r0,#0 | beq pr_bad | cmp r3,#0 | beq pr_bad | cmp r2,r1 | bhs pr_bad | cmp r1,#256 | bhi pr_bad | push {r4-r11,lr} | sub sp,sp,#4 | ldr r4,[sp,#40] | cmp r4,#0 | beq pr_fail | movs r9,#0 | mvn r10,#0 | movs r11,#0
pr_init: | cmp r9,r1 | bhs pr_start | str r10,[r3,r9,lsl #2] | strb r11,[r4,r9] | adds r9,#1 | b pr_init
pr_start: | str r11,[r3,r2,lsl #2] | movs r5,#0 | movs r6,#0
pr_outer: | cmp r6,r1 | bhs pr_done | mov r7,r1 | mvn r8,#0 | movs r9,#0
pr_select: | cmp r9,r1 | bhs pr_accept | ldrb r10,[r4,r9] | cmp r10,#0 | bne pr_sn | ldr r10,[r3,r9,lsl #2] | cmp r10,r8 | bhs pr_sn | mov r8,r10 | mov r7,r9
pr_sn: | adds r9,#1 | b pr_select
pr_accept: | cmp r7,r1 | beq pr_fail | adds r5,r5,r8 | bcs pr_fail | cmn r5,#1 | beq pr_fail | movs r10,#1 | strb r10,[r4,r7] | movs r9,#0
pr_edges: | cmp r9,r1 | bhs pr_next | ldrb r10,[r4,r9] | cmp r10,#0 | bne pr_en | mla r12,r7,r1,r9 | ldr r10,[r0,r12,lsl #2] | cmp r10,#0 | beq pr_en | ldr r11,[r3,r9,lsl #2] | cmp r10,r11 | bhs pr_en | str r10,[r3,r9,lsl #2]
pr_en: | adds r9,#1 | b pr_edges
pr_next: | adds r6,#1 | b pr_outer
pr_done: | mov r0,r5 | b pr_return
pr_fail: | mvn r0,#0
pr_return: | add sp,sp,#4 | pop {r4-r11,pc}
pr_bad: | mvn r0,#0 | bx lr''',
'unsigned w[]={0,2,9,2,0,3,9,3,0},b[3];unsigned char u[3];CHECK(prim_mst(w,3,0,b,u)==5);unsigned d[]={0,0,0,0};CHECK(prim_mst(d,2,0,b,u)==UINT_MAX);CHECK(prim_mst(d,1,0,b,u)==0);unsigned big[]={0,UINT_MAX-1,0,UINT_MAX-1,0,2,0,2,0};CHECK(prim_mst(big,3,0,b,u)==UINT_MAX);')
old('kruskal-mst','typedef struct{size_t u,v;unsigned w;}MstEdge;\nunsigned kruskal_mst(const MstEdge *edges, size_t m, size_t n, size_t *parent)',
'Supply edges sorted by nondecreasing weight, n=1..256, valid endpoints and n parent words. Return MST weight or UINT_MAX for invalid ordering/endpoints, disconnection or total overflow. This generic MST differs from the supplied maze-generation exam.',
'1. Validate ordering and endpoints.\n2. Initialize one component per vertex.\n3. Accept edges joining different roots, checking total weight.',
'Sorted edges (0,1,2),(1,2,3),(0,2,9): accept the first two, total 5.',
'''#include <stddef.h>
#include <limits.h>
#include <stdint.h>
typedef struct{size_t u,v;unsigned w;}MstEdge;
static size_t mst_root(size_t*p,size_t x){while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;}
unsigned kruskal_mst(const MstEdge*e,size_t m,size_t n,size_t*p){if(!p||!n||n>256||(!e&&m)||m>UINT32_MAX/12)return UINT_MAX;for(size_t i=0;i<m;i++)if(e[i].u>=n||e[i].v>=n||(i&&e[i].w<e[i-1].w))return UINT_MAX;for(size_t i=0;i<n;i++)p[i]=i;size_t used=0;unsigned total=0;for(size_t i=0;i<m&&used+1<n;i++){size_t a=mst_root(p,e[i].u),b=mst_root(p,e[i].v);if(a!=b){if(e[i].w>=UINT_MAX-total)return UINT_MAX;p[b]=a;total+=e[i].w;used++;}}return used+1==n?total:UINT_MAX;}''',
'''cmp r3,#0 | beq kr_bad | cmp r2,#1 | blo kr_bad | cmp r2,#256 | bhi kr_bad | cmp r1,#0 | beq kr_setup | cmp r0,#0 | beq kr_bad
kr_setup: | push {r4-r11,lr} | sub sp,sp,#12 | mov r4,r0 | mov r5,r1 | mov r6,r2 | mov r7,r3 | ldr r0,=357913941 | cmp r5,r0 | bhi kr_fail | movs r8,#0 | movs r9,#0
kr_validate: | cmp r8,r5 | bhs kr_initialize | add r11,r8,r8,lsl #1 | add r11,r4,r11,lsl #2 | ldr r0,[r11] | cmp r0,r6 | bhs kr_fail | ldr r0,[r11,#4] | cmp r0,r6 | bhs kr_fail | ldr r0,[r11,#8] | cmp r0,r9 | blo kr_fail | mov r9,r0 | adds r8,#1 | b kr_validate
kr_initialize: | movs r8,#0
kr_init: | cmp r8,r6 | bhs kr_start | str r8,[r7,r8,lsl #2] | adds r8,#1 | b kr_init
kr_start: | movs r8,#0 | movs r9,#0 | movs r10,#0
kr_loop: | add r0,r9,#1 | cmp r0,r6 | beq kr_done | cmp r8,r5 | bhs kr_fail | add r11,r8,r8,lsl #1 | add r11,r4,r11,lsl #2 | mov r0,r7 | ldr r1,[r11] | bl kr_root | str r0,[sp] | mov r0,r7 | ldr r1,[r11,#4] | bl kr_root | ldr r1,[sp] | cmp r0,r1 | beq kr_next | ldr r2,[r11,#8] | adds r10,r10,r2 | bcs kr_fail | cmn r10,#1 | beq kr_fail | str r1,[r7,r0,lsl #2] | adds r9,#1
kr_next: | adds r8,#1 | b kr_loop
kr_done: | mov r0,r10 | b kr_return
kr_fail: | mvn r0,#0
kr_return: | add sp,sp,#12 | pop {r4-r11,pc}
kr_bad: | mvn r0,#0 | bx lr''',
'MstEdge e[]={{0,1,2},{1,2,3},{0,2,9}};size_t p[3];CHECK(kruskal_mst(e,3,3,p)==5);e[2].v=3;CHECK(kruskal_mst(e,3,3,p)==UINT_MAX);CHECK(kruskal_mst(0,0,1,p)==0);CHECK(kruskal_mst(0,0,2,p)==UINT_MAX);',
helpers='''kr_root: | ldr r2,[r0,r1,lsl #2] | cmp r2,r1 | beq kr_root_done | ldr r3,[r0,r2,lsl #2] | str r3,[r0,r1,lsl #2] | mov r1,r3 | b kr_root
kr_root_done: | mov r0,r1 | bx lr''')
old('bellman-ford','typedef struct{size_t from,to;int weight;}Edge;\nint bellman_ford(const Edge *edges, size_t m, size_t n, size_t start, int *distance)',
'Directed edge list, n=1..256, valid endpoints, and n distance words. INT_MAX is unreachable and reserved. Return 0 for invalid input, reachable negative cycle or arithmetic outside INT_MIN..INT_MAX-1; failure during relaxation may leave partial distances.',
'1. Validate every endpoint before indexing.\n2. Relax all edges up to n-1 times, exiting if unchanged.\n3. An improvement on pass n proves a reachable negative cycle.',
'Edges 0->1 weight 4,1->2 weight -2,0->2 weight 9 yield distances [0,4,2].',
'''#include <stddef.h>
#include <limits.h>
#include <stdint.h>
typedef struct{size_t from,to;int weight;}Edge;
int bellman_ford(const Edge*e,size_t m,size_t n,size_t s,int*d){if(!d||(!e&&m)||s>=n||n>256||m>UINT32_MAX/12)return 0;for(size_t i=0;i<m;i++)if(e[i].from>=n||e[i].to>=n)return 0;for(size_t i=0;i<n;i++)d[i]=INT_MAX;d[s]=0;for(size_t k=1;k<=n;k++){int changed=0;for(size_t i=0;i<m;i++)if(d[e[i].from]!=INT_MAX){int64_t x=(int64_t)d[e[i].from]+e[i].weight;if(x<INT_MIN||x>=INT_MAX)return 0;if(x<d[e[i].to]){if(k==n)return 0;d[e[i].to]=(int)x;changed=1;}}if(!changed)return 1;}return 1;}''',
'''cmp r3,r2 | bhs bf_bad | cmp r2,#256 | bhi bf_bad | cmp r1,#0 | beq bf_setup | cmp r0,#0 | beq bf_bad
bf_setup: | push {r4-r11,lr} | sub sp,sp,#20 | str r3,[sp] | mov r4,r0 | mov r5,r1 | mov r6,r2 | ldr r7,[sp,#56] | cmp r7,#0 | beq bf_fail | ldr r0,=357913941 | cmp r5,r0 | bhi bf_fail | movs r9,#0 | ldr r11,=2147483647
bf_validate: | cmp r9,r5 | bhs bf_initialize | add r0,r9,r9,lsl #1 | add r0,r4,r0,lsl #2 | ldr r1,[r0] | ldr r2,[r0,#4] | cmp r1,r6 | bhs bf_fail | cmp r2,r6 | bhs bf_fail | adds r9,#1 | b bf_validate
bf_initialize: | movs r9,#0
bf_init: | cmp r9,r6 | bhs bf_start | str r11,[r7,r9,lsl #2] | adds r9,#1 | b bf_init
bf_start: | ldr r0,[sp] | movs r1,#0 | str r1,[r7,r0,lsl #2] | movs r8,#1
bf_pass: | movs r9,#0 | movs r10,#0
bf_edge: | cmp r9,r5 | bhs bf_nextpass | add r0,r9,r9,lsl #1 | add r0,r4,r0,lsl #2 | ldr r1,[r0] | ldr r2,[r0,#4] | ldr r3,[r0,#8] | ldr r1,[r7,r1,lsl #2] | cmp r1,r11 | beq bf_nextedge | adds r1,r1,r3 | bvs bf_fail | cmp r1,r11 | beq bf_fail | ldr r3,[r7,r2,lsl #2] | cmp r1,r3 | bge bf_nextedge | cmp r8,r6 | beq bf_fail | str r1,[r7,r2,lsl #2] | movs r10,#1
bf_nextedge: | adds r9,#1 | b bf_edge
bf_nextpass: | cmp r10,#0 | beq bf_good | adds r8,#1 | b bf_pass
bf_good: | movs r0,#1 | b bf_return
bf_fail: | movs r0,#0
bf_return: | add sp,sp,#20 | pop {r4-r11,pc}
bf_bad: | movs r0,#0 | bx lr''',
'Edge e[]={{0,1,4},{1,2,-2},{0,2,9}};int d[3];CHECK(bellman_ford(e,3,3,0,d)&&d[0]==0&&d[1]==4&&d[2]==2);e[2].from=9;CHECK(!bellman_ford(e,3,3,0,d));Edge cyc[]={{0,1,1},{1,0,-2}};CHECK(!bellman_ford(cyc,2,2,0,d));CHECK(bellman_ford(0,0,3,0,d)&&d[1]==INT_MAX);')
old('floyd-warshall','int floyd_warshall(int *distance, size_t n, int infinity)',
'In-place distance matrix, n<=256, positive infinity sentinel. Finite distances must be less than infinity; initialize diagonal to zero. Candidates at or above infinity remain unrepresentable. Return 0 on invalid input, signed overflow or negative cycle, possibly after partial updates.',
'1. For each intermediate k, visit all pairs i,j.\n2. Skip unreachable legs.\n3. Add finite legs with overflow checking and improve the distance.',
'0->1=4,1->2=-2,0->2=9: after intermediate 1, distance 0->2 becomes 2.',
'''#include <stddef.h>
#include <stdint.h>
#include <limits.h>
int floyd_warshall(int*d,size_t n,int inf){if(!d||n>256||inf<=0)return 0;for(size_t k=0;k<n;k++)for(size_t i=0;i<n;i++)for(size_t j=0;j<n;j++)if(d[i*n+k]!=inf&&d[k*n+j]!=inf){int64_t x=(int64_t)d[i*n+k]+d[k*n+j];if(x<INT_MIN||x>INT_MAX)return 0;if(x<d[i*n+j])d[i*n+j]=(int)x;}for(size_t i=0;i<n;i++)if(d[i*n+i]<0)return 0;return 1;}''',
'''cmp r0,#0 | beq fw_bad | cmp r1,#256 | bhi fw_bad | cmp r2,#0 | ble fw_bad | push {r4-r10,lr} | movs r4,#0
fw_k: | cmp r4,r1 | bhs fw_diag_start | movs r5,#0
fw_i: | cmp r5,r1 | bhs fw_kn | movs r6,#0
fw_j: | cmp r6,r1 | bhs fw_in | mla r7,r5,r1,r4 | ldr r8,[r0,r7,lsl #2] | cmp r8,r2 | beq fw_jn | mla r7,r4,r1,r6 | ldr r9,[r0,r7,lsl #2] | cmp r9,r2 | beq fw_jn | adds r8,r8,r9 | bvs fw_fail | mla r7,r5,r1,r6 | ldr r10,[r0,r7,lsl #2] | cmp r8,r10 | bge fw_jn | str r8,[r0,r7,lsl #2]
fw_jn: | adds r6,#1 | b fw_j
fw_in: | adds r5,#1 | b fw_i
fw_kn: | adds r4,#1 | b fw_k
fw_diag_start: | movs r4,#0
fw_diag: | cmp r4,r1 | bhs fw_ok | mla r5,r4,r1,r4 | ldr r6,[r0,r5,lsl #2] | cmp r6,#0 | blt fw_fail | adds r4,#1 | b fw_diag
fw_ok: | movs r0,#1 | pop {r4-r10,pc}
fw_fail: | pop {r4-r10,lr}
fw_bad: | movs r0,#0 | bx lr''',
'int d[]={0,4,9,999,0,-2,999,999,0};CHECK(floyd_warshall(d,3,999)&&d[2]==2&&d[3]==999);int cyc[]={0,-1,-1,0};CHECK(!floyd_warshall(cyc,2,999));int big[]={0,INT_MAX-1,INT_MAX-1,0};CHECK(!floyd_warshall(big,2,INT_MAX));')
old('a-star-grid','int astar_grid(const unsigned char *wall, size_t rows, size_t cols, size_t start, size_t goal, unsigned *g, unsigned char *closed)',
'Four-neighbor unit-cost grid, rows/cols=1..256, zero=passage and nonzero=wall. g and closed each have rows*cols elements and do not overlap other storage. Return 1 if the goal is reachable, with its shortest distance in g[goal]; return 0 for invalid or unreachable input. Blocked start/goal fail.',
'1. Set start distance to zero and other distances to UINT_MAX.\n2. Select the open cell minimizing g plus Manhattan distance.\n3. Close it and relax legal unblocked neighbors.\n4. Stop at the goal or when no open cell remains.',
'Open 2x3 grid, start 0, goal 5: a shortest path uses 3 steps. A full middle wall column makes the goal unreachable.',
'''#include <stddef.h>
#include <limits.h>
int astar_grid(const unsigned char*w,size_t rows,size_t cols,size_t start,size_t goal,unsigned*g,unsigned char*c){if(!w||!g||!c||!rows||!cols||rows>256||cols>256)return 0;size_t n=rows*cols;if(start>=n||goal>=n||w[start]||w[goal])return 0;for(size_t i=0;i<n;i++){g[i]=UINT_MAX;c[i]=0;}g[start]=0;for(;;){size_t v=n;unsigned best=UINT_MAX;for(size_t i=0;i<n;i++)if(!c[i]&&g[i]!=UINT_MAX){size_t r=i/cols,x=i%cols,gr=goal/cols,gx=goal%cols;unsigned h=(unsigned)((r>gr?r-gr:gr-r)+(x>gx?x-gx:gx-x));if(g[i]+h<best){best=g[i]+h;v=i;}}if(v==n)return 0;if(v==goal)return 1;c[v]=1;size_t next[4],count=0;if(v>=cols)next[count++]=v-cols;if(v+cols<n)next[count++]=v+cols;if(v%cols)next[count++]=v-1;if(v%cols+1<cols)next[count++]=v+1;for(size_t j=0;j<count;j++){size_t x=next[j];if(!w[x]&&!c[x]&&g[v]+1<g[x])g[x]=g[v]+1;}}}''',
'''push {r4-r11,lr} | sub sp,sp,#28 | mov r4,r0 | mov r5,r1 | mov r6,r2 | ldr r7,[sp,#64] | ldr r8,[sp,#68] | ldr r9,[sp,#72] | cmp r4,#0 | beq as_bad | cmp r8,#0 | beq as_bad | cmp r9,#0 | beq as_bad | cmp r5,#1 | blo as_bad | cmp r6,#1 | blo as_bad | cmp r5,#256 | bhi as_bad | cmp r6,#256 | bhi as_bad | mul r10,r5,r6 | cmp r3,r10 | bhs as_bad | cmp r7,r10 | bhs as_bad | ldrb r0,[r4,r3] | cmp r0,#0 | bne as_bad | ldrb r0,[r4,r7] | cmp r0,#0 | bne as_bad | movs r0,#0 | mvn r1,#0 | movs r2,#0
as_init: | cmp r0,r10 | bhs as_start | str r1,[r8,r0,lsl #2] | strb r2,[r9,r0] | adds r0,#1 | b as_init
as_start: | str r2,[r8,r3,lsl #2] | udiv r0,r7,r6 | mls r1,r0,r6,r7 | str r0,[sp,#16] | str r1,[sp,#20]
as_outer: | str r10,[sp] | mvn r0,#0 | str r0,[sp,#4] | movs r0,#0
as_scan: | cmp r0,r10 | bhs as_choose | ldrb r1,[r9,r0] | cmp r1,#0 | bne as_sn | ldr r1,[r8,r0,lsl #2] | cmn r1,#1 | beq as_sn | udiv r2,r0,r6 | mls r3,r2,r6,r0 | ldr r11,[sp,#16] | subs r2,r2,r11 | bpl as_rowabs | rsb r2,r2,#0
as_rowabs: | add r1,r2 | ldr r11,[sp,#20] | subs r3,r3,r11 | bpl as_colabs | rsb r3,r3,#0
as_colabs: | add r1,r3 | ldr r2,[sp,#4] | cmp r1,r2 | bhs as_sn | str r1,[sp,#4] | str r0,[sp]
as_sn: | adds r0,#1 | b as_scan
as_choose: | ldr r11,[sp] | cmp r11,r10 | beq as_bad | cmp r11,r7 | beq as_good | movs r0,#1 | strb r0,[r9,r11] | ldr r0,[r8,r11,lsl #2] | adds r0,#1 | str r0,[sp,#8] | cmp r11,r6 | blo as_down | sub r0,r11,r6 | bl as_relax
as_down: | add r0,r11,r6 | cmp r0,r10 | bhs as_left | bl as_relax
as_left: | udiv r0,r11,r6 | mls r0,r0,r6,r11 | cmp r0,#0 | beq as_right | sub r0,r11,#1 | bl as_relax
as_right: | udiv r0,r11,r6 | mls r0,r0,r6,r11 | adds r0,#1 | cmp r0,r6 | bhs as_outer | add r0,r11,#1 | bl as_relax | b as_outer
as_good: | movs r0,#1 | b as_return
as_bad: | movs r0,#0
as_return: | add sp,sp,#28 | pop {r4-r11,pc}''',
'unsigned char w[6]={0},c[6];unsigned g[6];CHECK(astar_grid(w,2,3,0,5,g,c)&&g[5]==3);w[1]=w[4]=1;CHECK(!astar_grid(w,2,3,0,5,g,c));w[1]=w[4]=0;w[0]=1;CHECK(!astar_grid(w,2,3,0,0,g,c));w[0]=0;CHECK(astar_grid(w,2,3,0,0,g,c)&&g[0]==0);CHECK(!astar_grid(w,0,3,0,0,g,c));',
helpers='''as_relax: | ldrb r1,[r4,r0] | cmp r1,#0 | bne as_relax_done | ldrb r1,[r9,r0] | cmp r1,#0 | bne as_relax_done | ldr r1,[r8,r0,lsl #2] | ldr r2,[sp,#8] | cmp r2,r1 | bhs as_relax_done | str r2,[r8,r0,lsl #2]
as_relax_done: | bx lr''')
