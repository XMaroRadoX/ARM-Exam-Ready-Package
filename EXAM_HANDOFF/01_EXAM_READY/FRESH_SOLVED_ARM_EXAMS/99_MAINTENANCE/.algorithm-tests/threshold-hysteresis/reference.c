#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stdint.h>
#include <stddef.h>
#include <limits.h>
#include <stdint.h>
int hysteresis_update(uint16_t sample,uint16_t low,uint16_t high,uint8_t*state){if(state==0||low>=high)return 0;if(*state==0u&&sample>=high)*state=1u;else if(*state!=0u&&sample<=low)*state=0u;return 1;}
