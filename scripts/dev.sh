#!/bin/bash

# EduEquity OS Development Server Script
# Starts both frontend and backend development servers

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  EduEquity OS Development Server${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${GREEN}Shutting down servers...${NC}"
    # Kill background jobs
    jobs -p | xargs -r kill 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend server
echo -e "${GREEN}Starting Backend Server...${NC}"
cd apps/api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ../..

echo -e "${GREEN}Backend server started on http://localhost:8000${NC}"

# Start frontend server
echo -e "${GREEN}Starting Frontend Server...${NC}"
cd apps/web
npm run dev &
FRONTEND_PID=$!
cd ../..

echo -e "${GREEN}Frontend server started on http://localhost:3000${NC}"

echo ""
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  Servers Running${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

