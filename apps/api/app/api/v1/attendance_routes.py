from typing import Any, List, Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.core.dependencies import get_current_user, require_roles
from app.db.session import get_db
from app.db.models.user import User

router = APIRouter()

# ── In-memory store (replace with DB tables via Alembic in production) ──
attendance_sessions: dict = {}
attendance_records: dict = {}


# ── Schemas ──
class CreateSessionRequest(BaseModel):
    course_name: str
    date: str  # ISO date string e.g. "2026-03-25"
    time: str  # e.g. "09:00 AM"
    room: str
    duration_minutes: int = 60


class MarkAttendanceRequest(BaseModel):
    student_id: str
    status: str  # "present" | "absent" | "late" | "excused"


class AttendanceSession(BaseModel):
    id: str
    teacher_id: str
    course_name: str
    date: str
    time: str
    room: str
    duration_minutes: int
    qr_code: str
    created_at: str
    records: List[dict] = []


# ── Routes ──

@router.get("/sessions")
async def get_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """Get all attendance sessions. Teachers see their own; students see sessions for their classes."""
    if current_user.role == "teacher":
        sessions = [s for s in attendance_sessions.values() if s["teacher_id"] == str(current_user.id)]
    else:
        sessions = list(attendance_sessions.values())
    return {"success": True, "data": sessions, "total": len(sessions)}


@router.post("/sessions", status_code=status.HTTP_201_CREATED)
async def create_session(
    request: CreateSessionRequest,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
    db: Session = Depends(get_db),
) -> Any:
    """Create a new attendance session (teachers/principals only)."""
    session_id = str(uuid.uuid4())
    qr_token = str(uuid.uuid4())[:8].upper()

    session = {
        "id": session_id,
        "teacher_id": str(current_user.id),
        "teacher_name": current_user.full_name,
        "course_name": request.course_name,
        "date": request.date,
        "time": request.time,
        "room": request.room,
        "duration_minutes": request.duration_minutes,
        "qr_code": qr_token,
        "qr_url": f"/api/v1/attendance/checkin/{qr_token}",
        "created_at": datetime.utcnow().isoformat(),
        "records": [],
        "status": "active",
    }
    attendance_sessions[session_id] = session

    return {"success": True, "data": session, "message": "Session created"}


@router.get("/sessions/{session_id}")
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get a specific attendance session with all records."""
    session = attendance_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True, "data": session}


@router.get("/sessions/{session_id}/qr")
async def get_qr_code(
    session_id: str,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
) -> Any:
    """Get QR code token for a session."""
    session = attendance_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "success": True,
        "qr_code": session["qr_code"],
        "qr_url": session["qr_url"],
        "session_id": session_id,
    }


@router.post("/checkin/{qr_token}")
async def checkin_via_qr(
    qr_token: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Student checks in using a QR code token."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can check in")

    session = next(
        (s for s in attendance_sessions.values() if s["qr_code"] == qr_token),
        None,
    )
    if not session:
        raise HTTPException(status_code=404, detail="Invalid or expired QR code")

    # Check already checked in
    already = any(r["student_id"] == str(current_user.id) for r in session["records"])
    if already:
        raise HTTPException(status_code=409, detail="Already checked in to this session")

    record = {
        "id": str(uuid.uuid4()),
        "student_id": str(current_user.id),
        "student_name": current_user.full_name,
        "status": "present",
        "checked_in_at": datetime.utcnow().isoformat(),
    }
    session["records"].append(record)

    return {"success": True, "message": "Checked in successfully", "record": record}


@router.post("/sessions/{session_id}/mark")
async def mark_attendance(
    session_id: str,
    request: MarkAttendanceRequest,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
) -> Any:
    """Teacher manually marks attendance for a student."""
    session = attendance_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    valid_statuses = {"present", "absent", "late", "excused"}
    if request.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {valid_statuses}")

    # Update if exists, else add
    existing = next((r for r in session["records"] if r["student_id"] == request.student_id), None)
    if existing:
        existing["status"] = request.status
        existing["updated_at"] = datetime.utcnow().isoformat()
        record = existing
    else:
        record = {
            "id": str(uuid.uuid4()),
            "student_id": request.student_id,
            "status": request.status,
            "marked_by": str(current_user.id),
            "marked_at": datetime.utcnow().isoformat(),
        }
        session["records"].append(record)

    return {"success": True, "data": record}


@router.get("/my")
async def get_my_attendance(
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get attendance records for the current student."""
    records = []
    for session in attendance_sessions.values():
        student_record = next(
            (r for r in session["records"] if r["student_id"] == str(current_user.id)),
            None,
        )
        records.append({
            "session_id": session["id"],
            "course_name": session["course_name"],
            "date": session["date"],
            "time": session["time"],
            "status": student_record["status"] if student_record else "absent",
        })

    total = len(records)
    present = sum(1 for r in records if r["status"] == "present")
    rate = round((present / total * 100) if total > 0 else 0, 1)

    return {
        "success": True,
        "data": records,
        "stats": {
            "total_sessions": total,
            "present": present,
            "absent": total - present,
            "attendance_rate": rate,
        },
    }


@router.get("/stats")
async def get_attendance_stats(
    current_user: User = Depends(require_roles(["teacher", "principal"])),
) -> Any:
    """Get attendance statistics (teachers/principals)."""
    sessions = [s for s in attendance_sessions.values() if s["teacher_id"] == str(current_user.id)]
    total_records = sum(len(s["records"]) for s in sessions)
    present_records = sum(
        sum(1 for r in s["records"] if r["status"] == "present") for s in sessions
    )
    rate = round((present_records / total_records * 100) if total_records > 0 else 0, 1)
    return {
        "success": True,
        "data": {
            "total_sessions": len(sessions),
            "total_records": total_records,
            "present": present_records,
            "overall_attendance_rate": rate,
        },
    }
