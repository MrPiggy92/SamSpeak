class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def accept(self, visitor):
        return visitor.visitAssignExpr(self)
    def __repr__(self):
        return f"Assign: ({self.name}, {self.value})"
class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)
    def __repr__(self):
        return f"Binary: ({self.left}, {self.operator}, {self.right})"
class Call:
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments
    def accept(self, visitor):
        return visitor.visitCallExpr(self)
    def __repr__(self):
        return f"Call: ({self.callee}, {self.paren}, {self.arguments})"
class Access:
    def __init__(self, accessee, bracket, index):
        self.accessee = accessee
        self.bracket = bracket
        self.index = index
    def accept(self, visitor):
        return visitor.visitAccessExpr(self)
    def __repr__(self):
        return f"Access: ({self.accessee}, {self.bracket}, {self.index})"
class Get:
    def __init__(self, object, name):
        self.object = object
        self.name = name
    def accept(self, visitor):
        return visitor.visitGetExpr(self)
    def __repr__(self):
        return f"Get: ({self.object}, {self.name})"
class Grouping:
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)
    def __repr__(self):
        return f"Grouping: ({self.expression})"
class List:
    def __init__(self, items):
        self.items = items
    def accept(self, visitor):
        return visitor.visitListExpr(self)
    def __repr__(self):
        return f"List: ({self.items})"
class Literal:
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)
    def __repr__(self):
        return f"Literal: ({self.value})"
class Logical:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def accept(self, visitor):
        return visitor.visitLogicalExpr(self)
    def __repr__(self):
        return f"Logical: ({self.left}, {self.operator}, {self.right})"
class Set:
    def __init__(self, object, name, value):
        self.object = object
        self.name = name
        self.value = value
    def accept(self, visitor):
        return visitor.visitSetExpr(self)
    def __repr__(self):
        return f"Set: ({self.object}, {self.name}, {self.value})"
class Super:
    def __init__(self, keyword, method):
        self.keyword = keyword
        self.method = method
    def accept(self, visitor):
        return visitor.visitSuperExpr(self)
    def __repr__(self):
        return f"Super: ({self.keyword}, {self.method})"
class Me:
    def __init__(self, keyword):
        self.keyword = keyword
    def accept(self, visitor):
        return visitor.visitMeExpr(self)
    def __repr__(self):
        return f"Me: ({self.keyword})"
class Unary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)
    def __repr__(self):
        return f"Unary: ({self.operator}, {self.right})"
class Variable:
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        return visitor.visitVariableExpr(self)
    def __repr__(self):
        return f"Variable: ({self.name})"
class TypeCast:
    def __init__(self, left, colon, new_type):
        self.left = left
        self.colon = colon
        self.new_type = new_type
    def accept(self, visitor):
        return visitor.visitTypeCastExpr(self)
    def __repr__(self):
        return f"TypeCast: ({self.left}, {self.colon}, {self.new_type})"
class Type:
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        return visitor.visitTypeExpr(self)
    def __repr__(self):
        return f"Type: ({self.name})"
