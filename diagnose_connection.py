#!/usr/bin/env python3
"""
Diagnostic tool for React Native Expo ↔ FastAPI connection issues.

Run this script to identify and troubleshoot connection problems.
"""

import socket
import requests
import sys
import subprocess
import os
from pathlib import Path

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{title}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.ENDC}\n")


def print_success(msg):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {msg}{Colors.ENDC}")


def print_fail(msg):
    """Print failure message"""
    print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")


def print_warning(msg):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {msg}{Colors.ENDC}")


def print_info(msg):
    """Print info message"""
    print(f"{Colors.OKBLUE}ℹ️  {msg}{Colors.ENDC}")


def get_local_ip():
    """Get computer's local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return None


def get_hostname():
    """Get computer hostname"""
    try:
        return socket.gethostname()
    except:
        return None


def is_port_listening(port, host='127.0.0.1'):
    """Check if port is listening"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def test_endpoint(url, timeout=2):
    """Test an API endpoint"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code, response.json()
    except requests.exceptions.Timeout:
        return 'TIMEOUT', None
    except requests.exceptions.ConnectionError:
        return 'CONNECTION_ERROR', None
    except Exception as e:
        return 'ERROR', str(e)


def check_server_running():
    """Check if FastAPI server is running"""
    print_section("1. Checking if Backend Server is Running")

    if is_port_listening(8000):
        print_success("Port 8000 is listening")
        return True
    else:
        print_fail("Port 8000 is NOT listening")
        print_info("Start the server with:")
        print(f"  {Colors.OKCYAN}uvicorn api_server:app --host 0.0.0.0 --port 8000{Colors.ENDC}")
        return False


def test_localhost():
    """Test localhost connection"""
    print_section("2. Testing Localhost Connection")

    endpoints = {
        '/health': 'Health Check',
        '/info': 'API Info',
        '/risk-levels': 'Risk Levels',
    }

    all_working = True

    for endpoint, description in endpoints.items():
        url = f'http://localhost:8000{endpoint}'
        status, response = test_endpoint(url)

        if status == 200:
            print_success(f"{description}: {url}")
        else:
            print_fail(f"{description}: {status}")
            all_working = False

    return all_working


def get_network_info():
    """Get network configuration info"""
    print_section("3. Your Computer's Network Configuration")

    # Local IP
    local_ip = get_local_ip()
    if local_ip:
        print_success(f"Local IP Address: {Colors.OKCYAN}{local_ip}{Colors.ENDC}")
    else:
        print_fail("Could not determine local IP address")
        return None

    # Hostname
    hostname = get_hostname()
    if hostname:
        print_info(f"Hostname: {Colors.OKCYAN}{hostname}{Colors.ENDC}")
    else:
        print_fail("Could not determine hostname")

    return local_ip


def test_network_ip(ip):
    """Test connecting via network IP"""
    print_section("4. Testing Network IP Connection")

    endpoints = {
        '/health': 'Health Check',
        '/info': 'API Info',
    }

    all_working = True

    for endpoint, description in endpoints.items():
        url = f'http://{ip}:8000{endpoint}'
        status, response = test_endpoint(url)

        if status == 200:
            print_success(f"{description}: {url}")
        else:
            print_fail(f"{description}: {url}")
            print_info(f"  Status: {status}")
            all_working = False

    return all_working


def show_mobile_setup_instructions(local_ip):
    """Show setup instructions for mobile"""
    print_section("5. Mobile App Configuration")

    print_info("Your mobile device needs to know how to reach your backend server.")
    print()

    # Android Emulator
    print(f"{Colors.BOLD}For Android Emulator:{Colors.ENDC}")
    print(f"  API_URL = '{Colors.OKCYAN}http://10.0.2.2:8000{Colors.ENDC}'")
    print(f"  (10.0.2.2 is the special alias for your computer in Android emulator)")
    print()

    # iOS Simulator
    print(f"{Colors.BOLD}For iOS Simulator:{Colors.ENDC}")
    print(f"  API_URL = '{Colors.OKCYAN}http://localhost:8000{Colors.ENDC}'")
    print(f"  (iOS simulator can reach localhost directly)")
    print()

    # Physical Device
    print(f"{Colors.BOLD}For Physical Device (on same WiFi):{Colors.ENDC}")
    print(f"  API_URL = '{Colors.OKCYAN}http://{local_ip}:8000{Colors.ENDC}'")
    print(f"  (Use your computer's IP address)")
    print()

    # Code example
    print(f"{Colors.BOLD}Code Example:{Colors.ENDC}")
    print(f"""
{Colors.OKCYAN}// app/config.js or app.js
const API_URL = 'http://{local_ip}:8000';

// In your API calls:
fetch(API_URL + '/analyze-breathing', {{
  method: 'POST',
  body: formData
}})
.then(r => r.json())
.then(results => console.log(results))
.catch(e => console.error('Error:', e)){Colors.ENDC}
""")


def show_quick_fix():
    """Show most common quick fix"""
    print_section("🚀 Most Likely Quick Fix")

    local_ip = get_local_ip()

    print(f"{Colors.WARNING}{Colors.BOLD}The Problem:{Colors.ENDC}")
    print(f"  Your app is probably using:")
    print(f"    ❌ API_URL = 'http://localhost:8000'")
    print()

    print(f"{Colors.OKGREEN}{Colors.BOLD}The Solution:{Colors.ENDC}")
    print(f"  Change to:")
    print(f"    ✅ API_URL = 'http://{local_ip}:8000'")
    print()

    print(f"{Colors.BOLD}Steps:{Colors.ENDC}")
    print(f"  1. Make sure backend is running:")
    print(f"     {Colors.OKCYAN}uvicorn api_server:app --host 0.0.0.0 --port 8000{Colors.ENDC}")
    print()
    print(f"  2. In your React Native code, change:")
    print(f"     {Colors.OKCYAN}const API_URL = 'http://{local_ip}:8000';{Colors.ENDC}")
    print()
    print(f"  3. Restart your app:")
    print(f"     - If using Expo Go: Reload the app (⌘R or Cmd+R)")
    print(f"     - If using emulator: Restart the emulator")
    print()
    print(f"  4. Test the connection from your device:")
    print(f"     - Open browser and visit: http://{local_ip}:8000/health")
    print(f"     - Should see: {Colors.OKCYAN}{{ \"status\": \"healthy\", ... }}{Colors.ENDC}")


def run_full_diagnostic():
    """Run complete diagnostic"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║     React Native Expo ↔ FastAPI Connection Diagnostics           ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")

    # Step 1: Check if server is running
    server_running = check_server_running()

    if not server_running:
        print()
        print_fail("Backend server is not running!")
        print_info("Please start the server first:")
        print(f"  {Colors.OKCYAN}cd /path/to/project")
        print(f"  uvicorn api_server:app --host 0.0.0.0 --port 8000{Colors.ENDC}")
        return

    # Step 2: Test localhost
    localhost_working = test_localhost()

    # Step 3: Get network info
    local_ip = get_network_info()

    if not local_ip:
        print_fail("Could not determine your local IP address")
        return

    # Step 4: Test network IP
    if server_running:
        network_working = test_network_ip(local_ip)
    else:
        network_working = False

    # Step 5: Show mobile setup
    show_mobile_setup_instructions(local_ip)

    # Final summary
    print_section("Summary & Next Steps")

    print(f"{Colors.BOLD}Server Status:{Colors.ENDC}")
    if server_running and localhost_working:
        print_success("Backend server is running correctly on localhost")
    else:
        print_fail("Backend server has issues - please check server logs")

    print()
    print(f"{Colors.BOLD}Network Status:{Colors.ENDC}")
    if network_working:
        print_success(f"Backend is accessible via network at http://{local_ip}:8000")
    else:
        print_warning(f"Cannot reach http://{local_ip}:8000 from other computers")
        print_info("Possible causes:")
        print_info("  - Backend not listening on 0.0.0.0 (try --host 0.0.0.0)")
        print_info("  - Firewall blocking port 8000")
        print_info("  - Different networks")

    print()
    print(f"{Colors.BOLD}{Colors.OKGREEN}What To Do:{Colors.ENDC}")
    print(f"  1. Start backend: {Colors.OKCYAN}uvicorn api_server:app --host 0.0.0.0 --port 8000{Colors.ENDC}")
    print(f"  2. Update app: {Colors.OKCYAN}API_URL = 'http://{local_ip}:8000'{Colors.ENDC}")
    print(f"  3. Restart app in Expo Go or emulator")
    print(f"  4. Test from device browser: {Colors.OKCYAN}http://{local_ip}:8000/health{Colors.ENDC}")

    # Show quick fix
    print()
    show_quick_fix()


if __name__ == '__main__':
    try:
        run_full_diagnostic()
        print()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Diagnostics cancelled by user{Colors.ENDC}\n")
    except Exception as e:
        print(f"\n{Colors.FAIL}Error during diagnostics: {e}{Colors.ENDC}\n")
        import traceback
        traceback.print_exc()
