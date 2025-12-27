import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __repr__(self): return f"{self.type}:{self.value}"

class Lexer:
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        rules = [
            ('COMMENT',  r'#.*'),
            ('DEF', r'def'), ('IF', r'if'), ('ELIF', r'elif'), ('ELSE', r'else'),
            ('FOR', r'for'), ('TO', r'to'), ('WHILE', r'while'), ('TRY', r'try'),
            ('CATCH', r'catch'), ('IMPORT', r'import'), ('BREAK', r'break'),
            ('CONTINUE', r'continue'), ('RETURN', r'return'), ('PRINT', r'print'),
            ('INPUT', r'input'), ('INT', r'int'), ('AND', r'and'), ('OR', r'or'),
            ('TRUE', r'True'), ('FALSE', r'False'),
            ('NUMBER', r'\d+(\.\d+)?'), ('STRING', r'"[^"]*"'),
            ('ID', r'[A-Za-z_]\w*'),
            ('EQ', r'=='), ('NE', r'!='), ('LTE', r'<='), ('GTE', r'>='),
            ('LT', r'<'), ('GT', r'>'), ('ASSIGN', r'='),
            ('PLUS', r'\+'), ('MINUS', r'-'), ('MUL', r'\*'), ('DIV', r'/'),
            ('LPAREN', r'\('), ('RPAREN', r'\)'), ('LBRACE', r'\{'), ('RBRACE', r'\}'),
            ('LBRACKET', r'\['), ('RBRACKET', r'\]'), ('COMMA', r','),
            ('SKIP', r'[ \t\n\r]+'),
        ]
        regex = '|'.join('(?P<%s>%s)' % pair for pair in rules)
        tokens = []
        for mo in re.finditer(regex, self.text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'SKIP' or kind == 'COMMENT': continue
            if kind == 'NUMBER': value = float(value) if '.' in value else int(value)
            if kind == 'STRING': value = value[1:-1]
            tokens.append(Token(kind, value))
        return tokens