from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Auth Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    session_id: str
    user: Dict[str, Any]
    message: str = "Login successful"


class AuthStatus(BaseModel):
    authenticated: bool
    user: Optional[Dict[str, Any]] = None


# Assignment Schemas
class AssignmentType(str, Enum):
    MCQ = "mcq"
    CODING = "coding"
    FRONTEND = "frontend"
    MIXED = "mixed"


class AssignmentStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class AssignmentDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class AssignmentListItem(BaseModel):
    hash: str
    title: str
    type: str
    due_date: Optional[datetime] = None
    questions_total: int
    questions_solved: int
    xp: int
    difficulty: Optional[str] = None
    status: str
    course_hash: str


class QuestionDetail(BaseModel):
    hash: str
    text: str
    type: str
    options: Optional[Dict[str, str]] = None
    solved: bool = False
    correct: Optional[bool] = None


class AssignmentDetail(BaseModel):
    hash: str
    title: str
    description: Optional[str] = None
    type: str
    questions: List[QuestionDetail]
    due_date: Optional[datetime] = None
    xp: int
    difficulty: Optional[str] = None


class SolveMode(str, Enum):
    LEARNING = "learning"
    AUTO_SUBMIT = "auto_submit"


class SolveRequest(BaseModel):
    mode: SolveMode = SolveMode.LEARNING
    questions: Optional[List[str]] = None  # Specific question hashes to solve


class QuestionResult(BaseModel):
    question_hash: str
    solved: bool
    answer: Any
    correct: Optional[bool] = None
    explanation: Optional[str] = None


class SolveResponse(BaseModel):
    status: str
    results: List[QuestionResult]
    score: Optional[float] = None
    xp_earned: Optional[int] = None


class AssignmentStatusResponse(BaseModel):
    solved: int
    total: int
    score: Optional[float] = None
    submitted: bool


# Schedule Schemas
class ClassSession(BaseModel):
    hash: str
    time: str
    subject: str
    room: Optional[str] = None
    join_url: Optional[str] = None
    instructor: Optional[str] = None
    start_timestamp: int
    end_timestamp: int


class JoinClassRequest(BaseModel):
    lecture_slot_hash: str


class JoinClassResponse(BaseModel):
    join_url: str
    status: str = "opened"


# Solver Schemas
class MCQSolveRequest(BaseModel):
    question: str
    options: Dict[str, str]
    context: Optional[str] = None


class MCQSolveResponse(BaseModel):
    answer: str
    confidence: float
    explanation: str


class CodingSolveRequest(BaseModel):
    problem: str
    language: str = "python"
    test_cases: Optional[str] = None
    constraints: Optional[str] = None


class CodingSolveResponse(BaseModel):
    code: str
    language: str


class FrontendSolveRequest(BaseModel):
    requirements: str
    reference_image: Optional[str] = None


class FrontendSolveResponse(BaseModel):
    html: str
    css: str
    javascript: str


# Performance Schemas
class PerformanceOverview(BaseModel):
    lecture_attendance: float
    assignments_completed: float
    total_xp: int
    streak_days: int


class CoursePerformance(BaseModel):
    course_hash: str
    course_name: str
    attendance: float
    assignments: float
    quizzes: Optional[float] = None


# Course Schemas
class CourseListItem(BaseModel):
    hash: str
    name: str
    enrolled: bool
    instructor: Optional[str] = None


class CourseDetail(BaseModel):
    hash: str
    name: str
    lectures: int
    attendance: float
    assignments_total: int
    assignments_completed: int


# User Schema
class UserInfo(BaseModel):
    name: str
    email: str
    courses: List[str]
