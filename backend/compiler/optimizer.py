from compiler.ast_nodes import *

class Optimizer:
    def __init__(self):
        # This list tracks changes to show in the Frontend UI
        self.optimizations = []

    def optimize(self, node):
        if node is None:
            return None
        method = f"opt_{type(node).__name__}"
        return getattr(self, method, self.generic_opt)(node)

    def generic_opt(self, node):
        return node

    def opt_Program(self, node):
        node.statements = [self.optimize(s) for s in node.statements]
        node.statements = [s for s in node.statements if s is not None]
        return node

    def opt_VarDecl(self, node):
        node.value = self.optimize(node.value)
        return node

    def opt_Assignment(self, node):
        node.value = self.optimize(node.value)
        return node

    def opt_BinaryOp(self, node):
        node.left = self.optimize(node.left)
        node.right = self.optimize(node.right)

        # Constant Folding Logic
        if isinstance(node.left, Number) and isinstance(node.right, Number):
            try:
                l_val = float(node.left.value)
                r_val = float(node.right.value)
                res = 0
                if node.op == '+': res = l_val + r_val
                elif node.op == '-': res = l_val - r_val
                elif node.op == '*': res = l_val * r_val
                elif node.op == '/' and r_val != 0: res = l_val / r_val
                else: return node

                self.optimizations.append(f"Folded math: {l_val} {node.op} {r_val} → {res}")
                return Number(str(int(res) if res.is_integer() else res))
            except:
                return node
        return node

    def opt_If(self, node):
        node.condition = self.optimize(node.condition)
        
        # Dead Code Removal
        if isinstance(node.condition, Number):
            val = float(node.condition.value)
            if val == 0:
                self.optimizations.append("Removed 'if' block: condition is always False")
                return self.optimize(node.else_body) if node.else_body else None
            else:
                self.optimizations.append("Simplified 'if': condition is always True")
                return node.body # In a real compiler, you'd flatten this

        node.body = [self.optimize(s) for s in node.body if s]
        if node.else_body:
            node.else_body = [self.optimize(s) for s in node.else_body if s]
        return node

    def opt_While(self, node):
        node.condition = self.optimize(node.condition)
        if isinstance(node.condition, Number) and float(node.condition.value) == 0:
            self.optimizations.append("Removed unreachable 'while' loop")
            return None
        node.body = [self.optimize(s) for s in node.body if s]
        return node