import colorama
from colorama import Fore, Back, Style

def init_terminal() -> None:
    """Does the colorama init."""
    colorama.init()

LL_default = 0

LL_output = -1
LL_error = 0
LL_warning = 1
LL_debug = 2
LL_disect = 3

log_colors = {
    LL_output:Fore.WHITE,
    LL_error:Fore.RED,
    LL_warning:Fore.YELLOW,
    LL_debug:Fore.GREEN,
    LL_disect:Fore.CYAN,
}


log_level = LL_default

def log(text: str, level: int, nl: bool = True) -> None:
    """Prints a piece of text in the specified loglevel, folowed by \\n by default."""
    if log_level >= level:
        print(f"{log_colors[level]}{text}{Fore.RESET}{Back.RESET}", end=("\n" if nl else ""))

def set_log_level(level: int) -> None:
    """Sets the global log level (used by the args parser only)."""
    global log_level
    log_level = level