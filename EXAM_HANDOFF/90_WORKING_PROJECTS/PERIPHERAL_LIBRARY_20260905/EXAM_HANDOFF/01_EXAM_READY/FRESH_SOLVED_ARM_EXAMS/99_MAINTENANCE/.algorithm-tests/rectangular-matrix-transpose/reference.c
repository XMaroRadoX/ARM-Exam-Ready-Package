#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
#include <stdint.h>
int matrix_transpose(const int*a,size_t r,size_t c,int*out){if(!r||!c)return 1;if(!a||!out||a==out||r>0x3fffffffu/c)return 0;for(size_t i=0;i<r;i++)for(size_t j=0;j<c;j++)out[j*r+i]=a[i*c+j];return 1;}
