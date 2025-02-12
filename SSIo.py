from SamSpeakCallable import *

class Input(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        return input(arguments[0])
    def __repr__(self):
        return "<native fn input> Output text to console then wait for user input and return it"
class Println(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        strignified = interpreter.stringify(arguments[0])
        print(strignified)
        return strignified
    def __repr__(self):
        return "<native fn println> Output text to the console"

builtins = {"input": Input(), "println": Println()}
