School project that aims to build a simple processor inspired by ARMv7 in
Logisim Evolution

Authors:

    DURAND Clément
    GOBBIN Arno
    HAENLIN Jason
    UNG Vincent

This project contains the following parts:

    The CPU circuits:
        alu.circ
        BancDeRegistres.circ
        controller.circ
        MachineAvecCPU.circ

    The assembler language parser:
        armparser.py
        instruction.py
        label.py
        main.py

To use the parser, launch the following command in Windows cmd, PowerShell or
Bash:

    python main.py path/to/input_file.asm path/to/output_file.txt

...replacing the arguments with the actual paths you want the parser to use.
You must have installed Python 3. You may have to replace python with python3 on
Linux or macOS. On Windows, you may have to use the path to python.exe if it's
not in the PATH variable already.

Note to future contributors : 
    Flags_Out_Mask and Carry are uncomplete in the controller.circ file.
