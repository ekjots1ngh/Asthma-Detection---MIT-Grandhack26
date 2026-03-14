# Respiratory Screening API - Documentation

Complete REST API for respiratory audio analysis and wheeze detection using FastAPI.

## Overview

The Respiratory Screening API provides endpoints for:
- **Single file analysis**: Upload and analyze breathing audio files
- **Batch processing**: Analyze multiple files in one request
- **Health monitoring**: Check API status and get configuration info
- **Risk assessment**: Receive clinical guidance based on analysis results

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

```bash
# Install dependencies
pip install -r requirements-python.txt

# Or install specific packages
pip install fastapi uvicorn python-multipart requests
```

## Running the Server

### Development Mode (with auto-reload)

```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements-python.txt .
RUN pip install -r requirements-python.txt
COPY . .
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## API Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Description**: Check if the API server is running and healthy.

**Response**:
```json
{
  "status": "healthy",
  "service": "respiratory-screening-api",
  "version": "1.0.0"
}
```

**Example**:
```bash
curl http://localhost:8000/health
```

---

### 2. Analyze Single Breathing File

**Endpoint**: `POST /analyze-breathing`

**Description**: Upload and analyze a single breathing audio file.

**Request**:
- **Content-Type**: multipart/form-data
- **Parameter**: `file` (binary audio file)

**Supported Audio Formats**:
- `.wav` (WAV)
- `.mp3` (MPEG-3)
- `.flac` (FLAC)
- `.ogg` (OGG Vorbis)
- `.m4a` (M4A)

**Response** (Status 200):
```json
{
  "wheeze_probability": 0.45,
  "respiratory_rate": 22,
  "risk_level": "medium",
  "guidance": {
    "title": "Possible Wheezing",
    "message": "Possible wheezing detected. Monitor symptoms.",
    "recommendation": "Keep monitoring symptoms. Consider scheduling a healthcare provider consultation if symptoms persist.",
    "emoji": "⚠"
  },
  "metrics": {
    "wheeze_intensity": 0.32
  }
}
```

**Error Responses**:

- **400 Bad Request**: Invalid file or missing file
```json
{
  "detail": "Invalid file type. Supported formats: .wav, .mp3, .flac, .ogg, .m4a"
}
```

- **500 Internal Server Error**: Analysis failure
```json
{
  "detail": "An unexpected error occurred during analysis"
}
```

**Example - Python Requests**:
```python
import requests

with open('breathing_sample.wav', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/analyze-breathing',
        files=files
    )

results = response.json()
print(f"Risk Level: {results['risk_level']}")
print(f"Guidance: {results['guidance']['message']}")
```

**Example - cURL**:
```bash
curl -X POST \
  -F "file=@breathing_sample.wav" \
  http://localhost:8000/analyze-breathing
```

**Example - JavaScript/Fetch**:
```javascript
const formData = new FormData();
formData.append('file', audioBlob, 'breathing.wav');

const response = await fetch('http://localhost:8000/analyze-breathing', {
  method: 'POST',
  body: formData
});

const results = await response.json();
console.log(`Risk Level: ${results.risk_level}`);
```

---

### 3. Batch Analyze Multiple Files

**Endpoint**: `POST /batch-analyze`

**Description**: Upload and analyze multiple breathing audio files at once.

**Constraints**:
- Maximum 10 files per request
- Each file must be valid audio format

**Request**:
- **Content-Type**: multipart/form-data
- **Parameter**: `files` (multiple binary audio files)

**Response** (Status 200):
```json
{
  "results": [
    {
      "filename": "clear_breathing.wav",
      "wheeze_probability": 0.15,
      "respiratory_rate": 20,
      "risk_level": "low",
      "guidance": {
        "title": "Clear Breathing",
        "message": "Clear breathing. Continue monitoring."
      }
    },
    {
      "filename": "wheezy_breathing.wav",
      "wheeze_probability": 0.65,
      "respiratory_rate": 28,
      "risk_level": "high",
      "guidance": {
        "title": "Concerning Wheezing",
        "message": "Concerning wheezing detected. Consider using rescue inhaler or seeking care."
      }
    }
  ]
}
```

**Example - Python**:
```python
import requests

files = [
    ('files', open('sample1.wav', 'rb')),
    ('files', open('sample2.wav', 'rb')),
    ('files', open('sample3.wav', 'rb')),
]

response = requests.post(
    'http://localhost:8000/batch-analyze',
    files=files
)

batch_results = response.json()
for result in batch_results['results']:
    print(f"{result['filename']}: {result['risk_level']}")
```

---

### 4. Get API Information

**Endpoint**: `GET /info`

**Description**: Get detailed information about the API, supported formats, and output fields.

**Response**:
```json
{
  "api_name": "Respiratory Screening API",
  "version": "1.0.0",
  "description": "Analyzes breathing audio for asthma screening",
  "endpoints": {
    "health_check": "/health",
    "analyze_single": "/analyze-breathing",
    "analyze_batch": "/batch-analyze",
    "info": "/info"
  },
  "supported_formats": [".wav", ".mp3", ".flac", ".ogg", ".m4a"],
  "max_file_size_mb": 50,
  "max_batch_files": 10,
  "output_fields": {
    "wheeze_probability": "float (0-1)",
    "respiratory_rate": "int (breaths/min)",
    "risk_level": "str (low/medium/high)",
    "guidance": "dict with title, message, recommendation",
    "metrics": "dict with wheeze_intensity"
  }
}
```

---

### 5. Get Risk Levels Information

**Endpoint**: `GET /risk-levels`

**Description**: Get information about risk level classifications and guidance messages.

**Response**:
```json
{
  "risk_levels": {
    "low": {
      "title": "Clear Breathing",
      "message": "Clear breathing. Continue monitoring.",
      "recommendation": "No immediate action needed. Continue regular check-ups.",
      "emoji": "✓"
    },
    "medium": {
      "title": "Possible Wheezing",
      "message": "Possible wheezing detected. Monitor symptoms.",
      "recommendation": "Keep monitoring symptoms. Consider scheduling a healthcare provider consultation if symptoms persist.",
      "emoji": "⚠"
    },
    "high": {
      "title": "Concerning Wheezing",
      "message": "Concerning wheezing detected. Consider using rescue inhaler or seeking care.",
      "recommendation": "Seek medical attention. Consider using rescue inhaler if available. Contact healthcare provider promptly.",
      "emoji": "⚠⚠"
    }
  },
  "descriptions": {
    "low": "Clear breathing detected - no immediate concerns",
    "medium": "Possible wheezing detected - monitor and consider consultation",
    "high": "Concerning wheezing detected - seek medical attention"
  }
}
```

---

## Response Fields

### Analysis Output

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `wheeze_probability` | float | 0.0-1.0 | Probability that wheeze is present (0-100%) |
| `respiratory_rate` | int | 12-60 | Estimated breaths per minute |
| `risk_level` | string | low/medium/high | Clinical risk assessment |
| `wheeze_intensity` | float | 0.0-1.0 | Strength of detected wheeze (0-100%) |

### Guidance Object

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Short title for the risk level |
| `message` | string | Main guidance message for the patient |
| `recommendation` | string | Recommended actions or follow-up |
| `emoji` | string | Visual indicator (✓, ⚠, ⚠⚠) |

---

## Risk Levels

### Low Risk (✓)
- **Characteristics**: Clear breathing detected
- **Message**: "Clear breathing. Continue monitoring."
- **Recommendation**: No immediate action needed. Continue regular check-ups.
- **Action**: Routine monitoring

### Medium Risk (⚠)
- **Characteristics**: Possible wheezing detected
- **Message**: "Possible wheezing detected. Monitor symptoms."
- **Recommendation**: Keep monitoring symptoms. Consider scheduling a healthcare provider consultation if symptoms persist.
- **Action**: Monitor closely, schedule appointment if symptoms persist

### High Risk (⚠⚠)
- **Characteristics**: Concerning wheezing detected
- **Message**: "Concerning wheezing detected. Consider using rescue inhaler or seeking care."
- **Recommendation**: Seek medical attention. Consider using rescue inhaler if available. Contact healthcare provider promptly.
- **Action**: Seek immediate medical attention

---

## Usage Examples

### Example 1: Basic Single File Analysis

```python
#!/usr/bin/env python3
import requests
import json

def analyze_breathing(audio_file_path, api_url='http://localhost:8000'):
    """Analyze a breathing audio file."""

    with open(audio_file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f'{api_url}/analyze-breathing',
            files=files
        )

    if response.status_code == 200:
        results = response.json()
        print(json.dumps(results, indent=2))
        return results
    else:
        print(f'Error: {response.status_code}')
        print(response.json())

# Usage
results = analyze_breathing('breathing_sample.wav')
print(f"\nRisk Level: {results['risk_level'].upper()}")
print(f"Guidance: {results['guidance']['message']}")
```

### Example 2: Batch Processing with Results Summary

```python
#!/usr/bin/env python3
import requests
from pathlib import Path

def batch_analyze(directory_path, api_url='http://localhost:8000'):
    """Analyze all audio files in a directory."""

    audio_files = list(Path(directory_path).glob('*.wav'))

    files = [('files', open(f, 'rb')) for f in audio_files]
    response = requests.post(f'{api_url}/batch-analyze', files=files)

    # Close files
    for _, f in files:
        f.close()

    if response.status_code == 200:
        batch_results = response.json()

        # Print summary
        print(f"\nAnalyzed {len(batch_results['results'])} files:")
        print('-' * 60)

        for result in batch_results['results']:
            risk = result['risk_level'].upper()
            prob = result['wheeze_probability']
            name = result['filename']
            print(f"{name:30} Risk: {risk:6} Prob: {prob:.0%}")

        return batch_results
    else:
        print(f'Error: {response.status_code}')

# Usage
batch_analyze('./audio_samples/')
```

### Example 3: Integrate with Mobile App Backend

```python
#!/usr/bin/env python3
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import requests

router = APIRouter()

@router.post('/screen-breathing')
async def screen_breathing(file: UploadFile = File(...)):
    """Wrapper endpoint for mobile app."""

    # Save file temporarily
    contents = await file.read()
    with open(f'/tmp/{file.filename}', 'wb') as f:
        f.write(contents)

    # Forward to analysis API
    with open(f'/tmp/{file.filename}', 'rb') as f:
        api_response = requests.post(
            'http://localhost:8000/analyze-breathing',
            files={'file': f}
        )

    if api_response.status_code == 200:
        results = api_response.json()

        # Add app-specific fields
        results['app_version'] = '1.0.0'
        results['timestamp'] = datetime.now().isoformat()

        return JSONResponse(content=results)
    else:
        return JSONResponse(
            status_code=500,
            content={'error': 'Analysis failed'}
        )
```

---

## Testing

### Run API Tests

```bash
# Terminal 1: Start the server
uvicorn api_server:app --reload

# Terminal 2: Run tests
python test_api_client.py
```

### Test Suite Includes

1. **Single File Analysis** - Analyze different breathing patterns
2. **Multiple Recordings** - Compare clear, moderate, and severe wheeze
3. **Batch Analysis** - Process multiple files efficiently
4. **API Information** - Verify endpoints and configuration
5. **Error Handling** - Test invalid inputs and error responses

---

## Performance & Limits

### Processing Time
- **Typical Duration**: 100-200ms per file
- **Network Latency**: Add 100-500ms depending on connection
- **Total Latency**: 200-700ms per analysis

### Limits
- **Max File Size**: 50 MB
- **Max Batch Files**: 10 files per request
- **Concurrent Requests**: Limited by server resources
- **Audio Duration**: Recommended 5-10 seconds

### Optimization Tips

1. **Use Batch Analysis** for multiple files
   - More efficient than sequential uploads
   - Single HTTP connection

2. **Cache Results** for repeated analyses
   - Avoid re-uploading same audio
   - Store results locally

3. **Compress Audio** before upload
   - Use MP3 format for smaller files
   - Reduces network bandwidth

---

## CORS & Security

### Cross-Origin Resource Sharing (CORS)

Currently configured to allow all origins:
```python
allow_origins=['*']
```

**For Production**, restrict to specific origins:
```python
allow_origins=[
    'https://app.example.com',
    'https://www.example.com',
]
```

### Security Best Practices

1. **Use HTTPS** in production
2. **Validate Audio Files** before processing
3. **Set Rate Limits** to prevent abuse
4. **Add Authentication** if needed (API keys)
5. **Log & Monitor** all requests

---

## Integration with React Native Mobile App

### Step 1: Upload Audio from Mobile

```javascript
// Recording.js - React Native
async function uploadAudio(audioUri) {
  const formData = new FormData();
  formData.append('file', {
    uri: audioUri,
    type: 'audio/wav',
    name: 'breathing.wav',
  });

  const response = await fetch(
    'http://your-api-server.com/analyze-breathing',
    {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );

  const results = await response.json();
  return results;
}
```

### Step 2: Display Results in App

```javascript
// Results.js - React Native
function ResultsScreen({ results }) {
  const getRiskColor = (risk) => {
    switch (risk) {
      case 'low': return '#4CAF50';      // Green
      case 'medium': return '#FFC107';   // Yellow
      case 'high': return '#F44336';     // Red
      default: return '#999';
    }
  };

  return (
    <View style={{ backgroundColor: getRiskColor(results.risk_level) }}>
      <Text>{results.guidance.title}</Text>
      <Text>{results.guidance.message}</Text>
      <Text>{results.guidance.recommendation}</Text>
    </View>
  );
}
```

---

## Troubleshooting

### API Won't Start

**Error**: `Address already in use`

**Solution**: Change port or kill existing process
```bash
# Use different port
uvicorn api_server:app --port 8001

# Or kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### File Upload Fails

**Error**: `413 Request Entity Too Large`

**Solution**: Increase upload size limit
```python
from fastapi import FastAPI

app = FastAPI()
# Default is 25MB, increase to 50MB
app.add_middleware(...)
```

### Analysis Times Out

**Error**: Timeout waiting for response

**Solutions**:
1. Check if server is running
2. Increase timeout on client
3. Use shorter audio clips
4. Check server logs for errors

### CORS Issues

**Error**: `Access to XMLHttpRequest blocked by CORS`

**Solution**: Add allowed origins
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://your-app.com'],
    allow_credentials=True,
    allow_methods=['POST', 'GET'],
    allow_headers=['*'],
)
```

---

## API Monitoring

### View Server Logs

```bash
# With timestamps and log level
uvicorn api_server:app --log-level debug

# Filter by level
tail -f api_server.log | grep ERROR
```

### Health Check Script

```bash
#!/bin/bash
# Check API health every 30 seconds
while true; do
  response=$(curl -s http://localhost:8000/health)
  timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$timestamp] $response"
  sleep 30
done
```

---

## Version History

### v1.0.0 (Current)
- Initial release
- Single and batch file analysis
- Risk level classification
- Comprehensive API documentation
- Full test suite

---

## Support & Contact

For questions or issues:
1. Check the troubleshooting section above
2. Run the test suite: `python test_api_client.py`
3. Review the source code: `api_server.py`
4. Check server logs for detailed error messages

---

**Last Updated**: March 14, 2026
**Status**: Production Ready
