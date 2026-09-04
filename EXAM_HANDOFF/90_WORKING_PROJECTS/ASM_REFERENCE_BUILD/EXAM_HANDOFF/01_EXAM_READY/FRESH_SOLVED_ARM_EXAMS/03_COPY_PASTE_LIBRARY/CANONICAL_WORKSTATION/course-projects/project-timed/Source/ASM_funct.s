        AREA |.text.course_sum|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT sum_words
sum_words PROC
        MOV R2, #0
        MOV R3, #0
next    CMP R2, R1
        BHS done
        LDR R12, [R0, R2, LSL #2]
        ADD R3, R3, R12
        ADD R2, R2, #1
        B next
done    MOV R0, R3
        BX LR
        ENDP
        END
