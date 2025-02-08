from SamSpeakCallable import *
import time, random

class Clock(SamSpeakCallable):
    def arity(self): return 0
    def call(self, interpeter, arguments):
        return time.time()
    def __repr__(self):
        return "<native fn clock> Get current computer time"
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
class Random(SamSpeakCallable):
    def arity(self): return 0
    def call(self, interpreter, arguments):
        return random.random()
    def __repr__(self):
        return "<native fn random> generate a random number between 0 and 1"
class Round(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        return float(round(arguments[0]))
    def __repr__(self):
        return "<native fn round> round numbers to nearest integer"
