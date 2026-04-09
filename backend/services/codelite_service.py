from compiler.tokenizer import tokenize
from compiler.parser import Parser
from compiler.optimizer import Optimizer
from compiler.codegen import CodeGenerator
from compiler.plagiarism import compute_final_score


# -------------------------------
# Compile CodeLite++ → Tokens + AST
# -------------------------------
def compile_code(code: str):
    """
    Converts CodeLite++ code into tokens and AST
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    return tokens, ast


# -------------------------------
# Plagiarism Check Service
# -------------------------------
def check_plagiarism(code1: str, code2: str):
    """
    Runs full plagiarism pipeline:
    Tokenize → Parse → Compare
    """
    try:
        tokens1, ast1 = compile_code(code1)
        tokens2, ast2 = compile_code(code2)

        result = compute_final_score(ast1, ast2, tokens1, tokens2)

        return result

    except Exception as e:
        return {
            "error": str(e)
        }


# -------------------------------
# Code Optimization Service
# -------------------------------
def optimize_codelite(code: str):
    """
    Runs optimization pipeline:
    Parse → Optimize AST → Generate Python code
    """
    try:
        tokens, ast = compile_code(code)

        # Optimize AST
        optimizer = Optimizer()
        optimized_ast = optimizer.optimize(ast)

        # Generate Python code
        generator = CodeGenerator()
        generator.generate(optimized_ast)

        return {
            "optimized_code": generator.get_code(),
            "optimizations": optimizer.optimizations
        }

    except Exception as e:
        return {
            "error": str(e)
        }