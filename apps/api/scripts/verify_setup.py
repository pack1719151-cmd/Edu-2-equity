#!/usr/bin/env python3
"""
EduEquity OS Backend Verification Script
Verifies that the backend is set up correctly:
- Creates venv if missing
- Installs requirements
- Imports the app
- Lists routes
- Optionally checks HTTP health if server is running
"""
import os
import sys
import subprocess
import importlib
from pathlib import Path

# Colors for output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
API_DIR = Path(__file__).parent.parent
VENV_DIR = API_DIR / "venv"
REQS_FILE = API_DIR / "requirements.txt"


def print_header(title: str):
    print(f"\n{BLUE}{'='*60}{NC}")
    print(f"{BLUE}  {title}{NC}")
    print(f"{BLUE}{'='*60}{NC}")


def print_pass(msg: str):
    print(f"{GREEN}[PASS]{NC} {msg}")


def print_fail(msg: str):
    print(f"{RED}[FAIL]{NC} {msg}")


def print_warn(msg: str):
    print(f"{YELLOW}[WARN]{NC} {msg}")


def print_info(msg: str):
    print(f"{BLUE}[INFO]{NC} {msg}")


def run_command(cmd: list, cwd: Path = None) -> tuple:
    """Run a command and return (success, output)"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or API_DIR,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def check_venv() -> bool:
    """Check if virtual environment exists"""
    print_header("Virtual Environment Check")
    
    if VENV_DIR.exists():
        print_pass(f"Virtual environment exists at {VENV_DIR}")
        
        # Check if it's a valid venv
        python_path = VENV_DIR / "bin" / "python"
        if python_path.exists():
            print_pass("Python executable found in venv")
            return True
    
    print_warn("Virtual environment not found or invalid")
    return False


def create_venv() -> bool:
    """Create virtual environment"""
    print_header("Creating Virtual Environment")
    
    print_info(f"Creating venv at {VENV_DIR}...")
    success, output = run_command([sys.executable, "-m", "venv", str(VENV_DIR)])
    
    if success:
        print_pass("Virtual environment created successfully")
        return True
    else:
        print_fail(f"Failed to create venv: {output}")
        return False


def install_requirements() -> bool:
    """Install requirements from requirements.txt"""
    print_header("Installing Requirements")
    
    if not REQS_FILE.exists():
        print_fail(f"requirements.txt not found at {REQS_FILE}")
        return False
    
    print_info(f"Installing from {REQS_FILE}...")
    
    pip_path = VENV_DIR / "bin" / "pip"
    success, output = run_command([str(pip_path), "install", "-r", str(REQS_FILE)])
    
    if success:
        print_pass("All requirements installed successfully")
        return True
    else:
        print_fail(f"Failed to install requirements: {output}")
        return False


def check_package_installed(package: str) -> bool:
    """Check if a package is installed in the venv"""
    pip_path = VENV_DIR / "bin" / "pip"
    success, output = run_command([str(pip_path), "show", package])
    return success


def import_and_verify_app() -> bool:
    """Import the FastAPI app and verify it loads correctly"""
    print_header("App Import Verification")
    
    python_path = VENV_DIR / "bin" / "python"
    
    # Build PYTHONPATH to include the API directory
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH", "")
    if pythonpath:
        env["PYTHONPATH"] = f"{API_DIR}:{pythonpath}"
    else:
        env["PYTHONPATH"] = str(API_DIR)
    
    # Test import
    code, output = run_command([
        str(python_path), "-c",
        "from app.main import app; print('App imported successfully'); print(f'App title: {app.title}'); print(f'Routes: {[r.path for r in app.routes]}')"
    ], cwd=API_DIR)
    
    if code:
        print_pass("App imported successfully")
        # Extract and print route info
        for line in output.split('\n'):
            if 'Routes:' in line:
                print_info(f"Registered routes: {line.split('Routes:')[1].strip()}")
        return True
    else:
        print_fail(f"Failed to import app: {output}")
        return False


def check_server_health() -> bool:
    """Check if server is running and responding"""
    print_header("Server Health Check")
    
    import requests
    
    # Check root endpoint
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_pass(f"Root endpoint: {data.get('message', 'OK')}")
            print_info(f"Version: {data.get('version')}")
        else:
            print_fail(f"Root endpoint returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print_warn(f"Server not running at {BASE_URL} (connection refused)")
        print_info("Start server with: cd apps/api && source venv/bin/activate && uvicorn app.main:app --reload --port 8000")
        return False
    except requests.exceptions.Timeout:
        print_fail("Server request timed out")
        return False
    
    # Check health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_pass(f"Health endpoint: {response.json().get('status')}")
        else:
            print_fail(f"Health endpoint returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print_warn("Health endpoint not reachable")
    except requests.exceptions.Timeout:
        print_warn("Health endpoint timed out")
    
    # Check API health
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        if response.status_code == 200:
            print_pass(f"API Health endpoint: {response.json().get('status')}")
        else:
            print_fail(f"API Health returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print_warn("API health endpoint not reachable")
    except requests.exceptions.Timeout:
        print_warn("API health endpoint timed out")
    
    return True


def verify_requests_package() -> bool:
    """Verify requests package is installed"""
    print_header("Package Verification")
    
    if check_package_installed("requests"):
        print_pass("requests package is installed")
        return True
    else:
        print_fail("requests package is NOT installed")
        return False


def main():
    """Run all verification steps"""
    print_header("EduEquity OS Backend Verification")
    print_info(f"API Directory: {API_DIR}")
    print_info(f"Base URL: {BASE_URL}")
    
    all_passed = True
    
    # Step 1: Check/Create venv
    if not check_venv():
        if not create_venv():
            all_passed = False
    
    # Step 2: Install requirements
    if not install_requirements():
        all_passed = False
    
    # Step 3: Verify requests package
    if not verify_requests_package():
        all_passed = False
    
    # Step 4: Import and verify app
    if not import_and_verify_app():
        all_passed = False
    
    # Step 5: Check server health (if running)
    check_server_health()
    
    # Summary
    print_header("Verification Summary")
    if all_passed:
        print_pass("All verification checks passed!")
        print_info("Backend is ready to use.")
        print_info("\nTo start the server:")
        print_info(f"  cd {API_DIR}")
        print_info("  source venv/bin/activate")
        print_info("  uvicorn app.main:app --reload --port 8000")
        return 0
    else:
        print_fail("Some verification checks failed.")
        print_info("Please review the errors above and fix them.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

