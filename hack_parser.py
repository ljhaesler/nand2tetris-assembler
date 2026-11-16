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
        command = "C_COMMAND"
        if self.currentcommand.startswith('@'):
            command = "A_COMMAND"
        if self.currentcommand.startswith('(') and self.currentcommand.endswith(')'):
            command = "L_COMMAND"
        logger.info(f'{self.currentcommand} is parsed as {command}')
        return command

    def symbol(self):
        if self.currentcommand.startswith('@'):
            logger.info(f'SYMBOL: {self.currentcommand[1:]}')
            return self.currentcommand[1:]
        if self.currentcommand.startswith('(') and self.currentcommand.endswith(')'):
            logger.info(f'SYMBOL: {self.currentcommand[1:-1]}')
            return self.currentcommand[1:-1]

    def dest(self):
        if "=" in self.currentcommand:
            dest = self.currentcommand[:self.currentcommand.find('=')]
            logger.info(f'DEST: {dest}')
            return dest

        logger.info("DEST: null")
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

        logger.info("JUMP: null")
        return "null"

