#include "exam_api.h"
volatile uint32_t svc_result;
void exam_svc_dispatch(uint8_t service_number, exam_exception_frame_t *frame) {
  svc_result=service_number;frame->r0=service_number+1u;
}
extern uint32_t invoke_service(void);
volatile uint32_t returned;
int main(void){exam_init();returned=invoke_service();for (;;) {}}
