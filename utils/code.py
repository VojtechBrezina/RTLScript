from __future__ import annotations

import struct
from typing import *

from utils.instructions import *

DK_string = 0

DK_names = {
    DK_string: "STRING"
}

class Data:
    """Represents one item in the `Code`'s data header."""

    def __init__(self, kind: int, data: Any) -> None:
        self.kind = kind
        self.data = data
    
    def serialize(self) -> List[int]:
        """Serializes the `Data` into an array of bytes for file output."""
        pass

    def __str__(self) -> str:
        k = DK_names[self.kind]
        v = self.data
        if self.kind == DK_string:
            v = v.replace("\n", "\\n")
        return f"{k}:{v}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, value: Code) -> bool:
        return self.kind == value.kind and self.data == value.data


class Code:
    """The runnable compiled code representation. 
    
    It has an array of static data like string literals and an array of 8-bit instructions
    """

    def __init__(self) -> None:
        self.data = []
        self.instructions = []
    
    def put_data(self, data: Data) -> int:
        """Inserts a new instance of the `Data` class and returns the new id.
        
        If the `Data` is equivalent to some existing item, returns the old id instead to save filesize.
        """
        if data in self.data:
            return self.data.index(data)
        self.data.append(data)
        return len(self.data) - 1
    
    def get_data(self, index: int) -> Data:
        """Retrieves a `Data` item with the given id."""
        return self.data[index]
    
    def put_instruction(self, instruction: int, pos: Any = None) -> int:
        """Shorthand for putting one byte into the instruction array. See `put_bytes()`."""
        return self.put_bytes(instruction, 1, pos)
        self.pu
    
    def put_bytes(self, number: int, count: int, pos: Any = None) -> int:
        """Puts a series of bytes represented by a single `int` into the instructions array at the desired position
        
        If `pos` is `None`, the bytes are appended at the end.
        Returns the posistion of the inserted data in the instructions array.
        """
        if pos == None:
            pos = len(self.instructions)
        while pos + count - 1 >= len(self.instructions):
            self.instructions.append(0)
        codes = [((number >> (i * 8)) & 0xFF) for i in range(count - 1, -1, -1)]
        for i, c in enumerate(codes):
            self.instructions[pos + i] = c
        return pos

    def get_bytes(self, pos: int, count: int) -> int:
        """Retrieves the sepicified amount of bytes from the instructions array and packs them into an `int`."""
        number = 0
        for i in range(0, count):
            number += self.instructions[pos + i] << ((count - 1 - i) * 8)
        return number
    
    def get_instruction(self, pos: int) -> int:
        """Shorthand for retrieving a single byte from the instruction array. see `get_bytes()`."""
        return self.get_bytes(pos, 1)
    
    def get_number(self, pos: int) -> float:
        """Retrieves 8 bytes from the instruction array and packs them into a `float` (RTLScript number)."""
        return struct.unpack(">d", bytes(self.instructions[pos:pos+8]))[0]
    
    def put_number(self, number: float, pos: Any = None) -> int:
        """Disassembles a `float` (RTLScript number) into 8 bytes and puts them into the instructions array.
        
        See `put_bytes()` for the behavior of `pos`.
        """
        if pos == None:
            pos = len(self.instructions)
        while pos + 8 - 1 >= len(self.instructions):
            self.instructions.append(0)
        codes = struct.pack(">d", number)
        for i, c in enumerate(codes):
            self.instructions[pos + i] = c
        return pos
    
    def __str__(self) -> str:
        from utils.instructions import instructions
        data = "\n".join([f"        {d}" for d in self.data])
        ir = " ".join([f"{i:02X}" for i in self.instructions])
        pos = 0
        i = ""
        try:
            while pos < len(self.instructions):
                code = self.get_instruction(pos)
                pos += 1
                decomp_str = instructions[code].decomp_str
                ii, decomp_str = decomp_str.split(",")
                i += str(pos - 1).rjust(9, "-") + " " + ii + " "
                for c in decomp_str:
                    if c == "i":
                        i += str(self.get_bytes(pos, 4))
                        pos += 4
                    elif c == "n":
                        i += str(self.get_number(pos))
                        pos += 8
                    i += ", "
                i = i[:(-2 if len(decomp_str) != 0 else -1)]
                i += "\n        "
            i = i[:-9]
        except:
            pass
        return f"    Data:\n{data}\n    Instructions:\n        {ir}\n    Decomposed:\n        {i}"
