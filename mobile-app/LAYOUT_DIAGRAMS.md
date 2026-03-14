# Layout Diagrams - Breathing Check App

## Screen 1: Home Screen - Default State

```
┌────────────────────────────────────────────┐
│ STATUS BAR (20px)                          │
├────────────────────────────────────────────┤
│ SAFE AREA                                  │
│                                            │
│                                            │
│         Breathing Check                    │  ← H1 Title (36px)
│                                            │  ← Padding: 32px top
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────────────────────────────┐  │  ← Last Check Card
│  │ LAST CHECK                      ✓    │  │  ← bg: #F9FAFB
│  │                                      │  │  ← padding: 16px
│  │ Status                          Green│  │  ← border-radius: 16px
│  │ 5 minutes ago                       │  │  ← MiniRiskIndicator (60px)
│  └──────────────────────────────────────┘  │
│                                            │  ← Margin: 24px
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────────────────────────────┐  │  ← PRIMARY BUTTON
│  │                                      │  │  ← Height: 80px
│  │       🎤  Check Breathing            │  │  ← Font: 24px bold
│  │                                      │  │  ← bg: #3B82F6
│  │                                      │  │  ← border-radius: 20px
│  └──────────────────────────────────────┘  │  ← Margin: 24px
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────────────────────────────┐  │  ← INFO CARD
│  │ 💡 Tip                              │  │  ← bg: #3B82F6
│  │                                      │  │  ← text: White (14px)
│  │ Make sure it's quiet so we can       │  │  ← padding: 16px
│  │ hear breathing clearly               │  │  ← border-radius: 16px
│  └──────────────────────────────────────┘  │
│                                            │  ← Margin: 24px
├────────────────────────────────────────────┤
│                                            │
│  ┌────────────┐                           │  ← QUICK ACTIONS
│  │  History   │                           │  ← SmallButton (60px)
│  └────────────┘                           │  ← Secondary variant
│                                            │
│  ← SAFE AREA                               │
└────────────────────────────────────────────┘
```

### Dimensions Reference

```javascript
HeaderSection:
  alignItems: 'center'
  marginBottom: 32px (xl)

Title:
  fontSize: 36 (h1)
  fontWeight: 'bold'
  color: #1F2937 (dark)
  marginBottom: 16px

Subtitle:
  fontSize: 16 (body)
  color: #6B7280 (dark-gray)
  textAlign: 'center'
  marginBottom: 24px

LastCheckSection:
  backgroundColor: '#F9FAFB' (surface)
  borderRadius: 16 (lg)
  padding: 16 (md)
  marginBottom: 32 (xl)

MainButton:
  height: 80
  borderRadius: 20 (xl)
  backgroundColor: '#3B82F6' (info)
  text: 24px, bold, white

TipSection:
  backgroundColor: '#3B82F6' (info)
  borderRadius: 16 (lg)
  padding: 16 (md)
  marginTop: 24 (lg)

TipText:
  fontSize: 16 (body)
  color: white
  lineHeight: 24
```

---

## Screen 2: Recording Screen - Pre-Recording

```
┌────────────────────────────────────────────┐
│ STATUS BAR (20px)                          │
├────────────────────────────────────────────┤
│ SAFE AREA                                  │
│                                            │
│         Get Ready                          │  ← H2 Title (24px)
│                                            │  ← Padding: 32px top
│                                            │
├────────────────────────────────────────────┤
│                                            │
│       How to Check                         │  ← Instruction Title (20px)
│                                            │
│  ┌──────────────────────────────────────┐  │  ← Steps Container
│  │                                      │  │  ← bg: transparent
│  │ 1  Find a quiet place                │  │  ← padding: 0
│  │                                      │  │
│  │ 2  Hold phone close to               │  │  ← Each Step:
│  │    your mouth                        │  │  ├─ padding: 16px vertical
│  │                                      │  │  ├─ step number: 36px, blue
│  │ 3  Breathe normally for 15 seconds   │  │  ├─ step text: 16px, dark
│  │                                      │  │  └─ border-bottom: 1px light-gray
│  │ 4  We'll analyze the results         │  │
│  │                                      │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  📱 Make sure it's quiet so we can         │  ← Tip text (16px, gray)
│  hear clearly                              │  ← Margin: 24px
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────────────────────────────┐  │  ← PRIMARY BUTTON
│  │                                      │  │  ← Height: 80px
│  │       ▶  Start Check                 │  │  ← Font: 24px bold
│  │                                      │  │  ← bg: #3B82F6
│  └──────────────────────────────────────┘  │
│                                            │
│ ← SAFE AREA                                │
└────────────────────────────────────────────┘
```

---

## Screen 2: Recording Screen - During Recording

```
┌────────────────────────────────────────────┐
│ STATUS BAR (20px)                          │
├────────────────────────────────────────────┤
│ SAFE AREA                                  │
│                                            │
│      Recording...                          │  ← H2 Title (24px)
│                                            │  ← Padding: 32px top
│                                            │
├────────────────────────────────────────────┤
│         Keep listening                     │  ← Instruction (20px)
│                                            │
│                                            │
│      ┌──────────────────────┐              │  ← Animated Circle
│      │                      │              │  ├─ Width: 50% of screen
│      │       🎤             │              │  ├─ Height: equal to width
│      │   (Pulsing scale)    │              │  ├─ bg: #3B82F6
│      │                      │              │  ├─ border-radius: 50%
│      └──────────────────────┘              │  ├─ icon: 80px
│                                            │  ├─ animation: scale + opacity
│      Stay still and keep the phone         │
│      close to your mouth                   │
│                                            │
│      Recording Time                        │  ← Timer Label (12px, gray)
│           0:15                             │  ← Timer Value (48px, blue)
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────────────────────────────┐  │  ← DANGER BUTTON
│  │                                      │  │  ← Height: 80px
│  │       ⏹  Stop                       │  │  ← Font: 24px bold
│  │                                      │  │  ← bg: #EF4444
│  └──────────────────────────────────────┘  │
│                                            │
│ ← SAFE AREA                                │
└────────────────────────────────────────────┘
```

### Animation Details

```javascript
Animated Circle:
  width: Dimensions.get('window').width * 0.5
  height: === width
  borderRadius: width / 2
  animation: {
    scale: 1 → 1.1 → 1 (500ms loop)
    opacity: 0.6 → 1 → 0.6 (500ms loop)
  }

Icon:
  fontSize: 80
  color: white
  marginBottom: 8px

Timer:
  fontSize: 48 (h1)
  color: #3B82F6 (info)
  fontWeight: 'bold'
  marginBottom: 16px
```

---

## Screen 3: Results Screen - Healthy (Green)

```
┌────────────────────────────────────────────┐
│ STATUS BAR (20px)                          │
├────────────────────────────────────────────┤
│ SAFE AREA                                  │
│                                            │
│        Your Results                        │  ← H2 Title (24px)
│                                            │  ← Padding: 32px top
│                                            │
├────────────────────────────────────────────┤
│                                            │
│      ┌──────────────────────┐              │  ← Risk Indicator
│      │         ✓            │              │  ├─ Width: 180px
│      │    (Green circle)    │              │  ├─ Height: 180px
│      │                      │              │  ├─ bg: #10B981 (green)
│      │                      │              │  ├─ border-radius: 50%
│      └──────────────────────┘              │  ├─ icon: 80px
│                                            │  ├─ shadow: 4px offset
│            Healthy                         │  ├─ elevation: 8
│     Breathing looks good!                  │
│                                            │
│         Risk Score                         │  ← Score Label (12px, gray)
│            85/100                          │  ← Score Value (36px, green)
│                                            │
├────────────────────────────────────────────┤
│  ┌──────────────────────────────────────┐  │  ← Metrics Card
│  │ DETAILS                              │  │  ├─ bg: #F9FAFB
│  │                                      │  │  ├─ padding: 16px
│  │ Coughs Detected           3          │  │  ├─ border-radius: 16px
│  │ Breathing Rate     20 breaths/min    │  │
│  │ Wheeze Sound       Not detected      │  │  ← Each metric:
│  │ Duration           10s               │  │  ├─ padding-vertical: 16px
│  │                                      │  │  ├─ border-bottom: 1px
│  └──────────────────────────────────────┘  │  └─ except last item
│                                            │
│  ┌──────────────────────────────────────┐  │  ← Guidance Card
│  │ All Good!                            │  │  ├─ bg: #10B981 (green)
│  │                                      │  │  ├─ padding: 16px
│  │ Your child's breathing is healthy.   │  │  ├─ border-radius: 16px
│  │                                      │  │
│  │ ┌────────────────────────────────┐  │  │  ← Actions List
│  │ │ • Continue regular check-ups   │  │  │  ├─ bg: rgba(255,255,255,0.2)
│  │ │                                │  │  │  ├─ border-radius: 12px
│  │ │ • Follow medication as         │  │  │  ├─ padding: 12px
│  │ │   prescribed                   │  │  │  └─ color: white
│  │ └────────────────────────────────┘  │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │  ← Disclaimer
│  │ ⓘ This app provides general          │  │  ├─ bg: #F3F4F6
│  │ guidance only. Always consult with   │  │  ├─ padding: 16px
│  │ healthcare provider for medical      │  │  ├─ border-radius: 16px
│  │ advice, diagnosis, or treatment.     │  │  ├─ font: 12px
│  │                                      │  │  └─ color: #6B7280
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │  ← Primary Button
│  │                                      │  │  ├─ height: 80px
│  │   ✓  Check Again                     │  │  ├─ bg: #10B981 (green)
│  │                                      │  │  └─ font: 24px bold
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │  ← Secondary Button
│  │       Back to Home                   │  │  ├─ height: 60px
│  │                                      │  │  ├─ bg: #F3F4F6
│  │                                      │  │  └─ font: 16px
│  └──────────────────────────────────────┘  │
│                                            │
│ ← SAFE AREA                                │
└────────────────────────────────────────────┘
```

---

## Screen 3: Results Screen - Warning (Yellow)

```
Same layout as Healthy, but:

Risk Indicator:
  bg: #F59E0B (yellow)
  icon: ⚠

Label & Description:
  color: #F59E0B (yellow)
  Monitor / Watch for changes

Guidance Card:
  bg: #F59E0B (yellow)
  title: Monitor Closely
  message: Watch for changes in breathing...
  actions:
    • Keep medication nearby
    • Monitor for other symptoms
    • Schedule check-up if persists

Button:
  bg: #F59E0B (yellow)
```

---

## Screen 3: Results Screen - Critical (Red)

```
Same layout as Healthy, but:

Risk Indicator:
  bg: #EF4444 (red)
  icon: ⚠

Label & Description:
  color: #EF4444 (red)
  Check Now / Contact healthcare provider today

Guidance Card:
  bg: #EF4444 (red)
  title: Take Action
  message: Please contact your healthcare provider today.
  actions:
    • Call your doctor
    • Use rescue inhaler if prescribed
    • Go to urgent care if worsens

Button:
  bg: #EF4444 (red)
```

---

## Component Size Reference

### Buttons

```
Large Button:
  Height: 80px
  Padding H: 24px (lg)
  Font Size: 24px
  Font Weight: bold
  Border Radius: 20px (xl)
  Touch Target: ✓ Exceeds 44px minimum

Medium Button:
  Height: 60px
  Font Size: 18px

Small Button:
  Height: 50px
  Padding H: 24px (lg)
  Font Size: 16px
  Font Weight: 600
  Border Radius: 16px (lg)
```

### Circle Indicators

```
Risk Indicator (Main):
  Diameter: 180px
  Border Radius: 90px (50%)
  Icon: 80px
  Shadow: 4px offset, 8 elevation

Mini Risk Indicator:
  Diameter: 60px (default, adjustable)
  Border Radius: 30px (50%)
  Icon: 30px

Mini Risk Indicator (Status Card):
  Diameter: 48px
  Icon: 24px
```

### Spacing Scale

```
xs: 8px    ← Small gap between inline elements
sm: 12px   ← Vertical spacing in cards
md: 16px   ← Standard padding
lg: 24px   ← Section padding
xl: 32px   ← Large section spacing
xxl: 48px  ← Screen edge padding (not used in mobile)
```

---

## Typography Hierarchy

```
H1 (Titles):
  Font Size: 36px
  Font Weight: bold
  Line Height: 44px
  Color: #1F2937 (dark)
  Use: App title (Home Screen)

H2 (Screen Titles):
  Font Size: 24px
  Font Weight: 600
  Line Height: 32px
  Color: #1F2937 (dark)
  Use: Screen headers

H3 (Section Headers):
  Font Size: 20px
  Font Weight: 600
  Line Height: 28px
  Color: #1F2937 (dark)
  Use: Card titles

Body (Main Text):
  Font Size: 16px
  Font Weight: 400
  Line Height: 24px
  Color: #1F2937 or #6B7280
  Use: Instructions, descriptions

Label (Field Labels):
  Font Size: 14px
  Font Weight: 500
  Line Height: 20px
  Color: #6B7280 (gray)
  Use: Labels, captions

Small (Fine Print):
  Font Size: 12px
  Font Weight: 400
  Line Height: 16px
  Color: #9CA3AF (light-gray)
  Use: Disclaimers, timestamps
```

---

## Responsive Design Grid

```
Screen Width: 390px (iPhone 12 base)

Horizontal Padding: 24px (lg) on each side
Safe Area: 390 - (24 × 2) = 342px content width

For Wider Screens (iPhone Pro Max, 430px):
  → Same padding maintained
  → Content width: 430 - (24 × 2) = 382px
  → No horizontal scaling (portrait locked)

For Narrower Screens (iPhone SE, 375px):
  → Same padding maintained
  → Content width: 375 - (24 × 2) = 327px
  → Buttons still 80px height
  → Text remains readable
```

---

## Safe Area Considerations

```
All screens wrapped in:
  <SafeAreaView style={styles.safeArea}>
    {/* Content here */}
  </SafeAreaView>

SafeAreaView automatically handles:
  ✓ Status bar (20px top)
  ✓ Notches (iPhone X+)
  ✓ Home indicator (bottom inset)
  ✓ Dynamic island (iPhone 14+)

Container padding:
  paddingHorizontal: 24px (lg)
  paddingVertical: 32px (xl)
  Scroll padding: additional 32px bottom
```

---

## Color Contrast Reference

```
Text on Background:
  #1F2937 (dark) on #FFFFFF (white)
  Contrast Ratio: 15.3:1 ✓ WCAG AAA

Text on Green:
  #FFFFFF (white) on #10B981 (green)
  Contrast Ratio: 4.5:1 ✓ WCAG AA (normal)

Text on Yellow:
  #1F2937 (dark) on #F59E0B (yellow)
  Contrast Ratio: 8.6:1 ✓ WCAG AAA

Text on Red:
  #FFFFFF (white) on #EF4444 (red)
  Contrast Ratio: 3.9:1 ⚠ Below AA
  → Use larger text (18px+) or lighter red

Text on Blue (Info):
  #FFFFFF (white) on #3B82F6 (blue)
  Contrast Ratio: 4.5:1 ✓ WCAG AA
```

---

**Last Updated:** March 14, 2026
**Format:** ASCII diagrams + React Native dimensions
**Target Devices:** iPhone SE (375px) to Pro Max (430px)
