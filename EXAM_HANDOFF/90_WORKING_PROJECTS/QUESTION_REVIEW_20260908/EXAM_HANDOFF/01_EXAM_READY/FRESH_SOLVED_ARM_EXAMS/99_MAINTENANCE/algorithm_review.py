"""Reviewed behavior of each unique pre-existing algorithm source."""
from pathlib import Path
import re
from legacy_algorithm_tests import declarations
# Contracts describe actual accepted inputs and outcomes, not generic promises.
REVIEWS = {
'ARRAY-REVERSAL':('Reverse n signed words in place; null input is a no-op.','[1,2,3,4] -> [4,2,3,1] -> [4,3,2,1].'),
'ARRAY-ROTATION':('Normalize rotation modulo count. Left/right variants mutate in place; scratch rotation requires disjoint scratch_count>=count.','[1,2,3,4], left 1 -> [2,3,4,1]; right 1 -> [4,1,2,3].'),
'BFS':('Byte adjacency matrix with n<=65535; seen is caller-initialized and queue holds n words. Mark on enqueue. Return visited count; zero on invalid input.','0 connects to 1 and 2: queue starts [0], then [1,2]; visit count 3.'),
'BINARY-SEARCH':('Ascending signed words. Primary returns lower-bound index in [0,count]; exact returns first matching index or -1. Exact-index results require count<=INT32_MAX.','[1,2,2,4], key 2: lower bound=1, exact index=1.'),
'BITFIELD':('Insert/extract only fields fitting within 32 bits. Invalid insertion leaves the word unchanged; invalid extraction returns zero. Packing combines two unsigned halfwords.','Insert value 3 into a zero word at shift 4,width 2 -> 0x30.'),
'BUBBLE-SORT':('Stable ascending signed-word sorting in place. Stop early when a pass makes no swaps; null input is a no-op.','[3,2,1] -> [2,1,3] -> [1,2,3].'),
'CHECKSUM-CRC':('Primary packs XOR checksum in bits 16..23 and additive checksum modulo 65536 in bits 0..15. CRC variant requires a caller-supplied reflected 256-word table.','Bytes [1,2,3] have XOR 0 and sum 6; packed result 6.'),
'COIN-CHANGE':('Caller provides amount+1 DP words. Return the minimum number of reusable coins or UINT32_MAX if unreachable/invalid; amount must fit the guarded word address range. Zero-value coins do not improve a state.','Coins [1,3,4], amount 6: minimum 2 using 3+3.'),
'COMPONENT-MERGE':('Five arguments: labels,count,from,to,limit. Replace matching labels if count<=limit; return number of matches. This is a helper for component merging, not the full seven-argument maze exam.','[1,2,1], from 1,to 3 -> [3,2,3], return 2.'),
'CONSUME-ONCE-MATCH':('At most 32 bytes per guess/secret. Return exact-position matches and write misplaced matches through cows. Consume duplicate occurrences once.','Secret [1,1], guess [1,2]: one bull, zero cows.'),
'COUNTING-SORT':('Unsigned bytes, range<=256, caller count array has range words. Reject an out-of-range value before output sorting. Scratch frequencies are consumed to zero.','[2,0,2], range 3 -> [0,2,2]; counters finish [0,0,0].'),
'DECIMAL-DIGITS':('Primary packs digit sum and the low 16 bits of decimal reversal; it is not a full reversal API. The palindrome variant compares a full widened reversal. Extraction writes least-significant digits first and may leave a prefix on insufficient capacity. Legacy reconstruction wraps modulo 2^32; digits must be 0..9. Kaprekar operates on the low four decimal digits.','123321 reverses to 123321, so palindrome=true; it must not be compared with only 57785.'),
'DFS-STACK':('Byte adjacency matrix, n<=65535, zero-initialized seen and n-word stack. Mark on push, so each vertex is pending at most once. Return newly visited count; an already-seen start returns zero.','A complete six-vertex graph visits six vertices without requiring more than six stack entries.'),
'DIJKSTRA':('Nonnegative unsigned matrix weights; zero means no edge. n<=32767; dist and done hold n elements. UINT32_MAX is reserved for unreachable/unrepresentable distances. Checked addition prevents wrapping a path into a smaller one.','Edges 0->1=2,1->2=3,0->2=9 yield distances [0,2,5].'),
'EDIT-DISTANCE':('Explicit string lengths. Two-row version needs separate arrays of second_length+1 words; full version checks table_elements. Return edit count, or UINT32_MAX on rejected input/dimensions.','"cat" to "cut": one substitution, distance 1.'),
'FAST-POWER':('Primary computes exponentiation by squaring; nonzero modulus gives modular arithmetic, modulus zero gives modulo-2^32 arithmetic. Checked variant returns status and leaves output unchanged on overflow.','3^5=243; modulo 7 gives 5.'),
'FLOOD-FILL':('Four-neighbor byte grid, dimensions must multiply without overflow. Queue has rows*cols words; old and new colors must differ. Mark cells before enqueue and return recolored count.','An all-zero 2x2 grid filled from cell zero changes four cells.'),
'GCD-LCM':('Euclidean GCD; gcd(0,0)=0. Checked LCM divides first, then checks multiplication; zero operands produce zero successfully.','gcd(12,18)=6; lcm=12/6*18=36.'),
'HEAP-SORT':('Ascending signed-word heap sort, in place and unstable. Null input is a no-op. Heap descent stops at leaves before calculating children.','[3,1,2]: max heap has root 3; repeated extraction produces [1,2,3].'),
'HISTOGRAM-MODE':('Unsigned-byte values, range=1..256, and range frequency words. Ignore values outside the chosen range. Ties select the smallest value; empty valid input returns zero.','[2,1,2,1] -> tied frequencies; choose mode 1.'),
'HORNER':('Coefficients are stored from constant term upward. Legacy result uses defined 64-bit two-complement wraparound; null input returns zero. The checked variant returns status, rejects intermediate overflow and leaves output unchanged on failure.','Coefficients [1,2,3], x=2: ((3*2)+2)*2+1=17.'),
'INDIRECT-RECURRENCE':('Primary generates Recaman terms beginning 0, using a subtraction only if nonnegative and unused; fallback addition overflow returns zero with a partial prefix. Hofstadter Q begins 1,1; its computed predecessor indexes and addition are checked. A failed Q generation may leave a prefix.','Recaman: 0,1,3,6,2,7; Hofstadter Q: 1,1,2,3,3.'),
'INTEGER-SQRT':('Unsigned integer square root rounded down; no floating-point operations.','sqrt(15) -> 3; sqrt(16) -> 4; UINT32_MAX -> 65535.'),
'KNAPSACK':('Zero-one knapsack with unsigned-halfword weights/values, n<=65535. DP has cap+1 words. Traverse capacity downward; each item is used once, including zero-weight items. Invalid input returns zero.','One item weight 2,value 3, capacity 4 -> value 3, not 6.'),
'LCG':('Five arguments: x,a,c,m,shift. First compute a*x+c modulo 2^32, then optional modulus, then right shift. shift>=32 returns zero.','x=3,a=5,c=1,m=16,shift=0 -> (16 mod 16)=0.'),
'LINEAR-SEARCH':('First/last variants return a signed index or -1, so require count<=INT32_MAX. All-matches variant returns total matches while writing at most capacity indexes.','[4,2,4]: first 0,last 2,all [0,2]. Capacity one writes only 0 and still returns 2.'),
'LIS':('Strictly increasing subsequence length, not necessarily contiguous. Caller DP has n words. Empty or invalid input returns zero.','[3,1,2,5]: subsequence [1,2,5] has length 3.'),
'LOOK-AND-SAY':('Encode equal-byte runs as (count,value) byte pairs. A run above 255 or insufficient capacity returns zero; a prefix may already be written. Input/output must not overlap.','[1,1,2] -> [(2,1),(1,2)], four output bytes.'),
'MEMMOVE':('Overlap-safe byte movement using integer address ordering. Return destination. Null inputs are a no-op; valid spans must contain n accessible bytes.','Move "abcd" one byte right inside its buffer -> "aabcd".'),
'MERGE-SORT':('Stable signed-word merge sort. Scratch has n disjoint words; identical buffers are rejected as a no-op. Recursion depth grows logarithmically.','[3,1,2] splits into [3] and [1,2], then merges into [1,2,3].'),
'MOVING-AVERAGE':('Signed-word moving average with 64-bit accumulator. Require 1<=window<=n and window<=INT32_MAX. Output has n-window+1 words; use disjoint storage. Division truncates toward zero.','[2,4,6], window 2 -> [3,5].'),
'PACKED-MATMUL':('Packed 8x8 binary matrices; bit 8*r+c represents cell(r,c). Multiplication is over GF(2): XOR the AND products.','Multiplying any packed matrix by the binary identity preserves it.'),
'POPCOUNT-PARITY':('Count set bits in an unsigned word. Parity variant returns that count modulo two.','0b1011 has three set bits, parity 1.'),
'PREFIX-SUM':('Signed-word input builds count+1 signed 64-bit prefix values, starting at zero. Range queries use [begin,end) within the count and must use a prefix array built under this contract.','[2,-1,4] -> prefix [0,2,1,5]; sum [1,3)=5-2=3.'),
'PRIME-FACTORIZATION':('Primary tests primality; factorize emits ascending prime factors and returns total count even when capacity truncates writes. Zero and one have no factors.','36 -> factors 2,2,3,3; count 4.'),
'QUICKSORT':('In-place ascending signed-word partition sorting; n<=INT32_MAX. Midpoint pivot, recursive partitions, not stable. Worst-case stack/time remain input-dependent.','[3,1,2] partitions around 1, then sorts the right portion to [1,2,3].'),
'RECURSIVE-DFS':('Byte adjacency matrix with n<=256 and caller-initialized seen. Return newly visited count. The public helper validates vertex and depth; recursion depth is bounded by n.','0->1->2: enter 0,1,2, then return counts 1,2,3.'),
'REDUCTION':('Nonempty signed/unsigned word scans return status and a result struct with minimum,maximum and 64-bit sum. Result storage is disjoint from input. Both signed and unsigned variants have matching assembly.','[-2,7,1] -> minimum -2,maximum 7,sum 6.'),
'RUN-LENGTH':('Encode byte values into separate value/run arrays with capacity entries. Runs longer than 255 are split. Return entry count, or zero on failure with a possible output prefix.','256 repeated A bytes -> values [A,A], runs [255,1].'),
'SATURATING-ARITHMETIC':('Clamp signed 64-bit values into chosen signed-word limits. Reversed limits return minimum. Absolute INT32_MIN is returned as unsigned 2147483648; signed addition saturates.','INT32_MAX+1 saturates to INT32_MAX.'),
'SELECTION-SORT':('In-place ascending signed-word selection sort, not stable. Null input is a no-op.','[3,1,2]: select 1, then 2 -> [1,2,3].'),
'STRING-PRIMITIVES':('Bounded length and unsigned-byte comparison; NUL-terminated source strings. Copy truncates to capacity-1 and always terminates when capacity>0; it does not report truncation as failure. Substring search returns first index or -1.','Copy "abcd" into capacity 4 -> "abc" plus terminator, return 3.'),
'ASM-OBJECTS':('Examples export initialized words, reserved workspace, masks and a magic constant using C-matching names; old assembly aliases remain. Word sum wraps modulo 2^32.','Initialized [1,2,3,4] sums to 10; mask table is [1,2,4,8].'),
'WIDE-DIVISION':('Signed 64-by-32 division truncates toward zero; remainder has dividend sign. Divisor zero returns zero and writes zero remainder. INT64_MIN/-1 retains the legacy INT64_MIN bit-pattern result and must be treated as overflow by callers.','-17/5 -> quotient -3, remainder -2.'),
'CIRCULAR-QUEUE':('Caller initializes a valid queue. tail is the enqueue index, head is dequeue; reject corrupt indexes/count and full/empty operations. Synchronization is caller-owned.','Capacity two: enqueue 4,5; dequeue returns 4; next enqueue wraps.'),
'LINKED-LIST':('Caller supplies an acyclic singly linked list. Find/remove first matching value; inserted node must be detached and distinct from position. Removal detaches the returned node.','1->2->3, remove 2 -> 1->3; removed node next=NULL.'),
'RING-BUFFER':('Caller initializes a valid ring. head is producer index, tail is consumer; validate indexes/count. This reference is not independently interrupt-safe: shared operations require caller synchronization.','Capacity two: put 4,5; take 4; put 6; remaining order 5,6.'),
'STACK':('top is a count in [0,cap]. Reject invalid state before access; push fails when full and pop when empty. Return 1 only for a completed operation.','Push 4 then 5; pop returns 5 and decrements top.'),
'UNION-FIND':('Parent links must form an initialized forest with roots pointing to themselves and valid ranks. The wrapper checks endpoint indexes. The raw find helper assumes valid forest links; corrupt or cyclic input is outside this interface contract.','Initially parent [0,1,2]; union(0,1) joins their roots, while 2 remains separate.'),
'PACKED-TRANSPOSE':('Packed 8x8 bit matrix: move bit 8*r+c to bit 8*c+r.','A bit at (0,1), value 2, moves to (1,0), value 256.')
}
# Only the suffix routine named here is the focus of a variant page.
VARIANT_SUFFIX={
'First matching array element':'','Last matching array element':'_last','Collect every matching index':'_all',
'Lower bound insertion position':'','Exact binary search from lower bound':'_exact',
'Right array rotation with normalized distance':'_right','Left array rotation by reversal':'',
'Overflow-aware least common multiple':'_lcm','Trial prime factorization':'_factorize',
'Decimal extraction and reconstruction':'_extract','Kaprekar digit ordering step':'_kaprekar_4',
'Parity from population count':'_parity','Bitfield extraction':'_extract',
'Bitfield insertion without neighbor damage':'','Saturating addition':'_add_i32',
'Constant-time range sums':'_range','Bounded string copy':'_copy',
'Lexicographic byte comparison':'_compare','Two-row edit distance':''
}
def source_key(folder):
 return re.sub(r'^PAT-(?:ALG|DS|MEM|DATA)-|-\d+$','',folder.name)
def source_details(folder):
 raw=(folder/'c/reference.c').read_text()
 code=raw.split('#ifdef PATTERN_HOST_TEST')[0]
 key=source_key(folder)
 if key not in REVIEWS:raise ValueError('Missing review: '+key)
 contract,trace=REVIEWS[key]
 helper_contracts={
 'HEAP-SORT':' The exported down helper repairs the heap rooted at i: i<n, both child subtrees must already be max-heaps, and a contains n words.',
 'MERGE-SORT':' The exported ms helper sorts [l,r); require l<=r and both buffers to cover r words. The merge helper requires l<=m<=r and each half already sorted; scratch must be disjoint.',
 'QUICKSORT':' The exported qs helper uses inclusive signed bounds l and r; supply valid indexes and an accessible array for every index in that interval.',
 'RECURSIVE-DFS':' The exported visit helper is also shown below; its seen array and adjacency matrix obey the same storage contract.'
 }
 contract+=helper_contracts.get(key,'')
 decl=declarations(code)
 prototypes=re.findall(r'(?m)^((?:[A-Za-z_]\w*[\s*]+)+[A-Za-z_]\w*\s*\([^;{}]*\))\s*;',decl)
 prototypes=[re.sub(r'\s+',' ',p).strip() for p in prototypes if not p.startswith('static ')]
 tests=raw.split('#ifdef PATTERN_HOST_TEST',1)[1].rsplit('#endif',1)[0]
 return dict(contract=contract,trace=trace,prototype=';\n'.join(prototypes)+';',tests=tests,source_id=folder.name,
             history='Possible variation',summary=contract)
