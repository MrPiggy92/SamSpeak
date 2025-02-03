from SamSpeakCallable import *
from SamSpeakInstance import *

class SamSpeakClass(SamSpeakCallable):
    def __init__(self, name, superclass, methods):
        self.name = name
        self.methods = methods
        self.superclass = superclass
    def __repr__(self):
        return self.name
    def call(self, interpreter, arguments):
        instance = SamSpeakInstance(self)
        initialiser = self.findMethod("init")
        if initialiser != None:
            initialiser.bind(instance).call(interpreter, arguments)
        return instance
    def arity(self):
        initialiser = self.findMethod("init")
        if initialiser == None: return 0
        return initialiser.arity()
    def findMethod(self, name):
        if name in self.methods.keys():
            return self.methods[name]
        if self.superclass != None:
            return self.superclass.findMethod(name)
        return None
