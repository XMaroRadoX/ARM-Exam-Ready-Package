#ifndef EXAM_USER_H
#define EXAM_USER_H

#include "exam_api.h"
#include "exam_compat.h"

void exam_user_init(void);
void exam_user_loop(void);
void exam_user_10ms_hook(void);

/* Default assembly sanity routine. Replace this prototype and the matching
 * EXPORT in exam_asm.s with the exact signature required by the paper. */
uint32_t exam_asm_solution(uint32_t value);

#endif
