# FastAPI Backend - Quick Start Guide

Get the respiratory screening API up and running in minutes.

## 1. Install Dependencies

```bash
pip install -r requirements-python.txt
```

Or manually:
```bash
pip install fastapi uvicorn python-multipart requests
pip install numpy scipy librosa
```

## 2. Start the API Server

```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

## 3. Test the API

In a new terminal:

```bash
# Check health
curl http://localhost:8000/health

# Get API info
curl http://localhost:8000/info

# Test analysis with sample audio
python test_api_client.py
```

## 4. Interactive API Documentation

Open your browser and visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test endpoints directly in the browser!

## 5. Use the API

### Python Example
```python
import requests

# Upload and analyze
with open('breathing.wav', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/analyze-breathing',
        files={'file': f}
    )

results = response.json()
print(f"Risk Level: {results['risk_level']}")
print(f"Message: {results['guidance']['message']}")
```

### JavaScript/React Native Example
```javascript
const formData = new FormData();
formData.append('file', audioBlob, 'breathing.wav');

const response = await fetch('http://localhost:8000/analyze-breathing', {
  method: 'POST',
  body: formData
});

const results = await response.json();
console.log(`Risk: ${results.risk_level}`);
```

### cURL Example
```bash
curl -X POST \
  -F "file=@breathing.wav" \
  http://localhost:8000/analyze-breathing
```

## 6. Endpoints Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check API status |
| GET | `/info` | API information |
| GET | `/risk-levels` | Risk level definitions |
| POST | `/analyze-breathing` | Analyze single audio file |
| POST | `/batch-analyze` | Analyze multiple files |

## 7. Response Format

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

## 8. Production Deployment

### Using Gunicorn + Uvicorn

```bash
pip install gunicorn

gunicorn api_server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Using Docker

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements-python.txt .
RUN pip install --no-cache-dir -r requirements-python.txt

# Copy code
COPY api_server.py audio_analyzer.py ./

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run**:
```bash
docker build -t respiratory-api .
docker run -p 8000:8000 respiratory-api
```

## Troubleshooting

### Port Already in Use
```bash
# Use different port
uvicorn api_server:app --port 8001
```

### Module Not Found
```bash
# Make sure you're in the right directory
cd /path/to/Asthma-Detection---MIT-Grandhack26

# Install dependencies again
pip install -r requirements-python.txt
```

### Can't Connect from Mobile App
- Make sure API is accessible from mobile device
- Use actual IP address instead of localhost
- Check firewall settings
- Ensure same network or proper tunneling

### Analysis Fails with "librosa not found"
```bash
pip install librosa --upgrade
```

## Next Steps

1. **Read Full Documentation**: See `API_DOCUMENTATION.md`
2. **Review Code**: Check `api_server.py`
3. **Run Test Suite**: Execute `python test_api_client.py`
4. **Integrate with Mobile App**: Use examples in documentation
5. **Deploy to Production**: Follow deployment section above

## Key Files

- `api_server.py` - FastAPI application (main backend)
- `audio_analyzer.py` - Audio analysis engine
- `test_api_client.py` - API test suite
- `API_DOCUMENTATION.md` - Comprehensive documentation
- `requirements-python.txt` - Python dependencies

## Support

For more help:
- Check `API_DOCUMENTATION.md` for detailed endpoint documentation
- Review `example_usage.py` for analysis examples
- Run `python test_api_client.py` to verify setup
- Check server logs for error messages

---

**Ready to go!** 🚀
