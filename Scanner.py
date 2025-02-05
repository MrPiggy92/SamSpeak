from Token import Token

class Scanner:
    keywords = [
        "and", "class", "else", "false",
        "for", "fn", "if", "nil",
        "or", "return", "super",
        "me", "true", "var", "while",
    ]
    types = [
        "Num", "Str", "Nil", "Bool", "List"
    ]
    def __init__(self, source, SamSpeak):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.SamSpeak_class = SamSpeak
    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens
    def isAtEnd(self):
        return self.current >= len(self.source)
    def scanToken(self):
        c = self.advance()
        if c == '(': self.addSingleToken("LEFT_PAREN")
        elif c == ')': self.addSingleToken("RIGHT_PAREN")
        elif c == '{': self.addSingleToken("LEFT_BRACE")
        elif c == '}': self.addSingleToken("RIGHT_BRACE")
        elif c == '[': self.addSingleToken("LEFT_BRACKET")
        elif c == ']': self.addSingleToken("RIGHT_BRACKET")
        elif c == ',': self.addSingleToken("COMMA")
        elif c == '.':
            if self.match('.'):
                self.addSingleToken("DOTDOT")
            else:
                self.addSingleToken("DOT")
        elif c == ':':
            if self.match('='): self.addSingleToken("COLON_EQUAL")
            else: self.addSingleToken("COLON")
        elif c == '-': self.addSingleToken("MINUS")
        elif c == '+': self.addSingleToken("PLUS")
        elif c == ';': self.addSingleToken("SEMICOLON")
        elif c == '*': self.addSingleToken("STAR")
        elif c == '%': self.addSingleToken("MODULO")
        elif c == '^': self.addSingleToken("UP_ARROW")
        elif c == '!': self.addSingleToken("BANG_EQUAL" if self.match('=') else "BANG")
        elif c == '=': self.addSingleToken("EQUAL_EQUAL" if self.match('=') else "EQUAL")
        elif c == '<': self.addSingleToken("LESS_EQUAL" if self.match('=') else "LESS")
        elif c == '>': self.addSingleToken("GREATER_EQUAL" if self.match('=') else "GREATER")
        elif c == '/':
            if self.match('/'):
                while self.peek() != "\n" and not self.isAtEnd(): self.advance()
            else:
                self.addSingleToken("SLASH")
        elif c == '"': self.string()
        elif self.isDigit(c): self.number()
        elif self.isAlpha(c): self.identifier()
        elif c in [' ', "\r", "\t"]: pass
        elif c == "\n": self.line += 1
        else: self.SamSpeak_class.error(self.line, f"Unexpected character ({c}).")
    def advance(self):
        self.current += 1
        return self.source[self.current-1]
    def addSingleToken(self, type):
        self.addToken(type,None)
    def addToken(self, type, literal):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
    def match(self, char):
        if self.isAtEnd(): return False
        if self.source[self.current] != char: return False
        self.current += 1
        return True
    def peek(self):
        if self.isAtEnd(): return "\0"
        return self.source[self.current]
    def peekNext(self):
        if self.current + 1 > len(self.source): return "\0"
        return self.source[self.current+1]
    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == "\n": self.line += 1
            self.advance()
        if self.isAtEnd():
            self.SamSpeak_class.error(self.line, "Unterminated string.")
            return
        self.advance()
        value = self.source[self.start+1 : self.current-1]
        self.addToken("STRING", value)
    def isDigit(self, char):
        return char <= "9" and char >= "0"
    def number(self):
        while self.isDigit(self.peek()): self.advance()
        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()
            while self.isDigit(self.peek()): self.advance()
        num = float(self.source[self.start : self.current])
        self.addToken("NUMBER", num)
    def isAlpha(self, char):
        return (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or (char == '_')
    def isAlphaNumeric(self, char):
        return self.isDigit(char) or self.isAlpha(char)
    def identifier(self):
        while self.isAlphaNumeric(self.peek()): self.advance()
        text = self.source[self.start : self.current]
        if text in self.keywords:
            self.addSingleToken(text.upper())
            return
        elif text in self.types:
            self.addSingleToken(text.upper())
            return
        self.addToken("IDENTIFIER", text)
