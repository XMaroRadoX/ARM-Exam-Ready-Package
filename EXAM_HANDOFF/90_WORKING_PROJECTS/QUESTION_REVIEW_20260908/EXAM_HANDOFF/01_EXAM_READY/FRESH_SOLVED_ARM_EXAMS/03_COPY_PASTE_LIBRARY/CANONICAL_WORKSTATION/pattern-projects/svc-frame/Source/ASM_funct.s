        AREA |.text.pattern_svc|, CODE, READONLY
        THUMB
        PRESERVE8
        IMPORT exam_svc_capture_from_exception
        EXPORT SVC_Handler
SVC_Handler PROC
        TST LR,#4
        ITE EQ
        MRSEQ R0,MSP
        MRSNE R0,PSP
        B exam_svc_capture_from_exception
        ENDP
        EXPORT invoke_service
invoke_service PROC
        SVC #7
        BX LR
        ENDP
        END
