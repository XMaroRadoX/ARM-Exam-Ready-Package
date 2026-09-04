#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stddef.h>
void cocktail_sort(int *a, size_t n) {
  size_t lo = 0u, hi = n;
  int changed = 1;
  if (a == NULL) return;
  while (changed && hi > lo + 1u) {
    size_t i;
    changed = 0;
    for (i = lo + 1u; i < hi; ++i) if (a[i - 1u] > a[i]) { int t=a[i-1u]; a[i-1u]=a[i]; a[i]=t; changed=1; }
    if (!changed) break;
    --hi; changed = 0;
    for (i = hi - 1u; i > lo; --i) if (a[i - 1u] > a[i]) { int t=a[i-1u]; a[i-1u]=a[i]; a[i]=t; changed=1; }
    ++lo;
  }
}

#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)

#include <stddef.h>
#include <limits.h>
void cocktail_sort(int *a, size_t n);
int test_main(void) {
{
{ int32_t property_a[]={987654};
cocktail_sort(property_a,0);
CHECK(property_a[0]==(987654LL));
}
{ int32_t property_a[]={7,987654};
cocktail_sort(property_a,1);
CHECK(property_a[0]==(7LL));
CHECK(property_a[1]==(987654LL));
}
{ int32_t property_a[]={3,3,3,987654};
cocktail_sort(property_a,3);
CHECK(property_a[0]==(3LL));
CHECK(property_a[1]==(3LL));
CHECK(property_a[2]==(3LL));
CHECK(property_a[3]==(987654LL));
}
{ int32_t property_a[]={2147483647,-2147483648,0,987654};
cocktail_sort(property_a,3);
CHECK(property_a[0]==(-2147483648LL));
CHECK(property_a[1]==(0LL));
CHECK(property_a[2]==(2147483647LL));
CHECK(property_a[3]==(987654LL));
}
{ int32_t property_a[]={0,1,2,3,4,5,6,7,8,9,10,11,987654};
cocktail_sort(property_a,12);
CHECK(property_a[0]==(0LL));
CHECK(property_a[1]==(1LL));
CHECK(property_a[2]==(2LL));
CHECK(property_a[3]==(3LL));
CHECK(property_a[4]==(4LL));
CHECK(property_a[5]==(5LL));
CHECK(property_a[6]==(6LL));
CHECK(property_a[7]==(7LL));
CHECK(property_a[8]==(8LL));
CHECK(property_a[9]==(9LL));
CHECK(property_a[10]==(10LL));
CHECK(property_a[11]==(11LL));
CHECK(property_a[12]==(987654LL));
}
{ int32_t property_a[]={11,10,9,8,7,6,5,4,3,2,1,0,987654};
cocktail_sort(property_a,12);
CHECK(property_a[0]==(0LL));
CHECK(property_a[1]==(1LL));
CHECK(property_a[2]==(2LL));
CHECK(property_a[3]==(3LL));
CHECK(property_a[4]==(4LL));
CHECK(property_a[5]==(5LL));
CHECK(property_a[6]==(6LL));
CHECK(property_a[7]==(7LL));
CHECK(property_a[8]==(8LL));
CHECK(property_a[9]==(9LL));
CHECK(property_a[10]==(10LL));
CHECK(property_a[11]==(11LL));
CHECK(property_a[12]==(987654LL));
}
{ int32_t property_a[]={-19,1,-1,987654};
cocktail_sort(property_a,3);
CHECK(property_a[0]==(-19LL));
CHECK(property_a[1]==(-1LL));
CHECK(property_a[2]==(1LL));
CHECK(property_a[3]==(987654LL));
}
{ int32_t property_a[]={-16,-8,-10,-19,14,987654};
cocktail_sort(property_a,5);
CHECK(property_a[0]==(-19LL));
CHECK(property_a[1]==(-16LL));
CHECK(property_a[2]==(-10LL));
CHECK(property_a[3]==(-8LL));
CHECK(property_a[4]==(14LL));
CHECK(property_a[5]==(987654LL));
}
{ int32_t property_a[]={-2,-16,-16,20,20,9,6,15,987654};
cocktail_sort(property_a,8);
CHECK(property_a[0]==(-16LL));
CHECK(property_a[1]==(-16LL));
CHECK(property_a[2]==(-2LL));
CHECK(property_a[3]==(6LL));
CHECK(property_a[4]==(9LL));
CHECK(property_a[5]==(15LL));
CHECK(property_a[6]==(20LL));
CHECK(property_a[7]==(20LL));
CHECK(property_a[8]==(987654LL));
}
{ int32_t property_a[]={-18,-6,9,-5,17,-3,3,7,17,17,12,-11,-20,987654};
cocktail_sort(property_a,13);
CHECK(property_a[0]==(-20LL));
CHECK(property_a[1]==(-18LL));
CHECK(property_a[2]==(-11LL));
CHECK(property_a[3]==(-6LL));
CHECK(property_a[4]==(-5LL));
CHECK(property_a[5]==(-3LL));
CHECK(property_a[6]==(3LL));
CHECK(property_a[7]==(7LL));
CHECK(property_a[8]==(9LL));
CHECK(property_a[9]==(12LL));
CHECK(property_a[10]==(17LL));
CHECK(property_a[11]==(17LL));
CHECK(property_a[12]==(17LL));
CHECK(property_a[13]==(987654LL));
}
{ int32_t property_a[]={-1,-8,-10,-5,-14,-14,-7,11,6,-11,2,12,-10,11,-14,16,17,-13,18,-9,987654};
cocktail_sort(property_a,20);
CHECK(property_a[0]==(-14LL));
CHECK(property_a[1]==(-14LL));
CHECK(property_a[2]==(-14LL));
CHECK(property_a[3]==(-13LL));
CHECK(property_a[4]==(-11LL));
CHECK(property_a[5]==(-10LL));
CHECK(property_a[6]==(-10LL));
CHECK(property_a[7]==(-9LL));
CHECK(property_a[8]==(-8LL));
CHECK(property_a[9]==(-7LL));
CHECK(property_a[10]==(-5LL));
CHECK(property_a[11]==(-1LL));
CHECK(property_a[12]==(2LL));
CHECK(property_a[13]==(6LL));
CHECK(property_a[14]==(11LL));
CHECK(property_a[15]==(11LL));
CHECK(property_a[16]==(12LL));
CHECK(property_a[17]==(16LL));
CHECK(property_a[18]==(17LL));
CHECK(property_a[19]==(18LL));
CHECK(property_a[20]==(987654LL));
}
}

int a[]={3,2,1,INT_MIN,INT_MAX,2};cocktail_sort(a,6);for(int i=1;i<6;i++)CHECK(a[i-1]<=a[i]);CHECK(a[0]==INT_MIN&&a[5]==INT_MAX);cocktail_sort(0,0);
return 0;
}

int main(void){return test_main();}
