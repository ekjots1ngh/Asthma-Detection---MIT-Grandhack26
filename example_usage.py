#!/usr/bin/env python3
"""
Example usage of the respiratory audio analyzer.

This script demonstrates how to use the audio analyzer with real-world scenarios.
"""

from audio_analyzer import analyze_breathing, RespiratoryAnalyzer
import tempfile
import os
from test_audio_analyzer import (
    create_clear_breathing_audio,
    create_test_audio,
    create_severe_wheeze_audio,
)


def print_results(filename: str, results: dict) -> None:
    """Pretty print analysis results."""
    print(f"\n{'=' * 60}")
    print(f"Analysis Results: {os.path.basename(filename)}")
    print('=' * 60)
    print(f"Wheeze Probability:  {results['wheeze_probability']:>6.1%}")
    print(f"Wheeze Intensity:    {results['wheeze_intensity']:>6.1%}")
    print(f"Respiratory Rate:    {results['respiratory_rate']:>6} breaths/min")
    print(f"Risk Level:          {results['risk_level'].upper():>6}")
    print('=' * 60)


def get_risk_description(risk_level: str) -> str:
    """Get a user-friendly description of the risk level."""
    descriptions = {
        'low': '✓ Clear breathing detected. Child appears to be breathing normally.',
        'medium': '⚠️  Possible wheeze detected. Consider monitoring and consulting '
                  'with a healthcare provider if symptoms persist.',
        'high': '⚠️⚠️  Significant wheeze detected. Please contact your healthcare '
                'provider promptly for evaluation.',
    }
    return descriptions.get(risk_level, 'Unknown risk level')


def example_1_single_file_analysis():
    """Example 1: Analyze a single breathing audio file."""
    print('\n' + '=' * 60)
    print('Example 1: Single File Analysis')
    print('=' * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create sample audio
        audio_file = os.path.join(tmpdir, 'sample_breathing.wav')
        create_test_audio(audio_file, duration=8.0)

        # Analyze
        results = analyze_breathing(audio_file)
        print_results(audio_file, results)

        # Print interpretation
        print('\nInterpretation:')
        print(get_risk_description(results['risk_level']))


def example_2_compare_multiple_recordings():
    """Example 2: Compare multiple recordings from the same patient."""
    print('\n' + '=' * 60)
    print('Example 2: Compare Multiple Recordings')
    print('=' * 60)

    recordings = [
        ('Morning Recording', create_clear_breathing_audio),
        ('Afternoon Recording', create_test_audio),
        ('Evening Recording', create_severe_wheeze_audio),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        results_list = []

        for name, audio_generator in recordings:
            # Create sample audio
            audio_file = os.path.join(tmpdir, f'{name.lower().replace(" ", "_")}.wav')
            audio_generator(audio_file, duration=6.0)

            # Analyze
            results = analyze_breathing(audio_file)
            results['time'] = name
            results_list.append(results)
            print_results(audio_file, results)

        # Compare trends
        print('\n' + '=' * 60)
        print('Trend Analysis Over Time')
        print('=' * 60)
        for results in results_list:
            print(f"\n{results['time']}:")
            print(f"  Wheeze Probability:  {results['wheeze_probability']:.1%}")
            print(f"  Wheeze Intensity:    {results['wheeze_intensity']:.1%}")
            print(f"  Respiratory Rate:    {results['respiratory_rate']} bpm")
            print(f"  Risk Level:          {results['risk_level'].upper()}")


def example_3_batch_processing():
    """Example 3: Batch process multiple patient recordings."""
    print('\n' + '=' * 60)
    print('Example 3: Batch Processing')
    print('=' * 60)

    patients = [
        ('Patient_001_Child', create_clear_breathing_audio),
        ('Patient_002_Child', create_test_audio),
        ('Patient_003_Child', create_severe_wheeze_audio),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        print('\nProcessing patient recordings...\n')

        for patient_id, audio_generator in patients:
            # Create sample audio
            audio_file = os.path.join(tmpdir, f'{patient_id}.wav')
            audio_generator(audio_file, duration=10.0)

            # Analyze
            results = analyze_breathing(audio_file)

            # Display summary
            status = {
                'low': '✓',
                'medium': '⚠',
                'high': '⚠⚠',
            }[results['risk_level']]

            print(f"{status} {patient_id:20} - Risk: {results['risk_level'].upper():6} "
                  f"(Prob: {results['wheeze_probability']:.0%}, "
                  f"RR: {results['respiratory_rate']} bpm)")


def example_4_custom_analyzer():
    """Example 4: Use RespiratoryAnalyzer with custom settings."""
    print('\n' + '=' * 60)
    print('Example 4: Custom Analyzer Configuration')
    print('=' * 60)

    # Create custom analyzer
    analyzer = RespiratoryAnalyzer(sr=22050)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test audio
        audio_file = os.path.join(tmpdir, 'custom_test.wav')
        create_test_audio(audio_file)

        # Analyze with custom analyzer
        results = analyzer.analyze(audio_file)

        print('\nUsing RespiratoryAnalyzer class:')
        print_results(audio_file, results)

        # Show individual metrics
        print('\nDetailed Metrics:')
        print(f"  Wheeze Probability: {results['wheeze_probability']:.4f}")
        print(f"  Wheeze Intensity:   {results['wheeze_intensity']:.4f}")
        print(f"  Respiratory Rate:   {results['respiratory_rate']:.1f} bpm")


def example_5_decision_logic():
    """Example 5: Implement decision logic based on analysis results."""
    print('\n' + '=' * 60)
    print('Example 5: Clinical Decision Logic')
    print('=' * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create multiple test cases
        test_cases = [
            ('Clear Breathing', create_clear_breathing_audio),
            ('Moderate Wheeze', create_test_audio),
            ('Severe Wheeze', create_severe_wheeze_audio),
        ]

        for case_name, generator in test_cases:
            audio_file = os.path.join(tmpdir, f'{case_name.lower().replace(" ", "_")}.wav')
            generator(audio_file)
            results = analyze_breathing(audio_file)

            print(f'\n{case_name}:')
            print('-' * 60)

            # Decision logic
            if results['risk_level'] == 'low':
                action = 'No immediate action required. Continue regular monitoring.'
            elif results['risk_level'] == 'medium':
                action = 'Schedule appointment with healthcare provider. Monitor symptoms.'
            else:  # high
                action = 'Seek prompt medical attention. Consider urgent care visit.'

            print(f"Risk Level: {results['risk_level'].upper()}")
            print(f"Action:     {action}")

            # Additional recommendations based on respiratory rate
            rr = results['respiratory_rate']
            if rr > 40:
                print(f"Note:       Elevated respiratory rate ({rr} bpm) detected.")
            elif rr < 14:
                print(f"Note:       Low respiratory rate ({rr} bpm) detected.")


def main():
    """Run all examples."""
    print('\n' + '=' * 60)
    print('Respiratory Audio Analyzer - Usage Examples')
    print('=' * 60)

    try:
        example_1_single_file_analysis()
        example_2_compare_multiple_recordings()
        example_3_batch_processing()
        example_4_custom_analyzer()
        example_5_decision_logic()

        print('\n' + '=' * 60)
        print('All examples completed successfully!')
        print('=' * 60 + '\n')

    except Exception as e:
        print(f'\n❌ Error running examples: {e}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
