#!/usr/bin/env python3
"""
Environmental Asthma Risk Factor Module
========================================

Retrieves environmental factors that affect asthma symptoms:
  - Air Quality Index (AQI)
  - Pollen levels
  - Humidity
  - Temperature

Calculates an environmental risk score (0-100) that combines these factors.

Data Sources:
  - OpenWeatherMap API (weather, air quality)
  - Geographic location data (city coordinates)
  - Seasonal pollen patterns (estimated from date)
  - Default fallback data for demo purposes

Usage:
    from environmental_risk import get_environmental_risk

    risk = get_environmental_risk(city='New York')
    print(f"Environmental Risk: {risk.risk_score}/100")
    print(f"Risk Level: {risk.risk_level}")
    print(f"Recommendations: {risk.recommendations}")
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from enum import Enum
import json
from datetime import datetime
import requests


class EnvironmentalRiskLevel(Enum):
    """Environmental risk severity levels"""
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"


@dataclass
class EnvironmentalMetrics:
    """Environmental measurements"""
    aqi: int                    # Air Quality Index (0-500)
    pm25: float                 # PM2.5 particulates (μg/m³)
    pm10: float                 # PM10 particulates (μg/m³)
    humidity: float             # Relative humidity (0-100%)
    temperature: float          # Temperature (°C)
    pollen_level: float         # Pollen level (0-100, estimated)
    city: str
    timestamp: str              # ISO format timestamp


@dataclass
class EnvironmentalRisk:
    """Environmental risk assessment"""
    risk_level: EnvironmentalRiskLevel
    risk_score: float           # 0-100
    confidence: float           # 0-1 (data quality)
    metrics: EnvironmentalMetrics
    explanation: str
    recommendations: list
    component_scores: Dict      # Breakdown of factors
    data_source: str            # API used or 'mock'


class EnvironmentalRiskCalculator:
    """
    Calculates environmental asthma risk from weather/air quality data.

    Algorithm:
    ----------
    1. Retrieve environmental metrics (AQI, humidity, pollen, temp)
    2. Score each component (0-100)
    3. Combine with weighted average:
       Overall Score = (AQI × 0.40) +
                      (Pollen × 0.35) +
                      (Humidity × 0.15) +
                      (Temperature × 0.10)

    Weighting rationale:
      40% → AQI (strongest trigger for asthma)
      35% → Pollen (seasonal allergen exposure)
      15% → Humidity (affects airway reactivity)
      10% → Temperature (extreme cold/heat triggers)
    """

    # API Keys (free tier)
    OPENWEATHER_API_KEY = "demo"  # Use your own key for production
    OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
    WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

    # City coordinates (fallback for demo)
    CITY_COORDS = {
        "new york": (40.7128, -74.0060),
        "los angeles": (34.0522, -118.2437),
        "chicago": (41.8781, -87.6298),
        "houston": (29.7604, -95.3698),
        "phoenix": (33.4484, -112.0742),
        "philadelphia": (39.9526, -75.1652),
        "san antonio": (29.4241, -98.4936),
        "san diego": (32.7157, -117.1611),
        "dallas": (32.7767, -96.7970),
        "san jose": (37.3382, -121.8863),
        "london": (51.5074, -0.1278),
        "paris": (48.8566, 2.3522),
        "tokyo": (35.6762, 139.6503),
        "sydney": (33.8688, 151.2093),
    }

    # Pollen calendar (seasonal patterns)
    POLLEN_PATTERNS = {
        "spring": 0.8,   # High pollen (March-May)
        "summer": 0.5,   # Moderate pollen (June-August)
        "fall": 0.6,     # Moderate-high pollen (Sept-Nov)
        "winter": 0.2,   # Low pollen (Dec-Feb)
    }

    def __init__(self, use_api: bool = False, api_key: Optional[str] = None):
        """
        Initialize calculator.

        Args:
            use_api: Whether to use real API calls (requires valid API key)
            api_key: OpenWeatherMap API key for real data
        """
        self.use_api = use_api
        if api_key:
            self.OPENWEATHER_API_KEY = api_key

    def get_environmental_risk(self, city: str) -> EnvironmentalRisk:
        """
        Get environmental risk for a city.

        Args:
            city: City name (e.g., 'New York')

        Returns:
            EnvironmentalRisk with assessment
        """
        # Retrieve metrics
        metrics = self._get_metrics(city)

        # Calculate component scores
        aqi_score = self._score_aqi(metrics.aqi, metrics.pm25)
        pollen_score = self._score_pollen(metrics.pollen_level)
        humidity_score = self._score_humidity(metrics.humidity)
        temp_score = self._score_temperature(metrics.temperature)

        # Combine with weighted average
        overall_score = (
            aqi_score * 0.40 +
            pollen_score * 0.35 +
            humidity_score * 0.15 +
            temp_score * 0.10
        )

        # Classify risk level
        risk_level = self._classify_risk(overall_score)

        # Calculate confidence
        confidence = self._calculate_confidence(metrics)

        # Generate explanation
        explanation = self._generate_explanation(metrics)

        # Get recommendations
        recommendations = self._get_recommendations(risk_level, metrics)

        return EnvironmentalRisk(
            risk_level=risk_level,
            risk_score=round(overall_score, 1),
            confidence=round(confidence, 2),
            metrics=metrics,
            explanation=explanation,
            recommendations=recommendations,
            component_scores={
                "aqi": round(aqi_score, 1),
                "pollen": round(pollen_score, 1),
                "humidity": round(humidity_score, 1),
                "temperature": round(temp_score, 1),
            },
            data_source="OpenWeatherMap API" if self.use_api else "Mock data (demo)"
        )

    def _get_metrics(self, city: str) -> EnvironmentalMetrics:
        """Retrieve environmental metrics for city."""
        if self.use_api:
            return self._get_metrics_from_api(city)
        else:
            return self._get_metrics_mock(city)

    def _get_metrics_from_api(self, city: str) -> EnvironmentalMetrics:
        """
        Retrieve real data from OpenWeatherMap API.

        Requires valid API key.
        """
        try:
            # Get coordinates
            coords = self._get_coordinates(city)
            if not coords:
                return self._get_metrics_mock(city)

            lat, lon = coords

            # Get air quality data
            params_pollution = {
                "lat": lat,
                "lon": lon,
                "appid": self.OPENWEATHER_API_KEY
            }

            response_aqi = requests.get(
                self.OPENWEATHER_URL,
                params=params_pollution,
                timeout=5
            )
            aqi_data = response_aqi.json()

            # Get weather data
            params_weather = {
                "lat": lat,
                "lon": lon,
                "appid": self.OPENWEATHER_API_KEY,
                "units": "metric"
            }

            response_weather = requests.get(
                self.WEATHER_URL,
                params=params_weather,
                timeout=5
            )
            weather_data = response_weather.json()

            # Extract values
            aqi = aqi_data.get("list", [{}])[0].get("main", {}).get("aqi", 2)
            # Convert AQI 1-5 scale to 0-500 scale
            aqi_score = aqi * 100 if aqi else 200

            components = aqi_data.get("list", [{}])[0].get("components", {})
            pm25 = components.get("pm2_5", 35.0)
            pm10 = components.get("pm10", 50.0)

            humidity = weather_data.get("main", {}).get("humidity", 60.0)
            temperature = weather_data.get("main", {}).get("temp", 20.0)

            # Estimate pollen
            pollen = self._estimate_pollen(temperature)

            return EnvironmentalMetrics(
                aqi=int(aqi_score),
                pm25=pm25,
                pm10=pm10,
                humidity=humidity,
                temperature=temperature,
                pollen_level=pollen,
                city=city,
                timestamp=datetime.now().isoformat()
            )

        except Exception as e:
            print(f"API error: {e}, using mock data")
            return self._get_metrics_mock(city)

    def _get_coordinates(self, city: str) -> Optional[Tuple[float, float]]:
        """Get latitude/longitude for city."""
        city_lower = city.lower()

        # Check hardcoded list
        if city_lower in self.CITY_COORDS:
            return self.CITY_COORDS[city_lower]

        # Try geocoding (requires extra API call)
        try:
            params = {
                "q": city,
                "appid": self.OPENWEATHER_API_KEY,
                "limit": 1
            }
            response = requests.get(
                "https://api.openweathermap.org/geo/1.0/direct",
                params=params,
                timeout=5
            )
            data = response.json()
            if data:
                return (data[0]["lat"], data[0]["lon"])
        except Exception:
            pass

        return None

    def _get_metrics_mock(self, city: str) -> EnvironmentalMetrics:
        """
        Generate realistic mock data for demonstration.

        Simulates seasonal and geographic variations.
        """
        # Simulate variation by city
        city_lower = city.lower()
        city_hash = sum(ord(c) for c in city_lower) % 100

        # Base AQI by city (higher for polluted cities)
        city_aqi_map = {
            "los angeles": 120,
            "new york": 85,
            "chicago": 95,
            "houston": 90,
            "phoenix": 75,
            "beijing": 180,
            "delhi": 200,
            "london": 60,
            "paris": 65,
        }
        base_aqi = city_aqi_map.get(city_lower, 80 + (city_hash % 40))

        # Seasonal variation
        month = datetime.now().month
        if 3 <= month <= 5:  # Spring: high pollen
            pollen = 75 + (city_hash % 20)
            aqi_adjustment = 0
        elif 6 <= month <= 8:  # Summer: moderate
            pollen = 50 + (city_hash % 20)
            aqi_adjustment = -10
        elif 9 <= month <= 11:  # Fall: moderate-high
            pollen = 60 + (city_hash % 20)
            aqi_adjustment = 5
        else:  # Winter: low pollen
            pollen = 20 + (city_hash % 20)
            aqi_adjustment = 20

        # Temperature by latitude
        if city_lower in ["phoenix", "houston", "san antonio", "dallas", "los angeles"]:
            temperature = 28 + (city_hash % 10)
        elif city_lower in ["chicago", "new york", "philadelphia", "dallas"]:
            temperature = 15 + (city_hash % 10)
        elif city_lower in ["london", "paris"]:
            temperature = 12 + (city_hash % 8)
        elif city_lower in ["tokyo", "sydney"]:
            temperature = 18 + (city_hash % 8)
        else:
            temperature = 15 + (city_hash % 15)

        # Humidity varies with temperature and season
        if pollen > 60:
            humidity = 50 + (city_hash % 20)
        else:
            humidity = 45 + (city_hash % 25)

        aqi = int(base_aqi + aqi_adjustment + (city_hash % 20))
        pm25 = aqi * 0.3
        pm10 = aqi * 0.5

        return EnvironmentalMetrics(
            aqi=aqi,
            pm25=float(pm25),
            pm10=float(pm10),
            humidity=float(humidity),
            temperature=float(temperature),
            pollen_level=float(pollen),
            city=city,
            timestamp=datetime.now().isoformat()
        )

    def _estimate_pollen(self, temperature: float) -> float:
        """
        Estimate pollen level from temperature.

        Higher in spring/early summer with moderate temperatures (15-25°C).
        """
        month = datetime.now().month

        # Base pollen by season
        if 3 <= month <= 5:
            base_pollen = 75
        elif 6 <= month <= 8:
            base_pollen = 45
        elif 9 <= month <= 11:
            base_pollen = 60
        else:
            base_pollen = 20

        # Adjust by temperature
        if 15 <= temperature <= 25:
            temp_factor = 1.0  # Optimal for pollen
        elif temperature < 15:
            temp_factor = 0.7  # Cold slows pollen
        else:
            temp_factor = 0.8  # Hot reduces pollen

        return min(100.0, base_pollen * temp_factor)

    def _score_aqi(self, aqi: int, pm25: float) -> float:
        """
        Score Air Quality Index (0-100).

        Logic:
          AQI 0-50 (Good):              0-20 points
          AQI 51-100 (Moderate):        20-40 points
          AQI 101-150 (Unhealthy SCG):  40-60 points
          AQI 151-200 (Unhealthy):      60-80 points
          AQI 201+ (Very Unhealthy):    80-100 points

        PM2.5 is also considered:
          <12 μg/m³:   Good
          12-35 μg/m³: Moderate
          >35 μg/m³:   Unhealthy
        """
        if aqi <= 50:
            aqi_score = 15
        elif aqi <= 100:
            aqi_score = 30 + (aqi - 50) * 0.4  # 30-50
        elif aqi <= 150:
            aqi_score = 50 + (aqi - 100) * 0.4  # 50-70
        elif aqi <= 200:
            aqi_score = 70 + (aqi - 150) * 0.4  # 70-90
        else:
            aqi_score = 90 + min(10, (aqi - 200) * 0.01)

        # Bonus from PM2.5
        if pm25 > 35:
            aqi_score += 10
        elif pm25 > 12:
            aqi_score += 5

        return min(aqi_score, 100.0)

    def _score_pollen(self, pollen_level: float) -> float:
        """
        Score pollen exposure (0-100).

        Logic:
          0-20 (Low):           0-20 points
          21-40 (Moderate):     20-40 points
          41-70 (High):         40-75 points
          71-100 (Very High):   75-100 points
        """
        if pollen_level < 20:
            return pollen_level
        elif pollen_level < 40:
            return 20 + (pollen_level - 20) * 1.0  # 20-40
        elif pollen_level < 70:
            return 40 + (pollen_level - 40) * 1.17  # 40-75
        else:
            return 75 + (pollen_level - 70) * 0.83  # 75-100

    def _score_humidity(self, humidity: float) -> float:
        """
        Score humidity impact on asthma (0-100).

        Logic:
          Optimal: 40-60% humidity (0-10 points)
          Dry: <40% humidity (10-40 points) - airway irritation
          Humid: >60% humidity (10-50 points) - mold/dust mites
          Very humid: >75% (40-80 points) - strong mold risk
        """
        if 40 <= humidity <= 60:
            return 5 + (humidity - 40) * 0.1  # 5-7 (optimal)
        elif humidity < 40:
            return 40 - (40 - humidity) * 0.5  # 40 at 0%, 10 at 40%
        elif humidity <= 75:
            return 10 + (humidity - 60) * 1.0  # 10-25
        else:
            return 25 + (humidity - 75) * 2.0  # 25-80

    def _score_temperature(self, temperature: float) -> float:
        """
        Score temperature extremes (0-100).

        Logic:
          Optimal: 18-24°C (0-10 points)
          Cool: 10-18°C (10-30 points) - can trigger asthma
          Warm: 24-28°C (10-30 points)
          Cold: <10°C (30-70 points) - strong trigger
          Hot: >28°C (30-60 points) - ozone increases
        """
        if 18 <= temperature <= 24:
            return 5
        elif temperature < 18:
            if temperature < 10:
                return min(70.0, 30 + (10 - temperature) * 4)
            else:
                return 10 + (18 - temperature) * 2.5
        else:  # > 24
            if temperature > 28:
                return 30 + (temperature - 28) * 4
            else:
                return 10 + (temperature - 24) * 5

    def _classify_risk(self, score: float) -> EnvironmentalRiskLevel:
        """Classify environmental risk level."""
        if score <= 35:
            return EnvironmentalRiskLevel.LOW
        elif score <= 65:
            return EnvironmentalRiskLevel.MODERATE
        else:
            return EnvironmentalRiskLevel.HIGH

    def _calculate_confidence(self, metrics: EnvironmentalMetrics) -> float:
        """
        Calculate confidence in environmental assessment (0-1).

        Higher when data is recent and values are reasonable.
        """
        confidence = 0.8

        # Confidence factors
        if metrics.aqi > 300:  # Extreme values might be unreliable
            confidence -= 0.1

        if not (0 <= metrics.humidity <= 100):  # Invalid data
            confidence -= 0.2

        if not (-50 < metrics.temperature < 50):  # Invalid data
            confidence -= 0.2

        return max(0.5, min(1.0, confidence))

    def _generate_explanation(self, metrics: EnvironmentalMetrics) -> str:
        """Generate human-readable explanation of environmental factors."""
        parts = []

        # AQI finding
        if metrics.aqi <= 50:
            parts.append(f"✓ Air quality GOOD (AQI {metrics.aqi})")
        elif metrics.aqi <= 100:
            parts.append(f"⚠ Air quality MODERATE (AQI {metrics.aqi})")
        elif metrics.aqi <= 150:
            parts.append(f"⚠ Air quality UNHEALTHY for sensitive groups (AQI {metrics.aqi})")
        else:
            parts.append(f"⚠ Air quality UNHEALTHY (AQI {metrics.aqi})")

        # Pollen finding
        if metrics.pollen_level < 30:
            parts.append(f"✓ Pollen LOW ({metrics.pollen_level:.0f})")
        elif metrics.pollen_level < 60:
            parts.append(f"⚠ Pollen MODERATE ({metrics.pollen_level:.0f})")
        else:
            parts.append(f"⚠ Pollen HIGH ({metrics.pollen_level:.0f})")

        # Humidity finding
        if 40 <= metrics.humidity <= 60:
            parts.append(f"✓ Humidity OPTIMAL ({metrics.humidity:.0f}%)")
        elif metrics.humidity < 40:
            parts.append(f"⚠ Humidity LOW/DRY ({metrics.humidity:.0f}%)")
        else:
            parts.append(f"⚠ Humidity HIGH ({metrics.humidity:.0f}%)")

        # Temperature finding
        if 18 <= metrics.temperature <= 24:
            parts.append(f"✓ Temperature comfortable ({metrics.temperature:.1f}°C)")
        elif metrics.temperature < 10:
            parts.append(f"⚠ Temperature very COLD ({metrics.temperature:.1f}°C)")
        elif metrics.temperature < 18:
            parts.append(f"⚠ Temperature COOL ({metrics.temperature:.1f}°C)")
        elif metrics.temperature > 28:
            parts.append(f"⚠ Temperature HOT ({metrics.temperature:.1f}°C)")
        else:
            parts.append(f"⚠ Temperature warm ({metrics.temperature:.1f}°C)")

        return " | ".join(parts)

    def _get_recommendations(
        self,
        risk_level: EnvironmentalRiskLevel,
        metrics: EnvironmentalMetrics
    ) -> list:
        """Get recommendations based on environmental factors."""
        recommendations = []

        # AQI recommendations
        if metrics.aqi > 100:
            recommendations.append("Limit outdoor activities due to poor air quality")
            recommendations.append("Keep windows closed, use air purifier indoors")
        elif metrics.aqi > 50:
            recommendations.append("Monitor air quality, be ready to reduce outdoor activity")

        # Pollen recommendations
        if metrics.pollen_level > 60:
            recommendations.append("High pollen: Keep windows closed during peak times")
            recommendations.append("Take allergy medication before going outside")
        elif metrics.pollen_level > 40:
            recommendations.append("Moderate pollen: Rinse nasal passages after outdoor time")

        # Humidity recommendations
        if metrics.humidity > 70:
            recommendations.append("High humidity: Use dehumidifier to reduce mold")
        elif metrics.humidity < 40:
            recommendations.append("Dry air: Use humidifier to ease airway irritation")

        # Temperature recommendations
        if metrics.temperature < 10:
            recommendations.append("Cold weather: Wear scarf over nose/mouth")
            recommendations.append("Avoid intense outdoor activity in cold")
        elif metrics.temperature > 30:
            recommendations.append("Hot weather: Avoid peak heat hours, stay hydrated")

        # General recommendations
        if risk_level == EnvironmentalRiskLevel.HIGH:
            recommendations.insert(0, "High environmental risk: Check with healthcare provider")
        elif risk_level == EnvironmentalRiskLevel.MODERATE:
            if not recommendations:
                recommendations.append("Environmental conditions acceptable, standard precautions")

        if not recommendations:
            recommendations.append("Environmental conditions favorable for breathing")

        return recommendations


def get_environmental_risk(city: str, use_api: bool = False, api_key: Optional[str] = None) -> EnvironmentalRisk:
    """
    Convenience function for quick environmental risk calculation.

    Args:
        city: City name
        use_api: Whether to use real API (requires valid key)
        api_key: OpenWeatherMap API key

    Returns:
        EnvironmentalRisk assessment
    """
    calculator = EnvironmentalRiskCalculator(use_api=use_api, api_key=api_key)
    return calculator.get_environmental_risk(city)


# ============================================================================
# TEST CASES - Demonstrate functionality
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("ENVIRONMENTAL RISK ASSESSMENT - TEST CASES")
    print("="*80)

    # Test Case 1: Clean city
    print("\n" + "-"*80)
    print("TEST 1: Clean City (Good Environmental Conditions)")
    print("-"*80)
    risk = get_environmental_risk("London")
    print(f"City:                {risk.metrics.city}")
    print(f"Risk Level:          {risk.risk_level.value}")
    print(f"Risk Score:          {risk.risk_score}/100")
    print(f"Confidence:          {risk.confidence*100:.0f}%")
    print(f"Data Source:         {risk.data_source}")
    print(f"\nMetrics:")
    print(f"  Air Quality:       AQI {risk.metrics.aqi} (PM2.5: {risk.metrics.pm25:.1f} μg/m³)")
    print(f"  Pollen Level:      {risk.metrics.pollen_level:.0f}/100")
    print(f"  Humidity:          {risk.metrics.humidity:.0f}%")
    print(f"  Temperature:       {risk.metrics.temperature:.1f}°C")
    print(f"\nComponent Scores:")
    for component, score in risk.component_scores.items():
        print(f"  {component.capitalize():15} {score:6.1f}/100")
    print(f"\nExplanation:         {risk.explanation}")
    print(f"Recommendations:")
    for i, rec in enumerate(risk.recommendations, 1):
        print(f"  {i}. {rec}")

    # Test Case 2: Polluted city
    print("\n" + "-"*80)
    print("TEST 2: Polluted City (Poor Air Quality)")
    print("-"*80)
    risk = get_environmental_risk("Los Angeles")
    print(f"City:                {risk.metrics.city}")
    print(f"Risk Level:          {risk.risk_level.value}")
    print(f"Risk Score:          {risk.risk_score}/100")
    print(f"Confidence:          {risk.confidence*100:.0f}%")
    print(f"\nMetrics:")
    print(f"  Air Quality:       AQI {risk.metrics.aqi}")
    print(f"  Pollen Level:      {risk.metrics.pollen_level:.0f}/100")
    print(f"  Humidity:          {risk.metrics.humidity:.0f}%")
    print(f"  Temperature:       {risk.metrics.temperature:.1f}°C")
    print(f"\nExplanation:         {risk.explanation}")
    print(f"Recommendations:")
    for i, rec in enumerate(risk.recommendations, 1):
        print(f"  {i}. {rec}")

    # Test Case 3: Spring allergies
    print("\n" + "-"*80)
    print("TEST 3: Spring Season (High Pollen)")
    print("-"*80)
    risk = get_environmental_risk("New York")
    print(f"City:                {risk.metrics.city}")
    print(f"Risk Level:          {risk.risk_level.value}")
    print(f"Risk Score:          {risk.risk_score}/100")
    print(f"\nMetrics:")
    print(f"  Air Quality:       AQI {risk.metrics.aqi}")
    print(f"  Pollen Level:      {risk.metrics.pollen_level:.0f}/100 (Spring high)")
    print(f"  Humidity:          {risk.metrics.humidity:.0f}%")
    print(f"  Temperature:       {risk.metrics.temperature:.1f}°C")
    print(f"\nExplanation:         {risk.explanation}")

    # Test Case 4: Winter cold
    print("\n" + "-"*80)
    print("TEST 4: Winter Cold Snap (Temperature Trigger)")
    print("-"*80)
    risk = get_environmental_risk("Chicago")
    print(f"City:                {risk.metrics.city}")
    print(f"Risk Level:          {risk.risk_level.value}")
    print(f"Risk Score:          {risk.risk_score}/100")
    print(f"\nMetrics:")
    print(f"  Air Quality:       AQI {risk.metrics.aqi}")
    print(f"  Pollen Level:      {risk.metrics.pollen_level:.0f}/100")
    print(f"  Humidity:          {risk.metrics.humidity:.0f}%")
    print(f"  Temperature:       {risk.metrics.temperature:.1f}°C (Winter)")
    print(f"\nExplanation:         {risk.explanation}")

    # Test Case 5: Very high pollution
    print("\n" + "-"*80)
    print("TEST 5: Extreme Air Pollution (Critical)")
    print("-"*80)
    risk = get_environmental_risk("Beijing")
    print(f"City:                {risk.metrics.city}")
    print(f"Risk Level:          {risk.risk_level.value}")
    print(f"Risk Score:          {risk.risk_score}/100")
    print(f"\nMetrics:")
    print(f"  Air Quality:       AQI {risk.metrics.aqi} (Very Unhealthy)")
    print(f"  Pollen Level:      {risk.metrics.pollen_level:.0f}/100")
    print(f"  Humidity:          {risk.metrics.humidity:.0f}%")
    print(f"  Temperature:       {risk.metrics.temperature:.1f}°C")
    print(f"\nExplanation:         {risk.explanation}")
    print(f"Recommendations:")
    for i, rec in enumerate(risk.recommendations, 1):
        print(f"  {i}. {rec}")

    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80 + "\n")
