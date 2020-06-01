import re

from utils.tokens import *
from utils.terminal import *

def tokenize(script):
    log("    Reversing madness...", LL_debug)
    for index, line in enumerate(script):
        script[index] = line[::-1]
    script = "".join(script)
    #log(script, LL_debug)
    log("    Grabbing tokens...", LL_debug)
    tokens = []
    pos = 0
    result = re.search("^\s*", script[pos:], re.I | re.S)
    if result:
        pos += result.end()
    while pos < len(script):
        for token_type in TT_all:
            result = re.search("^" + token_type.regex, script[pos:], re.I | re.S)
            if result:
                token = TokenInstance(token_type, script[pos + result.start():pos + result.end()])
                tokens.append(token)
                pos += result.end()
                acceptable = token_type.next_types
                log(f"        {token}", LL_debug)
                break
        else:
            found = "\n".join(script[pos+15:pos-1:-1].split("\n"))
            log(f"        RTL_COMP thinks, that this makes no sense:            \n{found}", LL_error)
            log("        RTL_COMP could not build your script.", LL_warning)
            return None
        result = re.search("^\s*", script[pos:], re.I | re.S)
        if result:
            pos += result.end()
    return tokens