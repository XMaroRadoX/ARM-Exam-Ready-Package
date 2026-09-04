#include <stdint.h>
#include <stddef.h>
#include <limits.h>
uint32_t unique_unsorted(int32_t*a,uint32_t n){uint32_t k=0;if(a)for(uint32_t i=0;i<n;i++){uint32_t j=0;while(j<k&&a[j]!=a[i])j++;if(j==k)a[k++]=a[i];}return k;}
