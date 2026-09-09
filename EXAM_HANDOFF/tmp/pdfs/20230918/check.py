def digit_sum(a):
    total = 0
    while a:
        a, digit = divmod(a, 10)
        total += digit
    return total

def series(a, n):
    values = [a]
    total = 0
    for i in range(n):
        total += digit_sum(a)
        if i == n - 1:
            return values, total
        a += digit_sum(a)
        if a > 0xffffffff:
            return values, 0
        values.append(a)

assert digit_sum(4294967295) == 57
assert series(47, 5) == ([47, 58, 71, 79, 95], 62)
assert series(47, 1) == ([47], 11)
assert series(4294967295, 2) == ([4294967295], 0)
assert series(0, 10) == ([0] * 10, 0)
for a in range(1, 1000):
    values, total = series(a, 50)
    assert total == values[-1] - values[0] + digit_sum(values[-1])
k = 0
for bit in (1, 0, 0, 1, 1, 0):
    k = (k << 1) | bit
assert k == 38
print('Arithmetic and boundary checks passed; 999 formula cases.')
print('K=38:', series(k, 10))
