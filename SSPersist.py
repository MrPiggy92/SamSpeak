import yaml

from SamSpeakCallable import *

class Dumps(SamSpeakCallable):
    def arity(self): return 2
    def call(self, interpreter, arguments):
        if arguments[0] == "yaml":
            return yaml.dump(arguments[1])
    def __repr__(self):
        return "<native fn dumps> Return a string containing the encoded data"
class Loadf(SamSpeakCallable):
    def arity(self): return 2
    def call(self, interpreter, arguments):
        if arguments[0] == "yaml":
            with open(arguments[1]) as file:
                return yaml.safe_load(file)
    def __repr__(self):
        return "<native fn loadf> Load and decode data from a file"


builtins = {"dumps": Dumps(), "loadf": Loadf()}
