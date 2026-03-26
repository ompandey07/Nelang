import ast
from .ast_nodes import *

class CompilerError(Exception): pass

class Compiler:
    def compile(self, node):
        module_body = self.visit(node)
        if not isinstance(module_body, list):
            module_body = [module_body]
            
        python_ast = ast.Module(body=module_body, type_ignores=[])
        ast.fix_missing_locations(python_ast)
        return python_ast

    def wrap_stmt(self, node):
        visited = self.visit(node)
        if isinstance(visited, ast.expr):
            return ast.Expr(value=visited)
        return visited

    def visit(self, node):
        if isinstance(node, Program):
            return [self.wrap_stmt(stmt) for stmt in node.statements if stmt is not None]
        
        if isinstance(node, Block):
            body = [self.wrap_stmt(stmt) for stmt in node.statements if stmt is not None]
            if not body:
                body = [ast.Pass()]
            return body

        if isinstance(node, Assign):
            target = ast.Name(id=node.name, ctx=ast.Store())
            value = self.visit(node.value)
            return ast.Assign(targets=[target], value=value)

        if isinstance(node, Print):
            func = ast.Name(id='lekha', ctx=ast.Load())
            args = [self.visit(e) for e in node.exprs]
            return ast.Expr(value=ast.Call(func=func, args=args, keywords=[]))

        if isinstance(node, IfNode):
            test = self.visit(node.condition)
            body = self.visit(node.body)
            orelse = self.visit(node.else_body) if node.else_body else []
            return ast.If(test=test, body=body, orelse=orelse)

        if isinstance(node, WhileNode):
            test = self.visit(node.condition)
            body = self.visit(node.body)
            return ast.While(test=test, body=body, orelse=[])

        if isinstance(node, ForNode):
            target = ast.Name(id=node.var_name, ctx=ast.Store())
            iter_ = self.visit(node.iterable)
            body = self.visit(node.body)
            return ast.For(target=target, iter=iter_, body=body, orelse=[])

        if isinstance(node, FunctionDef):
            args = ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg=p, annotation=None) for p in node.params],
                kwonlyargs=[], kw_defaults=[], defaults=[], vararg=None, kwarg=None
            )
            body = self.visit(node.body)
            return ast.FunctionDef(name=node.name, args=args, body=body, decorator_list=[], returns=None)

        if isinstance(node, ReturnNode):
            value = self.visit(node.value) if node.value else None
            return ast.Return(value=value)

        if isinstance(node, ImportNode):
            func = ast.Name(id='__nelang_import__', ctx=ast.Load())
            args = [ast.Constant(value=node.module_name)]
            return ast.Expr(value=ast.Call(func=func, args=args, keywords=[]))

        if isinstance(node, BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            op_map = {
                '+': ast.Add(), '-': ast.Sub(), '*': ast.Mult(), '/': ast.Div(),
                '<': ast.Lt(), '>': ast.Gt(), '<=': ast.LtE(), '>=': ast.GtE(),
                '==': ast.Eq(), '!=': ast.NotEq()
            }
            op = node.op
            if op in ('ra', 'wa'):
                bool_op = ast.And() if op == 'ra' else ast.Or()
                return ast.BoolOp(op=bool_op, values=[left, right])
            if op in ('<', '>', '<=', '>=', '==', '!='):
                return ast.Compare(left=left, ops=[op_map[op]], comparators=[right])
            
            return ast.BinOp(left=left, op=op_map[op], right=right)

        if isinstance(node, UnaryOp):
            operand = self.visit(node.right)
            if node.op == '-':
                return ast.UnaryOp(op=ast.USub(), operand=operand)
            if node.op == 'hoina':
                return ast.UnaryOp(op=ast.Not(), operand=operand)

        if isinstance(node, Call):
            func = self.visit(node.name)
            args = [self.visit(arg) for arg in node.args]
            return ast.Call(func=func, args=args, keywords=[])

        if isinstance(node, PropertyAccess):
            value = self.visit(node.obj)
            return ast.Attribute(value=value, attr=node.prop, ctx=ast.Load())

        if isinstance(node, Identifier):
            return ast.Name(id=node.name, ctx=ast.Load())

        if isinstance(node, Number) or isinstance(node, String) or isinstance(node, Boolean):
            return ast.Constant(value=node.value)

        if isinstance(node, List):
            elts = [self.visit(item) for item in node.items]
            return ast.List(elts=elts, ctx=ast.Load())

        raise CompilerError(f"Unknown node to transpile: {type(node)}")
