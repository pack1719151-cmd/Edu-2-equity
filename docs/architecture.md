# EduEquity OS Architecture

## Overview

EduEquity OS is a full-stack educational platform built with a modern tech stack:

- **Frontend**: Next.js 14 with App Router, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI (Python) with SQLAlchemy, JWT authentication
- **Database**: PostgreSQL
- **Monorepo**: pnpm workspaces

## Project Structure

```
eduequity-os/
├── apps/
│   ├── web/              # Next.js frontend application
│   └── api/              # FastAPI backend application
├── packages/
│   ├── shared-types/     # Shared TypeScript types
│   └── shared-config/    # Shared ESLint/TS/Tailwind configs
├── infra/                # Docker and deployment configs
├── scripts/              # Development and setup scripts
└── docs/                 # Documentation
```

## Frontend Architecture

### App Router Structure

```
apps/web/src/app/
├── (auth)/              # Route group for authentication
│   ├── login/
│   └── register/
├── dashboard/           # Protected dashboard routes
│   ├── student/
│   ├── teacher/
│   └── principal/
├── api/v1/[...route]/   # API proxy route
├── layout.tsx           # Root layout
└── page.tsx             # Home page
```

### Component Structure

```
apps/web/src/components/
├── ui/                  # shadcn/ui base components
├── layout/              # Layout components (Sidebar, Header)
├── attendance/          # Attendance-related components
└── dashboard/           # Dashboard-specific components
```

## Backend Architecture

### FastAPI Structure

```
apps/api/app/
├── main.py              # FastAPI app entry point
├── core/                # Core configurations
│   ├── config.py
│   ├── security.py
│   ├── dependencies.py
│   └── middleware.py
├── api/v1/              # API routes
│   ├── auth_routes.py
│   ├── user_routes.py
│   ├── attendance_routes.py
│   └── quiz_routes.py
├── db/                  # Database layer
│   ├── models/
│   ├── repositories/
│   └── session.py
├── schemas/             # Pydantic schemas
└── modules/             # Business logic
    ├── auth/
    ├── users/
    └── attendance/
```

## Authentication Flow

1. User submits credentials to `/api/v1/auth/login`
2. Backend validates and returns JWT in httpOnly cookie
3. Frontend stores role in accessible cookie for routing
4. Subsequent requests include cookies automatically
5. API proxy forwards cookies to backend

## API Routes

### Authentication (`/api/v1/auth`)
- `POST /register` - Register new user
- `POST /login` - Login and get tokens
- `POST /logout` - Clear cookies
- `POST /refresh` - Refresh access token
- `GET /me` - Get current user

### Attendance (`/api/v1/attendance`)
- `GET /sessions` - List sessions
- `POST /sessions` - Create session
- `GET /sessions/:id/qr` - Get QR code
- `POST /sessions/:id/mark` - Mark attendance

### Quizzes (`/api/v1/quizzes`)
- `GET /` - List quizzes
- `POST /` - Create quiz
- `POST /:id/submit` - Submit answers

## Environment Variables

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (`.env`)
```env
DATABASE_URL=postgresql://...
SECRET_KEY=...
JWT_SECRET_KEY=...
```

## Development Workflow

1. Frontend runs on `http://localhost:3000`
2. Backend runs on `http://localhost:8000`
3. API proxy in Next.js forwards `/api/v1/*` to backend
4. Hot reload enabled for both frontend and backend

## Production Deployment

- Frontend: Deployed to Vercel or similar
- Backend: Docker container on cloud provider
- Database: Managed PostgreSQL service
- Nginx: Reverse proxy for production

