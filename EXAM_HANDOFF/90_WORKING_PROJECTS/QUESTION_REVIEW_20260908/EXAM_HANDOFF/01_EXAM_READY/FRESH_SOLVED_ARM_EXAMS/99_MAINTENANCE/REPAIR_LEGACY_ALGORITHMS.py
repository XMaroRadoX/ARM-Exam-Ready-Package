"""Apply reviewed corrections to canonical legacy C/ARM sources.

Idempotent transformations are kept here so the repair scope is reviewable.
Correct existing handwritten routines are retained; missing variants are added.
"""
from pathlib import Path
import re,json,subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
LIB=ROOT/'03_ADDITIONAL_STUDY_MATERIAL'/'02 - Code Recipes'/'11 - Maximum Algorithm Reference'
CHANGED=set()
NOTES={}
def change(pid,old,new,note):
 p=LIB/pid/'c/reference.c';s=p.read_text()
 if new in s: pass
 elif old in s:
  s=s.replace(old,new);p.write_text(s);CHANGED.add(pid)
 elif new not in s:raise ValueError('Missing expected source in '+pid+': '+old[:50])
 NOTES.setdefault(pid,[]).append(note)
def replace_function(pid,name,new,note):
 p=LIB/pid/'c/reference.c';s=p.read_text()
 match=re.search(r'(?m)^(?:static\s+)?(?:[A-Za-z_]\w*[\s*]+)+'+name+r'\s*\([^;{}]*\)\s*\{',s)
 if not match:raise ValueError(name)
 depth=1;i=match.end()
 while depth:
  if s[i]=='{':depth+=1
  if s[i]=='}':depth-=1
  i+=1
 if s[match.start():i]!=new:
  s=s[:match.start()]+new+s[i:];p.write_text(s);CHANGED.add(pid)
 NOTES.setdefault(pid,[]).append(note)
def vector(pid,code):
 p=LIB/pid/'c/reference.c';s=p.read_text();mark='static int pattern_edge_vectors(void) {'
 if code not in s:s=s.replace(mark,mark+'\n  '+code);p.write_text(s)
def asm_file(pid,body):
 path=LIB/pid/'arm/implementation.s'
 if path.read_text()!=body:path.write_text(body)
def handwritten(name,body):
 lines=[]
 for line in body.splitlines():
  for part in line.split(' | '):
   part=part.strip()
   if part:lines.append(part[:-1] if part.endswith(':') else '        '+part)
 return '; Handwritten Cortex-M3 Thumb exam reference.\n        AREA |.text.patterns|, CODE, READONLY\n        THUMB\n        PRESERVE8\n        EXPORT '+name+'\n'+name+'\n'+'\n'.join(lines)+'\n        LTORG\n        ALIGN\n        END\n'
def append_routine(pid,name,body):
 p=LIB/pid/'arm/implementation.s';s=p.read_text()
 if re.search(r'EXPORT\s+'+name+r'\b',s):return
 fragment=handwritten(name,body)
 fragment=fragment[fragment.index('        EXPORT'):fragment.rindex('        LTORG')]
 s=re.sub(r'\s+END\s*$', '\n'+fragment+'\n        ALIGN\n        END\n',s)
 p.write_text(s)

replace_function('PAT-ALG-DECIMAL-DIGITS-001','pat_alg_decimal_digits_001_is_palindrome',
'''int pat_alg_decimal_digits_001_is_palindrome(uint32_t value) {
  uint32_t original=value;
  uint64_t reversed=0;
  do { reversed=reversed*10u+value%10u; value/=10u; } while(value);
  return reversed==original;
}''','Fix numeric palindrome comparison: use the full reversed value, not the 16-bit packed summary.')
vector('PAT-ALG-DECIMAL-DIGITS-001','if (!pat_alg_decimal_digits_001_is_palindrome(123321u) || !pat_alg_decimal_digits_001_is_palindrome(4000000004u) || pat_alg_decimal_digits_001_is_palindrome(UINT32_MAX)) return 0;')

change('PAT-ALG-COUNTING-SORT-001','while (count[i]--)\n      a[k++] = (uint8_t)i;',
       'while (count[i] != 0u) {\n      --count[i];\n      a[k++] = (uint8_t)i;\n    }','Do not underflow exhausted frequency counters.')
vector('PAT-ALG-COUNTING-SORT-001','uint8_t check_a[3]={2,0,2}; uint32_t check_c[3]; if(!pat_alg_counting_sort_001(check_a,3,3,check_c)||check_c[0]||check_c[1]||check_c[2]) return 0;')

# Reject invalid state before its index can access a queue/stack buffer.
for pid in ['PAT-DS-CIRCULAR-QUEUE-001','PAT-DS-RING-BUFFER-001']:
 change(pid,'if (!q || !q->b || !q->cap || !value)','if (!q || !q->b || !q->cap || !value || q->head >= q->cap || q->tail >= q->cap || q->count > q->cap)',
 'Validate head, tail and count before a buffer access.')
 typ='queue_t' if 'QUEUE' in pid else 'ring_t';fn=pid.lower().replace('-','_')
 vector(pid,f'int32_t guard_data[2]={{7,8}},guard_value=9; {typ} badq={{guard_data,2,2,0,0}}; if({fn}(&badq,1,&guard_value)||guard_data[0]!=7) return 0;')
change('PAT-DS-STACK-001','if (!a || !top || !value)','if (!a || !top || !value || *top > cap)',
 'Reject a corrupted top index for pop as well as push.')
vector('PAT-DS-STACK-001','int32_t guarded[1]={7},v_bad=9;uint32_t top_bad=2;if(pat_ds_stack_001(guarded,1,&top_bad,0,&v_bad)||v_bad!=9) return 0;')
change('PAT-DS-LINKED-LIST-001','if ((position == NULL) || (node == NULL))','if ((position == NULL) || (node == NULL) || (position == node))',
 'Reject self-insertion, which otherwise creates a cycle.')
vector('PAT-DS-LINKED-LIST-001','pat_ds_linked_list_001_node_t lone={1,NULL};if(pat_ds_linked_list_001_insert_after(&lone,&lone)||lone.next!=NULL) return 0;')

# Bound dimension arithmetic; backing storage remains a caller precondition.
change('PAT-ALG-FLOOD-FILL-001','uint32_t h = 0, t = 0, c = 0, n = rows * cols;',
       'uint32_t h = 0, t = 0, c = 0;\n  if (!cols || rows > UINT32_MAX / cols) return 0;\n  uint32_t n = rows * cols;','Reject zero columns and overflowing matrix dimensions before address arithmetic.')
for pid,old,new in [
 ('PAT-ALG-BFS-001','if (!adj || !seen || !q || start >= n)','if (!adj || !seen || !q || start >= n || n > 65535u)'),
 ('PAT-ALG-DIJKSTRA-001','if (!w || !dist || !done || start >= n)','if (!w || !dist || !done || start >= n || n > 32767u)'),
 ('PAT-ALG-RECURSIVE-DFS-001','(!a || !s || start >= n)','(!a || !s || start >= n || n > 256u)')]:
 change(pid,old,new,'Bound matrix indexing; recursive DFS additionally has an explicit 256-vertex stack-depth bound.')
change('PAT-ALG-RECURSIVE-DFS-001','if (depth > n || s[v])','if (!a || !s || v >= n || !depth || depth > n || s[v])',
 'Validate a directly called recursive helper before indexing seen.')
replace_function('PAT-ALG-DFS-STACK-001','pat_alg_dfs_stack_001',
'''uint32_t pat_alg_dfs_stack_001(const uint8_t *adj, uint32_t n, uint32_t start,
                               uint8_t *seen, uint32_t *stack) {
  uint32_t top=0,visited=0;
  if(!adj||!seen||!stack||start>=n||n>65535u||seen[start])return 0;
  seen[start]=1;stack[top++]=start;
  while(top){
    uint32_t v=stack[--top]; ++visited;
    for(uint32_t w=n;w>0;--w)if(adj[v*n+w-1]&&!seen[w-1]){
      seen[w-1]=1; stack[top++]=w-1;
    }
  }
  return visited;
}''','Mark vertices when pushed so duplicate pending entries cannot exhaust the n-element stack and drop reachable vertices.')
asm_file('PAT-ALG-DFS-STACK-001',handwritten('pat_alg_dfs_stack_001',
'''ldr r12,[sp] | cmp r0,#0 | beq df_bad | cmp r3,#0 | beq df_bad | cmp r12,#0 | beq df_bad | cmp r2,r1 | bhs df_bad | push {r4-r10,lr} | ldr r4,=65535 | cmp r1,r4 | bhi df_fail | ldrb r4,[r3,r2] | cmp r4,#0 | bne df_fail | mov r4,r0 | mov r5,r1 | mov r6,r3 | mov r7,r12 | movs r8,#1 | movs r9,#0 | str r2,[r7] | strb r8,[r6,r2]
df_outer: | cmp r8,#0 | beq df_done | subs r8,#1 | ldr r10,[r7,r8,lsl #2] | adds r9,#1 | mov r2,r5
df_neighbor: | cmp r2,#0 | beq df_outer | subs r2,#1 | mla r0,r10,r5,r2 | ldrb r1,[r4,r0] | cmp r1,#0 | beq df_neighbor | ldrb r1,[r6,r2] | cmp r1,#0 | bne df_neighbor | movs r1,#1 | strb r1,[r6,r2] | str r2,[r7,r8,lsl #2] | adds r8,#1 | b df_neighbor
df_done: | mov r0,r9 | pop {r4-r10,pc}
df_fail: | pop {r4-r10,lr}
df_bad: | movs r0,#0 | bx lr'''))
vector('PAT-ALG-DFS-STACK-001','uint8_t dense[36],seen2[6]={0};uint32_t stack2[7]={0};for(unsigned z=0;z<36;z++)dense[z]=1;stack2[6]=77;if(pat_alg_dfs_stack_001(dense,6,0,seen2,stack2)!=6||stack2[6]!=77)return 0;')

# Fix size+1 loops and missing pointer guards.
change('PAT-ALG-COIN-CHANGE-001','uint32_t i, x;\n  for','uint32_t i, x;\n  if (!dp || (!coin && n) || amount >= UINT32_MAX / 4u) return UINT32_MAX;\n  for',
 'Validate scratch and coin pointers; prevent amount+1 wrap and word-address overflow.')
change('PAT-ALG-KNAPSACK-001','uint32_t i, c;\n  for','uint32_t i, c;\n  if (!dp || ((!wt || !val) && n) || cap >= UINT32_MAX / 4u || n > 65535u) return 0;\n  for',
 'Reject invalid pointers and oversized DP dimensions; bound item-value sums to 32 bits.')
change('PAT-ALG-LIS-001','uint32_t i, j, best = 0;\n  for','uint32_t i, j, best = 0;\n  if ((!a || !dp) && n) return 0;\n  for','Guard null nonempty inputs.')
change('PAT-ALG-HISTOGRAM-MODE-001','uint32_t i, mode = 0;\n  for','uint32_t i, mode = 0;\n  if (!freq || (!a && n) || !range || range > 256u) return 0;\n  for','Validate histogram storage and byte-domain range.')
change('PAT-ALG-MOVING-AVERAGE-001','if (!w || w > n)','if (!a || !out || !w || w > n || w > INT32_MAX)',
 'Validate pointers and prevent unsigned windows from becoming a negative signed divisor.')
change('PAT-ALG-EDIT-DISTANCE-001','(current == NULL))','(current == NULL) || (current == previous) || first_length == UINT32_MAX || second_length >= UINT32_MAX/4u)',
 'Prevent increment wrap and reject aliasing scratch rows.')
change('PAT-ALG-EDIT-DISTANCE-001','(columns == 0u) || (first_length + 1u > UINT32_MAX / columns)',
 '(columns == 0u) || first_length == UINT32_MAX || (first_length + 1u > UINT32_MAX / 4u / columns)',
 'Reject wrapped row count and tables whose word offsets exceed the address range.')
for pid,needle in [('PAT-ALG-ARRAY-REVERSAL-001','  uint32_t i;'),('PAT-ALG-BUBBLE-SORT-001','  uint32_t i;'),('PAT-ALG-SELECTION-SORT-001','  uint32_t i, j, m;'),('PAT-ALG-HEAP-SORT-001','  uint32_t i;')]:
 change(pid,needle,needle+'\n  if (!a) return;','Make a null input a no-op rather than dereferencing it.')
change('PAT-ALG-HEAP-SORT-001','uint32_t m = i, l = 2 * i + 1, r = l + 1;',
 'if (!a || i >= n || i >= n/2u) return;\n    uint32_t m = i, l = 2 * i + 1, r = l + 1;','Stop heap descent at a leaf before child-index arithmetic.')
change('PAT-ALG-QUICKSORT-001','if (a && n)','if (a && n && n <= INT32_MAX)','Reject unsigned lengths not representable by the signed partition indexes.')
change('PAT-ALG-MERGE-SORT-001','if (a && scratch)','if (a && scratch && a != scratch)','Reject identical scratch and input buffers.')
change('PAT-ALG-MEMMOVE-001','if (o < i)', 'if (!d || !s) return d;\n  if ((uintptr_t)o < (uintptr_t)i)','Use integer addresses for ordering distinct objects and guard null pointers.')
change('PAT-ALG-MEMMOVE-001','else if (o > i)','else if ((uintptr_t)o > (uintptr_t)i)','Avoid relational comparison between pointers to unrelated objects.')
change('PAT-ALG-ARRAY-ROTATION-001','(scratch_count < count))','(scratch_count < count) || values == scratch)','Reject identical scratch and input buffers.')
change('PAT-ALG-ARRAY-ROTATION-001','values[(index + positions) % count]',
 'values[index >= count-positions ? index-(count-positions) : index+positions]','Avoid overflowing index+rotation before normalization.')
change('PAT-ALG-STRING-PRIMITIVES-001','(index + matched < limit)','(matched < limit - index)','Avoid overflow in substring bound checking.')
change('PAT-ALG-PREFIX-SUM-001','((values == NULL) && (count != 0u)))',
 '((values == NULL) && (count != 0u)) || count >= UINT32_MAX/8u)','Reject prefix arrays whose count+1 or byte offsets cannot be represented.')

# Preserve the legacy Horner return interface with defined modulo arithmetic.
replace_function('PAT-ALG-HORNER-001','pat_alg_horner_001',
'''int64_t pat_alg_horner_001(const int32_t *c, uint32_t n, int32_t x) {
  uint64_t y=0;
  if(!c)return 0;
  while(n)y=y*(uint64_t)(int64_t)x+(uint64_t)(int64_t)c[--n];
  if(y<=INT64_MAX)return (int64_t)y;
  return INT64_MIN+(int64_t)(y-(UINT64_C(1)<<63));
}''','Define legacy Horner wraparound explicitly, avoiding C signed-overflow undefined behavior.')
vector('PAT-ALG-HORNER-001','if(pat_alg_horner_001(NULL,3,2)!=0)return 0;')
# Existing assembly already returns this bit pattern for the exceptional quotient.
change('PAT-ALG-WIDE-DIVISION-001','return negq ? -(int64_t)q : (int64_t)q;',
 'if (q == (UINT64_C(1) << 63)) return INT64_MIN;\n  return negq ? -(int64_t)q : (int64_t)q;',
 'Avoid negating INT64_MIN in C. INT64_MIN/-1 retains the existing INT64_MIN bit-pattern result; document the overflow case.')
vector('PAT-ALG-WIDE-DIVISION-001','int32_t rem_limit=99;if(pat_alg_wide_division_001(INT64_MIN,1,&rem_limit)!=INT64_MIN||rem_limit!=0||pat_alg_wide_division_001(INT64_MIN,-1,&rem_limit)!=INT64_MIN)return 0;')

# Missing ARM variants are appended, without replacing the existing routine.
append_routine('PAT-ALG-REDUCTION-001','pat_alg_reduction_001_unsigned',
'''cmp r0,#0 | beq ur_bad | cmp r2,#0 | beq ur_bad | cmp r1,#0 | beq ur_bad | push {r4-r9} | ldr r4,[r0] | mov r5,r4 | movs r6,#0 | movs r7,#0 | movs r8,#0
ur_loop: | cmp r8,r1 | bhs ur_done | ldr r9,[r0,r8,lsl #2] | cmp r9,r4 | bhs ur_max | mov r4,r9
ur_max: | cmp r9,r5 | bls ur_sum | mov r5,r9
ur_sum: | adds r6,r6,r9 | adc r7,r7,#0 | adds r8,#1 | b ur_loop
ur_done: | str r4,[r2] | str r5,[r2,#4] | str r6,[r2,#8] | str r7,[r2,#12] | movs r0,#1 | pop {r4-r9} | bx lr
ur_bad: | movs r0,#0 | bx lr''')
NOTES.setdefault('PAT-ALG-REDUCTION-001',[]).append('Add the missing unsigned-reduction ARM export already present in C and its tests.')
replace_function('PAT-ALG-INDIRECT-RECURRENCE-001','pat_alg_indirect_recurrence_001_hofstadter_q',
'''uint32_t pat_alg_indirect_recurrence_001_hofstadter_q(uint32_t *output,uint32_t count) {
  if(!output||!count)return 0;
  output[0]=1;if(count==1)return 1;output[1]=1;
  for(uint32_t i=2;i<count;i++){
    uint32_t a=output[i-1],b=output[i-2];
    if(!a||!b||a>i||b>i)return 0;
    a=output[i-a];b=output[i-b];
    if(a>UINT32_MAX-b)return 0;
    output[i]=a+b;
  }
  return count;
}''','Validate computed Hofstadter dependency indexes and addition; supply its missing ARM entry point.')
append_routine('PAT-ALG-INDIRECT-RECURRENCE-001','pat_alg_indirect_recurrence_001_hofstadter_q',
'''cmp r0,#0 | beq hq_bad | cmp r1,#0 | beq hq_bad | movs r2,#1 | str r2,[r0] | cmp r1,#1 | beq hq_single | str r2,[r0,#4] | push {r4-r8,lr} | movs r2,#2
hq_loop: | cmp r2,r1 | bhs hq_done | sub r3,r2,#1 | ldr r4,[r0,r3,lsl #2] | subs r3,#1 | ldr r5,[r0,r3,lsl #2] | cmp r4,#0 | beq hq_fail | cmp r5,#0 | beq hq_fail | cmp r4,r2 | bhi hq_fail | cmp r5,r2 | bhi hq_fail | sub r4,r2,r4 | sub r5,r2,r5 | ldr r6,[r0,r4,lsl #2] | ldr r7,[r0,r5,lsl #2] | adds r6,r6,r7 | bcs hq_fail | str r6,[r0,r2,lsl #2] | adds r2,#1 | b hq_loop
hq_done: | mov r0,r1 | pop {r4-r8,pc}
hq_fail: | pop {r4-r8,lr}
hq_bad: | movs r0,#0 | bx lr
hq_single: | movs r0,#1 | bx lr''')

# Add the canonical object names while retaining the old assembly aliases.
p=LIB/'PAT-DATA-ASM-OBJECTS-001/arm/implementation.s';s=p.read_text()
if 'EXPORT  pat_data_asm_objects_001_magic' not in s:
 s=s.replace('pattern_initialized_words DCD','        EXPORT  pat_data_asm_objects_001_initialized_words\npat_data_asm_objects_001_initialized_words\npattern_initialized_words DCD')
 s=s.replace('pattern_workspace SPACE','        EXPORT  pat_data_asm_objects_001_workspace\npat_data_asm_objects_001_workspace\npattern_workspace SPACE')
 s=s.replace('pattern_masks   DCD','        EXPORT  pat_data_asm_objects_001_magic\npat_data_asm_objects_001_magic DCD 0x13579BDF\n        EXPORT  pat_data_asm_objects_001_masks\npat_data_asm_objects_001_masks\npattern_masks   DCD')
 p.write_text(s)
NOTES.setdefault('PAT-DATA-ASM-OBJECTS-001',[]).append('Export the canonical C data names and magic constant, preserving old aliases.')
vector('PAT-DATA-ASM-OBJECTS-001','if(pat_data_asm_objects_001_magic!=0x13579BDFu||pat_data_asm_objects_001_initialized_words[3]!=4||pat_data_asm_objects_001_masks[3]!=8)return 0;')

# Refresh only pre-existing compiler-derived listings when their C changed.
def refresh_compiled(pid):
 p=LIB/pid;target=p/'arm/implementation.s'
 if not target.read_text().startswith('; Matching'):return
 output=HERE/'.algorithm-tests'/pid/'refresh.gnu.s';output.parent.mkdir(parents=True,exist_ok=True)
 command=['C:/Program Files/LLVM/bin/clang.exe','--target=arm-none-eabi','-mcpu=cortex-m3','-mthumb','-O1','-ffreestanding','-fno-builtin','-S',str(p/'c/reference.c'),'-o',str(output)]
 subprocess.run(command,check=True,capture_output=True,text=True)
 gas=output.read_text()
 exported=re.findall(r'^\s*\.globl\s+(\w+)',gas,re.M)
 labels=set(re.findall(r'^([\w.]+):',gas,re.M))
 calls=set(re.findall(r'\bbl\s+([\w.]+)',gas))
 lines=['; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.','        AREA |.text.patterns|, CODE, READONLY','        THUMB','        PRESERVE8']
 lines+=['        EXPORT '+e for e in exported]+['        IMPORT '+e for e in sorted(calls-labels)]
 for raw in gas.splitlines():
  line=raw.split('@')[0].rstrip()
  t=line.strip()
  if not t:continue
  if t.startswith('.p2align'):lines.append('        ALIGN '+t.split()[1].split(',')[0]);continue
  if t.startswith(('.long','.word')):lines.append('        DCD '+t.split(None,1)[1]);continue
  if t.startswith('.'): 
   if t.endswith(':'):lines.append(t[:-1].replace('.','_'))
   continue
  if t.endswith(':'):lines.append(t[:-1]);continue
  lines.append('        '+t)
 result='\n'.join(lines)+'\n        ALIGN\n        END\n'
 for label in sorted(labels,key=len,reverse=True):
  if '.' in label:result=result.replace(label,label.replace('.','_'))
 target.write_text(result)
for pid in sorted(CHANGED):refresh_compiled(pid)
(HERE/'LEGACY_REPAIR_NOTES.json').write_text(json.dumps(NOTES,indent=2)+'\n')
print('Reviewed corrections in',len(NOTES),'source groups; refreshed',len(CHANGED),'C sources.')
