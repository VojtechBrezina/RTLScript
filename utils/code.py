import struct

from utils.instructions import *

DK_string = 0

DK_names = {
    DK_string: "STRING"
}

class Data:
    def __init__(self, kind, data):
        self.kind = kind
        self.data = data
    
    def serialize(self):
        pass

    def __str__(self):
        k = DK_names[self.kind]
        v = self.data
        if self.kind == DK_string:
            v = v.replace("\n", "\\n")
        return f"{k}:{v}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, value):
        return self.kind == value.kind and self.data == value.data


class Code:
    def __init__(self):
        self.data = []
        self.instructions = []
    
    def put_data(self, data):
        if data in self.data:
            return self.data.index(data)
        self.data.append(data)
        return len(self.data) - 1
    
    def get_data(self, index):
        return self.data[index]
    
    def put_instruction(self, instruction, pos = None):
        return self.put_bytes(instruction, 1, pos)
    
    def put_bytes(self, number, count, pos = None):
        if pos == None:
            pos = len(self.instructions)
        while pos + count - 1 >= len(self.instructions):
            self.instructions.append(0)
        codes = [((number >> (i * 8)) & 0xFF) for i in range(count - 1, -1, -1)]
        for i, c in enumerate(codes):
            self.instructions[pos + i] = c
        return pos

    def get_bytes(self, pos, count):
        number = 0
        for i in range(0, count):
            number += self.instructions[pos + i] << ((count - 1 - i) * 8)
        return number
    
    def get_instruction(self, pos):
        return self.get_bytes(pos, 1)
    
    def get_number(self, pos):
        return struct.unpack(">d", bytes(self.instructions[pos:pos+8]))[0]
    
    def put_number(self, number, pos = None):
        if pos == None:
            pos = len(self.instructions)
        while pos + 8 - 1 >= len(self.instructions):
            self.instructions.append(0)
        codes = struct.pack(">d", number)
        for i, c in enumerate(codes):
            self.instructions[pos + i] = c
        return pos
    
    def __str__(self):
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
                i += ii + " "
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
        return f"    Data:\n{data}\n    Insructions:\n        {ir}\n    Decomposed:\n        {i}"
