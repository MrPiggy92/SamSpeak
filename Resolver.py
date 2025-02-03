class Resolver:
    def __init__(self, interpreter, SamSpeak_class):
        self.interpeter = interpreter
        self.scopes = []
        self.SamSpeak = SamSpeak_class
        self.currentFunction = "NONE"
        self.currentClass = "NONE"
    def visitBlockStmt(self, stmt):
        self.beginScope()
        self.resolve(stmt.statements)
        self.endScope()
        return None
    def visitVarStmt(self, stmt):
        self.declare(stmt.name)
        if stmt.initialiser != None:
            self.resolve(stmt.initialiser)
        self.define(stmt.name)
        return None
    def visitFunctionStmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolveFunction(stmt, "FUNCTION")
        return None
    def visitExpressionStmt(self, stmt):
        self.resolve(stmt.expression)
        return None
    def visitIfStmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        if stmt.elseBranch != None: self.resolve(stmt.elseBranch)
        return None
    def visitReturnStmt(self, stmt):
        if self.currentFunction == "NONE":
            self.SamSpeak.parseError(stmt.keyword, "Can't return from top-level code.")
        if stmt.value != None:
            if self.currentFunction == "INITIALISER":
                self.SamSpeak.parseError(stmt.keyword, "Can't return a value from an initialiser.")
            self.resolve(stmt.value)
        return None
    def visitWhileStmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
    def visitClassStmt(self, stmt):
        enclosingClass = self.currentClass
        self.currentClass = "CLASS"
        self.declare(stmt.name)
        self.define(stmt.name)
        if stmt.superclass != None and stmt.name.lexeme == stmt.superclass.name.lexeme:
            self.SamSpeak.parseError(stmt.superclass.name, "A class can't inherit from itself.")
        if stmt.superclass != None:
            self.currentClass = "SUBCLASS"
            self.resolve(stmt.superclass)
        if stmt.superclass != None:
            self.beginScope()
            self.scopes[-1]["super"] = True
        self.beginScope()
        self.scopes[-1]["this"] = True
        for method in stmt.methods:
            declaration = "METHOD"
            if method.name.lexeme == "init":
                declaration = "INITIALISER"
            self.resolveFunction(method, declaration)
        self.endScope()
        if stmt.superclass != None: self.endScope()
        self.currentClass = enclosingClass
        return None
    def visitListExpr(self, expr):
        for item in expr.items:
            self.resolve(item)
        return None
    def visitGetExpr(self, expr):
        self.resolve(expr.object)
        return None
    def visitSuperExpr(self, expr):
        if self.currentClass == "NONE":
            self.SamSpeak.parseError(expr.keyword, "Can't use 'super' outside a class.")
        elif self.currentClass != "SUBCLASS":
            self.SamSpeak.parseError(expr.keyword, "Can't use 'super' in a class with no superclass.")
        self.resolveLocal(expr, expr.keyword)
        return None
    def visitSetExpr(self, expr):
        self.resolve(expr.value)
        self.resolve(expr.object)
        return None
    def visitVariableExpr(self, expr):
        #print(self.scopes)
        #print(self.scopes[-1])
        try:
            if len(self.scopes) > 0 and not self.scopes[-1][expr.name.lexeme]:
                self.SamSpeak.parseError(expr.name, "Can't read local variable in its own initialiser.")
        except:
            pass
        self.resolveLocal(expr, expr.name)
        return None
    def visitBinaryExpr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None
    def visitCallExpr(self, expr):
        self.resolve(expr.callee)
        for arg in expr.arguments:
            self.resolve(arg)
        return None
    def visitAccessExpr(self, expr):
        self.resolve(expr.accessee)
        self.resolve(expr.index)
        return None
    def visitGroupingExpr(self, expr):
        self.resolve(expr.expression)
        return None
    def visitLiteralExpr(self, expr):
        return None
    def visitLogicalExpr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None
    def visitUnaryExpr(self, expr):
        self.resolve(expr.right)
        return None
    def visitMeExpr(self, expr):
        if self.currentClass == "NONE":
            self.SamSpeak.parseError(expr.keyword, "Can't use 'me' outside of a class.")
            return None
        self.resolveLocal(expr, expr.keyword)
        return None
    def resolve(self, statements):
        if type(statements) == list:
            for statement in statements:
                self.resolve(statement)
        else:
            statements.accept(self)
    def declare(self, name):
        if len(self.scopes) == 0: return
        scope = self.scopes[-1]
        if name.lexeme in scope.keys():
            self.SamSpeak.error(name, "Already a variable with this name in this scope.")
        scope[name.lexeme] = False
    def define(self, name):
        if len(self.scopes) == 0: return
        self.scopes[-1][name.lexeme] = True
    def resolveLocal(self, expr, name):
        for i in range(len(self.scopes)-1, -1, -1):
            if name.lexeme in self.scopes[i].keys():
                self.interpeter.resolve(expr, len(self.scopes)-1-i)
                return
    def resolveFunction(self, function, type):
        enclosingFunction = self.currentFunction
        self.currentFunction = type
        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.endScope()
        self.currentFunction = enclosingFunction
    def visitAssignExpr(self, expr):
        self.resolve(expr.value)
        self.resolveLocal(expr, expr.name)
        return None
    def beginScope(self):
        self.scopes.append({})
    def endScope(self):
        self.scopes.pop()

functionType = [
    "NONE",
    "FUNCTION",
    "METHOD",
    "INITIALISER"
]
classType = [
    "NONE",
    "CLASS",
    "SUBCLASS"
]
