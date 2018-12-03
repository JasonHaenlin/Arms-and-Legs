def bin16(n):
    """
        Converts an 16-bits int to it's 16-bits binary form
        Built-in bin function removes exceeding '0' at the
        left of the result
    """
    return ''.join(str(1 & int(n) >> i) for i in range(16)[::-1])

def putByte(byte, maxrank, minrank, value):
    """
        Manipulates bits in a given 16-bits int
        Writes value starting at rank minrank
        and finishing at maxrank

        putByte(128, 6, 3, 5) outputs 184
        128: 0000000010000000
        5:   0000000000000101
        184: 0000000010101000
    """
    if type(value) == str:
        value = value.replace("#", "").replace("r", "").replace("R", "")
    value = int(value)

    mask = value * 2**minrank
    i=15
    while i>maxrank:
        if bin16(mask)[15-i] == "1":        
            mask -= 2**i
        i-=1
    i=0
    newbyte = 0
    byte16 = bin16(byte)
    mask16 = bin16(mask)
    while i<=15:
        if byte16[i] == "1" or mask16[i] == "1":
            newbyte += 2**(15-i)
        i+=1
    return newbyte

def LSLSimm(rd, rm, imm5):
    """
        function: immediate logical left shift
        assembly: LSLS rd, rm, #imm5
        binary: 000 00 imm5 rm rd
    """
    byte = 0
    byte = putByte(byte, 10, 6, imm5)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rd)
    return byte

def LSRSimm(rd, rm, imm5):
    """
        function: immediate logical right shift
        assembly: LSRS rd, rm, #imm5
        binary: 000 01 imm5 rm rd
    """
    byte = 0
    byte = putByte(byte, 12, 11, 1)
    byte = putByte(byte, 10, 6, imm5)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rd)
    return byte

def ASRSimm(rd, rm, imm5):
    """
        function: immediate arithmetic shift right
        assembly: ASRS rd, rm, #imm5
        binary: 000 10 imm5 rm rd
    """
    byte = 0
    byte = putByte(byte, 12, 11, 2)
    byte = putByte(byte, 10, 6, imm5)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rd)
    return yte

def ADDS(rd, rn, rm):
    """
        function: add register
        assembly: ADDS rd, rn, rm
        binary: 000 11 00 rm rn rd
    """
    byte = 0
    byte = putByte(byte, 12, 11, 3)
    byte = putByte(byte, 8, 6, rm)
    byte = putByte(byte, 5, 3, rn)
    byte = putByte(byte, 2, 0, rd)
    return byte

def SUBS(rd, rn, rm):
    """
        function: substract register
        assembly: SUBS rd, rn, rm
        binary: 000 11 01 rm rn rd
    """
    byte = 0
    byte = putByte(byte, 12, 11, 3)
    byte = putByte(byte, 9, 9, 1)
    byte = putByte(byte, 8, 6, rm)
    byte = putByte(byte, 5, 3, rn)
    byte = putByte(byte, 2, 0, rd)
    return byte

def ADDSimm(rd, rn, imm3):
    """
        function: add 3-bits immediate
        assembly: ADDS rd, rn, #imm3
        binary: 000 11 10 imm3 rn rd
    """
    byte = 0
    byte = putByte(byte, 12, 11, 3)
    byte = putByte(byte, 10, 10, 1)    
    byte = putByte(byte, 8, 6, imm3)
    byte = putByte(byte, 5, 3, rn)
    byte = putByte(byte, 2, 0, rd)
    return byte

def SUBSimm(rd, rn, imm3):
    """
        function: substract 3-bits immediate
        assembly: SUBS rd, rn, #imm
        binary: 000 11 11 imm3 rn rd
    """
    byte = 0
    byte = putByte(byte, 12, 9, 15)
    byte = putByte(byte, 10, 10, 1)
    byte = putByte(byte, 9, 9, 1) 
    byte = putByte(byte, 8, 6, imm3)
    byte = putByte(byte, 5, 3, rn)
    byte = putByte(byte, 2, 0, rd)
    return byte

def MOVSimm(rd, imm8):
    """
        function: move
        assembly: MOVS rd, #imm8
        binary: 001 00 rd imm8
    """
    byte = 0
    byte = putByte(byte, 15, 13, 1)
    byte = putByte(byte, 10, 8, rd)
    byte = putByte(byte, 7, 0, imm8)
    return byte

def ANDS(rdn, rm):
    """
        function: bitwise and
        assembly: ANDS rdn, rm
        binary: 010000 0000 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def EORS(rdn,rm):
    """
        function: exclusive or
        assembly: EORS rdn, rm
        binary: 010000 0001 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 1)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def LSLS(rdn, rm):
    """
        function: logical shift left
        assembly: LSLS rdn, rm
        binary: 010000 0010 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 2)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def LSRS(rdn, rm):
    """
        function: logical shift right
        assembly: LSRS rdn, rm
        binary: 010000 0011 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 3)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def ASRS(rdn, rm):
    """
        function: arithmetic shift right
        assembly: ASRS rdn, rm
        binary: 010000 0100 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 4)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def ADCS(rdn, rm):
    """
        function: add with carry
        assembly: ADCS rdn, rm
        binary: 010000 0101 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 5)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def SBCS(rdn, rm):
    """
        function: substract with carry
        assembly: SBCS rdn, rm
        binary: 010000 0110 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 6)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def RORS(rdn, rm):
    """
        function: rotate right
        assembly: RORS rdn, rm
        binary: 010000 0111 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 7)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def TST(rdn, rm):
    """
        function: set flags on bitwise and
        assembly: TST rdn, rm
        binary: 010000 1000 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 8)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def RSBS(rdn, rm):
    """
        function: immediate reverse substract from 0
        assembly: RSBS rdn, rm
        binary: 010000 1001 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 9)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def CMP(rdn, rm):
    """
        function: compare registers
        assembly: CMP rdn, rm
        binary: 010000 1010 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 10)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def CMN(rdn, rm):
    """
        function: compare negative
        assembly: CMN rdn, rm
        binary: 010000 1011 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 11)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def ORRS(rdn, rm):
    """
        function: logical or
        assembly: ORRS rdn, rm
        binary: 010000 1100 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 12)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def MULS(rdm, rm):
    """
        function: multiply two registers
        assembly: MULS rdn, rm
        binary: 010000 1101 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 13)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def BICS(rdn, rm):
    """
        function: bit clear
        assembly: BICS rdn, rm
        binary: 010000 1110 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 14)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def MVNS(rdn, rm):
    """
        function: bitwise not
        assembly: MVNS rdn, rm
        binary: 010000 1111 rm rdn
    """
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 15)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def STR(rt, imm8):
    """
        function: immediate store register
        assembly: STR rt, [SP, #imm8]
        binary: 1001 0 rt imm8
    """
    byte = 0
    byte = putByte(byte, 15, 12, 9)
    byte = putByte(byte, 10, 8, rt)
    byte = putByte(byte, 7, 0, imm8)
    return byte

def LDR(rt, imm8):
    """
        function: load register
        assembly: LDR rt, [SP, #imm8]
        binary: 1001 1 rt imm8
    """
    byte = 0
    byte = putByte(byte, 15, 12, 9)
    byte = putByte(byte, 11, 11, 1)
    byte = putByte(byte, 10, 8, rt)
    byte = putByte(byte, 7, 0, imm8)
    return byte

def ADDspimm(imm7):
    """
        function: add immediate to sp
        assembly: ADD [SP,] SP, #imm7
        binary: 1011 0000 0 imm7
    """
    byte = 0
    byte = putByte(byte, 15, 12, 11)
    byte = putByte(byte, 6, 0, imm7)
    return byte

def SUBspimm(imm7):
    """
        function: substract immediate to sp
        assembly: SUBS [SP,] SP, #imm7
        binary: 1011 0000 1 imm7
    """
    byte = 0
    byte = putByte(byte, 15, 12, 11)
    byte = putByte(byte, 7, 7, 1)
    byte = putByte(byte, 6, 0, imm7)
    return byte

def B(c, label):
    """
        function: conditionnal branch
        assembly: Bc label
        binary: 1101 c imm8
    """
    byte = 0
    byte = putByte(byte, 15, 12, 13)
    byte = putByte(byte, 11, 8, c)
    byte = putByte(byte, 7, 0, label)
    return byte
