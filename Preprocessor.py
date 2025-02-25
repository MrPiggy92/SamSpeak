import os

class Preprocessor:
    def __init__(self, filename, SamSpeak, code):
        self.filesRead = [filename]
        self.SamSpeak = SamSpeak
        self.code = code.split('\n')
    def preprocess(self):
        for num, line in enumerate(self.code):
            if line.startswith('#'):
                self.code.pop(num)
                if not os.path.exists(f"{line[1:]}.ss"):
                    self.SamSpeak.scanError(num+1, "This file doesn't exist!")
                    continue
                if f"{line[1:]}.ss" in self.filesRead:
                    continue
                else:
                    self.filesRead.append(f"{line[1:]}.ss")
                with open(f"{line[1:]}.ss") as file:
                    lineNum = 0
                    for line in file.readlines():
                        self.code.insert(num+lineNum, line.strip())
                        lineNum += 1
                self.code = self.preprocess()
            elif line.startswith('!'):
                #print(line[1:])
                self.code.pop(num)
                self.SamSpeak.interpreter.addModule(line[1:])
                self.code = self.preprocess()
        return self.code
