from typing import Any, List, Optional
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
quizzes: dict = {}
submissions: dict = {}


# ── Schemas ──
class QuestionCreate(BaseModel):
    text: str
    type: str  # "multiple_choice" | "true_false" | "short_answer"
    options: Optional[List[str]] = None
    correct_answer: str
    points: int = 10


class CreateQuizRequest(BaseModel):
    title: str
    description: Optional[str] = None
    course_name: str
    time_limit_minutes: int = 30
    passing_score: int = 60
    questions: List[QuestionCreate] = []


class UpdateQuizRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit_minutes: Optional[int] = None
    passing_score: Optional[int] = None
    status: Optional[str] = None


class SubmitQuizRequest(BaseModel):
    answers: List[dict]  # [{"question_id": "...", "answer": "..."}]


# ── Helpers ──
def _grade_submission(quiz: dict, answers: List[dict]) -> dict:
    answer_map = {a["question_id"]: a["answer"] for a in answers}
    total_points = 0
    earned_points = 0
    graded = []

    for q in quiz.get("questions", []):
        qid = q["id"]
        total_points += q["points"]
        given = answer_map.get(qid, "")
        correct = given.lower().strip() == q["correct_answer"].lower().strip()
        if correct:
            earned_points += q["points"]
        graded.append({
            "question_id": qid,
            "given_answer": given,
            "correct_answer": q["correct_answer"],
            "is_correct": correct,
            "points_earned": q["points"] if correct else 0,
        })

    score_pct = round((earned_points / total_points * 100) if total_points > 0 else 0, 1)
    passed = score_pct >= quiz.get("passing_score", 60)
    return {
        "total_points": total_points,
        "earned_points": earned_points,
        "score_percentage": score_pct,
        "passed": passed,
        "graded_answers": graded,
    }


# ── Routes ──

@router.get("/")
async def get_quizzes(
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get quizzes. Teachers see their own; students see published quizzes."""
    if current_user.role in ("teacher", "principal"):
        result = [q for q in quizzes.values() if q["teacher_id"] == str(current_user.id)]
    else:
        result = [q for q in quizzes.values() if q["status"] == "published"]

    if status_filter:
        result = [q for q in result if q["status"] == status_filter]

    return {"success": True, "data": result, "total": len(result)}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_quiz(
    request: CreateQuizRequest,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
) -> Any:
    """Create a new quiz."""
    quiz_id = str(uuid.uuid4())
    questions_with_ids = [
        {**q.model_dump(), "id": str(uuid.uuid4())}
        for q in request.questions
    ]

    quiz = {
        "id": quiz_id,
        "teacher_id": str(current_user.id),
        "teacher_name": current_user.full_name,
        "title": request.title,
        "description": request.description or "",
        "course_name": request.course_name,
        "time_limit_minutes": request.time_limit_minutes,
        "passing_score": request.passing_score,
        "questions": questions_with_ids,
        "status": "draft",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "submission_count": 0,
    }
    quizzes[quiz_id] = quiz

    return {"success": True, "data": quiz, "message": "Quiz created"}


@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get a specific quiz. Students only see questions without correct answers."""
    quiz = quizzes.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if current_user.role == "student":
        if quiz["status"] != "published":
            raise HTTPException(status_code=404, detail="Quiz not available")
        # Strip correct answers for students
        student_view = {**quiz}
        student_view["questions"] = [
            {k: v for k, v in q.items() if k != "correct_answer"}
            for q in quiz["questions"]
        ]
        return {"success": True, "data": student_view}

    return {"success": True, "data": quiz}


@router.patch("/{quiz_id}")
async def update_quiz(
    quiz_id: str,
    request: UpdateQuizRequest,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
) -> Any:
    """Update quiz metadata or status."""
    quiz = quizzes.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if quiz["teacher_id"] != str(current_user.id) and current_user.role != "principal":
        raise HTTPException(status_code=403, detail="Not authorized to edit this quiz")

    updates = request.model_dump(exclude_none=True)
    if updates:
        quiz.update(updates)
        quiz["updated_at"] = datetime.utcnow().isoformat()

    return {"success": True, "data": quiz, "message": "Quiz updated"}


@router.post("/{quiz_id}/publish")
async def publish_quiz(
    quiz_id: str,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
) -> Any:
    """Publish a quiz so students can take it."""
    quiz = quizzes.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if not quiz["questions"]:
        raise HTTPException(status_code=400, detail="Cannot publish a quiz with no questions")

    quiz["status"] = "published"
    quiz["published_at"] = datetime.utcnow().isoformat()
    return {"success": True, "data": quiz, "message": "Quiz published"}


@router.post("/{quiz_id}/questions")
async def add_question(
    quiz_id: str,
    question: QuestionCreate,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
) -> Any:
    """Add a question to an existing quiz."""
    quiz = quizzes.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    new_question = {**question.model_dump(), "id": str(uuid.uuid4())}
    quiz["questions"].append(new_question)
    quiz["updated_at"] = datetime.utcnow().isoformat()

    return {"success": True, "data": new_question, "message": "Question added"}


@router.post("/{quiz_id}/submit")
async def submit_quiz(
    quiz_id: str,
    request: SubmitQuizRequest,
    current_user: User = Depends(require_roles(["student"])),
) -> Any:
    """Student submits answers for a quiz."""
    quiz = quizzes.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if quiz["status"] != "published":
        raise HTTPException(status_code=400, detail="Quiz is not open for submissions")

    # Check already submitted
    already = any(
        s["student_id"] == str(current_user.id) and s["quiz_id"] == quiz_id
        for s in submissions.values()
    )
    if already:
        raise HTTPException(status_code=409, detail="Already submitted this quiz")

    result = _grade_submission(quiz, request.answers)
    submission_id = str(uuid.uuid4())
    submission = {
        "id": submission_id,
        "quiz_id": quiz_id,
        "student_id": str(current_user.id),
        "student_name": current_user.full_name,
        "submitted_at": datetime.utcnow().isoformat(),
        **result,
    }
    submissions[submission_id] = submission
    quiz["submission_count"] = quiz.get("submission_count", 0) + 1

    return {"success": True, "data": submission, "message": "Quiz submitted and graded"}


@router.get("/{quiz_id}/results")
async def get_results(
    quiz_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get quiz results. Students see their own; teachers see all."""
    quiz = quizzes.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if current_user.role == "student":
        my_submission = next(
            (s for s in submissions.values()
             if s["quiz_id"] == quiz_id and s["student_id"] == str(current_user.id)),
            None,
        )
        if not my_submission:
            raise HTTPException(status_code=404, detail="You haven't submitted this quiz yet")
        return {"success": True, "data": my_submission}

    # Teacher/principal: all submissions for this quiz
    quiz_submissions = [s for s in submissions.values() if s["quiz_id"] == quiz_id]
    scores = [s["score_percentage"] for s in quiz_submissions]
    avg = round(sum(scores) / len(scores), 1) if scores else 0

    return {
        "success": True,
        "data": {
            "quiz_id": quiz_id,
            "quiz_title": quiz["title"],
            "total_submissions": len(quiz_submissions),
            "average_score": avg,
            "pass_rate": round(
                sum(1 for s in quiz_submissions if s["passed"]) / len(quiz_submissions) * 100
                if quiz_submissions else 0, 1
            ),
            "submissions": quiz_submissions,
        },
    }


@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: str,
    current_user: User = Depends(require_roles(["teacher", "principal"])),
) -> Any:
    """Delete a quiz (only if draft)."""
    quiz = quizzes.get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if quiz["status"] == "published" and current_user.role != "principal":
        raise HTTPException(status_code=400, detail="Cannot delete a published quiz. Close it first.")

    del quizzes[quiz_id]
    return {"success": True, "message": "Quiz deleted"}
