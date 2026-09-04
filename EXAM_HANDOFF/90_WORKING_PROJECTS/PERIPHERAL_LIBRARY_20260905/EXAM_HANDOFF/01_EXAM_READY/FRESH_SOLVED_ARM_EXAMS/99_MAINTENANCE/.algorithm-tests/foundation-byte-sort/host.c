#include <stdint.h>
void copyData(const int8_t *source,int8_t *destination,uint32_t length){uint32_t i;for(i=0;i<length;i++)destination[i]=source[i];}
void insertionSort(int8_t *values,uint32_t length){uint32_t i;for(i=1;i<length;i++){int8_t key=values[i];int32_t j=(int32_t)i-1;while(j>=0 && values[j]>key){values[j+1]=values[j];--j;}values[j+1]=key;}}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

void copyData(const int8_t*,int8_t*,uint32_t);
void insertionSort(int8_t*,uint32_t);
int test_main(void){int8_t source[]={127,-128,-1,0},out[5]={0,0,0,0,77};copyData(source,out,4);insertionSort(out,4);CHECK(out[0]==-128 && out[1]==-1 && out[2]==0 && out[3]==127);CHECK(out[4]==77 && source[0]==127);copyData(0,0,0);insertionSort(0,0);return 0;}

int main(void){return test_main();}
