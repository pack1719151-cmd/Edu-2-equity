# EduEquity OS — Setup Guide

## Quick Start (Development)

### 1. Backend (FastAPI)
```bash
cd apps/api
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend runs on http://localhost:8000  
API docs available at http://localhost:8000/docs

### 2. Frontend (Next.js)
```bash
cd apps/web
npm install
npm run dev
```
The frontend runs on http://localhost:3000

### 3. Express Server (Quiz/Analytics)
```bash
cd apps/express-server
npm install
npm run dev
```
Runs on http://localhost:3001

---

## Environment Variables

### Backend: `apps/api/.env`
```
APP_ENV=development
JWT_SECRET_KEY=<your-random-secret>
SECRET_KEY=<your-random-secret>
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/eduequity
```
In development, SQLite is used automatically (no PostgreSQL needed).

### Frontend: `apps/web/.env.local`
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## API Endpoints Summary

### Auth
- `POST /api/v1/auth/register` — Create account
- `POST /api/v1/auth/login` — Login (sets cookies)
- `POST /api/v1/auth/logout` — Clear session
- `POST /api/v1/auth/refresh` — Refresh access token
- `GET  /api/v1/auth/me` — Get current user

### Users
- `GET    /api/v1/users/me` — Get my profile
- `PATCH  /api/v1/users/me` — Update profile
- `POST   /api/v1/users/me/change-password` — Change password
- `GET    /api/v1/users/` — List users (teacher/principal)
- `PATCH  /api/v1/users/{id}/deactivate` — Deactivate user (principal)

### Dashboard
- `GET /api/v1/dashboard/student`
- `GET /api/v1/dashboard/teacher`
- `GET /api/v1/dashboard/principal`

### Attendance
- `GET    /api/v1/attendance/sessions` — List sessions
- `POST   /api/v1/attendance/sessions` — Create session
- `GET    /api/v1/attendance/sessions/{id}` — Get session
- `GET    /api/v1/attendance/sessions/{id}/qr` — Get QR code
- `POST   /api/v1/attendance/checkin/{qr_token}` — Student QR check-in
- `POST   /api/v1/attendance/sessions/{id}/mark` — Manual mark
- `GET    /api/v1/attendance/my` — My attendance records
- `GET    /api/v1/attendance/stats` — Stats (teacher)

### Quizzes
- `GET    /api/v1/quizzes/` — List quizzes
- `POST   /api/v1/quizzes/` — Create quiz
- `GET    /api/v1/quizzes/{id}` — Get quiz
- `PATCH  /api/v1/quizzes/{id}` — Update quiz
- `POST   /api/v1/quizzes/{id}/publish` — Publish quiz
- `POST   /api/v1/quizzes/{id}/questions` — Add question
- `POST   /api/v1/quizzes/{id}/submit` — Submit answers
- `GET    /api/v1/quizzes/{id}/results` — Get results
- `DELETE /api/v1/quizzes/{id}` — Delete quiz

### Feed & Approvals
- `GET  /api/v1/feed/pending` — Pending approvals (teacher/principal)
- `GET  /api/v1/feed/my-requests` — My submitted requests
- `POST /api/v1/feed/submit` — Submit new request
- `GET  /api/v1/feed/{id}` — Get request details
- `POST /api/v1/feed/approve/{id}` — Approve request
- `POST /api/v1/feed/reject/{id}` — Reject request

---

## Database Migrations (Alembic)
```bash
cd apps/api
# Create a new migration
alembic revision --autogenerate -m "description"
# Apply migrations
alembic upgrade head
# Rollback one step
alembic downgrade -1
```

---

## Security Notes
- Passwords hashed with bcrypt (passlib)
- JWT tokens stored in httpOnly cookies
- Role-based access enforced on every protected route
- `secure=True` cookies automatically enabled in production
- Never commit `.env` files with real secrets
