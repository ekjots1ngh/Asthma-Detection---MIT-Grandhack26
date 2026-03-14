# React Native Expo ↔ FastAPI Backend - Debugging Guide

Complete guide to fix "localhost refused to connect" and other connection issues.

---

## 🔍 Understanding the Problem

### Why "localhost refused to connect"?

When you run your React Native app on a mobile device (or emulator) and try to connect to `http://localhost:8000`, it fails because:

- **`localhost` = the device itself**
- When running on a **mobile device**, `localhost:8000` means "port 8000 on the phone"
- The FastAPI server is actually running on **your computer**, not the phone
- The device has **no way to access your computer's localhost**

---

## 🚨 Possible Causes (Ranked by Likelihood)

### **1. Mobile Device Using `localhost` (MOST COMMON) 🔴**

**Symptom**: Works on web/emulator, fails on real device

**Why**: Real devices can't reach `localhost` on your computer

**Solution**: Use your computer's IP address instead

---

### **2. Backend Server Not Running 🔴**

**Symptom**: Connection timeout or immediate refusal

**Why**: FastAPI isn't started or crashed

**Solution**: Start the server properly

---

### **3. Incorrect Port 🟡**

**Symptom**: Connection refused

**Why**: App configured for wrong port

**Solution**: Verify port matches (default: 8000)

---

### **4. Firewall Blocking Connection 🟡**

**Symptom**: Works on same machine, fails from network

**Why**: Firewall blocks incoming connections

**Solution**: Allow port through firewall

---

### **5. Wrong Network Setup 🟡**

**Symptom**: Works on WiFi, fails on mobile hotspot (or vice versa)

**Why**: Different networks or routing issues

**Solution**: Verify network connectivity

---

### **6. App Running on Different Machine 🟡**

**Symptom**: Can't reach backend from another computer

**Why**: Backend only listens on localhost (127.0.0.1)

**Solution**: Configure to listen on all interfaces (0.0.0.0)

---

---

## ✅ Step-by-Step Troubleshooting

### **STEP 1: Verify the Backend Server is Running**

#### Option A: Check if Server is Running

```bash
# Check if port 8000 is in use
lsof -i :8000           # macOS/Linux
netstat -ano | grep 8000  # Windows

# You should see something like:
# python    25131 user   11u  IPv4 0x12345  0t0 TCP 127.0.0.1:8000 (LISTEN)
```

#### Option B: Test Health Endpoint

```bash
# Method 1: cURL
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","service":"respiratory-screening-api","version":"1.0.0"}

# Method 2: Python
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"

# Method 3: Browser
# Open: http://localhost:8000/docs
# Should show Swagger UI with interactive documentation
```

#### Option C: Check Server Logs

```bash
# If server running in terminal, check console output
# Look for:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete

# If running in background, check logs
tail -f /tmp/api_demo.log
```

---

### **STEP 2: Identify Which Setup You Have**

#### Scenario A: Android Emulator
```
Your Computer
├── FastAPI Server (localhost:8000)
└── Android Emulator
    └── React Native App

Connection: Emulator can reach computer via 10.0.2.2
```

#### Scenario B: iOS Simulator
```
Your Computer (macOS)
├── FastAPI Server (localhost:8000)
└── iOS Simulator
    └── React Native App

Connection: Simulator can reach computer via localhost or 127.0.0.1
```

#### Scenario C: Physical Android Device (Same WiFi)
```
Router (WiFi Network)
├── Your Computer (192.168.1.100)
│   └── FastAPI Server (localhost:8000)
└── Android Device (192.168.1.50)
    └── React Native App

Connection: Device can reach computer via 192.168.1.100:8000
```

#### Scenario D: Physical iOS Device (Same WiFi)
```
Router (WiFi Network)
├── Your Computer (192.168.1.100)
│   └── FastAPI Server (localhost:8000)
└── iPhone (192.168.1.101)
    └── React Native App

Connection: Device can reach computer via 192.168.1.100:8000
```

#### Scenario E: Expo Go App on Phone
```
Same as Scenario C or D - physical device on same WiFi
```

---

### **STEP 3: Get Your Computer's IP Address**

#### macOS/Linux:
```bash
# Get all network info
ifconfig

# Or more specifically
ipconfig getifaddr en0    # macOS
hostname -I               # Linux

# Look for inet address like: 192.168.1.100
```

#### Windows:
```bash
ipconfig

# Look for "IPv4 Address" like: 192.168.1.100
```

#### macOS (Easiest):
```bash
# Run this simple command
python -c "import socket; print(socket.gethostbyname(socket.gethostname()))"

# Or
python -c "import os; os.system('ifconfig | grep \"inet \" | grep -v 127.0.0.1')"
```

---

### **STEP 4: Configure Backend to Accept External Connections**

#### Current Configuration (Only Localhost):
```python
# ❌ This ONLY accepts localhost connections
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
```

#### Correct Configuration (All Interfaces):
```python
# ✅ This accepts connections from any device
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
```

#### Start Server Correctly:
```bash
# Option 1: Development with reload
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000

# Option 2: Production mode
uvicorn api_server:app --host 0.0.0.0 --port 8000

# Option 3: Multiple workers
gunicorn api_server:app -w 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

### **STEP 5: Update Your Mobile App's API URL**

#### Find the API URL Configuration in Your App

Look in your React Native code for where you define the API URL:

```javascript
// ❌ OLD - Only works for web/emulator
const API_URL = 'http://localhost:8000';

// ✅ NEW - Works for mobile devices
const API_URL = 'http://192.168.1.100:8000';  // Your computer's IP
```

#### Create Dynamic Configuration

```javascript
// app/config.js
import { Platform } from 'react-native';

let API_URL;

if (Platform.OS === 'web') {
  // Web browser
  API_URL = 'http://localhost:8000';
} else {
  // Mobile app - use your computer's IP
  API_URL = 'http://192.168.1.100:8000';
}

export default API_URL;
```

#### Or Use Environment Variables

```javascript
// Create .env file
API_URL=http://192.168.1.100:8000

// In your code
import { API_URL } from '@env';
```

---

### **STEP 6: Test the Connection**

#### Test from Your Computer:
```bash
# Method 1: cURL
curl -X POST -F "file=@test.wav" http://localhost:8000/analyze-breathing

# Method 2: Python
python test_api_client.py

# Method 3: Browser
open http://localhost:8000/docs
```

#### Test from Mobile Device (Same WiFi):
```bash
# On iOS/Android, open browser and visit:
http://192.168.1.100:8000/health

# Should see response

# Or in your React Native app, test with:
fetch('http://192.168.1.100:8000/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

#### Test from Command Line on Physical Device:
```bash
# From device's terminal (if available)
curl http://192.168.1.100:8000/health
```

---

## 🔧 Complete Troubleshooting Checklist

### **Checklist for Physical Device on Same WiFi**

```
□ Backend server started with: uvicorn api_server:app --host 0.0.0.0 --port 8000
□ Verified server running: curl http://localhost:8000/health → 200 OK
□ Found your computer's IP: ipconfig getifaddr en0 (e.g., 192.168.1.100)
□ Updated app API_URL to: http://192.168.1.100:8000
□ Device on same WiFi network as computer
□ Firewall allows port 8000 (may need to add rule)
□ Tested from device browser: http://192.168.1.100:8000/health → works
□ Mobile app now uses correct API_URL
□ Restarted mobile app after URL change
□ Verified connection: fetch('http://192.168.1.100:8000/health').then(...)
```

### **Checklist for Android Emulator**

```
□ Backend server started with: uvicorn api_server:app --host 0.0.0.0 --port 8000
□ Verified server running: curl http://localhost:8000/health → 200 OK
□ Android emulator can reach host via: 10.0.2.2
□ Updated app API_URL to: http://10.0.2.2:8000
□ Restarted emulator if needed
□ Tested from emulator browser: http://10.0.2.2:8000/health
```

### **Checklist for iOS Simulator**

```
□ Backend server started with: uvicorn api_server:app --host 0.0.0.0 --port 8000
□ Verified server running: curl http://localhost:8000/health → 200 OK
□ iOS simulator can reach host via: localhost or 127.0.0.1
□ API_URL: http://localhost:8000 (this works on simulator!)
□ Tested from simulator browser: http://localhost:8000/health
```

---

## 🛠️ Quick Fix Scenarios

### **Scenario 1: "Connection refused" on Physical Device**

```
1. ❌ Problem: Using http://localhost:8000
   ✅ Solution: Change to http://YOUR_IP:8000

2. ❌ Problem: Server only listening on 127.0.0.1
   ✅ Solution: Start with --host 0.0.0.0

3. ❌ Problem: Device on different WiFi
   ✅ Solution: Ensure both on same network

4. ❌ Problem: Firewall blocking
   ✅ Solution: Allow port 8000 in firewall settings
```

### **Scenario 2: Works from Computer, Not from Device**

```
This is the MOST COMMON problem!

1. ✅ Check: curl http://localhost:8000/health → Works
2. ✅ Check: Your IP: ipconfig getifaddr en0 → 192.168.1.100
3. ❌ Check: App using localhost instead of IP

SOLUTION:
- Change app from: http://localhost:8000
- Change app to: http://192.168.1.100:8000
```

### **Scenario 3: Works on Emulator, Not on Real Device**

```
1. ✅ Emulator: http://10.0.2.2:8000 works
2. ❌ Device: http://192.168.1.100:8000 fails

SOLUTIONS:
a) Different networks:
   - Verify device on same WiFi
   - Device might be on mobile hotspot

b) Firewall issue:
   - Allow port 8000 on computer
   - Check macOS/Windows firewall

c) Backend not accessible:
   - Verify with: curl http://YOUR_IP:8000/health
   - From a different computer on network
```

---

## 📱 Specific Instructions by Platform

### **Android Emulator**

```javascript
// In your React Native code
const API_URL = 'http://10.0.2.2:8000';

// Why 10.0.2.2?
// - Android emulator runs in a virtual machine
// - 10.0.2.2 is a special alias for the host machine
// - Your computer running Android Studio
```

**Test in Emulator Browser:**
1. Open Chrome on emulator
2. Visit: `http://10.0.2.2:8000/docs`
3. Should see Swagger UI

---

### **iOS Simulator**

```javascript
// In your React Native code
const API_URL = 'http://localhost:8000';

// Why localhost works?
// - iOS simulator runs on the same machine
// - localhost resolves to 127.0.0.1 (your computer)
// - No special aliasing needed
```

**Test in Simulator Browser:**
1. Open Safari on simulator
2. Visit: `http://localhost:8000/docs`
3. Should see Swagger UI

---

### **Physical Android Device (Expo Go)**

```javascript
// In your React Native code
// Option 1: Use computer's IP
const API_URL = 'http://192.168.1.100:8000';

// Option 2: Use computer's hostname (if on same network)
const API_URL = 'http://YourComputerName.local:8000';

// Test what YOUR IP is:
// macOS: ipconfig getifaddr en0
// Windows: ipconfig | grep "IPv4 Address"
// Linux: hostname -I
```

**Setup:**
1. Get your computer's IP: `ipconfig getifaddr en0`
2. Ensure phone on same WiFi
3. Update app code with your IP
4. Reload app (⌘R on simulator, Cmd+Shift+R in Expo Go)

---

### **Physical iOS Device (Expo Go)**

```javascript
// Same as Physical Android
const API_URL = 'http://YOUR_COMPUTER_IP:8000';

// Example:
const API_URL = 'http://192.168.1.100:8000';
```

**Setup:**
1. Get your computer's IP (macOS: `ifconfig | grep inet`)
2. Ensure iPhone on same WiFi
3. Update app code
4. Reload in Expo Go

---

## 🌍 Development vs Production Setup

### **Development (Local Machine)**

```
Your Computer:
├── FastAPI Server: 0.0.0.0:8000
├── React Web: localhost:3000
├── iOS Simulator: localhost:8000
└── Android Emulator: 10.0.2.2:8000

Mobile Device on same WiFi:
└── YOUR_COMPUTER_IP:8000
```

**Start server:**
```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

---

### **Production (Cloud Server)**

```
Cloud Server (AWS/GCP/Azure):
├── FastAPI Server: https://api.example.com
└── React App: https://example.com

Mobile Device (Anywhere):
└── https://api.example.com
```

**Update app:**
```javascript
const API_URL = 'https://api.example.com';
```

---

## 🔐 Firewall & Security

### **macOS - Allow Port 8000**

```bash
# Check if port is blocked
sudo lsof -i :8000

# If needed, allow in System Preferences:
# System Preferences → Security & Privacy → Firewall Options
# Add python to allowed apps
```

### **Windows - Allow Port 8000**

```bash
# Check if port is listening
netstat -ano | grep 8000

# Allow in Windows Defender Firewall:
# Settings → Privacy & Security → Firewall & network protection
# Allow an app through firewall → Add python/uvicorn
```

### **Linux - Allow Port 8000**

```bash
# Check if port is open
sudo ufw status

# Allow port 8000
sudo ufw allow 8000
```

---

## 🧪 Complete Test Script

```python
# test_connection.py
import requests
import socket

def get_local_ip():
    """Get computer's local IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def test_api(base_url):
    """Test API connectivity"""
    print(f"\nTesting: {base_url}")
    print("-" * 50)

    endpoints = [
        '/health',
        '/info',
        '/risk-levels',
    ]

    for endpoint in endpoints:
        try:
            response = requests.get(f'{base_url}{endpoint}', timeout=2)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {str(e)}")

# Test all endpoints
print("=" * 50)
print("API Connection Test")
print("=" * 50)

# Test localhost
test_api('http://localhost:8000')

# Test local IP
local_ip = get_local_ip()
test_api(f'http://{local_ip}:8000')

print("\n" + "=" * 50)
print(f"Your computer's IP: {local_ip}")
print(f"Use in mobile app: http://{local_ip}:8000")
print("=" * 50)
```

**Run it:**
```bash
python test_connection.py
```

---

## 📚 Common Error Messages & Solutions

### **"Connection refused"**
```
Cause: Server not running or wrong port
Fix: uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### **"Timeout"**
```
Cause: Server reachable but not responding
Fix: Check if server is hung, restart it
```

### **"Network unreachable"**
```
Cause: Device can't access network
Fix: Verify device on same WiFi
```

### **"Cannot GET /health"**
```
Cause: Backend not running, or wrong URL
Fix: Check backend started, verify IP address
```

### **"CORS error"**
```
Cause: Browser blocking cross-origin request
Fix: Backend already has CORS enabled, should work
```

---

## ✨ Final Quick Reference

| Scenario | API URL | How to Test |
|----------|---------|------------|
| **Web Browser** | `http://localhost:8000` | `curl http://localhost:8000/health` |
| **iOS Simulator** | `http://localhost:8000` | Safari in simulator |
| **Android Emulator** | `http://10.0.2.2:8000` | Chrome in emulator |
| **Physical Device (WiFi)** | `http://192.168.1.100:8000` | Browser on device |
| **Expo Go (Physical)** | `http://YOUR_IP:8000` | In-app fetch() call |
| **Production** | `https://api.example.com` | Browser or fetch() |

**To find YOUR_IP:**
```bash
# macOS/Linux
ipconfig getifaddr en0
# or
hostname -I

# Windows
ipconfig
# Look for "IPv4 Address"
```

---

## 🚀 Next Steps

1. **Identify your setup** (emulator, simulator, physical device)
2. **Get your computer's IP** (if using physical device)
3. **Start backend** with `--host 0.0.0.0`
4. **Update app API_URL**
5. **Test with curl first** before running app
6. **Restart app** after changing URL
7. **Check browser** on mobile device

---

**Still having issues?** Check the troubleshooting checklist above, or test each step individually with the provided commands.
