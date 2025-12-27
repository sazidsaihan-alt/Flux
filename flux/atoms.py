from dataclasses import dataclass
from typing import Any

@dataclass
class NumberNode: token: Any
@dataclass
class StringNode: token: Any
@dataclass
class BooleanNode: value: bool
@dataclass
class ListNode: element_nodes: list
@dataclass
class IndexNode: left: Any; index: Any
@dataclass
class VarAccessNode: token: Any
@dataclass
class VarAssignNode: token: Any; value_node: Any
@dataclass
class BinOpNode: left_node: Any; op_token: Any; right_node: Any
@dataclass
class PrintNode: expr: Any
@dataclass
class ProgramNode: statements: list
@dataclass
class FuncDefNode: name_token: Any; arg_name_tokens: list; body_node: Any
@dataclass
class CallNode: node_to_call: Any; arg_nodes: list
@dataclass
class ReturnNode: node: Any
@dataclass
class InputNode: prompt_node: Any
@dataclass
class IntCastNode: node: Any
@dataclass
class IfNode: condition: Any; body: list; elif_cases: list; else_body: list = None
@dataclass
class WhileNode: condition: Any; body: list
@dataclass
class ForNode: var_name: Any; start_value: Any; end_value: Any; body: list
@dataclass
class BreakNode: pass
@dataclass
class ContinueNode: pass
@dataclass
class TryCatchNode: try_body: list; catch_body: list
@dataclass
class ImportNode: file_path_node: Any