#include <stdint.h>
uint8_t matrix_get_u8(const uint8_t*a,uint32_t row,uint32_t columns,uint32_t col){return a[row*columns+col];}