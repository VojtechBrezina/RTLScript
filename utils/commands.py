from utils.instructions import *

commands = dict()

class Command:
    def __init__(self, text, exp_count, build_func, block = 0):
        self.text = text
        self.exp_count = exp_count
        self.build = build_func
        self.block = block
        commands[text] = self
    
    def __str__(self):
        return self.text

def BC_print(code):
    code.put_instruction(IC_print)
Command("PRINT", 1, BC_print)

def BC_stop(code):
    code.put_instruction(IC_stop)
Command("STOP", 0, BC_stop)

def BC_set(code):
    code.put_instruction(IC_set)
Command("SET", 2, BC_set)

Command("FUNCTION", -1, None, True)
Command("IF", 1, None, True)
Command("LOOP", 1, None, True)
Command("BREAK", 0, None)