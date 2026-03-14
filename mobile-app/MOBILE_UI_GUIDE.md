# Breathing Check Mobile App - UI Guide

## Overview

**Breathing Check** is a child-friendly mobile app designed for parents to monitor their children's respiratory health through simple audio recording and analysis.

**Target Users:** Parents of children aged 5-11
**Platform:** React Native Expo (iOS/Android)
**Design Philosophy:** Minimal text, large buttons, color-coded results

---

## Design System

### Color Scheme (Traffic Light)

```
✓ GREEN (#10B981)   - Healthy breathing detected
⚠ YELLOW (#F59E0B)  - Monitor for changes
⚠ RED (#EF4444)     - Seek medical attention
```

### Touch Targets
- **Large buttons:** 80px height (minimum 44px accessibility standard)
- **Spacing:** 16px base unit (padding, margins)
- **Text size:** 24px for titles, 16px for body
- **Border radius:** 16px for buttons, 12px for cards

### Typography Hierarchy
```
Title (H1):      36px, Bold     - "Breathing Check"
Heading (H2):    24px, 600wt    - Screen titles
Heading (H3):    20px, 600wt    - Section headers
Body:            16px, 400wt    - Instructions
Label:           14px, 500wt    - Field labels
Small:           12px, 400wt    - Captions
```

---

## Screen Architecture

### 1. Home Screen

**Purpose:** Entry point, show last check status
**Navigation:** → Recording, → Results (history)

**Layout:**
```
┌─────────────────────────────────────┐
│          SAFE AREA TOP              │
├─────────────────────────────────────┤
│                                     │
│         Breathing Check             │  <- H1 Title (36px)
│     (stacked on 2 lines)            │
│  Monitor your child's breathing     │  <- Subtitle
│                                     │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │   LAST CHECK         ✓        │  │  <- Status Card
│  │   Status             Green    │  │     (if available)
│  │   5 minutes ago      (80px)   │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │  🎤 Check Breathing           │  │  <- Primary Button
│  │    [80px height]              │  │     (LargeButton)
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  💡 Tip                       │  │  <- Info Card
│  │  Make sure it's quiet so we   │  │
│  │  can hear breathing clearly   │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  ┌──────────┐          ┌──────────┐ │
│  │ History  │                      │ │  <- Quick Actions
│  └──────────┘                      │ │
│                                     │
└─────────────────────────────────────┘
```

**Components:**
- Header: Title + Subtitle
- Last Check Card (conditional)
- Main CTA Button (size: large, icon: 🎤)
- Tip Section (info box)
- Quick Action Buttons

**Key Features:**
- ✓ Large 80px button (minimum 44px touch target)
- ✓ Minimal text (icons + key words)
- ✓ Color-coded status indicator
- ✓ Clear information hierarchy

---

### 2. Recording Screen

**Purpose:** Capture breathing audio with visual instructions
**Navigation:** ← Home, → Results

**Layout (Pre-Recording):**
```
┌─────────────────────────────────────┐
│          SAFE AREA TOP              │
├─────────────────────────────────────┤
│         Get Ready                   │  <- H2 Title
│                                     │
├─────────────────────────────────────┤
│                                     │
│         How to Check                │  <- Instructions
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 1  Find a quiet place        │   │  <- Step List
│  │                              │   │
│  │ 2  Hold phone close to       │   │
│  │    your mouth                │   │
│  │                              │   │
│  │ 3  Breathe normally for      │   │
│  │    15 seconds                │   │
│  │                              │   │
│  │ 4  We'll analyze results     │   │
│  └─────────────────────────────┘   │
│                                     │
│  📱 Make sure it's quiet so        │  <- Tip text
│  we can hear clearly               │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ▶ Start Check                │  │  <- Primary Button
│  │    [80px height]              │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Layout (During Recording):**
```
┌─────────────────────────────────────┐
│          SAFE AREA TOP              │
├─────────────────────────────────────┤
│       Recording...                  │  <- H2 Title
│                                     │
├─────────────────────────────────────┤
│                                     │
│           Keep listening            │  <- Instruction
│                                     │
│     ┌──────────────────────┐        │
│     │                      │        │
│     │   🎤 (Pulsing)       │        │  <- Animated Circle
│     │   (width*0.5)        │        │     (pulsing scale)
│     │                      │        │
│     └──────────────────────┘        │
│                                     │
│  Stay still and keep the phone      │
│  close to your mouth                │
│                                     │
│      Recording Time                 │
│            0:15                     │  <- Timer (48px)
│                                     │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ⏹ Stop                       │  │  <- Danger Button
│  │    [80px height]              │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Components:**
- Header: Status ("Get Ready" / "Recording...")
- Instructions (pre-recording)
- Animated Circle with Icon (50% width, pulsing animation)
- Timer Display (48px font)
- Action Button (Start/Stop)

**Key Features:**
- ✓ Simple step-by-step instructions
- ✓ Animated recording indicator (pulsing circle)
- ✓ Real-time timer (seconds)
- ✓ Large, clear action button
- ✓ Minimal text (just essential instructions)

**Animation Details:**
- Circle scale: 1 → 1.1 → 1 (500ms cycle)
- Circle opacity: 0.6 → 1 → 0.6 (500ms cycle)
- Smooth loop while recording

---

### 3. Results Screen

**Purpose:** Display analysis results with risk indicator and guidance
**Navigation:** ← Recording, → Home (check again)

**Layout:**
```
┌─────────────────────────────────────┐
│          SAFE AREA TOP              │
├─────────────────────────────────────┤
│         Your Results                │  <- H2 Title
│                                     │
├─────────────────────────────────────┤
│                                     │
│      ┌──────────────────────┐       │
│      │       ✓              │       │  <- Risk Indicator
│      │     (180px circle)   │       │  - Green/Yellow/Red
│      │                      │       │  - Animated/Glowing
│      └──────────────────────┘       │
│                                     │
│            Healthy                  │  <- Risk Label
│   Breathing looks good!             │  <- Risk Description
│                                     │
│          Risk Score                 │
│              85/100                 │  <- Score
│                                     │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │  DETAILS                      │  │  <- Metrics Card
│  │                              │  │
│  │  Coughs Detected      3       │  │
│  │  Breathing Rate      20 br/min│  │
│  │  Wheeze Sound   Not detected  │  │
│  │  Duration          10s        │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │  All Good!                    │  │  <- Guidance Card
│  │                              │  │  (color-coded)
│  │  Your child's breathing is    │  │
│  │  healthy.                     │  │
│  │                              │  │
│  │  • Continue regular check-ups │  │
│  │  • Follow medication as       │  │
│  │    prescribed                 │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  ⓘ This app provides general        │  <- Disclaimer
│  guidance only. Always consult       │     (small text)
│  with healthcare provider...         │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Check Again                  │  │  <- Primary Button
│  │    [80px height]              │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Back to Home                 │  │  <- Secondary Button
│  │    [60px height]              │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Components:**
- Header: "Your Results"
- Risk Indicator (180px circle, color-coded)
  - Green: ✓
  - Yellow: ⚠
  - Red: ⚠
- Risk Label & Description
- Score Display (e.g., "85/100")
- Metrics Card (coughs, respiratory rate, wheeze, duration)
- Guidance Card (color-matched to risk level)
  - Title
  - Message
  - Action items (bulleted list)
- Disclaimer
- Action Buttons (Check Again, Back to Home)

**Risk Indicator Variations:**

**Green (Healthy):**
```
✓ Healthy
Breathing looks good!

Actions:
• Continue regular check-ups
• Follow medication as prescribed
```

**Yellow (Monitor):**
```
⚠ Monitor
Watch for changes

Actions:
• Keep medication nearby
• Monitor for other symptoms
• Schedule check-up if persists
```

**Red (Critical):**
```
⚠ Check Now
Contact healthcare provider today

Actions:
• Call your doctor
• Use rescue inhaler if prescribed
• Go to urgent care if worsens
```

---

## Component Library

### 1. LargeButton
```jsx
<LargeButton
  title="Check Breathing"
  onPress={handlePress}
  variant="primary" | "success" | "warning" | "danger"
  size="large" | "medium"
  icon="🎤"  // Optional emoji
  loading={false}
  disabled={false}
/>
```

**Variants:**
- `primary`: Blue (info color)
- `success`: Green
- `warning`: Amber
- `danger`: Red
- `secondary`: Light gray with border

**Sizes:**
- `large`: 80px height, 24px text
- `medium`: 60px height, 18px text

---

### 2. SmallButton
```jsx
<SmallButton
  title="History"
  onPress={handlePress}
  variant="primary" | "secondary"
/>
```

**Height:** 50px
**Text:** 16px (600 weight)

---

### 3. RiskIndicator
```jsx
<RiskIndicator
  riskLevel="HEALTHY" | "WARNING" | "CRITICAL"
  score={85}
  showDetails={true}
/>
```

**Circle:** 180px diameter
**Animation:** Shadow, glowing effect
**Score display:** Optional (85/100)

---

### 4. MiniRiskIndicator
```jsx
<MiniRiskIndicator
  riskLevel="HEALTHY"
  size={60}  // diameter in pixels
/>
```

**Sizes:** 48px, 60px, 80px (flexible)
**Use:** Status cards, history list items

---

### 5. RiskBadge
```jsx
<RiskBadge riskLevel="WARNING" />
```

**Inline badge** for showing status in cards/lists

---

## File Structure

```
mobile-app/
├── App.js                          # Main entry point
├── app.json                        # Expo config
├── package.json                    # Dependencies
├── src/
│   ├── theme.js                    # Colors, spacing, typography
│   ├── components/
│   │   ├── Button.js              # LargeButton, SmallButton
│   │   └── RiskIndicator.js       # Risk display components
│   ├── screens/
│   │   ├── HomeScreen.js          # Home (check status)
│   │   ├── RecordingScreen.js     # Recording UI
│   │   └── ResultsScreen.js       # Results with indicator
│   └── navigation/
│       └── RootNavigator.js       # Screen navigation
├── assets/
│   ├── icon.png                   # App icon
│   ├── splash.png                 # Splash screen
│   └── adaptive-icon.png          # Android adaptive icon
└── MOBILE_UI_GUIDE.md            # This file
```

---

## Integration with Backend

### Audio Recording API

```javascript
// src/services/audioService.js
const recordAudio = async (duration = 15) => {
  const recording = new Audio.Recording();
  await recording.prepareToRecordAsync(
    Audio.RecordingOptionsPresets.HIGH_QUALITY
  );
  await recording.startAsync();

  // Wait for duration
  await new Promise(r => setTimeout(r, duration * 1000));

  await recording.stopAndUnloadAsync();
  return recording.getURI();
};
```

### Analysis API Integration

```javascript
// src/services/analysisService.js
const analyzeBreathing = async (audioUri) => {
  const formData = new FormData();
  formData.append('audio', {
    uri: audioUri,
    type: 'audio/wav',
    name: 'breathing.wav'
  });

  const response = await fetch(
    'https://api.breathing-check.com/analyze',
    {
      method: 'POST',
      body: formData
    }
  );

  const results = await response.json();

  return {
    riskLevel: determineRiskLevel(results),
    score: calculateScore(results),
    metrics: {
      coughCount: results.cough_count,
      respiratoryRate: results.respiratory_rate,
      wheezeDetected: results.wheeze_detected,
      recordingDuration: results.duration
    }
  };
};

function determineRiskLevel(results) {
  if (results.wheeze_detected && results.respiratory_rate > 30) {
    return 'CRITICAL';
  }
  if (results.cough_count > 10 || results.respiratory_rate > 25) {
    return 'WARNING';
  }
  return 'HEALTHY';
}

function calculateScore(results) {
  // Score calculation logic
  // Higher = healthier (0-100)
  return 100 - (results.risk_score * 100);
}
```

### Results Navigation

```javascript
// From RecordingScreen after analysis
const handleAnalysisComplete = (results) => {
  navigation.navigate('Results', {
    riskLevel: results.riskLevel,
    score: results.score,
    metrics: results.metrics
  });
};
```

---

## Accessibility Considerations

### Touch Targets
✓ Minimum 44x44 points (iOS), 48x48 dp (Android)
✓ All buttons meet or exceed this standard
✓ Spacing between targets: 16px minimum

### Text Contrast
✓ WCAG AA: 4.5:1 for normal text
✓ WCAG AA: 3:1 for large text
✓ Color-coded indicators include text labels

### Readability
✓ Large fonts (24px+)
✓ Minimal text on screen
✓ High contrast colors
✓ Simple language for children

### VoiceOver/TalkBack
- All interactive elements labeled
- Screen readers announce results clearly
- Test IDs for automation testing

---

## Responsive Design

### Device Sizes
- **iPhone SE (375px):** Optimized
- **iPhone 12 (390px):** Primary target
- **iPhone Pro Max (430px):** Full width layouts
- **Android (various):** Flexible spacing

### Orientation
- **Portrait:** Primary (locked)
- **Landscape:** Not supported (for children safety)

### Safe Areas
- Use `SafeAreaView` for all screens
- Account for notches/status bars
- Consistent padding (16px)

---

## Testing Checklist

### Visual Testing
- [ ] All buttons are 80px height
- [ ] Text is legible (min 16px)
- [ ] Colors are traffic light system
- [ ] Animations are smooth
- [ ] No horizontal scroll needed

### Functional Testing
- [ ] Home → Recording navigation works
- [ ] Recording starts/stops correctly
- [ ] Results display correct data
- [ ] Back navigation works
- [ ] "Check Again" restarts flow

### Accessibility Testing
- [ ] Touch targets are 44x44+ minimum
- [ ] Text contrast meets WCAG AA
- [ ] Screen reader compatible
- [ ] Color blind friendly (shapes + text)

### Device Testing
- [ ] iPhone SE (375px)
- [ ] iPhone 12 (390px)
- [ ] iPhone Pro Max (430px)
- [ ] Various Android phones
- [ ] Tablets (landscape disabled)

---

## Customization

### Brand Colors
Edit `src/theme.js`:
```javascript
export const Colors = {
  GREEN: '#10B981',
  YELLOW: '#F59E0B',
  RED: '#EF4444',
  INFO: '#3B82F6',  // Primary button color
};
```

### Button Sizes
Edit `src/components/Button.js`:
```javascript
size: "large"  // 80px height
size: "medium" // 60px height
```

### Risk Level Labels
Edit `src/theme.js`:
```javascript
export const RiskLevel = {
  HEALTHY: { label: 'Healthy', ... },
  WARNING: { label: 'Monitor', ... },
  CRITICAL: { label: 'Check Now', ... },
};
```

---

## Installation & Setup

### Prerequisites
```bash
npm install -g expo-cli
```

### Install Dependencies
```bash
cd mobile-app
npm install
```

### Run on Simulator
```bash
# iOS
npm run ios

# Android
npm run android
```

### Build APK/IPA
```bash
# iOS (Testflight)
expo build:ios

# Android (Google Play)
expo build:android
```

### Environment Variables
Create `.env` file:
```
REACT_APP_API_URL=https://api.breathing-check.com
REACT_APP_API_KEY=your_key_here
```

---

## Troubleshooting

### Build Issues
**Problem:** Expo won't start
**Solution:** `npm install` → `expo start -c` (clear cache)

**Problem:** Microphone permission denied
**Solution:** Check `app.json` plugin configuration

### Performance Issues
**Problem:** Animations are choppy
**Solution:** Use `useNativeDriver: true` in Animated API

**Problem:** Large audio files slow app
**Solution:** Compress audio, implement streaming

### Styling Issues
**Problem:** Layout shifts on different devices
**Solution:** Use `Dimensions` API, test multiple screen sizes

---

## Future Enhancements

### Phase 2
- [ ] Family profiles (multiple children)
- [ ] Symptom history/trends
- [ ] Medication reminders
- [ ] Doctor sharing (secure link)

### Phase 3
- [ ] ML-based risk scoring
- [ ] Predictive alerts
- [ ] Integration with EHR systems
- [ ] Telemedicine integration

### Phase 4
- [ ] Wearable device support
- [ ] Cloud sync across devices
- [ ] Dark mode
- [ ] Multiple languages

---

## Best Practices

### Code Organization
- Keep components small and focused
- Use hooks for state management
- Separate navigation logic
- Extract theme to constants

### Performance
- Lazy load screens
- Memoize expensive computations
- Optimize images (16x9 ratio)
- Use FlatList for long lists

### User Experience
- Show loading states
- Provide haptic feedback
- Clear error messages
- Undo/cancel options

### Testing
- Unit test utilities
- Integration test flows
- Visual regression tests
- A/B test with users

---

## Design References

### Similar Apps
- MyFitnessPal (simple interface)
- Calm (large buttons, minimal text)
- Medisafe (medication reminders, clear UI)

### Design Inspiration
- Material Design 3 (rounded buttons)
- Apple Human Interface Guidelines
- A11y Project (accessibility)

---

**Version:** 1.0.0
**Last Updated:** March 14, 2026
**Status:** Production Ready for Hackathon
