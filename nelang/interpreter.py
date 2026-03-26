import sys
import time
import traceback
import math
import os
from .lexer import lex
from .parser import Parser, ParserError
from .compiler import Compiler, CompilerError
from .errors import NeLangSyntaxError, NeLangRuntimeError

MAGENTA = '\033[95m'
RESET = '\033[0m'
RED = '\033[91m'
BOLD = '\033[1m'
YELLOW = '\033[93m'

def built_in_import(module_name, runtime_env):
    module_path = module_name + ".nl"
    if module_name in ['math', 'string']:
        return
    if not os.path.exists(module_path):
        raise RuntimeError(f"Cannot import '{module_name}': file '{module_path}' not found.")
        
    with open(module_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    tokens = lex(source)
    ast_tree = Parser(tokens).parse()
    python_ast = Compiler().compile(ast_tree)
    compiled_code = compile(python_ast, module_path, 'exec')
    
    module_env = dict(runtime_env)
    exec(compiled_code, module_env)
    
    runtime_env[module_name] = type('Module', (), module_env)

class StringUtils:
    @staticmethod
    def uppercase(s): return str(s).upper()
    @staticmethod
    def lowercase(s): return str(s).lower()
    @staticmethod
    def length(s): return len(str(s))

class NeLangInterpreter:
    def __init__(self, logger=None, debug=False):
        self.logger = logger
        self.debug = debug
        
    def execute(self, source_code, filename="<string>"):
        start_time = time.time()
        success = True
        try:
            tokens = lex(source_code)
            if self.debug: self.logger.debug(f"Lexed Tokens: {tokens}")
                
            parser = Parser(tokens)
            ast_tree = parser.parse()
            if self.debug: self.logger.debug(f"Custom AST successfully built.")
            
            compiler = Compiler()
            python_ast = compiler.compile(ast_tree)
            
            if self.debug:
                import ast
                self.logger.debug(f"Compiled Python AST:\n{ast.dump(python_ast, indent=2)}")

            compiled_code = compile(python_ast, filename, 'exec')
            
            local_env = {
                '__builtins__': __builtins__,
                'lina': input,
                'lekha': print,
                'math': math,
                'string': StringUtils,
            }
            local_env['__nelang_import__'] = lambda name: built_in_import(name, local_env)
            
            exec(compiled_code, local_env)
            
        except NeLangSyntaxError as e:
            e.filename = filename
            e.print_error()
            success = False
            sys.exit(1)
        except NeLangRuntimeError as e:
            e.filename = filename
            e.print_error()
            success = False
            sys.exit(1)
        except ParserError as e:
            print(f"{RED}{BOLD}⨯ Parsing Error in '{filename}'{RESET}", file=sys.stderr)
            print(f"  {e}", file=sys.stderr)
            success = False
            sys.exit(1)
        except CompilerError as e:
            print(f"{RED}{BOLD}⨯ Compilation Error in '{filename}'{RESET}", file=sys.stderr)
            print(f"  {e}", file=sys.stderr)
            success = False
            sys.exit(1)
        except Exception as e:
            print(f"{RED}{BOLD}⨯ Fatal Runtime Trace in '{filename}'{RESET}", file=sys.stderr)
            traceback.print_exc()
            success = False
            sys.exit(1)
        finally:
            if success:
                elapsed_ms = (time.time() - start_time) * 1000
                print(f"\n{MAGENTA}✨ Execution finished in {elapsed_ms:.2f}ms{RESET}")
