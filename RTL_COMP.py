import sys
import re
import io
from typing import *

from rtlscript.logging import log, LL_debug, LL_warning, LL_output, set_log_level
from rtlscript.script import Script

from utils.tokenizing import *
from utils.tokens import *
from utils.commands import *
from utils.instructions import *
from utils.code import *
from utils.nodes import *
from utils.building import *
from utils.running import *

def build_script(script: List[str]) -> Code:
    """Builds a given script into bytecode."""
    log("Building script...", LL_debug)
    tokens = tokenize(script)
    return build_tokens(tokens)

def load_script(path: str) -> List[str]:
    """Loads a *.RTLS into a `List[str]`."""
    log(f"Loading script from {path}...", LL_debug)
    file = open(path, "rt")
    script = file.readlines()
    file.close()
    return script

def load_code(path: str) -> Code:
    """Loads a *.RTLS into a `Code` object."""
    log(f"Loading code from {path}...", LL_debug)

def run_code(code: Code) -> None:
    """Runs a `Code` object."""
    log("Running code...", LL_debug)
    if code == None:
        log("    Nothing to run.", LL_warning)
        return
    log(code, LL_debug)
    state = RunState(code)
    state.start()

def run_script(script: List[str]) -> None:
    """Performs all the necessary steps to run a script (represented as a line array)."""
    log("Running script...", LL_debug)
    run_code(build_script(script))

def format_script(script: List[str]) -> List[str]:
    """Formats script according to the chosen options."""
    log("Formating script...", LL_debug)

def save_code(code: Code, path: str) -> None:
    """Serializes a `Code` object and saves it into a file."""
    log(f"Saving code to {path}...", LL_debug)

def save_script(script: List[str], path: str) -> None:
    """Saves an array of lines into a file (used for formatting)."""
    log(f"Saving script to {path}...", LL_debug)
    file = open(path, "wt")
    file.writelines(script)
    file.close()

def disassemble_code(code: Code) -> None:
    """Disassembles a `Code` object and prints the result to the terminal for debuging purposes."""
    log("Disassembling code...", LL_debug)


if __name__ == "__main__":
    args = sys.argv.copy()
    args.pop(0)
    
    if "-loglevel" in args:
        set_log_level(int(args[args.index("-loglevel") + 1]))
    
    if len(args) == 0:
        log("You passed no arguments to RTL_COMP, so it assumed, you need some help.", LL_output, 0)
        log("If you do, visit https://github.com/VojtechBrezina/RTLScript", LL_output, 0)
    else:
        if args[0] == "-build":
            path = args[1]
            script = Script(path)
            #TODO build sript
            if len(args) >= 4 and args[2] == "-path":
                path = args[3]
            else:
                path = ".".join(path.split(".")[:-1]) + ".RTLC"
            #TODO save the code
        else: #run
            path = args[0]
            if path.endswith(".RTLC"):
                pass #TODO run code
            else:
                script = Script.from_file(path)
                pass #TODO run script

    if not "-autoexit" in args:
        input("RTL_COMP is done. Press Enter to exit.")

