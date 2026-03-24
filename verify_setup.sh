#!/bin/bash

echo "🔍 Verifying EduEquity-OS setup..."

# Check directory structure
echo "📁 Checking directory structure..."
if [ ! -d "apps/web" ]; then
    echo "❌ apps/web directory missing"
    exit 1
fi

if [ ! -d "apps/api" ]; then
    echo "❌ apps/api directory missing"
    exit 1
fi

if [ ! -d "packages/shared-types" ]; then
    echo "❌ packages/shared-types directory missing"
    exit 1
fi

echo "✅ Directory structure looks good"

# Check key files
echo "📄 Checking key files..."
files_to_check=(
    "apps/api/app/main.py"
    "apps/api/app/core/config.py"
    "apps/api/app/api/v1/router.py"
    "apps/api/app/api/v1/auth_routes.py"
    "apps/api/app/core/security.py"
    "apps/api/app/core/dependencies.py"
    "apps/api/app/db/session.py"
    "apps/api/app/db/models/base.py"
    "apps/api/app/db/models/user.py"
    "apps/api/app/schemas/auth.py"
    "apps/api/requirements.txt"
    "apps/api/Dockerfile"
    "apps/api/scripts/test_auth.py"
    "apps/web/package.json"
    "apps/web/next.config.js"
    "apps/web/middleware.ts"
    "docker-compose.yml"
    ".env.example"
)

for file in "${files_to_check[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ $file missing"
        exit 1
    fi
done

echo "✅ All key files present"

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Docker is available"
else
    echo "⚠️  Docker not found, but that's okay for local development"
fi

echo "🎉 Setup verification complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and update values"
echo "2. Run: docker-compose up --build"
echo "3. Test auth: docker-compose exec api python scripts/test_auth.py"
