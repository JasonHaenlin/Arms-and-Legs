"""Launches the parser, reading ASM code on the standard input, and
writing compiled code on the standard output"""

import sys
import os.path

import armparser


def main(argv):
    """Parse the ASM code in the input file (first argument) and write
    the resulting compiled code in the output file (second argument)"""
    # recover the input and output file paths
    if len(argv) != 3:
        print("expected exactly one input file and one output file")
        fail("usage: main.py <inputfile> <outputfile>")
    input_path, output_path = argv[1], argv[2]
    if not os.path.isfile(input_path):
        fail("input file does not exist")
    # parse the input file
    with open(input_path) as input_file:
        parser = armparser.ASMParser(input_file)
        parser.parse()
    # write the result to the given output file
    with open(output_path, "w") as output_file:
        parser.write_hex_code(output_file)


def fail(msg):
    """Print the message on the standard error output and quit with an
    error code"""
    print("error: " + msg, file=sys.stderr)
    exit(1)


# run the program
if __name__ == "__main__":
    arg = "main.py", "input1.asm", "output.asm"
    main(arg)
