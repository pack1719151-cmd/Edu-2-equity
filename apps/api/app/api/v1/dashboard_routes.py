from typing import Any

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user

router = APIRouter()


@router.get("/student")
async def student_dashboard(current_user=Depends(get_current_user)) -> Any:
    """Return dashboard data for a student (development/demo data)."""
    # Demo metrics - in a full implementation these would be calculated
    # from quizzes, attendance and assignments tables
    data = {
        "attendance_rate": 85,
        "quizzes_completed": 12,
        "average_score": 78,
        "learning_streak_days": 7,
        "recent_activity": [
            {"title": "Mathematics Quiz", "description": "Completed with 85%", "timestamp": "2 hours ago"},
            {"title": "Science Attendance", "description": "Marked present", "timestamp": "Yesterday"},
            {"title": "English Assignment", "description": "Submitted", "timestamp": "2 days ago"},
        ],
    }
    return data


@router.get("/teacher")
async def teacher_dashboard(current_user=Depends(get_current_user)) -> Any:
    """Return dashboard data for a teacher (development/demo data)."""
    data = {
        "active_classes": 4,
        "total_students": 120,
        "active_quizzes": 8,
        "avg_attendance": 92,
        "today_schedule": [
            {"class": "Mathematics - Grade 10", "time": "9:00 AM - 10:00 AM", "room": "101"},
        ],
    }
    return data


@router.get("/principal")
async def principal_dashboard(current_user=Depends(get_current_user)) -> Any:
    """Return dashboard data for a principal (development/demo data)."""
    data = {
        "total_students": 1250,
        "teaching_staff": 45,
        "avg_attendance": 94,
        "pending_approvals": 8,
    }
    return data
