import time
from SamSpeakCallable import *

class Now(SamSpeakCallable):
    def arity(self): return 0
    def call(self, interpeter, arguments):
        return time.time()
    def __repr__(self):
        return "<native fn now> Get current computer time"
class Pause(SamSpeakCallable):
    def arity(self): return 1
    def call(self, interpreter, arguments):
        time.sleep(arguments[0])
    def __repr__(self):
        return "<native fn pause> Pause for a number of seconds"

builtins = {"now": Now(), "pause": Pause()}
