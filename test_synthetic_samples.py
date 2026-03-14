#!/usr/bin/env python3
"""
Synthetic Audio Sample Testing Script
======================================

Tests wheeze detection algorithm against synthetic respiratory samples.
Validates that normal breathing, mild wheeze, severe wheeze, and coughing
are correctly classified.

Usage:
    python test_synthetic_samples.py

Output:
    - Detailed analysis results for each sample
    - Risk level classification accuracy
    - Spectral characteristics summary
    - Sample comparison statistics
"""

import os
import json
from audio_analyzer import RespiratoryAnalyzer


def print_header(title: str) -> None:
    """Print formatted section header."""
    print("\n" + "=" * 90)
    print(title.center(90))
    print("=" * 90)


def print_result(sample_name: str, result: dict, expected: str) -> bool:
    """
    Print formatted result for a sample.

    Args:
        sample_name: Name of the sample file
        result: Analysis result dictionary
        expected: Expected risk level

    Returns:
        True if result matches expected, False otherwise
    """
    match = result['risk_level'].upper() == expected
    status = "✓ PASS" if match else "✗ FAIL"

    print(f"\n{sample_name}")
    print("-" * 90)
    print(f"  Wheeze Probability:    {result['wheeze_probability']:.1%}")
    print(f"  Wheeze Intensity:      {result['wheeze_intensity']:.2f} / 1.0")
    print(f"  Respiratory Rate:      {result['respiratory_rate']} breaths/min")
    print(f"  Risk Level:            {result['risk_level'].upper()}")
    print(f"  Combined Score:        {(0.5 * result['wheeze_probability'] + 0.5 * result['wheeze_intensity']):.2f}")
    print(f"  Status:                {status}")

    return match


def main():
    """Run comprehensive tests on synthetic audio samples."""

    print_header("SYNTHETIC RESPIRATORY AUDIO - ALGORITHM VALIDATION TEST")

    # Initialize analyzer
    analyzer = RespiratoryAnalyzer()

    # Define test cases
    test_cases = [
        {
            'file': 'samples/normal_breathing.wav',
            'name': '1. Normal Breathing',
            'expected': 'LOW',
            'description': 'Clear breathing with minimal wheeze (no respiratory distress)'
        },
        {
            'file': 'samples/mild_wheeze.wav',
            'name': '2. Mild Wheeze',
            'expected': 'MEDIUM',
            'description': 'Intermittent wheeze during exhalation (moderate symptoms)'
        },
        {
            'file': 'samples/severe_wheeze.wav',
            'name': '3. Severe Wheeze',
            'expected': 'HIGH',
            'description': 'Continuous wheeze with multiple harmonics (acute exacerbation)'
        },
        {
            'file': 'samples/coughing.wav',
            'name': '4. Coughing',
            'expected': 'LOW',
            'description': 'Cough bursts (coughs are not wheezes, different frequency profile)'
        }
    ]

    results = []
    passed = 0
    failed = 0

    print_header("ANALYSIS RESULTS")

    for test in test_cases:
        if not os.path.exists(test['file']):
            print(f"\n{test['name']}")
            print("-" * 90)
            print(f"  ERROR: File not found - {test['file']}")
            failed += 1
            continue

        print(f"\n{test['name']}")
        print(f"Description: {test['description']}")

        try:
            result = analyzer.analyze(test['file'])
            is_pass = print_result(test['file'], result, test['expected'])

            if is_pass:
                passed += 1
            else:
                failed += 1

            results.append({
                'name': test['name'],
                'file': test['file'],
                'expected': test['expected'],
                'actual': result['risk_level'].upper(),
                'wheeze_prob': result['wheeze_probability'],
                'wheeze_intensity': result['wheeze_intensity'],
                'respiratory_rate': result['respiratory_rate'],
                'passed': is_pass
            })

        except Exception as e:
            print(f"  ERROR: {str(e)}")
            failed += 1

    # Summary statistics
    print_header("TEST SUMMARY")

    print(f"\nTotal Tests:     {len(results)}")
    print(f"Passed:          {passed} ✓")
    print(f"Failed:          {failed} ✗")
    print(f"Pass Rate:       {(passed / len(results) * 100):.1f}%")

    # Detailed comparison
    print_header("RISK LEVEL CLASSIFICATION COMPARISON")

    print("\nExpected vs Actual:")
    print("-" * 90)
    print(f"{'Sample':<25} {'Expected':<15} {'Actual':<15} {'Status':<20}")
    print("-" * 90)

    for r in results:
        status = "✓ CORRECT" if r['passed'] else f"✗ WRONG (got {r['actual']})"
        print(f"{r['name']:<25} {r['expected']:<15} {r['actual']:<15} {status:<20}")

    # Spectral characteristics
    print_header("SPECTRAL CHARACTERISTICS SUMMARY")

    print("\nProbability & Intensity Distribution:")
    print("-" * 90)
    print(f"{'Sample':<25} {'Probability':<20} {'Intensity':<20}")
    print("-" * 90)

    for r in results:
        print(f"{r['name']:<25} {r['wheeze_prob']:.1%}".ljust(45) + f"{r['wheeze_intensity']:.2f}")

    # Usage instructions
    print_header("USING THESE SAMPLES FOR TESTING")

    print("""
These synthetic samples are designed for testing and validating the wheeze
detection algorithm. Each represents a realistic respiratory scenario:

NORMAL_BREATHING.WAV
  - Represents healthy breathing without wheeze
  - Low frequency content, primarily air movement noise
  - Should score LOW risk (<25% combined score)
  - Use Case: Baseline testing, negative control

MILD_WHEEZE.WAV
  - Represents early asthma symptoms (moderate distress)
  - Intermittent wheeze tones (300 Hz) during exhalation
  - Should score MEDIUM risk (25-50% combined score)
  - Use Case: Early detection validation, sensitivity testing

SEVERE_WHEEZE.WAV
  - Represents acute asthma exacerbation
  - Continuous wheeze with harmonics (250, 500, 625 Hz)
  - Should score HIGH risk (>50% combined score)
  - Use Case: Clinical validation, high-risk detection

COUGHING.WAV
  - Represents cough bursts (not wheeze)
  - Broadband noise (100-3000 Hz), different from wheeze tones
  - Should score LOW risk (<25% combined score)
  - Use Case: Distinguish coughs from wheezes, specificity testing

TESTING APPROACH:
  1. Use as positive/negative controls for algorithm validation
  2. Test mobile app upload and analysis with these files
  3. Validate API response accuracy and formatting
  4. Benchmark performance (processing time, accuracy)
  5. Fine-tune detection thresholds if needed
  6. Demonstrate to judges/stakeholders in hackathon

INTEGRATION WITH MOBILE APP:
  1. Copy samples to mobile app's sample directory
  2. Add UI button to load and analyze pre-recorded samples
  3. Test network integration with real audio analysis
  4. Verify results display and risk level rendering

EXTENDING WITH REAL AUDIO:
  After hackathon, collect real patient data:
  - Use samples as initial training/validation set
  - Collect diverse age groups (infant, child, adolescent)
  - Include various wheeze severities and patterns
  - Implement audio augmentation for robust detection
    """)

    print_header("SAMPLE FILES LOCATION")

    print("""
All synthetic samples are located in the 'samples/' directory:
  - samples/normal_breathing.wav    (~10 seconds, 22.05 kHz)
  - samples/mild_wheeze.wav         (~10 seconds, 22.05 kHz)
  - samples/severe_wheeze.wav       (~10 seconds, 22.05 kHz)
  - samples/coughing.wav            (~10 seconds, 22.05 kHz)

Each file is:
  - 10 seconds duration (matches app recording time)
  - 22050 Hz sample rate (CD quality, mobile-friendly)
  - 16-bit PCM WAV format (standard, uncompressed)
  - ~220 KB file size each
    """)

    # Final status
    print_header("FINAL STATUS")

    if failed == 0:
        print("\n✅ ALL TESTS PASSED - Algorithm is correctly classifying samples\n")
        return 0
    else:
        print(f"\n⚠️  {failed} TEST(S) FAILED - Review algorithm or sample parameters\n")
        return 1


if __name__ == "__main__":
    exit(main())
