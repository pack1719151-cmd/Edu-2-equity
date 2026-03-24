#!/usr/bin/env python3
"""
Comprehensive Auth Test Script for EduEquity OS
Tests all auth endpoints with both Bearer token and cookie authentication.
"""
import os
import requests
import json
import sys

# Use BASE_URL env var with fallback
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
API_BASE = f"{BASE_URL}/api/v1"

# Store session cookies
session = requests.Session()


def check_api_reachable():
    """Check if the API is reachable before running tests"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.Timeout:
        pass
    return False


def wait_for_api(max_attempts=10, delay=1):
    """Wait for API to be reachable"""
    for i in range(max_attempts):
        if check_api_reachable():
            return True
        if i < max_attempts - 1:
            import time
            time.sleep(delay)
    return False


def print_header(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_result(test_name: str, passed: bool, details: str = ""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {test_name}")
    if details and not passed:
        print(f"       Details: {details}")
    return passed


def test_health():
    """Test root health endpoint"""
    print_header("Health Checks")
    
    tests_passed = 0
    tests_total = 2
    
    # Test root health
    try:
        response = requests.get(f"{BASE_URL}/health")
        passed = response.status_code == 200 and response.json().get("status") == "healthy"
        tests_passed += 1 if passed else 0
        print_result("Root /health endpoint", passed, response.text if not passed else "")
    except Exception as e:
        print_result("Root /health endpoint", False, str(e))
        tests_total -= 1
    
    # Test API health
    try:
        response = requests.get(f"{API_BASE}/health")
        passed = response.status_code == 200 and response.json().get("status") == "healthy"
        tests_passed += 1 if passed else 0
        print_result("API /api/v1/health endpoint", passed, response.text if not passed else "")
    except Exception as e:
        print_result("API /api/v1/health endpoint", False, str(e))
        tests_total -= 1
    
    return tests_passed, tests_total


def test_register():
    """Test user registration"""
    print_header("Registration Tests")
    
    tests_passed = 0
    tests_total = 3
    
    # Test registration with student role
    try:
        data = {
            "email": "student_test@example.com",
            "password": "password123",
            "full_name": "Test Student",
            "role": "student"
        }
        response = requests.post(f"{API_BASE}/auth/register", json=data)
        passed = response.status_code == 200
        tests_passed += 1 if passed else 0
        print_result("Register student user", passed, response.text if not passed else "")
        if passed:
            user_data = response.json()
            print(f"       User ID: {user_data.get('id')}")
    except Exception as e:
        print_result("Register student user", False, str(e))
        tests_total -= 1
    
    # Test registration with teacher role
    try:
        data = {
            "email": "teacher_test@example.com",
            "password": "password123",
            "full_name": "Test Teacher",
            "role": "teacher"
        }
        response = requests.post(f"{API_BASE}/auth/register", json=data)
        passed = response.status_code == 200
        tests_passed += 1 if passed else 0
        print_result("Register teacher user", passed, response.text if not passed else "")
    except Exception as e:
        print_result("Register teacher user", False, str(e))
        tests_total -= 1
    
    # Test duplicate registration
    try:
        data = {
            "email": "student_test@example.com",
            "password": "password123",
            "full_name": "Duplicate User",
            "role": "student"
        }
        response = requests.post(f"{API_BASE}/auth/register", json=data)
        passed = response.status_code == 400
        tests_passed += 1 if passed else 0
        print_result("Reject duplicate registration", passed, response.text if not passed else "")
    except Exception as e:
        print_result("Reject duplicate registration", False, str(e))
        tests_total -= 1
    
    return tests_passed, tests_total


def test_login_logout():
    """Test login and logout with cookie authentication"""
    print_header("Login/Logout Tests (Cookie Auth)")
    
    tests_passed = 0
    tests_total = 4
    
    # Test login
    login_response = None
    try:
        data = {
            "email": "student_test@example.com",
            "password": "password123"
        }
        # Use session to preserve cookies
        response = session.post(f"{API_BASE}/auth/login", json=data)
        login_response = response
        passed = response.status_code == 200
        tests_passed += 1 if passed else 0
        print_result("Login with credentials", passed, response.text if not passed else "")
        
        if passed:
            # Check that cookies are set
            cookies = session.cookies.get_dict()
            print(f"       Cookies set: {list(cookies.keys())}")
            if "eduequity_session" in cookies:
                print("       ✅ Access token cookie set")
            if "refresh_token" in cookies:
                print("       ✅ Refresh token cookie set")
            if "user_role" in cookies:
                print(f"       ✅ User role cookie set: {cookies['user_role']}")
    except Exception as e:
        print_result("Login with credentials", False, str(e))
        tests_total -= 1
    
    # Test /me with cookie auth
    try:
        response = session.get(f"{API_BASE}/auth/me")
        passed = response.status_code == 200
        tests_passed += 1 if passed else 0
        print_result("GET /me with cookie", passed, response.text if not passed else "")
        if passed:
            user_data = response.json()
            print(f"       User: {user_data.get('full_name')} ({user_data.get('role')})")
    except Exception as e:
        print_result("GET /me with cookie", False, str(e))
        tests_total -= 1
    
    # Test /me with Bearer token
    try:
        if login_response and login_response.status_code == 200:
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{API_BASE}/auth/me", headers=headers)
            passed = response.status_code == 200
            tests_passed += 1 if passed else 0
            print_result("GET /me with Bearer token", passed, response.text if not passed else "")
        else:
            print_result("GET /me with Bearer token", False, "No token available")
            tests_total -= 1
    except Exception as e:
        print_result("GET /me with Bearer token", False, str(e))
        tests_total -= 1
    
    # Test logout
    try:
        response = session.post(f"{API_BASE}/auth/logout")
        passed = response.status_code == 200
        tests_passed += 1 if passed else 0
        print_result("Logout", passed, response.text if not passed else "")
        
        # Verify cookies are cleared
        cookies = session.cookies.get_dict()
        if not cookies:
            print("       ✅ All cookies cleared")
    except Exception as e:
        print_result("Logout", False, str(e))
        tests_total -= 1
    
    return tests_passed, tests_total


def test_refresh_token():
    """Test token refresh endpoint"""
    print_header("Token Refresh Tests")
    
    tests_passed = 0
    tests_total = 2
    
    # Login first
    try:
        data = {
            "email": "teacher_test@example.com",
            "password": "password123"
        }
        response = session.post(f"{API_BASE}/auth/login", json=data)
        passed = response.status_code == 200
        print_result("Login before refresh test", passed, response.text if not passed else "")
        if not passed:
            return 0, 2
    except Exception as e:
        print_result("Login before refresh test", False, str(e))
        return 0, 2
    
    # Test refresh
    try:
        response = session.post(f"{API_BASE}/auth/refresh")
        passed = response.status_code == 200
        tests_passed += 1 if passed else 0
        print_result("Refresh token", passed, response.text if not passed else "")
        
        if passed:
            # Check new access token
            cookies = session.cookies.get_dict()
            print(f"       New cookies: {list(cookies.keys())}")
    except Exception as e:
        print_result("Refresh token", False, str(e))
        tests_total -= 1
    
    # Test refresh without token (should fail)
    try:
        # Create new session without cookies
        fresh_session = requests.Session()
        response = fresh_session.post(f"{API_BASE}/auth/refresh")
        passed = response.status_code == 401
        tests_passed += 1 if passed else 0
        print_result("Reject refresh without token", passed, response.text if not passed else "")
    except Exception as e:
        print_result("Reject refresh without token", False, str(e))
        tests_total -= 1
    
    return tests_passed, tests_total


def test_auth_health():
    """Test auth-specific health endpoint"""
    print_header("Auth Health Check")
    
    try:
        response = requests.get(f"{API_BASE}/auth/health")
        passed = response.status_code == 200 and response.json().get("status") == "healthy"
        print_result("GET /api/v1/auth/health", passed, response.text if not passed else "")
        return 1 if passed else 0, 1
    except Exception as e:
        print_result("GET /api/v1/auth/health", False, str(e))
        return 0, 1


def run_all_tests():
    """Run all auth tests"""
    print_header("EduEquity OS Auth System Test Suite")
    print(f"Target: {BASE_URL}")
    print(f"API Base: {API_BASE}")
    
    # Check if API is reachable
    print("\nChecking API availability...")
    if not check_api_reachable():
        print("\n❌ ERROR: API is not reachable at {BASE_URL}")
        print("Start backend first: uvicorn app.main:app --reload --port 8000")
        print("In another terminal, run:")
        print("    cd /workspaces/eduequity-os/apps/api")
        print("    source venv/bin/activate")
        print("    uvicorn app.main:app --reload --port 8000")
        sys.exit(1)
    
    all_passed = 0
    all_total = 0
    
    # Run tests
    passed, total = test_health()
    all_passed += passed
    all_total += total
    
    passed, total = test_register()
    all_passed += passed
    all_total += total
    
    passed, total = test_login_logout()
    all_passed += passed
    all_total += total
    
    passed, total = test_refresh_token()
    all_passed += passed
    all_total += total
    
    passed, total = test_auth_health()
    all_passed += passed
    all_total += total
    
    # Summary
    print_header("Test Summary")
    print(f"Total Tests: {all_total}")
    print(f"Passed: {all_passed}")
    print(f"Failed: {all_total - all_passed}")
    print(f"Success Rate: {(all_passed/all_total)*100:.1f}%")
    
    if all_passed == all_total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠️  {all_total - all_passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())

