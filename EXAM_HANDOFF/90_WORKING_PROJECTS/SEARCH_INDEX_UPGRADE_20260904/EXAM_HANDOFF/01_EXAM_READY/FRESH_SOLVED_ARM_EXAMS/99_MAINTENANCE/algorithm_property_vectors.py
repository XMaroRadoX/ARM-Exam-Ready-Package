"""Deterministic independent mathematical vectors beyond the worked examples."""
import math,random,re
def augment(entry):
    slug=entry['slug']
    checks=[]
    def ck(expr):checks.append('CHECK('+expr+');')
    rng=random.Random(9042026)
    words=[0,1,2,9,10,123321,4000000004,4294967295]+[rng.randrange(1<<32) for _ in range(24)]
    scalar={
      'decimal-digit-count':('decimal_digit_count',lambda x:len(str(x))),
      'decimal-digit-product':('decimal_digit_product',lambda x:math.prod(map(int,str(x)))),
      'digital-root':('digital_root',lambda x:0 if not x else 1+(x-1)%9),
      'armstrong-number':('armstrong_number',lambda x:int(sum(int(d)**len(str(x)) for d in str(x))==x)),
      'reverse-32-bits':('reverse_bits',lambda x:int(f'{x:032b}'[::-1],2)),
      'longest-one-bit-run':('longest_one_run',lambda x:max(map(len,re.findall('1+',f'{x:032b}')),default=0)),
      'trailing-zero-count':('trailing_zero_count',lambda x:32 if not x else (x&-x).bit_length()-1),
      'leading-zero-count':('leading_zero_count',lambda x:32-x.bit_length()),
      'pat-alg-popcount-parity-001':('pat_alg_popcount_parity_001',lambda x:x.bit_count()),
      'pat-alg-integer-sqrt-001':('pat_alg_integer_sqrt_001',math.isqrt)
    }
    if slug in scalar:
        name,oracle=scalar[slug]
        for value in words:ck(f'{name}({value}u)=={oracle(value)}u')
    if slug in ('factorial-iterative','factorial-recursive'):
        name=slug.replace('-','_')
        checks.append('uint32_t property_out=77;')
        for n in range(13):ck(f'{name}({n},&property_out)&&property_out=={math.factorial(n)}u')
        ck(f'!{name}(13,&property_out)')
    if slug=='fibonacci-number':
        checks.append('uint32_t property_out=77;')
        a,b=0,1
        for n in range(48):
            ck(f'fibonacci_number({n},&property_out)&&property_out=={a}u');a,b=b,a+b
    if slug=='word-hamming-distance':
        for a,b in zip(words,words[::-1]):ck(f'word_hamming({a}u,{b}u)=={(a^b).bit_count()}u')
    if slug=='bit-width-palindrome':
        for a in words[:12]:
            for width in (0,1,4,8,16,31,32):
                bits=f'{a:032b}'[-width:] if width else ''
                ck(f'bit_palindrome({a}u,{width})=={int(bits==bits[::-1])}')
    if slug=='checked-decimal-reversal':
        checks.append('uint32_t property_out=77;')
        for a in words:
            v=int(str(a)[::-1]);ck(f'reverse_decimal({a}u,&property_out)&&property_out=={v}u' if v<1<<32 else f'!reverse_decimal({a}u,&property_out)')
    sortnames={
      'insertion-sort':'insertion_sort','cocktail-sort':'cocktail_sort','shell-sort':'shell_sort',
      'pat-alg-bubble-sort-001':'pat_alg_bubble_sort_001','pat-alg-selection-sort-001':'pat_alg_selection_sort_001',
      'pat-alg-quicksort-001':'pat_alg_quicksort_001','pat-alg-heap-sort-001':'pat_alg_heap_sort_001'}
    samples=[[],[7],[3,3,3],[2147483647,-2147483648,0],list(range(12)),list(range(12))[::-1]]
    samples += [[rng.randrange(-20,21) for _ in range(n)] for n in (3,5,8,13,20)]
    if slug in sortnames:
        fn=sortnames[slug]
        for a in samples:
            checks.append('{ int32_t property_a[]={'+','.join(map(str,a+[987654]))+'};')
            checks.append(f'{fn}(property_a,{len(a)});')
            for i,v in enumerate(sorted(a)+[987654]):ck(f'property_a[{i}]==({v}LL)')
            checks.append('}')
    if slug=='pat-alg-heap-sort-001':
        checks.append('{ int32_t property_heap[]={1,5,3,4,2,987654}; down(property_heap,5,0);')
        for i,v in enumerate([5,4,3,1,2,987654]):ck(f'property_heap[{i}]=={v}')
        checks.append('}')
    if slug in ('second-largest','second-smallest'):
        fn=slug.replace('-','_')
        for a in samples:
            distinct=sorted(set(a));result=distinct[-2] if slug.endswith('largest') and len(distinct)>1 else distinct[1] if len(distinct)>1 else None
            checks.append('{ int32_t property_a[]={'+','.join(map(str,a+[987654]))+'},property_out=77;')
            ck(f'{fn}(property_a,{len(a)},&property_out)&&property_out==({result}LL)' if result is not None else f'!{fn}(property_a,{len(a)},&property_out)&&property_out==77')
            checks.append('}')
    if slug=='maximum-subarray-sum':
        for a in samples:
            expected=max((sum(a[i:j]) for i in range(len(a)) for j in range(i+1,len(a)+1)),default=0)
            checks.append('{ int32_t property_a[]={'+','.join(map(str,a+[0]))+'};')
            ck(f'maximum_subarray(property_a,{len(a)})==({expected}LL)');checks.append('}')
    if slug=='pat-alg-wide-division-001':
        for a,b in [(-17,5),(-17,-5),(17,-5),(-9223372036854775808,1),(-9223372036854775807,2147483647),(9223372036854775807,-2147483648)]:
            q=abs(a)//abs(b)
            if (a<0)!=(b<0):q=-q
            rem=a-q*b
            av='INT64_MIN' if a==-(1<<63) else f'({a}LL)'
            qv='INT64_MIN' if q==-(1<<63) else f'({q}LL)'
            checks.append('{ int32_t property_rem=77;')
            ck(f'pat_alg_wide_division_001({av},({b}LL),&property_rem)=={qv}&&property_rem==({rem}LL)')
            checks.append('}')
    if not checks:return entry
    test=entry['test']
    match=re.search(r'int test_main\(void\)\s*\{',test)
    if not match:raise ValueError('test_main not found: '+slug)
    # An inner scope prevents collisions with the original worked-example locals.
    test=test[:match.end()]+'\n{\n'+'\n'.join(checks)+'\n}\n'+test[match.end():]
    return {**entry,'test':test,'independent_assertions':sum('CHECK(' in x for x in checks)}
