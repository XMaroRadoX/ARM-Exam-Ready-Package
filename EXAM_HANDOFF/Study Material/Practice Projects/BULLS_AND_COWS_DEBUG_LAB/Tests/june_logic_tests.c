#include <assert.h>
#include <stdint.h>
#include <stdio.h>

static int reference_bulls_and_cows(const int guess[4], const int secret[4]) {
    int gf[4] = {0, 0, 0, 0};
    int sf[4] = {0, 0, 0, 0};
    int bulls = 0;
    int cows = 0;
    int i;

    for (i = 0; i < 4; ++i) {
        if (guess[i] == secret[i]) ++bulls;
        else {
            ++gf[guess[i]];
            ++sf[secret[i]];
        }
    }
    for (i = 0; i < 4; ++i) cows += gf[i] < sf[i] ? gf[i] : sf[i];
    return (int)((((1u << (uint32_t)bulls) - 1u) << 4) +
                 ((1u << (uint32_t)cows) - 1u));
}

int main(void) {
    const int example_g[4] = {0, 1, 2, 3};
    const int example_s[4] = {1, 2, 2, 0};
    const int exact_g[4] = {0, 1, 2, 3};
    const int exact_s[4] = {0, 1, 2, 3};
    const int none_g[4] = {0, 0, 0, 0};
    const int none_s[4] = {3, 3, 3, 3};
    const int repeated_g[4] = {1, 1, 1, 1};
    const int repeated_s[4] = {1, 2, 2, 2};

    assert(reference_bulls_and_cows(example_g, example_s) == 19);
    assert(reference_bulls_and_cows(exact_g, exact_s) == 0xF0);
    assert(reference_bulls_and_cows(none_g, none_s) == 0x00);
    assert(reference_bulls_and_cows(repeated_g, repeated_s) == 0x10);
    puts("BullsAndCows reference tests passed");
    return 0;
}
