from utils.nodes import *
from utils.code import *
from rtlscript.logging import *
from utils.errors import *

def build_tokens(tokens: List[TokenInstance]):
    """Builds the token sequence into an AST."""
    log("    Planting a tree...", LL_debug)
    if tokens == None:
        log("        Nothing to build.", LL_warning)
        return None
    try:
        tree_root = RootNode(tokens, 0)
    except RTLScriptError as err:
        log(f"        {err}", LL_error)
        log("        RTL_COMP could not build your script.", LL_warning)
        return None
    log("    Chopping that tree...", LL_debug)
    code = Code()
    tree_root.build(code)
    return code
    