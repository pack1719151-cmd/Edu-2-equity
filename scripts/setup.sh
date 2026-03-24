#!/bin/bash

# EduEquity OS Setup Script
# This script sets up the development environment for EduEquity OS

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  EduEquity OS Setup Script${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v)
    print_status "Node.js is installed: $NODE_VERSION"
else
    print_error "Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_status "Python is installed: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed. Please install Python 3.10+"
    exit 1
fi

# Check PostgreSQL
if command -v psql &> /dev/null; then
    print_status "PostgreSQL is installed"
else
    print_warning "PostgreSQL is not installed. You may need to install it."
fi

# Check Redis
if command -v redis-cli &> /dev/null; then
    print_status "Redis is installed"
else
    print_warning "Redis is not installed. You may need to install it."
fi

# Check pnpm
if command -v pnpm &> /dev/null; then
    PNPM_VERSION=$(pnpm -v)
    print_status "pnpm is installed: v$PNPM_VERSION"
else
    print_warning "pnpm is not installed. Installing..."
    npm install -g pnpm
fi

echo ""
print_info "Installing dependencies..."

# Install pnpm dependencies
echo -e "${YELLOW}Installing pnpm dependencies...${NC}"
pnpm install

print_status "Dependencies installed"

echo ""
print_info "Setting up environment variables..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    print_status "Created .env file from template"
    print_warning "Please edit .env with your database credentials"
else
    print_status ".env file already exists"
fi

echo ""
print_info "Setting up database..."

# Create database if it doesn't exist
DB_NAME=${DATABASE_NAME:-eduequity}
DB_USER=${DATABASE_USER:-postgres}
DB_PASSWORD=${DATABASE_PASSWORD:-postgres}

if command -v psql &> /dev/null; then
    if PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw $DB_NAME; then
        print_status "Database '$DB_NAME' already exists"
    else
        print_info "Creating database '$DB_NAME'..."
        PGPASSWORD=$DB_PASSWORD createdb -U $DB_USER $DB_NAME 2>/dev/null || \
        PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || \
        print_warning "Could not create database. Please create it manually."
    fi
fi

echo ""
print_info "Running database migrations..."

# Run migrations
cd apps/api && python -m alembic upgrade head 2>/dev/null || \
    print_warning "Could not run migrations. Please run them manually: cd apps/api && python -m alembic upgrade head"

cd ../..

echo ""
print_info "Seeding demo data..."

# Seed demo data
cd apps/api && python scripts/seed_demo_data.py 2>/dev/null || \
    print_warning "Could not seed demo data. Please run manually: cd apps/api && python scripts/seed_demo_data.py"

cd ../..

echo ""
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env with your database credentials"
echo "2. Start the development servers: pnpm dev"
echo ""
echo "Default login credentials (after seeding):"
echo "  Admin: admin@eduequity.local / admin123"
echo "  Teacher: teacher@eduequity.local / teacher123"
echo "  Student: student@eduequity.local / student123"
echo ""
print_info "Access the application at http://localhost:3000"

