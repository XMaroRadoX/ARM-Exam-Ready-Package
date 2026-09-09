"""Check the paper's arithmetic and state sequence; not hardware execution."""
import json
import struct
from pathlib import Path


def trunc_div(numerator, denominator):
    return (-1 if numerator < 0 else 1) * (abs(numerator) // denominator)


def maclaurin(y, n):
    term = total = 10 * y
    terms = [term]
    for i in range(1, n + 1):
        numerator = -term * y * y
        denominator = (2 * i) * (2 * i + 1) * 100
        assert -(2**31) <= numerator < 2**31
        term = trunc_div(numerator, denominator)
        total += term
        terms.append(term)
    return total, terms


def f32(value):
    return struct.unpack('f', struct.pack('f', value))[0]


def sample(ticks):
    scaled = f32(f32(1.428) * ticks)
    y = int(f32(scaled + (0.5 if scaled >= 0 else -0.5)))
    # Verify the float implementation agrees with the paper's decimal rule.
    exact_numerator = 1428 * ticks
    exact_y = trunc_div(exact_numerator + (500 if ticks >= 0 else -500), 1000)
    assert y == exact_y
    result, _ = maclaurin(y, 3)
    output = 500 + trunc_div(result, 2)
    assert 0 <= output <= 1023
    assert (output << 6) >> 6 == output
    return y, result, output


def main():
    assert maclaurin(20, 3) == (91, [200, -133, 26, -2])
    for n, expected in enumerate([200, 67, 93, 91]):
        assert maclaurin(20, n)[0] == expected
        assert maclaurin(-20, n)[0] == -expected
        assert maclaurin(0, n)[0] == 0

    rows = [dict(ticks=t, input=sample(t)[0], maclaurin=sample(t)[1],
                 output=sample(t)[2], index=t + 22) for t in range(-22, 23)]
    ticks = repeat = writes = 0
    values = [None] * 45
    first_indexes = []
    while repeat < 200:
        index = ticks + 22
        assert 0 <= index < 45
        values[index] = sample(ticks)[2]
        if repeat == 0:
            first_indexes.append(index)
        writes += 1
        ticks += 1
        if ticks > 22:
            ticks = -22
            repeat += 1

    assert first_indexes == list(range(22, 45))
    assert writes == 23 + 199 * 45 == 8978
    assert values == [r['output'] for r in rows]
    assert ticks == -22 and repeat == 200
    report = dict(status='PASS', scope='Reference arithmetic/state model, not ARM execution',
                  sample_rate_hz=25000000 / 1263,
                  waveform_frequency_hz=25000000 / (1263 * 45),
                  computed_sample_writes=writes, first_zero_interrupt=writes + 1,
                  output_range=[min(values), max(values)], samples=rows)
    Path(__file__).with_name('math_check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'samples'}, indent=2))


if __name__ == '__main__':
    main()
