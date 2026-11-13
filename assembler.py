import argparse
import parser
import code

argparser = argparse.ArgumentParser(
    prog='Hack Assembler',
    description='Takes a .asm file and converts it into a .hack file')

argparser.add_argument('filename')

args=argparser.parse_args()
assert args.filename.endswith(".asm"), "Input file is not a .asm file"


hackParser = parser.Parser(args.filename)
hackCode = code.Code()
hackMachineCode = []

while hackParser.hasMoreCommands():
    hackParser.advance()
    if hackParser.commandType() == 'A_COMMAND':
        hackMachineCode.append(format(int(hackParser.symbol()), "b"))
    if hackParser.commandType() == 'C_COMMAND':
        hackMachineCode.append(hackCode.dest(hackParser.dest()))
        hackMachineCode.append(hackCode.comp(hackParser.comp()))
        hackMachineCode.append(hackCode.jump(hackParser.jump()))

finalMachineCode = "".join(hackMachineCode)
writeFileName = args.filename.removesuffix(".asm") + ".hack"
