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
        strignified = self.stringify(arguments[0])
        print(strignified)
        return strignified
    def __repr__(self):
        return "<native fn println>"
    def stringify(self, value):
        if value == None: return "nil"
        if type(value) == float:
            text = str(value)
            if text[-2:] == ".0":
                text = text[:-2]
            return text
        elif type(value) == list:
            strList = [self.stringify(item) for item in value]
            stringified = '['
            stringified += ' '.join(strList)
            stringified += ']'
            return stringified
        return str(value)
