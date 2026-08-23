#include "exam_board.h"

volatile fault_snapshot_t fault_snapshot;
volatile uint8_t fault_snapshot_valid;

void fault_traps_configure(void)
{
#if CA_TRAP_DIVIDE_BY_ZERO
  SCB->CCR |= SCB_CCR_DIV_0_TRP_Msk;
#else
  SCB->CCR &= ~SCB_CCR_DIV_0_TRP_Msk;
#endif
#if CA_TRAP_UNALIGNED
  SCB->CCR |= SCB_CCR_UNALIGN_TRP_Msk;
#else
  SCB->CCR &= ~SCB_CCR_UNALIGN_TRP_Msk;
#endif
#if CA_ENABLE_CONFIGURABLE_FAULTS
  SCB->SHCSR |= SCB_SHCSR_USGFAULTENA_Msk |
                SCB_SHCSR_BUSFAULTENA_Msk |
                SCB_SHCSR_MEMFAULTENA_Msk;
#endif
}

void fault_capture_from_exception(uint32_t *stack, uint32_t exc_return)
{
  fault_snapshot.exception_number = SCB->ICSR & SCB_ICSR_VECTACTIVE_Msk;
  fault_snapshot.exc_return = exc_return;
  fault_snapshot.r0 = stack[0];
  fault_snapshot.r1 = stack[1];
  fault_snapshot.r2 = stack[2];
  fault_snapshot.r3 = stack[3];
  fault_snapshot.r12 = stack[4];
  fault_snapshot.lr = stack[5];
  fault_snapshot.pc = stack[6];
  fault_snapshot.xpsr = stack[7];
  fault_snapshot.cfsr = SCB->CFSR;
  fault_snapshot.hfsr = SCB->HFSR;
  fault_snapshot.bfar = SCB->BFAR;
  fault_snapshot.mmfar = SCB->MMFAR;
  fault_snapshot_valid = 1u;
#ifdef SIMULATOR
  __BKPT(0);
#endif
  for (;;) { __NOP(); }
}

#define FAULT_WRAPPER(name) \
  __attribute__((naked)) void name(void) { \
    __asm volatile( \
      "tst lr, #4\n" \
      "ite eq\n" \
      "mrseq r0, msp\n" \
      "mrsne r0, psp\n" \
      "mov r1, lr\n" \
      "b fault_capture_from_exception\n"); \
  }

FAULT_WRAPPER(HardFault_Handler)
FAULT_WRAPPER(MemManage_Handler)
FAULT_WRAPPER(BusFault_Handler)
FAULT_WRAPPER(UsageFault_Handler)

void __attribute__((weak)) svc_dispatch(uint8_t service_number, svc_context_t *context)
{
  (void)service_number;
  (void)context;
}

void svc_capture_from_exception(svc_context_t *stack)
{
  uint8_t service_number = ((const uint8_t *)(uintptr_t)stack->pc)[-2];
  svc_dispatch(service_number, stack);
}

#if !EXAM_OWN_SVC_HANDLER
__attribute__((naked)) void SVC_Handler(void)
{
  __asm volatile(
    "tst lr, #4\n"
    "ite eq\n"
    "mrseq r0, msp\n"
    "mrsne r0, psp\n"
    "b svc_capture_from_exception\n");
}
#endif
