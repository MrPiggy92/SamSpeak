from Expr import *

class Transpiler:
    def __init__(self, SamSpeak):
        self.samspeakclass = SamSpeak
        self.code = ''
    def generate(self, statements):
        for statement in statements[:-1]:
            self.code += statement.accept(self)
            self.code += '\n'
        self.code += """if __name__ == "__main__":
    import sys
    args = sys.argv
    args.pop(0)
    main(args)
"""
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
        if mylist.endswith(' '): mylist = mylist[:-2]
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
        #print(expr.callee)
        callee = self.evaluate(expr.callee)
        #print(callee)
        if type(expr.callee) == Get and expr.callee.name.lexeme == "new":
            callee = self.evaluate(expr.callee.object)
        elif type(expr.callee) == Super and expr.callee.method.lexeme == "new":
            callee = "super().__init__"
        result = f"{str(callee)}("
        for item in expr.arguments:
            result += self.evaluate(item)
            result += ", "
        if result.endswith(' '): result = result[:-2]
        result += ')'
        return result
    def visitAccessExpr(self, expr):
        accessee = self.evaluate(expr.accessee)
        index = self.evaluate(expr.index)
        return f"{accessee}[{index}]"
    def visitChAccessExpr(self, expr):
        accessee = self.evaluate(expr.accessee)
        index = self.evaluate(expr.index)
        value = self.evaluate(expr.value)
        return f"{accessee}[{index}] = {value}"
    def visitTypeCastExpr(self, expr):
        left = self.evaluate(expr.left)
        if expr.new_type.name.type == "NUM":
            return f"float({left})"
        elif expr.new_type.name.type == "STR":
            return f"str({left})"
        elif expr.new_type.name.type == "NIL":
            return "None"
        elif expr.new_type.name.type == "LIST":
            return f"list({left})"
        elif expr.new_type.name.type == "MAP":
            return f"dict({left})"
        elif expr.new_type.name.type == "BOOL":
            return self.isTruthy(left)
    def visitMeExpr(self, expr):
        return "self"
    def visitSuperExpr(self, expr):
        return "super()"
    def visitExpressionStmt(self, stmt):
        return self.evaluate(stmt.expression)
    def visitFunctionStmt(self, stmt, method=False):
        name = stmt.name.lexeme
        if name == "new" and method:
            name = "__init__"
        body = [self.evaluate(item) for item in stmt.body]
        result = f"def {name}("
        if method:
            result += "self, "
        for param in stmt.params:
            result += param.lexeme
            result += ", "
        if result.endswith(' '): result = result[:-2]
        result += '):\n    '
        for stmt in body:
            for line in stmt.split('\n'):
                result += line
                result += "\n    "
        result = result[:-5]
        return result
    def visitReturnStmt(self, stmt):
        value = self.evaluate(stmt.value)
        return f"return {value}"
    def visitRaiseStmt(self, stmt):
        value = self.evaluate(stmt.value)
        return f"raise RuntimeError({value})"
    def visitVarStmt(self, stmt):
        if stmt.initialiser != None:
            init = self.evaluate(stmt.initialiser)
            return f"{stmt.name.lexeme} = {init}"
        return f"{stmt.name.lexeme} = None"
    def visitBlockStmt(self, stmt):
        func = """def _():
    """
        for item in stmt.statements:
            for line in self.evaluate(item).split('\n'):
                func += line
                func += "\n    "
        func = func[:-4]
        func += "_()"
        return func
    def visitClassStmt(self, stmt):
        result = f"class {stmt.name.lexeme}"
        superclass = None
        if stmt.superclass != None:
            superclass = self.evaluate(stmt.superclass)
            result += f"({superclass})"
        result += ":\n    "
        for method in stmt.methods:
            for line in self.visitFunctionStmt(method, method=True).split('\n'):
                result += line
                result += "\n    "
        result = result[:-5]
        return result
    def visitIfStmt(self, stmt):
        pass
    def evaluate(self, expr):
        return expr.accept(self)
