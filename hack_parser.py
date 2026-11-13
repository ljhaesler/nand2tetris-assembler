PREDEFINED_SYMBOLS = ["SP", "LCL", "ARG", "THIS", "THAT",
                      "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9",
                      "R10", "R11", "R12", "R13", "R14", "R15",
                      "SCREEN", "KBD"]

import logging
logging.basicConfig(level=logging.INFO, format='PARSER %(levelname)s: %(message)s')


class Parser:
    def __init__(self, filename):
        logging.info("Parsing file")
        with open(filename) as file:
            self.commands = file.readlines()
        logging.info(f'File contains {len(self.commands)} lines')

    def _stripCommand(self, command):
        return command.split("//")[0].strip()

    def hasMoreCommands(self):
        logging.info(f'File has {len(self.commands)} lines left')

        for i in range(len(self.commands)):
            if len(self._stripCommand(self.commands[i])) > 0:
                return True

        return False;

    def advance(self):
        self.currentcommand = self._stripCommand(self.commands.pop())

    def commandType(self):
        if self.currentcommand.startswith('@'):
            if self.currentcommand[1:].isdecimal():
                logging.info('Command is parsed as A_COMMAND')
                return "A_COMMAND"
            logging.info('Command is parsed as L_COMMAND')
            return "L_COMMAND"
        logging.info('Command is parsed as C_COMMAND')
        return "C_COMMAND"

    def symbol(self):
        logging.info(f'Current command symbol is {self.currentcommand[1:]}')
        return self.currentcommand[1:]

    def dest(self):
        if "=" in self.currentcommand:
                return self.currentcommand[:self.currentcommand.find('=')]

        logging.info('Unfound DEST mnemonic, returning string "null"')
        return "null"

    def comp(self):
        comp = self.currentcommand.split('=')[-1].split(";")[0]

        if len(comp) == 1:
            return comp

        logging.error('Invalid COMP mnemonic, exiting')
        exit()

    def jump(self):
        if ";" in self.currentcommand:
            return self.currentcommand[self.currentcommand.find(';')+1:]

        logging.info('Unfound JUMP mnemonic, returning string "null"')
        return "null"

