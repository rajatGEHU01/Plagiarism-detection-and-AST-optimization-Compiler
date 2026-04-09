from compiler.ast_nodes import *


class CodeGenerator:
    def __init__(self):
        self.code = []
        self.indent_level = 0

    # -------------------------------
    # Helpers
    # -------------------------------
    def indent(self):
        return "    " * self.indent_level

    def emit(self, line):
        self.code.append(self.indent() + line)

    # -------------------------------
    # Entry
    # -------------------------------
    def generate(self, node):
        method = f"gen_{type(node).__name__}"
        return getattr(self, method, self.generic_gen)(node)

    def generic_gen(self, node):
        raise Exception(f"Unknown node type: {type(node).__name__}")

    # =====================================================
    # PROGRAM
    # =====================================================
    def gen_Program(self, node):
        for stmt in node.statements:
            self.generate(stmt)

    # =====================================================
    # STATEMENTS
    # =====================================================
    def gen_VarDecl(self, node):
        self.emit(f"{node.name} = {self.expr(node.value)}")

    def gen_Assignment(self, node):
        self.emit(f"{node.name} = {self.expr(node.value)}")

    def gen_Print(self, node):
        self.emit(f"print({self.expr(node.value)})")

    def gen_Input(self, node):
        self.emit(f"{node.name} = int(input())")

    def gen_If(self, node):
        self.emit(f"if {self.expr(node.condition)}:")
        self.indent_level += 1

        for stmt in node.body:
            self.generate(stmt)

        self.indent_level -= 1

        if node.else_body:
            self.emit("else:")
            self.indent_level += 1

            for stmt in node.else_body:
                self.generate(stmt)

            self.indent_level -= 1

    def gen_While(self, node):
        self.emit(f"while {self.expr(node.condition)}:")
        self.indent_level += 1

        for stmt in node.body:
            self.generate(stmt)

        self.indent_level -= 1

    def gen_Function(self, node):
        params = ", ".join(node.params)
        self.emit(f"def {node.name}({params}):")
        self.indent_level += 1

        for stmt in node.body:
            self.generate(stmt)

        # Ensure function is not empty
        if not node.body:
            self.emit("pass")

        self.indent_level -= 1

    def gen_Return(self, node):
        self.emit(f"return {self.expr(node.value)}")

    def gen_Increment(self, node):
        self.emit(f"{node.name} += 1")

    def gen_Decrement(self, node):
        self.emit(f"{node.name} -= 1")

    # =====================================================
    # EXPRESSIONS
    # =====================================================
    def expr(self, node):
        if isinstance(node, Number):
            return node.value

        elif isinstance(node, String):
            return node.value

        elif isinstance(node, Identifier):
            return node.name

        elif isinstance(node, BinaryOp):
            return f"{self.expr(node.left)} {node.op} {self.expr(node.right)}"

        elif isinstance(node, Array):
            elements = ", ".join(self.expr(e) for e in node.elements)
            return f"[{elements}]"

        elif isinstance(node, Index):
            return f"{node.array}[{self.expr(node.index)}]"

        else:
            raise Exception(f"Unknown expression: {type(node).__name__}")

    # -------------------------------
    def get_code(self):
        return "\n".join(self.code)