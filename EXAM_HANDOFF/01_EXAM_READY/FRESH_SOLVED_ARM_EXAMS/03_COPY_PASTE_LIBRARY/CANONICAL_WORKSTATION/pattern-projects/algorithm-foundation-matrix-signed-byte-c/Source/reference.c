#include <stdint.h>
int8_t matrix_get_i8(const int8_t*a,uint32_t row,uint32_t columns,uint32_t col){return a[row*columns+col];}