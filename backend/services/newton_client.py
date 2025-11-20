import httpx
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta


class NewtonClient:
    BASE_URL = "https://my.newtonschool.co"

    def __init__(self, cookies: Dict[str, str]):
        self.client = httpx.AsyncClient(
            cookies=cookies,
            timeout=30.0,
            follow_redirects=True
        )

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    async def get_user_info(self) -> Dict[str, Any]:
        """GET /api/v1/user/me/"""
        response = await self.client.get(f"{self.BASE_URL}/api/v1/user/me/")
        response.raise_for_status()
        return response.json()

    async def get_courses(self) -> List[Dict[str, Any]]:
        """GET /api/v2/course/all/applied/"""
        response = await self.client.get(
            f"{self.BASE_URL}/api/v2/course/all/applied/",
            params={"pagination": "false", "completed": "false"}
        )
        response.raise_for_status()
        return response.json()

    async def get_course_details(self, course_hash: str) -> Dict[str, Any]:
        """GET /api/v2/course/h/{course_hash}/"""
        response = await self.client.get(
            f"{self.BASE_URL}/api/v2/course/h/{course_hash}/"
        )
        response.raise_for_status()
        return response.json()

    async def get_assignments(
        self,
        course_hash: str,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """GET /api/v2/course/h/{course_hash}/assignment/all/"""
        response = await self.client.get(
            f"{self.BASE_URL}/api/v2/course/h/{course_hash}/assignment/all/",
            params={"limit": limit, "offset": offset}
        )
        response.raise_for_status()
        return response.json()

    async def get_assignment_details(
        self,
        course_hash: str,
        assignment_hash: str
    ) -> Dict[str, Any]:
        """GET /api/v2/course/h/{course_hash}/assignment/h/{assignment_hash}/"""
        response = await self.client.get(
            f"{self.BASE_URL}/api/v2/course/h/{course_hash}/assignment/h/{assignment_hash}/"
        )
        response.raise_for_status()
        return response.json()

    async def get_assessment_questions(
        self,
        course_hash: str,
        assessment_hash: str
    ) -> Dict[str, Any]:
        """GET /api/v1/course/h/{course_hash}/assessment/h/{assessment_hash}/"""
        response = await self.client.get(
            f"{self.BASE_URL}/api/v1/course/h/{course_hash}/assessment/h/{assessment_hash}/"
        )
        response.raise_for_status()
        return response.json()

    async def get_schedule(
        self,
        course_hash: str,
        start_ts: int,
        end_ts: int
    ) -> List[Dict[str, Any]]:
        """GET /api/v2/course/h/{course_hash}/lecture_slot/all/"""
        response = await self.client.get(
            f"{self.BASE_URL}/api/v2/course/h/{course_hash}/lecture_slot/all/",
            params={
                "pagination": "false",
                "start_timestamp": start_ts,
                "end_timestamp": end_ts
            }
        )
        response.raise_for_status()
        return response.json()

    async def get_today_schedule(self, course_hash: str) -> List[Dict[str, Any]]:
        """Get today's schedule"""
        now = datetime.now()
        start = datetime(now.year, now.month, now.day, 0, 0, 0)
        end = start + timedelta(days=1)

        start_ts = int(start.timestamp())
        end_ts = int(end.timestamp())

        return await self.get_schedule(course_hash, start_ts, end_ts)

    async def get_week_schedule(
        self,
        course_hash: str,
        start_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get week's schedule"""
        if not start_date:
            start_date = datetime.now()

        start = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
        end = start + timedelta(days=7)

        start_ts = int(start.timestamp())
        end_ts = int(end.timestamp())

        return await self.get_schedule(course_hash, start_ts, end_ts)

    async def submit_mcq(
        self,
        course_hash: str,
        assessment_hash: str,
        question_hash: str,
        answer: str
    ) -> Dict[str, Any]:
        """POST /api/v1/course/h/{course}/assessment/h/{assessment}/question/h/{question}/attempt/"""
        response = await self.client.post(
            f"{self.BASE_URL}/api/v1/course/h/{course_hash}/assessment/h/{assessment_hash}/question/h/{question_hash}/attempt/",
            json={"hash": question_hash, "value": answer}
        )
        response.raise_for_status()
        return response.json()

    async def get_coding_playground(
        self,
        course_hash: str,
        playground_hash: str
    ) -> Dict[str, Any]:
        """GET /api/v1/course/h/{course_hash}/playground/coding/h/{playground_hash}/"""
        response = await self.client.get(
            f"{self.BASE_URL}/api/v1/course/h/{course_hash}/playground/coding/h/{playground_hash}/"
        )
        response.raise_for_status()
        return response.json()

    async def submit_coding(
        self,
        course_hash: str,
        playground_hash: str,
        code: str,
        language_id: int = 71  # Python 3
    ) -> Dict[str, Any]:
        """PATCH /api/v1/course/h/{course_hash}/playground/coding/h/{playground_hash}/"""
        response = await self.client.patch(
            f"{self.BASE_URL}/api/v1/course/h/{course_hash}/playground/coding/h/{playground_hash}/",
            params={"run_hidden_test_cases": "true"},
            json={
                "hash": playground_hash,
                "source_code": code,
                "language_id": language_id,
                "standard_input": None,
                "run_hidden_test": True
            }
        )
        response.raise_for_status()
        return response.json()

    async def get_frontend_playground(
        self,
        course_hash: str,
        playground_hash: str
    ) -> Dict[str, Any]:
        """GET /api/v1/course/h/{course_hash}/playground/front_end/h/{playground_hash}/"""
        response = await self.client.get(
            f"{self.BASE_URL}/api/v1/course/h/{course_hash}/playground/front_end/h/{playground_hash}/"
        )
        response.raise_for_status()
        return response.json()

    async def submit_frontend(
        self,
        course_hash: str,
        playground_hash: str,
        html: str,
        css: str,
        js: str = ""
    ) -> Dict[str, Any]:
        """PATCH /api/v1/course/h/{course_hash}/playground/front_end/h/{playground_hash}/"""
        response = await self.client.patch(
            f"{self.BASE_URL}/api/v1/course/h/{course_hash}/playground/front_end/h/{playground_hash}/",
            params={"create_and_run_build": "true"},
            json={
                "hash": playground_hash,
                "html": html,
                "css": css,
                "javascript": js,
                "createAndRunBuild": True
            }
        )
        response.raise_for_status()
        return response.json()

    async def get_performance_overview(self, course_hash: str) -> Dict[str, Any]:
        """GET /api/v2/course/h/{course_hash}/user/performance/"""
        response = await self.client.get(
            f"{self.BASE_URL}/api/v2/course/h/{course_hash}/user/performance/"
        )
        response.raise_for_status()
        return response.json()
