from typing import Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.core.dependencies import get_current_user, require_roles
from app.db.session import get_db
from app.db.models.user import User

router = APIRouter()

# ── In-memory store ──
requests_store: dict = {}

VALID_TYPES = {"leave", "accommodation", "appeal", "resource", "other"}


# ── Schemas ──
class SubmitRequestSchema(BaseModel):
    type: str  # leave | accommodation | appeal | resource | other
    title: str
    description: str
    related_id: Optional[str] = None  # e.g. course_id or quiz_id


class ReviewRequestSchema(BaseModel):
    comment: Optional[str] = None


# ── Routes ──

@router.get("/pending")
async def get_pending_approvals(
    type_filter: Optional[str] = None,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
) -> Any:
    """Get all pending requests for review (teachers/principals only)."""
    pending = [r for r in requests_store.values() if r["status"] == "pending"]
    if type_filter:
        pending = [r for r in pending if r["type"] == type_filter]
    return {"success": True, "data": pending, "total": len(pending)}


@router.get("/my-requests")
async def get_my_requests(
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get all requests submitted by the current user."""
    my = [r for r in requests_store.values() if r["submitted_by_id"] == str(current_user.id)]
    if status_filter:
        my = [r for r in my if r["status"] == status_filter]
    return {"success": True, "data": my, "total": len(my)}


@router.post("/submit", status_code=status.HTTP_201_CREATED)
async def submit_request(
    request: SubmitRequestSchema,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Submit a new approval request."""
    if request.type not in VALID_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Type must be one of: {sorted(VALID_TYPES)}"
        )

    req_id = str(uuid.uuid4())
    new_request = {
        "id": req_id,
        "type": request.type,
        "title": request.title,
        "description": request.description,
        "related_id": request.related_id,
        "status": "pending",
        "submitted_by_id": str(current_user.id),
        "submitted_by_name": current_user.full_name,
        "submitted_by_role": current_user.role,
        "submitted_at": datetime.utcnow().isoformat(),
        "reviewed_by_id": None,
        "reviewed_by_name": None,
        "reviewed_at": None,
        "comment": None,
    }
    requests_store[req_id] = new_request

    return {"success": True, "data": new_request, "message": "Request submitted"}


@router.get("/{request_id}")
async def get_request(
    request_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get a specific request."""
    req = requests_store.get(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    # Students can only see their own
    if current_user.role == "student" and req["submitted_by_id"] != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")

    return {"success": True, "data": req}


@router.post("/approve/{request_id}")
async def approve_request(
    request_id: str,
    body: ReviewRequestSchema,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
) -> Any:
    """Approve a pending request."""
    req = requests_store.get(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    if req["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Request is already {req['status']}")

    req.update({
        "status": "approved",
        "reviewed_by_id": str(current_user.id),
        "reviewed_by_name": current_user.full_name,
        "reviewed_at": datetime.utcnow().isoformat(),
        "comment": body.comment,
    })

    return {"success": True, "data": req, "message": "Request approved"}


@router.post("/reject/{request_id}")
async def reject_request(
    request_id: str,
    body: ReviewRequestSchema,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
) -> Any:
    """Reject a pending request."""
    req = requests_store.get(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    if req["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Request is already {req['status']}")

    req.update({
        "status": "rejected",
        "reviewed_by_id": str(current_user.id),
        "reviewed_by_name": current_user.full_name,
        "reviewed_at": datetime.utcnow().isoformat(),
        "comment": body.comment,
    })

    return {"success": True, "data": req, "message": "Request rejected"}
