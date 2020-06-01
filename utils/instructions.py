from utils.terminal import *

instructions = dict()

class Instruction:
    def __init__(self, code, run_func):
        instructions[code] = self
        self.code = code
        self.run = run_func

def IR_push_string(state, code, pos):
    state.exp_push(code.get_data(code.get_bytes(pos, 4)).data)
    return 4
IC_push_string = 0x00
Instruction(IC_push_string, IR_push_string)

def IR_push_number(state, code, pos):
    state.exp_push(code.get_number(pos))
    return 8
IC_push_number = 0x01
Instruction(IC_push_number, IR_push_number)

def IR_print(state, code, pos):
    log(state.exp_pop(), LL_output)
    return 0
IC_print = 0x02
Instruction(IC_print, IR_print)

def IR_stop(state, code, pos):
    return len(code.instructions) - pos
IC_stop = 0x03
Instruction(IC_stop, IR_stop)

def IR_set(state, code, pos):
    where = state.exp_pop()
    what = state.exp_pop()
    state.set_local(where, what)
    return 0
IC_set = 0x04
Instruction(IC_set, IR_set)

def IR_push_var(state, code, pos):
    which = state.exp_pop()
    state.exp_push(state.get_local(which))
    return 0
IC_push_var = 0x05
Instruction(IC_push_var, IR_push_var)