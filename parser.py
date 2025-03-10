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
                self.error(self.tokens[-1], "You haven't even made a main function!")
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
        name = self.consume("IDENTIFIER", "You're meant to tell us the variable name!")
        initialiser = None
        if self.match("COLON_EQUAL", "EQUAL"):
            initialiser = self.expression()
        return Var(name, initialiser)
    def classDeclaration(self):
        name = self.consume("IDENTIFIER", "You're meant to tell us the class name!")
        superclass = None
        if self.match("LESS"):
            self.consume("IDENTIFIER", "I need to know the name of the superclass!")
            superclass = Variable(self.previous())
        self.consume("COLON", "I need a colon before the class body, you know!")
        methods = []
        while not(self.check("SEMICOLON")) and not(self.isAtEnd()):
            methods.append(self.function("method"))
        self.consume("SEMICOLON", "You need to close the class body!")
        return Class(name, superclass, methods)
    def statement(self):
        stmt = None
        if self.match("PRINT"): stmt = self.printStatement()
        elif self.match("IF"): stmt = self.ifStatement()
        elif self.match("WHILE"): stmt = self.whileStatement()
        elif self.match("FOR"): stmt = self.forStatement()
        elif self.match("TRY"): stmt = self.tryStatement()
        elif self.match("COLON"): stmt = Block(self.block())
        elif self.match("RETURN"): stmt = self.returnStatement()
        elif self.match("RAISE"): stmt = self.raiseStatement()
        if stmt == None: stmt = self.expressionStatement()
        if not self.currentBlock and self.file:
            self.error(self.previous(), "Outside of the main function, you can only declare things! How do you not know this?")
            return
        return stmt
    def ifStatement(self):
        self.consume("LEFT_PAREN", "I need a '(' after 'if'!")
        condition = self.expression()
        self.consume("RIGHT_PAREN", "I need a '(' after an if condition!")
        thenBranch = self.statement()
        elseBranch = None
        if self.match("ELSE"):
            elseBranch = self.statement()
        return If(condition, thenBranch, elseBranch)
    def whileStatement(self):
        self.consume("LEFT_PAREN", "I need a '(' after 'while'!")
        condition = self.expression()
        #print(condition)
        self.consume("RIGHT_PAREN", "I need a ')' after a while condition!")
        body = self.statement()
        return While(condition, body)
    def forStatement(self):
        self.consume("LEFT_PAREN", "I need a '(' after 'for'!")
        if self.match("SEMICOLON"):
            initialiser = None
        elif self.match("VAR"):
            initialiser = self.varDeclaration()
            self.consume("SEMICOLON", "I expect ';' after initialiser, you know!")
        else:
            initialiser = self.expressionStatement()
        if not self.check("SEMICOLON"):
            condition = self.expression()
        else:
            condition = None
        self.consume("SEMICOLON", "I expect ';' after condition, you know!")
        if not self.check("RIGHT_PAREN"):
            increment = self.expression()
        else:
            increment = None
        self.consume("RIGHT_PAREN", "I need ')' after for clauses!")
        body = self.statement()
        if increment != None:
            body = Block([body, Expression(increment)])
        if condition == None: condition = Literal(True)
        body = While(condition, body)
        if initialiser != None:
            body = Block([initialiser, body])
        return body
    def tryStatement(self):
        content = self.statement()
        if self.match("CATCH"):
            catch = self.statement()
        else:
            catch = None
        return Try(content, catch)
    def returnStatement(self):
        keyword = self.previous()
        value = self.expression()
        #if not self.check("SEMICOLON"):
        #    value = self.expression()
        #self.consume("SEMICOLON", "Expect ';' after return value.")
        return Return(keyword, value)
    def raiseStatement(self):
        keyword = self.previous()
        value = self.expression()
        return Raise(keyword, value)
    def expressionStatement(self):
        expr = self.expression()
        #print(type(expr))
        #print(type(expr.arguments))
        #print(type(expr.arguments[0]))
        #print(expr.arguments)
        #print(expr.arguments[0])
        #print(expr.arguments[0].name)
        #self.consume("SEMICOLON", "Expect ';' after value.")
        return Expression(expr)
    def function(self, kind):
        name = self.consume("IDENTIFIER", f"You need to tell me the name of the {kind}!")
        self.consume("LEFT_PAREN", f"You must always press '(' after {kind} name!")
        parameters = []
        if not self.check("RIGHT_PAREN"):
            parameters.append(self.consume("IDENTIFIER", "Why don't you want to tell me the parameter name!?"))
            while not self.check("RIGHT_PAREN") and not self.isAtEnd():
                if len(parameters) >= 255:
                    self.error(self.peek(), "You can't have more than 255 paramaters! That's just greedy")
                parameters.append(self.consume("IDENTIFIER", "Why don't you want to tell me the parameter name!?"))
        self.consume("RIGHT_PAREN", "I need ')' after the paramter list!")
        self.consume("COLON", f"I absolutely require ':' before {kind} body!")
        body = self.block()
        if name.lexeme == "main" and kind == "function": self.mainFunction = True
        return Function(name, parameters, body)
    def block(self):
        previousBlock = self.currentBlock
        self.currentBlock = True
        statements = []
        while (not self.check("SEMICOLON")) and (not self.isAtEnd()):
            statements.append(self.declaration())
        self.consume("SEMICOLON", "You need to have ';' after a block!")
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
            self.error(equals, "That's an invalid assignment target!")
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
            elif type(expr) == Access:
                #print(expr.accessee)
                return ChAccess(expr.accessee, expr.index, value)
            self.error(equals, "That's an invalid assignment target!")
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
            elif type(expr) == Access:
                #print(expr.accessee)
                return ChAccess(expr.accessee, expr.index, value)
            self.error(equals, "That's an invalid assignment target!")
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
            elif type(expr) == Access:
                #print(expr.accessee)
                return ChAccess(expr.accessee, expr.index, value)
            self.error(equals, "That's an invalid assignment target!")
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
            elif type(expr) == Access:
                #print(expr.accessee)
                return ChAccess(expr.accessee, expr.index, value)
            self.error(equals, "That's an invalid assignment target!")
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
            elif type(expr) == Access:
                #print(expr.accessee)
                return ChAccess(expr.accessee, expr.index, value)
            self.error(equals, "That's an invalid assignment target!")
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
            elif type(expr) == Access:
                #print(expr.accessee)
                return ChAccess(expr.accessee, expr.index, value)
            self.error(equals, "That's an invalid assignment target!")
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
            elif type(expr) == Access:
                #print(expr.accessee)
                return ChAccess(expr.accessee, expr.index, value)
            self.error(equals, "That's an invalid assignment target!")
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
            elif type(expr) == Access:
                #print(expr.accessee)
                return ChAccess(expr.accessee, expr.index, value)
            self.error(equals, "That's an invalid assignment target!")
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
            #print("\n")
            #print(self.previous().line)
            keys = []
            values = []
            while not self.match("RIGHT_BRACE"):
                item1 = self.list()
                #print(f"Item 1: {item1}")
                self.consume("COLON", "I expect ':' between map items!")
                item2 = self.map()
                #print(f"Item 2: {item2}")
                keys.append(item1)
                values.append(item2)
                #print(keys)
                #print(values)
                #print('\n')
                #print()
            #print(keys)
            #print(values)
            return Map(keys, values)
        else:
            return self.list()
    def list(self):
        if self.match("LEFT_BRACKET"):
            contents = []
            while not self.match("RIGHT_BRACKET"):
                item = self.map()
                #print(f"\n{item}\n")
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
        expr = self.inExpr()
        while self.match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = self.previous()
            right = self.inExpr()
            expr = Binary(expr, operator, right)
        return expr
    def inExpr(self):
        expr = self.mod()
        while self.match("IN"):
            operator = self.previous()
            right = self.mod()
            expr = In(expr, operator, right)
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
                index = self.expression()
                close = self.consume("RIGHT_BRACKET", "I expect ']' after list access!")
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
                name = self.consume("IDENTIFIER", "You need to tell me the property name after '.'!")
                expr = Get(expr, name)
            else:
                break
        return expr
    def lam(self):
        if self.match("LM"):
            self.consume("LEFT_PAREN", f"You need to start the paramater list with '('!")
            parameters = []
            if not self.check("RIGHT_PAREN"):
                parameters.append(self.consume("IDENTIFIER", "Tell us the parameter name!"))
                while not self.check("RIGHT_PAREN") and not self.isAtEnd():
                    if len(parameters) >= 255:
                        self.error(self.peek(), "Having more than 255 parameters is just greedy!")
                    parameters.append(self.consume("IDENTIFIER", "Tell us the parameter name!"))
            self.consume("RIGHT_PAREN", "Close the parameter list with ')'!")
            self.consume("COLON", "You need to use ':' to start a lambda body!")
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
            self.consume("DOT", "You need a dot to access superclass methods!")
            method = self.consume("IDENTIFIER", "I can't run the superclass method without its name!")
            return Super(keyword, method)
        elif self.match("ME"):
            return Me(self.previous())
        elif self.match("IDENTIFIER"):
            #print(self.previous())
            return Variable(self.previous())
        elif self.match("NUM", "STR", "NIL", "BOOL", "LIST", "MAP"):
            return Type(self.previous())
        elif self.match("LEFT_PAREN"):
            expr = self.expression()
            self.consume("RIGHT_PAREN", "I need ')' after an expression!")
            return Grouping(expr)
        #if type(self.statements[-1]) == Function:
        #    
        raise self.error(self.peek(), "Give me an expression!")
    def finishCall(self, callee):
        arguments = []
        if not self.check("RIGHT_PAREN"):
            arguments.append(self.expression())
            while not self.check("RIGHT_PAREN") and not self.isAtEnd():
                if len(arguments) >= 255:
                    self.error(self.peek(), "Having more than 255 arguments is greedy!")
                arguments.append(self.expression())
        paren = self.consume("RIGHT_PAREN", "Close the paramter list with ')'!")
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
