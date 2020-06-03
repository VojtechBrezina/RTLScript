from typing import *

from utils.tokenizing import *

TT_all = []

class TokenType:
    """A class that defines one type of token.
    
    A token type has a name for debugging purposes, a regex to perform the check and a clean function called to e.g. remove
    qotes from a string literal and unwrap the escapes.
    """
    def __init__(self, name: str, regex: str, clean_func: Callable[[str], str]) -> None:
        TT_all.append(self)
        self.name = name
        self.regex = regex
        self.next_types = []
        self.clean_func = clean_func
    
    def __str__(self) -> str:
        return self.name

class TokenInstance:
    """Specifies an instance of a token with the actual contents of a specific token."""
    def __init__(self, token_type: TokenType, text: str):
        self.token_type = token_type
        self.raw = text
        self.text = token_type.clean_func(text)
    
    def __str__(self) -> str:
        tmp_text = self.text.replace("\n", "\\n")[::-1]
        tmp_tt = str(self.token_type).ljust(20)
        return f"TT_{tmp_tt}{tmp_text}"

TT_end = TokenType(
    "END", 
    r"END", 
    lambda text: "END"
)

TT_command = TokenType(
    "COMMAND", 
    r"[A-Z]+", 
    lambda text: re.sub(r"\s", "", text)
)
    
TT_string_literal = TokenType(
    "STRING_LITERAL", 
    r"\".*?(?<!\\)\"", 
    lambda text: re.sub(r"\\\"", "\"", text[1:-1])
)

TT_number = TokenType(
    "NUMBER",
    r"-?\d+\.?\d*",
    lambda text: text
)

TT_variable_start = TokenType(
    "VARIABLE_START",
    r"\](@*|\$)",
    lambda text: text
)

TT_variable_end = TokenType(
    "VARIABLE_END",
    r"\[",
    lambda text: text
)

#TT_all = [TT_end, TT_command, TT_string_literal, TT_number, TT_variable_start, TT_variable_end]