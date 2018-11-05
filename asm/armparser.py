"""Internal ASM parser code"""

import re

from instruction import *
from label import *

BIN_INSTRUCTION_SIZE = 16


class ASMParserError(Exception):
    """Represents an error in the parsed file"""

    def __init__(self, msg, line_count=None):
        if line_count is None:
            super().__init__(msg)
        else:
            super().__init__("line {}: {}".format(line_count, msg))


class ASMParser:
    """This class parses a single ASM file and writes the compiled code
    to another file"""

    def __init__(self, input_file):
        # the file that contains the ASM code
        self.input_file = input_file
        # the list of compiled instructions in Logisim hex format
        self.hex_instructions = []
        # maps each label to its address (instruction number)
        # in the compiled code
        self.labels = {}
        # maps each variable name to the address we allocated it
        self.variables = {}
        # checks if the parsing has ended (otherwise we can't write
        # the result yet)
        self.parsing_ended = False
        # tracks the current line's number in the input file
        self.line_count = 0
        # tracks the instructions line's number in the input file
        self.instruction_count = 0
        # keep in memory the condition that need to be manage with the line instruction
        self.label_needed = {}

    def parse(self):
        """Read and parse the input file until the end of the code is
        reached, fills the hex_instructions list with compiled
        instructions in hexadecimal format"""
        self.__parse_data()
        self.__parse_text()

    def __parse_data(self):
        """Parse the data section of the file and fills the variables
        map"""
        line = ""
        while not line:
            line = self.__next_line()
        if line != ".data":
            raise ASMParserError("expected .data", self.line_count)
        first_free_address = 0
        end = False
        while not end:
            print("ligne data")
            line = self.__next_line()
            if not line:
                pass
            elif line == ".end":
                end = True
            else:
                varname, vartype, value = self.__match_declaration(line)
                address = first_free_address
                print("variable {} de type {} et de valeur {} à {}"
                      .format(varname, vartype, value, address))
                first_free_address += 1
                self.variables[varname] = address
                # value_int = int(value, 0)
                # MOV R0 value_int
                # alloc_instr = "00100000" + bin(value_int)[2:].zfill(8)
                # self.__add_instruction_bin(alloc_instr)
                # STR R0 address
                # str_instr = "10010000" + bin(address)[2:].zfill(8)
                # self.__add_instruction_bin(str_instr)

    def __match_declaration(self, line):
        """Parse a variable declaration line and return a (name, type,
        value) tuple"""
        decl_regex = r"""(\w+): [.](\w+)[ ,](\w+)"""
        m = re.match(decl_regex, line)
        if m is None or len(m.groups()) != 3:
            raise ASMParserError("bad declaration", self.line_count)
        return m.groups()

    def __imm_is_define(self, isImm):
        return isImm in self.variables

    def __immediate_to_bin_str(self, immediate, str_len):
        """Converts an immediate in "#XX form to a binary string of the
        given length"""
        if not self.__imm_is_define(immediate):
            if not immediate.startswith("#"):
                raise ASMParserError(
                    "immediate doesn't start with '#' or the data is not set",
                    self.line_count
                )
        if self.__imm_is_define(immediate):
            n_str = self.variables[immediate]
        else:
            n_str = immediate[1:]
        n = int(n_str)
        return self.__int_to_bin_str(n, str_len)

    def __reg_to_bin_str(self, reg_name, str_len):
        """Converts a register name "RX" into a binary string of the
        given length representing the register's address"""
        if not reg_name.startswith("R"):
            raise ASMParserError(
                "register name doesn't start with 'R'",
                self.line_count
            )
        n_str = reg_name[1:]
        n = int(n_str)
        return self.__int_to_bin_str(n, str_len)

    def __int_to_bin_str(self, i, str_len):
        """Converts i to a binary string of the given length"""
        b_str = bin(i)[2:].zfill(str_len)
        return b_str

    def __parse_text(self):
        line = ""
        while not line:
            line = self.__next_line()
        if line != ".text":
            raise ASMParserError("expected .text", self.line_count)
        # parse labels and instructions
        while not self.parsing_ended:
            line = self.__next_line()
            # check if the section is over
            if not line:
                pass
            elif line == ".end":
                self.parsing_ended = True
            # check if this line defines a label
            elif line.endswith(":"):
                label_name = line[:-1]
                # this label is mapped to the next instruction we will
                # read
                self.labels[label_name] = self.instruction_count
                if label_name in self.label_needed:
                    line, name = self.label_needed[label_name]
                    name = B_INSTR_CONDI + self.__labed_condition(name) \
                        + self.__immediate_to_bin_str("#" + str(self.instruction_count), 8)
                    self.__change_instruction_bin(name, line)
            else:
                self.__parse_instructions(line)

    def __parse_instructions(self, line):
        instr_name, argstr = line.split(" ")
        if len(argstr) >= 2:
            args = argstr.split(",")
        else:
            args = argstr
        final_bin_instr = None
        print("ligne : " + str(self.instruction_count) + "  " + instr_name)
        if instr_name == "LSL":
            final_bin_instr = LSL_INSTR_IMM \
                + self.__immediate_to_bin_str(args[2], 5) \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "LSR":
            final_bin_instr = LSL_INSTR_IMM \
                + self.__immediate_to_bin_str(args[2], 5) \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "ASR":
            final_bin_instr = ASR_INSTR_IMM \
                + self.__immediate_to_bin_str(args[2], 5) \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "ADD":
            if args[0] == "SP":
                final_bin_instr = ADD_IMM_TO_SP \
                    + self.__immediate_to_bin_str(args[0], 7)
            elif args[2].startswith("R"):
                final_bin_instr = ADD_INSTR_REG \
                    + self.__reg_to_bin_str(args[2], 3) \
                    + self.__reg_to_bin_str(args[1], 3) \
                    + self.__reg_to_bin_str(args[0], 3)
            else:
                final_bin_instr = ADD_INSTR_IMM \
                    + self.__immediate_to_bin_str(args[2], 3) \
                    + self.__reg_to_bin_str(args[1], 3) \
                    + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "SUB":
            if args[0] == "SP":
                final_bin_instr = SUB_IMM_TO_SP \
                    + self.__immediate_to_bin_str(args[0], 7)
            elif args[2].startswith("R"):
                final_bin_instr = SUB_INSTR_REG \
                    + self.__reg_to_bin_str(args[2], 3) \
                    + self.__reg_to_bin_str(args[1], 3) \
                    + self.__reg_to_bin_str(args[0], 3)
            else:
                final_bin_instr = SUB_INSTR_IMM \
                    + self.__immediate_to_bin_str(args[2], 3) \
                    + self.__reg_to_bin_str(args[1], 3) \
                    + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "MOV":
            final_bin_instr = MOV_INSTR_IMM \
                + self.__reg_to_bin_str(args[0], 3) \
                + self.__immediate_to_bin_str(args[1], 8)
        elif instr_name == "AND":
            final_bin_instr = AND_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "EOR":
            final_bin_instr = EOR_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "LSL":
            final_bin_instr = LSL_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "LSR":
            final_bin_instr = LSR_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "ASR":
            final_bin_instr = ASR_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "ADC":
            final_bin_instr = ADC_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "SBC":
            final_bin_instr = SBC_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "ROR":
            final_bin_instr = ROR_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "TST":
            final_bin_instr = TST_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "RSB":
            final_bin_instr = RSB_INSTR_IMM \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "CMP":
            final_bin_instr = CMP_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "CMN":
            final_bin_instr = CMN_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "ORR":
            final_bin_instr = ORR_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "MUL":
            final_bin_instr = MUL_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "BIC":
            final_bin_instr = BIC_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "MVN":
            final_bin_instr = MVN_INSTR_REG \
                + self.__reg_to_bin_str(args[1], 3) \
                + self.__reg_to_bin_str(args[0], 3)
        elif instr_name == "STR":
            final_bin_instr = STR_INSTR_IMM \
                + self.__reg_to_bin_str(args[0], 3) \
                + self.__immediate_to_bin_str(args[1], 8)
        elif instr_name == "LDR":
            final_bin_instr = LDR_INSTR_IMM \
                + self.__reg_to_bin_str(args[0], 3) \
                + self.__immediate_to_bin_str(args[1], 8)
        elif instr_name.startswith("B"):
            if args[0] in self.labels:
                args[0] = "#" + str(self.labels[args[0]])
            else:
                self.label_needed[args[0]
                                  ] = self.instruction_count, instr_name
                args[0] = "#0"
            final_bin_instr = B_INSTR_CONDI \
                + self.__labed_condition(instr_name) \
                + self.__immediate_to_bin_str(args[0], 8)
        else:
            raise ASMParserError(
                "bad instruction name: " + instr_name,
                self.line_count
            )
        self.__add_instruction_bin(final_bin_instr)
        self.instruction_count += 1

    def __add_instruction_bin(self, bin_instr):
        """Adds the instruction, given as a binary number in a string,
        to the list of instructions in hexadecimal format"""
        hex_str = self.__build_hexa(
            bin_instr)  # pad left with zeros if necessary
        self.hex_instructions.append(hex_str)

    def __change_instruction_bin(self, bin_instr, line_instr):
        """Change the instruction, given as a binary number in a string,
        to the list of instructions in hexadecimal format"""
        hex_str = self.__build_hexa(bin_instr)
        # pad left with zeros if necessary
        self.hex_instructions[line_instr] = hex_str

    def __build_hexa(self, bin_instr):
        if len(bin_instr) != BIN_INSTRUCTION_SIZE:
            raise ASMParserError("bad binary instruction: "
                                 "must be {} bytes long, got {}".format(
                                     BIN_INSTRUCTION_SIZE,
                                     bin_instr),
                                 self.line_count)
        hex_str = hex(int(bin_instr, 2))
        hex_str = hex_str[2:]  # delete the '0x' prefix
        hex_str = hex_str.zfill(4)  # pad left with zeros if necessary
        return hex_str

    def __next_line(self):
        # delete control characters
        regex = re.compile(r'[\n\r\t]')
        self.line_count += 1
        s = regex.sub("", self.input_file.readline())
        s = s.rstrip()
        s = s.lstrip()
        return s

    def write_hex_code(self, output_file):
        """Write the resulting compiled code to the given output file"""
        if not self.parsing_ended:
            raise ASMParserError(
                "can't write result: parsing was not completed")
        output_file.write("v2.0 raw\n")
        for instruction in self.hex_instructions:
            output_file.write(instruction + "\n")

    def __labed_condition(self, condition):
        label = condition[1:]  # delete the 'B' caractere
        if (label == "EQ") | (label == "E"):
            return EQ
        elif label == "NE":
            return NE
        elif (label == "CS") | (label == "HS"):
            return CS
        elif (label == "CC") | (label == "LO"):
            return CC
        elif label == "MI":
            return MI
        elif label == "PL":
            return PL
        elif label == "VS":
            return VS
        elif label == "VC":
            return VC
        elif label == "HI":
            return HI
        elif label == "LS":
            return LS
        elif label == "GE":
            return GE
        elif label == "LT":
            return LT
        elif label == "GT":
            return GT
        elif label == "LE":
            return LE
        elif label == "AL":
            return AL
        elif not label:
            return AL
        else:
            raise ASMParserError(
                "bad condition label: " + label,
            )
