import random
from SamSpeakCallable import *

class Random(SamSpeakCallable):
    def arity(self): return 0
    def call(self, interpreter, arguments):
        return random.random()
    def __repr__(self):
        return "<native fn random> generate a random number between 0 and 1"
class Randint(SamSpeakCallable):
    def arity(self): return 2
    def call(self, interpreter, arguments):
        return random.randint(arguments[0], arguments[1])
    def __repr__(self):
        return "<native fn randint> Genrate a random integer between the arguments inclusive"
class Choice(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        return random.choice(arguments[0])
    def __repr__(self):
        return "<native fn choice> Pick a random item out of a list"

builtins = {"random": Random(), "randint": Randint(), "choice": Choice()}
