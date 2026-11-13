PREDEFINED_SYMBOLS = ["SP", "LCL", "ARG", "THIS", "THAT",
                      "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9",
                      "R10", "R11", "R12", "R13", "R14", "R15",
                      "SCREEN", "KBD"]

import logging
logger = logging.getLogger(__name__)


class Parser:
    def __init__(self, filename):
        logger.info("Parsing file")
        with open(filename) as file:
            self.commands = self._stripAllLines(file.readlines())
        logger.info(f'File contains {len(self.commands)} lines')

    def _stripAllLines(self, lines):
        commands = []

        for i in range(len(lines)):
            command = lines[i].split("//")[0].strip()
            if len(command) > 0:
                commands.append(command)

        if len(commands) > 0:
            return commands

        logger.error("No commands found in .asm file, exiting.")
        exit()

    def hasMoreCommands(self):
        logger.info(f'File has {len(self.commands)} lines left')

        if len(self.commands) > 0:
            return True

        return False;

    def advance(self):
        self.currentcommand = self.commands.pop(0)

    def commandType(self):
        if self.currentcommand.startswith('@'):
            if self.currentcommand[1:].isdecimal():
                logger.info(f'{self.currentcommand} is parsed as A_COMMAND')
                return "A_COMMAND"
            logger.info(f'{self.currentcommand} is parsed as L_COMMAND')
            return "L_COMMAND"
        logger.info(f'{self.currentcommand} is parsed as C_COMMAND')
        return "C_COMMAND"

    def symbol(self):
        logger.info(f'SYMBOL: {self.currentcommand[1:]}')
        return self.currentcommand[1:]

    def dest(self):
        if "=" in self.currentcommand:
            dest = self.currentcommand[:self.currentcommand.find('=')]
            logger.info(f'DEST: {dest}')
            return dest

        logger.info('Unfound DEST mnemonic, returning string "null"')
        return "null"

    def comp(self):
        comp = self.currentcommand.split('=')[-1].split(";")[0]

        if len(comp) > 0:
            logger.info(f'COMP: {comp}')
            return comp

        logger.error('Invalid COMP mnemonic, exiting')
        exit()

    def jump(self):
        if ";" in self.currentcommand:
            jump = self.currentcommand[self.currentcommand.find(';')+1:]
            logger.info(f'JUMP: {jump}')
            return jump

        logger.info('Unfound JUMP mnemonic, returning string "null"')
        return "null"

