class Preprocessor:
    def __init__(self, filename, SamSpeak, code):
        self.filesRead = [filename]
        self.SamSpeak = SamSpeak
        self.code = code.split('\n')
    def preprocess(self):
        for num, line in enumerate(self.code):
            if line.startswith('#'):
                if f"{line[1:]}.ss" in self.filesRead:
                    continue
                else:
                    self.filesRead.append(f"{line[1:]}.ss")
                self.code.pop(num)
                with open(f"{line[1:]}.ss") as file:
                    lineNum = 0
                    for line in file.readlines():
                        self.code.insert(num+lineNum, line.strip())
                        lineNum += 1
                self.code = self.preprocess()
        return self.code
