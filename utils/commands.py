from typing import *

from utils.instructions import *

commands = dict()

class Command:
    """Represents a RTLScript command.
    
    A command has the text like "PRINT", the amount of arguments, 
    a fuction for building it into instructions ant the optional 
    amount of code blocks that follow.
    """
    def __init__(self, text: str, exp_count: int, build_func: Callable[[Code], None], block: int = 0):
        self.text = text
        self.exp_count = exp_count
        self.build = build_func
        self.block = block
        commands[text] = self
    
    def __str__(self) -> str:
        return self.text

def BC_print(code: Code) -> None:
    code.put_instruction(IC_print)
Command("PRINT", 1, BC_print)

def BC_stop(code: Code) -> None:
    code.put_instruction(IC_stop)
Command("STOP", 0, BC_stop)

def BC_set(code: Code) -> None:
    code.put_instruction(IC_set)
Command("SET", 2, BC_set)

def BC_if(code: Code) -> None:
    pass
Command("IF", 1, BC_if, 2)

#Command("FUNCTION", -1, None, True)
#Command("LOOP", 1, None, True)
#Command("BREAK", 0, None)