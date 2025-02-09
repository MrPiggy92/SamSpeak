from Expr import *
from Stmt import *
from Token import *

class Parser:
    def __init__(self, tokens, SamSpeak, runFromFile):
        self.tokens = tokens
        self.current = 0
        self.SamSpeak_class = SamSpeak
        self.file = runFromFile
    def parse(self, args=None):
        self.currentBlock = False
        self.mainFunction = False
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
            if statements[-1] == None:
                statements.pop()
        if self.file:
            betterArgs = List([Literal(value) for value in args])
            if not self.mainFunction:
                self.error(self.tokens[-1], "No main function.")
            mainCall = Call(Variable(Token("IDENTIFIER", "main", "main", -1)), Token("RIGHT_PAREN", None, ')', -1), [betterArgs])
            statements.append(mainCall)
        return statements
    def declaration(self):
        try:
            if self.match("VAR"): return self.varDeclaration()
            elif self.match("FN"): return self.function("function")
            elif self.match("CLASS"): return self.classDeclaration()
            return self.statement()
        except ParseError:
            self.synchronise()
            return None
    def varDeclaration(self):
        name = self.consume("IDENTIFIER", "Expect variable name.")
        initialiser = None
        if self.match("COLON_EQUAL", "EQUAL"):
            initialiser = self.expression()
        elif self.match("EQUAL"):
            self.error(self.previous(), "Can't declare variables without :=")
            raise self.error(self.previous(), "Can't declare variables without :=")
        self.consume("SEMICOLON", "Expect ';' after variable declaration.")
        return Var(name, initialiser)
    def classDeclaration(self):
        name = self.consume("IDENTIFIER", "Expect class name.")
        superclass = None
        if self.match("LESS"):
            self.consume("IDENTIFIER", "Expect superclass name.")
            superclass = Variable(self.previous())
        self.consume("LEFT_BRACE", "Expect '{' before class body")
        methods = []
        while not(self.check("RIGHT_BRACE")) and not(self.isAtEnd()):
            methods.append(self.function("method"))
        self.consume("RIGHT_BRACE", "Expect '}' after class body")
        return Class(name, superclass, methods)
    def statement(self):
        stmt = None
        if self.match("PRINT"): stmt = self.printStatement()
        elif self.match("IF"): stmt = self.ifStatement()
        elif self.match("WHILE"): stmt = self.whileStatement()
        elif self.match("FOR"): stmt = self.forStatement()
        elif self.match("LEFT_BRACE"): stmt = Block(self.block())
        elif self.match("RETURN"): stmt = self.returnStatement()
        if stmt == None: stmt = self.expressionStatement()
        if not self.currentBlock and self.file:
            self.error(self.previous(), "Outside of main function, you can only declare things.")
            return
        return stmt
    def ifStatement(self):
        self.consume("LEFT_PAREN", "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume("RIGHT_PAREN", "Expect ')' after if condition.")
        thenBranch = self.statement()
        elseBranch = None
        if self.match("ELSE"):
            elseBranch = self.statement()
        return If(condition, thenBranch, elseBranch)
    def whileStatement(self):
        self.consume("LEFT_PAREN", "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume("RIGHT_PAREN", "Expect ')' after while condition.")
        body = self.statement()
        return While(condition, body)
    def forStatement(self):
        self.consume("LEFT_PAREN", "Expect '(' after 'for'.")
        if self.match("SEMICOLON"):
            initialiser = None
        elif self.match("VAR"):
            initialiser = self.varDeclaration()
        else:
            initialiser = self.expressionStatement()
        if not self.check("SEMICOLON"):
            condition = self.expression()
        else:
            condition = None
        self.consume("SEMICOLON", "Expect ';' after loop condition.")
        if not self.check("RIGHT_PAREN"):
            increment = self.expression()
        else:
            increment = None
        self.consume("RIGHT_PAREN", "Expect ')' after for clauses.")
        body = self.statement()
        if increment != None:
            body = Block([body, Expression(increment)])
        if condition == None: condition = Literal(True)
        body = While(condition, body)
        if initialiser != None:
            body = Block([initialiser, body])
        return body
    def returnStatement(self):
        keyword = self.previous()
        value = None
        if not self.check("SEMICOLON"):
            value = self.expression()
        self.consume("SEMICOLON", "Expect ';' after return value.")
        return Return(keyword, value)
    def expressionStatement(self):
        expr = self.expression()
        #print(type(expr))
        #print(type(expr.arguments))
        #print(type(expr.arguments[0]))
        #print(expr.arguments)
        #print(expr.arguments[0])
        #print(expr.arguments[0].name)
        self.consume("SEMICOLON", "Expect ';' after value.")
        return Expression(expr)
    def function(self, kind):
        name = self.consume("IDENTIFIER", f"Expect {kind} name.")
        self.consume("LEFT_PAREN", f"Expect '(' after {kind} name.")
        parameters = []
        if not self.check("RIGHT_PAREN"):
            parameters.append(self.consume("IDENTIFIER", "Expect paramter name."))
            while self.match("COMMA"):
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 paramaters.")
                parameters.append(self.consume("IDENTIFIER", "Expect paramter name."))
        self.consume("RIGHT_PAREN", "Expect ')' after parameters.")
        self.consume("LEFT_BRACE", "Expect '{' before " + kind + " body.")
        body = self.block()
        if name.lexeme == "main": self.mainFunction = True
        return Function(name, parameters, body)
    def block(self):
        previousBlock = self.currentBlock
        self.currentBlock = True
        statements = []
        while (not self.check("RIGHT_BRACE")) and (not self.isAtEnd()):
            statements.append(self.declaration())
        self.consume("RIGHT_BRACE", "Expect '}' after block.")
        self.currentBlock = previousBlock
        return statements
    def assignment(self):
        expr = self.type_cast()
        #print(expr)
        #print(self.peek())
        if self.match("EQUAL"):
            equals = self.previous()
            value = self.assignment()
            #print(expr)
            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)
            elif type(expr) == Get:
                get = expr
                return Set(get.object, get.name, value)
            elif type(expr) == Access:
                #print(expr.accessee)
                return ChAccess(expr.accessee, expr.index, value)
            self.error(equals, "Invalid assignment target.")
        elif self.match("PLUS_EQUAL"):
            equals = self.previous()
            value = self.assignment()
            value = Binary(expr, Token("PLUS", '+', None, equals.line), value)
            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)
            elif type(expr) == Get:
                get = expr
                return Set(get.object, get.name, value)
            self.error(equals, "Invalid assignment target.")
        elif self.match("MINUS_EQUAL"):
            equals = self.previous()
            value = self.assignment()
            value = Binary(expr, Token("MINUS", '-', None, equals.line), value)
            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)
            elif type(expr) == Get:
                get = expr
                return Set(get.object, get.name, value)
            self.error(equals, "Invalid assignment target.")
        elif self.match("STAR_EQUAL"):
            equals = self.previous()
            value = self.assignment()
            value = Binary(expr, Token("STAR", '*', None, equals.line), value)
            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)
            elif type(expr) == Get:
                get = expr
                return Set(get.object, get.name, value)
            self.error(equals, "Invalid assignment target.")
        elif self.match("SLASH_EQUAL"):
            equals = self.previous()
            value = self.assignment()
            value = Binary(expr, Token("SLASH", '/', None, equals.line), value)
            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)
            elif type(expr) == Get:
                get = expr
                return Set(get.object, get.name, value)
            self.error(equals, "Invalid assignment target.")
        elif self.match("MODULO_EQUAL"):
            equals = self.previous()
            value = self.assignment()
            value = Binary(expr, Token("MODULO", '%', None, equals.line), value)
            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)
            elif type(expr) == Get:
                get = expr
                return Set(get.object, get.name, value)
            self.error(equals, "Invalid assignment target.")
        elif self.match("UP_ARROW_EQUAL"):
            equals = self.previous()
            value = self.assignment()
            value = Binary(expr, Token("UP_ARROW", '^', None, equals.line), value)
            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)
            elif type(expr) == Get:
                get = expr
                return Set(get.object, get.name, value)
            self.error(equals, "Invalid assignment target.")
        elif self.match("PLUS_PLUS"):
            equals = self.previous()
            value = Literal(1.0)
            value = Binary(expr, Token("PLUS", '+', None, equals.line), value)
            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)
            elif type(expr) == Get:
                get = expr
                return Set(get.object, get.name, value)
            self.error(equals, "Invalid assignment target.")
        elif self.match("MINUS_MINUS"):
            equals = self.previous()
            value = Literal(1.0)
            value = Binary(expr, Token("MINUS", '-', None, equals.line), value)
            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)
            elif type(expr) == Get:
                get = expr
                return Set(get.object, get.name, value)
            self.error(equals, "Invalid assignment target.")
        return expr
    def type_cast(self):
        left = self.map()
        while self.match("COLON"):
            colon = self.previous()
            right = self.map()
            left = TypeCast(left, colon, right)
        return left
    def map(self):
        if self.match("LEFT_BRACE"):
            keys = []
            values = []
            while not self.match("RIGHT_BRACE"):
                item1 = self.list()
                #print(item1)
                self.consume("COLON", "Expect ':' between map items.")
                item2 = self.list()
                #print(item2)
                keys.append(item1)
                values.append(item2)
                #print()
            return Map(keys, values)
        else:
            return self.list()
    def list(self):
        if self.match("LEFT_BRACKET"):
            contents = []
            while not self.match("RIGHT_BRACKET"):
                item = self.logicalOr()
                contents.append(item)
            return List(contents)
        else:
            return self.logicalOr()
    def logicalOr(self):
        expr = self.logicalAnd()
        while self.match("OR"):
            operator = self.previous()
            right = self.logicalAnd()
            expr = Logical(expr, operator, right)
        return expr
    def logicalAnd(self):
        expr = self.equality()
        while self.match("AND"):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        return expr
    def expression(self):
        return self.assignment()
    def equality(self):
        expr = self.comparison()
        while self.match("BANG_EQUAL", "EQUAL_EQUAL"):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr
    def comparison(self):
        expr = self.mod()
        while self.match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = self.previous()
            right = self.mod()
            expr = Binary(expr, operator, right)
        return expr
    def mod(self):
        expr = self.term()
        while self.match("MODULO", "UP_ARROW", "DOTDOT"):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
    def term(self):
        expr = self.factor()
        while self.match("MINUS", "PLUS"):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    def factor(self):
        expr = self.unary()
        while self.match("STAR", "SLASH"):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr
    def unary(self):
        if self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.access()
    def access(self):
        expr = self.call()
        #print(expr)
        while True:
            if self.match("LEFT_BRACKET"):
                index = self.call()
                close = self.consume("RIGHT_BRACKET", "Expect ']' after list access.")
                expr = Access(expr, close, index)
            else:
                break
        return expr
    def call(self):
        expr = self.lam()
        while True:
            if self.match("LEFT_PAREN"):
                expr = self.finishCall(expr)
            elif self.match("DOT"):
                name = self.consume("IDENTIFIER", "Expect property name after '.'.")
                expr = Get(expr, name)
            else:
                break
        return expr
    def lam(self):
        if self.match("LM"):
            self.consume("LEFT_PAREN", f"Expect '(' after 'lm'.")
            parameters = []
            if not self.check("RIGHT_PAREN"):
                parameters.append(self.consume("IDENTIFIER", "Expect paramter name."))
                while self.match("COMMA"):
                    if len(parameters) >= 255:
                        self.error(self.peek(), "Can't have more than 255 paramaters.")
                    parameters.append(self.consume("IDENTIFIER", "Expect paramter name."))
            self.consume("RIGHT_PAREN", "Expect ')' after parameters.")
            self.consume("LEFT_BRACE", "Expect '{' before lambda body.")
            body = self.block()
            return Lambda(parameters, body)
        else:
            return self.primary()
    def primary(self):
        if self.match("TRUE"): return Literal(True)
        elif self.match("FALSE"): return Literal(False)
        elif self.match("NIL"): return Literal(None)
        elif self.match("NUMBER", "STRING"):
            return Literal(self.previous().literal)
        elif self.match("SUPER"):
            keyword = self.previous()
            self.consume("DOT", "Expect '.' after 'super'.")
            method = self.consume("IDENTIFIER", "Expect superclass method name.")
            return Super(keyword, method)
        elif self.match("ME"):
            return Me(self.previous())
        elif self.match("IDENTIFIER"):
            #print(self.previous())
            return Variable(self.previous())
        elif self.match("NUM", "STR", "NIL", "BOOL", "LIST"):
            return Type(self.previous())
        elif self.match("LEFT_PAREN"):
            expr = self.expression()
            self.consume("RIGHT_PAREN", "Expect ')' after expression.")
            return Grouping(expr)
        #if type(self.statements[-1]) == Function:
        #    
        raise self.error(self.peek(), "Expect expression.")
    def finishCall(self, callee):
        arguments = []
        if not self.check("RIGHT_PAREN"):
            arguments.append(self.expression())
            while self.match("COMMA"):
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
        paren = self.consume("RIGHT_PAREN", "Expect ')' after arguments")
        return Call(callee, paren, arguments)
    def match(self, *args):
        for type in args:
            if self.check(type):
                self.advance()
                return True
        return False
    def check(self, type):
        if self.isAtEnd(): return False
        return self.peek().type == type
    def isAtEnd(self):
        return self.peek().type == "EOF"
    def peek(self):
        return self.tokens[self.current]
    def advance(self):
        if not self.isAtEnd(): self.current += 1
        return self.previous()
    def previous(self):
        return self.tokens[self.current-1]
    def consume(self, token, message):
        if self.check(token): return self.advance()
        self.error(self.peek(), message)
        raise self.error(self.peek(), message)
    def error(self, token, message):
        self.SamSpeak_class.parseError(token, message)
        return ParseError()
    def synchronise(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == "SEMICOLON": return
            nextType = self.peek().type
            if nextType in ["CLASS", "FN", "VAR", "FOR", "IF", "WHILE", "RETURN"]:
                return
            self.advance()
class ParseError(RuntimeError):
    pass
