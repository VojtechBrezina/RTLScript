from __future__ import annotations

from typing import List

from .logging import log, LL_debug, LL_error
from .code import Code

class Script:
    """Represents the script as a piece of plain text.
    
    The script is stored in its unreversed form to make tokenizing possible.
    """

    @classmethod
    def from_file(cls, path: str) -> Script:
        """Returns a Script loaded from file or raises the appropriate error if reding the file fails."""
        log(f"Loading script from {path}...", LL_debug, 0)
        try:
            with open(path, "rt") as file:
                lines = file.readlines()
        except FileNotFoundError as err:
            log(f"Could not find {path}.", LL_error, 1)
            raise FileNotFoundError from err
        else:
            return Script(lines)

    def __init__(self, lines: List[str]) -> None:
        log("    Reversing madness...", LL_debug)
        for index, line in enumerate(lines):
            lines[index] = line[::-1]
        self.content = "".join(lines)
    
    def build(self) -> Code:
        """Compiles the Script into Code."""
        pass #TODO implement script build

    def run(self) -> None:
        pass #TODO implement script run
