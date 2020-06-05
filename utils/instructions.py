from typing import *

from rtlscript.logging import *
from utils.running import *

instructions = dict()

class Instruction:
    """Represents a single instruction runnble by the interpreter.
    
    It contains an 8-bit code, a function that runs it on a given set of state variables and
    a string that describes it to the decompiler.
    """
    def __init__(self, code: int, run_func: Callable[[RunState, Code, int], int], decomp_str: str):
        global instructions
        instructions[code] = self
        self.code = code
        self.run = run_func
        self.decomp_str = decomp_str

def IR_push_string(state: RunState, code: Code, pos: int) -> int:
    state.exp_push(code.get_data(code.get_bytes(pos, 4)).data)
    return 4
IC_push_string = 0x00
Instruction(IC_push_string, IR_push_string, "PUSH_STRING,i")

def IR_push_number(state: RunState, code: Code, pos: int) -> int:
    state.exp_push(code.get_number(pos))
    return 8
IC_push_number = 0x01
Instruction(IC_push_number, IR_push_number, "PUSH_NUMBER,n")

def IR_print(state: RunState, code: Code, pos: int) -> int:
    log(state.exp_pop(), LL_output, nl = False)
    return 0
IC_print = 0x02
Instruction(IC_print, IR_print, "PRINT,")

def IR_stop(state: RunState, code: Code, pos: int) -> int:
    return len(code.instructions) - pos
IC_stop = 0x03
Instruction(IC_stop, IR_stop, "STOP,")

def IR_set(state: RunState, code: Code, pos: int) -> int:
    where = state.exp_pop()
    what = state.exp_pop()
    state.set_local(where, what)
    return 0
IC_set = 0x04
Instruction(IC_set, IR_set, "SET,")

def IR_push_var(state: RunState, code: Code, pos: int) -> int:
    which = state.exp_pop()
    state.exp_push(state.get_local(which))
    return 0
IC_push_var = 0x05
Instruction(IC_push_var, IR_push_var, "PUSH_VAR,")

def IR_pop_exp(state: RunState, code: Code, pos: int) -> int:
    state.exp_pop()
    return 0
IC_pop_exp = 0x06
Instruction(IC_pop_exp, IR_pop_exp, "POP_EXP,")

def IR_branch(state: RunState, code: Code, pos: int) -> int:
    condition = state.exp_pop()
    if condition == 0 or condition == "":
        return code.get_bytes(pos, 4) - pos
    return code.get_bytes(pos + 4, 4) - pos
IC_branch = 0x07
Instruction(IC_branch, IR_branch, "BRANCH,ii")

def IR_jump(state: RunState, code: Code, pos: int) -> int:
    return code.get_bytes(pos, 4) - pos
IC_jump = 0x08
Instruction(IC_jump, IR_jump, "JUMP,i")
