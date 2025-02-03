class SamSpeakRuntimeError(RuntimeError):
    def __init__(self, token, message):
        super().__init__(self, message)
        self.token = token
