from fastapi import APIRouter, Depends
from database import Session as DBSession
from api.auth import get_session_from_header
from services import NewtonClient
from schemas import PerformanceOverview, CoursePerformance
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/overview", response_model=PerformanceOverview)
async def get_performance_overview(
    db_session: DBSession = Depends(get_session_from_header)
):
    """
    Get overall performance overview
    """
    newton_client = NewtonClient(db_session.cookies)

    try:
        # Get courses
        courses = await newton_client.get_courses()

        total_attendance = 0
        total_assignments = 0
        total_xp = 0
        course_count = 0

        for course in courses:
            course_hash = course.get("hash")
            if not course_hash:
                continue

            try:
                # Get course performance
                performance = await newton_client.get_performance_overview(course_hash)

                total_attendance += performance.get("attendance", 0)
                total_assignments += performance.get("assignments_completed", 0)
                total_xp += performance.get("total_xp", 0)
                course_count += 1

            except Exception as e:
                logger.error(f"Error fetching performance for course {course_hash}: {str(e)}")
                continue

        # Calculate averages
        avg_attendance = total_attendance / course_count if course_count > 0 else 0
        avg_assignments = total_assignments / course_count if course_count > 0 else 0

        # TODO: Calculate streak days from activity logs
        streak_days = 0

        return PerformanceOverview(
            lecture_attendance=round(avg_attendance, 1),
            assignments_completed=round(avg_assignments, 1),
            total_xp=total_xp,
            streak_days=streak_days
        )

    finally:
        await newton_client.close()


@router.get("/course/{course_hash}", response_model=CoursePerformance)
async def get_course_performance(
    course_hash: str,
    db_session: DBSession = Depends(get_session_from_header)
):
    """
    Get performance for a specific course
    """
    newton_client = NewtonClient(db_session.cookies)

    try:
        # Get course details
        course = await newton_client.get_course_details(course_hash)
        performance = await newton_client.get_performance_overview(course_hash)

        return CoursePerformance(
            course_hash=course_hash,
            course_name=course.get("name", "Unknown"),
            attendance=performance.get("attendance", 0),
            assignments=performance.get("assignments_completed", 0),
            quizzes=performance.get("quizzes_completed")
        )

    finally:
        await newton_client.close()


@router.get("/courses", response_model=List[CoursePerformance])
async def get_all_courses_performance(
    db_session: DBSession = Depends(get_session_from_header)
):
    """
    Get performance for all enrolled courses
    """
    newton_client = NewtonClient(db_session.cookies)

    try:
        courses = await newton_client.get_courses()
        performances = []

        for course in courses:
            course_hash = course.get("hash")
            if not course_hash:
                continue

            try:
                performance = await newton_client.get_performance_overview(course_hash)

                performances.append(CoursePerformance(
                    course_hash=course_hash,
                    course_name=course.get("name", "Unknown"),
                    attendance=performance.get("attendance", 0),
                    assignments=performance.get("assignments_completed", 0),
                    quizzes=performance.get("quizzes_completed")
                ))

            except Exception as e:
                logger.error(f"Error fetching performance for course {course_hash}: {str(e)}")
                continue

        return performances

    finally:
        await newton_client.close()
