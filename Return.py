from SamSpeakRuntimeError import *
class Return(SamSpeakRuntimeError):
    def __init__(self, value):
        self.value = value
