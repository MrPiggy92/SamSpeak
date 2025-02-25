from SamSpeakInstance import *

class SamSpeakClass:
    def __init__(self, name, superclass, methods):
        self.name = name
        self.methods = methods
        self.superclass = superclass
    def __repr__(self):
        return f"<{self.name} class>"
    def new(self):
        instance = SamSpeakInstance(self)
        return instance
    #def arity(self):
    #    initialiser = self.findMethod("new")
    #    if initialiser == None: return 0
    #    return initialiser.arity()
    def findMethod(self, name):
        if name in self.methods.keys():
            return self.methods[name]
        if self.superclass != None:
            return self.superclass.findMethod(name)
        return None
