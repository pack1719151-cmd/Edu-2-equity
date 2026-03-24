from fastapi import APIRouter

from app.api.v1.auth_routes import router as auth_router
from app.api.v1.dashboard_routes import router as dashboard_router
from app.api.v1.attendance_routes import router as attendance_router
from app.api.v1.quiz_routes import router as quiz_router
from app.api.v1.feed_routes import router as feed_router
from app.api.v1.user_routes import router as user_router

api_router = APIRouter()

# Health check
health_router = APIRouter()

@health_router.get("/health")
async def api_health_check():
    return {"status": "healthy", "api_version": "1.0.0"}

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])
api_router.include_router(quiz_router, prefix="/quizzes", tags=["Quizzes"])
api_router.include_router(feed_router, prefix="/feed", tags=["Feed & Approvals"])
