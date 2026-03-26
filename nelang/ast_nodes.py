class ASTNode: pass

class Program(ASTNode):
    def __init__(self, statements): self.statements = statements

class Block(ASTNode):
    def __init__(self, statements): self.statements = statements

class Assign(ASTNode):
    def __init__(self, name, value): self.name = name; self.value = value

class Print(ASTNode):
    def __init__(self, exprs): self.exprs = exprs

class IfNode(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition; self.body = body; self.else_body = else_body

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition; self.body = body

class ForNode(ASTNode):
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name; self.iterable = iterable; self.body = body

class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name; self.params = params; self.body = body

class ReturnNode(ASTNode):
    def __init__(self, value): self.value = value

class ImportNode(ASTNode):
    def __init__(self, module_name): self.module_name = module_name

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left; self.op = op; self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op, right):
        self.op = op; self.right = right

class Call(ASTNode):
    def __init__(self, name, args):
        self.name = name; self.args = args

class PropertyAccess(ASTNode):
    def __init__(self, obj, prop):
        self.obj = obj; self.prop = prop

class Identifier(ASTNode):
    def __init__(self, name): self.name = name

class Number(ASTNode):
    def __init__(self, value): self.value = value

class String(ASTNode):
    def __init__(self, value): self.value = value

class Boolean(ASTNode):
    def __init__(self, value): self.value = value
    
class List(ASTNode):
    def __init__(self, items): self.items = items
