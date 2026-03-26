import tokenize
import io

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line})"

KEYWORDS = {
    'yadi', 'tyasovaye', 'jaba', 'lagi', 'vitra', 
    'lekha', 'karya', 'firta', 'satya', 'jhuto', 
    'ra', 'wa', 'hoina', 'lyaau'
}

def lex(source_code):
    stream = io.BytesIO(source_code.encode('utf-8')).readline
    tokens = []
    try:
        for tok in tokenize.tokenize(stream):
            type_name = tokenize.tok_name[tok.type]
            val = tok.string

            if type_name in ('ENCODING', 'NL', 'COMMENT'):
                continue
            
            if type_name == 'NAME' and val in KEYWORDS:
                tokens.append(Token('KEYWORD', val, tok.start[0], tok.start[1]))
            elif type_name == 'NAME':
                if val == 'rakha': continue
                tokens.append(Token('IDENTIFIER', val, tok.start[0], tok.start[1]))
            elif type_name == 'NUMBER':
                tokens.append(Token('NUMBER', val, tok.start[0], tok.start[1]))
            elif type_name == 'STRING':
                tokens.append(Token('STRING', val, tok.start[0], tok.start[1]))
            elif type_name == 'OP':
                tokens.append(Token('OP', val, tok.start[0], tok.start[1]))
            elif type_name == 'NEWLINE':
                tokens.append(Token('NEWLINE', '\n', tok.start[0], tok.start[1]))
            elif type_name == 'INDENT':
                tokens.append(Token('INDENT', 'INDENT', tok.start[0], tok.start[1]))
            elif type_name == 'DEDENT':
                tokens.append(Token('DEDENT', 'DEDENT', tok.start[0], tok.start[1]))
            elif type_name == 'ENDMARKER':
                tokens.append(Token('EOF', 'EOF', tok.start[0], tok.start[1]))
    except tokenize.TokenError as e:
        from .errors import NeLangSyntaxError
        msg, (line, col) = e.args
        raise NeLangSyntaxError(f"Tokenizer error: {msg}", line=line)
    
    return tokens
