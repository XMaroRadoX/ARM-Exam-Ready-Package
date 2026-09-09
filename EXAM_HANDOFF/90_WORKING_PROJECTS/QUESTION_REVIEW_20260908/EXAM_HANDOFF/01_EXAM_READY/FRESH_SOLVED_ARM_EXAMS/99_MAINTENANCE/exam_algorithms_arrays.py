"""Directly authored array scans, transformations, and wide reductions."""
from algorithm_catalog import add
A='Arrays and matrices'
add('array-length-contract','Array length: fixed count or bounded sentinel',A,
'int bounded_word_length(const uint32_t *a, uint32_t capacity, uint32_t sentinel, uint32_t *length)',
'For a fixed C array, use sizeof array / sizeof array[0] at the caller. A pointer has no length. This routine handles only an explicit sentinel-terminated word array: return 1 and the number of words before the first sentinel within capacity, or return 0 without writing when no sentinel is found or a required pointer is null.',
'1. If the real array is visible, calculate its element count with sizeof array / sizeof array[0].\n2. After an array becomes a pointer, pass its count separately.\n3. Only when the data contract defines a sentinel, scan no farther than capacity and return the sentinel index as the length.',
'For {4,7,0,9}, capacity 4, sentinel 0: the sentinel is at index 2, so the bounded length is 2. Without a sentinel contract, the known fixed-array count is 4 and must be passed by the caller.',
'int bounded_word_length(const uint32_t*a,uint32_t capacity,uint32_t sentinel,uint32_t*length){if(!a||!length)return 0;for(uint32_t i=0;i<capacity;i++)if(a[i]==sentinel){*length=i;return 1;}return 0;}',
'''cmp r0,#0 | beq al_bad | cmp r3,#0 | beq al_bad | push {r4,lr} | movs r4,#0
al_loop: | cmp r4,r1 | bhs al_missing | ldr r12,[r0,r4,lsl #2] | cmp r12,r2 | beq al_found | adds r4,#1 | b al_loop
al_found: | str r4,[r3] | movs r0,#1 | pop {r4,pc}
al_missing: | movs r0,#0 | pop {r4,pc}
al_bad: | movs r0,#0 | bx lr''',
'uint32_t a[]={4,7,0,9},b[]={4,7,9},length=99;size_t count=sizeof a/sizeof a[0];CHECK(count==4);CHECK(bounded_word_length(a,(uint32_t)count,0,&length)&&length==2);length=99;CHECK(!bounded_word_length(b,3,0,&length)&&length==99);CHECK(!bounded_word_length(0,0,0,&length)&&length==99);',
complexity='O(capacity) worst-case time; O(1) auxiliary storage',
registers='R0=array base, R1=maximum element count, R2=sentinel value, R3=length output. R4 is saved and used as the index. R0 returns 1 when the sentinel is found, otherwise 0.')
for largest in (True,False):
 name='second_largest' if largest else 'second_smallest'
 better='bgt' if largest else 'blt'
 worse='ble' if largest else 'bge'
 cmp='>' if largest else '<'
 add(name.replace('_','-'),name.replace('_',' ').capitalize()+' distinct value',A,
 f'int {name}(const int32_t *a, uint32_t n, int32_t *out)',
 'Return 1 and store the second distinct extremum. Return 0 without writing for null storage, empty input, or fewer than two distinct values.',
 '1. Seed the best value from element zero.\n2. Keep a separate flag for a second distinct value.\n3. Update the best and second-best using signed comparisons.',
 '[4,9,9,2]: distinct descending values 9,4,2; second largest=4, second smallest=4.',
 f'int {name}(const int32_t*a,uint32_t n,int32_t*out){{if(!a||!out||!n)return 0;int32_t best=a[0],second=0;int have=0;for(uint32_t i=1;i<n;i++){{int32_t x=a[i];if(x{cmp}best){{second=best;best=x;have=1;}}else if(x!=best&&(!have||x{cmp}second)){{second=x;have=1;}}}}if(have)*out=second;return have;}}',
 f'''cmp r0,#0 | beq sx_bad | cmp r2,#0 | beq sx_bad | cmp r1,#0 | beq sx_bad | push {{r4-r8,lr}} | ldr r4,[r0] | movs r5,#0 | movs r6,#0 | movs r3,#1
sx_loop: | cmp r3,r1 | bhs sx_done | ldr r7,[r0,r3,lsl #2] | cmp r7,r4 | {better} sx_best | beq sx_next | cmp r6,#0 | beq sx_second | cmp r7,r5 | {worse} sx_next
sx_second: | mov r5,r7 | movs r6,#1 | b sx_next
sx_best: | mov r5,r4 | mov r4,r7 | movs r6,#1
sx_next: | adds r3,#1 | b sx_loop
sx_done: | cmp r6,#0 | beq sx_no | str r5,[r2]
sx_no: | mov r0,r6 | pop {{r4-r8,pc}}
sx_bad: | movs r0,#0 | bx lr''',
 f'int32_t a[]={{4,9,9,2}},e[]={{INT32_MIN,INT32_MAX}},v=77;CHECK({name}(a,4,&v)&&v==4);CHECK({name}(e,2,&v)&&v=={"INT32_MIN" if largest else "INT32_MAX"});v=77;CHECK(!{name}(a,1,&v)&&v==77);CHECK(!{name}(0,0,&v));')
add('extrema-indexes','Minimum and maximum indexes',A,
'int extrema_indexes(const int32_t *a, uint32_t n, uint32_t *min_index, uint32_t *max_index)',
'Return 1 and the first indexes of the minimum and maximum signed words. Empty input or null required pointers returns 0 without writes. Output pointers must be distinct.',
'1. Seed both indexes with zero.\n2. Change an index only for a strictly smaller or larger value.',
'[7,-2,7,-2]: minimum index 1, maximum index 0.',
'int extrema_indexes(const int32_t*a,uint32_t n,uint32_t*lo,uint32_t*hi){if(!a||!n||!lo||!hi||lo==hi)return 0;uint32_t l=0,h=0;for(uint32_t i=1;i<n;i++){if(a[i]<a[l])l=i;if(a[i]>a[h])h=i;}*lo=l;*hi=h;return 1;}',
'''cmp r0,#0 | beq ei_bad | cmp r1,#0 | beq ei_bad | cmp r2,#0 | beq ei_bad | cmp r3,#0 | beq ei_bad | cmp r2,r3 | beq ei_bad | push {r4-r10,lr} | movs r4,#0 | movs r5,#0 | movs r6,#1 | ldr r8,[r0] | mov r9,r8
ei_loop: | cmp r6,r1 | bhs ei_done | ldr r7,[r0,r6,lsl #2] | cmp r7,r8 | bge ei_max | mov r8,r7 | mov r4,r6
ei_max: | cmp r7,r9 | ble ei_next | mov r9,r7 | mov r5,r6
ei_next: | adds r6,#1 | b ei_loop
ei_done: | str r4,[r2] | str r5,[r3] | movs r0,#1 | pop {r4-r10,pc}
ei_bad: | movs r0,#0 | bx lr''',
'int32_t a[]={7,-2,7,-2};uint32_t l=99,h=99;CHECK(extrema_indexes(a,4,&l,&h)&&l==1&&h==0);CHECK(!extrema_indexes(a,0,&l,&h)&&l==1&&h==0);')
add('count-above-threshold','Count above a signed threshold',A,
'uint32_t count_above(const int32_t *a, uint32_t n, int32_t threshold)',
'Count elements strictly greater than threshold. Empty input or a null input pointer returns zero.',
'1. Load each signed word.\n2. Compare with threshold.\n3. Increment only for a strict match.',
'[-3,0,4,4], threshold 0 -> count 2.',
'uint32_t count_above(const int32_t*a,uint32_t n,int32_t t){uint32_t c=0;if(a)for(uint32_t i=0;i<n;i++)if(a[i]>t)c++;return c;}',
'''movs r3,#0 | cmp r0,#0 | beq ca_done | push {r4,r5}
ca_loop: | cmp r1,#0 | beq ca_pop | ldr r4,[r0],#4 | cmp r4,r2 | ble ca_next | adds r3,#1
ca_next: | subs r1,#1 | b ca_loop
ca_pop: | pop {r4,r5}
ca_done: | mov r0,r3 | bx lr''',
'int32_t a[]={-3,0,4,4};CHECK(count_above(a,4,0)==2);CHECK(count_above(a,4,INT32_MAX)==0);CHECK(count_above(0,0,0)==0);')
add('stable-threshold-filter','Stable threshold filtering',A,
'uint32_t threshold_filter(const int32_t *a, uint32_t n, int32_t threshold, int32_t *out, uint32_t capacity)',
'Copy values strictly greater than threshold in input order. Output capacity must be at least n; exact in-place filtering is allowed, other overlap is not. Return count or UINT32_MAX on invalid input before writing.',
'1. Validate worst-case output capacity.\n2. Scan left to right.\n3. Write accepted values at the next output index.',
'[4,-1,7,4], threshold 3 -> [4,7,4], count 3.',
'uint32_t threshold_filter(const int32_t*a,uint32_t n,int32_t t,int32_t*out,uint32_t cap){if(cap<n||((!a||!out)&&n))return UINT32_MAX;uint32_t k=0;for(uint32_t i=0;i<n;i++)if(a[i]>t)out[k++]=a[i];return k;}',
'''ldr r12,[sp] | cmp r12,r1 | blo tf_bad | cmp r1,#0 | beq tf_zero | cmp r0,#0 | beq tf_bad | cmp r3,#0 | beq tf_bad | push {r4-r6,lr} | movs r4,#0
tf_loop: | cmp r1,#0 | beq tf_done | ldr r5,[r0],#4 | cmp r5,r2 | ble tf_next | str r5,[r3,r4,lsl #2] | adds r4,#1
tf_next: | subs r1,#1 | b tf_loop
tf_done: | mov r0,r4 | pop {r4-r6,pc}
tf_zero: | movs r0,#0 | bx lr
tf_bad: | mvn r0,#0 | bx lr''',
'int32_t a[]={4,-1,7,4},b[5]={0};b[4]=77;CHECK(threshold_filter(a,4,3,b,4)==3&&b[0]==4&&b[1]==7&&b[2]==4&&b[4]==77);CHECK(threshold_filter(a,4,3,b,3)==UINT32_MAX);CHECK(threshold_filter(a,4,3,a,4)==3&&a[1]==7);')
add('majority-element','Majority element with verification',A,
'int majority_element(const int32_t *a, uint32_t n, int32_t *out)',
'Return 1 and a value appearing more than n/2 times, or 0 without writing. A candidate must pass a second counting scan.',
'1. Cancel unequal pairs to choose a candidate.\n2. Count candidate occurrences.\n3. Require a strict majority.',
'[2,1,2,3,2]: candidate 2; occurrence count 3>2, return 2.',
'int majority_element(const int32_t*a,uint32_t n,int32_t*out){if(!a||!n||!out)return 0;int32_t v=0;uint32_t votes=0,c=0;for(uint32_t i=0;i<n;i++){if(!votes){v=a[i];votes=1;}else if(v==a[i])votes++;else votes--;}for(uint32_t i=0;i<n;i++)c+=a[i]==v;if(c<=n/2)return 0;*out=v;return 1;}',
'''cmp r0,#0 | beq mj_bad | cmp r1,#0 | beq mj_bad | cmp r2,#0 | beq mj_bad | push {r4-r8,lr} | movs r3,#0 | movs r4,#0 | movs r5,#0
mj_loop: | cmp r5,r1 | bhs mj_verify | ldr r6,[r0,r5,lsl #2] | cmp r3,#0 | beq mj_choose | cmp r4,r6 | beq mj_inc | subs r3,#1 | b mj_next
mj_choose: | mov r4,r6
mj_inc: | adds r3,#1
mj_next: | adds r5,#1 | b mj_loop
mj_verify: | movs r5,#0 | movs r7,#0
mj_count: | cmp r5,r1 | bhs mj_check | ldr r6,[r0,r5,lsl #2] | cmp r6,r4 | bne mj_cn | adds r7,#1
mj_cn: | adds r5,#1 | b mj_count
mj_check: | lsrs r1,#1 | cmp r7,r1 | bls mj_fail | str r4,[r2] | movs r0,#1 | pop {r4-r8,pc}
mj_fail: | movs r0,#0 | pop {r4-r8,pc}
mj_bad: | movs r0,#0 | bx lr''',
'int32_t a[]={2,1,2,3,2},b[]={1,2,3,4},v=99;CHECK(majority_element(a,5,&v)&&v==2);v=99;CHECK(!majority_element(b,4,&v)&&v==99);CHECK(!majority_element(0,0,&v));')
for sorted_input in (True,False):
 name='unique_sorted' if sorted_input else 'unique_unsorted'
 code='if(!k||a[i]!=a[k-1])a[k++]=a[i];' if sorted_input else 'uint32_t j=0;while(j<k&&a[j]!=a[i])j++;if(j==k)a[k++]=a[i];'
 body='''cmp r2,#0 | beq uq_write | sub r4,r2,#1 | ldr r5,[r0,r4,lsl #2] | cmp r3,r5 | beq uq_next''' if sorted_input else '''movs r4,#0
uq_find: | cmp r4,r2 | beq uq_write | ldr r5,[r0,r4,lsl #2] | cmp r3,r5 | beq uq_next | adds r4,#1 | b uq_find'''
 add(name.replace('_','-'),('Sorted' if sorted_input else 'Unsorted')+' duplicate removal',A,
 f'uint32_t {name}(int32_t *a, uint32_t n)',
 ('Input must be sorted in ascending signed order. ' if sorted_input else '')+'Compact distinct values in place, preserving first occurrences; return new length. Null or empty input returns zero.',
 '1. Keep a write index for accepted values.\n2. Reject a value already represented in the output prefix.\n3. Store each new value and advance.',
 '[1,1,2,3,3] -> [1,2,3], length 3.' if sorted_input else '[3,1,3,2,1] -> [3,1,2], length 3.',
 f'uint32_t {name}(int32_t*a,uint32_t n){{uint32_t k=0;if(a)for(uint32_t i=0;i<n;i++){{{code}}}return k;}}',
 f'''cmp r0,#0 | beq uq_zero | push {{r4-r6,lr}} | movs r2,#0 | movs r6,#0
uq_loop: | cmp r6,r1 | bhs uq_done | ldr r3,[r0,r6,lsl #2] | {body}
uq_write: | str r3,[r0,r2,lsl #2] | adds r2,#1
uq_next: | adds r6,#1 | b uq_loop
uq_done: | mov r0,r2 | pop {{r4-r6,pc}}
uq_zero: | movs r0,#0 | bx lr''',
 f'int32_t a[]={"{1,1,2,3,3}" if sorted_input else "{3,1,3,2,1}"};CHECK({name}(a,5)==3&&a[0]=={1 if sorted_input else 3}&&a[1]=={2 if sorted_input else 1}&&a[2]=={3 if sorted_input else 2});CHECK({name}(0,0)==0);',
 complexity='O(n) time, O(1) space' if sorted_input else 'O(n squared) time, O(1) space')
# Three two-pointer variants. Scratch output must not overlap either input.
for mode in ('merge','intersection','union'):
 name='sorted_'+mode
 if mode=='intersection':
  cb='''while(i<n&&j<m){if(a[i]<b[j])i++;else if(a[i]>b[j])j++;else{int32_t x=a[i++];j++;if(!k||out[k-1]!=x)out[k++]=x;}}'''
  ab='''cmp r6,r1 | bhs sm_done | cmp r7,r3 | bhs sm_done | ldr r9,[r0,r6,lsl #2] | ldr r10,[r2,r7,lsl #2] | cmp r9,r10 | blt sm_ia | bgt sm_ib | adds r6,#1 | adds r7,#1 | b sm_accept
sm_ia: | adds r6,#1 | b sm_loop
sm_ib: | adds r7,#1 | b sm_loop'''
 else:
  cb='''while(i<n||j<m){int32_t x;if(j==m||(i<n&&a[i]<=b[j]))x=a[i++];else x=b[j++];'''+('out[k++]=x;' if mode=='merge' else 'if(!k||out[k-1]!=x)out[k++]=x;')+'}'
  ab='''cmp r6,r1 | bhs sm_from_b | cmp r7,r3 | bhs sm_from_a | ldr r9,[r0,r6,lsl #2] | ldr r10,[r2,r7,lsl #2] | cmp r9,r10 | ble sm_from_a
sm_from_b: | cmp r7,r3 | bhs sm_done | ldr r9,[r2,r7,lsl #2] | adds r7,#1 | b sm_accept
sm_from_a: | ldr r9,[r0,r6,lsl #2] | adds r6,#1'''
  # sorted merge preserves all duplicates.
 dedup='' if mode=='merge' else '''cmp r8,#0 | beq sm_write | sub r10,r8,#1 | ldr r10,[r4,r10,lsl #2] | cmp r10,r9 | beq sm_loop
sm_write: | '''
 add(name.replace('_','-'),{'merge':'Merge two sorted arrays','intersection':'Distinct sorted intersection','union':'Distinct sorted union'}[mode],A,
 f'uint32_t {name}(const int32_t *a, uint32_t n, const int32_t *b, uint32_t m, int32_t *out, uint32_t capacity)',
 'Inputs are signed ascending arrays. Require capacity>=n+m without count overflow, and disjoint output. Return output count or UINT32_MAX before writes on invalid input. '+('Keep all duplicates.' if mode=='merge' else 'Output each selected value once.'),
 '1. Compare the next unconsumed input values.\n2. Advance the appropriate input indexes.\n3. Emit according to the merge/intersection/union rule.',
 '[1,2,2] and [2,3] -> '+{'merge':'[1,2,2,2,3]','intersection':'[2]','union':'[1,2,3]'}[mode]+'.',
 f'uint32_t {name}(const int32_t*a,uint32_t n,const int32_t*b,uint32_t m,int32_t*out,uint32_t cap){{if(n>UINT32_MAX-m||cap<n+m||(!a&&n)||(!b&&m)||(!out&&(n||m)))return UINT32_MAX;uint32_t i=0,j=0,k=0;{cb}return k;}}',
 f'''push {{r4-r10,lr}} | ldr r4,[sp,#32] | ldr r5,[sp,#36] | adds r6,r1,r3 | bcs sm_bad | cmp r5,r6 | blo sm_bad | cmp r6,#0 | beq sm_empty | cmp r4,#0 | beq sm_bad | cmp r1,#0 | beq sm_bcheck | cmp r0,#0 | beq sm_bad
sm_bcheck: | cmp r3,#0 | beq sm_start | cmp r2,#0 | beq sm_bad
sm_start: | movs r6,#0 | movs r7,#0 | movs r8,#0
sm_loop: | {ab}
sm_accept: | {dedup}str r9,[r4,r8,lsl #2] | adds r8,#1 | b sm_loop
sm_done: | mov r0,r8 | pop {{r4-r10,pc}}
sm_empty: | movs r0,#0 | pop {{r4-r10,pc}}
sm_bad: | mvn r0,#0 | pop {{r4-r10,pc}}''',
 f'int32_t a[]={{1,2,2}},b[]={{2,3}},o[6]={{0}};o[5]=77;CHECK({name}(a,3,b,2,o,5)=={5 if mode=="merge" else 1 if mode=="intersection" else 3}&&o[0]=={2 if mode=="intersection" else 1}&&o[5]==77);CHECK({name}(a,3,b,2,o,4)==UINT32_MAX);CHECK({name}(0,0,0,0,0,0)==0);',
 complexity='O(n+m) time, O(1) auxiliary storage')
for increasing in (False,True):
 name='longest_increasing_run' if increasing else 'longest_equal_run'
 condition='a[i]>a[i-1]' if increasing else 'a[i]==a[i-1]'
 branch='ble' if increasing else 'bne'
 add(name.replace('_','-'), 'Longest '+('strictly increasing' if increasing else 'equal-value')+' contiguous run',A,
 f'uint32_t {name}(const int32_t *a, uint32_t n)',
 'Return the longest contiguous run; null or empty input returns zero. Signed comparisons apply.',
 '1. Start a one-element run.\n2. Extend while the adjacent-pair condition holds.\n3. Otherwise restart at one; retain the best length.',
 '[1,2,2,3,4]: longest increasing run=3; longest equal run=2.',
 f'uint32_t {name}(const int32_t*a,uint32_t n){{if(!a||!n)return 0;uint32_t r=1,b=1;for(uint32_t i=1;i<n;i++){{r={condition}?r+1:1;if(r>b)b=r;}}return b;}}',
 f'''cmp r0,#0 | beq lr_bad | cmp r1,#0 | beq lr_bad | push {{r4-r6,lr}} | ldr r2,[r0],#4 | movs r3,#1 | movs r4,#1 | subs r1,#1
lr_loop: | cmp r1,#0 | beq lr_done | ldr r5,[r0],#4 | cmp r5,r2 | {branch} lr_reset | adds r3,#1 | b lr_max
lr_reset: | movs r3,#1
lr_max: | cmp r3,r4 | bls lr_next | mov r4,r3
lr_next: | mov r2,r5 | subs r1,#1 | b lr_loop
lr_done: | mov r0,r4 | pop {{r4-r6,pc}}
lr_bad: | movs r0,#0 | bx lr''',
 f'int32_t a[]={{1,2,2,3,4}},b[]={{-1,-1,-1}};CHECK({name}(a,5)=={3 if increasing else 2});CHECK({name}(b,3)=={1 if increasing else 3});CHECK({name}(0,0)==0);')
add('maximum-subarray-sum','Maximum contiguous subarray sum',A,
'int64_t maximum_subarray(const int32_t *a, uint32_t n)',
'Return the maximum nonempty contiguous signed-word sum in 64 bits. Null or empty input returns zero; an all-negative array returns its largest element.',
'1. Seed current and best from the first element.\n2. Restart when the current sum is negative.\n3. Add the next value and update the best.',
'[-2,3,-1,4,-8]: current sums -2,3,2,6,-2; best 6.',
'int64_t maximum_subarray(const int32_t*a,uint32_t n){if(!a||!n)return 0;int64_t cur=a[0],best=cur;for(uint32_t i=1;i<n;i++){if(cur<0)cur=0;cur+=a[i];if(cur>best)best=cur;}return best;}',
'''cmp r0,#0 | beq ms_zero | cmp r1,#0 | beq ms_zero | push {r4-r10,lr} | ldr r4,[r0],#4 | asr r5,r4,#31 | mov r6,r4 | mov r7,r5 | subs r1,#1
ms_loop: | cmp r1,#0 | beq ms_done | cmp r5,#0 | bge ms_add | movs r4,#0 | movs r5,#0
ms_add: | ldr r8,[r0],#4 | asr r9,r8,#31 | adds r4,r4,r8 | adc r5,r5,r9 | cmp r5,r7 | bgt ms_best | blt ms_next | cmp r4,r6 | bls ms_next
ms_best: | mov r6,r4 | mov r7,r5
ms_next: | subs r1,#1 | b ms_loop
ms_done: | mov r0,r6 | mov r1,r7 | pop {r4-r10,pc}
ms_zero: | movs r0,#0 | movs r1,#0 | bx lr''',
'int32_t a[]={-2,3,-1,4,-8},b[]={-9,-2,-7},c[]={INT32_MAX,INT32_MAX};CHECK(maximum_subarray(a,5)==6);CHECK(maximum_subarray(b,3)==-2);CHECK(maximum_subarray(c,2)==4294967294LL);CHECK(maximum_subarray(0,0)==0);')
add('first-interior-peak','First strict interior peak',A,
'int32_t first_peak(const int32_t *a, uint32_t n)',
'Return the first interior index i with a[i]>a[i-1] and a[i]>a[i+1], or -1. Require n<=INT32_MAX; endpoints are not peaks.',
'1. Begin at index one.\n2. Compare both neighbors with signed comparisons.\n3. Stop before the last element.',
'[1,4,2,5,1] -> first peak index 1.',
'int32_t first_peak(const int32_t*a,uint32_t n){if(!a||n<3||n>INT32_MAX)return -1;for(uint32_t i=1;i+1<n;i++)if(a[i]>a[i-1]&&a[i]>a[i+1])return (int32_t)i;return -1;}',
'''cmp r0,#0 | beq pk_bad | cmp r1,#3 | blo pk_bad | cmp r1,#0 | bmi pk_bad | push {r4-r6,lr} | movs r2,#1 | subs r1,#1
pk_loop: | cmp r2,r1 | bhs pk_fail | sub r3,r2,#1 | ldr r4,[r0,r3,lsl #2] | ldr r5,[r0,r2,lsl #2] | cmp r5,r4 | ble pk_next | add r3,r2,#1 | ldr r6,[r0,r3,lsl #2] | cmp r5,r6 | ble pk_next | mov r0,r2 | pop {r4-r6,pc}
pk_next: | adds r2,#1 | b pk_loop
pk_fail: | pop {r4-r6,lr}
pk_bad: | mvn r0,#0 | bx lr''',
'int32_t a[]={1,4,2,5,1},b[]={1,2,2,1};CHECK(first_peak(a,5)==1);CHECK(first_peak(b,4)==-1);CHECK(first_peak(a,2)==-1);')
for mode in ('dot','hamming','squared'):
 name={'dot':'dot_i16','hamming':'array_bit_differences','squared':'squared_differences_i16'}[mode]
 typ='uint32_t' if mode=='hamming' else 'int16_t'
 ret='int64_t' if mode=='dot' else 'uint64_t'
 cb={'dot':'s+=(int64_t)a[i]*b[i];','hamming':'uint32_t x=a[i]^b[i];while(x){s++;x&=x-1;}','squared':'int64_t d=(int32_t)a[i]-b[i];s+=(uint64_t)(d*d);'}[mode]
 ab={'dot':'''ldrsh r4,[r0],#2 | ldrsh r5,[r1],#2 | smlal r6,r7,r4,r5''',
 'hamming':'''ldr r4,[r0],#4 | ldr r5,[r1],#4 | eor r4,r4,r5
wr_bits: | cmp r4,#0 | beq wr_next | sub r5,r4,#1 | and r4,r4,r5 | adds r6,#1 | adc r7,r7,#0 | b wr_bits''',
 'squared':'''ldrsh r4,[r0],#2 | ldrsh r5,[r1],#2 | sub r4,r4,r5 | smull r4,r5,r4,r4 | adds r6,r6,r4 | adc r7,r7,r5'''}[mode]
 tests={'dot':'int16_t a[]={-32768,-32768},b[]={-32768,-32768};CHECK(dot_i16(a,b,2)==2147483648LL);',
 'hamming':'uint32_t a[]={0,0xffffffffu},b[]={0xffffffffu,0};CHECK(array_bit_differences(a,b,2)==64);',
 'squared':'int16_t a[]={-32768,-32768},b[]={32767,32767};CHECK(squared_differences_i16(a,b,2)==8589672450ULL);'}[mode]
 add(name.replace('_','-'),{'dot':'Signed 16-bit dot product','hamming':'Total bit differences between word arrays','squared':'Sum of squared signed 16-bit differences'}[mode],A,
 f'{ret} {name}(const {typ} *a, const {typ} *b, uint32_t n)',
 'Return an exact 64-bit sum. Zero count or a null input pointer returns zero. Arrays each contain n elements; no outputs are mutated.',
 '1. Load corresponding elements at the declared width.\n2. Compute their contribution.\n3. Accumulate with carry into a 64-bit result.',
 {'dot':'[-32768,-32768] dot itself = 2147483648.','hamming':'[0,0xFFFFFFFF] versus [0xFFFFFFFF,0] -> 64 differing bits.','squared':'[-32768,-32768] versus [32767,32767] -> 2*65535^2=8589672450.'}[mode],
 f'{ret} {name}(const {typ}*a,const {typ}*b,uint32_t n){{{ret} s=0;if(a&&b)for(uint32_t i=0;i<n;i++){{{cb}}}return s;}}',
 f'''push {{r4-r8,lr}} | movs r6,#0 | movs r7,#0 | cmp r0,#0 | beq wr_done | cmp r1,#0 | beq wr_done
wr_loop: | cmp r2,#0 | beq wr_done | {ab}
wr_next: | subs r2,#1 | b wr_loop
wr_done: | mov r0,r6 | mov r1,r7 | pop {{r4-r8,pc}}''',
 tests+f'CHECK({name}(0,0,0)==0);')
