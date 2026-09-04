.syntax unified
.cpu cortex-m3
.thumb
.text
.global plus_one
plus_one:
        ADDS R0, R0, #1
        BX LR
