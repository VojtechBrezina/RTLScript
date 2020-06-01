import colorama
from colorama import Fore, Back, Style

def init_terminal():
    colorama.init()

LL_default = 0

LL_output = -1
LL_error = 0
LL_warning = 1
LL_debug = 2

log_colors = {
    LL_output:Fore.WHITE,
    LL_error:Fore.RED,
    LL_warning:Fore.YELLOW,
    LL_debug:Fore.GREEN
}


log_level = LL_default

def log(text, level, nl = True):
    if log_level >= level:
        print(f"{log_colors[level]}{text}{Fore.RESET}", end=("\n" if nl else ""))

def set_log_level(level):
    global log_level
    log_level = level