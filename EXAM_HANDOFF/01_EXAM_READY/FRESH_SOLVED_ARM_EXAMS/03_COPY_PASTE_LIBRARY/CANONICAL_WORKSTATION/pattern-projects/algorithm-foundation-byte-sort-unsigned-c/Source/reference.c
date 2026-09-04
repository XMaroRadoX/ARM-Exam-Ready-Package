#include <stdint.h>
void copyData(const uint8_t *source,uint8_t *destination,uint32_t length){uint32_t i;for(i=0;i<length;i++)destination[i]=source[i];}
void insertionSortUnsigned(uint8_t *values,uint32_t length){uint32_t i;for(i=1;i<length;i++){uint8_t key=values[i];int32_t j=(int32_t)i-1;while(j>=0 && values[j]>key){values[j+1]=values[j];--j;}values[j+1]=key;}}
