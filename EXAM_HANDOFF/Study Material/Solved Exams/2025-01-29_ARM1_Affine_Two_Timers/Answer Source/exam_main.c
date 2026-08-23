/* Internal connection file. Normal answers belong in exam_user.c. */
#include "exam_user.h"

int main(void)
{
  exam_init();
  exam_user_init();

  for (;;) {
    exam_user_loop();
    exam_idle();
  }
}
