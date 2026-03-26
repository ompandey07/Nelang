import sys

RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

class NeLangError(Exception):
    pass

class NeLangSyntaxError(NeLangError):
    def __init__(self, message, line, filename="<unknown>"):
        self.message = message
        self.line = line
        self.filename = filename
        super().__init__(self.message)

    def print_error(self):
        print(f"{RED}{BOLD}⨯ SyntaxError in '{self.filename}'{RESET}", file=sys.stderr)
        print(f"{YELLOW}  Line {self.line}: {self.message}{RESET}", file=sys.stderr)

class NeLangRuntimeError(NeLangError):
    def __init__(self, message, filename="<unknown>"):
        self.message = message
        self.filename = filename
        super().__init__(self.message)

    def print_error(self):
        print(f"{RED}{BOLD}⨯ RuntimeError in '{self.filename}'{RESET}", file=sys.stderr)
        print(f"  {self.message}", file=sys.stderr)
