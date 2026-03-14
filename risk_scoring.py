#!/usr/bin/env python3
"""
Risk Scoring Algorithm for Asthma Monitoring in Children
=========================================================

Simple, transparent risk calculation for respiratory health assessment.

Combines multiple respiratory metrics into a single risk score:
  - Wheeze detection (presence + intensity)
  - Respiratory rate abnormality
  - Cough frequency

Output: LOW / MODERATE / HIGH risk

Design: Hackathon-friendly (simple rules, easy to explain)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Tuple


class RiskLevel(Enum):
    """Risk severity levels"""
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"


@dataclass
class RiskMetrics:
    """Input metrics for risk calculation"""
    wheeze_probability: float  # 0-1, confidence that wheeze is present
    wheeze_intensity: float    # 0-1, loudness/prominence of wheeze
    respiratory_rate: int      # breaths per minute
    cough_frequency: float     # coughs per minute


@dataclass
class RiskScore:
    """Output risk assessment"""
    risk_level: RiskLevel
    risk_score: float          # 0-100 (0=healthy, 100=critical)
    confidence: float          # 0-1, confidence in assessment
    explanation: str           # Human-readable explanation
    component_scores: dict     # Breakdown of each factor


class RiskScoringAlgorithm:
    """
    Simple, transparent risk scoring for asthma monitoring.

    Algorithm Overview:
    -------------------
    1. Calculate individual component scores (0-100) for:
       - Wheeze risk
       - Respiratory rate abnormality
       - Cough risk

    2. Combine with weighted average:
       Overall Score = (wheeze_score × 0.4) +
                      (rate_score × 0.35) +
                      (cough_score × 0.25)

    3. Classify into risk level:
       LOW:       0-40
       MODERATE: 41-70
       HIGH:     71-100

    Weighting rationale:
      - Wheeze (40%): Strongest indicator of airway obstruction
      - Rate (35%):   Indicates respiratory effort
      - Cough (25%):  Supporting indicator
    """

    # Age-appropriate respiratory rate ranges (breaths per minute)
    # Source: Pediatric normal ranges
    RESPIRATORY_RATE_NORMAL = {
        "5-6_years": (20, 26),
        "7-8_years": (19, 25),
        "9-11_years": (18, 24),
        "default": (18, 26),  # Conservative range for 5-11 years
    }

    def __init__(self, age_years: int = 8):
        """
        Initialize scorer.

        Args:
            age_years: Child's age (5-11 years)
        """
        self.age_years = age_years
        self._set_normal_rate_range()

    def _set_normal_rate_range(self):
        """Set normal respiratory rate range based on age."""
        if self.age_years <= 6:
            self.normal_rate = self.RESPIRATORY_RATE_NORMAL["5-6_years"]
        elif self.age_years <= 8:
            self.normal_rate = self.RESPIRATORY_RATE_NORMAL["7-8_years"]
        else:
            self.normal_rate = self.RESPIRATORY_RATE_NORMAL["9-11_years"]

    def calculate_risk(self, metrics: RiskMetrics) -> RiskScore:
        """
        Calculate overall respiratory risk.

        Args:
            metrics: RiskMetrics with wheeze, rate, cough data

        Returns:
            RiskScore with level, score, and explanation
        """
        # Calculate individual component scores
        wheeze_score = self._score_wheeze(
            metrics.wheeze_probability,
            metrics.wheeze_intensity
        )
        rate_score = self._score_respiratory_rate(metrics.respiratory_rate)
        cough_score = self._score_cough_frequency(metrics.cough_frequency)

        # Combine with weighted average
        overall_score = (
            wheeze_score * 0.40 +
            rate_score * 0.35 +
            cough_score * 0.25
        )

        # Classify into risk level
        risk_level = self._classify_risk(overall_score)

        # Calculate confidence
        confidence = self._calculate_confidence(metrics)

        # Generate explanation
        explanation = self._generate_explanation(
            overall_score,
            wheeze_score,
            rate_score,
            cough_score,
            metrics
        )

        return RiskScore(
            risk_level=risk_level,
            risk_score=round(overall_score, 1),
            confidence=round(confidence, 2),
            explanation=explanation,
            component_scores={
                "wheeze": round(wheeze_score, 1),
                "respiratory_rate": round(rate_score, 1),
                "cough": round(cough_score, 1),
            }
        )

    def _score_wheeze(
        self,
        wheeze_probability: float,
        wheeze_intensity: float
    ) -> float:
        """
        Score wheeze component (0-100).

        Logic:
          - No wheeze detected: 0 points
          - Wheeze probability < 0.3: 10 points
          - Wheeze probability 0.3-0.5: 30 points
          - Wheeze probability 0.5-0.7: 50 points
          - Wheeze probability > 0.7: 70+ points

          If wheeze detected, add intensity bonus:
            - Mild (0-0.3): +0 points
            - Moderate (0.3-0.7): +15 points
            - Severe (>0.7): +30 points

        Returns:
            Score 0-100
        """
        if wheeze_probability < 0.1:
            # No wheeze detected
            return 0.0

        # Base score from probability
        if wheeze_probability < 0.3:
            base_score = 10
        elif wheeze_probability < 0.5:
            base_score = 30
        elif wheeze_probability < 0.7:
            base_score = 50
        else:
            base_score = 70

        # Bonus from intensity
        intensity_bonus = 0
        if wheeze_intensity > 0.3:
            intensity_bonus = 15
        if wheeze_intensity > 0.7:
            intensity_bonus = 30

        score = base_score + intensity_bonus
        return min(score, 100.0)

    def _score_respiratory_rate(self, respiratory_rate: int) -> float:
        """
        Score respiratory rate abnormality (0-100).

        Logic:
          Normal range for age: 0 points
          ±2 bpm above/below normal: 20 points (slightly elevated)
          ±4 bpm above/below normal: 40 points (moderately elevated)
          ±6 bpm above/below normal: 60 points (elevated)
          >6 bpm outside normal range: 80+ points (very elevated)

        Why rates matter:
          - Too slow (bradypnea): <15 breaths/min (depression)
          - Too fast (tachypnea): >35 breaths/min (distress)
          - Normal: 18-26 breaths/min for 5-11 years

        Returns:
            Score 0-100
        """
        low, high = self.normal_rate

        # Check if within normal range
        if low <= respiratory_rate <= high:
            return 0.0

        # Calculate deviation from normal range
        if respiratory_rate < low:
            deviation = low - respiratory_rate
        else:
            deviation = respiratory_rate - high

        # Score based on deviation
        if deviation <= 2:
            return 20.0
        elif deviation <= 4:
            return 40.0
        elif deviation <= 6:
            return 60.0
        else:
            return min(80.0 + (deviation - 6) * 5, 100.0)

    def _score_cough_frequency(self, cough_frequency: float) -> float:
        """
        Score cough frequency (0-100).

        Logic:
          No cough (0 coughs/min): 0 points
          Occasional (0-2 coughs/min): 10 points
          Mild (2-5 coughs/min): 25 points
          Moderate (5-10 coughs/min): 45 points
          Frequent (10-15 coughs/min): 65 points
          Very frequent (>15 coughs/min): 85+ points

        Context:
          - Normal: 0-5 coughs per minute during day
          - Concerning: >10 coughs per minute
          - Severe: >20 coughs per minute

        Returns:
            Score 0-100
        """
        if cough_frequency < 0.5:
            return 0.0
        elif cough_frequency < 2:
            return 10.0
        elif cough_frequency < 5:
            return 25.0
        elif cough_frequency < 10:
            return 45.0
        elif cough_frequency < 15:
            return 65.0
        else:
            return min(85.0 + (cough_frequency - 15) * 2, 100.0)

    def _classify_risk(self, score: float) -> RiskLevel:
        """
        Classify risk level based on overall score.

        Thresholds:
          LOW (0-40):           Healthy, no concerns
          MODERATE (41-70):     Monitor, watch for changes
          HIGH (71-100):        Urgent, contact healthcare provider

        Returns:
            RiskLevel enum value
        """
        if score <= 40:
            return RiskLevel.LOW
        elif score <= 70:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.HIGH

    def _calculate_confidence(self, metrics: RiskMetrics) -> float:
        """
        Calculate confidence in the assessment (0-1).

        Confidence is higher when:
          - Multiple indicators align
          - Wheeze is clearly detected (high probability + intensity)
          - Respiratory rate is clearly abnormal

        Logic:
          Base: 0.7 (7/10 confidence)
          +0.1 if wheeze probability > 0.5 (clear wheeze)
          +0.1 if cough frequency > 10 (clear cough pattern)
          +0.1 if rate is >6 bpm outside normal (clear abnormality)

        Returns:
            Confidence 0-1
        """
        confidence = 0.7

        if metrics.wheeze_probability > 0.5:
            confidence += 0.1

        if metrics.cough_frequency > 10:
            confidence += 0.1

        low, high = self.normal_rate
        rate_deviation = abs(metrics.respiratory_rate - low)
        if metrics.respiratory_rate > high:
            rate_deviation = abs(metrics.respiratory_rate - high)

        if rate_deviation > 6:
            confidence += 0.1

        return min(confidence, 1.0)

    def _generate_explanation(
        self,
        overall_score: float,
        wheeze_score: float,
        rate_score: float,
        cough_score: float,
        metrics: RiskMetrics
    ) -> str:
        """
        Generate human-readable explanation.

        Returns:
            Explanation string with findings
        """
        parts = []

        # Wheeze finding
        if metrics.wheeze_probability < 0.1:
            parts.append("✓ No wheeze detected")
        elif metrics.wheeze_probability < 0.5:
            parts.append(f"⚠ Possible wheeze ({metrics.wheeze_probability*100:.0f}% confidence)")
        else:
            parts.append(f"⚠ Clear wheeze detected ({metrics.wheeze_probability*100:.0f}% confidence)")

        # Respiratory rate finding
        low, high = self.normal_rate
        if low <= metrics.respiratory_rate <= high:
            parts.append(f"✓ Breathing rate normal ({metrics.respiratory_rate} br/min)")
        else:
            if metrics.respiratory_rate < low:
                parts.append(f"⚠ Breathing rate LOW ({metrics.respiratory_rate} br/min, normal {low}-{high})")
            else:
                parts.append(f"⚠ Breathing rate HIGH ({metrics.respiratory_rate} br/min, normal {low}-{high})")

        # Cough finding
        if metrics.cough_frequency < 2:
            parts.append("✓ No significant cough")
        elif metrics.cough_frequency < 5:
            parts.append(f"⚠ Occasional cough ({metrics.cough_frequency:.1f} coughs/min)")
        elif metrics.cough_frequency < 10:
            parts.append(f"⚠ Moderate cough ({metrics.cough_frequency:.1f} coughs/min)")
        else:
            parts.append(f"⚠ Frequent cough ({metrics.cough_frequency:.1f} coughs/min)")

        return " | ".join(parts)

    def get_recommendations(self, risk_score: RiskScore) -> list:
        """
        Get recommendations based on risk level.

        Returns:
            List of actionable recommendations
        """
        if risk_score.risk_level == RiskLevel.LOW:
            return [
                "Continue regular check-ups",
                "Follow medication as prescribed",
                "Monitor for any changes",
            ]
        elif risk_score.risk_level == RiskLevel.MODERATE:
            return [
                "Keep medication nearby",
                "Monitor symptoms daily",
                "Schedule a check-up if condition persists",
                "Avoid known asthma triggers",
            ]
        else:  # HIGH
            return [
                "Call healthcare provider today",
                "Use rescue inhaler if prescribed",
                "Go to urgent care if breathing worsens",
                "Seek emergency care if severe difficulty breathing",
            ]


def calculate_risk(
    wheeze_probability: float,
    wheeze_intensity: float,
    respiratory_rate: int,
    cough_frequency: float,
    age_years: int = 8
) -> RiskScore:
    """
    Convenience function for quick risk calculation.

    Args:
        wheeze_probability: 0-1, confidence wheeze is present
        wheeze_intensity: 0-1, loudness of wheeze
        respiratory_rate: breaths per minute
        cough_frequency: coughs per minute
        age_years: child's age (5-11)

    Returns:
        RiskScore with assessment
    """
    scorer = RiskScoringAlgorithm(age_years=age_years)
    metrics = RiskMetrics(
        wheeze_probability=wheeze_probability,
        wheeze_intensity=wheeze_intensity,
        respiratory_rate=respiratory_rate,
        cough_frequency=cough_frequency
    )
    return scorer.calculate_risk(metrics)


# ============================================================================
# TEST CASES - Demonstrate algorithm behavior
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("RISK SCORING ALGORITHM - TEST CASES")
    print("="*70)

    # Test Case 1: Healthy child
    print("\n" + "-"*70)
    print("TEST 1: Healthy Child")
    print("-"*70)
    score = calculate_risk(
        wheeze_probability=0.0,
        wheeze_intensity=0.0,
        respiratory_rate=22,
        cough_frequency=0.5,
        age_years=8
    )
    print(f"Risk Level:        {score.risk_level.value}")
    print(f"Risk Score:        {score.risk_score}/100")
    print(f"Confidence:        {score.confidence*100:.0f}%")
    print(f"Component Scores:  Wheeze: {score.component_scores['wheeze']}, "
          f"Rate: {score.component_scores['respiratory_rate']}, "
          f"Cough: {score.component_scores['cough']}")
    print(f"Explanation:       {score.explanation}")
    print(f"Recommendations:   {RiskScoringAlgorithm().get_recommendations(score)}")

    # Test Case 2: Possible wheeze, normal rate
    print("\n" + "-"*70)
    print("TEST 2: Possible Wheeze + Normal Breathing Rate")
    print("-"*70)
    score = calculate_risk(
        wheeze_probability=0.6,
        wheeze_intensity=0.4,
        respiratory_rate=24,
        cough_frequency=3.0,
        age_years=8
    )
    print(f"Risk Level:        {score.risk_level.value}")
    print(f"Risk Score:        {score.risk_score}/100")
    print(f"Confidence:        {score.confidence*100:.0f}%")
    print(f"Component Scores:  Wheeze: {score.component_scores['wheeze']}, "
          f"Rate: {score.component_scores['respiratory_rate']}, "
          f"Cough: {score.component_scores['cough']}")
    print(f"Explanation:       {score.explanation}")
    print(f"Recommendations:   {RiskScoringAlgorithm().get_recommendations(score)}")

    # Test Case 3: Elevated rate + cough
    print("\n" + "-"*70)
    print("TEST 3: Elevated Breathing Rate + Moderate Cough")
    print("-"*70)
    score = calculate_risk(
        wheeze_probability=0.2,
        wheeze_intensity=0.0,
        respiratory_rate=32,
        cough_frequency=8.0,
        age_years=8
    )
    print(f"Risk Level:        {score.risk_level.value}")
    print(f"Risk Score:        {score.risk_score}/100")
    print(f"Confidence:        {score.confidence*100:.0f}%")
    print(f"Component Scores:  Wheeze: {score.component_scores['wheeze']}, "
          f"Rate: {score.component_scores['respiratory_rate']}, "
          f"Cough: {score.component_scores['cough']}")
    print(f"Explanation:       {score.explanation}")
    print(f"Recommendations:   {RiskScoringAlgorithm().get_recommendations(score)}")

    # Test Case 4: Clear wheeze + elevated rate + frequent cough
    print("\n" + "-"*70)
    print("TEST 4: Clear Wheeze + Elevated Rate + Frequent Cough (CRITICAL)")
    print("-"*70)
    score = calculate_risk(
        wheeze_probability=0.9,
        wheeze_intensity=0.8,
        respiratory_rate=38,
        cough_frequency=18.0,
        age_years=8
    )
    print(f"Risk Level:        {score.risk_level.value}")
    print(f"Risk Score:        {score.risk_score}/100")
    print(f"Confidence:        {score.confidence*100:.0f}%")
    print(f"Component Scores:  Wheeze: {score.component_scores['wheeze']}, "
          f"Rate: {score.component_scores['respiratory_rate']}, "
          f"Cough: {score.component_scores['cough']}")
    print(f"Explanation:       {score.explanation}")
    print(f"Recommendations:   {RiskScoringAlgorithm().get_recommendations(score)}")

    # Test Case 5: Young child with slightly elevated rate
    print("\n" + "-"*70)
    print("TEST 5: Young Child (Age 5) - Slightly Elevated Rate")
    print("-"*70)
    score = calculate_risk(
        wheeze_probability=0.1,
        wheeze_intensity=0.0,
        respiratory_rate=28,  # Slightly high for age 5 (normal: 20-26)
        cough_frequency=1.0,
        age_years=5
    )
    print(f"Risk Level:        {score.risk_level.value}")
    print(f"Risk Score:        {score.risk_score}/100")
    print(f"Confidence:        {score.confidence*100:.0f}%")
    print(f"Component Scores:  Wheeze: {score.component_scores['wheeze']}, "
          f"Rate: {score.component_scores['respiratory_rate']}, "
          f"Cough: {score.component_scores['cough']}")
    print(f"Explanation:       {score.explanation}")
    print(f"Recommendations:   {RiskScoringAlgorithm().get_recommendations(score)}")

    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70 + "\n")
