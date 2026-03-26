from .ast_nodes import *

class ParserError(Exception): pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self): 
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]
        
    def advance(self): self.pos += 1

    def match(self, type_, val=None):
        tok = self.current()
        if tok.type == type_ and (val is None or tok.value == val):
            self.advance()
            return True
        return False

    def expect(self, type_, val=None):
        tok = self.current()
        if tok.type == type_ and (val is None or tok.value == val):
            self.advance()
            return tok
        expected = val if val else type_
        raise ParserError(f"Expected {expected} at line {tok.line}, got {tok.type} '{tok.value}'")

    def parse(self):
        stmts = []
        while self.current().type != 'EOF':
            while self.match('NEWLINE'): pass
            if self.current().type == 'EOF': break
            stmts.append(self.parse_statement())
        return Program(stmts)

    def parse_statement(self):
        tok = self.current()
        if tok.type == 'KEYWORD':
            if tok.value == 'karya': return self.parse_function()
            if tok.value == 'yadi': return self.parse_if()
            if tok.value == 'jaba': return self.parse_while()
            if tok.value == 'lagi': return self.parse_for()
            if tok.value == 'lekha': return self.parse_print()
            if tok.value == 'firta': return self.parse_return()
            if tok.value == 'lyaau': return self.parse_import()
        
        # Assignment Check
        if tok.type == 'IDENTIFIER':
            if self.pos + 1 < len(self.tokens):
                next_tok = self.tokens[self.pos+1]
                if next_tok.type == 'OP' and next_tok.value == '=':
                    name = tok.value
                    self.advance(); self.advance() # consume id and '='
                    expr = self.parse_expr()
                    self.match('NEWLINE')
                    return Assign(name, expr)
        
        expr = self.parse_expr()
        self.match('NEWLINE')
        return expr 

    def parse_block(self):
        self.expect('OP', ':')
        self.expect('NEWLINE')
        self.expect('INDENT')
        stmts = []
        while self.current().type != 'DEDENT' and self.current().type != 'EOF':
            while self.match('NEWLINE'): pass
            if self.current().type == 'DEDENT': break
            stmts.append(self.parse_statement())
        self.expect('DEDENT')
        return Block(stmts)

    def parse_function(self):
        self.expect('KEYWORD', 'karya')
        name = self.expect('IDENTIFIER').value
        self.expect('OP', '(')
        params = []
        if not self.match('OP', ')'):
            params.append(self.expect('IDENTIFIER').value)
            while self.match('OP', ','):
                params.append(self.expect('IDENTIFIER').value)
            self.expect('OP', ')')
        body = self.parse_block()
        return FunctionDef(name, params, body)

    def parse_if(self):
        self.expect('KEYWORD', 'yadi')
        cond = self.parse_expr()
        body = self.parse_block()
        else_body = None
        current = self.current()
        if current.type == 'KEYWORD' and current.value == 'tyasovaye':
            self.advance()
            else_body = self.parse_block()
        return IfNode(cond, body, else_body)

    def parse_while(self):
        self.expect('KEYWORD', 'jaba')
        cond = self.parse_expr()
        body = self.parse_block()
        return WhileNode(cond, body)

    def parse_for(self):
        self.expect('KEYWORD', 'lagi')
        var_name = self.expect('IDENTIFIER').value
        self.expect('KEYWORD', 'vitra')
        iterable = self.parse_expr()
        body = self.parse_block()
        return ForNode(var_name, iterable, body)

    def parse_print(self):
        self.expect('KEYWORD', 'lekha')
        self.expect('OP', '(')
        exprs = []
        if not self.match('OP', ')'):
            exprs.append(self.parse_expr())
            while self.match('OP', ','):
                exprs.append(self.parse_expr())
            self.expect('OP', ')')
        self.match('NEWLINE')
        return Print(exprs)

    def parse_return(self):
        self.expect('KEYWORD', 'firta')
        expr = self.parse_expr()
        self.match('NEWLINE')
        return ReturnNode(expr)

    def parse_import(self):
        self.expect('KEYWORD', 'lyaau')
        module_name = self.expect('IDENTIFIER').value
        self.match('NEWLINE')
        return ImportNode(module_name)

    def parse_expr(self): return self.parse_logic_or()

    def parse_logic_or(self):
        left = self.parse_logic_and()
        while self.match('KEYWORD', 'wa'):
            left = BinOp(left, 'wa', self.parse_logic_and())
        return left

    def parse_logic_and(self):
        left = self.parse_comp()
        while self.match('KEYWORD', 'ra'):
            left = BinOp(left, 'ra', self.parse_comp())
        return left

    def parse_comp(self):
        left = self.parse_arith()
        while True:
            tok = self.current()
            if tok.type == 'OP' and tok.value in ('<', '>', '<=', '>=', '==', '!='):
                op = tok.value; self.advance()
                left = BinOp(left, op, self.parse_arith())
            else: break
        return left

    def parse_arith(self):
        left = self.parse_term()
        while True:
            tok = self.current()
            if tok.type == 'OP' and tok.value in ('+', '-'):
                op = tok.value; self.advance()
                left = BinOp(left, op, self.parse_term())
            else: break
        return left

    def parse_term(self):
        left = self.parse_factor()
        while True:
            tok = self.current()
            if tok.type == 'OP' and tok.value in ('*', '/'):
                op = tok.value; self.advance()
                left = BinOp(left, op, self.parse_factor())
            else: break
        return left

    def parse_factor(self):
        tok = self.current()
        if tok.type == 'KEYWORD' and tok.value == 'hoina':
            self.advance()
            return UnaryOp('hoina', self.parse_factor())
        if tok.type == 'OP' and tok.value in ('+', '-'):
            op = tok.value; self.advance()
            return UnaryOp(op, self.parse_factor())
        return self.parse_primary()

    def parse_primary(self):
        tok = self.current()
        if tok.type == 'NUMBER':
            self.advance()
            return Number(float(tok.value) if '.' in tok.value else int(tok.value))
        if tok.type == 'STRING':
            self.advance()
            return String(eval(tok.value))
        if tok.type == 'KEYWORD' and tok.value == 'satya':
            self.advance(); return Boolean(True)
        if tok.type == 'KEYWORD' and tok.value == 'jhuto':
            self.advance(); return Boolean(False)
        if tok.type == 'OP' and tok.value == '[':
            self.advance()
            items = []
            if not self.match('OP', ']'):
                items.append(self.parse_expr())
                while self.match('OP', ','):
                    items.append(self.parse_expr())
                self.expect('OP', ']')
            return List(items)
            
        if tok.type == 'IDENTIFIER':
            name = tok.value
            self.advance()
            node = Identifier(name)
            while True:
                if self.match('OP', '.'):
                    prop = self.expect('IDENTIFIER').value
                    node = PropertyAccess(node, prop)
                elif self.match('OP', '('):
                    args = []
                    if not self.match('OP', ')'):
                        args.append(self.parse_expr())
                        while self.match('OP', ','):
                            args.append(self.parse_expr())
                        self.expect('OP', ')')
                    node = Call(node, args)
                else:
                    break
            return node

        if tok.type == 'OP' and tok.value == '(':
            self.advance()
            expr = self.parse_expr()
            self.expect('OP', ')')
            
            # Sub-properties after parenthesis check i.e (5 + 5).string_method
            node = expr
            while True:
                if self.match('OP', '.'):
                    prop = self.expect('IDENTIFIER').value
                    node = PropertyAccess(node, prop)
                elif self.match('OP', '('):
                    args = []
                    if not self.match('OP', ')'):
                        args.append(self.parse_expr())
                        while self.match('OP', ','):
                            args.append(self.parse_expr())
                        self.expect('OP', ')')
                    node = Call(node, args)
                else:
                    break
            return node
        
        raise ParserError(f"Unexpected token {tok.type} '{tok.value}' at line {tok.line}")
