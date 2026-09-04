.syntax unified
.cpu cortex-m3
.thumb
        TST LR, #4
        ITE EQ
        MRSEQ R0, MSP
        MRSNE R0, PSP
        LDR R1, [R0, #24]
        LDRB R2, [R1, #-2]
