"""Handwritten matrix calculations and recursive binary search."""
from algorithm_catalog import add
M='Arrays and matrices'
add('matrix-row-column-sums','Matrix row and column sums',M,
'int matrix_sums(const int16_t *a, uint32_t rows, uint32_t cols, int64_t *out, uint32_t capacity)',
'For a row-major signed-halfword matrix, write rows row sums followed by cols column sums. Require dimensions 1..256, capacity>=rows+cols and disjoint output; return 0 before writes on invalid input, otherwise 1.',
'1. Sum contiguous elements for each row.\n2. Sum stride-separated elements for each column.\n3. Store each sum as a sign-extended 64-bit value.',
'[[1,2,3],[4,5,6]] -> row sums [6,15], column sums [5,7,9].',
'int matrix_sums(const int16_t*a,uint32_t r,uint32_t c,int64_t*out,uint32_t cap){if(!a||!out||!r||!c||r>256||c>256||cap<r+c)return 0;for(uint32_t i=0;i<r;i++){int32_t s=0;for(uint32_t j=0;j<c;j++)s+=a[i*c+j];out[i]=s;}for(uint32_t j=0;j<c;j++){int32_t s=0;for(uint32_t i=0;i<r;i++)s+=a[i*c+j];out[r+j]=s;}return 1;}',
'''cmp r0,#0 | beq mx_bad | cmp r3,#0 | beq mx_bad | cmp r1,#1 | blo mx_bad | cmp r2,#1 | blo mx_bad | cmp r1,#256 | bhi mx_bad | cmp r2,#256 | bhi mx_bad | ldr r12,[sp] | push {r4-r11,lr} | sub sp,sp,#4 | add r4,r1,r2 | cmp r12,r4 | blo mx_fail | mov r4,r0 | mov r5,r1 | mov r6,r2 | mov r7,r3 | movs r8,#0
mx_row: | cmp r8,r5 | bhs mx_columns | movs r9,#0 | movs r10,#0
mx_ri: | cmp r9,r6 | bhs mx_rs | mla r11,r8,r6,r9 | lsl r11,r11,#1 | ldrsh r0,[r4,r11] | add r10,r0 | adds r9,#1 | b mx_ri
mx_rs: | str r10,[r7],#4 | asr r0,r10,#31 | str r0,[r7],#4 | adds r8,#1 | b mx_row
mx_columns: | movs r8,#0
mx_col: | cmp r8,r6 | bhs mx_done | movs r9,#0 | movs r10,#0
mx_ci: | cmp r9,r5 | bhs mx_cs | mla r11,r9,r6,r8 | lsl r11,r11,#1 | ldrsh r0,[r4,r11] | add r10,r0 | adds r9,#1 | b mx_ci
mx_cs: | str r10,[r7],#4 | asr r0,r10,#31 | str r0,[r7],#4 | adds r8,#1 | b mx_col
mx_done: | movs r0,#1 | b mx_return
mx_fail: | movs r0,#0
mx_return: | add sp,sp,#4 | pop {r4-r11,pc}
mx_bad: | movs r0,#0 | bx lr''',
'int16_t a[]={1,2,3,4,5,6};int64_t o[6]={0};o[5]=77;CHECK(matrix_sums(a,2,3,o,5)&&o[0]==6&&o[1]==15&&o[2]==5&&o[4]==9&&o[5]==77);CHECK(!matrix_sums(a,2,3,o,4));CHECK(!matrix_sums(a,0,3,o,5));',
complexity='O(rows*cols) time, O(1) auxiliary space')
add('matrix-diagonal-sums','Main and secondary diagonal sums',M,
'int diagonal_sums(const int16_t *a, uint32_t n, int64_t *out, uint32_t capacity)',
'Square row-major matrix with n<=256. Write main and secondary sums into two 64-bit outputs. Empty matrix yields two zeros. Require capacity>=2 and valid output; nonempty input must be valid and disjoint.',
'1. Load a[i*n+i] for the main diagonal.\n2. Load a[i*n+n-1-i] for the secondary diagonal.\n3. Store both widened sums; each diagonal includes its own center.',
'[[1,2,3],[4,5,6],[7,8,9]] -> [15,15].',
'int diagonal_sums(const int16_t*a,uint32_t n,int64_t*out,uint32_t cap){if(!out||cap<2||n>256||(!a&&n))return 0;int32_t x=0,y=0;for(uint32_t i=0;i<n;i++){x+=a[i*n+i];y+=a[i*n+n-1-i];}out[0]=x;out[1]=y;return 1;}',
'''cmp r2,#0 | beq dg_bad | cmp r3,#2 | blo dg_bad | cmp r1,#256 | bhi dg_bad | cmp r1,#0 | beq dg_start | cmp r0,#0 | beq dg_bad
dg_start: | push {r4-r8,lr} | movs r4,#0 | movs r5,#0 | movs r6,#0
dg_loop: | cmp r6,r1 | bhs dg_done | mla r7,r6,r1,r6 | lsl r7,r7,#1 | ldrsh r8,[r0,r7] | add r4,r8 | mul r7,r6,r1 | add r7,r1 | subs r7,#1 | sub r7,r6 | lsl r7,r7,#1 | ldrsh r8,[r0,r7] | add r5,r8 | adds r6,#1 | b dg_loop
dg_done: | str r4,[r2] | asr r4,r4,#31 | str r4,[r2,#4] | str r5,[r2,#8] | asr r5,r5,#31 | str r5,[r2,#12] | movs r0,#1 | pop {r4-r8,pc}
dg_bad: | movs r0,#0 | bx lr''',
'int16_t a[]={1,2,3,4,5,6,7,8,9};int64_t o[3]={0};o[2]=77;CHECK(diagonal_sums(a,3,o,2)&&o[0]==15&&o[1]==15&&o[2]==77);CHECK(diagonal_sums(0,0,o,2)&&o[0]==0);CHECK(!diagonal_sums(a,3,o,1));',
complexity='O(n) time, O(1) space')
add('matrix-symmetry','Square-matrix symmetry test',M,
'int matrix_symmetric(const int32_t *a, uint32_t n)',
'Check a[r,c]==a[c,r] for a signed-word square matrix with n<=256. Empty matrix is symmetric; null nonempty input or oversized dimension returns 0.',
'1. Visit entries strictly above the diagonal.\n2. Compare each with its transposed partner.',
'[[1,2],[2,3]] is symmetric; changing the lower-left 2 to 4 makes it false.',
'int matrix_symmetric(const int32_t*a,uint32_t n){if(n>256||(!a&&n))return 0;for(uint32_t r=0;r<n;r++)for(uint32_t c=r+1;c<n;c++)if(a[r*n+c]!=a[c*n+r])return 0;return 1;}',
'''cmp r1,#256 | bhi sy_bad | cmp r1,#0 | beq sy_yes | cmp r0,#0 | beq sy_bad | push {r4-r8,lr} | movs r2,#0
sy_outer: | cmp r2,r1 | bhs sy_ok | add r3,r2,#1
sy_inner: | cmp r3,r1 | bhs sy_next | mla r4,r2,r1,r3 | mla r5,r3,r1,r2 | ldr r6,[r0,r4,lsl #2] | ldr r7,[r0,r5,lsl #2] | cmp r6,r7 | bne sy_fail | adds r3,#1 | b sy_inner
sy_next: | adds r2,#1 | b sy_outer
sy_ok: | pop {r4-r8,lr}
sy_yes: | movs r0,#1 | bx lr
sy_fail: | pop {r4-r8,lr}
sy_bad: | movs r0,#0 | bx lr''',
'int32_t a[]={1,2,2,3};CHECK(matrix_symmetric(a,2));a[2]=4;CHECK(!matrix_symmetric(a,2));CHECK(matrix_symmetric(0,0));CHECK(!matrix_symmetric(a,257));',
complexity='O(n squared) time, O(1) space')
add('matrix-clockwise-rotation','Clockwise square-matrix rotation',M,
'int matrix_rotate_clockwise(const int32_t *a, uint32_t n, int32_t *out, uint32_t capacity)',
'Rotate a signed-word square matrix 90 degrees clockwise into separate storage. Require n<=256 and capacity>=n*n. Empty matrix succeeds; exact aliasing is rejected, other overlap is prohibited.',
'1. Visit input row r and column c.\n2. Store at output row c, column n-1-r.',
'[[1,2],[3,4]] -> [[3,1],[4,2]].',
'int matrix_rotate_clockwise(const int32_t*a,uint32_t n,int32_t*out,uint32_t cap){if(n>256||cap<n*n||((!a||!out||a==out)&&n))return 0;for(uint32_t r=0;r<n;r++)for(uint32_t c=0;c<n;c++)out[c*n+n-1-r]=a[r*n+c];return 1;}',
'''cmp r1,#256 | bhi rt_bad | mul r12,r1,r1 | cmp r3,r12 | blo rt_bad | cmp r1,#0 | beq rt_yes | cmp r0,#0 | beq rt_bad | cmp r2,#0 | beq rt_bad | cmp r0,r2 | beq rt_bad | push {r4-r8,lr} | movs r3,#0
rt_outer: | cmp r3,r1 | bhs rt_done | movs r4,#0
rt_inner: | cmp r4,r1 | bhs rt_next | mla r5,r3,r1,r4 | mul r6,r4,r1 | add r6,r1 | subs r6,#1 | sub r6,r3 | ldr r7,[r0,r5,lsl #2] | str r7,[r2,r6,lsl #2] | adds r4,#1 | b rt_inner
rt_next: | adds r3,#1 | b rt_outer
rt_done: | pop {r4-r8,lr}
rt_yes: | movs r0,#1 | bx lr
rt_bad: | movs r0,#0 | bx lr''',
'int32_t a[]={1,2,3,4},o[5]={0};o[4]=77;CHECK(matrix_rotate_clockwise(a,2,o,4)&&o[0]==3&&o[1]==1&&o[2]==4&&o[3]==2&&o[4]==77);CHECK(!matrix_rotate_clockwise(a,2,a,4));CHECK(!matrix_rotate_clockwise(a,2,o,3));',
complexity='O(n squared) time; n*n output words')
add('integer-matrix-multiplication','Signed 16-bit integer matrix multiplication',M,
'int matrix_multiply_i16(const int16_t *a, const int16_t *b, uint32_t rows, uint32_t inner, uint32_t cols, int64_t *out, uint32_t capacity)',
'Multiply row-major A[rows,inner] by B[inner,cols]. Dimensions must be 1..256; capacity counts 64-bit output cells and must be >=rows*cols. Output is disjoint. Invalid input returns 0 before writes.',
'1. Choose output row and column.\n2. Multiply matching signed halfwords across the inner dimension.\n3. Accumulate in 64 bits and store one output cell.',
'[[1,2],[3,4]] times [[5,6],[7,8]] -> [[19,22],[43,50]].',
'int matrix_multiply_i16(const int16_t*a,const int16_t*b,uint32_t r,uint32_t k,uint32_t c,int64_t*out,uint32_t cap){if(!a||!b||!out||!r||!k||!c||r>256||k>256||c>256||cap<r*c)return 0;for(uint32_t i=0;i<r;i++)for(uint32_t j=0;j<c;j++){int64_t s=0;for(uint32_t t=0;t<k;t++)s+=(int32_t)a[i*k+t]*b[t*c+j];out[i*c+j]=s;}return 1;}',
'''push {r4-r11,lr} | sub sp,sp,#28
; Original stack arguments are now 64 bytes above SP.
ldr r4,[sp,#64] | ldr r5,[sp,#68] | ldr r6,[sp,#72] | cmp r0,#0 | beq mm_bad | cmp r1,#0 | beq mm_bad | cmp r5,#0 | beq mm_bad | cmp r2,#1 | blo mm_bad | cmp r3,#1 | blo mm_bad | cmp r4,#1 | blo mm_bad | cmp r2,#256 | bhi mm_bad | cmp r3,#256 | bhi mm_bad | cmp r4,#256 | bhi mm_bad | mul r7,r2,r4 | cmp r6,r7 | blo mm_bad
str r0,[sp] | str r1,[sp,#4] | str r2,[sp,#8] | str r3,[sp,#12] | str r4,[sp,#16] | str r5,[sp,#20] | movs r6,#0
mm_rows: | ldr r0,[sp,#8] | cmp r6,r0 | bhs mm_good | movs r7,#0
mm_cols: | ldr r0,[sp,#16] | cmp r7,r0 | bhs mm_nextrow | movs r8,#0 | movs r9,#0 | movs r10,#0
mm_inner: | ldr r0,[sp,#12] | cmp r8,r0 | bhs mm_store | mla r1,r6,r0,r8 | lsl r1,r1,#1 | ldr r2,[sp] | ldrsh r3,[r2,r1] | ldr r0,[sp,#16] | mla r1,r8,r0,r7 | lsl r1,r1,#1 | ldr r2,[sp,#4] | ldrsh r4,[r2,r1] | smlal r9,r10,r3,r4 | adds r8,#1 | b mm_inner
mm_store: | ldr r0,[sp,#20] | str r9,[r0],#4 | str r10,[r0],#4 | str r0,[sp,#20] | adds r7,#1 | b mm_cols
mm_nextrow: | adds r6,#1 | b mm_rows
mm_good: | movs r0,#1 | b mm_return
mm_bad: | movs r0,#0
mm_return: | add sp,sp,#28 | pop {r4-r11,pc}''',
'int16_t a[]={1,2,3,4},b[]={5,6,7,8};int64_t o[5]={0};o[4]=77;CHECK(matrix_multiply_i16(a,b,2,2,2,o,4)&&o[0]==19&&o[1]==22&&o[2]==43&&o[3]==50&&o[4]==77);CHECK(!matrix_multiply_i16(a,b,2,2,2,o,3));int16_t x[]={-32768,-32768};CHECK(matrix_multiply_i16(x,x,1,2,1,o,1)&&o[0]==2147483648LL);',
complexity='O(rows*inner*cols) time, O(1) auxiliary storage')
add('recursive-binary-search','Recursive binary search', 'Searching and selection',
'int32_t recursive_binary_search(const int32_t *a, uint32_t n, int32_t key)',
'Search ascending signed words, n<=INT32_MAX. Return a matching index or -1; any occurrence is allowed for duplicates. Empty or null input returns -1. At most 32 recursive frames.',
'1. Choose the middle element.\n2. Recurse on the half that can contain the key.\n3. Offset a successful right-half result back into the original array.',
'[1,3,5,7,9], key 7: middle 5 -> right half [7,9] -> 7, original index 3.',
'int32_t recursive_binary_search(const int32_t*a,uint32_t n,int32_t key){if(!a||!n||n>INT32_MAX)return -1;uint32_t m=n/2;if(a[m]==key)return (int32_t)m;if(key<a[m])return recursive_binary_search(a,m,key);int32_t p=recursive_binary_search(a+m+1,n-m-1,key);return p<0?-1:(int32_t)(m+1)+(int32_t)p;}',
'''cmp r0,#0 | beq bs_bad | cmp r1,#0 | beq bs_bad | bmi bs_bad | push {r4,lr} | lsrs r4,r1,#1 | ldr r3,[r0,r4,lsl #2] | cmp r3,r2 | beq bs_found | bgt bs_left | adds r4,#1 | add r0,r0,r4,lsl #2 | sub r1,r1,r4 | bl recursive_binary_search | cmp r0,#0 | blt bs_return | add r0,r4 | b bs_return
bs_left: | mov r1,r4 | bl recursive_binary_search | b bs_return
bs_found: | mov r0,r4
bs_return: | pop {r4,pc}
bs_bad: | mvn r0,#0 | bx lr''',
'int32_t a[]={1,3,5,7,9},b[]={INT32_MIN,0,INT32_MAX};CHECK(recursive_binary_search(a,5,7)==3);CHECK(recursive_binary_search(a,5,8)==-1);CHECK(recursive_binary_search(b,3,INT32_MIN)==0);CHECK(recursive_binary_search(b,3,INT32_MAX)==2);CHECK(recursive_binary_search(0,0,3)==-1);',
complexity='O(log n) time and O(log n) stack; eight bytes per active frame')
