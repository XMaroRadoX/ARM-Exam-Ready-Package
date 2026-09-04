#include "exam_api.h"

void RIT_IRQHandler(void) { exam_rit_ack(); exam_debounce_tick(); }
