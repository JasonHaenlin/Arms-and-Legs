from sys import *
from instructions import *

def readFile(filename):
    file = open(filename, "r")
    content = file.read()
    file.close()
    return content

def writeFile(filename, binaries):
    file = open(filename, "w")
    file.write(binaries)
    file.close()

def translate(args):
    try:
        cmd = args[0].lower()
        imm = any("#" in arg for arg in args)
        sp = any("sp" in arg for arg in args)
        hexa = 0
        if cmd == "lsls":
            if imm:
                hexa = LSLSimm(args[1], args[2], args[3])
            else:
                hexa = LSLS(args[1], args[2])
        elif cmd == "lsrs":
            if imm:
                hexa = LSRSimm(args[1], args[2], args[3]);
            else: hexa = LSRS(args[1], args[2]);
        elif cmd == "asrs":
            if imm:
                hexa = ASRSimm(args[1], args[2], args[3])
            else:
                hexa = ASRS(args[1], args[2])
        elif cmd == "adds":
            if imm:
                hexa = ADDSimm(args[1], args[2], args[3])
            else:
                hexa = ADDS(args[1], args[2], args[3])
        elif cmd == "subs":
            if imm:
                hexa = SUBSimm(args[1], args[2], args[3])
            else:
                hexa = SUBS(args[1], args[2], args[3])
        elif cmd == "movs":
            hexa = MOVSimm(args[1], args[2])
        elif cmd == "ands":
            hexa = ANDS(args[1], args[2])
        elif cmd == "eors":
            hexa = EORS(args[1], args[2])
        elif cmd == "adcs":
            hexa = ADCS(args[1], args[2])
        elif cmd == "sbcs":
            hexa = SBCS(args[1], args[2])
        elif cmd == "rors":
            hexa = RORS(args[1], args[2])
        elif cmd == "tst":
            hexa = TST(args[1], args[2])
        elif cmd == "rsbs":
            hexa = RSBS(args[1], args[2])
        elif cmd == "cmp":
            hexa = CMP(args[1], args[2])
        elif cmd == "cmn":
            hexa = CMN(args[1], args[2])
        elif cmd == "orrs":
            hexa = ORRS(args[1], args[2])
        elif cmd == "muls":
            hexa = MULS(args[1], args[2])
        elif cmd == "bics":
            hexa = BICS(args[1], args[2])
        elif cmd == "mvns":
            hexa = MVNS(args[1], args[2])
        elif cmd == "str":
            try:
                hexa = STR(args[1], args[3])
            except:
                hexa = STR(args[1], "0")
        elif cmd == "ldr":
            hexa = LDR(args[1], args[3])
        elif cmd == "add":
            hexa = ADDspimm(args[2])
        elif cmd == "sub":
            hexa = SUBspimm(args[2])
        elif cmd == "b":
            hexa = B(args[1], args[2])
        return hex(hexa).replace("0x", "")
    except:
        return ""

def readLine(line):
    args = line.replace(",", "").replace("  ", " ").replace("\t", " ").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "").split(' ')
    for i in range(len(args)):
        if args[i] == "":
            del args[i]
    return args

def parse(content):
    binaries = ""
    for line in content.split('\n'):
        translation = translate(readLine(line))
        if translation !="":
            if binaries != "":
                binaries += " "
            binaries += translation
    return binaries

if __name__ == "__main__":
    filename = argv[1]
    output = argv[2]
    code = readFile(filename)
    binaries = "v2.0 raw\n" + parse(code) + "\n"
    writeFile(output, binaries)  
