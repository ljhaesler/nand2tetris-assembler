import argparse
import logging
import os
import sys
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
logger = logging.getLogger("assembler")

first_pass = hack_parser.Parser(args.filename)
second_pass = hack_parser.Parser(args.filename)

code = hack_code.Code()
hack = []
symbolTable = hack_symbol.SymbolTable()

ROM_address = 0
RAM_address = 16

while first_pass.hasMoreCommands():
    first_pass.advance()
    command = first_pass.commandType()

    if command == 'L_COMMAND':
        symbol = first_pass.symbol()
        if symbolTable.contains(symbol):
            # covers both a label defined twice and a label reusing a built-in name
            logger.error(f"Duplicate label: ({symbol}) is already defined, exiting.")
            sys.exit(1)

        symbolTable.addEntry(symbol, ROM_address)
        continue # don't increment ROM_address

    ROM_address += 1

while second_pass.hasMoreCommands():
    second_pass.advance()
    command = second_pass.commandType()

    if command == 'L_COMMAND':
        continue

    elif command == 'A_COMMAND':
        symbol = second_pass.symbol()

        if symbol.isdecimal():
            hack.append(format(int(symbol), "016b"))
        else:
            if not symbolTable.contains(symbol):
                symbolTable.addEntry(symbol, RAM_address)
                RAM_address += 1

            hack.append(format(symbolTable.getAddress(symbol), "016b"))

    elif command == 'C_COMMAND':
        c_instruction = ["111"]
        c_instruction.append(code.comp(second_pass.comp()))
        c_instruction.append(code.dest(second_pass.dest()))
        c_instruction.append(code.jump(second_pass.jump()))
        hack.append("".join(c_instruction))


machine_code = "\n".join(hack)
writeFileName = os.path.basename(args.filename).removesuffix(".asm") + ".hack"

# output goes next to this script, regardless of where it's run from
outputDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "machine_code")
os.makedirs(outputDir, exist_ok=True) # create the output directory if it's missing
with open(os.path.join(outputDir, writeFileName), "w") as file:
    file.write(machine_code)
    file.write("\n")
