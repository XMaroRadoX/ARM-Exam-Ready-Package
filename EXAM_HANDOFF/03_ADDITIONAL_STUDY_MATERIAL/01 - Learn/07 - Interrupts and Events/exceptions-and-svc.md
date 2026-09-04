# Exceptions and SVC

## 1. What Cortex-M3 does automatically

On exception entry Cortex-M3 stacks eight 32-bit words in this exact order:

| Offset | Stacked value |
|---:|---|
| 0 | R0 |
| 4 | R1 |
| 8 | R2 |
| 12 | R3 |
| 16 | R12 |
| 20 | LR |
| 24 | PC |
| 28 | xPSR |

The LR visible inside the handler is not an ordinary return address. It contains `EXC_RETURN`. Bit 2 tells which stack supplied the frame:

- bit 2 = 0: MSP
- bit 2 = 1: PSP

The LPC1768 has no floating-point extension, so this eight-word Cortex-M3 frame is the relevant exam frame.

## 2. Template ownership

The canonical Exam API does not own fault or SVC vectors. The weak handlers in
`startup_LPC17xx.s` remain active until the question supplies a strong handler
from the current project's designated IRQ owner or `Source/ASM_funct.s`. This keeps an exam-required handler
visible and prevents an API helper from hiding the mechanism being tested.

Define each vector exactly once. Do not add both a C and assembly definition of
the same handler.

## 3. Direct fault handling

When a question asks for fault configuration, write the required SCB bits
directly and provide the requested handler. Keep diagnostics deliberately small:
capture only the stacked frame and status registers the question names. A
captured frame is diagnostic; it does not skip or repair the faulting
instruction.

Important limits:

- `BFAR` and `MMFAR` are meaningful only when their valid bits in `CFSR` are set.
- If configurable faults are disabled, related failures may escalate to HardFault.
- `HFSR.FORCED` indicates escalation from another configurable fault.
- Use `volatile` for state written by a handler and inspected by foreground code.

## 4. Direct SVC dispatch

When the paper asks for an SVC handler, decode the immediate from the stacked PC
and pass the frame to a C dispatcher if that interface is allowed:

```asm
SVC_Handler PROC
        TST     LR, #4
        ITE     EQ
        MRSEQ   R0, MSP
        MRSNE   R0, PSP          ; R0 points to stacked frame
        LDR     R1, [R0, #24]    ; stacked PC
        LDRB    R1, [R1, #-2]    ; immediate byte of Thumb SVC
        B       svc_dispatch_c
        ENDP
```

A service returns through the hardware frame. Writing the word at frame offset
zero changes the caller's R0 when exception return restores the context. Keep
the dispatcher contract beside the answer code; it is exam code, not part of
`exam_api.h`.

## 5. Privilege and CONTROL

Thread mode can select PSP and drop to unprivileged execution through `CONTROL`. After writing CONTROL, execute `ISB` so following instructions use the new execution context.

Unprivileged thread code cannot restore itself to privileged mode merely by clearing `CONTROL.nPRIV`; use an exception such as SVC to perform a validated privileged service or to change the saved/control state as the question requires.

Do not confuse:

- `IPSR`: which exception is currently active
- `CONTROL`: thread privilege and stack selection
- `PRIMASK`: global masking of configurable interrupts
- `EXC_RETURN`: exception-return mode and stack selection

## 6. Exam checklist

- Confirm who owns each vector.
- Decode SVC at stacked PC minus 2, not at LR.
- Preserve the eight-word frame layout.
- Treat lower numerical NVIC priority values as higher priority.
- Use W1C writes correctly for peripheral status registers.
- Build every required Keil target after changing preprocessor symbols.
- A successful build is not a hardware test; inspect fault/SVC behavior in the simulator or on the LPC1768 board.
