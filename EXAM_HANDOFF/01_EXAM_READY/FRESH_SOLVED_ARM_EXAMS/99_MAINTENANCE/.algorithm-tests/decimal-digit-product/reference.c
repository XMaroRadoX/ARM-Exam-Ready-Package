#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t decimal_digit_product(uint32_t n){uint32_t v=1;do{uint32_t d=n%10;(void)d;v*=d;n/=10;}while(n);return v;}
