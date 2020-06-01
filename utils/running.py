from collections import deque, defaultdict

from utils.instructions import *

class RunState:
    def __init__(self, code):
        self.scope_stack = deque()
        self.exp_stack = deque()
        self.code = code
    
    def start(self):
        self.scope_push()
        self.pos = 0
        while self.pos < len(self.code.instructions):
            self.pos += 1 + instructions[self.code.get_instruction(self.pos)].run(self, self.code, self.pos + 1)

    def scope_push(self):
        self.scope_stack.appendleft(defaultdict(lambda: 0))
    
    def scope_pop(self):
        self.scope_stack.popleft()

    def exp_push(self, what):
        self.exp_stack.appendleft(what)
    
    def exp_pop(self):
        return self.exp_stack.popleft()
    
    def set_local(self, where, what, depth = 0):
        self.scope_stack[depth][where] = what
    
    def get_local(self, where, depth = 0):
        return self.scope_stack[depth][where]