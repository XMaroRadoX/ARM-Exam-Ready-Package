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
