import difflib

def compute_final_score(ast1, ast2, tokens1, tokens2):
    """
    Detailed multi-metric plagiarism analysis
    """
    
    # 1. Token Sequence Similarity (Normalized)
    # We ignore the actual values (names) and only look at the TYPES of tokens
    t1_types = [t[0] for t in tokens1]
    t2_types = [t[0] for t in tokens2]
    token_sim = difflib.SequenceMatcher(None, t1_types, t2_types).ratio() * 100

    # 2. AST Node Structure
    # Compares the sequence of operations (e.g., VarDecl -> While -> Print)
    def flatten_ast(node):
        nodes = []
        if isinstance(node, list):
            for item in node: nodes.extend(flatten_ast(item))
        elif hasattr(node, '__dict__'):
            nodes.append(type(node).__name__)
            for attr in vars(node).values():
                nodes.extend(flatten_ast(attr))
        return nodes

    ast1_flat = flatten_ast(ast1)
    ast2_flat = flatten_ast(ast2)
    ast_sim = difflib.SequenceMatcher(None, ast1_flat, ast2_flat).ratio() * 100

    # 3. Pattern/Logic Fingerprinting
    # Checks for similar nesting levels and logic flow
    pattern_score = (ast_sim * 0.7) + (token_sim * 0.3)

    # 4. Function Logic Similarity
    f1 = [n for n in ast1_flat if n == "Function"]
    f2 = [n for n in ast2_flat if n == "Function"]
    func_sim = 100.0 if (len(f1) == len(f2) and len(f1) > 0) else 0.0
    if len(f1) != len(f2):
        func_sim = (min(len(f1), len(f2)) / max(len(f1), len(f2))) * 100 if max(len(f1), len(f2)) > 0 else 0

    # Weighted Calculation
    final_score = (ast_sim * 0.45) + (token_sim * 0.25) + (pattern_score * 0.30)
    
    # Determine confidence level
    confidence = "LOW"
    if final_score > 80: confidence = "HIGH"
    elif final_score > 45: confidence = "MEDIUM"

    return {
        "final_score": round(final_score, 2),
        "confidence": confidence,
        "breakdown": {
            "ast": round(ast_sim, 2),
            "token": round(token_sim, 2),
            "pattern": round(pattern_score, 2),
            "function": round(func_sim, 2)
        }
    }