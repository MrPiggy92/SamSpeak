from SamSpeakRuntimeError import *

class SamSpeakInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}
    def __repr__(self):
        return f"<{self.klass.name} instance>"
    def get(self, name):
        if name.lexeme in self.fields.keys():
            return self.fields[name.lexeme]
        method = self.klass.findMethod(name.lexeme)
        if method != None: return method.bind(self)
        raise SamSpeakRuntimeError(name, f"Undefined property '{name.lexeme}'.")
    def set(self, name, value):
        self.fields[name.lexeme] = value
