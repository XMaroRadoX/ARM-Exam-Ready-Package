#include <stdint.h>
#include "LPC17xx.h"
#include "exam_api.h"

extern const uint8_t matrix[8];
extern uint8_t matrix_T[8];
extern void transpose(const uint8_t *source, uint8_t *destination);

int main(void)
{
    exam_init();
    transpose(matrix, matrix_T);
    /* Watch matrix_T: 8F C7 E3 F1 F8 7C 3E 1F. */
    for (;;) {
        __WFI();
    }
}
