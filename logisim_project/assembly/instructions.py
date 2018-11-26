def bin16(n):
    return ''.join(str(1 & int(n) >> i) for i in range(16)[::-1])

def putByte(byte, maxrank, minrank, value):
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
    byte = 0
    byte = putByte(byte, 10, 6, imm5)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rd)
    return byte

def LSRSimm(rd, rm, imm5):
    byte = 0
    byte = putByte(byte, 12, 11, 1)
    byte = putByte(byte, 10, 6, imm5)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rd)
    return byte

def ASRSimm(rd, rm, imm5):
    byte = 0
    byte = putByte(byte, 12, 11, 2)
    byte = putByte(byte, 10, 6, imm5)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rd)
    return yte

def ADDS(rd, rn, rm):
    byte = 0
    byte = putByte(byte, 12, 11, 3)
    byte = putByte(byte, 8, 6, rm)
    byte = putByte(byte, 5, 3, rn)
    byte = putByte(byte, 2, 0, rd)
    return byte

def SUBS(rd, rn, rm):
    byte = 0
    byte = putByte(byte, 12, 11, 3)
    byte = putByte(byte, 9, 9, 1)
    byte = putByte(byte, 8, 6, rm)
    byte = putByte(byte, 5, 3, rn)
    byte = putByte(byte, 2, 0, rd)
    return byte

def ADDSimm(rd, rn, imm3):
    byte = 0
    byte = putByte(byte, 12, 11, 3)
    byte = putByte(byte, 10, 10, 1)    
    byte = putByte(byte, 8, 6, imm3)
    byte = putByte(byte, 5, 3, rn)
    byte = putByte(byte, 2, 0, rd)
    return byte

def SUBSimm(rd, rn, imm3):
    byte = 0
    byte = putByte(byte, 12, 9, 15)
    byte = putByte(byte, 10, 10, 1)
    byte = putByte(byte, 9, 9, 1) 
    byte = putByte(byte, 8, 6, imm3)
    byte = putByte(byte, 5, 3, rn)
    byte = putByte(byte, 2, 0, rd)
    return byte

def MOVSimm(rd, imm8):
    byte = 0
    byte = putByte(byte, 15, 13, 1)
    byte = putByte(byte, 10, 8, rd)
    byte = putByte(byte, 7, 0, imm8)
    return byte

def ANDS(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def EORS(rdn,rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 1)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def LSLS(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 2)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def LSRS(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 3)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def ASRS(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 4)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def ADCS(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 5)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def ADCS(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 6)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def RORS(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 7)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def TST(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 8)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def RSBS(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 9)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def CMP(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 10)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def CMN(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 11)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def ORRS(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 12)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def MULS(rdm, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 13)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def BICS(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 14)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def MVNS(rdn, rm):
    byte = 0
    byte = putByte(byte, 15, 10, 16)
    byte = putByte(byte, 9, 6, 15)
    byte = putByte(byte, 5, 3, rm)
    byte = putByte(byte, 2, 0, rdn)
    return byte

def STR(rt, imm8):
    byte = 0
    byte = putByte(byte, 15, 12, 9)
    byte = putByte(byte, 10, 8, rt)
    byte = putByte(byte, 7, 0, imm8)
    return byte

def LDR(rt, imm8):
    byte = 0
    byte = putByte(byte, 15, 12, 9)
    byte = putByte(byte, 11, 11, 1)
    byte = putByte(byte, 10, 8, rt)
    byte = putByte(byte, 7, 0, imm8)
    return byte

def ADDspimm(imm7):
    byte = 0
    byte = putByte(byte, 15, 12, 11)
    byte = putByte(byte, 6, 0, imm7)
    return byte

def SUBspimm(imm7):
    byte = 0
    byte = putByte(byte, 15, 12, 11)
    byte = putByte(byte, 7, 7, 1)
    byte = putByte(byte, 6, 0, imm7)
    return byte

def B(c, label):
    byte = 0
    byte = putByte(byte, 15, 12, 13)
    byte = putByte(byte, 11, 8, c)
    byte = putByte(byte, 7, 0, label)
    return byte
