#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
int second_largest(const int32_t *a, uint32_t n, int32_t *out);
int test_main(void) {
{
{ int32_t property_a[]={987654},property_out=77;
CHECK(!second_largest(property_a,0,&property_out)&&property_out==77);
}
{ int32_t property_a[]={7,987654},property_out=77;
CHECK(!second_largest(property_a,1,&property_out)&&property_out==77);
}
{ int32_t property_a[]={3,3,3,987654},property_out=77;
CHECK(!second_largest(property_a,3,&property_out)&&property_out==77);
}
{ int32_t property_a[]={2147483647,-2147483648,0,987654},property_out=77;
CHECK(second_largest(property_a,3,&property_out)&&property_out==(0LL));
}
{ int32_t property_a[]={0,1,2,3,4,5,6,7,8,9,10,11,987654},property_out=77;
CHECK(second_largest(property_a,12,&property_out)&&property_out==(10LL));
}
{ int32_t property_a[]={11,10,9,8,7,6,5,4,3,2,1,0,987654},property_out=77;
CHECK(second_largest(property_a,12,&property_out)&&property_out==(10LL));
}
{ int32_t property_a[]={-19,1,-1,987654},property_out=77;
CHECK(second_largest(property_a,3,&property_out)&&property_out==(-1LL));
}
{ int32_t property_a[]={-16,-8,-10,-19,14,987654},property_out=77;
CHECK(second_largest(property_a,5,&property_out)&&property_out==(-8LL));
}
{ int32_t property_a[]={-2,-16,-16,20,20,9,6,15,987654},property_out=77;
CHECK(second_largest(property_a,8,&property_out)&&property_out==(15LL));
}
{ int32_t property_a[]={-18,-6,9,-5,17,-3,3,7,17,17,12,-11,-20,987654},property_out=77;
CHECK(second_largest(property_a,13,&property_out)&&property_out==(12LL));
}
{ int32_t property_a[]={-1,-8,-10,-5,-14,-14,-7,11,6,-11,2,12,-10,11,-14,16,17,-13,18,-9,987654},property_out=77;
CHECK(second_largest(property_a,20,&property_out)&&property_out==(17LL));
}
}

int32_t a[]={4,9,9,2},e[]={INT32_MIN,INT32_MAX},v=77;CHECK(second_largest(a,4,&v)&&v==4);CHECK(second_largest(e,2,&v)&&v==INT32_MIN);v=77;CHECK(!second_largest(a,1,&v)&&v==77);CHECK(!second_largest(0,0,&v));
return 0;
}
