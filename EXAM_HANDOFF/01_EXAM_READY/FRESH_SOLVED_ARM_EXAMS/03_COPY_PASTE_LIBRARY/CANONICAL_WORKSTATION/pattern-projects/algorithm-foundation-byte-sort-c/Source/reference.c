#include <stdint.h>
void copyData(const int8_t *source,int8_t *destination,uint32_t length){uint32_t i;for(i=0;i<length;i++)destination[i]=source[i];}
void insertionSort(int8_t *values,uint32_t length){uint32_t i;for(i=1;i<length;i++){int8_t key=values[i];int32_t j=(int32_t)i-1;while(j>=0 && values[j]>key){values[j+1]=values[j];--j;}values[j+1]=key;}}
