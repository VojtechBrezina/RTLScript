from utils.tokenizing import *

class TokenType:
    def __init__(self, name, regex, clean_func):
        self.name = name
        self.regex = regex
        self.next_types = []
        self.clean_func = clean_func
    
    def __str__(self):
        return self.name

class TokenInstance:
    def __init__(self, token_type, text):
        self.token_type = token_type
        self.raw = text
        self.text = token_type.clean_func(text)
    
    def __str__(self):
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
    r"\d+\.*\d*",
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

TT_all = [TT_end, TT_command, TT_string_literal, TT_number, TT_variable_start, TT_variable_end]