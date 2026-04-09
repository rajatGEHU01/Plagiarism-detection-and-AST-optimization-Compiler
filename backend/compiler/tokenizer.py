import re
from typing import List, Tuple

# Token = (TYPE, VALUE)
Token = Tuple[str, str]

# ---------------------------------------------------------
# Expanded Token Definitions for CodeLite++
# ---------------------------------------------------------
TOKEN_SPEC = [
    # Literals
    ("NUMBER",      r"\d+(\.\d+)?"),           # Supports ints and floats
    ("STRING",      r'"[^"]*"'),               # Supports double-quoted strings
    
    # Data Types (C++ Style)
    ("INT",         r"\bint\b"),
    ("FLOAT",       r"\bfloat\b"),
    ("STRING_TYPE", r"\bstring\b"),
    
    # Keywords (Hybrid Style)
    ("FUNC",        r"\bfunc\b"),              # Function definition
    ("RETURN",      r"\breturn\b"),
    ("IF",          r"\bif\b"),
    ("ELSE",        r"\belse\b"),
    ("WHILE",       r"\bwhile\b"),
    ("INPUT",       r"\binput\b"),
    ("PRINT",       r"\bprint\b"),
    
    # Logical Operators
    ("AND",         r"\band\b"),
    ("OR",          r"\bor\b"),

    # Multi-Character Operators (Must be defined BEFORE single chars)
    ("INCREMENT",   r"\+\+"),                  # C++ Style
    ("DECREMENT",   r"--"),                    # C++ Style
    ("EQ",          r"=="),                    # Comparison
    ("NEQ",         r"!="),
    ("LE",          r"<="),
    ("GE",          r">="),

    # Single Operators
    ("ASSIGN",      r"="),
    ("LT",          r"<"),
    ("GT",          r">"),
    ("PLUS",        r"\+"),
    ("MINUS",       r"-"),
    ("MULT",        r"\*"),
    ("DIV",         r"/"),

    # Symbols
    ("LPAREN",      r"\(|（"),                 # Supports standard and full-width parens
    ("RPAREN",      r"\)|）"),
    ("LBRACKET",    r"\["),
    ("RBRACKET",    r"\]"),
    ("COMMA",       r","),
    ("COLON",       r":"),                     # Python Style block starts

    # Identifiers (Variable and function names)
    ("IDENTIFIER",  r"[a-zA-Z_][a-zA-Z0-9_]*"),

    # Ignored Patterns
    ("COMMENT",     r"#.*"),                   # Python Style comments
    ("NEWLINE",     r"\n"),
    ("SKIP",        r"[ \t]+"),                # Whitespace
]

# Build the master regex string
MASTER_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)

def tokenize(code: str) -> List[Token]:
    """
    Converts raw CodeLite++ source into a stream of tokens.
    """
    tokens = []
    for match in re.finditer(MASTER_REGEX, code):
        kind = match.lastgroup
        value = match.group()

        # We skip noise like spaces and comments, but keep track of keywords
        if kind in ("SKIP", "COMMENT", "NEWLINE"):
            continue
        
        tokens.append((kind, value))

    return tokens