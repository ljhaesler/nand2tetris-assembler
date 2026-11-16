import argparse
import logging
import os
import hack_parser
import hack_code
import hack_symbol

argparser = argparse.ArgumentParser(
    prog='Hack Assembler',
    description='Takes a .asm file and converts it into a .hack file')

argparser.add_argument('filename')
argparser.add_argument('-v', '--verbose', action='store_true',
                       help='show INFO-level parsing details')

args=argparser.parse_args()
assert args.filename.endswith(".asm"), "Input file is not a .asm file"

logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                    format='%(name)s %(levelname)s: %(message)s')


parser = hack_parser.Parser(args.filename)
code = hack_code.Code()
hack = []
symbolTable = hack_symbol.SymbolTable()

ROM_address = 0
RAM_address = 16

while parser.hasMoreCommands():
    parser.advance()
    command = parser.commandType()

    if command == 'L_COMMAND':
        symbol = parser.symbol()
        symbolTable.addEntry(symbol, ROM_address)

        continue # don't increment ROM_address

    elif command == 'A_COMMAND':
        symbol = parser.symbol()
        if symbol.isdecimal():
            hack.append(format(int(symbol), "016b"))
        else:
            symbolTable.addEntry(symbol, RAM_address)
            hack.append(format(int(symbolTable.getAddress(symbol)), "016b"))

            RAM_address += 1

    elif command == 'C_COMMAND':
        c_instruction = ["111"]
        c_instruction.append(code.comp(parser.comp()))
        c_instruction.append(code.dest(parser.dest()))
        c_instruction.append(code.jump(parser.jump()))
        hack.append("".join(c_instruction))

    ROM_address += 1

machine_code = "\n".join(hack)
writeFileName = os.path.basename(args.filename).removesuffix(".asm") + ".hack"

with open(f"machine_code/{writeFileName}", "w") as file:
    file.write(machine_code)
    file.write("\n")
