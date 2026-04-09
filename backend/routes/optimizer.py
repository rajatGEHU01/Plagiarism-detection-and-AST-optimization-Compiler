from fastapi import APIRouter
from pydantic import BaseModel

from services.codelite_service import optimize_codelite

router = APIRouter()


# -------------------------------
# Request Model
# -------------------------------
class CodeInput(BaseModel):
    code: str


# -------------------------------
# Endpoint: Code Optimization
# -------------------------------
@router.post("/optimize-code")
def optimize(data: CodeInput):
    """
    Optimize CodeLite++ code using AST transformations.
    
    Returns:
    - Optimized Python code
    - List of optimizations applied
    """
    result = optimize_codelite(data.code)
    return result