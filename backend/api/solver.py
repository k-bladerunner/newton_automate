from fastapi import APIRouter, Depends, HTTPException
from services import AISolver
from schemas import (
    MCQSolveRequest,
    MCQSolveResponse,
    CodingSolveRequest,
    CodingSolveResponse,
    FrontendSolveRequest,
    FrontendSolveResponse
)
from config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


def get_ai_solver():
    """Dependency to get AI solver"""
    if not settings.anthropic_api_key:
        raise HTTPException(status_code=500, detail="AI solver not configured")
    return AISolver(settings.anthropic_api_key)


@router.post("/mcq", response_model=MCQSolveResponse)
async def solve_mcq(
    request: MCQSolveRequest,
    solver: AISolver = Depends(get_ai_solver)
):
    """
    Solve a single MCQ question
    """
    try:
        answer, explanation, confidence = await solver.solve_mcq(
            question=request.question,
            options=request.options,
            context=request.context
        )

        return MCQSolveResponse(
            answer=answer,
            confidence=confidence,
            explanation=explanation
        )

    except Exception as e:
        logger.error(f"Error solving MCQ: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to solve MCQ: {str(e)}")


@router.post("/coding", response_model=CodingSolveResponse)
async def solve_coding(
    request: CodingSolveRequest,
    solver: AISolver = Depends(get_ai_solver)
):
    """
    Solve a coding problem
    """
    try:
        code = await solver.solve_coding(
            problem=request.problem,
            test_cases=request.test_cases,
            constraints=request.constraints,
            language=request.language
        )

        return CodingSolveResponse(
            code=code,
            language=request.language
        )

    except Exception as e:
        logger.error(f"Error solving coding problem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to solve coding problem: {str(e)}")


@router.post("/frontend", response_model=FrontendSolveResponse)
async def solve_frontend(
    request: FrontendSolveRequest,
    solver: AISolver = Depends(get_ai_solver)
):
    """
    Solve a frontend problem
    """
    try:
        html, css, js = await solver.solve_frontend(
            requirements=request.requirements,
            reference_image=request.reference_image
        )

        return FrontendSolveResponse(
            html=html,
            css=css,
            javascript=js
        )

    except Exception as e:
        logger.error(f"Error solving frontend problem: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to solve frontend problem: {str(e)}")
