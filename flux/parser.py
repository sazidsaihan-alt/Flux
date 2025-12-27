from .atoms import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse(self):
        statements = []
        while self.current_token:
            stmt = self.statement()
            if stmt: statements.append(stmt)
        return ProgramNode(statements)

    def block(self):
        self.advance() # {
        stmts = []
        while self.current_token and self.current_token.type != 'RBRACE':
            stmts.append(self.statement())
        if self.current_token: self.advance() # }
        return stmts

    def statement(self):
        if not self.current_token: return None
        t = self.current_token.type
        
        if t == 'DEF': return self.func_def()
        if t == 'IF': return self.if_stmt()
        if t == 'FOR': return self.for_stmt()
        if t == 'WHILE': return self.while_stmt()
        if t == 'TRY': return self.try_stmt()
        if t == 'IMPORT': self.advance(); return ImportNode(self.expr())
        if t == 'BREAK': self.advance(); return BreakNode()
        if t == 'CONTINUE': self.advance(); return ContinueNode()
        if t == 'PRINT': self.advance(); return PrintNode(self.expr())
        if t == 'RETURN': self.advance(); return ReturnNode(self.expr())
        
        if t == 'ID':
            peek = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if peek and peek.type == 'ASSIGN':
                id_tok = self.current_token
                self.advance(); self.advance()
                return VarAssignNode(id_tok, self.expr())
        
        return self.expr()

    def expr(self):
        node = self.comp_expr()
        while self.current_token and self.current_token.type in ('AND', 'OR'):
            op = self.current_token; self.advance()
            node = BinOpNode(node, op, self.comp_expr())
        return node

    def comp_expr(self):
        node = self.arith_expr()
        while self.current_token and self.current_token.type in ('EQ', 'NE', 'LT', 'GT', 'LTE', 'GTE'):
            op = self.current_token; self.advance()
            node = BinOpNode(node, op, self.arith_expr())
        return node

    def arith_expr(self):
        node = self.term()
        while self.current_token and self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token; self.advance()
            node = BinOpNode(node, op, self.term())
        return node

    def term(self):
        node = self.call_index_expr()
        while self.current_token and self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token; self.advance()
            node = BinOpNode(node, op, self.call_index_expr())
        return node

    def call_index_expr(self):
        node = self.factor()
        while self.current_token and self.current_token.type in ('LPAREN', 'LBRACKET'):
            if self.current_token.type == 'LPAREN':
                self.advance()
                args = []
                if self.current_token.type != 'RPAREN':
                    args.append(self.expr())
                    while self.current_token.type == 'COMMA':
                        self.advance(); args.append(self.expr())
                self.advance(); node = CallNode(node, args)
            elif self.current_token.type == 'LBRACKET':
                self.advance()
                index = self.expr()
                self.advance(); node = IndexNode(node, index)
        return node

    def factor(self):
        tok = self.current_token
        if tok.type == 'NUMBER': self.advance(); return NumberNode(tok)
        if tok.type == 'STRING': self.advance(); return StringNode(tok)
        if tok.type == 'TRUE': self.advance(); return BooleanNode(True)
        if tok.type == 'FALSE': self.advance(); return BooleanNode(False)
        if tok.type == 'LBRACKET':
            self.advance()
            elements = []
            if self.current_token.type != 'RBRACKET':
                elements.append(self.expr())
                while self.current_token.type == 'COMMA':
                    self.advance(); elements.append(self.expr())
            self.advance(); return ListNode(elements)
        if tok.type == 'ID':
            id_tok = tok; self.advance(); return VarAccessNode(id_tok)
        if tok.type == 'LPAREN':
            self.advance(); n = self.expr(); self.advance(); return n
        raise Exception(f"Syntax Error: {tok}")

    # Logic for Statements
    def if_stmt(self):
        self.advance(); cond = self.expr(); body = self.block()
        elif_cases = []
        while self.current_token and self.current_token.type == 'ELIF':
            self.advance(); e_cond = self.expr(); e_body = self.block()
            elif_cases.append((e_cond, e_body))
        else_body = None
        if self.current_token and self.current_token.type == 'ELSE':
            self.advance(); else_body = self.block()
        return IfNode(cond, body, elif_cases, else_body)

    def for_stmt(self):
        self.advance(); var_tok = self.current_token; self.advance()
        self.advance(); start = self.expr(); self.advance(); end = self.expr(); body = self.block()
        return ForNode(var_tok, start, end, body)

    def while_stmt(self):
        self.advance(); cond = self.expr(); body = self.block(); return WhileNode(cond, body)

    def try_stmt(self):
        self.advance(); try_body = self.block(); self.advance(); catch_body = self.block()
        return TryCatchNode(try_body, catch_body)

    def func_def(self):
        self.advance(); name = self.current_token; self.advance(); self.advance()
        args = []
        if self.current_token.type == 'ID':
            args.append(self.current_token); self.advance()
            while self.current_token.type == 'COMMA':
                self.advance(); args.append(self.current_token); self.advance()
        self.advance(); body = ProgramNode(self.block()); return FuncDefNode(name, args, body)