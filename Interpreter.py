from SamSpeakRuntimeError import *
from Environment import *
from SamSpeakCallable import *
from SamSpeakFunction import *
from Return import *
from SamSpeakClass import *
#from Builtins import *
from Expr import *
import time
import importlib

class Interpreter:
    def __init__(self, SamSpeak):
        self.SamSpeak_class = SamSpeak
        self.globals = Environment()
        self.environment = self.globals
        self.modules = {"time": "SSTime", "io": "SSIo", "random": "SSRandom", "data": "SSLists", "math": "SSMath"}
        self.locals = {}
        self.currentBlock = "NONE"
    def addModule(self, module):
        if module in self.modules.keys():
            module = importlib.import_module(self.modules[module])
            for func in module.builtins.keys():
                self.globals.define(func, module.builtins[func])
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except SamSpeakRuntimeError as e:
            self.SamSpeak_class.runtimeError(e)
    def visitLiteralExpr(self, expr):
        return expr.value
    def visitGroupingExpr(self, expr):
        return self.evaluate(expr.expression)
    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator.type == "MINUS":
            self.checkNumberOperand(expr.operator, right)
            return -float(right)
        elif expr.operator.type == "BANG":
            return not self.isTruthy(right.value)
    def visitGetExpr(self, expr):
        object = self.evaluate(expr.object)
        if type(object) == SamSpeakInstance:
            return object.get(expr.name)
        raise SamSpeakRuntimeError(expr.name, "Only instances have properties.")
    def visitSetExpr(self, expr):
        object = self.evaluate(expr.object)
        if type(object) != SamSpeakInstance:
            raise SamSpeakRuntimeError(expr.name, "Only instances have fields.")
        value = self.evaluate(expr.value)
        object.set(expr.name, value)
        return value
    def visitBinaryExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        # print('\n')
        # print(left)
        # print(type(left))
        # print(right)
        # print(type(right))
        # print(expr.operator.type)
        if expr.operator.type == "GREATER":
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == "GREATER_EQUAL":
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == "LESS":
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == "LESS_EQUAL":
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.type == "EQUAL_EQUAL":
            self.checkNumberOperands(expr.operator, left, right)
            return self.isEqual(left, right)
        elif expr.operator.type == "BANG_EQUAL":
            self.checkNumberOperands(expr.operator, left, right)
            return not self.isEqual(left, right)
        elif expr.operator.type == "MINUS":
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type == "SLASH":
            self.checkNumberOperands(expr.operator, left, right)
            if right == 0:
                raise SamSpeakRuntimeError(expr.operator, "You can't divide by 0")
            return float(left) / float(right)
        elif expr.operator.type == "STAR":
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type == "PLUS":
            if type(left) == list or type(right) == list:
                if type(left) == type(right): return left + right
                if type(left) == list:
                    return left + [right]
                else:
                    return [left] + right
            if type(left) == float and type(right) == float:
                return float(left) + float(right)
            elif type(left) == str and type(right) == str:
                return self.stringify(left) + self.stringify(right)
            raise SamSpeakRuntimeError(expr.operator, "Operands must be two numbers or two strigns.")
        elif expr.operator.type == "MODULO":
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) % float(right)
        elif expr.operator.type == "UP_ARROW":
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) ** float(right)
        elif expr.operator.type == "DOTDOT":
            self.checkNumberOperands(expr.operator, left, right)
            return list(range(int(left), int(right+1.5)))
        return None
    def visitListExpr(self, expr):
        contents = []
        for item in expr.items:
            contents.append(self.evaluate(item))
        #print(contents)
        return contents
    def visitMapExpr(self, expr):
        contents = {}
        for key, value in zip(expr.keys, expr.values):
            newDict = {self.evaluate(key): self.evaluate(value)}
            #print(newDict)
            contents.update(newDict)
        return contents
    def visitInExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if type(right) == list:
            return left in right
        elif type(right) == dict:
            return left in list(right.keys()) or left in list(right.values())
        #elif type(right) == str:
        #
        else:
            raise SamSpeakRuntimeError(expr.operator, f"Can't check if a value is in a {type(expr.right)}.")
    def visitVariableExpr(self, expr):
        return self.lookUpVariable(expr.name, expr)
    def lookUpVariable(self, name, expr):
        #print(name)
        #print(self.globals.get(name))
        #print('\n')
        try:
            #print(self.locals)
            distance = self.locals[expr]
            #print("-----")
            #print(name)
            #print(distance)
            #print(self.environment.getAt(distance, name.lexeme))
            #print(isinstance(self.environment.getAt(distance, name.lexeme), SamSpeakCallable))
            #print(type(self.environment.getAt(distance, name.lexeme)))
            #print('\n-----')
            return self.environment.getAt(distance, name.lexeme)
        except:
            try:
                return self.environment.get(name)
            except:
                return self.globals.get(name)
    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        try:
            distance = self.locals[expr]
            self.environment.assignAt(distance, expr.name, value)
        except:
            self.globals.assign(expr.name, value)
        return value
    def visitLogicalExpr(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator.type == "OR":
            if self.isTruthy(left): return left
        else:
            if not self.isTruthy(left): return left
        return self.evaluate(expr.right)
    def visitCallExpr(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            #print(argument)
            arguments.append(self.evaluate(argument))
            #print(arguments[-1])
        if not isinstance(callee, SamSpeakCallable):
            #print(callee)
            #print(type(callee))
            raise SamSpeakRuntimeError(expr.paren, "Can only call functions and classes.")
        function = SamSpeakCallable(callee) # Callee
        if len(arguments) != function.arity():
            raise SamSpeakRuntimeError(expr.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")
        return function.call(self, arguments)
    def visitAccessExpr(self, expr):
        accessee = self.evaluate(expr.accessee)
        #print(f"h{accessee}h")
        index = self.evaluate(expr.index)
        if type(index) == float and type(accessee) in [list, str]: index = int(index)
        elif type(index) == float and type(accessee) == dict and index not in accessee.keys(): index = int(index)
        #print(type(accessee))
        #if type(accessee) == dict: print(accessee.keys())
        if type(accessee) not in  [list, str, dict]:
            raise SamSpeakRuntimeError(expr.bracket, "Can only access elements of lists, maps or strings.")
        if type(accessee) != dict and index >= len(accessee):
            raise SamSpeakRuntimeError(expr.bracket, "List index greater than list length.")
        elif type(accessee) == dict and index not in accessee.keys():
            raise SamSpeakRuntimeError(expr.bracket, "Key not in map.")
        return accessee[index]
    def visitChAccessExpr(self, expr):
        #print(self.environment.values)
        accessee = self.evaluate(expr.name)
        index = self.evaluate(expr.index)
        if type(index) == float and type(accessee) == list: index = int(index)
        elif type(index) == float and type(accessee) == dict and index not in accessee.keys(): index = int(index)
        value = self.evaluate(expr.value)
        #print(self.locals)
        #print(expr.name in self.locals)
        #print(expr.name)
        if type(accessee) not in  [list, str, dict]:
            raise SamSpeakRuntimeError(expr.name.name, "Can only access elements of lists, maps or strings.")
        #if index >= len(accessee) and type(accessee) != dict:
        #    raise SamSpeakRuntimeError(expr.name.name, "List index greater than list length.")
        #elif type(accessee) == dict and index not in accessee.keys():
        #    raise SamSpeakRuntimeError(expr.name.name, "Key not in map.")
        try:
            distance = self.locals[expr.name]
            #print(distance)
            if type(accessee) == str:
                accessee = [char for char in accessee]
                accessee[index] = value
                accessee = ''.join(accessee)
            elif type(accessee) == list:
                while len(accessee) <= index:
                    accessee.append(None)
            accessee[index] = value
            #print(self.environment.values)
            #print("hello")
            self.environment.assignAt(distance, expr.name.name, accessee)
        except Exception as e:
            #print(e)
            #print(accessee)
            accessee[index] = value
            self.globals.assign(expr.name.name, accessee)
        return accessee
    def visitTypeCastExpr(self, expr):
        left = self.evaluate(expr.left)
        if type(expr.new_type) != Type:
            raise SamSpeakRuntimeError(expr.colon, "Can only cast to a builtin type.")
        if expr.new_type.name.type == "NUM":
            try:
                return float(left)
            except:
                raise SamSpeakRuntimeError(expr.colon, f"Can't convert {left} to {expr.new_type.name.lexeme}")
        elif expr.new_type.name.type == "STR":
            try:
                return self.stringify(left)
            except:
                raise SamSpeakRuntimeError(expr.colon, f"Can't convert {left} to {expr.new_type.name.lexeme}")
        elif expr.new_type.name.type == "NIL":
            return None
        elif expr.new_type.name.type == "LIST":
            try:
                return list(left)
            except:
                raise SamSpeakRuntimeError(expr.colon, f"Can't convert {left} to {expr.new_type.name.lexeme}")
        elif expr.new_type.name.type == "BOOL":
            return self.isTruthy(left)
    def visitMeExpr(self, expr):
        return self.lookUpVariable(expr.keyword, expr)
    def visitLambdaExpr(self, expr):
        function = SamSpeakFunction(expr, self.environment, False)
        return function
    def visitSuperExpr(self, expr):
        distance = self.locals[expr]
        superclass = self.environment.getAt(distance, "super")
        object = self.environment.getAt(distance-1, "this")
        method = superclass.findMethod(expr.method.lexeme)
        if method == None:
            raise SamSpeakRuntimeError(expr.method, f"Undefined property '{expr.method.lexeme}'.")
        return method.bind(object)
    def visitExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)
        return None
    def visitFunctionStmt(self, stmt):
        function = SamSpeakFunction(stmt, self.environment, False)
        self.environment.define(stmt.name.lexeme, function)
        return function
    def visitReturnStmt(self, stmt):
        value = self.evaluate(stmt.value)
        raise Return(value)
    def visitRaiseStmt(self, stmt):
        value = self.evaluate(stmt.value)
        value = self.stringify(value)
        raise SamSpeakRuntimeError(stmt.keyword, value)
    def visitVarStmt(self, stmt):
        value = None
        if stmt.initialiser != None:
            value = self.evaluate(stmt.initialiser)
        self.environment.define(stmt.name.lexeme, value)
        return None
    def visitBlockStmt(self, stmt):
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None
    def visitClassStmt(self, stmt):
        superclass = None
        if stmt.superclass != None:
            superclass = self.evaluate(stmt.superclass)
            if type(superclass) != SamSpeakClass:
                raise SamSpeakRuntimeError(stmt.superclass.name, "Superclass must be a class.")
        self.environment.define(stmt.name.lexeme, None)
        if stmt.superclass != None:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)
        methods = {}
        for method in stmt.methods:
            function = SamSpeakFunction(method, self.environment, method.name.lexeme == "init")
            methods[method.name.lexeme] = function
        klass = SamSpeakClass(stmt.name.lexeme, superclass, methods)
        if superclass != None:
            self.environment = self.environment.enclosing
        self.environment.assign(stmt.name, klass)
        return None
    def visitIfStmt(self, stmt):
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch != None:
            self.execute(stmt.elseBranch)
        return None
    def visitWhileStmt(self, stmt):
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None
    def visitTryStmt(self, stmt):
        try:
            self.execute(stmt.contents)
        except SamSpeakRuntimeError:
            if stmt.catch != None:
                self.execute(stmt.catch)
    def executeBlock(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
    def execute(self, stmt):
        #print(self.environment.get('n'))
        stmt.accept(self)
    def resolve(self, expr, depth):
        self.locals[expr] = depth
    def evaluate(self, expr):
        return expr.accept(self)
    def isTruthy(self, value):
        if value == None: return False
        elif type(value) == bool: return bool(value)
        elif value == 0: return False
        return True
    def isEqual(self, a, b):
        if a == None and b == None: return True
        if a == None: return False
        return a == b
    def checkNumberOperand(self, operator, operand):
        if type(operand) == float: return
        raise SamSpeakRuntimeError(operator, "Operand should be a number.")
    def checkNumberOperands(self, operator, left, right):
        if type(left) == type(right) == float: return
        raise SamSpeakRuntimeError(operator, "Operands must be numbers.")
    def stringify(self, value):
        if value == None: return "nil"
        if type(value) == float:
            text = str(value)
            if text[-2:] == ".0":
                text = text[:-2]
            return text
        elif type(value) == list:
            strList = [self.stringify(item) for item in value]
            stringified = '['
            stringified += ' '.join(strList)
            stringified += ']'
            return stringified
        elif type(value) == dict:
            stringified = '{'
            for key, value in zip(value.keys(), value.values()):
                stringified += self.stringify(key)
                stringified += ':'
                stringified += self.stringify(value)
                stringified += ' '
            if stringified.endswith(' '): stringified = stringified[:-1]
            stringified += '}'
            return stringified
        return str(value)
