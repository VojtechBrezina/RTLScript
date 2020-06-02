from __future__ import annotations

from collections import deque, defaultdict

from utils.instructions import *
from utils.code import *
from utils.running import *

class RunState:
    """Represents a state of the interpretter.
    
    This class is used to actually interpret the `Code`.
    It contains a `Code` and the curent position. It also 
    optionally contains a prefix if it is a library state
    and the RunState that spawned the library for scopesharing.
    """
    def __init__(self, code: Code, prefix: str = "", lib_parent: RunState = None):
        if lib_parent == None:
            self.scope_stack = deque()
            self.exp_stack = deque()
        else:
            self.scope_stack = lib_parent.scope_stack
            self.exp_stack = lib_parent.exp_stack
        self.code = code
        self.prefix = prefix
    
    def start(self, pos = 0, lib_call = False) -> None:
        """Starts the execution.
        
        If the `pos` is specified it starts from a given position.
        If it is a lib call, then the execution stops as soon as the
        outer function returns ot ends. 
        """
        from utils.instructions import instructions
        self.scope_push()
        self.pos = pos
        while self.pos < len(self.code.instructions):
            self.pos += 1 + instructions[self.code.get_instruction(self.pos)].run(self, self.code, self.pos + 1)

    def scope_push(self) -> None:
        """Introduces a fresh local scope."""
        self.scope_stack.appendleft(defaultdict(lambda: 0))
    
    def scope_pop(self) -> None:
        """Destroys the local scope and returns back up in the stack."""
        self.scope_stack.popleft()

    def exp_push(self, what: Any) -> None:
        """Pushes an expression onto the stack."""
        self.exp_stack.appendleft(what)
    
    def exp_pop(self) -> Any:
        """Pops an expression from the stack."""
        return self.exp_stack.popleft()
    
    def set_local(self, where: Any, what: Any, depth: int = 0) -> None:
        """Sets a local (or from any scope if the `depth` is specified,
        the name has historical reasons) variable."""
        self.scope_stack[depth][where] = what
    
    def get_local(self, where: Any, depth: int = 0) -> Any:
        """Retrieves a local (or from any scope if the `depth` is specified,
        the name has historical reasons) variable."""
        return self.scope_stack[depth][where]