
## How to run the armAssembly program

### Requirements

The program is written in C# you'll need :

- .NET 4+ on Windows
- mono on Linux

### Command arguments

On Windows:

    armAssembly.exe <input-file> <output-file>

On Linux:

    mono armAssembly.exe <input-file> <output-file>

### Input file

The input file is an assembly file. It should follow the format of gcc's compiler output.

instructions should be lower-case:

    str, mov, ldr, ...

Upper-case instructions may not work:

    STR, MOV, LDR, ...

Labels and variables should been named correctly, i.e not the same as a reserved word.

Reserved words are the instructions + directives keywords.

### Output file

The output file follows Logisim input format:
    first line is : v2.0 raw
    other lines are 4 hexadecimal digits each

### Resource files

#### InstructionSet.xml

This file describes the instructions and how to translate them.
To add an instruction add these lines right before  `</instructions>`
```xml
       <command>
            <name>foo</name>
            <pattern>foo r(?<1>[0-9]+), #(?<2>[0-9]+)</pattern>
            <ranges>
                <range max="15" min="8" value="1"></range>
                <range max="7" min="3" value="#1"></range>
                <range max="2" min="0" value="#2"></range>
            </ranges>
        </command>
```
- **name**:    actual name of the command
- **pattern**: regex to parse te command
`(?<n>[0-9]+)` means "this is the nth variable of the command, and it is a number"<br>
`note that < and > have to be replaced with respectively &lt; and &gt;`
- **range**:
    describes how to generate the output from the command
- **value**:
    if value is "n" then the 16-bit integer represented by "n" will be used
    else if value is "#n" then the actual value is replaced by the corresponding one in the command


#### TypeSet.xml
```xml
       <type>
           <name>byte</name>
           <size>1</size>
       </type>
```
  - **name**:	actual name of the type
  - **size**:	size of the data in bytes
