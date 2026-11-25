// Box.asm  (K = 91)
// start row = K = 91 -> start address = 16384 + 32*91 = 19296
// height = 20 rows ; width = 16*((91 mod 4)+1) = 64 pixels = 4 words
(MAIN)
    @KBD
    D=M
    @BLACK
    D;JNE
    @color
    M=0            // no key -> white
    @DRAW
    0;JMP
(BLACK)
    @color
    M=-1           // key pressed -> black
(DRAW)
    @19296
    D=A
    @addr
    M=D            // addr = first word of row 91
    @20
    D=A
    @rows
    M=D            // rows = 20
(ROW)
    @addr
    D=M
    @p
    M=D            // p = start of current row
    @4
    D=A
    @cols
    M=D            // cols = width in words
(COL)
    @color
    D=M
    @p
    A=M
    M=D            // RAM[p] = color
    @p
    M=M+1
    @cols
    M=M-1
    D=M
    @COL
    D;JGT
    @addr
    D=M
    @32
    D=D+A
    @addr
    M=D            // next row
    @rows
    M=M-1
    D=M
    @ROW
    D;JGT
    @MAIN
    0;JMP
