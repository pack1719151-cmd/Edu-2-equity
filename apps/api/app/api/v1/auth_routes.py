from datetime import timedelta
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password, get_password_hash, decode_access_token
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
    RefreshTokenRequest,
    UserMeResponse,
)
from app.core.dependencies import get_current_user

router = APIRouter()


@router.get("/health")
async def auth_health_check():
    """Health check endpoint for auth routes"""
    return {"status": "healthy", "auth_version": "1.0.0"}


@router.post("/register", response_model=UserResponse)
def register(
    *,
    db: Session = Depends(get_db),
    request: RegisterRequest
) -> Any:
    """
    Register a new user.
    """
    # Check if user already exists
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    # Create new user
    user = User(
        email=request.email,
        hashed_password=get_password_hash(request.password),
        full_name=request.full_name,
        role=request.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    *,
    db: Session = Depends(get_db),
    response: Response,
    request: LoginRequest
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    Sets both access token and refresh token as httpOnly cookies.
    """
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is disabled",
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires,
        data={"role": user.role}
    )

    # Create refresh token
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_access_token(
        subject=str(user.id),
        expires_delta=refresh_token_expires,
        data={"type": "refresh"}
    )

    is_production = settings.APP_ENV == "production"

    # Set access token cookie
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=is_production,
        samesite="lax",
    )

    # Set refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        secure=is_production,
        samesite="lax",
    )

    # Set user_role cookie (not httpOnly, accessible to JS for redirects)
    response.set_cookie(
        key="user_role",
        value=user.role,
        httponly=False,  # Not httpOnly so JS can read it for redirects
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=is_production,
        samesite="lax",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(response: Response) -> Any:
    """
    Logout user by clearing all auth cookies.
    """
    # Clear access token cookie
    response.delete_cookie(
        key=settings.COOKIE_NAME,
        httponly=True,
        secure=False,
        samesite="lax",
    )

    # Clear refresh token cookie
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="lax",
    )

    # Clear user_role cookie
    response.delete_cookie(
        key="user_role",
        httponly=False,
        secure=False,
        samesite="lax",
    )

    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    *,
    request: Request,
    response: Response,
    refresh_request: Optional[RefreshTokenRequest] = None,
    db: Session = Depends(get_db)
) -> Any:
    """
    Refresh access token using refresh token from cookie or JSON body.
    """
    # Try to get refresh token from cookie first, then from JSON body
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token and refresh_request:
        refresh_token = refresh_request.refresh_token
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found in cookie or body",
        )

    try:
        payload = decode_access_token(refresh_token)
        token_type = payload.get("type")
        
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is disabled",
        )

    # Create new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires,
        data={"role": user.role}
    )

    # Create new refresh token
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    new_refresh_token = create_access_token(
        subject=str(user.id),
        expires_delta=refresh_token_expires,
        data={"type": "refresh"}
    )

    # Set new access token cookie
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=False,
        samesite="lax",
    )

    # Set new refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        secure=False,
        samesite="lax",
    )

    # Update user_role cookie
    response.set_cookie(
        key="user_role",
        value=user.role,
        httponly=False,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=False,
        samesite="lax",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserMeResponse)
def read_users_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "role": current_user.role,
    }

