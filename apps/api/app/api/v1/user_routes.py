from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.core.dependencies import get_current_user, require_roles
from app.core.security import get_password_hash, verify_password
from app.db.session import get_db
from app.db.models.user import User

router = APIRouter()


# ── Schemas ──
class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class UserListResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


# ── Routes ──

@router.get("/me")
async def get_my_profile(
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get current user's profile."""
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }


@router.patch("/me")
async def update_my_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """Update current user's profile (name or email)."""
    if request.email and request.email != current_user.email:
        # Check email not taken by another user
        existing = db.query(User).filter(
            User.email == request.email,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = request.email

    if request.full_name:
        current_user.full_name = request.full_name

    db.commit()
    db.refresh(current_user)

    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "message": "Profile updated successfully",
    }


@router.post("/me/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """Change the current user's password."""
    if not verify_password(request.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    if len(request.new_password) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters")

    current_user.hashed_password = get_password_hash(request.new_password)
    db.commit()

    return {"message": "Password changed successfully"}


@router.get("/")
async def list_users(
    role: Optional[str] = None,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
    db: Session = Depends(get_db),
) -> Any:
    """List users. Teachers see students; principals see everyone."""
    query = db.query(User)

    if current_user.role == "teacher":
        query = query.filter(User.role == "student")
    elif role:
        query = query.filter(User.role == role)

    users = query.all()
    return {
        "success": True,
        "data": [
            {
                "id": str(u.id),
                "email": u.email,
                "full_name": u.full_name,
                "role": u.role,
                "is_active": u.is_active,
            }
            for u in users
        ],
        "total": len(users),
    }


@router.patch("/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    current_user: User = Depends(require_roles(["principal"])),
    db: Session = Depends(get_db),
) -> Any:
    """Deactivate a user account (principals only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if str(user.id) == str(current_user.id):
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")

    user.is_active = False
    db.commit()

    return {"message": f"User {user.full_name} has been deactivated"}
