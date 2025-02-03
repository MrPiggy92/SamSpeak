from SamSpeakRuntimeError import *

class Environment:
    def __init__(self, *args):
        if len(args) > 0:
            self.enclosing = args[0]
        else:
            self.enclosing = None
        self.values = {}
    def define(self, name, value):
        self.values[name] = value
    def ancestor(self, distance):
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment
    def get(self, name):
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        elif self.enclosing != None:
            return self.enclosing.get(name)
        raise SamSpeakRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
    def getAt(self, distance, name):
        return self.ancestor(distance).values[name]
    def assignAt(self, distance, name, value):
        self.ancestor(distance).values[name.lexeme] = value
    def assign(self, name, value):
        #print(f"Assigning value {str(value)} to variable {name}")
        if name.lexeme in self.values.keys():
            #print("found")
            self.values[name.lexeme] = value
            #print(self.values[name.lexeme])
            return
        elif self.enclosing != None:
            self.enclosing.assign(name, value)
            return
        #print(self.values[name.lexeme])
        raise SamSpeakRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
