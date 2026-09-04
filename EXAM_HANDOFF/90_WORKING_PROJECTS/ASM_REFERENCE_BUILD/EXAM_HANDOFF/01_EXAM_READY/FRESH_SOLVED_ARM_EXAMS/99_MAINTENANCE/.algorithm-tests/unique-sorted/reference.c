#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t unique_sorted(int32_t*a,uint32_t n){uint32_t k=0;if(a)for(uint32_t i=0;i<n;i++){if(!k||a[i]!=a[k-1])a[k++]=a[i];}return k;}
