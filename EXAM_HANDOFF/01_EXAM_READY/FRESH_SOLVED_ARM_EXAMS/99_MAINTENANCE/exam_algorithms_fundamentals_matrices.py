"""Fundamental row-major matrix prompts with bounded dimensions."""
from algorithm_catalog import add

FAMILY='Arrays and matrices'


def entry(slug,title,prototype,contract,method,trace,c_code,asm_code,tests,
          complexity='O(rows*cols) time; O(1) auxiliary storage'):
    teaching_comment=('/* Exam prompt: '+title+'\n * Contract: '+contract+
                      '\n * Method:\n * '+method.replace('\n','\n * ')+'\n */\n')
    add(slug,title,FAMILY,prototype,contract,method,trace,teaching_comment+c_code,asm_code,tests,
        complexity=complexity,fundamentals_group='Matrices')


entry('sum-all-matrix-elements', 'Sum all matrix elements',
'int matrix_total_sum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns, int64_t *sum_out)',
'Sum a contiguous row-major int32_t matrix into int64_t. rows and columns must each be at most 256. A zero dimension produces zero and permits a null matrix pointer. Invalid input returns 0 without writing.',
'1. Validate dimensions and output.\n2. Multiply rows by columns after applying the bounds.\n3. Sign-extend and accumulate each cell.\n4. Publish the final sum.',
'For [[1,-2,3],[4,5,-6]], the running total finishes at 5.',
'''int matrix_total_sum_i32(const int32_t *matrix, uint32_t rows,
                         uint32_t columns, int64_t *sum_out) {
  if(!sum_out || rows>256 || columns>256 ||
     (!matrix && rows && columns)) return 0;
  int64_t sum=0;
  for(uint32_t i=0;i<rows*columns;++i) sum+=matrix[i];
  *sum_out=sum;
  return 1;
}''',
'''; R0=matrix,R1=rows,R2=columns,R3=sum_out. R4:R5 is the 64-bit sum.
cmp r3,#0 | beq mts_bad | cmp r1,#256 | bhi mts_bad | cmp r2,#256 | bhi mts_bad | mul r1,r1,r2 | cmp r1,#0 | beq mts_empty | cmp r0,#0 | beq mts_bad | push {r4-r7,lr} | movs r4,#0 | movs r5,#0
mts_loop: | ldr r6,[r0],#4 | asr r7,r6,#31 | adds r4,r4,r6 | adc r5,r5,r7 | subs r1,#1 | bne mts_loop | str r4,[r3] | str r5,[r3,#4] | movs r0,#1 | pop {r4-r7,pc}
mts_empty: | movs r1,#0 | str r1,[r3] | str r1,[r3,#4] | movs r0,#1 | bx lr
mts_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={1,-2,3,4,5,-6};int64_t sum=99;
CHECK(matrix_total_sum_i32(a,2,3,&sum)&&sum==5);
CHECK(matrix_total_sum_i32(0,0,3,&sum)&&sum==0);
sum=99;CHECK(!matrix_total_sum_i32(a,257,1,&sum)&&sum==99);
CHECK(!matrix_total_sum_i32(a,2,3,0));''')

entry('calculate-square-matrix-trace', 'Calculate a square matrix trace',
'int matrix_trace_i32(const int32_t *matrix, uint32_t size, int64_t *trace_out)',
'Sum the main diagonal of a contiguous square int32_t matrix. size must be at most 256. A 0x0 matrix has trace zero and may be null.',
'1. Validate size and pointers.\n2. Start at index zero.\n3. Advance by size+1 to visit each diagonal cell.\n4. Accumulate in 64 bits.',
'For [[1,2,3],[4,5,6],[7,8,9]], the diagonal 1+5+9 gives 15.',
'''int matrix_trace_i32(const int32_t *matrix, uint32_t size,
                     int64_t *trace_out) {
  if(!trace_out || size>256 || (!matrix && size)) return 0;
  int64_t trace=0;
  for(uint32_t i=0;i<size;++i) trace+=matrix[i*size+i];
  *trace_out=trace;
  return 1;
}''',
'''; R0=matrix,R1=size,R2=trace_out. R3 is the diagonal index.
cmp r2,#0 | beq mtr_bad | cmp r1,#256 | bhi mtr_bad | cmp r1,#0 | beq mtr_empty | cmp r0,#0 | beq mtr_bad | push {r4-r7,lr} | movs r3,#0 | movs r4,#0 | movs r5,#0 | add r7,r1,#1
mtr_loop: | ldr r6,[r0,r3,lsl #2] | asr r12,r6,#31 | adds r4,r4,r6 | adc r5,r5,r12 | add r3,r3,r7 | subs r1,#1 | bne mtr_loop | str r4,[r2] | str r5,[r2,#4] | movs r0,#1 | pop {r4-r7,pc}
mtr_empty: | movs r3,#0 | str r3,[r2] | str r3,[r2,#4] | movs r0,#1 | bx lr
mtr_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={1,2,3,4,5,6,7,8,9};int64_t trace=99;
CHECK(matrix_trace_i32(a,3,&trace)&&trace==15);
CHECK(matrix_trace_i32(0,0,&trace)&&trace==0);
trace=99;CHECK(!matrix_trace_i32(a,257,&trace)&&trace==99);''',
complexity='O(size) time; O(1) auxiliary storage')


def matrix_extreme(maximum):
    word='maximum' if maximum else 'minimum'
    name='matrix_maximum_i32' if maximum else 'matrix_minimum_i32'
    op='>' if maximum else '<'; skip='ble' if maximum else 'bge'
    expected=9 if maximum else -6
    entry('find-'+word+'-matrix-value','Find the '+word+' matrix value',
          f'int {name}(const int32_t *matrix, uint32_t rows, uint32_t columns, int32_t *value_out)',
          'Return the signed matrix extremum. Require dimensions 1..256 and valid pointers. Invalid or empty input returns 0 without writing.',
          '1. Validate nonempty dimensions.\n2. Seed from the first cell.\n3. Scan remaining row-major cells using signed comparisons.',
          f'For [[1,-6,3],[4,9,2]], the {word} is {expected}.',
          f'''int {name}(const int32_t *matrix, uint32_t rows,
                      uint32_t columns, int32_t *value_out) {{
  if(!matrix || !value_out || !rows || !columns || rows>256 || columns>256)
    return 0;
  uint32_t count=rows*columns; int32_t best=matrix[0];
  for(uint32_t i=1;i<count;++i) if(matrix[i]{op}best) best=matrix[i];
  *value_out=best; return 1;
}}''',
          f'''; R0=matrix,R1=rows,R2=columns,R3=value_out.
cmp r0,#0 | beq mex_bad | cmp r3,#0 | beq mex_bad | cmp r1,#1 | blo mex_bad | cmp r2,#1 | blo mex_bad | cmp r1,#256 | bhi mex_bad | cmp r2,#256 | bhi mex_bad | mul r1,r1,r2 | push {{r4,lr}} | ldr r2,[r0],#4 | subs r1,#1
mex_loop: | cmp r1,#0 | beq mex_done | ldr r4,[r0],#4 | cmp r4,r2 | {skip} mex_next | mov r2,r4
mex_next: | subs r1,#1 | b mex_loop
mex_done: | str r2,[r3] | movs r0,#1 | pop {{r4,pc}}
mex_bad: | movs r0,#0 | bx lr''',
          f'''int32_t a[]={{1,-6,3,4,9,2}},out=77;
CHECK({name}(a,2,3,&out)&&out=={expected});
out=77;CHECK(!{name}(a,0,3,&out)&&out==77);
CHECK(!{name}(a,2,3,0));''')


matrix_extreme(False)
matrix_extreme(True)

entry('find-first-matching-matrix-coordinate',
      'Find the first matching matrix coordinate',
'''int matrix_find_first_i32(const int32_t *matrix, uint32_t rows,
                          uint32_t columns, int32_t target,
                          uint32_t *row_out, uint32_t *column_out)''',
'Find the first row-major cell equal to target. Require dimensions 1..256 and distinct valid output pointers. Failure or invalid input leaves both outputs unchanged.',
'1. Validate every pointer and dimension.\n2. Scan flat indexes from zero.\n3. Divide the first matching index by columns to recover row and remainder column.',
'In [[4,7,4],[2,4,9]], target 4 first appears at row 0, column 0.',
'''int matrix_find_first_i32(const int32_t *matrix, uint32_t rows,
                          uint32_t columns, int32_t target,
                          uint32_t *row_out, uint32_t *column_out) {
  if(!matrix || !row_out || !column_out || row_out==column_out ||
     !rows || !columns || rows>256 || columns>256) return 0;
  uint32_t count=rows*columns;
  for(uint32_t i=0;i<count;++i) if(matrix[i]==target) {
    *row_out=i/columns; *column_out=i%columns; return 1;
  }
  return 0;
}''',
'''; R0=matrix,R1=rows,R2=columns,R3=target. row_out and column_out are on entry stack.
ldr r12,[sp] | cmp r12,#0 | beq mff_bad | push {r4-r8,lr} | ldr r4,[sp,#28] | cmp r0,#0 | beq mff_fail | cmp r4,#0 | beq mff_fail | cmp r12,r4 | beq mff_fail | cmp r1,#1 | blo mff_fail | cmp r2,#1 | blo mff_fail | cmp r1,#256 | bhi mff_fail | cmp r2,#256 | bhi mff_fail | mul r5,r1,r2 | movs r6,#0
mff_loop: | cmp r6,r5 | bhs mff_fail | ldr r7,[r0,r6,lsl #2] | cmp r7,r3 | beq mff_found | adds r6,#1 | b mff_loop
mff_found: | udiv r7,r6,r2 | mls r8,r7,r2,r6 | str r7,[r12] | str r8,[r4] | movs r0,#1 | pop {r4-r8,pc}
mff_fail: | movs r0,#0 | pop {r4-r8,pc}
mff_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={4,7,4,2,4,9};uint32_t row=99,column=99;
CHECK(matrix_find_first_i32(a,2,3,4,&row,&column)&&row==0&&column==0);
row=99;column=99;CHECK(!matrix_find_first_i32(a,2,3,8,&row,&column)&&row==99&&column==99);
CHECK(!matrix_find_first_i32(a,2,3,4,&row,&row));''')

entry('count-matching-matrix-elements', 'Count matching matrix elements',
'uint32_t matrix_count_matches_i32(const int32_t *matrix, uint32_t rows, uint32_t columns, int32_t target)',
'Count cells equal to target in a matrix with dimensions at most 256. A zero dimension returns zero and permits a null matrix pointer. Other invalid input returns zero.',
'1. Validate dimensions.\n2. Convert dimensions to a bounded flat count.\n3. Scan and increment for exact signed equality.',
'In [[4,7,4],[2,4,9]], target 4 occurs three times.',
'''uint32_t matrix_count_matches_i32(const int32_t *matrix, uint32_t rows,
                                  uint32_t columns, int32_t target) {
  if(rows>256 || columns>256 || (!matrix && rows && columns)) return 0;
  uint32_t matches=0;
  for(uint32_t i=0;i<rows*columns;++i) if(matrix[i]==target) ++matches;
  return matches;
}''',
'''; R0=matrix,R1=rows,R2=columns,R3=target. R4 is match count.
cmp r1,#256 | bhi mcm_zero | cmp r2,#256 | bhi mcm_zero | mul r1,r1,r2 | cmp r1,#0 | beq mcm_zero | cmp r0,#0 | beq mcm_zero | push {r4,r5} | movs r4,#0
mcm_loop: | ldr r5,[r0],#4 | cmp r5,r3 | bne mcm_next | adds r4,#1
mcm_next: | subs r1,#1 | bne mcm_loop | mov r0,r4 | pop {r4,r5} | bx lr
mcm_zero: | movs r0,#0 | bx lr''',
'''int32_t a[]={4,7,4,2,4,9};CHECK(matrix_count_matches_i32(a,2,3,4)==3);
CHECK(matrix_count_matches_i32(a,2,3,8)==0);
CHECK(matrix_count_matches_i32(0,0,3,4)==0);
CHECK(matrix_count_matches_i32(a,257,1,4)==0);''')


def selected_extreme(axis,maximum):
    word='maximum' if maximum else 'minimum'
    name=f'matrix_{axis}_{word}_i32'
    title=f'Find the {word} value in a selected {axis}'
    index_name=axis+'_index'
    op='>' if maximum else '<'; skip='ble' if maximum else 'bge'
    if axis=='row':
        c_loop='''uint32_t base=row_index*columns; int32_t best=matrix[base];
  for(uint32_t column=1;column<columns;++column)
    if(matrix[base+column] OP best) best=matrix[base+column];'''.replace('OP',op)
        asm_setup='mul r1,r4,r2 | add r0,r0,r1,lsl #2 | mov r1,r2'
        limit='row_index>=rows'
        sample_index=1; expected=9 if maximum else 2
    else:
        c_loop='''int32_t best=matrix[column_index];
  for(uint32_t row=1;row<rows;++row)
    if(matrix[row*columns+column_index] OP best)
      best=matrix[row*columns+column_index];'''.replace('OP',op)
        asm_setup='add r0,r0,r4,lsl #2 | mov r1,r1 | lsl r2,r2,#2'
        limit='column_index>=columns'
        sample_index=1; expected=9 if maximum else -6
    entry(f'find-{word}-selected-{axis}',title,
          f'''int {name}(const int32_t *matrix, uint32_t rows,
                       uint32_t columns, uint32_t {index_name},
                       int32_t *value_out)''',
          f'Return the signed {word} in one {axis}. Require dimensions 1..256, a valid selected index, and valid pointers. Invalid input writes nothing.',
          f'1. Validate the selected {axis}.\n2. Seed from its first cell.\n3. Advance with the correct contiguous or strided access.\n4. Store the final candidate.',
          f'For [[1,-6,3],[4,9,2]], selected {axis} {sample_index} has {word} {expected}.',
          f'''int {name}(const int32_t *matrix, uint32_t rows,
                       uint32_t columns, uint32_t {index_name},
                       int32_t *value_out) {{
  if(!matrix || !value_out || !rows || !columns || rows>256 || columns>256 ||
     {limit}) return 0;
  {c_loop}
  *value_out=best; return 1;
}}''',
          f'''; R0=matrix,R1=rows,R2=columns,R3=selected index; value_out is at entry SP.
ldr r12,[sp] | cmp r0,#0 | beq mse_bad | cmp r12,#0 | beq mse_bad | cmp r1,#1 | blo mse_bad | cmp r2,#1 | blo mse_bad | cmp r1,#256 | bhi mse_bad | cmp r2,#256 | bhi mse_bad | cmp r3,{'r1' if axis=='row' else 'r2'} | bhs mse_bad | push {{r4-r6,lr}} | mov r4,r3 | {asm_setup} | ldr r3,[r0] | subs r1,#1
mse_loop: | cmp r1,#0 | beq mse_done | {'add r0,r0,#4' if axis=='row' else 'add r0,r0,r2'} | ldr r5,[r0] | cmp r5,r3 | {skip} mse_next | mov r3,r5
mse_next: | subs r1,#1 | b mse_loop
mse_done: | str r3,[r12] | movs r0,#1 | pop {{r4-r6,pc}}
mse_bad: | movs r0,#0 | bx lr''',
          f'''int32_t a[]={{1,-6,3,4,9,2}},out=77;
CHECK({name}(a,2,3,{sample_index},&out)&&out=={expected});
out=77;CHECK(!{name}(a,2,3,3,&out)&&out==77);
CHECK(!{name}(a,2,3,0,0));''',
          complexity=('O(columns) time; O(1) storage' if axis=='row' else
                      'O(rows) time; O(1) storage'))


for axis in ('row','column'):
    for maximum in (False,True):
        selected_extreme(axis,maximum)


def matrix_binary(subtract):
    name='matrix_subtract_i32' if subtract else 'matrix_add_i32'
    title=('Subtract two matrices with overflow detection' if subtract else
           'Add two matrices with overflow detection')
    op='-' if subtract else '+'; instruction='subs' if subtract else 'adds'
    expected='-4,-4,-4,-4' if subtract else '6,8,10,12'
    entry(('subtract-two-matrices-with-overflow' if subtract else
           'add-two-matrices-with-overflow'),title,
          f'''int {name}(const int32_t *left, const int32_t *right,
                      uint32_t rows, uint32_t columns,
                      int32_t *output, uint32_t capacity)''',
          'Perform elementwise signed int32_t arithmetic. Require dimensions at most 256, enough disjoint output storage, and no cell overflow. A complete preflight guarantees failure performs no writes.',
          '1. Validate dimensions, capacity, and pointers.\n2. Preflight every cell using widened arithmetic.\n3. Repeat the scan and store only after all cells are safe.',
          f'Using [1,2,3,4] and [5,6,7,8] produces [{expected}].',
          f'''int {name}(const int32_t *left, const int32_t *right,
                      uint32_t rows, uint32_t columns,
                      int32_t *output, uint32_t capacity) {{
  if(rows>256 || columns>256) return 0;
  uint32_t count=rows*columns;
  if(capacity<count || ((!left||!right||!output)&&count)) return 0;
  for(uint32_t i=0;i<count;++i) {{
    int64_t wide=(int64_t)left[i]{op}right[i];
    if(wide<INT32_MIN || wide>INT32_MAX) return 0;
  }}
  for(uint32_t i=0;i<count;++i) output[i]=left[i]{op}right[i];
  return 1;
}}''',
          f'''; R0=left,R1=right,R2=rows,R3=columns. output and capacity are on entry stack.
ldr r12,[sp] | push {{r4-r9,lr}} | sub sp,sp,#4 | ldr r4,[sp,#36] | cmp r2,#256 | bhi mbo_fail | cmp r3,#256 | bhi mbo_fail | mul r5,r2,r3 | cmp r4,r5 | blo mbo_fail | cmp r5,#0 | beq mbo_yes | cmp r0,#0 | beq mbo_fail | cmp r1,#0 | beq mbo_fail | cmp r12,#0 | beq mbo_fail | movs r6,#0
mbo_check: | cmp r6,r5 | bhs mbo_write_start | ldr r7,[r0,r6,lsl #2] | ldr r8,[r1,r6,lsl #2] | {instruction} r9,r7,r8 | bvs mbo_fail | adds r6,#1 | b mbo_check
mbo_write_start: | movs r6,#0
mbo_write: | cmp r6,r5 | bhs mbo_yes | ldr r7,[r0,r6,lsl #2] | ldr r8,[r1,r6,lsl #2] | {instruction} r9,r7,r8 | str r9,[r12,r6,lsl #2] | adds r6,#1 | b mbo_write
mbo_yes: | movs r0,#1 | b mbo_return
mbo_fail: | movs r0,#0
mbo_return: | add sp,sp,#4 | pop {{r4-r9,pc}}''',
          f'''int32_t a[]={{1,2,3,4}},b[]={{5,6,7,8}},o[5]={{0}};o[4]=77;
CHECK({name}(a,b,2,2,o,4));CHECK(o[0]=={expected.split(',')[0]}&&o[3]=={expected.split(',')[-1]}&&o[4]==77);
int32_t x[]={{INT32_MAX}},y[]={{{'-1' if subtract else '1'}}};o[0]=99;
CHECK(!{name}(x,y,1,1,o,1)&&o[0]==99);
CHECK(!{name}(a,b,2,2,o,3));''')


matrix_binary(False)
matrix_binary(True)

entry('multiply-matrix-by-scalar-with-overflow',
      'Multiply a matrix by a scalar with overflow detection',
'''int matrix_scalar_multiply_i32(const int32_t *matrix, uint32_t rows,
                               uint32_t columns, int32_t scalar,
                               int32_t *output, uint32_t capacity)''',
'Multiply every cell by scalar in signed int32_t. Require dimensions at most 256, enough disjoint output, and no overflow. A full preflight prevents partial writes.',
'1. Validate dimensions and storage.\n2. Use a signed 64-bit product to preflight each cell.\n3. Repeat and store after every product is known safe.',
'Multiplying [1,-2,3,4] by -3 produces [-3,6,-9,-12].',
'''int matrix_scalar_multiply_i32(const int32_t *matrix, uint32_t rows,
                               uint32_t columns, int32_t scalar,
                               int32_t *output, uint32_t capacity) {
  if(rows>256 || columns>256) return 0;
  uint32_t count=rows*columns;
  if(capacity<count || ((!matrix||!output)&&count)) return 0;
  for(uint32_t i=0;i<count;++i) {
    int64_t wide=(int64_t)matrix[i]*scalar;
    if(wide<INT32_MIN || wide>INT32_MAX) return 0;
  }
  for(uint32_t i=0;i<count;++i) output[i]=matrix[i]*scalar;
  return 1;
}''',
'''; R0=matrix,R1=rows,R2=columns,R3=scalar. output and capacity are on entry stack.
ldr r12,[sp] | push {r4-r9,lr} | sub sp,sp,#4 | ldr r4,[sp,#36] | cmp r1,#256 | bhi msm_fail | cmp r2,#256 | bhi msm_fail | mul r5,r1,r2 | cmp r4,r5 | blo msm_fail | cmp r5,#0 | beq msm_yes | cmp r0,#0 | beq msm_fail | cmp r12,#0 | beq msm_fail | movs r6,#0
msm_check: | cmp r6,r5 | bhs msm_write_start | ldr r7,[r0,r6,lsl #2] | smull r8,r9,r7,r3 | asr r7,r8,#31 | cmp r9,r7 | bne msm_fail | adds r6,#1 | b msm_check
msm_write_start: | movs r6,#0
msm_write: | cmp r6,r5 | bhs msm_yes | ldr r7,[r0,r6,lsl #2] | mul r7,r3,r7 | str r7,[r12,r6,lsl #2] | adds r6,#1 | b msm_write
msm_yes: | movs r0,#1 | b msm_return
msm_fail: | movs r0,#0
msm_return: | add sp,sp,#4 | pop {r4-r9,pc}''',
'''int32_t a[]={1,-2,3,4},o[5]={0};o[4]=77;
CHECK(matrix_scalar_multiply_i32(a,2,2,-3,o,4));
CHECK(o[0]==-3&&o[1]==6&&o[2]==-9&&o[3]==-12&&o[4]==77);
int32_t x[]={INT32_MAX};o[0]=99;
CHECK(!matrix_scalar_multiply_i32(x,1,1,2,o,1)&&o[0]==99);
CHECK(!matrix_scalar_multiply_i32(a,2,2,2,o,3));''')

entry('test-identity-matrix', 'Test whether a matrix is an identity matrix',
'int matrix_is_identity_i32(const int32_t *matrix, uint32_t size)',
'Return 1 when diagonal cells are one and every other cell is zero. size must be at most 256. The empty 0x0 matrix is accepted; a null nonempty matrix is invalid and returns 0.',
'1. Visit every row and column.\n2. Expect one when row equals column.\n3. Expect zero everywhere else.',
'[[1,0,0],[0,1,0],[0,0,1]] passes; changing any off-diagonal zero fails.',
'''int matrix_is_identity_i32(const int32_t *matrix, uint32_t size) {
  if(size>256 || (!matrix&&size)) return 0;
  for(uint32_t row=0;row<size;++row)
    for(uint32_t column=0;column<size;++column)
      if(matrix[row*size+column] != (row==column ? 1 : 0)) return 0;
  return 1;
}''',
'''; R0=matrix,R1=size. R2=row,R3=column,R4=expected value.
cmp r1,#256 | bhi mid_no | cmp r1,#0 | beq mid_yes | cmp r0,#0 | beq mid_no | push {r4-r6,lr} | movs r2,#0
mid_row: | cmp r2,r1 | bhs mid_done | movs r3,#0
mid_column: | cmp r3,r1 | bhs mid_next_row | movs r4,#0 | cmp r2,r3 | bne mid_load | movs r4,#1
mid_load: | mla r5,r2,r1,r3 | ldr r6,[r0,r5,lsl #2] | cmp r6,r4 | bne mid_fail | adds r3,#1 | b mid_column
mid_next_row: | adds r2,#1 | b mid_row
mid_done: | pop {r4-r6,lr}
mid_yes: | movs r0,#1 | bx lr
mid_fail: | pop {r4-r6,lr}
mid_no: | movs r0,#0 | bx lr''',
'''int32_t a[]={1,0,0,0,1,0,0,0,1};CHECK(matrix_is_identity_i32(a,3));
a[1]=2;CHECK(!matrix_is_identity_i32(a,3));
CHECK(matrix_is_identity_i32(0,0));CHECK(!matrix_is_identity_i32(a,257));''',
complexity='O(size squared) time; O(1) storage')


def triangular(upper):
    name='matrix_is_upper_triangular_i32' if upper else 'matrix_is_lower_triangular_i32'
    title='Test whether a matrix is '+('upper' if upper else 'lower')+' triangular'
    condition='row>column' if upper else 'column>row'
    asm_skip=('cmp r2,r3 | bls mtt_next' if upper else 'cmp r3,r2 | bls mtt_next')
    example=('[[1,2,3],[0,4,5],[0,0,6]] is upper triangular.' if upper else
             '[[1,0,0],[2,3,0],[4,5,6]] is lower triangular.')
    entry('test-'+('upper' if upper else 'lower')+'-triangular-matrix',title,
          f'int {name}(const int32_t *matrix, uint32_t size)',
          'Return 1 when every cell on the forbidden side of the main diagonal is zero. size must be at most 256. The empty matrix passes; null nonempty input fails.',
          '1. Visit every row and column.\n2. Skip the diagonal and allowed side.\n3. Reject a nonzero cell on the forbidden side.',
          example,
          f'''int {name}(const int32_t *matrix, uint32_t size) {{
  if(size>256 || (!matrix&&size)) return 0;
  for(uint32_t row=0;row<size;++row)
    for(uint32_t column=0;column<size;++column)
      if({condition} && matrix[row*size+column]!=0) return 0;
  return 1;
}}''',
          f'''; R0=matrix,R1=size. R2=row,R3=column.
cmp r1,#256 | bhi mtt_no | cmp r1,#0 | beq mtt_yes | cmp r0,#0 | beq mtt_no | push {{r4,r5}} | movs r2,#0
mtt_row: | cmp r2,r1 | bhs mtt_done | movs r3,#0
mtt_column: | cmp r3,r1 | bhs mtt_next_row | {asm_skip} | mla r4,r2,r1,r3 | ldr r5,[r0,r4,lsl #2] | cmp r5,#0 | bne mtt_fail
mtt_next: | adds r3,#1 | b mtt_column
mtt_next_row: | adds r2,#1 | b mtt_row
mtt_done: | pop {{r4,r5}}
mtt_yes: | movs r0,#1 | bx lr
mtt_fail: | pop {{r4,r5}}
mtt_no: | movs r0,#0 | bx lr''',
          f'''int32_t a[]={{{'1,2,3,0,4,5,0,0,6' if upper else '1,0,0,2,3,0,4,5,6'}}};
CHECK({name}(a,3));a[{6 if upper else 2}]=9;CHECK(!{name}(a,3));
CHECK({name}(0,0));CHECK(!{name}(a,257));''',
          complexity='O(size squared) time; O(1) storage')


triangular(True)
triangular(False)

entry('calculate-matrix-border-sum', 'Calculate a matrix border sum',
'int matrix_border_sum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns, int64_t *sum_out)',
'Sum cells in the first or last row or column exactly once. Dimensions must be at most 256. A zero dimension returns zero and permits a null matrix.',
'1. Handle empty, one-row, and one-column shapes.\n2. Sum top and bottom rows.\n3. For middle rows, add only first and last cells.',
'For [[1,2,3],[4,5,6],[7,8,9]], the border sum is 40; center 5 is excluded.',
'''int matrix_border_sum_i32(const int32_t *matrix, uint32_t rows,
                          uint32_t columns, int64_t *sum_out) {
  if(!sum_out || rows>256 || columns>256 || (!matrix&&rows&&columns)) return 0;
  int64_t sum=0;
  for(uint32_t row=0;row<rows;++row)
    for(uint32_t column=0;column<columns;++column)
      if(row==0 || row+1==rows || column==0 || column+1==columns)
        sum+=matrix[row*columns+column];
  *sum_out=sum; return 1;
}''',
'''; R0=matrix,R1=rows,R2=columns,R3=sum_out. Visit row-major and test border coordinates.
cmp r3,#0 | beq mbs_bad | cmp r1,#256 | bhi mbs_bad | cmp r2,#256 | bhi mbs_bad | cmp r1,#0 | beq mbs_empty | cmp r2,#0 | beq mbs_empty | cmp r0,#0 | beq mbs_bad | push {r4-r10,lr} | mov r4,r1 | mov r5,r2 | movs r6,#0 | movs r7,#0 | movs r8,#0
mbs_row: | cmp r8,r4 | bhs mbs_done | movs r9,#0
mbs_column: | cmp r9,r5 | bhs mbs_next_row | cmp r8,#0 | beq mbs_add | add r10,r8,#1 | cmp r10,r4 | beq mbs_add | cmp r9,#0 | beq mbs_add | add r10,r9,#1 | cmp r10,r5 | bne mbs_next
mbs_add: | mla r10,r8,r5,r9 | ldr r1,[r0,r10,lsl #2] | asr r2,r1,#31 | adds r6,r6,r1 | adc r7,r7,r2
mbs_next: | adds r9,#1 | b mbs_column
mbs_next_row: | adds r8,#1 | b mbs_row
mbs_done: | str r6,[r3] | str r7,[r3,#4] | movs r0,#1 | pop {r4-r10,pc}
mbs_empty: | movs r1,#0 | str r1,[r3] | str r1,[r3,#4] | movs r0,#1 | bx lr
mbs_bad: | movs r0,#0 | bx lr''',
'''int32_t a[]={1,2,3,4,5,6,7,8,9},row[]={1,2,3},column[]={1,2,3};int64_t sum=99;
CHECK(matrix_border_sum_i32(a,3,3,&sum)&&sum==40);
CHECK(matrix_border_sum_i32(row,1,3,&sum)&&sum==6);
CHECK(matrix_border_sum_i32(column,3,1,&sum)&&sum==6);
CHECK(matrix_border_sum_i32(0,0,3,&sum)&&sum==0);''')


def swap_axis(rows_axis):
    axis='rows' if rows_axis else 'columns'
    name='matrix_swap_rows_i32' if rows_axis else 'matrix_swap_columns_i32'
    title='Swap two matrix '+axis
    limit='rows' if rows_axis else 'columns'
    if rows_axis:
        c_body='''for(uint32_t column=0;column<columns;++column) {
    uint32_t a=first*columns+column, b=second*columns+column;
    int32_t temporary=matrix[a];matrix[a]=matrix[b];matrix[b]=temporary;
  }'''
        asm='''mul r5,r3,r2 | mul r6,r4,r2 | movs r1,#0
msa_loop: | cmp r1,r2 | bhs msa_done | add r7,r5,r1 | add r8,r6,r1 | ldr r9,[r0,r7,lsl #2] | ldr r10,[r0,r8,lsl #2] | str r10,[r0,r7,lsl #2] | str r9,[r0,r8,lsl #2] | adds r1,#1 | b msa_loop'''
        expected='4&&a[1]==5&&a[2]==6&&a[3]==1'
    else:
        c_body='''for(uint32_t row=0;row<rows;++row) {
    uint32_t a=row*columns+first, b=row*columns+second;
    int32_t temporary=matrix[a];matrix[a]=matrix[b];matrix[b]=temporary;
  }'''
        asm='''movs r5,#0
msa_loop: | cmp r5,r1 | bhs msa_done | mla r6,r5,r2,r3 | mla r7,r5,r2,r4 | ldr r8,[r0,r6,lsl #2] | ldr r9,[r0,r7,lsl #2] | str r9,[r0,r6,lsl #2] | str r8,[r0,r7,lsl #2] | adds r5,#1 | b msa_loop'''
        expected='3&&a[1]==2&&a[2]==1&&a[3]==6'
    entry('swap-two-matrix-'+axis,title,
          f'''int {name}(int32_t *matrix, uint32_t rows, uint32_t columns,
                      uint32_t first, uint32_t second)''',
          f'Swap two complete {axis}. Require dimensions 1..256 and both indexes below {limit}. Equal indexes are a successful no-op. Invalid input writes nothing.',
          f'1. Validate dimensions and both {axis} indexes.\n2. Visit each affected cell pair.\n3. Load both values before storing the swap.',
          ('Swapping rows 0 and 1 of [[1,2,3],[4,5,6]] produces [[4,5,6],[1,2,3]].'
           if rows_axis else
           'Swapping columns 0 and 2 of [[1,2,3],[4,5,6]] produces [[3,2,1],[6,5,4]].'),
          f'''int {name}(int32_t *matrix, uint32_t rows, uint32_t columns,
                      uint32_t first, uint32_t second) {{
  if(!matrix || !rows || !columns || rows>256 || columns>256 ||
     first>={limit} || second>={limit}) return 0;
  {c_body}
  return 1;
}}''',
          f'''; R0=matrix,R1=rows,R2=columns,R3=first; second is at entry SP.
ldr r12,[sp] | cmp r0,#0 | beq msa_bad | cmp r1,#1 | blo msa_bad | cmp r2,#1 | blo msa_bad | cmp r1,#256 | bhi msa_bad | cmp r2,#256 | bhi msa_bad | cmp r3,{'r1' if rows_axis else 'r2'} | bhs msa_bad | cmp r12,{'r1' if rows_axis else 'r2'} | bhs msa_bad | push {{r4-r10,lr}} | mov r4,r12 | {asm}
msa_done: | movs r0,#1 | pop {{r4-r10,pc}}
msa_bad: | movs r0,#0 | bx lr''',
          f'''int32_t a[]={{1,2,3,4,5,6}};CHECK({name}(a,2,3,0,{1 if rows_axis else 2}));
CHECK(a[0]=={expected}&&a[5]=={3 if rows_axis else 4});
int32_t before=a[0];CHECK(!{name}(a,2,3,0,3)&&a[0]==before);''',
          complexity=('O(columns) time; O(1) storage' if rows_axis else
                      'O(rows) time; O(1) storage'))


swap_axis(True)
swap_axis(False)
