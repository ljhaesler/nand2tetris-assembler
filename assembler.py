import argparse
import logging
import hack_parser
import hack_code

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

while parser.hasMoreCommands():
    parser.advance()
    if parser.commandType() == 'A_COMMAND':
        hack.append(format(int(parser.symbol()), "016b"))
    if parser.commandType() == 'C_COMMAND':
        c_instruction = ["111"]
        c_instruction.append(code.comp(parser.comp()))
        c_instruction.append(code.dest(parser.dest()))
        c_instruction.append(code.jump(parser.jump()))
        hack.append("".join(c_instruction))

machine_code = "\n".join(hack)
writeFileName = args.filename.removesuffix(".asm") + ".hack"

with open(f"machine_code/{writeFileName}", "w") as file:
    file.write(machine_code)
    file.write("\n")
