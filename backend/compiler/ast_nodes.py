# -------------------------------
# Base Node
# -------------------------------
class Node:
    pass


# -------------------------------
# Program Root
# -------------------------------
class Program(Node):
    def __init__(self, statements):
        self.statements = statements


# =====================================================
# STATEMENTS
# =====================================================

class VarDecl(Node):
    def __init__(self, var_type, name, value):
        self.var_type = var_type   # int / float / string
        self.name = name
        self.value = value


class Assignment(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Print(Node):
    def __init__(self, value):
        self.value = value


class Input(Node):
    def __init__(self, name):
        self.name = name


class If(Node):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body


class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class Function(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class Return(Node):
    def __init__(self, value):
        self.value = value


class Increment(Node):
    def __init__(self, name):
        self.name = name


class Decrement(Node):
    def __init__(self, name):
        self.name = name


# =====================================================
# EXPRESSIONS
# =====================================================

class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Number(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Identifier(Node):
    def __init__(self, name):
        self.name = name


class Array(Node):
    def __init__(self, elements):
        self.elements = elements


class Index(Node):
    def __init__(self, array, index):
        self.array = array   # variable name
        self.index = index   # expression


# =====================================================
# OPTIONAL: Debug Helper (very useful)
# =====================================================

def print_ast(node, indent=0):
    """
    Pretty-print AST for debugging
    """
    space = "  " * indent

    if isinstance(node, list):
        for item in node:
            print_ast(item, indent)
        return

    print(f"{space}{type(node).__name__}")

    for attr, value in vars(node).items():
        if isinstance(value, Node) or isinstance(value, list):
            print(f"{space}  {attr}:")
            print_ast(value, indent + 2)
        else:
            print(f"{space}  {attr}: {value}")