from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db, User, Session as DBSession
from schemas import LoginRequest, LoginResponse, AuthStatus
from services import AuthService, NewtonClient
from config import settings
import secrets
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


def get_session_from_header(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> DBSession:
    """Dependency to get session from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        session_id = authorization.replace("Bearer ", "")
        db_session = db.query(DBSession).filter(
            DBSession.session_id == session_id,
            DBSession.is_active == True
        ).first()

        if not db_session:
            raise HTTPException(status_code=401, detail="Invalid or expired session")

        # Check if session is expired
        if db_session.expires_at < datetime.utcnow():
            db_session.is_active = False
            db.commit()
            raise HTTPException(status_code=401, detail="Session expired")

        return db_session

    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with Google OAuth via Playwright
    """
    try:
        logger.info(f"Attempting login for {request.email}")

        # Use auth service to get cookies
        auth_service = AuthService(headless=True)
        cookies = await auth_service.authenticate_google(
            email=request.email,
            password=request.password
        )

        if not cookies:
            raise HTTPException(status_code=401, detail="Authentication failed")

        # Get user info from Newton API
        newton_client = NewtonClient(cookies)
        try:
            user_data = await newton_client.get_user_info()
        finally:
            await newton_client.close()

        # Create or update user
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            user = User(
                email=request.email,
                name=user_data.get("name", ""),
                newton_user_data=user_data
            )
            db.add(user)
        else:
            user.name = user_data.get("name", user.name)
            user.newton_user_data = user_data
            user.updated_at = datetime.utcnow()

        # Create session
        session_id = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=7)

        db_session = DBSession(
            session_id=session_id,
            user_email=request.email,
            cookies=cookies,
            is_active=True,
            expires_at=expires_at
        )
        db.add(db_session)
        db.commit()

        logger.info(f"Login successful for {request.email}")

        return LoginResponse(
            session_id=session_id,
            user=user_data
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/logout")
async def logout(
    db_session: DBSession = Depends(get_session_from_header),
    db: Session = Depends(get_db)
):
    """
    Logout user by invalidating session
    """
    db_session.is_active = False
    db.commit()

    return {"message": "Logout successful"}


@router.get("/status", response_model=AuthStatus)
async def get_status(
    db_session: DBSession = Depends(get_session_from_header),
    db: Session = Depends(get_db)
):
    """
    Get authentication status
    """
    user = db.query(User).filter(User.email == db_session.user_email).first()

    return AuthStatus(
        authenticated=True,
        user=user.newton_user_data if user else None
    )


@router.get("/user/me")
async def get_current_user(
    db_session: DBSession = Depends(get_session_from_header),
    db: Session = Depends(get_db)
):
    """
    Get current user information
    """
    # Get fresh user data from Newton API
    newton_client = NewtonClient(db_session.cookies)
    try:
        user_data = await newton_client.get_user_info()
        return user_data
    finally:
        await newton_client.close()
