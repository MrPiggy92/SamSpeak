from SamSpeakCallable import *

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

builtins = {"length": Length(), "split": Split(), "keys": Keys()}
