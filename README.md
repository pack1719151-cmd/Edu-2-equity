# EduEquity OS

<div align="center">

![EduEquity OS Logo](docs/screenshots/logo-placeholder.png)

**An educational equity platform with attendance tracking, quiz management, and approval workflows**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009166.svg)](https://fastapi.tiangolo.com/)

</div>

## 🎯 Overview

EduEquity OS is a comprehensive educational platform designed to promote equity in education through:
- **Smart Attendance Tracking** - QR code based attendance with real-time analytics
- **Quiz Management** - Create and manage quizzes with instant feedback
- **Approval Workflows** - Streamlined approval processes for students and teachers
- **Role-Based Dashboards** - Personalized dashboards for students, teachers, and principals
- **Learning Gap Alerts** - AI-powered insights to identify and address learning gaps

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        EduEquity OS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────────────┐    ┌─────────────────┐                    │
│   │   Next.js 14    │    │   FastAPI       │                    │
│   │   Frontend      │◄──►│   Backend       │                    │
│   │   (React)       │    │   (Python)      │                    │
│   └─────────────────┘    └─────────────────┘                    │
│           │                       │                              │
│           │                       │                              │
│   ┌───────▼───────┐      ┌───────▼───────┐                     │
│   │  PostgreSQL   │      │    Redis      │                     │
│   │  (Database)   │      │  (Sessions)   │                     │
│   └───────────────┘      └───────────────┘                     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- pnpm 8+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/eduequity/eduequity-os.git
   cd eduequity-os
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start the development servers**
   ```bash
   pnpm dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Docker Setup

```bash
docker-compose up -d
```

## 📁 Project Structure

```
eduequity-os/
├── apps/
│   ├── web/                    # Next.js 14 Frontend
│   │   ├── src/
│   │   │   ├── app/           # App Router
│   │   │   ├── components/    # Reusable components
│   │   │   ├── lib/           # Utilities
│   │   │   └── types/         # TypeScript types
│   │   └── ...
│   │
│   └── api/                    # FastAPI Backend
│       ├── app/
│       │   ├── core/          # Core functionality
│       │   ├── api/           # API routes
│       │   ├── schemas/       # Pydantic schemas
│       │   ├── db/            # Database
│       │   └── modules/       # Business logic
│       └── ...
│
├── packages/                   # Shared packages
│   ├── shared-types/          # Shared TypeScript types
│   └── shared-config/         # Shared configs
│
├── infra/                      # Infrastructure
│   ├── docker-compose.yml
│   └── nginx/
│
├── docs/                       # Documentation
├── scripts/                    # Utility scripts
└── ...
```

## 🎨 Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **UI Components**: Shadcn/ui + Tailwind CSS
- **State Management**: React Query + Zustand
- **Authentication**: JWT (HttpOnly cookies)
- **Language**: TypeScript

### Backend
- **Framework**: FastAPI
- **Database**: SQLAlchemy 2.0 + PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT with http-only cookies
- **Caching**: Redis
- **Language**: Python 3.10+

### DevOps
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **CI/CD**: GitHub Actions

## 📖 Documentation

- [Architecture](docs/architecture.md)
- [API Documentation](docs/api-docs.md)
- [Setup Guide](docs/setup-guide.md)
- [Demo Script](docs/demo-script.md)

## 🎯 Features

### For Students
- View attendance records
- Take quizzes and view results
- Submit approval requests
- Track learning progress

### For Teachers
- Create and manage quizzes
- Mark attendance with QR codes
- Review and approve student requests
- Monitor class performance

### For Principals
- School-wide analytics dashboard
- Learning gap identification
- Attendance trend analysis
- Resource allocation insights

## 🧪 Testing

```bash
# Run all tests
pnpm test

# Run frontend tests
pnpm test --workspace=apps/web

# Run backend tests
pnpm test --workspace=apps/api
```

## 📦 Deployment

### Production Build

```bash
# Build all applications
pnpm build

# Start production servers
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables

Make sure to set the following environment variables in production:
- `APP_ENV=production`
- `APP_DEBUG=false`
- Strong `JWT_SECRET_KEY`
- Secure `DATABASE_URL`
- Proper `CORS_ORIGINS`

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Shadcn/ui](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)

