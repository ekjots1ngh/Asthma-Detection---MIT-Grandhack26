"""
Test client for the respiratory screening API.

Demonstrates how to use the API endpoints with various scenarios.
"""

import requests
import json
import tempfile
import os
from pathlib import Path
from test_audio_analyzer import (
    create_clear_breathing_audio,
    create_test_audio,
    create_severe_wheeze_audio,
)


class RespiratoryAPIClient:
    """Client for interacting with the respiratory screening API."""

    def __init__(self, base_url: str = 'http://localhost:8000'):
        """Initialize API client.

        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url
        self.session = requests.Session()

    def health_check(self) -> dict:
        """Check API health status."""
        response = self.session.get(f'{self.base_url}/health')
        response.raise_for_status()
        return response.json()

    def get_info(self) -> dict:
        """Get API information."""
        response = self.session.get(f'{self.base_url}/info')
        response.raise_for_status()
        return response.json()

    def get_risk_levels(self) -> dict:
        """Get risk level information."""
        response = self.session.get(f'{self.base_url}/risk-levels')
        response.raise_for_status()
        return response.json()

    def analyze_breathing(self, audio_file_path: str) -> dict:
        """Analyze a breathing audio file.

        Args:
            audio_file_path: Path to audio file

        Returns:
            Analysis results as dictionary
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f'Audio file not found: {audio_file_path}')

        with open(audio_file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(
                f'{self.base_url}/analyze-breathing',
                files=files
            )
            response.raise_for_status()
            return response.json()

    def analyze_batch(self, audio_file_paths: list) -> dict:
        """Analyze multiple audio files.

        Args:
            audio_file_paths: List of paths to audio files

        Returns:
            Batch analysis results
        """
        files = [
            ('files', open(path, 'rb'))
            for path in audio_file_paths
        ]

        try:
            response = self.session.post(
                f'{self.base_url}/batch-analyze',
                files=files
            )
            response.raise_for_status()
            return response.json()
        finally:
            # Close all opened files
            for _, f in files:
                f.close()


def print_analysis_results(filename: str, results: dict) -> None:
    """Pretty print analysis results."""
    print(f'\n{"=" * 70}')
    print(f'Analysis Results: {os.path.basename(filename)}')
    print('=' * 70)

    # Main metrics
    print(f'\nMetrics:')
    print(f'  Wheeze Probability:  {results["wheeze_probability"]:>6.1%}')
    print(f'  Wheeze Intensity:    {results["metrics"]["wheeze_intensity"]:>6.1%}')
    print(f'  Respiratory Rate:    {results["respiratory_rate"]:>6} breaths/min')
    print(f'  Risk Level:          {results["risk_level"].upper():>6}')

    # Guidance
    guidance = results['guidance']
    print(f'\nGuidance:')
    print(f'  Title:           {guidance["emoji"]} {guidance["title"]}')
    print(f'  Message:         {guidance["message"]}')
    print(f'  Recommendation:  {guidance["recommendation"]}')
    print('=' * 70)


def test_single_file_analysis(client: RespiratoryAPIClient) -> None:
    """Test analyzing a single breathing file."""
    print('\n' + '=' * 70)
    print('Test 1: Single File Analysis')
    print('=' * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test audio
        audio_file = os.path.join(tmpdir, 'breathing_sample.wav')
        create_test_audio(audio_file, duration=8.0)

        print(f'\nUploading: {os.path.basename(audio_file)}')

        try:
            results = client.analyze_breathing(audio_file)
            print_analysis_results(audio_file, results)
        except requests.exceptions.RequestException as e:
            print(f'❌ Error: {e}')


def test_multiple_recordings(client: RespiratoryAPIClient) -> None:
    """Test analyzing different breathing patterns."""
    print('\n' + '=' * 70)
    print('Test 2: Multiple Breathing Patterns')
    print('=' * 70)

    test_cases = [
        ('Clear Breathing', create_clear_breathing_audio, 'low'),
        ('Moderate Wheeze', create_test_audio, 'medium'),
        ('Severe Wheeze', create_severe_wheeze_audio, 'high'),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        results_list = []

        for name, generator, expected_risk in test_cases:
            audio_file = os.path.join(tmpdir, f'{name.lower().replace(" ", "_")}.wav')
            generator(audio_file, duration=6.0)

            print(f'\nAnalyzing: {name}')

            try:
                results = client.analyze_breathing(audio_file)
                results_list.append((name, results, expected_risk))
                print_analysis_results(audio_file, results)

                # Verify risk level
                actual_risk = results['risk_level']
                if actual_risk == expected_risk:
                    print(f'✓ Risk level correct: {actual_risk}')
                else:
                    print(f'⚠ Risk level mismatch: expected {expected_risk}, got {actual_risk}')

            except requests.exceptions.RequestException as e:
                print(f'❌ Error: {e}')

        # Summary
        if results_list:
            print('\n' + '=' * 70)
            print('Summary of Results')
            print('=' * 70)
            for name, results, _ in results_list:
                print(f'{name:20} - Risk: {results["risk_level"].upper():6} '
                      f'(Prob: {results["wheeze_probability"]:.0%})')


def test_batch_analysis(client: RespiratoryAPIClient) -> None:
    """Test batch analysis of multiple files."""
    print('\n' + '=' * 70)
    print('Test 3: Batch Analysis')
    print('=' * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create multiple test files
        files = []
        generators = [
            ('clear.wav', create_clear_breathing_audio),
            ('moderate.wav', create_test_audio),
            ('severe.wav', create_severe_wheeze_audio),
        ]

        for filename, generator in generators:
            filepath = os.path.join(tmpdir, filename)
            generator(filepath, duration=5.0)
            files.append(filepath)

        print(f'\nUploading {len(files)} files for batch analysis...')

        try:
            batch_results = client.analyze_batch(files)

            print(f'\nBatch Analysis Results:')
            print('=' * 70)

            for result in batch_results['results']:
                if 'error' in result:
                    print(f'❌ {result["filename"]}: {result["error"]}')
                else:
                    risk = result['risk_level'].upper()
                    prob = result['wheeze_probability']
                    rr = result['respiratory_rate']
                    print(f'✓ {result["filename"]:20} Risk: {risk:6} Prob: {prob:.0%} RR: {rr} bpm')

        except requests.exceptions.RequestException as e:
            print(f'❌ Batch analysis failed: {e}')


def test_api_info(client: RespiratoryAPIClient) -> None:
    """Test getting API information."""
    print('\n' + '=' * 70)
    print('Test 4: API Information Endpoints')
    print('=' * 70)

    try:
        # Health check
        print('\n1. Health Check:')
        health = client.health_check()
        print(f'   Status: {health["status"]}')
        print(f'   Service: {health["service"]}')
        print(f'   Version: {health["version"]}')

        # API info
        print('\n2. API Info:')
        info = client.get_info()
        print(f'   Name: {info["api_name"]}')
        print(f'   Version: {info["version"]}')
        print(f'   Supported Formats: {", ".join(info["supported_formats"])}')
        print(f'   Max File Size: {info["max_file_size_mb"]}MB')
        print(f'   Max Batch Files: {info["max_batch_files"]}')

        # Risk levels
        print('\n3. Risk Levels:')
        risk_info = client.get_risk_levels()
        for risk_level, guidance in risk_info['risk_levels'].items():
            print(f'   {risk_level.upper():7} - {guidance["message"]}')

    except requests.exceptions.RequestException as e:
        print(f'❌ Error: {e}')


def test_error_handling(client: RespiratoryAPIClient) -> None:
    """Test API error handling."""
    print('\n' + '=' * 70)
    print('Test 5: Error Handling')
    print('=' * 70)

    # Test 1: Invalid file type
    print('\n1. Testing invalid file type:')
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        f.write(b'This is not an audio file')
        temp_file = f.name

    try:
        client.analyze_breathing(temp_file)
        print('   ❌ Should have rejected invalid file type')
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            print(f'   ✓ Correctly rejected: {e.response.json()["detail"]}')
        else:
            print(f'   ❌ Unexpected error: {e}')
    finally:
        os.remove(temp_file)

    # Test 2: Non-existent file
    print('\n2. Testing non-existent file:')
    try:
        client.analyze_breathing('/nonexistent/file.wav')
        print('   ❌ Should have raised FileNotFoundError')
    except FileNotFoundError as e:
        print(f'   ✓ Correctly raised error: {e}')

    print('\n' + '=' * 70)


def main():
    """Run all API tests."""
    print('\n' + '=' * 70)
    print('Respiratory Screening API - Test Suite')
    print('=' * 70)

    # Create client
    client = RespiratoryAPIClient('http://localhost:8000')

    # Test connection
    print('\nTesting API connection...')
    try:
        health = client.health_check()
        print(f'✓ API is running ({health["service"]} v{health["version"]})')
    except requests.exceptions.ConnectionError:
        print('❌ Cannot connect to API server')
        print('\nTo run the server, use:')
        print('  uvicorn api_server:app --reload --host 0.0.0.0 --port 8000')
        return
    except Exception as e:
        print(f'❌ Error: {e}')
        return

    # Run tests
    try:
        test_api_info(client)
        test_single_file_analysis(client)
        test_multiple_recordings(client)
        test_batch_analysis(client)
        test_error_handling(client)

        print('\n' + '=' * 70)
        print('✓ All tests completed successfully!')
        print('=' * 70 + '\n')

    except KeyboardInterrupt:
        print('\n\nTests interrupted by user')


if __name__ == '__main__':
    main()
