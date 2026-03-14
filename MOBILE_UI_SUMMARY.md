# Mobile UI Design Summary - Breathing Check

## Quick Overview

**Breathing Check** is a child-friendly asthma monitoring app with 3 simple screens and a traffic light color system.

---

## The Three Screens

### 1️⃣ HOME SCREEN - Check Breathing

**Purpose:** Entrance point, show last check status

**Layout:**
```
┌────────────────────────────┐
│   Breathing Check          │  ← Title (large)
│   Monitor your child's     │  ← Subtitle (minimal text)
│   breathing                │
│                            │
├────────────────────────────┤
│  LAST CHECK        ✓       │  ← Status card (if available)
│  Status: Healthy   Green   │  ← Color-coded indicator
│  5 minutes ago             │  ← Time reference
├────────────────────────────┤
│                            │
│   🎤 CHECK BREATHING       │  ← MAIN BUTTON
│   [80px height button]     │  ← Large, tappable area
│                            │
├────────────────────────────┤
│  💡 Make sure it's quiet   │  ← Helpful tip
│     so we can hear clearly │  ← Blue background
│                            │
└────────────────────────────┘
```

**Key Elements:**
- ✓ Minimal text (title, subtitle, labels)
- ✓ Large 80px button (exceeds 44px minimum touch target)
- ✓ Icon emoji (🎤) for quick recognition
- ✓ Color-coded status if available
- ✓ Clear call-to-action

---

### 2️⃣ RECORDING SCREEN - Get Ready

**Purpose:** Capture 15-second breathing audio with clear instructions

**Before Recording:**
```
┌────────────────────────────┐
│      Get Ready             │  ← Title
│                            │
│   How to Check             │  ← Instructions
│                            │
│   1  Find a quiet place    │  ← Numbered steps
│   2  Hold phone to mouth   │  ← 4 simple instructions
│   3  Breathe normally      │  ← Easy to understand
│   4  15 seconds            │
│                            │
│  📱 Make sure it's quiet   │  ← Tip reminder
│                            │
│   ▶ START CHECK            │  ← Large button (80px)
│   [Blue button]            │
│                            │
└────────────────────────────┘
```

**During Recording:**
```
┌────────────────────────────┐
│    Recording...            │  ← Status
│                            │
│   Keep listening           │  ← Instruction
│                            │
│     ┌────────────┐         │  ← Animated Circle
│     │            │         │  ← (pulsing scale + opacity)
│     │    🎤      │         │  ← Large icon
│     │            │         │  ← 50% of screen width
│     └────────────┘         │  ← 180px diameter
│                            │
│  Stay still and keep the   │  ← Reassurance
│  phone close to your mouth │
│                            │
│        0:15                │  ← Timer (48px font)
│                            │
│   ⏹ STOP                   │  ← Red stop button (80px)
│   [Red button]             │  ← Clear action
│                            │
└────────────────────────────┘
```

**Key Elements:**
- ✓ Step-by-step instructions (numbered)
- ✓ Pulsing animated circle (visual feedback)
- ✓ Real-time timer
- ✓ Clear start/stop buttons
- ✓ Reassuring messages

**Animation:**
- Circle scales: 1.0 → 1.1 → 1.0 (500ms loop)
- Circle opacity: 0.6 → 1.0 → 0.6 (500ms loop)
- Creates "recording in progress" feeling

---

### 3️⃣ RESULTS SCREEN - Your Results

**Purpose:** Display color-coded results with clear guidance

**Layout (HEALTHY - GREEN):**
```
┌────────────────────────────┐
│     Your Results           │  ← Title
│                            │
│       ┌────────────┐       │  ← 180px Circle
│       │     ✓      │       │  ← GREEN (#10B981)
│       │            │       │  ← Icon: ✓
│       └────────────┘       │  ← Glowing shadow
│                            │
│        HEALTHY             │  ← Risk Label
│  Breathing looks good!     │  ← Description
│        85/100              │  ← Score (0-100)
│                            │
├────────────────────────────┤
│   DETAILS                  │  ← Metrics Card
│   Coughs            3      │  ← Cough count
│   Breathing Rate   20/min  │  ← Breathing
│   Wheeze Sound    Detected │  ← Wheeze status
├────────────────────────────┤
│                            │
│  ✓ All Good! (GREEN CARD) │  ← Guidance Card
│                            │  ← Color-matched
│  Your child's breathing    │
│  is healthy.               │
│                            │
│  • Continue check-ups      │  ← Bullet actions
│  • Follow medications      │
│                            │
├────────────────────────────┤
│  ⓘ Always consult with     │  ← Disclaimer
│     your healthcare        │  ← (small text, gray)
│     provider for medical   │
│     advice                 │
├────────────────────────────┤
│                            │
│  ✓ CHECK AGAIN             │  ← Primary button (80px)
│  ○ BACK TO HOME            │  ← Secondary button (60px)
│                            │
└────────────────────────────┘
```

**Results Variations:**

**YELLOW - MONITOR (Warning):**
```
        ⚠
    (YELLOW circle)

    MONITOR
    Watch for changes
    Score: 65/100

    Actions:
    • Keep medication nearby
    • Monitor for symptoms
    • Schedule check-up
```

**RED - CHECK NOW (Critical):**
```
        ⚠
    (RED circle)

    CHECK NOW
    Contact healthcare provider
    Score: 35/100

    Actions:
    • Call your doctor
    • Use rescue inhaler
    • Go to urgent care
```

**Key Elements:**
- ✓ Large 180px risk indicator (impossible to miss)
- ✓ Traffic light colors (red/yellow/green)
- ✓ Simple icons (✓ or ⚠)
- ✓ Clear, actionable guidance
- ✓ Color-matched card design
- ✓ Medical disclaimer

---

## Design System

### Colors (Traffic Light)

```
✓ GREEN  #10B981   Healthy breathing
⚠ YELLOW #F59E0B   Monitor for changes
⚠ RED    #EF4444   Seek medical attention
```

### Typography

```
TITLE (H1):    36px, bold        "Breathing Check"
HEADING (H2):  24px, 600wt       "Your Results"
SECTION (H3):  20px, 600wt       "Details"
BODY:          16px, 400wt       Instructions
LABEL:         14px, 500wt       Captions
SMALL:         12px, 400wt       Disclaimers
```

### Spacing (8px scale)

```
xs  8px     → Small gaps
sm  12px    → Button padding
md  16px    → Standard padding
lg  24px    → Section padding
xl  32px    → Large spacing
```

### Buttons

```
PRIMARY (Large):
  Height: 80px
  Width: Full - 48px padding
  Font: 24px bold
  Color: Blue (#3B82F6)
  Border radius: 20px
  Icon: Emoji + text

SECONDARY (Small):
  Height: 60px
  Font: 16px bold
  Color: Light gray background
  Border: 2px gray border
```

### Touch Targets

```
✓ All buttons: 44px+ minimum (exceeds accessibility standard)
✓ Large primary: 80px height
✓ Spacing: 16px minimum between elements
✓ Safe area: Respects notches, home indicator
```

---

## Component Library

### Button Component

```jsx
<LargeButton
  title="Check Breathing"
  onPress={handlePress}
  icon="🎤"
  variant="primary"  // blue
/>

// Variants: primary, success, warning, danger, secondary
// Sizes: large (80px), medium (60px)
// Icons: Emoji support
```

### Risk Indicator

```jsx
<RiskIndicator
  riskLevel="HEALTHY"  // HEALTHY | WARNING | CRITICAL
  score={85}
  showDetails={true}
/>

// Returns: 180px circle with color, icon, score
// Animations: Shadow, glow effect
```

### Mini Indicator

```jsx
<MiniRiskIndicator
  riskLevel="HEALTHY"
  size={60}
/>

// For status cards and lists
// Flexible sizing
```

---

## User Flow

```
┌─ Open App ─┐
│            │
│   HOME     │  Last check: Healthy ✓
│  SCREEN    │  "Check Breathing" button (80px)
│            │
└─────┬──────┘
      │ User taps button
      ↓
┌─────────────┐
│ RECORDING   │  "Get Ready" title
│  SCREEN     │  Step-by-step instructions
│             │  ▶ Start Check button (80px)
└─────┬───────┘
      │ User taps Start
      ↓
┌─────────────┐
│ RECORDING   │  "Recording..." title
│  SCREEN     │  Animated pulsing circle
│ (Recording) │  Timer: 0:00 → 0:15
│             │  ⏹ Stop button (red, 80px)
└─────┬───────┘
      │ 15 sec elapsed or user taps Stop
      ↓
      [Upload to backend API]
      │ Analysis in progress
      ↓
┌─────────────┐
│ RESULTS     │  "Your Results" title
│  SCREEN     │  180px risk indicator (Green/Yellow/Red)
│             │  Risk score (0-100)
│             │  Detailed metrics
│             │  Color-matched guidance
└─────┬───────┘
      │ User can:
      ├─ Tap "Check Again" → back to RECORDING
      └─ Tap "Back Home" → back to HOME
```

---

## Design Principles

### 1. Minimal Text
- Icons and colors do most of the work
- One-liner instructions
- Clear labels on buttons
- ≤ 16 words per screen

### 2. Large Buttons
- 80px for primary actions (exceeds 44px standard)
- Easy for children to tap
- Emoji icons for quick recognition
- Tap-friendly spacing

### 3. Color-Coded Results
- Green = healthy, safe to continue
- Yellow = monitor, watch for changes
- Red = urgent, contact provider
- Consistent across all screens

### 4. Simple Navigation
- 3 screens, one clear flow
- Forward: Home → Recording → Results
- Backward: Results → Home
- No hidden menus or tabs

### 5. Child-Friendly
- Large, colorful interface
- Playful but professional
- Clear step-by-step instructions
- Reassuring messages
- Fast feedback (timer, animations)

---

## Mobile Platform Support

### iOS
- iPhone SE (375px)
- iPhone 12/13 (390px)
- iPhone Pro Max (430px)
- Notch/Dynamic Island: Handled
- Home Indicator: Respected

### Android
- Various screen sizes (flexible layout)
- Portrait orientation locked
- Safe area respected
- System navigation handled

### Responsive Design
- Same UI on all devices
- Flexible spacing
- Consistent padding (24px sides)
- No horizontal scrolling
- Touch targets always 44px+

---

## File Structure

```
mobile-app/
├── App.js                      # Entry point
├── app.json                    # Expo config
├── package.json               # Dependencies
│
├── src/
│   ├── theme.js               # Colors, spacing, typography
│   │
│   ├── components/
│   │   ├── Button.js
│   │   │   ├─ LargeButton (80px)
│   │   │   └─ SmallButton (60px)
│   │   └─ RiskIndicator.js
│   │       ├─ RiskIndicator (180px)
│   │       ├─ MiniRiskIndicator (flexible)
│   │       └─ RiskBadge (inline)
│   │
│   ├── screens/
│   │   ├─ HomeScreen.js       (Status, Check button)
│   │   ├─ RecordingScreen.js  (Instructions, Timer)
│   │   └─ ResultsScreen.js    (Risk indicator, Guidance)
│   │
│   └── navigation/
│       └─ RootNavigator.js     (Stack navigation)
│
├── assets/
│   ├── icon.png               (App icon)
│   ├── splash.png             (Splash screen)
│   └── adaptive-icon.png      (Android icon)
│
└── Documentation/
    ├── MOBILE_UI_GUIDE.md     (1000+ lines)
    ├── QUICK_START.md         (Setup guide)
    └── LAYOUT_DIAGRAMS.md     (Visual reference)
```

---

## Integration Points

### Connect to Backend

Edit `src/services/analysisService.js`:

```javascript
const API_URL = 'https://api.breathing-check.com';

const analyzeBreathing = async (audioUri) => {
  const formData = new FormData();
  formData.append('file', {
    uri: audioUri,
    type: 'audio/wav',
    name: 'breathing.wav'
  });

  const response = await fetch(API_URL + '/analyze', {
    method: 'POST',
    body: formData
  });

  return response.json();
};
```

### Pass Results to UI

```javascript
// In RecordingScreen.js
const results = await analyzeBreathing(audioUri);

navigation.navigate('Results', {
  riskLevel: results.risk_level,  // HEALTHY | WARNING | CRITICAL
  score: results.risk_score,      // 0-100
  metrics: {
    coughCount: results.cough_count,
    respiratoryRate: results.respiratory_rate,
    wheezeDetected: results.wheeze_detected,
    recordingDuration: 15
  }
});
```

---

## Testing Checklist

### Visual
- [ ] All buttons are 80px height (primary), 60px (secondary)
- [ ] Text is readable (16px+ minimum)
- [ ] Colors match traffic light system
- [ ] Spacing is consistent (multiples of 8px)
- [ ] Animations are smooth (60 FPS)
- [ ] No horizontal scroll needed

### Functional
- [ ] Home → Recording navigation works
- [ ] Recording starts and stops correctly
- [ ] Timer counts accurately
- [ ] Results display correct risk level
- [ ] All 3 risk colors (G/Y/R) display properly
- [ ] Back navigation works

### Accessibility
- [ ] Touch targets 44px+ minimum
- [ ] Text contrast meets WCAG AA (4.5:1)
- [ ] Screen reader compatible
- [ ] Color + text (not just color)

### Devices
- [ ] iPhone SE (375px)
- [ ] iPhone 12 (390px)
- [ ] iPhone Pro Max (430px)
- [ ] Android phones (various sizes)

---

## Performance Targets

| Metric | Target |
|--------|--------|
| App startup | < 2 sec |
| Screen transition | < 300 ms |
| Animation FPS | 60 FPS |
| Memory usage | < 100 MB |
| Battery per check | < 5% |

---

## Next Steps

1. **Setup Development**
   ```bash
   npm install -g expo-cli
   cd mobile-app
   npm install
   expo start
   ```

2. **Test on Device**
   - Scan QR code with Expo app
   - Test all 3 screens
   - Verify animations smooth

3. **Connect Backend**
   - Update API endpoint
   - Test audio upload
   - Verify results parsing

4. **Build for Release**
   ```bash
   expo build:ios
   expo build:android
   ```

---

**Status:** Production Ready for Hackathon ✓
**Last Updated:** March 14, 2026
**Platform:** React Native + Expo
**Target Ages:** 5-11 years
**Parent Users:** Non-technical to technical

