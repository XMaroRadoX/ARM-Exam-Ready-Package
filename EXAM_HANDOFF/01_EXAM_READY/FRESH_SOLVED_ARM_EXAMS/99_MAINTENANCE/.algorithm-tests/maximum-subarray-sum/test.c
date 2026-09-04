#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int64_t maximum_subarray(const int32_t *a, uint32_t n);
int test_main(void) {
{
{ int32_t property_a[]={0};
CHECK(maximum_subarray(property_a,0)==(0LL));
}
{ int32_t property_a[]={7,0};
CHECK(maximum_subarray(property_a,1)==(7LL));
}
{ int32_t property_a[]={3,3,3,0};
CHECK(maximum_subarray(property_a,3)==(9LL));
}
{ int32_t property_a[]={2147483647,-2147483648,0,0};
CHECK(maximum_subarray(property_a,3)==(2147483647LL));
}
{ int32_t property_a[]={0,1,2,3,4,5,6,7,8,9,10,11,0};
CHECK(maximum_subarray(property_a,12)==(66LL));
}
{ int32_t property_a[]={11,10,9,8,7,6,5,4,3,2,1,0,0};
CHECK(maximum_subarray(property_a,12)==(66LL));
}
{ int32_t property_a[]={-19,1,-1,0};
CHECK(maximum_subarray(property_a,3)==(1LL));
}
{ int32_t property_a[]={-16,-8,-10,-19,14,0};
CHECK(maximum_subarray(property_a,5)==(14LL));
}
{ int32_t property_a[]={-2,-16,-16,20,20,9,6,15,0};
CHECK(maximum_subarray(property_a,8)==(70LL));
}
{ int32_t property_a[]={-18,-6,9,-5,17,-3,3,7,17,17,12,-11,-20,0};
CHECK(maximum_subarray(property_a,13)==(74LL));
}
{ int32_t property_a[]={-1,-8,-10,-5,-14,-14,-7,11,6,-11,2,12,-10,11,-14,16,17,-13,18,-9,0};
CHECK(maximum_subarray(property_a,20)==(45LL));
}
}

int32_t a[]={-2,3,-1,4,-8},b[]={-9,-2,-7},c[]={INT32_MAX,INT32_MAX};CHECK(maximum_subarray(a,5)==6);CHECK(maximum_subarray(b,3)==-2);CHECK(maximum_subarray(c,2)==4294967294LL);CHECK(maximum_subarray(0,0)==0);
return 0;
}
