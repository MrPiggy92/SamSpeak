class Block:
    def __init__(self, statements):
        self.statements = statements
    def accept(self, visitor):
        return visitor.visitBlockStmt(self)
    def __repr__(self):
        return f"Block: (statements: {self.statements})"
class Class:
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods
    def accept(self, visitor):
        return visitor.visitClassStmt(self)
    def __repr__(self):
        return f"Class: (name: {self.name}, superclass: {self.superclass}, methods: {self.methods})"
class Expression:
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)
    def __repr__(self):
        return f"Expression: (expression: {self.expression})"
class Function:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def accept(self, visitor):
        return visitor.visitFunctionStmt(self)
    def __repr__(self):
        return f"Function: (name: {self.name}, params: {self.params}, body: {self.body})"
class If:
    def __init__(self, condition, thenBranch, elseBranch):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch
    def accept(self, visitor):
        return visitor.visitIfStmt(self)
    def __repr__(self):
        return f"If: (condition: {self.condition}, thenBranch: {self.thenBranch}, elseBranch: {self.elseBranch})"
class Return:
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value
    def accept(self, visitor):
        return visitor.visitReturnStmt(self)
    def __repr__(self):
        return f"Return: (keyword: {self.keyword}, value: {self.value})"
class Var:
    def __init__(self, name, initialiser):
        self.name = name
        self.initialiser = initialiser
    def accept(self, visitor):
        return visitor.visitVarStmt(self)
    def __repr__(self):
        return f"Var: (name: {self.name}, initialiser: {self.initialiser})"
class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def accept(self, visitor):
        return visitor.visitWhileStmt(self)
    def __repr__(self):
        return f"While: (condition: {self.condition}, body: {self.body})"
