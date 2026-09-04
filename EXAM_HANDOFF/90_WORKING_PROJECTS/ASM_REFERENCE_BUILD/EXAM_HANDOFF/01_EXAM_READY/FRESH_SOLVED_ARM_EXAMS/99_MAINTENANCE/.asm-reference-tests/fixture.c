#include <stdint.h>
extern uint32_t plus_one(uint32_t),fifth(uint32_t,uint32_t,uint32_t,uint32_t,uint32_t),sum_words(const uint32_t*,uint32_t),nested(uint32_t);
extern int32_t max_signed(int32_t,int32_t),signed_load_case(void);
extern uint32_t carry_case(void),borrow_case(void),wide_case(void),overflow_case(void),shift_case(void),remainder_case(uint32_t,uint32_t);
#define CHECK(x) do {if(!(x))return __LINE__;}while(0)
int test_main(void){
 uint32_t a[]={3,5,7},b[]={0xffffffffu,1};
 CHECK(plus_one(41)==42);CHECK(plus_one(0xffffffffu)==0);CHECK(fifth(1,2,3,4,99)==99);
 CHECK(sum_words(a,3)==15);CHECK(sum_words(a,0)==0);CHECK(sum_words(a,1)==3);CHECK(sum_words(b,2)==0);
 CHECK(max_signed(-1,2)==2);CHECK(max_signed(9,-1)==9);CHECK(max_signed(-7,-7)==-7);CHECK(max_signed(INT32_MIN,INT32_MAX)==INT32_MAX);
 CHECK((carry_case()>>28)==6);CHECK((borrow_case()>>28)==8);CHECK(wide_case()==1);CHECK(signed_load_case()==-2);
 CHECK(nested(41)==42);CHECK(overflow_case()==1);CHECK(shift_case()==0xfffffffeu);
 CHECK(remainder_case(47,10)==7);CHECK(remainder_case(0,10)==0);CHECK(remainder_case(9,10)==9);return 0;
}