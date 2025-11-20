from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db, Session as DBSession, ActivityLog
from api.auth import get_session_from_header
from services import NewtonClient, AISolver
from schemas import (
    AssignmentListItem,
    AssignmentDetail,
    SolveRequest,
    SolveResponse,
    AssignmentStatusResponse,
    QuestionResult,
    QuestionDetail
)
from config import settings
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=List[AssignmentListItem])
async def list_assignments(
    course_hash: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    db_session: DBSession = Depends(get_session_from_header),
    db: Session = Depends(get_db)
):
    """
    List all assignments with optional filters
    """
    newton_client = NewtonClient(db_session.cookies)

    try:
        assignments = []

        # Get courses
        if course_hash:
            courses = [{"hash": course_hash}]
        else:
            courses = await newton_client.get_courses()

        # Get assignments for each course
        for course in courses:
            c_hash = course.get("hash")
            if not c_hash:
                continue

            try:
                result = await newton_client.get_assignments(c_hash, limit=limit)
                course_assignments = result.get("results", []) if isinstance(result, dict) else result

                for assignment in course_assignments:
                    # Parse assignment data
                    item = AssignmentListItem(
                        hash=assignment.get("hash", ""),
                        title=assignment.get("title", ""),
                        type=assignment.get("type", "mixed"),
                        due_date=assignment.get("due_date"),
                        questions_total=assignment.get("questions_count", 0),
                        questions_solved=assignment.get("questions_solved", 0),
                        xp=assignment.get("xp", 0),
                        difficulty=assignment.get("difficulty"),
                        status="completed" if assignment.get("is_completed") else "pending",
                        course_hash=c_hash
                    )

                    # Apply filters
                    if status and item.status != status:
                        continue
                    if difficulty and item.difficulty != difficulty:
                        continue

                    assignments.append(item)

            except Exception as e:
                logger.error(f"Error fetching assignments for course {c_hash}: {str(e)}")
                continue

        return assignments[:limit]

    finally:
        await newton_client.close()


@router.get("/{assignment_hash}", response_model=AssignmentDetail)
async def get_assignment(
    assignment_hash: str,
    course_hash: str = Query(...),
    db_session: DBSession = Depends(get_session_from_header)
):
    """
    Get detailed assignment information including questions
    """
    newton_client = NewtonClient(db_session.cookies)

    try:
        # Get assignment details
        assignment = await newton_client.get_assignment_details(course_hash, assignment_hash)

        # Get questions if it's an assessment
        questions = []
        assessment_hash = assignment.get("assessment", {}).get("hash")

        if assessment_hash:
            assessment = await newton_client.get_assessment_questions(course_hash, assessment_hash)
            raw_questions = assessment.get("questions", [])

            for q in raw_questions:
                question = QuestionDetail(
                    hash=q.get("hash", ""),
                    text=q.get("text", ""),
                    type=q.get("type", "mcq"),
                    options=q.get("options", {}),
                    solved=q.get("is_solved", False),
                    correct=q.get("is_correct")
                )
                questions.append(question)

        return AssignmentDetail(
            hash=assignment.get("hash", ""),
            title=assignment.get("title", ""),
            description=assignment.get("description"),
            type=assignment.get("type", "mixed"),
            questions=questions,
            due_date=assignment.get("due_date"),
            xp=assignment.get("xp", 0),
            difficulty=assignment.get("difficulty")
        )

    finally:
        await newton_client.close()


@router.post("/{assignment_hash}/solve", response_model=SolveResponse)
async def solve_assignment(
    assignment_hash: str,
    request: SolveRequest,
    course_hash: str = Query(...),
    db_session: DBSession = Depends(get_session_from_header),
    db: Session = Depends(get_db)
):
    """
    Solve assignment using AI
    """
    if not settings.anthropic_api_key:
        raise HTTPException(status_code=500, detail="AI solver not configured")

    newton_client = NewtonClient(db_session.cookies)
    ai_solver = AISolver(settings.anthropic_api_key)

    try:
        # Get assignment details
        assignment = await newton_client.get_assignment_details(course_hash, assignment_hash)
        assessment_hash = assignment.get("assessment", {}).get("hash")

        if not assessment_hash:
            raise HTTPException(status_code=400, detail="Assignment has no assessment")

        # Get questions
        assessment = await newton_client.get_assessment_questions(course_hash, assessment_hash)
        questions = assessment.get("questions", [])

        # Filter specific questions if requested
        if request.questions:
            questions = [q for q in questions if q.get("hash") in request.questions]

        results = []
        total_score = 0
        total_questions = len(questions)

        for question in questions:
            q_hash = question.get("hash")
            q_type = question.get("type", "mcq").lower()
            q_text = question.get("text", "")

            try:
                if q_type == "mcq" or q_type == "single_choice":
                    # Solve MCQ
                    options = question.get("options", {})
                    answer, explanation, confidence = await ai_solver.solve_mcq(q_text, options)

                    # Submit if auto_submit mode
                    correct = None
                    if request.mode == "auto_submit":
                        submit_result = await newton_client.submit_mcq(
                            course_hash,
                            assessment_hash,
                            q_hash,
                            answer
                        )
                        correct = submit_result.get("is_correct", False)
                        if correct:
                            total_score += 1

                    results.append(QuestionResult(
                        question_hash=q_hash,
                        solved=True,
                        answer=answer,
                        correct=correct,
                        explanation=explanation
                    ))

                elif "coding" in q_type or "playground" in q_type:
                    # Get playground details
                    playground_hash = question.get("playground", {}).get("hash")
                    if not playground_hash:
                        continue

                    playground = await newton_client.get_coding_playground(course_hash, playground_hash)
                    problem = playground.get("problem_statement", q_text)

                    # Solve coding problem
                    code = await ai_solver.solve_coding(problem)

                    # Submit if auto_submit mode
                    correct = None
                    if request.mode == "auto_submit":
                        submit_result = await newton_client.submit_coding(
                            course_hash,
                            playground_hash,
                            code
                        )
                        # Check if all test cases passed
                        test_results = submit_result.get("test_results", [])
                        passed = all(t.get("passed", False) for t in test_results)
                        correct = passed
                        if passed:
                            total_score += 1

                    results.append(QuestionResult(
                        question_hash=q_hash,
                        solved=True,
                        answer=code,
                        correct=correct,
                        explanation="Code solution generated"
                    ))

                elif "frontend" in q_type or "html" in q_type:
                    # Get playground details
                    playground_hash = question.get("playground", {}).get("hash")
                    if not playground_hash:
                        continue

                    playground = await newton_client.get_frontend_playground(course_hash, playground_hash)
                    requirements = playground.get("problem_statement", q_text)

                    # Solve frontend problem
                    html, css, js = await ai_solver.solve_frontend(requirements)

                    # Submit if auto_submit mode
                    correct = None
                    if request.mode == "auto_submit":
                        submit_result = await newton_client.submit_frontend(
                            course_hash,
                            playground_hash,
                            html,
                            css,
                            js
                        )
                        # Frontend is usually auto-accepted
                        correct = True
                        total_score += 1

                    results.append(QuestionResult(
                        question_hash=q_hash,
                        solved=True,
                        answer={"html": html, "css": css, "js": js},
                        correct=correct,
                        explanation="Frontend solution generated"
                    ))

            except Exception as e:
                logger.error(f"Error solving question {q_hash}: {str(e)}")
                results.append(QuestionResult(
                    question_hash=q_hash,
                    solved=False,
                    answer=None,
                    explanation=f"Error: {str(e)}"
                ))

        # Calculate score
        score = (total_score / total_questions * 100) if total_questions > 0 else 0
        xp_earned = int(assignment.get("xp", 0) * (score / 100))

        # Log activity
        log = ActivityLog(
            user_email=db_session.user_email,
            action_type="solve_assignment",
            details={
                "assignment_hash": assignment_hash,
                "mode": request.mode,
                "score": score,
                "questions_solved": len(results)
            },
            status="success"
        )
        db.add(log)
        db.commit()

        return SolveResponse(
            status="completed",
            results=results,
            score=score if request.mode == "auto_submit" else None,
            xp_earned=xp_earned if request.mode == "auto_submit" else None
        )

    finally:
        await newton_client.close()


@router.get("/{assignment_hash}/status", response_model=AssignmentStatusResponse)
async def get_assignment_status(
    assignment_hash: str,
    course_hash: str = Query(...),
    db_session: DBSession = Depends(get_session_from_header)
):
    """
    Get assignment completion status
    """
    newton_client = NewtonClient(db_session.cookies)

    try:
        assignment = await newton_client.get_assignment_details(course_hash, assignment_hash)

        return AssignmentStatusResponse(
            solved=assignment.get("questions_solved", 0),
            total=assignment.get("questions_count", 0),
            score=assignment.get("score"),
            submitted=assignment.get("is_completed", False)
        )

    finally:
        await newton_client.close()
