"""
Unit tests and examples for respiratory audio analyzer.

This module tests the wheeze detection functionality and provides
examples of how to use the analyzer.
"""

import numpy as np
import librosa
from scipy.io import wavfile
import tempfile
import os
from audio_analyzer import RespiratoryAnalyzer, analyze_breathing


def create_test_audio(filename: str, duration: float = 5.0) -> str:
    """
    Create synthetic test audio with breathing and wheeze patterns.

    Args:
        filename: Output filename
        duration: Duration in seconds

    Returns:
        Path to created audio file
    """
    sr = 22050
    t = np.linspace(0, duration, int(sr * duration))

    # Create breathing pattern (0.3 Hz = 18 breaths/min)
    breathing_freq = 0.3
    breathing = 0.15 * np.sin(2 * np.pi * breathing_freq * t)

    # Add breathing envelope
    envelope = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * breathing_freq * t))

    # Create wheeze signal with two harmonics (400 Hz and 550 Hz)
    wheeze_1 = 0.25 * np.sin(2 * np.pi * 400 * t) * envelope
    wheeze_2 = 0.15 * np.sin(2 * np.pi * 550 * t) * envelope

    # Add some noise
    noise = 0.04 * np.random.randn(len(t))

    # Combine signals
    audio = wheeze_1 + wheeze_2 + breathing + noise
    audio = audio / (np.max(np.abs(audio)) + 1e-8)

    # Save audio file
    wavfile.write(filename, sr, (audio * 32767).astype(np.int16))
    return filename


def create_clear_breathing_audio(filename: str, duration: float = 5.0) -> str:
    """
    Create synthetic test audio with only normal breathing (no wheeze).

    Args:
        filename: Output filename
        duration: Duration in seconds

    Returns:
        Path to created audio file
    """
    sr = 22050
    t = np.linspace(0, duration, int(sr * duration))

    # Create breathing pattern only
    breathing_freq = 0.35
    breathing = 0.5 * np.sin(2 * np.pi * breathing_freq * t)

    # Add low-frequency envelope (chest wall motion)
    envelope = 0.7 + 0.3 * np.abs(np.sin(2 * np.pi * breathing_freq * t))

    # Add very minimal low-frequency turbulence only (< 100 Hz)
    low_freq_component = 0.08 * np.sin(2 * np.pi * 50 * t) * envelope

    # Very minimal noise focused at low frequencies
    noise = 0.02 * np.random.randn(len(t))

    # Combine signals - mostly just breathing with minimal high-frequency content
    audio = breathing + low_freq_component + noise
    audio = audio / (np.max(np.abs(audio)) + 1e-8)

    # Save audio file
    wavfile.write(filename, sr, (audio * 32767).astype(np.int16))
    return filename


def create_severe_wheeze_audio(filename: str, duration: float = 5.0) -> str:
    """
    Create synthetic test audio with pronounced wheeze patterns.

    Args:
        filename: Output filename
        duration: Duration in seconds

    Returns:
        Path to created audio file
    """
    sr = 22050
    t = np.linspace(0, duration, int(sr * duration))

    # Create breathing pattern
    breathing_freq = 0.4  # Faster breathing
    breathing = 0.1 * np.sin(2 * np.pi * breathing_freq * t)

    # Strong breathing envelope
    envelope = 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * breathing_freq * t))

    # Multiple wheeze frequencies with harmonics (common in asthma)
    wheeze_1 = 0.5 * np.sin(2 * np.pi * 300 * t) * envelope
    wheeze_2 = 0.4 * np.sin(2 * np.pi * 450 * t) * envelope
    wheeze_3 = 0.35 * np.sin(2 * np.pi * 700 * t) * envelope

    # Add small noise component
    noise = 0.02 * np.random.randn(len(t))

    # Combine signals - wheeze dominates in this case
    audio = wheeze_1 + wheeze_2 + wheeze_3 + breathing + noise
    audio = audio / (np.max(np.abs(audio)) + 1e-8)

    # Save audio file
    wavfile.write(filename, sr, (audio * 32767).astype(np.int16))
    return filename


def test_analyzer():
    """Test the analyzer with synthetic audio samples."""
    print('=' * 60)
    print('Respiratory Audio Analyzer - Test Suite')
    print('=' * 60)

    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test 1: Clear breathing (low risk)
        print('\nTest 1: Clear Breathing Audio')
        print('-' * 60)
        clear_file = os.path.join(tmpdir, 'clear_breathing.wav')
        create_clear_breathing_audio(clear_file)

        results = analyze_breathing(clear_file)
        print(f'Wheeze Probability: {results["wheeze_probability"]:.2%}')
        print(f'Wheeze Intensity: {results["wheeze_intensity"]:.2%}')
        print(f'Respiratory Rate: {results["respiratory_rate"]} breaths/min')
        print(f'Risk Level: {results["risk_level"].upper()}')
        assert results['risk_level'] == 'low', 'Clear breathing should be low risk'

        # Test 2: Moderate wheeze (medium risk)
        print('\nTest 2: Moderate Wheeze Audio')
        print('-' * 60)
        wheeze_file = os.path.join(tmpdir, 'wheeze.wav')
        create_test_audio(wheeze_file)

        results = analyze_breathing(wheeze_file)
        print(f'Wheeze Probability: {results["wheeze_probability"]:.2%}')
        print(f'Wheeze Intensity: {results["wheeze_intensity"]:.2%}')
        print(f'Respiratory Rate: {results["respiratory_rate"]} breaths/min')
        print(f'Risk Level: {results["risk_level"].upper()}')
        assert results['risk_level'] in ['medium', 'high'], 'Should detect wheeze pattern'

        # Test 3: Severe wheeze (high risk)
        print('\nTest 3: Severe Wheeze Audio')
        print('-' * 60)
        severe_file = os.path.join(tmpdir, 'severe_wheeze.wav')
        create_severe_wheeze_audio(severe_file)

        results = analyze_breathing(severe_file)
        print(f'Wheeze Probability: {results["wheeze_probability"]:.2%}')
        print(f'Wheeze Intensity: {results["wheeze_intensity"]:.2%}')
        print(f'Respiratory Rate: {results["respiratory_rate"]} breaths/min')
        print(f'Risk Level: {results["risk_level"].upper()}')
        assert results['wheeze_intensity'] > 0.2, 'Should detect significant wheeze pattern'
        assert results['risk_level'] == 'high', 'Severe wheeze should be high risk'

    print('\n' + '=' * 60)
    print('All tests passed! ✓')
    print('=' * 60)


def demonstrate_analysis():
    """Demonstrate the analyzer with different audio patterns."""
    print('\n' + '=' * 60)
    print('Analyzer Features Demonstration')
    print('=' * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        analyzer = RespiratoryAnalyzer()

        print('\nFeature 1: Frequency Analysis (100-1000 Hz wheeze range)')
        print('- Uses FFT with Hamming window for spectral analysis')
        print('- Savitzky-Golay filter for smooth magnitude spectrum')
        print('- Detects concentrated energy patterns characteristic of wheeze')

        print('\nFeature 2: Wheeze Detection Metrics')
        print('- Wheeze Probability: Based on energy ratio & spectral concentration')
        print('- Wheeze Intensity: Peak magnitude, mean magnitude, & variance')
        print('- Combined scoring for robust detection')

        print('\nFeature 3: Respiratory Rate Estimation')
        print('- Analyzes breathing envelope using STFT')
        print('- Detects dominant frequency in 0.2-0.8 Hz range (12-48 BPM)')
        print('- Validates result within physiological bounds (12-60 BPM)')

        print('\nFeature 4: Risk Level Classification')
        print('- Low Risk: < 30% combined score')
        print('- Medium Risk: 30-60% combined score')
        print('- High Risk: > 60% combined score')

        print('\nTesting on sample audio...')
        test_file = os.path.join(tmpdir, 'test.wav')
        create_test_audio(test_file, duration=10.0)

        results = analyze_breathing(test_file)
        print(f'\nSample Results:')
        print(f'  Wheeze Probability: {results["wheeze_probability"]:.1%}')
        print(f'  Wheeze Intensity: {results["wheeze_intensity"]:.1%}')
        print(f'  Respiratory Rate: {results["respiratory_rate"]} breaths/min')
        print(f'  Risk Level: {results["risk_level"].upper()}')


def validate_output_format():
    """Validate that output matches required format."""
    print('\n' + '=' * 60)
    print('Output Format Validation')
    print('=' * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, 'test.wav')
        create_test_audio(test_file)

        results = analyze_breathing(test_file)

        print('\nRequired Output Format:')
        print('{')
        print(f'  "wheeze_probability": {results["wheeze_probability"]} (float, 0-1),')
        print(f'  "wheeze_intensity": {results["wheeze_intensity"]} (float, 0-1),')
        print(f'  "respiratory_rate": {results["respiratory_rate"]} (int, bpm),')
        print(f'  "risk_level": "{results["risk_level"]}" (str: low/medium/high)')
        print('}')

        # Validate types
        assert isinstance(results['wheeze_probability'], float), 'Should be float'
        assert isinstance(results['wheeze_intensity'], float), 'Should be float'
        assert isinstance(results['respiratory_rate'], int), 'Should be int'
        assert results['risk_level'] in ['low', 'medium', 'high'], 'Should be valid risk'

        # Validate ranges
        assert 0 <= results['wheeze_probability'] <= 1, 'Probability out of range'
        assert 0 <= results['wheeze_intensity'] <= 1, 'Intensity out of range'
        assert 12 <= results['respiratory_rate'] <= 60, 'RR out of physiological range'

        print('\n✓ Output format valid and all values in correct ranges')


if __name__ == '__main__':
    test_analyzer()
    demonstrate_analysis()
    validate_output_format()
