"""Executable callers for the maintained small assembly recipes."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
RECIPES=ROOT/'03_ADDITIONAL_STUDY_MATERIAL/02 - Code Recipes'

def entries():
    result=[]
    def add(slug,path,code,test):
        result.append(dict(slug=slug,code='#include <stdint.h>\n'+code,assembly=(RECIPES/path).read_text(),test='#include <stdint.h>\n'+test,source=str((RECIPES/path).relative_to(ROOT))))
    add('foundation-sum7','02 - Assembly Building Blocks/five_to_seven_arguments.s',
      'uint32_t sum7(uint32_t a,uint32_t b,uint32_t c,uint32_t d,uint32_t e,uint32_t f,uint32_t g){return a+b+c+d+e+f+g;}',
      '''uint32_t sum7(uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,uint32_t);
int test_main(void){CHECK(sum7(1,2,3,4,5,6,7)==28);CHECK(sum7(0,0,0,0,9,10,11)==30);CHECK(sum7(UINT32_MAX,1,0,0,0,0,0)==0);return 0;}''')
    add('foundation-nonleaf','02 - Assembly Building Blocks/nonleaf_function.s',
      'uint32_t add_square(uint32_t a,uint32_t b){return a*a+b;}',
      '''uint32_t add_square(uint32_t,uint32_t);
int test_main(void){CHECK(add_square(3,4)==13);CHECK(add_square(0,7)==7);CHECK(add_square(65536,1)==1);return 0;}''')
    add('foundation-pair','04 - Algorithms/nested_search_with_break.s',
      'int first_equal_pair(const uint32_t*a,const uint32_t*b,uint32_t n,uint32_t m){uint32_t i,j;for(i=0;i<n;i++)for(j=0;j<m;j++)if(a[i]==b[j])return (int)((i<<16)|j);return -1;}',
      '''int first_equal_pair(const uint32_t*,const uint32_t*,uint32_t,uint32_t);
int test_main(void){uint32_t a[]={8,3,5},b[]={2,5,3};CHECK(first_equal_pair(a,b,3,3)==0x10002);CHECK(first_equal_pair(a,b,1,3)==-1);CHECK(first_equal_pair(a,b,0,3)==-1);CHECK(first_equal_pair(a,b,3,0)==-1);return 0;}''')
    add('foundation-q15','05 - Wide and Fixed Point/fixed_point_recurrence.s',
      'int32_t q15_multiply(int32_t a,int32_t b){int64_t x=(int64_t)a*b;return (int32_t)(uint32_t)((uint64_t)x>>15);}',
      '''int32_t q15_multiply(int32_t,int32_t);
int test_main(void){int32_t x=32768;CHECK(q15_multiply(32768,16384)==16384);CHECK(q15_multiply(-32768,16384)==-16384);x=q15_multiply(x,16384);x=q15_multiply(x,16384);CHECK(x==8192);return 0;}''')
    # Classify returns flags; capture them immediately in the assembly wrapper.
    flagasm=(RECIPES/'07 - Interrupts and Exceptions/apsr_flags.s').read_text()
    flagasm=flagasm.rsplit('                END',1)[0]+'''                EXPORT classify_and_read
classify_and_read PROC
                PUSH {R4,LR}
                BL classify_result_flags
                MRS R0,APSR
                POP {R4,PC}
                ENDP
                END
'''
    result.append(dict(slug='foundation-flags',code='#include <stdint.h>\nuint32_t classify_and_read(int32_t x){return x==0?0x40000000u:x<0?0x80000000u:0;}',assembly=flagasm,test='''#include <stdint.h>
uint32_t classify_and_read(int32_t);
int test_main(void){CHECK((classify_and_read(0)&0xF0000000u)==0x40000000u);CHECK((classify_and_read(-1)&0xF0000000u)==0x80000000u);CHECK((classify_and_read(1)&0xF0000000u)==0);return 0;}''',source='03_ADDITIONAL_STUDY_MATERIAL/02 - Code Recipes/07 - Interrupts and Exceptions/apsr_flags.s'))
    add('foundation-word-max','03 - Arrays and Matrices/array_scan_word.s',
      'uint32_t array_max_u32(const uint32_t*a,uint32_t n){uint32_t x=a[0],i;for(i=1;i<n;i++)if(a[i]>x)x=a[i];return x;}',
      '''uint32_t array_max_u32(const uint32_t*,uint32_t);
int test_main(void){uint32_t a[]={0,0x80000000u,7,UINT32_MAX};CHECK(array_max_u32(a,4)==UINT32_MAX);CHECK(array_max_u32(a,1)==0);return 0;}''')
    add('foundation-matrix-byte','03 - Arrays and Matrices/matrix_row_major_byte.s',
      'uint8_t matrix_get_u8(const uint8_t*a,uint32_t row,uint32_t columns,uint32_t col){return a[row*columns+col];}',
      '''uint8_t matrix_get_u8(const uint8_t*,uint32_t,uint32_t,uint32_t);
int test_main(void){uint8_t a[]={0,1,2,128,254,255};CHECK(matrix_get_u8(a,1,3,0)==128);CHECK(matrix_get_u8(a,1,3,2)==255);CHECK(matrix_get_u8(a,0,3,1)==1);return 0;}''')
    unsigned=result[-1]
    result.append(dict(slug='foundation-matrix-signed-byte',code=unsigned['code'].replace('uint8_t','int8_t').replace('matrix_get_u8','matrix_get_i8'),assembly=unsigned['assembly'].replace('LDRB','LDRSB').replace('matrix_get_u8','matrix_get_i8'),test='''#include <stdint.h>
int8_t matrix_get_i8(const int8_t*,uint32_t,uint32_t,uint32_t);
int test_main(void){int8_t a[]={0,1,2,-128,-2,-1};CHECK(matrix_get_i8(a,1,3,0)==-128);CHECK(matrix_get_i8(a,1,3,2)==-1);CHECK(matrix_get_i8(a,0,3,1)==1);return 0;}''',source=unsigned['source']))
    path=ROOT/'03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2023-02-07_Sort_FreeRunning_Timer/Answer Source/assembly.s'
    byte_code='''#include <stdint.h>
void copyData(const int8_t *source,int8_t *destination,uint32_t length){uint32_t i;for(i=0;i<length;i++)destination[i]=source[i];}
void insertionSort(int8_t *values,uint32_t length){uint32_t i;for(i=1;i<length;i++){int8_t key=values[i];int32_t j=(int32_t)i-1;while(j>=0 && values[j]>key){values[j+1]=values[j];--j;}values[j+1]=key;}}
'''
    byte_test='''#include <stdint.h>
void copyData(const int8_t*,int8_t*,uint32_t);
void insertionSort(int8_t*,uint32_t);
int test_main(void){int8_t source[]={127,-128,-1,0},out[5]={0,0,0,0,77};copyData(source,out,4);insertionSort(out,4);CHECK(out[0]==-128 && out[1]==-1 && out[2]==0 && out[3]==127);CHECK(out[4]==77 && source[0]==127);copyData(0,0,0);insertionSort(0,0);return 0;}
'''
    result.append(dict(slug='foundation-byte-sort',code=byte_code,assembly=path.read_text(encoding='utf-8'),test=byte_test,source=str(path.relative_to(ROOT))))
    e=result[-1]
    result.append(dict(slug='foundation-byte-sort-unsigned',code=byte_code.replace('int8_t','uint8_t').replace('insertionSort','insertionSortUnsigned'),assembly=e['assembly'].replace('LDRSB','LDRB').replace('BLE     sort_insert','BLS     sort_insert').replace('insertionSort','insertionSortUnsigned'),test='''#include <stdint.h>
void copyData(const uint8_t*,uint8_t*,uint32_t);
void insertionSortUnsigned(uint8_t*,uint32_t);
int test_main(void){uint8_t source[]={127,128,255,0},out[5]={0,0,0,0,77};copyData(source,out,4);insertionSortUnsigned(out,4);CHECK(out[0]==0 && out[1]==127 && out[2]==128 && out[3]==255);CHECK(out[4]==77 && source[0]==127);insertionSortUnsigned(0,0);return 0;}
''',source=e['source']))
    return result

SVC_MAIN='''#include "exam_api.h"
volatile uint32_t svc_result;
void exam_svc_dispatch(uint8_t service_number, exam_exception_frame_t *frame) {
  svc_result=service_number;frame->r0=service_number+1u;
}
extern uint32_t invoke_service(void);
volatile uint32_t returned;
int main(void){exam_init();returned=invoke_service();for (;;) {}}
'''
SVC_ASM='''        AREA |.text.pattern_svc|, CODE, READONLY
        THUMB
        PRESERVE8
        IMPORT exam_svc_capture_from_exception
        EXPORT SVC_Handler
SVC_Handler PROC
        TST LR,#4
        ITE EQ
        MRSEQ R0,MSP
        MRSNE R0,PSP
        B exam_svc_capture_from_exception
        ENDP
        EXPORT invoke_service
invoke_service PROC
        SVC #7
        BX LR
        ENDP
        END
'''
