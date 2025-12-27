class ReturnValue(Exception):
    def __init__(self, value): self.value = value
class BreakSignal(Exception): pass
class ContinueSignal(Exception): pass

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
    def get(self, name):
        if name in self.vars: return self.vars[name]
        if self.parent: return self.parent.get(name)
        return None
    def set(self, name, value): self.vars[name] = value

class Interpreter:
    def __init__(self, env=None):
        self.env = env if env else Environment()
        self.setup_builtins()

    def setup_builtins(self):
        # We map a Flux name to a Python function
        self.env.set("len", lambda args: len(args[0]))
        self.env.set("str", lambda args: str(args[0]))
        self.env.set("type", lambda args: str(type(args[0]).__name__))

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        return getattr(self, method_name)(node)

    def visit_ProgramNode(self, node):
        res = None
        for s in node.statements: res = self.visit(s)
        return res

    def visit_ListNode(self, node): return [self.visit(e) for e in node.element_nodes]
    def visit_IndexNode(self, node):
        left = self.visit(node.left)
        idx = self.visit(node.index)
        return left[int(idx)]

    def visit_BinOpNode(self, node):
        l, r = self.visit(node.left_node), self.visit(node.right_node)
        op = node.op_token.type
        if op == 'PLUS': return l + r
        if op == 'MINUS': return l - r
        if op == 'MUL': return l * r
        if op == 'DIV': return l / r
        if op == 'EQ': return l == r
        if op == 'LT': return l < r
        if op == 'GT': return l > r

    def visit_VarAssignNode(self, node):
        val = self.visit(node.value_node)
        self.env.set(node.token.value, val)
        return val

    def visit_VarAccessNode(self, node):
        v = self.env.get(node.token.value)
        if v is None: raise Exception(f"Undefined: {node.token.value}")
        return v

    def visit_PrintNode(self, node):
        val = self.visit(node.expr)
        print(val)
        return val

    def visit_NumberNode(self, node): return node.token.value
    def visit_StringNode(self, node): return node.token.value
    def visit_BooleanNode(self, node): return node.value