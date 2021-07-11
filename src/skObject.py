from enum import Enum

class Types(Enum):
    Number = 0
    Array = 1
    String = 2

class Object:
    def __init__(self, value, _type):
        self.value = value
        self.type= _type

    def copy(self):
        return Object(self.value, self.type)

    def __str__(self):
        val_str = repr(self.value)
        return f"Object({val_str}, {self.type})"

