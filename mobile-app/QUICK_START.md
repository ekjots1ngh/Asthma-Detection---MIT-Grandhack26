# Quick Start Guide - Breathing Check App

## 5-Minute Setup

### 1. Install Expo CLI
```bash
npm install -g expo-cli
```

### 2. Install Dependencies
```bash
cd mobile-app
npm install
```

### 3. Start Development Server
```bash
expo start
```

### 4. Run on Device/Simulator
```bash
# iOS Simulator
i

# Android Emulator
a

# Web (testing)
w

# Scan QR code with Expo app
```

---

## App Structure at a Glance

```
Home Screen
  ↓ Check Breathing button
Recording Screen
  ↓ 15 second recording
Results Screen
  ↓ Green/Yellow/Red indicator
  ↓ Check Again → back to Recording
```

---

## Key Files to Modify

### Add Your Logo/Icons
Replace in `assets/`:
- `icon.png` - App icon (1024x1024)
- `splash.png` - Splash screen (1242x2436)
- `adaptive-icon.png` - Android icon

### Connect to Backend
Edit `src/services/analysisService.js`:
```javascript
const API_URL = 'YOUR_API_ENDPOINT';

const analyzeBreathing = async (audioUri) => {
  const response = await fetch(API_URL + '/analyze', {
    method: 'POST',
    body: formData
  });
  return response.json();
};
```

### Customize Colors
Edit `src/theme.js`:
```javascript
export const Colors = {
  GREEN: '#10B981',    // Healthy
  YELLOW: '#F59E0B',   // Monitor
  RED: '#EF4444',      // Critical
};
```

---

## Common Tasks

### Add New Screen
```javascript
// 1. Create src/screens/NewScreen.js
export const NewScreen = ({ navigation }) => {
  return (
    <SafeAreaView>
      {/* Your content */}
    </SafeAreaView>
  );
};

// 2. Add to src/navigation/RootNavigator.js
<Stack.Screen name="New" component={NewScreen} />

// 3. Navigate from another screen
navigation.navigate('New');
```

### Test on Real Device
```bash
# 1. Install Expo app on phone
# 2. Run: expo start
# 3. Scan QR code with phone camera
```

### Build for App Store
```bash
# iOS TestFlight
expo build:ios

# Google Play
expo build:android

# Follow Expo's cloud build process
```

---

## Integration with Python Backend

### Send Audio to Analysis
```javascript
const sendAudioForAnalysis = async (audioUri) => {
  const formData = new FormData();
  formData.append('file', {
    uri: audioUri,
    type: 'audio/wav',
    name: 'recording.wav'
  });

  const response = await fetch(
    'http://your-server:5000/analyze',
    { method: 'POST', body: formData }
  );

  return response.json();
};
```

### Flask Backend Example
```python
from flask import Flask, request
from cough_detector import CoughDetector
from respiratory_rate_analyzer import RespiratoryRateEstimator

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    audio = request.files['file']
    audio.save('temp.wav')

    # Run analysis
    cough_detector = CoughDetector()
    coughs = cough_detector.detect_coughs('temp.wav')

    rr_estimator = RespiratoryRateEstimator()
    breathing = rr_estimator.estimate_rate('temp.wav')

    return {
        'cough_count': coughs['cough_count'],
        'respiratory_rate': breathing['respiratory_rate'],
        'risk_level': 'HEALTHY'  # Calculate based on metrics
    }
```

---

## Screen Reference

### Home Screen
```
Breathing Check
Monitor your child's breathing

[LAST CHECK CARD]
Status: Healthy (5 min ago) ✓

🎤 Check Breathing
(Large button, 80px)

💡 Make sure it's quiet...
```

### Recording Screen
```
Get Ready

How to Check
1. Find a quiet place
2. Hold phone close to mouth
3. Breathe normally for 15s
4. We'll analyze results

▶ Start Check
(Large button, 80px)
```

### Results Screen
```
Your Results

       ✓
    (Circle)
    180px diameter

Healthy
Breathing looks good!
Risk Score: 85/100

DETAILS
Coughs Detected: 3
Breathing Rate: 20 br/min

All Good!
Your child's breathing is healthy.
• Continue regular check-ups
• Follow medication...

✓ Check Again
○ Back to Home
```

---

## Testing Locally

### Test All Screens
```javascript
// In RecordingScreen.js
const handleStopRecording = () => {
  // Simulate results
  navigation.navigate('Results', {
    riskLevel: 'WARNING',  // Change to test
    score: 65,
    metrics: {
      coughCount: 5,
      respiratoryRate: 24,
      wheezeDetected: false,
      recordingDuration: 15
    }
  });
};
```

### Mock Audio Recording
```javascript
// Test without actual recording
const mockRecording = async () => {
  return 'mock-audio-uri.wav';
};
```

---

## Debugging

### View Logs
```bash
expo start
# → Logs appear in terminal
# → Use expo dev tools
```

### React DevTools
```bash
# Install
npm install -g react-devtools

# Run
react-devtools
```

### Device Console
```bash
# Shake phone → Open dev menu
# Select "Show JS Errors" or "Show Network Inspector"
```

---

## Performance Tips

### Optimize Images
- Icons: 48x48 to 96x96 px
- App icon: 1024x1024 px
- Use PNG for screenshots
- Compress with TinyPNG

### Reduce Bundle Size
```bash
# Check what's in your bundle
expo analyze

# Remove unused packages
npm uninstall unused-package
```

### Lazy Loading
```javascript
// Load screens on demand
const HomeScreen = React.lazy(() => import('./screens/HomeScreen'));
```

---

## Troubleshooting

### App won't start
```bash
# Clear cache and reinstall
expo start -c
npm install
```

### Microphone not working
- Check `app.json` permissions
- Grant permission in settings
- Check app manifests

### Navigation not working
- Verify screen names match
- Check `RootNavigator.js`
- Use `navigation.navigate('Home')` not `navigate`

### Styling looks wrong
- Check theme values in `src/theme.js`
- Verify `SafeAreaView` wraps screens
- Test on multiple device sizes

---

## Next Steps

1. **Connect Backend**
   - Replace API URL in analysisService.js
   - Test audio upload
   - Verify response parsing

2. **Add Custom Branding**
   - Replace app icon
   - Update colors in theme.js
   - Customize text/instructions

3. **Test on Real Device**
   - Build APK/IPA
   - Install on phone
   - Test full flow

4. **Deploy**
   - Submit to App Store
   - Submit to Google Play
   - Monitor for crashes

---

## Resources

### Documentation
- [Expo Docs](https://docs.expo.dev/)
- [React Native Docs](https://reactnative.dev/docs)
- [Navigation Docs](https://reactnavigation.org/docs)

### Design System
- See `MOBILE_UI_GUIDE.md` for detailed specs
- Theme colors in `src/theme.js`
- Component library in `src/components/`

### Example Code
- Full HomeScreen: `src/screens/HomeScreen.js`
- Full RecordingScreen: `src/screens/RecordingScreen.js`
- Full ResultsScreen: `src/screens/ResultsScreen.js`

---

**Happy coding! 🚀**
