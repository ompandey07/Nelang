import math
import os
from .ast_nodes import *

class ReturnException(Exception):
    def __init__(self, value): self.value = value

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
    def set(self, name, val):
        self.vars[name] = val
    def get(self, name):
        if name in self.vars: return self.vars[name]
        if self.parent: return self.parent.get(name)
        from .errors import NeLangRuntimeError
        raise NeLangRuntimeError(f"Undefined variable: {name}")

class Evaluator:
    def __init__(self, logger=None):
        self.logger = logger
        self.global_env = Environment()
        self.global_env.set('lina', input) # Built-in input mapping setup
        self.global_env.set('lekha', print)
        
        # Inject standard math module mapping to python's math
        math_env = {}
        for name in dir(math):
            if not name.startswith('_'):
                math_env[name] = getattr(math, name)
        self.global_env.set('math', math_env)
        
        # Simple generic string functions module
        string_env = {
            'uppercase': lambda s: str(s).upper(),
            'lowercase': lambda s: str(s).lower(),
            'length': lambda s: len(str(s))
        }
        self.global_env.set('string', string_env)
        
    def log(self, msg):
        if self.logger:
            self.logger.debug(msg)

    def evaluate(self, node, env):
        self.log(f"Evaluating {type(node).__name__}")
        if isinstance(node, Program):
            res = None
            for stmt in node.statements:
                res = self.evaluate(stmt, env)
            return res
            
        if isinstance(node, Block):
            for stmt in node.statements:
                self.evaluate(stmt, env)
            return None
            
        if isinstance(node, Assign):
            val = self.evaluate(node.value, env)
            env.set(node.name, val)
            
        if isinstance(node, Print):
            vals = [self.evaluate(e, env) for e in node.exprs]
            print(*vals)
            
        if isinstance(node, IfNode):
            if self.evaluate(node.condition, env):
                self.evaluate(node.body, env)
            elif node.else_body:
                self.evaluate(node.else_body, env)
                
        if isinstance(node, WhileNode):
            while self.evaluate(node.condition, env):
                self.evaluate(node.body, env)
                
        if isinstance(node, ForNode):
            iterable = self.evaluate(node.iterable, env)
            for item in iterable:
                env.set(node.var_name, item)
                self.evaluate(node.body, env)
                
        if isinstance(node, FunctionDef):
            env.set(node.name, node)
            
        if isinstance(node, ReturnNode):
            raise ReturnException(self.evaluate(node.value, env))
            
        if isinstance(node, ImportNode):
            module_name = node.module_name
            module_path = module_name + ".nl"
            if module_name in ['math', 'string']:
                return None
            if not os.path.exists(module_path):
                from .errors import NeLangRuntimeError
                raise NeLangRuntimeError(f"Cannot import '{module_name}': file '{module_path}' not found.")
                
            with open(module_path, 'r', encoding='utf-8') as f:
                source = f.read()
            from .lexer import lex
            from .parser import Parser
            tokens = lex(source)
            ast_tree = Parser(tokens).parse()
            
            module_env = Environment(self.global_env)
            self.evaluate(ast_tree, module_env)
            env.set(module_name, module_env.vars)
        
        if isinstance(node, BinOp):
            l = self.evaluate(node.left, env)
            r = self.evaluate(node.right, env)
            op = node.op
            if op == '+': return l + r
            if op == '-': return l - r
            if op == '*': return l * r
            if op == '/': return l / r
            if op == '<': return l < r
            if op == '>': return l > r
            if op == '<=': return l <= r
            if op == '>=': return l >= r
            if op == '==': return l == r
            if op == '!=': return l != r
            if op == 'ra': return l and r
            if op == 'wa': return l or r
            
        if isinstance(node, UnaryOp):
            r = self.evaluate(node.right, env)
            if node.op == '-': return -r
            if node.op == 'hoina': return not r
            
        if isinstance(node, PropertyAccess):
            obj = self.evaluate(node.obj, env)
            if isinstance(obj, dict):
                if node.prop in obj:
                    return obj[node.prop]
                from .errors import NeLangRuntimeError
                raise NeLangRuntimeError(f"Module has no attribute '{node.prop}'")
            if hasattr(obj, node.prop):
                return getattr(obj, node.prop)
            from .errors import NeLangRuntimeError
            raise NeLangRuntimeError(f"Object has no attribute '{node.prop}'")
            
        if isinstance(node, Call):
            func = self.evaluate(node.name, env)
            args = [self.evaluate(arg, env) for arg in node.args]
            
            if callable(func): 
                return func(*args)
            if isinstance(func, FunctionDef):
                local_env = Environment(env)
                for param, arg in zip(func.params, args):
                    local_env.set(param, arg)
                try:
                    self.evaluate(func.body, local_env)
                except ReturnException as ret:
                    return ret.value
                return None
            from .errors import NeLangRuntimeError
            raise NeLangRuntimeError(f"Object is not callable")
        
        if isinstance(node, Identifier): return env.get(node.name)
        if isinstance(node, Number): return node.value
        if isinstance(node, String): return node.value
        if isinstance(node, Boolean): return node.value
        if isinstance(node, List):
            return [self.evaluate(item, env) for item in node.items]
        
    def execute(self, ast_tree):
        self.evaluate(ast_tree, self.global_env)
