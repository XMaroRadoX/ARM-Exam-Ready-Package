.syntax unified
.cpu cortex-m3
.thumb
max_signed:
        CMP R0, R1
        BGE max_done
        MOV R0, R1
max_done:
        BX LR
