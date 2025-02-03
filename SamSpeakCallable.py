class SamSpeakCallable:
    def __init__(self, callee=None):
        if callee != None:
            self.call = callee.call
            self.arity = callee.arity
    def call(self, interpeter, arguments):
        pass
    def arity(self):
        pass
