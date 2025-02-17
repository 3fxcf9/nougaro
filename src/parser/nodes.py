#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Nougaro : a python-interpreted high-level programming language
# Copyright (C) 2021-2024  Jean Dubois (https://github.com/jd-develop) <jd-dev@laposte.net>
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# IMPORTS
# nougaro modules imports
from src.lexer.position import Position
from src.lexer.token import Token
from src.lexer.token_types import TT
# built-in python imports
# no imports


# ##########
# NODES
# ##########
class Node:
    pos_start = None
    pos_end = None
    attr = False


# VALUE NODES
class NumberNode(Node):
    """Node for numbers (both int and float). The tok type can be TT_INT or TT_FLOAT"""
    def __init__(self, token: Token):
        self.token: Token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'num:{self.token}'


class NumberENumberNode(Node):
    """Node for numbers like 10e2 or 4e-5"""
    def __init__(self, num_token: Token, exponent_token: Token):
        self.num_token = num_token
        self.exponent_token = exponent_token

        self.pos_start = num_token.pos_start
        self.pos_end = exponent_token.pos_end

    def __repr__(self):
        return f'numE:({self.num_token})e({self.exponent_token})'


class StringNode(Node):
    """Node for strings. Tok type can be TT_STRING"""
    def __init__(self, token: Token):
        self.token: Token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'string_node:{self.token}'


class ListNode(Node):
    """Node for list. self.element_nodes is a list of nodes. Needs pos_start and pos_end when init."""
    def __init__(self, element_nodes: list[tuple[Node, bool]], pos_start: Position, pos_end: Position):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'list:{str(self.element_nodes)}'


# VAR NODES
class VarAssignNode(Node):
    """Node for variable assign
    I’m too bored to rewrite examples. TODO: rewrite examples"""
    def __init__(
            self,
            var_names: list[list[Token | Node]],
            value_nodes: list[Node] | None,
            equal: Token = Token(TT["EQ"])
    ):
        self.var_names: list[list[Token | Node]] = var_names
        self.value_nodes = value_nodes
        self.equal = equal

        self.pos_start = self.var_names[0][0].pos_start
        if self.value_nodes is not None:
            self.pos_end = self.value_nodes[-1].pos_end
        else:
            self.pos_end = self.equal.pos_end

    def __repr__(self):
        return f'var_assign:({self.var_names} {self.equal} {self.value_nodes})'


class VarAccessNode(Node):
    """Node for variable access
    attr parameter is True when the var we try to access is an attribute, False if it is a global or local variable
    example: `foo`: var_name_tokens_list is [Token(TT_IDENTIFIER, 'foo')]
    example 2: `foo ? bar`: var_name_tokens_list is [Token(TT_IDENTIFIER, 'foo'), Token(TT_IDENTIFIER, 'bar')]
    """
    def __init__(self, var_name_tokens_list: list[Token | Node], attr: bool = False):
        self.var_name_tokens_list = var_name_tokens_list
        self.attr = attr

        self.pos_start = self.var_name_tokens_list[0].pos_start
        self.pos_end = self.var_name_tokens_list[-1].pos_end

    def __repr__(self):
        return f'var_access:{self.var_name_tokens_list}({self.attr})'


class VarDeleteNode(Node):
    """Node for variable delete, such as `del foo` where var_name_token is Token(TT_IDENTIFIER, 'foo')"""
    def __init__(self, var_name_token: Token):
        self.var_name_token = var_name_token
        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end

    def __repr__(self):
        return f'var_delete:{self.var_name_token}'


# OPERATOR NODES
class BinOpNode(Node):
    """Node for binary operations.
    Todo: rewrite examples
    """
    def __init__(self, left_node: Node | list[Node], op_token: Token, right_node: Node | list[Node]):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

        if isinstance(self.left_node, list):
            self.pos_start = self.left_node[0].pos_start
        else:
            self.pos_start = self.left_node.pos_start
        if isinstance(self.right_node, list):
            self.pos_end = self.right_node[-1].pos_end
        else:
            self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'bin_op:({self.left_node}, {self.op_token}, {self.right_node})'


class BinOpCompNode(Node):
    """Same as BinOpNode for comp operators (>, <, >=, ...)
    nodes_and_tokens_list are the list of all nodes and operator tokens, such as
        [NumberNode, Token(TT_NE), VarAccessNode, Token(TT_GTE), NumberNode, Token(TT_EE), ReadNode]

    Yeah, you can use ReadNodes here x)
    But IDK who makes that, because results of 'read' statement are often put into a variable...
    """
    def __init__(self, nodes_and_tokens_list: list[Node | Token | list[Node]]):
        self.nodes_and_tokens_list = nodes_and_tokens_list

        if isinstance(self.nodes_and_tokens_list[0], list):
            self.pos_start = self.nodes_and_tokens_list[0][0].pos_start
        else:
            self.pos_start = self.nodes_and_tokens_list[0].pos_start

        if isinstance(self.nodes_and_tokens_list[-1], list):
            self.pos_end = self.nodes_and_tokens_list[-1][-1].pos_end
        else:
            self.pos_end = self.nodes_and_tokens_list[-1].pos_end

    def __repr__(self):
        return f'bin_op_comp:({", ".join([str(x) for x in self.nodes_and_tokens_list])})'


class UnaryOpNode(Node):
    """Node for Unary operator (such as `not 1` or `~12`)
        op_token is the operator token. In these examples, it is respectively Token(TT_KEYWORD, 'not') and\
                                                                                                Token(TT_BITWISENOT)
        node is the node after the operator. In these examples, these are both NumberNode, the first with the number
                                             tok Token(TT_INT, 1) and the second with Token(TT_INT, 12)
    """
    def __init__(self, op_token: Token, node: Node | list[Node]):
        self.op_token = op_token
        self.node = node

        self.pos_start = self.op_token.pos_start
        if isinstance(self.node, list):
            self.pos_end = self.node[-1].pos_end
        else:
            self.pos_end = self.node.pos_end

    def __repr__(self):
        return f'unary_op:({self.op_token}, {self.node})'


# TEST NODES
class IfNode(Node):
    """Node for the 'if' structure. All the cases except the else case are in 'cases'.
    A case is a tuple under this form: (condition, expression if the condition is true)
    condition and expression are both Nodes, and should_return_node is a bool
    An else case is a Node
    """
    def __init__(self, cases: list[tuple[Node, Node]], else_case: Node | None, debug: bool = False):
        self.cases: list[tuple[Node, Node]] = cases
        self.else_case: Node | None = else_case

        self.pos_start = self.cases[0][0].pos_start

        if debug:
            print(f"else_case: type {type(self.else_case)}, value " + str(self.else_case))
            print(f"cases[-1][0]: type {type(self.cases[-1][0])}, value " + str(self.cases[-1][0]))
        self.pos_end = (self.else_case or self.cases[-1][0]).pos_end

    def __repr__(self):
        return f'if {self.cases[0][0]} then {self.cases[0][1]} ' \
               f'{" ".join([f"elif {case[0]} then {case[1]}" for case in self.cases[1:]])} ' \
               f'else {self.else_case}'


class AssertNode(Node):
    """Node for the 'assert' structure, such as `assert False, "blah blah blah that is an error message"`
    In this example, assertion is a VarAccessNode (identifier: False), and errmsg is a StringNode.
    errmsg can be None, like in `assert False`.
    """
    def __init__(self, assertion: Node, pos_start: Position, pos_end: Position, errmsg: Node | None = None):
        self.assertion = assertion
        self.errmsg = errmsg
        if self.errmsg is None:
            self.errmsg = StringNode(Token(
                TT["STRING"],
                value='',
                pos_start=pos_start.copy(),
                pos_end=pos_end.copy()
            ))

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'assert:({self.assertion}, {self.errmsg})'


# LOOP NODES
class ForNode(Node):
    """Node for 'for a = b to c (step d) then' structure.
    In this example :
        var_name_tok is Token(TT_IDENTIFIER, 'a')
        start_value_node is a VarAccessNode (identifier: b)
        end_value_node is a VarAccessNode (identifier: c)
        step_value_node is None or a VarAccessNode (identifier: d)
        body_node is the node after the 'then'
    """
    def __init__(
            self,
            var_name_token: Token,
            start_value_node: Node,
            end_value_node: Node,
            step_value_node: Node | None,
            body_node: Node,
    ):
        # by default step_value_node is None
        self.var_name_token: Token = var_name_token
        self.start_value_node: Node = start_value_node
        self.end_value_node: Node = end_value_node
        self.step_value_node: Node | None = step_value_node
        self.body_node: Node = body_node

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f"for:({self.var_name_token} = {self.start_value_node} to {self.end_value_node} step " \
               f"{self.step_value_node} then {self.body_node})"


class ForNodeList(Node):
    """Node for 'for a in b then' structure, where b is a list/iterable.
    In this example :
        var_name_tok is Token(TT_IDENTIFIER, 'a')
        body_node is the node after the 'then'
        list_node is a VarAccessNode (identifier: b)
    """
    def __init__(self, var_name_token: Token, body_node: Node, list_node: Node | ListNode):
        # if list = [1, 2, 3]
        # for var in list is same as for var = 1 to 3 (step 1)

        self.var_name_token: Token = var_name_token
        self.body_node = body_node
        self.list_node = list_node

        # Position
        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f"for:({self.var_name_token} in {self.list_node} then {self.body_node})"


class WhileNode(Node):
    """Node for 'while' structure.
    Example: while True then foo()
    Here, condition_node is a VarAccessNode (identifier: True)
          body_node is a CallNode (identifier: foo, no args)*
    """
    def __init__(self, condition_node: Node, body_node: Node):
        self.condition_node: Node = condition_node
        self.body_node: Node = body_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'while:({self.condition_node} then:{self.body_node})'


class DoWhileNode(Node):
    """Node for 'do then loop while' structure.
    Example: do foo() then loop while True
    Here, body_node is a CallNode (identifier: foo, no args)
          condition_node is a VarAccessNode (identifier: True)
    """
    def __init__(self, body_node: Node, condition_node: Node):
        self.body_node = body_node
        self.condition_node = condition_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'do:({self.body_node} then loop while:{self.condition_node})'


class BreakNode(Node):
    """Node for `break` statement"""
    def __init__(self, pos_start: Position, pos_end: Position):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return 'break'


class ContinueNode(Node):
    """Node for `continue` statement"""
    def __init__(self, pos_start: Position, pos_end: Position):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return 'continue'


# FUNCTION NODES
class FuncDefNode(Node):
    """Node for function definition.
    Example: `def a(bar) -> foo(bar)`
        Here, var_name_token is Token(TT_IDENTIFIER, 'a')
              param_names_tokens is [Token(TT_IDENTIFIER, 'bar')]
              body_node is CallNode (identifier: foo, args: bar)
    should_auto_return is bool (it happens in one-line functions)
    If, in the function definition, the name is not defined (like in `def()->void()`), var_name_token is None
    """
    def __init__(self, var_name_token: Token | None, param_names_tokens: list[Token], body_node: Node,
                 should_auto_return: bool):
        self.var_name_token = var_name_token
        self.param_names_tokens = param_names_tokens
        self.body_node = body_node
        self.should_auto_return = should_auto_return

        if self.var_name_token is not None:  # a name is given: we take its pos_start as our pos_start
            self.pos_start = self.var_name_token.pos_start
        elif len(self.param_names_tokens) > 0:  # there is no name given, but there is parameters. We take the first's
            #                                     pos_start as our pos_start.
            self.pos_start = self.param_names_tokens[0].pos_start
        else:  # there is no name nor parameters given, we take the body's pos_start as our pos_start.
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'def:{self.var_name_token}({self.param_names_tokens})->{self.body_node}'


class ClassNode(Node):
    """Node for class statement.
    Example: `class B(A) -> foo(bar)`
        Here, var_name_token is Token(TT_IDENTIFIER, 'B')
              parent_var_name_token is Token(TT_IDENTIFIER, 'A')
              body_node is CallNode (identifier: foo, args: bar)
    should_auto_return is bool (it happens in one-line functions)
    If, in the function definition, the name is not defined (like in `def()->void()`), var_name_token is None
    """
    def __init__(self, var_name_token: Token | None, parent_var_name_token: Token | None, body_node: Node,
                 should_auto_return: bool):
        self.var_name_token = var_name_token
        self.parent_var_name_token = parent_var_name_token
        self.body_node = body_node
        self.should_auto_return = should_auto_return

        if self.var_name_token is not None:  # a name is given: we take its pos_start as our pos_start
            self.pos_start = self.var_name_token.pos_start
        elif self.parent_var_name_token is not None:  # there is no name given, but there is a parent given.
            self.pos_start = self.parent_var_name_token.pos_start
        else:  # there is no name nor parameters given, we take the body's pos_start as our pos_start.
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        if self.parent_var_name_token is not None:
            return f'class:{self.var_name_token}({self.parent_var_name_token})->{self.body_node}'
        else:
            return f'class:{self.var_name_token}->{self.body_node}'


class CallNode(Node):
    """Node for call structure (like `foo(bar, 1)`)
    Here: node_to_call is a VarAccessNode (identifier: foo)
          arg_nodes is [VarAccessNode (identifier: bar), NumberNode (num: 1)]
    If there is no arguments given, arg_nodes is empty.
    """
    def __init__(self, node_to_call: Node, arg_nodes: list[tuple[Node, bool]]):
        self.node_to_call: Node = node_to_call
        self.arg_nodes: list[tuple[Node, bool]] = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:  # if there are arguments, we take the last one's pos_end as our pos_end.
            self.pos_end = self.arg_nodes[-1][0].pos_end
        else:  # if there is no parameter, we take the node_to_call's pos_end as our pos_end.
            self.pos_end = self.node_to_call.pos_end

    def __repr__(self):
        return f'call:{self.node_to_call}({self.arg_nodes})'


class ReturnNode(Node):
    """Node for `return` structure.
    node_to_return is the node after the 'return' keyword. It may be None
    """
    def __init__(self, node_to_return: Node | None, pos_start: Position, pos_end: Position):
        self.node_to_return: Node | None = node_to_return

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'return:({self.node_to_return})'


# MODULE NODES
class ImportNode(Node):
    """Node for `import` structure.
    identifier is the name of the module to import. It is a token. Example: Token(TT_IDENTIFIER, 'math')
    """
    def __init__(self, identifiers: list[Token], pos_start: Position, pos_end: Position,
                 as_identifier: Token | None = None):
        self.identifiers: list[Token] = identifiers
        self.as_identifier: Token | None = as_identifier

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        names = [str(identifier) for identifier in self.identifiers]
        if self.as_identifier is None:
            return f"import:{'.'.join(names)}"
        return f'import:{".".join(names)}:as:{self.as_identifier}'


class ExportNode(Node):
    """Node for `export` structure.
    identifier is the name of the module to import. It is a token. Example: Token(TT_IDENTIFIER, 'lorem_ipsum')
    """
    def __init__(self, expr_or_identifier: Node | Token, as_identifier: Token | None,
                 pos_start: Position, pos_end: Position):
        self.expr_or_identifier: Node | Token = expr_or_identifier
        self.as_identifier: Token | None = as_identifier

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        if self.as_identifier is None:
            return f"export:{self.expr_or_identifier}"
        else:
            return f"export:{self.expr_or_identifier}:as:{self.as_identifier}"


# FILE NODES
class WriteNode(Node):
    """Node for `write` structure.
    Example: `write "some text" >> "path/to/file.ext" 6`
        Here, expr_to_write is a StingNode (value: "some text")
              file_name_expr is a StringNode (value: "path/to/file.ext")
              to_token is Token(TT_TO)
              line_number is a python int (value: 6)
    Example: `write text !>> path`
        Here, expr_to_write is a VarAccessNode (identifier: text)
              file_name_expr is a VarAccessNode (identifier: path)
              to_token is Token(TT_TO_AND_OVERWRITE)
              line_number is a python str (value: "last")

    Note that when interpreting, if to_token type is TT_TO_AND_OVERWRITE, it overwrites one line if a line number is
        given, and all the file if it isn't the case.
    """
    def __init__(self, expr_to_write: Node, file_name_expr: Node, to_token: Token, line_number: str | int,
                 pos_start: Position, pos_end: Position):
        self.expr_to_write: Node = expr_to_write
        self.file_name_expr: Node = file_name_expr
        self.to_token: Token = to_token
        self.line_number: str | int = line_number

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'write:({self.expr_to_write}{self.to_token.type}{self.file_name_expr} at line {self.line_number})'


class ReadNode(Node):
    """Node for `read` structure.
    Example: `read path`
        Here, file_name_expr is a VarAccessNode (identifier: path)
              identifier is None
              line_number is Python str "all"
    Example: `read "path/to/file" >> foo
        Here, file_name_expr is a StringNode (value: "path/to/file")
              identifier is Token(TT_IDENTIFIER, 'foo')
              line_number is Python str "all"
    Example: `read "path/to/file" 6`
        Here, file_name_expr is a StringNode (value: "path/to/file")
              identifier is None
              line_number is Python int 6
    Example: `read path >> foo 6`
        Here, file_name_expr is a VarAccessNode (identifier: path)
              identifier is Token(TT_IDENTIFIER, 'foo')
              line_number is Python int 6

    """
    def __init__(self, file_name_expr: Node, identifier: Token | None, line_number: int | str,
                 pos_start: Position, pos_end: Position):
        self.file_name_expr: Node = file_name_expr
        self.identifier: Token | None = identifier
        self.line_number: int | str = line_number

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'read:({self.file_name_expr}>>{self.identifier} at line {self.line_number})'


class DollarPrintNode(Node):
    """$identifier"""
    def __init__(self, identifier: Token, pos_start: Position, pos_end: Position):
        self.identifier: Token = identifier

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'${self.identifier}'


# SPECIAL NODES
class NoNode(Node):
    """If the file to execute is empty or filled by back lines, this node is the only node of the node list."""
    def __repr__(self):
        return "NoNode"
