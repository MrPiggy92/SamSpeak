import sys
if __name__ == "__main__":
    from Scanner import *
    from parser import *
    from Interpreter import *
    from Resolver import *
    from Preprocessor import *

class SamSpeak:
    def __init__(self):
        self.hadError = False
        self.hadRuntimeError = False
        self.interpreter = Interpreter(self)
    def main(self):
        #if len(sys.argv) > 2:
        #    print("Usage: python3 SamSpeak.py [script]")
        #    exit(64)
        if len(sys.argv) >= 2:
            self.runFile(sys.argv[1])
        else:
            self.runPrompt()
    def runFile(self, path):
        with open(path) as file:
            code = file.read()
        self.run(code, path)
        if self.hadError: exit(65)
        if self.hadRuntimeError: exit(70)
    def runPrompt(self):
        while True:
            line = input(" > ").strip()
            if line == None: break
            self.run(line)
            self.hadError = False
    def run(self, source, fileName=False):
        try:
            preprocessor = Preprocessor(fileName, self, source)
            source = '\n'.join(preprocessor.preprocess())
            scanner = Scanner(source, self)
            tokens = scanner.scanTokens()
            parser = Parser(tokens, self, fileName)
            if fileName:
                args = list(sys.argv)
                args.pop(0)
                args.pop(0)
                statements = parser.parse(args)
            else:
                statements = parser.parse()
            #print('\n\n'.join([str(statement) for statement in statements]))
            #print('\n\n'.join([str(statement) for statement in statements[0].body]))
            if self.hadError: return
            resolver = Resolver(self.interpreter, self)
            resolver.resolve(statements)
            if self.hadError: return
            self.interpreter.interpret(statements)
        except KeyboardInterrupt:
            print("Cancel")
            self.hadError = True
            return
        #print(expr)
        #for token in tokens:
        #    print(token)
    def error(self, line, message):
        print("ScanError")
        self.report(line, '', message)
    def parseError(self, token, message):
        print("ParseError")
        if token.type == "EOF": 
            self.report(token.line, "at end", message)
        else:
            self.report(token.line, f"at '{token.lexeme}'", message)
    def report(self, line, where, message):
        print(f"[line {line}] Error{(' ' + where) if where != '' else where}: {message}")
        self.hadError = True
    def runtimeError(self, e):
        print("RUNTIME")
        print(f"[line {e.token.line}] {str(e.args[1])}")
        self.hadRuntimeError = True
SamSpeak = SamSpeak()
SamSpeak.main()
