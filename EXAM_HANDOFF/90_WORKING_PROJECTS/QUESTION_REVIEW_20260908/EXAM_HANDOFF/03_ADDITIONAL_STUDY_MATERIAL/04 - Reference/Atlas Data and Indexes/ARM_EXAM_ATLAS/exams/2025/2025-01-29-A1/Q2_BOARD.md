# E2025-01-29-A1-Q2

- Delivery: `C + ASM call`
- Tags: `abi:nonleaf`, `board:gpio`, `board:timer`, `risk:irq-shared-state`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-GPIO-EVENT-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-PERIODIC-001`
- Source: `Material (8)\Exams\24-25\2025_01_29\20250129_ARM1.pdf`

## Requirement

Run Timer1 freely with reset at 0xFFFF and no IRQ; INT0 collects bytes and XORs/displays them; KEY1 calls the assembly transform; Timer0 blinks rows with a 0.5-second full period.

## Concepts

free-running timer; no-IRQ reset match; external interrupt; byte buffer; XOR; periodic blink

## Constraints and risks

Timer1 reset at 0xFFFF without IRQ; Timer0 0.5 s full blink period; Match packed-array pointer and size types; keep ISR work bounded.
