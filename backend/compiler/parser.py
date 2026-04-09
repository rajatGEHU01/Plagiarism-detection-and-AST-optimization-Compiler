from compiler.ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # ---------------------------------------------------------
    # Helper Methods
    # ---------------------------------------------------------
    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("EOF", "")

    def eat(self, token_type):
        """
        Consumes the current token if it matches the expected type.
        If not, it raises a detailed Syntax Error for the UI.
        """
        if self.current()[0] == token_type:
            token = self.current()
            self.pos += 1
            return token
        else:
            raise Exception(f"Expected {token_type}, but got {self.current()[0]} ('{self.current()[1]}')")

    # ---------------------------------------------------------
    # Entry Point
    # ---------------------------------------------------------
    def parse(self):
        statements = []
        while self.current()[0] != "EOF":
            statements.append(self.statement())
        return Program(statements)

    # ---------------------------------------------------------
    # Statement Handling
    # ---------------------------------------------------------
    def statement(self):
        tok_type = self.current()[0]

        # C++ style variable declarations
        if tok_type in ("INT", "FLOAT", "STRING_TYPE"):
            return self.var_decl()

        # Assignments or Increment/Decrement
        elif tok_type == "IDENTIFIER":
            return self.assignment_or_inc()

        # Built-in Commands
        elif tok_type == "PRINT":
            self.eat("PRINT")
            return Print(self.expression())

        elif tok_type == "INPUT":
            self.eat("INPUT")
            name = self.eat("IDENTIFIER")[1]
            return Input(name)

        # Control Flow (Python-style colons)
        elif tok_type == "IF":
            return self.if_stmt()

        elif tok_type == "WHILE":
            return self.while_stmt()

        elif tok_type == "FUNC":
            return self.func_def()

        elif tok_type == "RETURN":
            self.eat("RETURN")
            return Return(self.expression())

        # COMPLEXITY FIX: Handle math or standalone expressions
        # This prevents the 'Unexpected token MULT' error by 
        # allowing lines to start with values or math operators.
        else:
            return self.expression()

    # ---------------------------------------------------------
    # Specific Rules
    # ---------------------------------------------------------
    def var_decl(self):
        var_type = self.eat(self.current()[0])[1]
        name = self.eat("IDENTIFIER")[1]
        self.eat("ASSIGN")
        value = self.expression()
        return VarDecl(var_type, name, value)

    def assignment_or_inc(self):
        name = self.eat("IDENTIFIER")[1]
        
        if self.current()[0] == "INCREMENT":
            self.eat("INCREMENT")
            return Increment(name)
        elif self.current()[0] == "DECREMENT":
            self.eat("DECREMENT")
            return Decrement(name)
        elif self.current()[0] == "ASSIGN":
            self.eat("ASSIGN")
            return Assignment(name, self.expression())
        else:
            # Fallback for function calls or IDs used in expressions
            self.pos -= 1 
            return self.expression()

    def if_stmt(self):
        self.eat("IF")
        condition = self.expression()
        self.eat("COLON")
        body = self.block()
        
        else_body = None
        if self.current()[0] == "ELSE":
            self.eat("ELSE")
            self.eat("COLON")
            else_body = self.block()
        return If(condition, body, else_body)

    def while_stmt(self):
        self.eat("WHILE")
        condition = self.expression()
        self.eat("COLON")
        body = self.block()
        return While(condition, body)

    def func_def(self):
        self.eat("FUNC")
        name = self.eat("IDENTIFIER")[1]
        self.eat("LPAREN")
        params = []
        while self.current()[0] != "RPAREN":
            params.append(self.eat("IDENTIFIER")[1])
            if self.current()[0] == "COMMA":
                self.eat("COMMA")
        self.eat("RPAREN")
        self.eat("COLON")
        body = self.block()
        return Function(name, params, body)

    def block(self):
        """Processes multiple statements inside an indented scope."""
        statements = []
        # Stop block when hitting a keyword that changes top-level structure
        while self.current()[0] not in ("EOF", "ELSE", "FUNC"):
            statements.append(self.statement())
            # Basic break to prevent infinite loops in nested blocks
            if self.current()[0] in ("FUNC", "IF", "WHILE"):
                break
        return statements

    # ---------------------------------------------------------
    # Expression Engine (Precedence & Operations)
    # ---------------------------------------------------------
    def expression(self):
        """
        Handles all Binary Operations (Math and Comparison).
        Includes MULT and DIV to solve your previous error.
        """
        left = self.term()
        # Ensure the parser loops through all operators in the sequence
        while self.current()[0] in ("PLUS", "MINUS", "MULT", "DIV", "LT", "GT", "EQ", "LE", "GE", "AND", "OR"):
            op = self.current()[1]
            self.eat(self.current()[0])
            right = self.term()
            left = BinaryOp(left, op, right)
        return left

    def term(self):
        """Processes base units: Numbers, Strings, Identifiers, and Arrays."""
        tok = self.current()
        
        if tok[0] == "NUMBER":
            self.eat("NUMBER")
            return Number(tok[1])
        
        elif tok[0] == "STRING":
            self.eat("STRING")
            return String(tok[1])
        
        elif tok[0] == "IDENTIFIER":
            name = self.eat("IDENTIFIER")[1]
            # Handle Array Indexing (e.g., arr[0])
            if self.current()[0] == "LBRACKET":
                self.eat("LBRACKET")
                index = self.expression()
                self.eat("RBRACKET")
                return Index(name, index)
            return Identifier(name)
        
        elif tok[0] == "LBRACKET":
            return self.array()
            
        elif tok[0] == "LPAREN":
            self.eat("LPAREN")
            expr = self.expression()
            self.eat("RPAREN")
            return expr
            
        else:
            raise Exception(f"Unexpected token in expression: {tok}")

    def array(self):
        self.eat("LBRACKET")
        elements = []
        while self.current()[0] != "RBRACKET":
            elements.append(self.expression())
            if self.current()[0] == "COMMA":
                self.eat("COMMA")
        self.eat("RBRACKET")
        return Array(elements)