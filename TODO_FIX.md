# Fix Plan - EduEquity OS

## Phase 1: Infrastructure Setup
- [ ] 1.1 Start FastAPI backend on port 8000
- [ ] 1.2 Update .env.local with NEXT_PUBLIC_API_V1=/api/v1
- [ ] 1.3 Install/verify frontend dependencies

## Phase 2: Fix Proxy Route
- [ ] 2.1 Ensure proxy route works for all HTTP methods
- [ ] 2.2 Forward cookies and headers correctly
- [ ] 2.3 Test proxy with curl

## Phase 3: Fix UI/Auth Flow
- [ ] 3.1 Fix register page to show real backend errors
- [ ] 3.2 Fix login page to redirect based on user_role cookie
- [ ] 3.3 Ensure proper error handling

## Phase 4: Test End-to-End
- [ ] 4.1 Test: curl http://localhost:3000/api/v1/health
- [ ] 4.2 Test: curl http://localhost:3000/api/v1/auth/health
- [ ] 4.3 Test: Register user via browser/curl
- [ ] 4.4 Test: Login user via browser/curl

## Phase 5: Git Finalize
- [ ] 5.1 Show git status
- [ ] 5.2 Stage changes
- [ ] 5.3 Create clean commit
- [ ] 5.4 Push to main

