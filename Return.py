from SamSpeakRuntimeError import *
class SSReturn(SamSpeakRuntimeError):
    def __init__(self, value):
        self.value = value
