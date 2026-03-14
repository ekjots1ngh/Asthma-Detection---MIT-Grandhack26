# Respiratory Audio Analyzer - Wheeze Detection

A Python module for analyzing respiratory audio recordings and detecting wheezing patterns using FFT frequency analysis.

## Overview

The `RespiratoryAnalyzer` class provides comprehensive analysis of breathing sounds to detect asthma symptoms and assess respiratory health risk. It uses digital signal processing techniques including:

- **FFT Frequency Analysis**: Analyzes audio in the 100-1000 Hz wheeze frequency range
- **Spectral Analysis**: Detects concentrated energy patterns characteristic of wheezing
- **Breathing Rate Estimation**: Extracts respiratory rate from audio envelope
- **Risk Classification**: Provides actionable risk levels (low/medium/high)

## Installation

Install required dependencies:

```bash
pip install -r requirements-python.txt
```

Dependencies:
- `numpy` - Numerical computations
- `scipy` - Signal processing and FFT
- `librosa` - Audio loading and analysis

## Quick Start

### Basic Usage

```python
from audio_analyzer import analyze_breathing

# Analyze a breathing audio file
results = analyze_breathing('breathing_sample.wav')

# Results contain:
print(results)
# {
#   'wheeze_probability': 0.45,      # 0-1 (0% to 100%)
#   'wheeze_intensity': 0.32,        # 0-1 (0% to 100%)
#   'respiratory_rate': 22,          # breaths per minute
#   'risk_level': 'medium'           # 'low', 'medium', or 'high'
# }
```

### Using the RespiratoryAnalyzer Class

```python
from audio_analyzer import RespiratoryAnalyzer

# Create analyzer
analyzer = RespiratoryAnalyzer(sr=22050)

# Analyze audio file
results = analyzer.analyze('breathing_sample.wav')

# Access individual metrics
probability = results['wheeze_probability']
intensity = results['wheeze_intensity']
respiratory_rate = results['respiratory_rate']
risk_level = results['risk_level']
```

## Output Format

The analyzer returns a dictionary with four key metrics:

```python
{
    'wheeze_probability': float (0.0 to 1.0),
    'wheeze_intensity': float (0.0 to 1.0),
    'respiratory_rate': int (breaths per minute),
    'risk_level': str ('low', 'medium', or 'high')
}
```

### Metrics Explanation

**wheeze_probability** (0-1)
- Likelihood that wheezing is present in the audio
- Based on energy distribution in wheeze frequency band
- Considers spectral concentration and presence of peaks

**wheeze_intensity** (0-1)
- Strength/prominence of detected wheeze patterns
- Calculated from peak magnitude and spectral energy
- Higher values indicate more pronounced wheezing

**respiratory_rate** (breaths/min)
- Estimated number of breaths per minute
- Detected from breathing envelope using STFT
- Validated to physiological range: 12-60 breaths/min

**risk_level** (low/medium/high)
- Clinical risk assessment based on combined metrics
- Low Risk: < 25% combined wheeze score
- Medium Risk: 25-50% combined wheeze score
- High Risk: > 50% combined wheeze score

## Technical Details

### Frequency Analysis

The analyzer focuses on wheeze frequencies between **100 Hz and 1000 Hz**, which is the typical range where asthma-related wheezing occurs:

- **100-250 Hz**: Low-frequency components of breathing
- **250-500 Hz**: Common wheeze range
- **500-1000 Hz**: High-frequency wheeze harmonics

### Signal Processing Pipeline

1. **Audio Loading**: Loaded at 22050 Hz sample rate (sufficient for wheeze detection)

2. **Preprocessing**:
   - High-pass filter at 50 Hz to remove DC and low-frequency noise
   - Amplitude normalization

3. **Frequency Analysis**:
   - Hamming window applied to reduce spectral leakage
   - FFT computed for full spectrum
   - Savitzky-Golay filter applied to smooth magnitude spectrum

4. **Wheeze Detection**:
   - Extract magnitudes in 100-1000 Hz range
   - Calculate probability based on:
     - Energy ratio in wheeze band
     - Spectral concentration (peak vs mean)
     - Spectral sharpness (number of peaks)

5. **Breathing Rate Estimation**:
   - Compute STFT to get energy envelope
   - Analyze frequency domain of envelope
   - Find dominant frequency in 0.2-0.8 Hz range (12-48 BPM)
   - Validate within physiological bounds (12-60 BPM)

## Testing

Run the comprehensive test suite:

```bash
python test_audio_analyzer.py
```

This includes:
- Test on clear breathing audio (low risk)
- Test on moderate wheeze audio (medium risk)
- Test on severe wheeze audio (high risk)
- Output format validation
- Feature demonstration

### Creating Test Audio

The test module includes utilities to create synthetic test audio:

```python
from test_audio_analyzer import (
    create_clear_breathing_audio,
    create_test_audio,
    create_severe_wheeze_audio
)

# Create test files
create_clear_breathing_audio('clear.wav')
create_test_audio('moderate.wav')
create_severe_wheeze_audio('severe.wav')
```

## Integration with Mobile App

The analyzer can be integrated with the React Native mobile app:

```python
# In a Python backend service
from audio_analyzer import analyze_breathing
import json

def analyze_recording(audio_file_path):
    """Backend endpoint to analyze breathing recording"""
    results = analyze_breathing(audio_file_path)
    return json.dumps(results)
```

Then call from the mobile app:

```javascript
// React Native code
const results = await fetch('/api/analyze', {
  method: 'POST',
  body: formData  // Contains WAV file
})
const analysis = await results.json()

// Use results:
// analysis.risk_level -> Display color coding
// analysis.wheeze_probability -> Show confidence
// analysis.respiratory_rate -> Display metric
```

## Performance Considerations

- **Audio Duration**: Works best with 5-10 second recordings
- **Sample Rate**: Automatically resampled to 22050 Hz
- **Latency**: ~100-200ms for 10-second recording on modern CPU
- **Memory**: ~50MB for typical usage

## Limitations & Future Improvements

### Current Limitations

- Trained on synthetic audio patterns
- Works best for clear recording conditions
- May need calibration for different microphone types
- Does not distinguish between wheeze types

### Future Improvements

- Machine learning classification (CNN/LSTM)
- Support for real recorded breathing audio
- Wheeze subtype classification (stridor, rhonchi, etc.)
- Temporal analysis of wheeze patterns
- Environmental noise filtering

## API Reference

### RespiratoryAnalyzer

```python
class RespiratoryAnalyzer:
    def __init__(self, sr: int = 22050):
        """Initialize analyzer with sample rate"""

    def analyze(self, audio_path: str) -> Dict:
        """Analyze audio file and return results"""

    def _detect_wheeze(self, y: np.ndarray, sr: int) -> tuple:
        """Detect wheeze patterns in audio"""

    def _estimate_respiratory_rate(self, y: np.ndarray, sr: int) -> float:
        """Estimate breathing rate"""
```

### Helper Function

```python
def analyze_breathing(audio_path: str) -> Dict:
    """Convenience function to analyze audio"""
```

## Usage Examples

### Example 1: Analyze Single File

```python
from audio_analyzer import analyze_breathing

results = analyze_breathing('patient_sample.wav')

if results['risk_level'] == 'high':
    print("⚠️  High risk - recommend medical consultation")
elif results['risk_level'] == 'medium':
    print("⚠️  Medium risk - monitor closely")
else:
    print("✓ Clear breathing - no immediate concern")
```

### Example 2: Batch Analysis

```python
from audio_analyzer import analyze_breathing
import os
import csv

# Analyze multiple files
audio_dir = './breathing_samples/'
results = []

for filename in os.listdir(audio_dir):
    if filename.endswith('.wav'):
        path = os.path.join(audio_dir, filename)
        analysis = analyze_breathing(path)
        analysis['filename'] = filename
        results.append(analysis)

# Save results
with open('analysis_results.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
```

### Example 3: Real-time Monitoring

```python
from audio_analyzer import RespiratoryAnalyzer
import sounddevice as sd
import numpy as np

analyzer = RespiratoryAnalyzer()
sr = 22050

# Record 10 seconds
audio = sd.rec(int(10 * sr), samplerate=sr, channels=1)
sd.wait()

# Analyze
results = analyzer.analyze_array(audio.flatten(), sr)
print(f"Risk Level: {results['risk_level']}")
```

## Troubleshooting

### Issue: Low wheeze detection on real audio

**Solution**: Real recordings may require model calibration. Check:
- Audio quality and noise levels
- Microphone placement on stethoscope
- Sample rate compatibility

### Issue: Incorrect respiratory rate

**Solution**: Rate estimate depends on clear breathing envelope:
- Ensure audio captures full breath cycles
- Record in quiet environment
- Validate with manual count

### Issue: Memory errors on long recordings

**Solution**: Process in chunks:
```python
import librosa

# Load in chunks
chunk_size = 10 * sr
for start in range(0, len(audio), chunk_size):
    chunk = audio[start:start+chunk_size]
    results = analyzer.analyze_array(chunk, sr)
```

## License

This audio analyzer is part of the Asthma Detection application developed for MIT Grandhack 2026.

## References

- Breathing sounds classification: Gavriely & Caliham, 1991
- Wheeze detection techniques: Pasterkamp et al., 1997
- FFT analysis of respiratory sounds: Yadollahi & Moussavi, 2006
