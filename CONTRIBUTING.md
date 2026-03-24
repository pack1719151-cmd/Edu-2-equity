# Contributing to EduEquity OS

Thank you for your interest in contributing to EduEquity OS! This document provides guidelines and instructions for contributing.

## 🤝 Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- pnpm 8+
- Git

### Development Setup

1. **Fork the repository**
   Click the "Fork" button on GitHub and clone your fork:

   ```bash
   git clone https://github.com/YOUR_USERNAME/eduequity-os.git
   cd eduequity-os
   ```

2. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/eduequity/eduequity-os.git
   ```

3. **Install dependencies**
   ```bash
   pnpm install
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

5. **Set up the database**
   ```bash
   # Create PostgreSQL database
   createdb eduequity

   # Run migrations
   pnpm db:migrate

   # Seed demo data (optional)
   pnpm db:seed
   ```

6. **Start development servers**
   ```bash
   pnpm dev
   ```

## 📝 Making Changes

### 1. Create a Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create a new branch
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

Follow the coding standards:
- **Frontend**: TypeScript, React, Tailwind CSS
- **Backend**: Python, FastAPI, SQLAlchemy
- **Commits**: Conventional commits format

### 3. Test Your Changes

```bash
# Run all tests
pnpm test

# Run specific tests
pnpm test --workspace=apps/web
pnpm test --workspace=apps/api
```

### 4. Lint and Format

```bash
# Format code
pnpm format

# Check linting
pnpm lint
```

### 5. Commit Your Changes

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git add .
git commit -m "feat: add new attendance tracking feature"
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Maintenance tasks

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📐 Project Structure

### Frontend (Next.js)

```
apps/web/src/
├── app/              # App Router pages
├── components/       # Reusable components
│   ├── ui/          # Shadcn/ui components
│   ├── layout/      # Layout components
│   └── ...
├── lib/             # Utilities
└── types/           # TypeScript types
```

### Backend (FastAPI)

```
apps/api/app/
├── core/            # Core functionality
│   ├── config.py   # Settings
│   ├── security.py # JWT, passwords
│   └── ...
├── api/             # API routes
├── schemas/         # Pydantic schemas
├── db/              # Database
│   ├── models/     # SQLAlchemy models
│   └── repositories/
└── modules/         # Business logic
```

## 🧪 Testing Guidelines

### Frontend Tests

- Use Vitest for unit tests
- Use React Testing Library for component tests
- Place tests alongside source files: `component.tsx` → `component.test.tsx`

### Backend Tests

- Use pytest for testing
- Use fixtures from `conftest.py`
- Follow naming: `test_<module>.py`

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions
- Update API documentation in `docs/api-docs.md`
- Add inline comments for complex logic

## 🐛 Bug Reports

1. Check if the bug has already been reported
2. Create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details

## 💡 Feature Requests

1. Check if the feature exists or is planned
2. Create an issue with:
   - Clear description
   - Use cases
   - Proposed solution
   - Alternatives considered

## 📖 Coding Standards

### TypeScript

```typescript
// Use TypeScript best practices
interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
}

// Prefer functional components with hooks
const UserCard: React.FC<Props> = ({ user }) => {
  return <div>{user.name}</div>;
};
```

### Python

```python
# Use type hints
from typing import Optional

async def get_user(user_id: str) -> Optional[User]:
    """Get a user by ID."""
    return await UserRepository.get(user_id)

# Follow PEP 8
class UserService:
    """Service for user operations."""
    
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
```

## 🏷️ Review Process

1. All PRs require at least one review
2. Ensure CI passes
3. Address review comments
4. Squash commits before merging

## 🙏 Thank You!

Your contributions help make EduEquity OS better for everyone.

