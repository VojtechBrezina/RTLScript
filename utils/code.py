import struct

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
        return f"{k}:{self.data}"
    
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
    
    def put_instruction(self, instruction):
        return self.put_bytes(instruction, 1)
    
    def put_bytes(self, number, count):
        codes = [((number >> (i * 8)) & 0xFF) for i in range(count - 1, -1, -1)]
        self.instructions.extend(codes)
        return len(self.instructions) - count

    def get_bytes(self, pos, count):
        number = 0
        for i in range(0, count):
            number += self.instructions[pos + i] << ((count - 1 - i) * 8)
        return number
    
    def get_instruction(self, pos):
        return self.get_bytes(pos, 1)
    
    def get_number(self, pos):
        return struct.unpack(">d", bytes(self.instructions[pos:pos+8]))[0]
    
    def put_number(self, number):
        self.instructions.extend(struct.pack(">d", number))
        return len(self.instructions) - 8
    
    def __str__(self):
        data = "\n".join([f"        {d}" for d in self.data])
        i = " ".join([f"{i:02X}" for i in self.instructions])
        return f"    Data:\n{data}\n    Insructions:\n        {i}"
