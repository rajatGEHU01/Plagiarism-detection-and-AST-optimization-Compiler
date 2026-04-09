from fastapi import APIRouter
from pydantic import BaseModel

from services.codelite_service import check_plagiarism

router = APIRouter()


# -------------------------------
# Request Model
# -------------------------------
class CodeInput(BaseModel):
    code1: str
    code2: str


# -------------------------------
# Endpoint: Plagiarism Check
# -------------------------------
@router.post("/plagiarism-check")
def plagiarism_check(data: CodeInput):
    """
    Compare two CodeLite++ programs and return similarity score,
    confidence level, and detailed breakdown.
    """
    result = check_plagiarism(data.code1, data.code2)
    return result