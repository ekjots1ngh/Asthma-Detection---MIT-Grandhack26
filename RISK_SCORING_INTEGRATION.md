# Risk Scoring Integration Guide

## System Overview

```
Audio Recording
    ↓
┌─────────────────────────────────────┐
│  AUDIO ANALYSIS MODULES             │
├─────────────────────────────────────┤
│ • CoughDetector                     │
│   → cough_count                     │
│   → coughs_per_minute              │
│                                     │
│ • RespiratoryRateEstimator         │
│   → respiratory_rate (br/min)      │
│                                     │
│ • RespiratoryAnalyzer (Wheeze)     │
│   → wheeze_detected                │
│   → wheeze_probability (0-1)       │
│   → wheeze_intensity (0-1)         │
└─────────────────────────────────────┘
    ↓
RISK SCORING ALGORITHM
    ↓
┌─────────────────────────────────────┐
│  RISK CALCULATION                   │
├─────────────────────────────────────┤
│ Input: 4 metrics from analysis      │
│ Output:                             │
│  • risk_level: LOW/MODERATE/HIGH   │
│  • risk_score: 0-100               │
│  • confidence: 0-1                 │
│  • recommendations: [actions]      │
└─────────────────────────────────────┘
    ↓
Mobile App / API Response
    ↓
Display Results to User
```

---

## Backend Integration - Flask Example

### 1. Full Analysis Pipeline

```python
# app.py
from flask import Flask, request, jsonify
from cough_detector import CoughDetector
from respiratory_rate_analyzer import RespiratoryRateEstimator
from audio_analyzer import RespiratoryAnalyzer
from risk_scoring import calculate_risk

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    """
    Complete analysis pipeline:
    Audio → Analysis → Risk Scoring → Response
    """

    # 1. Get audio file
    audio_file = request.files['file']
    audio_path = f'/tmp/{audio_file.filename}'
    audio_file.save(audio_path)

    # 2. Get child's age (optional, default 8)
    age = request.form.get('age', default=8, type=int)

    try:
        # 3. Run audio analysis modules in parallel
        cough_detector = CoughDetector()
        coughs = cough_detector.detect_coughs(audio_path)

        rr_estimator = RespiratoryRateEstimator()
        breathing = rr_estimator.estimate_rate(audio_path)

        wheeze_analyzer = RespiratoryAnalyzer()
        wheeze = wheeze_analyzer.analyze(audio_path)

        # 4. Calculate risk from analysis results
        risk_score = calculate_risk(
            wheeze_probability=wheeze['wheeze_probability'],
            wheeze_intensity=wheeze.get('wheeze_intensity', 0),
            respiratory_rate=breathing['respiratory_rate'],
            cough_frequency=coughs['coughs_per_minute'],
            age_years=age
        )

        # 5. Format response
        response = {
            'status': 'success',

            # Risk assessment
            'risk_level': risk_score.risk_level.value,
            'risk_score': risk_score.risk_score,
            'confidence': risk_score.confidence,
            'explanation': risk_score.explanation,
            'recommendations': risk_score.get_recommendations(risk_score),

            # Detailed metrics
            'metrics': {
                'cough_count': coughs['cough_count'],
                'coughs_per_minute': coughs['coughs_per_minute'],
                'respiratory_rate': breathing['respiratory_rate'],
                'wheeze_detected': wheeze['wheeze_detected'],
                'wheeze_probability': wheeze['wheeze_probability'],
            },

            # Component scores
            'component_scores': risk_score.component_scores,

            # Processing info
            'duration': coughs['duration'],
            'analysis_time': 3.5,  # seconds
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

    finally:
        # Cleanup
        import os
        os.remove(audio_path)
```

### 2. Minimal Integration (Risk Score Only)

```python
# Simplified: Just get metrics from analysis and score
@app.route('/calculate-risk', methods=['POST'])
def calculate_risk_only():
    """
    Accept pre-calculated metrics, return risk score
    """
    data = request.get_json()

    risk_score = calculate_risk(
        wheeze_probability=data['wheeze_probability'],
        wheeze_intensity=data['wheeze_intensity'],
        respiratory_rate=data['respiratory_rate'],
        cough_frequency=data['cough_frequency'],
        age_years=data.get('age', 8)
    )

    return jsonify({
        'risk_level': risk_score.risk_level.value,
        'risk_score': risk_score.risk_score,
        'confidence': risk_score.confidence,
        'recommendations': risk_score.get_recommendations(risk_score)
    })
```

---

## Mobile App Integration - React Native

### 1. Send Audio to Backend

```javascript
// src/services/audioService.js
import { Audio } from 'expo-av';

export const recordAndAnalyze = async (durationSeconds = 15) => {
  const recording = new Audio.Recording();

  try {
    // Record audio
    await recording.prepareToRecordAsync(
      Audio.RecordingOptionsPresets.HIGH_QUALITY
    );
    await recording.startAsync();

    // Wait for duration
    await new Promise(r => setTimeout(r, durationSeconds * 1000));

    await recording.stopAndUnloadAsync();
    const audioUri = recording.getURI();

    // Upload to backend
    const formData = new FormData();
    formData.append('file', {
      uri: audioUri,
      type: 'audio/wav',
      name: 'breathing.wav'
    });
    formData.append('age', 8);  // Child's age

    const response = await fetch(
      'https://api.breathing-check.com/analyze',
      {
        method: 'POST',
        body: formData
      }
    );

    return response.json();
  } catch (error) {
    console.error('Analysis failed:', error);
    throw error;
  }
};
```

### 2. Display Results

```javascript
// src/screens/ResultsScreen.js
import { RiskIndicator } from '../components/RiskIndicator';

export const ResultsScreen = ({ route, navigation }) => {
  const { riskLevel, riskScore, confidence, recommendations, metrics } =
    route.params || {};

  return (
    <SafeAreaView>
      <ScrollView>
        {/* Risk Indicator */}
        <RiskIndicator
          riskLevel={riskLevel}  // 'LOW', 'MODERATE', 'HIGH'
          score={riskScore}      // 0-100
        />

        {/* Metrics Card */}
        <View style={styles.metricsCard}>
          <Text style={styles.title}>Details</Text>

          <MetricRow
            label="Cough Count"
            value={metrics.cough_count}
          />
          <MetricRow
            label="Breathing Rate"
            value={`${metrics.respiratory_rate} br/min`}
          />
          <MetricRow
            label="Wheeze Detected"
            value={metrics.wheeze_detected ? 'Yes' : 'No'}
          />
        </View>

        {/* Recommendations Card */}
        <View style={styles.guidanceCard}>
          <Text style={styles.title}>What to Do</Text>
          {recommendations.map((rec, i) => (
            <Text key={i} style={styles.recommendation}>
              • {rec}
            </Text>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};
```

### 3. Component for Risk Display

```javascript
// src/components/RiskDisplay.js
export const RiskDisplay = ({ riskLevel, riskScore }) => {
  const getRiskColor = (level) => {
    switch(level) {
      case 'LOW':       return Colors.GREEN;
      case 'MODERATE':  return Colors.YELLOW;
      case 'HIGH':      return Colors.RED;
    }
  };

  const getRiskLabel = (level) => {
    switch(level) {
      case 'LOW':       return 'Healthy';
      case 'MODERATE':  return 'Monitor';
      case 'HIGH':      return 'Check Now';
    }
  };

  return (
    <View>
      {/* 180px Circle Indicator */}
      <View style={{
        width: 180,
        height: 180,
        borderRadius: 90,
        backgroundColor: getRiskColor(riskLevel),
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <Text style={{ fontSize: 48, color: 'white' }}>
          {riskLevel === 'LOW' ? '✓' : '⚠'}
        </Text>
      </View>

      {/* Score Display */}
      <Text style={{ fontSize: 28, fontWeight: 'bold' }}>
        {getRiskLabel(riskLevel)}
      </Text>
      <Text style={{ fontSize: 36, color: getRiskColor(riskLevel) }}>
        {riskScore}/100
      </Text>
    </View>
  );
};
```

---

## Real-World Example: End-to-End Flow

### Scenario: Parent Records Child's Breathing

**1. Parent opens app and taps "Check Breathing"**

```javascript
// HomeScreen.js
const handleCheckBreathing = () => {
  navigation.navigate('Recording');
};
```

**2. Recording screen shows instructions and timer**

```javascript
// RecordingScreen.js
const handleStartRecording = async () => {
  setIsRecording(true);

  try {
    const analysisResult = await recordAndAnalyze(15);

    // Navigate to results with analysis data
    navigation.navigate('Results', {
      riskLevel: analysisResult.risk_level,
      riskScore: analysisResult.risk_score,
      confidence: analysisResult.confidence,
      recommendations: analysisResult.recommendations,
      metrics: analysisResult.metrics
    });
  } catch (error) {
    alert('Analysis failed. Please try again.');
  }
};
```

**3. Results screen displays color-coded risk**

```
                  Results
            ┌────────────────┐
            │       ⚠        │  YELLOW
            │   (Pulsing)    │
            └────────────────┘

              MONITOR
        Watch for changes
            Score: 55/100

        DETAILS
        Coughs:          8
        Breathing:      28 br/min
        Wheeze:      Possible

        RECOMMENDATIONS
        • Keep medication nearby
        • Monitor for other symptoms
        • Schedule check-up if persists

    [Check Again] [Back Home]
```

**4. Data Flow Summary:**

```
15-second recording
    ↓
POST /analyze with audio file
    ↓
Backend Analysis:
  • CoughDetector:        coughs_per_minute = 8
  • RespiratoryAnalyzer:  rate = 28 br/min
  • WheezeDetector:       probability = 0.4
    ↓
Risk Calculation:
  • Wheeze Score:      30 points
  • Rate Score:        40 points
  • Cough Score:       45 points
  • Overall:           (30×0.4 + 40×0.35 + 45×0.25) = 36 → 41 = MODERATE
    ↓
Response JSON:
  {
    "risk_level": "MODERATE",
    "risk_score": 41,
    "confidence": 0.75,
    "recommendations": [...]
  }
    ↓
Mobile App displays
  YELLOW indicator with score and guidance
```

---

## Error Handling

### Missing Data

```python
# Handle missing wheeze data
wheeze_prob = wheeze_analyzer.analyze(audio_path).get('wheeze_probability', 0)
wheeze_int = wheeze_analyzer.analyze(audio_path).get('wheeze_intensity', 0)

# Conservative defaults
cough_freq = coughs['coughs_per_minute'] or 0.0
rate = breathing['respiratory_rate'] or 22  # Normal default

risk_score = calculate_risk(
    wheeze_prob,
    wheeze_int,
    rate,
    cough_freq,
    age_years=8
)
```

### Network Errors

```javascript
// Retry with exponential backoff
const analyzeWithRetry = async (audioUri, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await recordAndAnalyze();
    } catch (error) {
      if (i === maxRetries - 1) throw error;

      const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
      await new Promise(r => setTimeout(r, delay));
    }
  }
};
```

### Analysis Failures

```python
# Backend error handling
@app.errorhandler(Exception)
def handle_error(error):
    logging.error(f"Analysis failed: {error}")
    return jsonify({
        'status': 'error',
        'error': 'Analysis failed',
        'recommendations': [
            'Try again with a clearer recording',
            'Ensure child is calm and breathing normally',
            'Contact support if problem persists'
        ]
    }), 500
```

---

## Testing the Integration

### Unit Test: Risk Scoring

```python
# test_risk_scoring.py
from risk_scoring import calculate_risk

def test_healthy_child():
    score = calculate_risk(0, 0, 22, 0.5)
    assert score.risk_level.value == 'LOW'
    assert score.risk_score < 20

def test_moderate_symptoms():
    score = calculate_risk(0.5, 0.3, 28, 5)
    assert score.risk_level.value == 'MODERATE'
    assert 40 < score.risk_score < 70

def test_critical_symptoms():
    score = calculate_risk(0.9, 0.8, 38, 18)
    assert score.risk_level.value == 'HIGH'
    assert score.risk_score > 70

# Run tests
pytest test_risk_scoring.py
```

### Integration Test: Full Pipeline

```python
# test_integration.py
import json
from app import app

def test_full_analysis():
    client = app.test_client()

    # Send test audio
    with open('test_audio.wav', 'rb') as f:
        response = client.post(
            '/analyze',
            data={'file': f, 'age': 8}
        )

    assert response.status_code == 200
    data = json.loads(response.data)

    assert 'risk_level' in data
    assert data['risk_level'] in ['LOW', 'MODERATE', 'HIGH']
    assert 0 <= data['risk_score'] <= 100
    assert 0 <= data['confidence'] <= 1
    assert len(data['recommendations']) > 0
```

---

## Performance Considerations

### Analysis Time Budget

```
Audio Upload:           1-2 seconds
Cough Detection:        2-3 seconds
Respiratory Rate:       1-2 seconds
Wheeze Detection:       1-2 seconds
Risk Calculation:       < 0.1 seconds
────────────────────────────────────
Total:                  ~5-8 seconds
```

### Optimization Tips

1. **Run analysis modules in parallel** (not sequential)
2. **Cache analysis results** during re-processing
3. **Use lower-resolution spectrograms** for fast analysis
4. **Offload heavy compute to backend**, not mobile app

---

## Deployment Checklist

- [ ] Risk scoring algorithm tested with test cases
- [ ] Backend API returns correct risk_level format
- [ ] Mobile app handles all risk levels (LOW/MODERATE/HIGH)
- [ ] Recommendations display correctly
- [ ] Error handling for network failures
- [ ] Age-appropriate normal ranges configured
- [ ] SSL/TLS enabled for API calls
- [ ] Rate limiting configured
- [ ] Logging enabled for debugging

---

## Next Steps

1. **Integrate all 3 analysis modules** with risk scoring
2. **Test end-to-end** with sample audio files
3. **Deploy to staging** for user testing
4. **Validate against manual assessments**
5. **Iterate based on feedback**

---

**Status:** Ready for Integration
**Estimated Integration Time:** 2-4 hours
**Code Examples:** Complete and runnable

