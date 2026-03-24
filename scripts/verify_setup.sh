#!/bin/bash

# EduEquity OS Verification Script
# Verifies that the project is set up correctly

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  EduEquity OS Verification${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

PASS=0
FAIL=0
WARN=0

check() {
    if $1; then
        echo -e "${GREEN}[PASS]${NC} $2"
        ((PASS++))
    else
        echo -e "${RED}[FAIL]${NC} $2"
        ((FAIL++))
    fi
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    ((WARN++))
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Check directory structure
echo -e "${YELLOW}Checking directory structure...${NC}"
check "[ -d apps/web ]" "Web app directory exists"
check "[ -d apps/api ]" "API app directory exists"
check "[ -d packages ]" "Packages directory exists"
check "[ -d docs ]" "Docs directory exists"
check "[ -d scripts ]" "Scripts directory exists"

echo ""

# Check root files
echo -e "${YELLOW}Checking root configuration files...${NC}"
check "[ -f package.json ]" "package.json exists"
check "[ -f pyproject.toml ]" "pyproject.toml exists"
check "[ -f .env.example ]" ".env.example exists"
check "[ -f .gitignore ]" ".gitignore exists"
check "[ -f README.md ]" "README.md exists"

echo ""

# Check web app
echo -e "${YELLOW}Checking web application...${NC}"
check "[ -f apps/web/package.json ]" "Web package.json exists"
check "[ -f apps/web/next.config.js ]" "Next.js config exists"
check "[ -f apps/web/tsconfig.json ]" "TypeScript config exists"
check "[ -f apps/web/src/app/layout.tsx ]" "Root layout exists"
check "[ -f apps/web/src/app/page.tsx ]" "Home page exists"
check "[ -f apps/web/middleware.ts ]" "Middleware exists"

echo ""

# Check API app
echo -e "${YELLOW}Checking API application...${NC}"
check "[ -f apps/api/app/main.py ]" "Main app exists"
check "[ -f apps/api/requirements.txt ]" "Requirements.txt exists"
check "[ -f apps/api/app/core/config.py ]" "Core config exists"
check "[ -f apps/api/app/db/session.py ]" "Database session exists"

echo ""

# Check node_modules
echo -e "${YELLOW}Checking dependencies...${NC}"
if [ -d node_modules ]; then
    check "[ -d node_modules/.bin ]" "Node modules binaries exist"
else
    warn "node_modules not found. Run 'pnpm install'"
fi

echo ""

# Check environment file
echo -e "${YELLOW}Checking environment configuration...${NC}"
if [ -f .env ]; then
    check "true" ".env file exists"
else
    warn ".env file not found. Copy .env.example to .env"
fi

echo ""

# Summary
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  Verification Summary${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo -e "Passed:  ${GREEN}$PASS${NC}"
echo -e "Failed:  ${RED}$FAIL${NC}"
echo -e "Warnings: ${YELLOW}$WARN${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}All critical checks passed!${NC}"
    exit 0
else
    echo -e "${RED}Some checks failed. Please review the errors above.${NC}"
    exit 1
fi

