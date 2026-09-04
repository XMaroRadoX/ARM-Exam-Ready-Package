.syntax unified
.cpu cortex-m3
.thumb
        CMP R0, #0
        IT NE
        ADDNE.W R1, R1, #1
