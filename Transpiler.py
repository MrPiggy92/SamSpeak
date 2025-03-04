from Expr import *

class Transpiler:
    def __init__(self, SamSpeak):
        self.samspeakclass = SamSpeak
        self.code = ''
    def generate(self, statements):
        for statement in statements:
            self.code += statement.accept(self)
            self.code += '\n'
        print(self.code)
    def visitLiteralExpr(self, expr):
        if type(expr.value) == str:
            return f"\"{expr.value}\""
        return str(expr.value)
    def visitGroupingExpr(self, expr):
        contents = str(self.evaluate(expr.expression))
        return f"({contents})"
    def visitUnaryExpr(self, expr):
        right = str(self.evaluate(expr.right))
        if expr.operator.type == "MINUS":
            return f"-{right}"
        elif expr.operator.type == "BANG":
            return f"not({right})"
    def visitGetExpr(self, expr):
        object = self.evaluate(expr.object)
        return f"{object}.{expr.name.lexeme}"
    def visitSetExpr(self, expr):
        object = self.evaluate(expr.object)
        value = self.evaluate(expr.value)
        return f"{object}.{expr.name.lexeme} = {value}"
    def visitBinaryExpr(self, expr):
        left = str(self.evaluate(expr.left))
        right = str(self.evaluate(expr.right))
        if expr.operator.type == "DOTDOT":
            return str(list(range(int(left), int(right)+1)))
        operators = {"PLUS": '+', "MINUS": '-', "SLASH": '/', "STAR": '*', "MODULO": '%', "UP_ARROW": "**", "GREATER": '>', "LESS": '<', "GREATER_EQUAL": ">=", "LESS_EQUAL": "<=", "EQUAL_EQUAL": "==", "BANG_EQUAL": "!="}
        operator = operators[expr.operator.type]
        return f"{left} {operator} {right}"
    def visitListExpr(self, expr):
        mylist = '['
        for item in expr.items:
            mylist += self.evaluate(item)
            mylist += ", "
        mylist = mylist[:-2]
        mylist += ']'
        return mylist
    def visitMapExpr(self, expr):
        mymap = '{'
        for item1, item2 in zip(expr.keys, expr.values):
            mymap += f"{str(self.evaluate(item1))}: {self.evaluate(item2)}, "
        mymap = mymap[:-2]
        mymap += '}'
        return mymap
    def visitInExpr(self, expr):
        left = str(self.evaluate(expr.left))
        right = str(self.evaluate(expr.right))
        return f"{left} in {right}"
    def visitVariableExpr(self, expr):
        return expr.name.lexeme
    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        return f"{expr.name.lexeme} = {value}"
    def visitLogicalExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        return f"{left} {expr.operator.type.lower()} {right}"
    def visitCallExpr(self, expr):
        callee = self.evaluate(expr.callee)
        if type(expr.callee) == Get and expr.callee.name.lexeme == "new":
            callee = self.evaluate(expr.callee.object)
        result = f"{str(callee)}("
        for item in expr.arguments:
            result += self.evaluate(item)
            result += ", "
        if result.endswith(' '): result = result[:-2]
        result += ')'
        return result
    def visitExpressionStmt(self, stmt):
        return self.evaluate(stmt.expression)
    def evaluate(self, expr):
        return expr.accept(self)
