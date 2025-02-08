from Environment import *
from SamSpeakCallable import *
from Return import *

class SamSpeakFunction(SamSpeakCallable):
    def __init__(self, declaration, closure, isInitialiser):
        self.isInitialiser = isInitialiser
        self.declaration = declaration
        self.closure = closure
    def call(self, interpreter, arguments):
        #print(arguments)
        #interpreter.currentBlock = "FUNC"
        environment = Environment(self.closure)
        for param, arg in zip(self.declaration.params, arguments):
            #print(param.lexeme)
            #print(arg)
            #print()
            environment.define(param.lexeme, arg)
            #print(environment.values)
        try:
            interpreter.executeBlock(self.declaration.body, environment)
            #interpreter.currentBlock = "NONE"
        except Return as e:
            if self.isInitialiser: return self.closure.getAt(0, "me")
            return e.value
        if self.isInitialiser: return self.closure.getAt(0, "me")
        return None
    def arity(self):
        return len(self.declaration.params)
    def __repr__(self):
        try:
            return f"<fn {self.declaration.name.lexeme}>"
        except:
            return "<lambda fn>"
    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define("me", instance)
        return SamSpeakFunction(self.declaration, environment, self.isInitialiser)
