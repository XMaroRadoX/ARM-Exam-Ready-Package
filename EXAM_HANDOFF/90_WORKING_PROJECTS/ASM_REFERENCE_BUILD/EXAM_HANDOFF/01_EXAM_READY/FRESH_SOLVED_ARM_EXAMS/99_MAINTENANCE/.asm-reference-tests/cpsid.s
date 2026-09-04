.syntax unified
.cpu cortex-m3
.thumb
        MRS R0, PRIMASK
        CPSID i
        MSR PRIMASK, R0
