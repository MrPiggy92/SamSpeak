class Block:
    def __init__(self, statements):
        self.statements = statements
    def accept(self, visitor):
        return visitor.visitBlockStmt(self)
    def __repr__(self):
        return f"Block: ({self.statements})"
class Class:
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods
    def accept(self, visitor):
        return visitor.visitClassStmt(self)
    def __repr__(self):
        return f"Class: ({self.name}, {self.superclass}, {self.methods})"
class Expression:
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)
    def __repr__(self):
        return f"Expression: ({self.expression})"
class Function:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def accept(self, visitor):
        return visitor.visitFunctionStmt(self)
    def __repr__(self):
        return f"Function: ({self.name}, {self.params}, {self.body})"
class If:
    def __init__(self, condition, thenBranch, elseBranch):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch
    def accept(self, visitor):
        return visitor.visitIfStmt(self)
    def __repr__(self):
        return f"If: ({self.condition}, {self.thenBranch}, {self.elseBranch})"
class Return:
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value
    def accept(self, visitor):
        return visitor.visitReturnStmt(self)
    def __repr__(self):
        return f"Return: ({self.keyword}, {self.value})"
class Var:
    def __init__(self, name, initialiser):
        self.name = name
        self.initialiser = initialiser
    def accept(self, visitor):
        return visitor.visitVarStmt(self)
    def __repr__(self):
        return f"Var: ({self.name}, {self.initialiser})"
class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def accept(self, visitor):
        return visitor.visitWhileStmt(self)
    def __repr__(self):
        return f"While: ({self.condition}, {self.body})"
