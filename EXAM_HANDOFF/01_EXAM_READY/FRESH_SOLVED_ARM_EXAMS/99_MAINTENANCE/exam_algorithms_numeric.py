"""Directly authored arithmetic, recurrence and bit manipulation routines."""
from algorithm_catalog import add
F='Arithmetic and number theory'
B='Bits and fixed point'
R='Recursion and dynamic programming'
add('factorial-iterative','Iterative factorial',R,'int factorial_iterative(uint32_t n, uint32_t *out)',
'Accept n=0..12 and a valid output pointer. Return 1 and write n!, or 0 without writing.',
'1. Reject n above 12.\n2. Start at one.\n3. Multiply by n and count down.',
'n=4: product 1 -> 4 -> 12 -> 24 -> 24.',
'int factorial_iterative(uint32_t n,uint32_t*out){if(!out||n>12)return 0;uint32_t v=1;while(n)v*=n--;*out=v;return 1;}',
'''cmp r1,#0 | beq fi_bad | cmp r0,#12 | bhi fi_bad | movs r2,#1
fi_loop: | cmp r0,#0 | beq fi_done | mul r2,r0,r2 | subs r0,#1 | b fi_loop
fi_done: | str r2,[r1] | movs r0,#1 | bx lr
fi_bad: | movs r0,#0 | bx lr''',
'uint32_t v=99;CHECK(factorial_iterative(0,&v)&&v==1);CHECK(factorial_iterative(4,&v)&&v==24);CHECK(factorial_iterative(12,&v)&&v==479001600);CHECK(!factorial_iterative(13,&v)&&v==479001600);')
add('factorial-recursive','Recursive factorial',R,'int factorial_recursive(uint32_t n, uint32_t *out)',
'Accept n=0..12. Return 1 and store n!, or 0 without writing. At most 13 helper frames of eight bytes.',
'1. Validate inputs.\n2. Save n across a call for n-1.\n3. Multiply on return.',
'n=3: calls 3,2,1,0; returned products 1,1,2,6.',
'static uint32_t fact_step(uint32_t n){return n?n*fact_step(n-1):1;}int factorial_recursive(uint32_t n,uint32_t*out){if(!out||n>12)return 0;*out=fact_step(n);return 1;}',
'''cmp r1,#0 | beq fr_bad | cmp r0,#12 | bhi fr_bad | push {r4,lr} | mov r4,r1 | bl fr_step | str r0,[r4] | movs r0,#1 | pop {r4,pc}
fr_bad: | movs r0,#0 | bx lr''',
'uint32_t v=0;CHECK(factorial_recursive(0,&v)&&v==1);CHECK(factorial_recursive(3,&v)&&v==6);CHECK(factorial_recursive(12,&v)&&v==479001600);CHECK(!factorial_recursive(13,&v));',
complexity='O(n) time and O(n) stack; n<=12',
helpers='''fr_step: | push {r4,lr} | mov r4,r0 | cmp r0,#0 | beq fr_base | subs r0,#1 | bl fr_step | mul r0,r4,r0 | pop {r4,pc}
fr_base: | movs r0,#1 | pop {r4,pc}''')
add('fibonacci-number','Nth Fibonacci number',R,'int fibonacci_number(uint32_t n, uint32_t *out)',
'F(0)=0,F(1)=1. Accept n<=47; return 1, or 0 without writing on failure.',
'1. Keep consecutive terms.\n2. Advance to the requested index.\n3. Avoid computing F(48).',
'n=5: pairs (0,1),(1,1),(1,2),(2,3),(3,5); result 5.',
'int fibonacci_number(uint32_t n,uint32_t*out){if(!out||n>47)return 0;if(!n){*out=0;return 1;}uint32_t a=0,b=1;while(--n){uint32_t t=a+b;a=b;b=t;}*out=b;return 1;}',
'''cmp r1,#0 | beq fn_bad | cmp r0,#47 | bhi fn_bad | movs r2,#0 | cmp r0,#0 | beq fn_store | movs r3,#1
fn_loop: | subs r0,#1 | beq fn_last | add r12,r2,r3 | mov r2,r3 | mov r3,r12 | b fn_loop
fn_last: | mov r2,r3
fn_store: | str r2,[r1] | movs r0,#1 | bx lr
fn_bad: | movs r0,#0 | bx lr''',
'uint32_t v=99;CHECK(fibonacci_number(0,&v)&&v==0);CHECK(fibonacci_number(5,&v)&&v==5);CHECK(fibonacci_number(47,&v)&&v==2971215073u);CHECK(!fibonacci_number(48,&v)&&v==2971215073u);')
for tri in (False,True):
 name='tribonacci_array' if tri else 'fibonacci_array'
 seed='0,0,1' if tri else '0,1'
 limit=32 if tri else 48
 calc='i<2?0:i==2?1:out[i-1]+out[i-2]+out[i-3]' if tri else 'i<2?i:out[i-1]+out[i-2]'
 body='''movs r3,#0 | cmp r2,#2 | blo seq_write | mov r3,#1 | beq seq_write | sub r3,r2,#1 | ldr r4,[r0,r3,lsl #2] | subs r3,#1 | ldr r5,[r0,r3,lsl #2] | add r4,r5 | subs r3,#1 | ldr r5,[r0,r3,lsl #2] | add r3,r4,r5''' if tri else '''cmp r2,#2 | bhs seq_sum | mov r3,r2 | b seq_write
seq_sum: | sub r3,r2,#1 | ldr r4,[r0,r3,lsl #2] | subs r3,#1 | ldr r5,[r0,r3,lsl #2] | add r3,r4,r5'''
 add(name.replace('_','-'),name.replace('_',' ').capitalize()+' generation',R,
 f'int {name}(uint32_t *out, uint32_t count, uint32_t capacity)',
 f'Seeds {seed}; accept count<={limit}, capacity>=count. Return 1 on success; invalid input returns 0 before writes. Empty output is valid.',
 '1. Validate count and capacity.\n2. Store requested seed terms.\n3. Sum preceding terms for every later index.',
 'count=7: 0,0,1,1,2,4,7.' if tri else 'count=6: 0,1,1,2,3,5.',
 f'int {name}(uint32_t*out,uint32_t n,uint32_t cap){{if(n>{limit}||n>cap||(!out&&n))return 0;for(uint32_t i=0;i<n;i++)out[i]={calc};return 1;}}',
 f'''cmp r1,#{limit} | bhi seq_bad | cmp r1,r2 | bhi seq_bad | cmp r1,#0 | beq seq_ok | cmp r0,#0 | beq seq_bad | push {{r4,r5}} | movs r2,#0
seq_loop: | {body}
seq_write: | str r3,[r0,r2,lsl #2] | adds r2,#1 | cmp r2,r1 | blo seq_loop | pop {{r4,r5}}
seq_ok: | movs r0,#1 | bx lr
seq_bad: | movs r0,#0 | bx lr''',
 f'uint32_t a[49]={{0}};a[48]=77;CHECK({name}(a,7,7)&&a[6]=={7 if tri else 8});CHECK(!{name}(a,8,7));CHECK({name}(0,0,0));CHECK({name}(a,{limit},{limit})&&a[48]==77);')
add('bounded-collatz','Bounded Collatz sequence',R,'uint32_t bounded_collatz(uint32_t seed, uint32_t *out, uint32_t capacity)',
'Store a positive seed and successive terms through 1. Return count, or 0 on invalid input, exhausted capacity or overflow. Failure may leave a valid prefix.',
'1. Store within capacity.\n2. Stop at 1.\n3. Halve even terms or check and compute 3n+1.',
'6,3,10,5,16,8,4,2,1; return 9.',
'uint32_t bounded_collatz(uint32_t v,uint32_t*out,uint32_t cap){uint32_t n=0;if(!v||!out)return 0;for(;;){if(n==cap)return 0;out[n++]=v;if(v==1)return n;if(v&1){if(v>1431655764u)return 0;v=3*v+1;}else v/=2;}}',
'''cmp r0,#0 | beq bc_bad | cmp r1,#0 | beq bc_bad | push {r4,r5} | movs r3,#0 | ldr r4,=1431655764
bc_loop: | cmp r3,r2 | bhs bc_fail | str r0,[r1,r3,lsl #2] | adds r3,#1 | cmp r0,#1 | beq bc_done | tst r0,#1 | beq bc_even | cmp r0,r4 | bhi bc_fail | add r0,r0,r0,lsl #1 | adds r0,#1 | b bc_loop
bc_even: | lsrs r0,#1 | b bc_loop
bc_done: | mov r0,r3 | pop {r4,r5} | bx lr
bc_fail: | pop {r4,r5}
bc_bad: | movs r0,#0 | bx lr''',
'uint32_t a[10]={0};a[9]=77;CHECK(bounded_collatz(6,a,9)==9&&a[8]==1&&a[9]==77);CHECK(!bounded_collatz(6,a,2));CHECK(bounded_collatz(1,a,1)==1);CHECK(!bounded_collatz(0,a,10));CHECK(!bounded_collatz(0xffffffffu,a,10));',
complexity='O(capacity) time and O(1) auxiliary space')
for slug,title,init,update,cu,expected in [
('decimal-digit-count','Decimal digit count',0,'adds r1,#1','v++',5),
('decimal-digit-product','Decimal digit product',1,'mul r1,r3,r1','v*=d',0)]:
 name=slug.replace('-','_')
 add(slug,title,F,f'uint32_t {name}(uint32_t n)',
 'Unsigned decimal input. Zero has one digit; return the count or product named by the routine.',
 '1. Extract a remainder modulo ten.\n2. Update the accumulator.\n3. Divide by ten; include one iteration for zero.',
 '12034: digits 4,3,0,2,1; count=5, product=0.',
 f'uint32_t {name}(uint32_t n){{uint32_t v={init};do{{uint32_t d=n%10;(void)d;{cu};n/=10;}}while(n);return v;}}',
 f'''movs r1,#{init} | movs r2,#10
dd_loop: | udiv r12,r0,r2 | mls r3,r12,r2,r0 | {update} | mov r0,r12 | cmp r0,#0 | bne dd_loop | mov r0,r1 | bx lr''',
 f'CHECK({name}(12034)=={expected});CHECK({name}(0)=={1 if init==0 else 0});CHECK({name}(123)=={3 if init==0 else 6});')
add('digital-root','Repeated digit sum and digital root',F,'uint32_t digital_root(uint32_t n)',
'Return repeated decimal digit sum, from 0 through 9; digital_root(0)=0.',
'1. Sum decimal digits.\n2. Repeat while the sum has at least two digits.',
'9875 -> 29 -> 11 -> 2.',
'uint32_t digital_root(uint32_t n){while(n>=10){uint32_t s=0;do{s+=n%10;n/=10;}while(n);n=s;}return n;}',
'''movs r3,#10
dr_outer: | cmp r0,#10 | blo dr_done | movs r1,#0
dr_inner: | udiv r12,r0,r3 | mls r2,r12,r3,r0 | adds r1,r2 | mov r0,r12 | cmp r0,#0 | bne dr_inner | mov r0,r1 | b dr_outer
dr_done: | bx lr''','CHECK(digital_root(9875)==2);CHECK(digital_root(0)==0);CHECK(digital_root(4294967295u)==3);')
add('checked-decimal-reversal','Checked decimal reversal',F,'int reverse_decimal(uint32_t n, uint32_t *out)',
'Reverse decimal digits, dropping leading zeros in the result. Return 0 without writing on overflow or null output.',
'1. Extract a digit.\n2. Check value*10+digit.\n3. Store only the completed result.',
'1203: 0 -> 3 -> 30 -> 302 -> 3021.',
'int reverse_decimal(uint32_t n,uint32_t*out){if(!out)return 0;uint64_t v=0;do{v=v*10+n%10;if(v>UINT32_MAX)return 0;n/=10;}while(n);*out=(uint32_t)v;return 1;}',
'''cmp r1,#0 | beq rd_bad | push {r4-r6,lr} | movs r2,#0 | movs r3,#10
rd_loop: | udiv r4,r0,r3 | mls r5,r4,r3,r0 | umull r0,r6,r2,r3 | adds r2,r0,r5 | bcs rd_fail | cmp r6,#0 | bne rd_fail | mov r0,r4 | cmp r0,#0 | bne rd_loop | str r2,[r1] | movs r0,#1 | pop {r4-r6,pc}
rd_fail: | pop {r4-r6,lr}
rd_bad: | movs r0,#0 | bx lr''',
'uint32_t v=7;CHECK(reverse_decimal(1203,&v)&&v==3021);CHECK(reverse_decimal(0,&v)&&v==0);v=99;CHECK(!reverse_decimal(4294967295u,&v)&&v==99);CHECK(reverse_decimal(123321,&v)&&v==123321);')
add('digit-sum-any-base','Digit sum in a supplied base',F,'int digit_sum_base(uint32_t n, uint32_t base, uint32_t *out)',
'Accept bases 2..36. Return 1 with the digit sum, or 0 without writing on invalid base or null output.',
'1. Divide by the base.\n2. Add the remainder.\n3. Continue with the quotient.',
'31 in base 16 has digits F and 1: sum=16.',
'int digit_sum_base(uint32_t n,uint32_t b,uint32_t*out){if(b<2||b>36||!out)return 0;uint32_t s=0;do{s+=n%b;n/=b;}while(n);*out=s;return 1;}',
'''cmp r1,#2 | blo ds_bad | cmp r1,#36 | bhi ds_bad | cmp r2,#0 | beq ds_bad | push {r4,r5} | movs r3,#0
ds_loop: | udiv r4,r0,r1 | mls r5,r4,r1,r0 | add r3,r5 | mov r0,r4 | cmp r0,#0 | bne ds_loop | str r3,[r2] | pop {r4,r5} | movs r0,#1 | bx lr
ds_bad: | movs r0,#0 | bx lr''',
'uint32_t v=8;CHECK(digit_sum_base(31,16,&v)&&v==16);CHECK(digit_sum_base(0xffffffffu,2,&v)&&v==32);CHECK(!digit_sum_base(3,1,&v));')
add('armstrong-number','Armstrong number test',F,'int armstrong_number(uint32_t n)',
'Return whether n equals the sum of decimal digits raised to the digit count. Zero is accepted; use a 64-bit sum.',
'1. Count digits.\n2. Raise each digit to that count.\n3. Compare the widened sum with the original.',
'153: 1^3+5^3+3^3=1+125+27=153.',
'int armstrong_number(uint32_t n){uint32_t k=0,x=n;do{k++;x/=10;}while(x);uint64_t s=0;x=n;do{uint32_t d=x%10;uint64_t p=1;for(uint32_t i=0;i<k;i++)p*=d;s+=p;x/=10;}while(x);return s==n;}',
'''push {r4-r10,lr} | mov r4,r0 | mov r5,r0 | movs r6,#0 | movs r7,#10
an_count: | adds r6,#1 | udiv r0,r0,r7 | cmp r0,#0 | bne an_count | movs r8,#0 | movs r9,#0
an_digit: | udiv r0,r5,r7 | mls r1,r0,r7,r5 | mov r5,r0 | mov r2,r6 | movs r3,#1
an_power: | mul r3,r1,r3 | subs r2,#1 | bne an_power | adds r8,r8,r3 | adc r9,r9,#0 | cmp r5,#0 | bne an_digit | movs r0,#0 | cmp r9,#0 | bne an_done | cmp r8,r4 | bne an_done | movs r0,#1
an_done: | pop {r4-r10,pc}''',
'CHECK(armstrong_number(0));CHECK(armstrong_number(153));CHECK(armstrong_number(9474));CHECK(!armstrong_number(154));CHECK(!armstrong_number(4294967295u));')
DIVHELP='''div_sum: | push {r4-r8,lr} | mov r4,r0 | movs r5,#1 | movs r6,#0 | movs r7,#0 | cmp r4,#0 | beq dv_done
dv_loop: | udiv r8,r4,r5 | cmp r5,r8 | bhi dv_done | mls r2,r8,r5,r4 | cmp r2,#0 | bne dv_next | adds r6,r6,r5 | adc r7,r7,#0 | cmp r5,r8 | beq dv_next | adds r6,r6,r8 | adc r7,r7,#0
dv_next: | adds r5,#1 | b dv_loop
dv_done: | mov r0,r6 | mov r1,r7 | pop {r4-r8,pc}'''
DIVC='static uint64_t divisor_sum_core(uint32_t n){uint64_t s=0;for(uint32_t d=1;n&&d<=n/d;d++)if(n%d==0){s+=d;if(d!=n/d)s+=n/d;}return s;}'
add('divisor-sum','Sum of positive divisors',F,'uint64_t divisor_sum(uint32_t n)',
'Sum positive divisors in 64 bits. Define the result for zero as zero.',
'1. Visit d while d<=n/d.\n2. Add divisor pairs.\n3. Count a square root once.',
'12: pairs (1,12),(2,6),(3,4); sum 28.',
DIVC+'uint64_t divisor_sum(uint32_t n){return divisor_sum_core(n);}',
'b div_sum','CHECK(divisor_sum(0)==0);CHECK(divisor_sum(1)==1);CHECK(divisor_sum(12)==28);CHECK(divisor_sum(36)==91);',
complexity='O(sqrt(n)) time, O(1) space',helpers=DIVHELP)
add('perfect-number','Perfect-number test',F,'int perfect_number(uint32_t n)',
'Return 1 when positive proper divisors sum to n. Zero and one are not perfect.',
'1. Sum divisor pairs in 64 bits.\n2. Compare the all-divisor sum with 2*n.',
'6: proper divisors 1,2,3 sum to 6.',
DIVC+'int perfect_number(uint32_t n){return n>1&&divisor_sum_core(n)==(uint64_t)n*2;}',
'''cmp r0,#2 | blo pn_bad | push {r4,lr} | mov r4,r0 | bl div_sum | lsrs r2,r4,#31 | lsls r4,#1 | cmp r1,r2 | bne pn_fail | cmp r0,r4 | bne pn_fail | movs r0,#1 | pop {r4,pc}
pn_fail: | movs r0,#0 | pop {r4,pc}
pn_bad: | movs r0,#0 | bx lr''',
'CHECK(perfect_number(6));CHECK(perfect_number(28));CHECK(!perfect_number(1));CHECK(!perfect_number(12));CHECK(!perfect_number(0));',
complexity='O(sqrt(n)) time, O(1) space',helpers=DIVHELP)
add('divisor-count','Number of positive divisors',F,'uint32_t divisor_count(uint32_t n)',
'Count positive divisors; divisor_count(0)=0.',
'1. Visit divisor pairs.\n2. Count two for unequal pairs and one for a square root.',
'36: (1,36),(2,18),(3,12),(4,9),(6,6); count 9.',
'uint32_t divisor_count(uint32_t n){uint32_t c=0;for(uint32_t d=1;n&&d<=n/d;d++)if(n%d==0)c+=d==n/d?1:2;return c;}',
'''push {r4,r5} | movs r1,#1 | movs r2,#0 | cmp r0,#0 | beq dc_done
dc_loop: | udiv r3,r0,r1 | cmp r1,r3 | bhi dc_done | mls r4,r3,r1,r0 | cmp r4,#0 | bne dc_next | adds r2,#1 | cmp r1,r3 | beq dc_next | adds r2,#1
dc_next: | adds r1,#1 | b dc_loop
dc_done: | mov r0,r2 | pop {r4,r5} | bx lr''',
'CHECK(divisor_count(0)==0);CHECK(divisor_count(1)==1);CHECK(divisor_count(36)==9);CHECK(divisor_count(13)==2);',complexity='O(sqrt(n)) time, O(1) space')
add('sieve-of-eratosthenes','Sieve of Eratosthenes',F,'int prime_sieve(uint8_t *flags, uint32_t limit, uint32_t capacity)',
'Fill flags[0..limit]: 1 for prime, 0 otherwise. Accept limit<=65535 and capacity>limit. Invalid input returns 0 before writes.',
'1. Initialize flags; clear 0 and 1.\n2. For each prime p, clear multiples from p*p.',
'limit=10: clear multiples of 2 then 3; primes 2,3,5,7.',
'int prime_sieve(uint8_t*f,uint32_t n,uint32_t cap){if(!f||n>65535||cap<=n)return 0;for(uint32_t i=0;i<=n;i++)f[i]=i>=2;for(uint32_t p=2;p<=n/p;p++)if(f[p])for(uint32_t j=p*p;j<=n;j+=p)f[j]=0;return 1;}',
'''cmp r0,#0 | beq ps_bad | ldr r3,=65535 | cmp r1,r3 | bhi ps_bad | cmp r2,r1 | bls ps_bad | push {r4-r6,lr} | movs r2,#0
ps_init: | movs r3,#0 | cmp r2,#2 | blo ps_write | movs r3,#1
ps_write: | strb r3,[r0,r2] | adds r2,#1 | cmp r2,r1 | bls ps_init | movs r2,#2
ps_outer: | udiv r3,r1,r2 | cmp r2,r3 | bhi ps_done | ldrb r3,[r0,r2] | cmp r3,#0 | beq ps_next | mul r4,r2,r2 | movs r5,#0
ps_inner: | cmp r4,r1 | bhi ps_next | strb r5,[r0,r4] | add r4,r2 | b ps_inner
ps_next: | adds r2,#1 | b ps_outer
ps_done: | movs r0,#1 | pop {r4-r6,pc}
ps_bad: | movs r0,#0 | bx lr''',
'uint8_t f[12]={0};f[11]=77;CHECK(prime_sieve(f,10,11)&&f[2]&&f[3]&&f[5]&&f[7]&&!f[0]&&!f[1]&&!f[4]&&!f[9]&&f[11]==77);CHECK(!prime_sieve(f,10,10));',
complexity='O(limit log log limit) time; limit+1 output bytes')
add('checked-binomial','Bounded checked binomial coefficient',F,'int binomial_coefficient(uint32_t n, uint32_t k, uint32_t *out)',
'Accept 0<=k<=n<=30. Return 1 and C(n,k), or 0 without writing. This bound keeps intermediate multiplication within 32 bits.',
'1. Replace k by min(k,n-k).\n2. Multiply by n-k+i and divide exactly by i.',
'C(5,2): 1*4/1=4; 4*5/2=10.',
'int binomial_coefficient(uint32_t n,uint32_t k,uint32_t*out){if(!out||n>30||k>n)return 0;if(k>n-k)k=n-k;uint32_t v=1;for(uint32_t i=1;i<=k;i++)v=v*(n-k+i)/i;*out=v;return 1;}',
'''cmp r2,#0 | beq bn_bad | cmp r0,#30 | bhi bn_bad | cmp r1,r0 | bhi bn_bad | push {r4-r6,lr} | sub r3,r0,r1 | cmp r1,r3 | bls bn_start | mov r1,r3
bn_start: | sub r0,r0,r1 | movs r3,#1 | movs r4,#1
bn_loop: | cmp r4,r1 | bhi bn_done | add r5,r0,r4 | mul r3,r5,r3 | udiv r3,r3,r4 | adds r4,#1 | b bn_loop
bn_done: | str r3,[r2] | movs r0,#1 | pop {r4-r6,pc}
bn_bad: | movs r0,#0 | bx lr''',
'uint32_t v=0;CHECK(binomial_coefficient(5,2,&v)&&v==10);CHECK(binomial_coefficient(30,15,&v)&&v==155117520);CHECK(binomial_coefficient(0,0,&v)&&v==1);CHECK(!binomial_coefficient(31,1,&v));')
add('modular-exponentiation','Bounded modular exponentiation',F,'int modular_power(uint32_t base, uint32_t exponent, uint32_t modulus, uint32_t *out)',
'Accept modulus 1..65535. Return 1 and base^exponent modulo modulus. Invalid modulus or null output fails without writing. Exponent zero returns 1 modulo modulus.',
'1. Reduce the base.\n2. Multiply for set exponent bits.\n3. Square and reduce the base.',
'3^5 mod 7: result 1 -> 3 -> 3 -> 5.',
'int modular_power(uint32_t b,uint32_t e,uint32_t m,uint32_t*out){if(!out||!m||m>65535)return 0;b%=m;uint32_t r=1%m;while(e){if(e&1)r=(r*b)%m;e>>=1;b=(b*b)%m;}*out=r;return 1;}',
'''cmp r3,#0 | beq mp_bad | cmp r2,#0 | beq mp_bad | push {r4-r6,lr} | ldr r4,=65535 | cmp r2,r4 | bhi mp_fail | udiv r4,r0,r2 | mls r0,r4,r2,r0 | movs r4,#1 | udiv r5,r4,r2 | mls r4,r5,r2,r4
mp_loop: | cmp r1,#0 | beq mp_done | tst r1,#1 | beq mp_square | mul r4,r0,r4 | udiv r5,r4,r2 | mls r4,r5,r2,r4
mp_square: | lsrs r1,#1 | mul r0,r0,r0 | udiv r5,r0,r2 | mls r0,r5,r2,r0 | b mp_loop
mp_done: | str r4,[r3] | movs r0,#1 | pop {r4-r6,pc}
mp_fail: | pop {r4-r6,lr}
mp_bad: | movs r0,#0 | bx lr''',
'uint32_t v=9;CHECK(modular_power(3,5,7,&v)&&v==5);CHECK(modular_power(2,0,1,&v)&&v==0);CHECK(!modular_power(3,2,0,&v));CHECK(modular_power(65534,2,65535,&v)&&v==1);',
complexity='O(log exponent) time, O(1) space')
add('word-hamming-distance','Word Hamming distance',B,'uint32_t word_hamming(uint32_t a, uint32_t b)',
'Count differing positions in two 32-bit words; result 0..32.',
'1. XOR the words.\n2. Clear the lowest set bit and count until zero.',
'1010 XOR 1100 = 0110; two set bits.',
'uint32_t word_hamming(uint32_t a,uint32_t b){uint32_t x=a^b,n=0;while(x){x&=x-1;n++;}return n;}',
'''eor r0,r0,r1 | movs r1,#0
wh_loop: | cmp r0,#0 | beq wh_done | sub r2,r0,#1 | and r0,r0,r2 | adds r1,#1 | b wh_loop
wh_done: | mov r0,r1 | bx lr''',
'CHECK(word_hamming(10,12)==2);CHECK(word_hamming(0,0xffffffffu)==32);CHECK(word_hamming(42,42)==0);',complexity='At most 32 iterations')
add('reverse-32-bits','Reverse all 32 bits',B,'uint32_t reverse_bits(uint32_t value)',
'Reverse all 32 positions, including leading zeros.',
'1. Shift the result left.\n2. Append the input low bit.\n3. Repeat exactly 32 times.',
'0x0000000D becomes 0xB0000000.',
'uint32_t reverse_bits(uint32_t v){uint32_t r=0;for(unsigned i=0;i<32;i++){r=(r<<1)|(v&1);v>>=1;}return r;}',
'''movs r1,#0 | movs r2,#32
rb_loop: | lsrs r0,#1 | adc r1,r1,r1 | subs r2,#1 | bne rb_loop | mov r0,r1 | bx lr''',
'CHECK(reverse_bits(13)==0xb0000000u);CHECK(reverse_bits(0)==0);CHECK(reverse_bits(0xffffffffu)==0xffffffffu);CHECK(reverse_bits(reverse_bits(123456))==123456);',complexity='Exactly 32 iterations')
add('longest-one-bit-run','Longest consecutive-one bit run',B,'uint32_t longest_one_run(uint32_t value)',
'Return longest adjacent set-bit run within 32 bits.',
'1. Read a low bit.\n2. Extend or reset the current run.\n3. Update the best run and shift.',
'1101110 has runs of 2 and 3; return 3.',
'uint32_t longest_one_run(uint32_t v){uint32_t best=0,run=0;for(unsigned i=0;i<32;i++){run=(v&1)?run+1:0;if(run>best)best=run;v>>=1;}return best;}',
'''movs r1,#0 | movs r2,#0 | movs r3,#32
lo_loop: | tst r0,#1 | beq lo_zero | adds r1,#1 | cmp r1,r2 | bls lo_next | mov r2,r1 | b lo_next
lo_zero: | movs r1,#0
lo_next: | lsrs r0,#1 | subs r3,#1 | bne lo_loop | mov r0,r2 | bx lr''',
'CHECK(longest_one_run(110)==3);CHECK(longest_one_run(0)==0);CHECK(longest_one_run(0xffffffffu)==32);',complexity='Exactly 32 iterations')
for trailing in (True,False):
 name='trailing_zero_count' if trailing else 'leading_zero_count'
 mask='1' if trailing else '0x80000000'
 shift='lsrs' if trailing else 'lsls'
 add(name.replace('_','-'),name.replace('_',' ').capitalize(),B,f'uint32_t {name}(uint32_t value)',
 'Count zeros from the named end; zero has a count of 32.',
 '1. Handle zero.\n2. Shift toward the tested end until a set bit arrives.',
 '0x00000008 has 3 trailing zeros and 28 leading zeros.',
 f'uint32_t {name}(uint32_t v){{if(!v)return 32;uint32_t n=0;while(!(v&{mask}u)){{n++;v{">>" if trailing else "<<"}=1;}}return n;}}',
 f'''cmp r0,#0 | beq z_all | movs r1,#0
z_loop: | tst r0,#{mask} | bne z_done | adds r1,#1 | {shift} r0,#1 | b z_loop
z_done: | mov r0,r1 | bx lr
z_all: | movs r0,#32 | bx lr''',
 f'CHECK({name}(8)=={3 if trailing else 28});CHECK({name}(0)==32);CHECK({name}(0xffffffffu)==0);',complexity='At most 32 iterations')
add('bit-width-palindrome','Palindrome within a bit width',B,'int bit_palindrome(uint32_t value, uint32_t width)',
'Compare the low width bits for width=0..32. Ignore higher bits. Width zero is a palindrome; width>32 returns 0.',
'1. Reverse exactly width bits.\n2. Compare with the masked original.',
'1001,width=4 -> true; 01001,width=5 -> false.',
'int bit_palindrome(uint32_t v,uint32_t w){if(w>32)return 0;uint32_t r=0,x=v;for(uint32_t i=0;i<w;i++){r=(r<<1)|(x&1);x>>=1;}uint32_t m=w==32?UINT32_MAX:w?((1u<<w)-1):0;return r==(v&m);}',
'''cmp r1,#32 | bhi bp_bad | push {r4,r5} | mov r4,r0 | movs r2,#0 | movs r3,#0
bp_loop: | cmp r1,#0 | beq bp_check | lsrs r0,#1 | adc r2,r2,r2 | lsls r3,#1 | adds r3,#1 | subs r1,#1 | b bp_loop
bp_check: | and r4,r4,r3 | movs r0,#0 | cmp r4,r2 | bne bp_done | movs r0,#1
bp_done: | pop {r4,r5} | bx lr
bp_bad: | movs r0,#0 | bx lr''',
'CHECK(bit_palindrome(9,4));CHECK(!bit_palindrome(9,5));CHECK(bit_palindrome(123,0));CHECK(bit_palindrome(0x80000001u,32));CHECK(!bit_palindrome(1,33));',complexity='O(width) time, width<=32')

