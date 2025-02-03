from SamSpeakCallable import *
import time

class Clock(SamSpeakCallable):
    def arity(self): return 0
    def call(self, interpeter, arguments):
        return time.time()
    def __repr__(self):
        return "<native fn clock>"
class Input(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        return input(arguments[0])
    def __repr__(self):
        return "<native fn input>"
class Println(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        print(arguments[0])
        return arguments[0]
    def __repr__(self):
        return "<native fn println>"
