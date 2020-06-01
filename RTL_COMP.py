import sys
import re
import io

from utils.tokenizing import *
from utils.tokens import *
from utils.commands import *
from utils.instructions import *
from utils.code import *
from utils.nodes import *
from utils.building import *
from utils.running import *
from utils.terminal import *

init_terminal()

args = sys.argv.copy()
args.pop(0)

help_str = \
"""You passed no arguments to RTL_COMP, so it assumed, you need some help.
Reading this google document should be all you need:
https://docs.google.com/document/d/1GKr_WNL3qzZV5JnkhncsI77dgBCWcAdCqXF2qjau9C8/edit?usp=sharing"""

def build_script(script):
    log("Building script...", LL_debug)
    tokens = tokenize(script)
    return build_tokens(tokens)
    

def load_script(path):
    log(f"Loading script from {path}...", LL_debug)
    file = open(path, "rt")
    script = file.readlines()
    file.close()
    return script

def load_code(path):
    log(f"Loading code from {path}...", LL_debug)

def run_code(code):
    log("Running code...", LL_debug)
    if code == None:
        log("    Nothing to run.", LL_warning)
        return
    log(code, LL_debug)
    state = RunState(code)
    state.start()


def run_script(script):
    log("Running script...", LL_debug)
    run_code(build_script(script))

def format_script(script):
    log("Formating script...", LL_debug)

def save_code(code, path):
    log(f"Saving code to {path}...", LL_debug)

def save_script(script, path):
    log(f"Saving script to {path}...", LL_debug)
    file = open(path, "wt")
    file.writelines(script)
    file.close()

def disassemble_code(code):
    log("Disassembling code...", LL_debug)

if len(args) == 0:
    print(help_str)
else:
    if "-loglevel" in args:
        set_log_level(int(args[args.index("-loglevel") + 1]))

    if args[0] == "-build":
        path = args[1]
        script = load_script(path)
        code = build_script(script)
        if len(args) >= 4 and args[2] == "-path":
            path = args[3]
        else:
            path = ".".join(path.split(".")[:-1]) + ".RTLC"
        save_code(code, path)
    else: #run
        path = args[0]
        if path.endswith(".RTLC"):
            run_code(load_code(path))
        else:
            run_script(load_script(path))

if not "-autoexit" in args:
    input("RTL_COMP is done. Press Enter to exit.")
