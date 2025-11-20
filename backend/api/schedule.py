from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Session as DBSession
from api.auth import get_session_from_header
from services import NewtonClient
from schemas import ClassSession, JoinClassRequest, JoinClassResponse
from typing import List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/today", response_model=List[ClassSession])
async def get_today_schedule(
    db_session: DBSession = Depends(get_session_from_header)
):
    """
    Get today's class schedule
    """
    newton_client = NewtonClient(db_session.cookies)

    try:
        # Get courses
        courses = await newton_client.get_courses()

        all_classes = []
        for course in courses:
            course_hash = course.get("hash")
            if not course_hash:
                continue

            try:
                # Get today's schedule for this course
                schedule = await newton_client.get_today_schedule(course_hash)

                for slot in schedule:
                    class_session = ClassSession(
                        hash=slot.get("hash", ""),
                        time=datetime.fromtimestamp(slot.get("start_timestamp", 0)).strftime("%H:%M"),
                        subject=slot.get("lecture", {}).get("name", "Unknown"),
                        room=slot.get("room", {}).get("name"),
                        join_url=slot.get("join_url"),
                        instructor=slot.get("instructor", {}).get("name"),
                        start_timestamp=slot.get("start_timestamp", 0),
                        end_timestamp=slot.get("end_timestamp", 0)
                    )
                    all_classes.append(class_session)

            except Exception as e:
                logger.error(f"Error fetching schedule for course {course_hash}: {str(e)}")
                continue

        # Sort by start time
        all_classes.sort(key=lambda x: x.start_timestamp)

        return all_classes

    finally:
        await newton_client.close()


@router.get("/week", response_model=List[ClassSession])
async def get_week_schedule(
    start_date: Optional[str] = Query(None),
    db_session: DBSession = Depends(get_session_from_header)
):
    """
    Get week's class schedule
    """
    newton_client = NewtonClient(db_session.cookies)

    try:
        # Parse start date
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        else:
            start_dt = datetime.now()

        # Get courses
        courses = await newton_client.get_courses()

        all_classes = []
        for course in courses:
            course_hash = course.get("hash")
            if not course_hash:
                continue

            try:
                # Get week's schedule for this course
                schedule = await newton_client.get_week_schedule(course_hash, start_dt)

                for slot in schedule:
                    class_session = ClassSession(
                        hash=slot.get("hash", ""),
                        time=datetime.fromtimestamp(slot.get("start_timestamp", 0)).strftime("%Y-%m-%d %H:%M"),
                        subject=slot.get("lecture", {}).get("name", "Unknown"),
                        room=slot.get("room", {}).get("name"),
                        join_url=slot.get("join_url"),
                        instructor=slot.get("instructor", {}).get("name"),
                        start_timestamp=slot.get("start_timestamp", 0),
                        end_timestamp=slot.get("end_timestamp", 0)
                    )
                    all_classes.append(class_session)

            except Exception as e:
                logger.error(f"Error fetching week schedule for course {course_hash}: {str(e)}")
                continue

        # Sort by start time
        all_classes.sort(key=lambda x: x.start_timestamp)

        return all_classes

    finally:
        await newton_client.close()


@router.post("/join-class", response_model=JoinClassResponse)
async def join_class(
    request: JoinClassRequest,
    db_session: DBSession = Depends(get_session_from_header)
):
    """
    Join a class (opens the join URL)
    """
    newton_client = NewtonClient(db_session.cookies)

    try:
        # Get all courses to find the lecture slot
        courses = await newton_client.get_courses()

        for course in courses:
            course_hash = course.get("hash")
            if not course_hash:
                continue

            try:
                # Get schedule to find the slot
                now = datetime.now()
                start = now - timedelta(hours=2)
                end = now + timedelta(hours=12)

                schedule = await newton_client.get_schedule(
                    course_hash,
                    int(start.timestamp()),
                    int(end.timestamp())
                )

                for slot in schedule:
                    if slot.get("hash") == request.lecture_slot_hash:
                        join_url = slot.get("join_url")
                        if join_url:
                            return JoinClassResponse(
                                join_url=join_url,
                                status="opened"
                            )

            except Exception as e:
                logger.error(f"Error searching for slot in course {course_hash}: {str(e)}")
                continue

        raise HTTPException(status_code=404, detail="Lecture slot not found")

    finally:
        await newton_client.close()
