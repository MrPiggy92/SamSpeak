class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def accept(self, visitor):
        return visitor.visitAssignExpr(self)
    def __repr__(self):
        return f"Assign: (name: {self.name}, value: {self.value})"
class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)
    def __repr__(self):
        return f"Binary: (left: {self.left}, operator: {self.operator}, right: {self.right})"
class Call:
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments
    def accept(self, visitor):
        return visitor.visitCallExpr(self)
    def __repr__(self):
        return f"Call: (callee: {self.callee}, paren: {self.paren}, arguments: {self.arguments})"
class Access:
    def __init__(self, accessee, bracket, index):
        self.accessee = accessee
        self.bracket = bracket
        self.index = index
    def accept(self, visitor):
        return visitor.visitAccessExpr(self)
    def __repr__(self):
        return f"Access: (accessee: {self.accessee}, bracket: {self.bracket}, index: {self.index})"
class Get:
    def __init__(self, object, name):
        self.object = object
        self.name = name
    def accept(self, visitor):
        return visitor.visitGetExpr(self)
    def __repr__(self):
        return f"Get: (object: {self.object}, name: {self.name})"
class Grouping:
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)
    def __repr__(self):
        return f"Grouping: (expression: {self.expression})"
class List:
    def __init__(self, items):
        self.items = items
    def accept(self, visitor):
        return visitor.visitListExpr(self)
    def __repr__(self):
        return f"List: (items: {self.items})"
class Map:
    def __init__(self, keys, values):
        self.keys = keys
        self.values = values
    def accept(self, visitor):
        return visitor.visitMapExpr(self)
    def __repr__(self):
        return f"Map: (keys: {self.keys}, values: {self.values})"
class Literal:
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)
    def __repr__(self):
        return f"Literal: (value: {self.value})"
class Logical:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def accept(self, visitor):
        return visitor.visitLogicalExpr(self)
    def __repr__(self):
        return f"Logical: (left: {self.left}, operator: {self.operator}, right: {self.right})"
class Set:
    def __init__(self, object, name, value):
        self.object = object
        self.name = name
        self.value = value
    def accept(self, visitor):
        return visitor.visitSetExpr(self)
    def __repr__(self):
        return f"Set: (object: {self.object}, name: {self.name}, value: {self.value})"
class Super:
    def __init__(self, keyword, method):
        self.keyword = keyword
        self.method = method
    def accept(self, visitor):
        return visitor.visitSuperExpr(self)
    def __repr__(self):
        return f"Super: (keyword: {self.keyword}, method: {self.method})"
class Me:
    def __init__(self, keyword):
        self.keyword = keyword
    def accept(self, visitor):
        return visitor.visitMeExpr(self)
    def __repr__(self):
        return f"Me: (keyword: {self.keyword})"
class Unary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)
    def __repr__(self):
        return f"Unary: (operator: {self.operator}, right: {self.right})"
class Variable:
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        return visitor.visitVariableExpr(self)
    def __repr__(self):
        return f"Variable: (name: {self.name})"
class TypeCast:
    def __init__(self, left, colon, new_type):
        self.left = left
        self.colon = colon
        self.new_type = new_type
    def accept(self, visitor):
        return visitor.visitTypeCastExpr(self)
    def __repr__(self):
        return f"TypeCast: (left: {self.left}, colon: {self.colon}, new_type: {self.new_type})"
class Type:
    def __init__(self, name):
        self.name = name
    def accept(self, visitor):
        return visitor.visitTypeExpr(self)
    def __repr__(self):
        return f"Type: (name: {self.name})"
class Lambda:
    def __init__(self, params, body):
        self.params = params
        self.body = body
    def accept(self, visitor):
        return visitor.visitLambdaExpr(self)
    def __repr__(self):
        return f"Lambda: (params: {self.params}, body: {self.body})"
class ChAccess:
    def __init__(self, name, index, value):
        self.name = name
        self.index = index
        self.value = value
    def accept(self, visitor):
        return visitor.visitChAccessExpr(self)
    def __repr__(self):
        return f"ChAccess: (name: {self.name}, index: {self.index}, value: {self.value})"
