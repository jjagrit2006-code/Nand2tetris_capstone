(LOOP)
    @KBD
    D=M
    @CLEAR
    D;JEQ
    @DRAW
    0;JMP

(DRAW)
    @SCREEN
    D=A
    @rowAddr
    M=D

    @91
    D=A
    @k
    M=D

(DRAW_INIT_LOOP)
    @k
    D=M
    @DRAW_ROWS
    D;JEQ
    @32
    D=A
    @rowAddr
    D=D+M
    @rowAddr
    M=D
    @k
    M=M-1
    @DRAW_INIT_LOOP
    0;JMP

(DRAW_ROWS)
    @20
    D=A
    @rowCount
    M=D

(DRAW_ROW_LOOP)
    @rowCount
    D=M
    @LOOP
    D;JEQ

    @rowAddr
    D=M
    @wordAddr
    M=D

    @4
    D=A
    @colCount
    M=D

(DRAW_WORD_LOOP)
    @colCount
    D=M
    @DRAW_NEXT_ROW
    D;JEQ

    @wordAddr
    A=M
    M=-1

    @wordAddr
    M=M+1
    @colCount
    M=M-1
    @DRAW_WORD_LOOP
    0;JMP

(DRAW_NEXT_ROW)
    @32
    D=A
    @rowAddr
    D=D+M
    @rowAddr
    M=D
    @rowCount
    M=M-1
    @DRAW_ROW_LOOP
    0;JMP

(CLEAR)
    @SCREEN
    D=A
    @rowAddr
    M=D

    @91
    D=A
    @k
    M=D

(CLEAR_INIT_LOOP)
    @k
    D=M
    @CLEAR_ROWS
    D;JEQ
    @32
    D=A
    @rowAddr
    D=D+M
    @rowAddr
    M=D
    @k
    M=M-1
    @CLEAR_INIT_LOOP
    0;JMP

(CLEAR_ROWS)
    @20
    D=A
    @rowCount
    M=D

(CLEAR_ROW_LOOP)
    @rowCount
    D=M
    @LOOP
    D;JEQ

    @rowAddr
    D=M
    @wordAddr
    M=D

    @4
    D=A
    @colCount
    M=D

(CLEAR_WORD_LOOP)
    @colCount
    D=M
    @CLEAR_NEXT_ROW
    D;JEQ

    @wordAddr
    A=M
    M=0

    @wordAddr
    M=M+1
    @colCount
    M=M-1
    @CLEAR_WORD_LOOP
    0;JMP

(CLEAR_NEXT_ROW)
    @32
    D=A
    @rowAddr
    D=D+M
    @rowAddr
    M=D
    @rowCount
    M=M-1
    @CLEAR_ROW_LOOP
    0;JMP