from typing import *

from utils.commands import *
from utils.tokens import *
from utils.code import *
from utils.instructions import *
from utils.terminal import *
from utils.errors import *


class Node:
    """A representation of an AST node.
    
    Every `Node` accepts the actual list of tokens and its level 
    in the tree (for debugging).
    """
    def __init__(self, tokens: List[TokenInstance], level: int):
        self.children = []
        self.print(level)
        self.print_level = level
        if len(tokens) == 0:
            raise RTLScriptError("RTL_COMP didn't expect the file to end here.")
    
    def print(self, level: int) -> None:
        """Debug-prints the node."""
        log("        " + ("   |" * level) + ("___" if level > 0 else "") + str(self), LL_debug)
    
    def build(self, code: Code) -> None:
        """An abstract method for building the node using the given `Code`."""
        pass

class BlockNode(Node):
    """A representation of a block of commands + expressions in the AST."""
    def __init__(self, tokens: List[TokenInstance], level: int, needs_end: bool = True):
        super().__init__(tokens, level)
        while len(tokens) > 0:
            if tokens[0].token_type is TT_command:
                self.children.append(CommandNode(tokens, level + 1))
            elif tokens[0].token_type is TT_end:
                if needs_end:
                    break
                else:
                    raise RTLScriptError(f"RTL_COMP did not expect END here.")
            else:
                self.children.append(ExpressionNode(tokens, level + 1))
        else:
            if needs_end:
                raise RTLScriptError("RTL_COMP didn't find END to close a block.")
        
    def __str__(self) -> str:
        return "BLOCK"
    
    def build(self, code: Code) -> None:
        for c in self.children:
            c.build(code)
            if isinstance(c, ExpressionNode):
                code.put_instruction(IC_pop_exp)

class RootNode(BlockNode):
    """The root `Node` in the AST is just an ENDless block."""
    def __init__(self, tokens: List[TokenInstance], level: int):
        super().__init__(tokens, level, False)
    
    def __str__(self) -> str:
        return "ROOT"

class CommandNode(Node):
    """An AST node that just builds the specified `Command`."""
    def __init__(self, tokens: List[TokenInstance], level: int):
        try:
            self.command = commands[tokens[0].text]
        except:
            raise RTLScriptError(f"Unknown command: {tokens[0].text}")
        super().__init__(tokens, level)

        tokens.pop(0)

        while len(self.children) < self.command.exp_count or self.command.exp_count < 0:
            if tokens[0].token_type is TT_end:
                if self.command.exp_count < 0:
                    if len(self.children) >= -self.command.exp_count:
                        tokens.pop(0)
                        break
                    else:
                        cnt = len(self.children)
                        raise RTLScriptError("RTL_COMP found {cnt} expressions, instead of {self.command.exp_count} for {self.command}.")
                else:
                    log(f"        RTL_COMP did not expect END here.", LL_error)
            self.children.append(ExpressionNode(tokens, level + 1))

        self.children.reverse()

        for i in range(self.command.block):
            self.children.append(BlockNode(tokens, level + 1))
    
    def __str__(self) -> str:
        return f"COMMAND: {self.command}"
    
    def build(self, code: Code) -> None:
        for c in self.children:
            c.build(code)
        self.command.build(code)

class ExpressionNode(Node):
    """Represents the root of any expression."""
    def __init__(self, tokens: List[TokenInstance], level: int):
        super().__init__(tokens, level)
        if tokens[0].token_type is TT_string_literal:
            self.children.append(StringNode(tokens, level + 1))
        elif tokens[0].token_type is TT_number:
            self.children.append(NumberNode(tokens, level + 1))
        elif tokens[0].token_type is TT_variable_start:
            self.children.append(VariableNode(tokens, level + 1))
        else:
            raise RTLScriptError("RTL_COMP expected an expression here.")
    
    def __str__(self) -> str:
        return f"EXPRESSION"
    
    def build(self, code: Code) -> None:
            self.children[0].build(code)

class StringNode(Node):
    """Represents a string literal."""
    def __init__(self, tokens: List[TokenInstance], level: int):
        self.text = tokens[0].text
        super().__init__(tokens, level)
        tokens.pop(0)
    
    def __str__(self) -> str:
        t = self.text.replace("\n", "\\n")
        return f"STRING: {t}"
    
    def build(self, code: Code) -> None:
        text = text = re.sub(r"\\n", "\n", self.text)
        data_pos = code.put_data(Data(DK_string, text))
        code.put_instruction(IC_push_string)
        code.put_bytes(data_pos, 4)

class NumberNode(Node):
    """Represents a number literal."""
    def __init__(self, tokens: List[TokenInstance], level: int) -> None:
        self.number = float(tokens[0].text)
        super().__init__(tokens, level)
        tokens.pop(0)
    
    def __str__(self) -> str:
        return f"NUMBER: {self.number}"
    
    def build(self, code: Code) -> None:
        code.put_instruction(IC_push_number)
        code.put_number(self.number)

class VariableNode(Node):
    """Represents a variable read."""
    def __init__(self, tokens: List[TokenInstance], level: int) -> None:
        super().__init__(tokens, level)
        tokens.pop(0)
        self.children.append(ExpressionNode(tokens, level + 1))
        if not (tokens[0].token_type is TT_variable_end):
            raise RTLScriptError(f" RTL_COMP expected variable to end here, instead found {tokens[0]}.")
        else:
            tokens.pop(0)
    
    def __str__(self) -> str:
        return "VARIABLE"
    
    def build(self, code: Code) -> None:
        self.children[0].build(code)
        code.put_instruction(IC_push_var)