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
class Length(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        if type(arguments[0]) == list:
            return float(len(arguments[0]))
        elif type(arguments[0]) == str:
            return float(len(arguments[0]))
        elif type(arguments[0]) == dict:
            return float(len(arguments[0].keys()))
        elif type(arguments[0]) == float:
            text = str(arguments[0])
            if text[-2:] == ".0":
                text = text[:-2]
            text = text.replace('.', '')
            return float(len(text))
        elif type(arguments[0]) == bool: return 1.0
    def __repr__(self):
        return "<native fn length> Find length of object"
class Split(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        return arguments[0].split()
    def __repr__(self):
        return "<native fn split> Split a string along the spaces into a list"
class Keys(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        return list(arguments[0].keys())
    def __repr__(self):
        return "<native fn keys> Get the keys to a map"
