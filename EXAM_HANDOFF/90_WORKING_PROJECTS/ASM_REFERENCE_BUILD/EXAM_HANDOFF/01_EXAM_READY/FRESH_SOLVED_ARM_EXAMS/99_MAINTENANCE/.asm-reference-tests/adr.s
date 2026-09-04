.syntax unified
.cpu cortex-m3
.thumb
        ADR R0, local_data
        B after_data
.balign 4
local_data:
.word 27
after_data:
