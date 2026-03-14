# Complete Integration Guide: Mobile App + Audio Analyzer + FastAPI Backend

End-to-end guide for deploying the respiratory screening system with all components.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    React Native Mobile App                      │
│  (Home Screen → Recording Screen → Results Screen)              │
│                                                                 │
│  - Records 10-second breathing audio                           │
│  - Displays real-time waveform visualization                   │
│  - Uploads to backend API                                      │
└──────────────────────┬──────────────────────────────────────────┘
                       │ HTTP POST /analyze-breathing
                       │ (WAV/MP3 file upload)
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│          FastAPI Backend Server (api_server.py)                 │
│                                                                 │
│  POST /analyze-breathing  →  Process Audio File               │
│  GET  /health             →  Health Check                      │
│  GET  /info               →  API Information                   │
│  POST /batch-analyze      →  Multiple Files                    │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│      Python Audio Analyzer (audio_analyzer.py)                  │
│                                                                 │
│  - FFT Frequency Analysis (100-1000 Hz)                        │
│  - Wheeze Detection                                             │
│  - Respiratory Rate Estimation                                  │
│  - Risk Classification (low/medium/high)                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │ Returns JSON Results
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│      Mobile App Results Display                                 │
│                                                                 │
│  - Color-coded risk level (🟢 🟡 🔴)                          │
│  - Wheeze probability                                           │
│  - Respiratory rate                                             │
│  - Clinical guidance message                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Setup & Installation

### Step 1: Install System Dependencies

```bash
# Python 3.8+ (for backend)
python3 --version

# Node.js 16+ (for mobile app)
node --version
npm --version
```

### Step 2: Install Python Dependencies

```bash
cd /path/to/Asthma-Detection---MIT-Grandhack26

# Install all Python requirements
pip install -r requirements-python.txt

# Includes:
# - numpy, scipy, librosa (audio analysis)
# - fastapi, uvicorn (API server)
# - requests (testing)
```

### Step 3: Install Node Dependencies

```bash
# Install Expo and React Native dependencies
npm install

# Verify installation
npx expo --version
```

---

## Running the Complete System

### Terminal 1: Start FastAPI Backend

```bash
cd /path/to/Asthma-Detection---MIT-Grandhack26

# Development mode (with auto-reload)
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000

# Or production mode
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

Output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2: Start React Native Mobile App

```bash
cd /path/to/Asthma-Detection---MIT-Grandhack26

# Start Expo development server
npm start

# Choose platform:
# - Press 'w' for web (http://localhost:19006)
# - Press 'a' for Android
# - Press 'i' for iOS
# - Scan QR code with Expo Go app
```

### Terminal 3: Run Tests (Optional)

```bash
# Test the API
python test_api_client.py

# Or run audio analyzer tests
python test_audio_analyzer.py
```

---

## Mobile App Integration Details

### File: `app/recording.tsx`

The recording screen captures audio and sends it to the backend:

```typescript
const stopRecording = useCallback(async () => {
  try {
    if (recording) {
      await recording.stopAndUnloadAsync();
      setIsRecording(false);
      const uri = recording.getURI();

      // Navigate to results with recording URI
      router.push({
        pathname: '/results',
        params: { recordingUri: uri },
      });
    }
  } catch (error) {
    console.error('Failed to stop recording:', error);
  }
}, [recording, router]);
```

### File: `app/results.tsx`

The results screen uploads audio to the API:

```typescript
useEffect(() => {
  const uploadAndAnalyze = async () => {
    if (recordingUri) {
      // Create FormData with audio file
      const formData = new FormData();
      formData.append('file', {
        uri: recordingUri,
        type: 'audio/wav',
        name: 'breathing.wav',
      });

      // Send to backend
      try {
        const response = await fetch(
          'http://your-api-server.com:8000/analyze-breathing',
          {
            method: 'POST',
            body: formData,
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        );

        const results = await response.json();

        // Display results
        setWheezeProbability(results.wheeze_probability);
        setRiskLevel(results.risk_level);
        setGuidance(results.guidance);

      } catch (error) {
        console.error('Analysis failed:', error);
      }
    }
  };

  uploadAndAnalyze();
}, [recordingUri]);
```

### Update API URL for Your Environment

In the mobile app, update the API URL based on your deployment:

**For Local Development** (same machine):
```javascript
const API_URL = 'http://localhost:8000';
```

**For Local Network** (different machines):
```javascript
const API_URL = 'http://192.168.1.100:8000';  // Use your server's IP
```

**For Production** (cloud):
```javascript
const API_URL = 'https://api.example.com';  // Use your domain
```

---

## Backend API Integration

### Health Check

Before sending audio, verify the API is ready:

```javascript
async function checkAPIHealth() {
  try {
    const response = await fetch(`${API_URL}/health`);
    const health = await response.json();
    console.log(`API Status: ${health.status}`);
  } catch (error) {
    console.error('API not available:', error);
  }
}
```

### Send Audio for Analysis

```javascript
async function analyzeBreathing(audioUri) {
  const formData = new FormData();
  formData.append('file', {
    uri: audioUri,
    type: 'audio/wav',
    name: 'breathing.wav',
  });

  const response = await fetch(`${API_URL}/analyze-breathing`, {
    method: 'POST',
    body: formData,
  });

  if (response.ok) {
    return await response.json();
  } else {
    throw new Error(`Analysis failed: ${response.status}`);
  }
}
```

### Handle Response

```javascript
const results = await analyzeBreathing(recordingUri);

// Results structure:
{
  wheeze_probability: 0.45,           // 0-1 (0-100%)
  respiratory_rate: 22,                // breaths/minute
  risk_level: "medium",               // "low", "medium", "high"
  guidance: {
    title: "Possible Wheezing",
    message: "Possible wheezing detected. Monitor symptoms.",
    recommendation: "Keep monitoring symptoms...",
    emoji: "⚠"
  },
  metrics: {
    wheeze_intensity: 0.32             // 0-1 (0-100%)
  }
}
```

---

## Data Flow: Step by Step

### User Records Breathing

1. User opens mobile app
2. Clicks "Check My Child's Breathing" button
3. App shows recording instructions
4. User places stethoscope on child's chest
5. App records 10 seconds of breathing audio
6. App captures audio waveform in real-time
7. Recording automatically stops at 10 seconds

### Audio Uploaded to Backend

8. App converts audio to WAV format
9. App creates HTTP POST request to `/analyze-breathing`
10. Audio file sent as multipart form data
11. Backend receives file and validates format

### Backend Processes Audio

12. Audio file saved to temporary location
13. Analyzer loads audio (auto-resampled to 22050 Hz)
14. Audio preprocessing (high-pass filter, normalization)
15. FFT analysis in 100-1000 Hz wheeze range
16. Wheeze probability calculated (energy ratio + spectral concentration)
17. Wheeze intensity calculated (peak magnitude analysis)
18. Respiratory rate estimated (STFT envelope analysis)
19. Risk level determined (combined scoring)
20. Guidance message selected based on risk level
21. Results returned as JSON
22. Temporary file deleted

### Results Displayed to User

23. Mobile app receives JSON response
24. Risk level determined (low/medium/high)
25. Background color set based on risk
26. Wheeze probability shown as percentage
27. Respiratory rate displayed
28. Guidance message displayed
29. User sees recommendations:
    - **Low Risk**: Continue monitoring
    - **Medium Risk**: Monitor and schedule consultation if needed
    - **High Risk**: Seek medical attention

### User Can Continue

30. User can:
    - Check another child (returns to home screen)
    - Re-record (returns to recording screen)
    - Share results (if implemented)
    - Exit app

---

## Network Configuration

### Local Development Setup

```
Your Computer (Laptop/Desktop)
├── FastAPI Server (Port 8000)
├── Expo Dev Server (Port 19006)
└── Mobile Device/Emulator
    └── Connects to API at http://localhost:8000
```

**Issue**: Mobile device can't reach `localhost` on your computer.

**Solution**: Use your machine's IP address:

```bash
# Get your IP address
ifconfig          # macOS/Linux
ipconfig          # Windows

# Then use in mobile app:
API_URL = 'http://192.168.1.100:8000'  # Your IP
```

### Docker Deployment

For production, containerize everything:

**docker-compose.yml**:
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - WORKERS=4
    volumes:
      - /tmp:/tmp

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
```

**Run**:
```bash
docker-compose up -d
```

---

## Testing the Integration

### Test 1: Verify API is Running

```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy",...}
```

### Test 2: Send Sample Audio

```bash
curl -X POST \
  -F "file=@breathing_sample.wav" \
  http://localhost:8000/analyze-breathing
# Expected: JSON with wheeze_probability, respiratory_rate, risk_level, guidance
```

### Test 3: Mobile App Connection

In mobile app console:
```javascript
fetch('http://your-server-ip:8000/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

---

## Deployment Checklist

### Backend Deployment

- [ ] Install Python 3.8+
- [ ] Install dependencies: `pip install -r requirements-python.txt`
- [ ] Run API server in production mode
- [ ] Configure firewall to allow port 8000
- [ ] Set up SSL/HTTPS certificate
- [ ] Configure CORS for your mobile app domain
- [ ] Enable logging and monitoring
- [ ] Test endpoints with curl/Postman
- [ ] Set up error alerting

### Mobile App Deployment

- [ ] Update API_URL to production server
- [ ] Test with real devices (not just emulator)
- [ ] Verify microphone permissions requested
- [ ] Test on both iOS and Android
- [ ] Test on slow/unreliable networks
- [ ] Add error handling for network failures
- [ ] Add timeout handling
- [ ] Test offline functionality (if applicable)
- [ ] Build and sign app for release

### Security Checklist

- [ ] Use HTTPS for API communication
- [ ] Validate file uploads (size, type, content)
- [ ] Implement rate limiting
- [ ] Add authentication if needed
- [ ] Sanitize file paths
- [ ] Clean up temporary files
- [ ] Log security events
- [ ] Regular security audits
- [ ] Keep dependencies updated

---

## Troubleshooting

### Mobile App Can't Connect to API

**Problem**: `Network request failed` or `Connection refused`

**Solutions**:
1. Verify API server is running: `curl http://localhost:8000/health`
2. Use correct IP address (not localhost)
3. Check firewall settings
4. Verify both on same network
5. Check API URL in mobile app code

### API Returns 400 Error

**Problem**: Invalid file or unsupported format

**Solutions**:
1. Ensure audio file is .wav format
2. Check file is not corrupted
3. Verify file is > 1 second
4. Check file permissions

### Slow Analysis

**Problem**: Takes > 1 second to process

**Solutions**:
1. Use shorter audio clips (5-10 seconds ideal)
2. Reduce sample rate if possible
3. Add more server resources
4. Use caching for repeated analyses

---

## Performance Optimization

### Client-Side

1. **Compress Audio**: Use MP3 format to reduce file size
2. **Cache Results**: Don't re-analyze same audio
3. **Show Progress**: Display loading indicator during upload
4. **Handle Timeouts**: Set request timeout to 30 seconds

### Server-Side

1. **Use Caching**: Cache analysis results by file hash
2. **Async Processing**: Process large batches asynchronously
3. **Database**: Store results in database instead of just returning
4. **Load Balancing**: Run multiple worker processes
5. **CDN**: Serve static files via CDN

---

## Monitoring & Logging

### Check API Logs

```bash
# View real-time logs
tail -f api_server.log

# Filter for errors
grep ERROR api_server.log

# Count requests by type
grep "POST /analyze" api_server.log | wc -l
```

### Monitor Server Health

```bash
# Check CPU/Memory usage
top

# Monitor network connections
netstat -an | grep 8000

# Check disk usage
df -h
```

---

## Next Steps

1. **Deploy Backend**: Choose hosting (AWS, GCP, Azure, etc.)
2. **Test Integration**: Verify mobile app ↔ backend communication
3. **User Testing**: Have real users test the app
4. **Collect Feedback**: Gather user feedback on usability
5. **Iterate**: Improve based on feedback
6. **Scale**: Add more features (history, sharing, etc.)
7. **Publish**: Release to App Store and Google Play

---

## Additional Resources

- **Mobile App**: See `README.md` in root directory
- **Audio Analyzer**: See `AUDIO_ANALYZER.md`
- **API Documentation**: See `API_DOCUMENTATION.md`
- **Quick Start**: See `API_QUICKSTART.md`
- **Examples**: See `example_usage.py`

---

## Support

For issues or questions:

1. Check the appropriate documentation file
2. Review example code
3. Run test suite
4. Check server logs
5. Search existing issues

---

**Created**: March 14, 2026
**Status**: Complete Integration Guide
**Ready for**: Production Deployment
