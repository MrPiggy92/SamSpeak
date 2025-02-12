from SamSpeakCallable import *
import math

class Round(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        return float(round(arguments[0]))
    def __repr__(self):
        return "<native fn round> round numbers to nearest integer"
class Floor(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        return float(int(arguments[0]))
    def __repr__(self):
        return "<native fn floor> Round numbers down to the nearest integer"
class Ceil(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpeter, arguments):
        return float(int(arguments[0]+1))
    def __repr__(self):
        return "<native fn ceil> Round numbers up to the nearest integer"
class Sqrt(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpeter, arguments):
        return float(math.sqrt(arguments[0]))
    def __repr__(self):
        return "<native fn sqrt> Get sqare root of a number"
builtins = {"round": Round(), "floor": Floor(), "ceil": Ceil(), "sqrt": Sqrt()}
