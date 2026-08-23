#include <assert.h>
#include <stdint.h>

static uint32_t period_ticks(uint32_t clock_hz, uint32_t period_ms)
{
  return (uint32_t)(((uint64_t)clock_hz * period_ms + 500u) / 1000u);
}
static uint16_t adc_value(uint32_t raw) { return (uint16_t)((raw >> 4) & 0x0FFFu); }
static uint16_t dac_percent(int percent) { return (uint16_t)((percent * 1023 + 50) / 100); }
static uint8_t confirmed(uint32_t low, uint32_t need) { return (uint8_t)(low >= need); }
static uint32_t remember_first(uint32_t saved, uint32_t now) { return saved ? saved : now; }

int main(void)
{
  assert(period_ticks(25000000u, 1000u) == 25000000u);
  assert(period_ticks(25000000u, 10u) == 250000u);
  assert(adc_value(0x0000FFF0u) == 4095u);
  assert(dac_percent(0) == 0u && dac_percent(100) == 1023u);
  assert(!confirmed(4u, 5u) && confirmed(5u, 5u));
  assert(remember_first(0u, 0x10u) == 0x10u);
  assert(remember_first(0x10u, 0x08u) == 0x10u);
  return 0;
}
