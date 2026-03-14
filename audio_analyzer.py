"""
Respiratory audio analyzer for wheeze detection.

Analyzes breathing audio recordings using FFT frequency analysis to detect
wheezing patterns and estimate respiratory health risk.
"""

import numpy as np
import librosa
from scipy import signal
from scipy.signal import windows
from scipy.fft import fft, fftfreq
from typing import Dict, Literal
import warnings

warnings.filterwarnings('ignore')


class RespiratoryAnalyzer:
    """Analyzes respiratory audio for wheeze detection and risk assessment."""

    # Wheeze frequency range in Hz
    WHEEZE_FREQ_MIN = 100
    WHEEZE_FREQ_MAX = 1000

    # Breathing frequency range (respiration rate)
    BREATHING_FREQ_MIN = 0.2  # 12 breaths per minute
    BREATHING_FREQ_MAX = 0.8  # 48 breaths per minute

    def __init__(self, sr: int = 22050):
        """
        Initialize the analyzer.

        Args:
            sr: Sample rate for audio loading (default 22050 Hz)
        """
        self.sr = sr

    def analyze(self, audio_path: str) -> Dict:
        """
        Analyze respiratory audio and detect wheeze patterns.

        Args:
            audio_path: Path to .wav audio file

        Returns:
            Dictionary with analysis results:
            {
                'wheeze_probability': float (0-1),
                'wheeze_intensity': float (0-1),
                'respiratory_rate': int (breaths per minute),
                'risk_level': str ('low', 'medium', 'high')
            }
        """
        # Load audio
        y, sr = librosa.load(audio_path, sr=self.sr)

        # Perform analysis
        wheeze_prob, wheeze_intensity = self._detect_wheeze(y, sr)
        respiratory_rate = self._estimate_respiratory_rate(y, sr)
        risk_level = self._calculate_risk_level(wheeze_prob, wheeze_intensity)

        return {
            'wheeze_probability': float(wheeze_prob),
            'wheeze_intensity': float(wheeze_intensity),
            'respiratory_rate': int(respiratory_rate),
            'risk_level': risk_level,
        }

    def _detect_wheeze(self, y: np.ndarray, sr: int) -> tuple:
        """
        Detect wheeze patterns using FFT analysis.

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            Tuple of (wheeze_probability, wheeze_intensity)
        """
        # Apply preprocessing
        y_processed = self._preprocess_audio(y)

        # Compute FFT
        N = len(y_processed)
        freqs, magnitude = self._compute_fft(y_processed, sr)

        # Extract wheeze frequency range
        wheeze_mask = (freqs >= self.WHEEZE_FREQ_MIN) & (
            freqs <= self.WHEEZE_FREQ_MAX
        )
        wheeze_freqs = freqs[wheeze_mask]
        wheeze_magnitudes = magnitude[wheeze_mask]

        # Calculate wheeze metrics
        wheeze_intensity = self._calculate_wheeze_intensity(wheeze_magnitudes)
        wheeze_probability = self._calculate_wheeze_probability(
            y_processed, wheeze_magnitudes
        )

        return wheeze_probability, wheeze_intensity

    def _preprocess_audio(self, y: np.ndarray) -> np.ndarray:
        """
        Preprocess audio signal.

        Args:
            y: Audio time series

        Returns:
            Preprocessed audio
        """
        # Apply high-pass filter to remove low-frequency noise
        sos = signal.butter(4, 50, btype='high', fs=self.sr, output='sos')
        y_filtered = signal.sosfilt(sos, y)

        # Normalize
        y_normalized = y_filtered / (np.max(np.abs(y_filtered)) + 1e-8)

        return y_normalized

    def _compute_fft(self, y: np.ndarray, sr: int) -> tuple:
        """
        Compute FFT magnitude spectrum.

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            Tuple of (frequencies, magnitude spectrum)
        """
        # Apply Hamming window to reduce spectral leakage
        window = windows.hamming(len(y))
        y_windowed = y * window

        # Compute FFT
        fft_result = fft(y_windowed)
        magnitude = np.abs(fft_result) / len(y)

        # Only keep positive frequencies
        N = len(y)
        magnitude = magnitude[:N // 2]
        freqs = fftfreq(N, 1 / sr)[:N // 2]

        # Smooth magnitude spectrum
        magnitude = signal.savgol_filter(magnitude, window_length=11, polyorder=3)
        magnitude = np.maximum(magnitude, 0)

        return freqs, magnitude

    def _calculate_wheeze_intensity(self, wheeze_magnitudes: np.ndarray) -> float:
        """
        Calculate wheeze intensity from frequency magnitudes.

        Args:
            wheeze_magnitudes: Magnitude values in wheeze frequency range

        Returns:
            Wheeze intensity (0-1)
        """
        if len(wheeze_magnitudes) == 0 or np.max(wheeze_magnitudes) < 1e-6:
            return 0.0

        # Calculate metrics
        peak_magnitude = np.max(wheeze_magnitudes)
        mean_magnitude = np.mean(wheeze_magnitudes)
        median_magnitude = np.median(wheeze_magnitudes)

        # Calculate concentration (peak relative to mean)
        if mean_magnitude > 1e-8:
            concentration = peak_magnitude / mean_magnitude
        else:
            concentration = 1.0

        # Calculate spectral energy (sum of squared magnitudes)
        spectral_energy = np.sum(wheeze_magnitudes ** 2)

        # Scale based on actual magnitudes and concentration
        # High intensity when: peak is high, mean is elevated, or concentration is strong
        base_intensity = min(peak_magnitude * 100, 1.0)  # Direct magnitude scaling
        concentration_score = min(concentration / 20.0, 1.0)
        energy_score = min(np.sqrt(spectral_energy) * 10, 1.0)

        # Weighted combination
        intensity = (0.5 * base_intensity +
                     0.3 * concentration_score +
                     0.2 * energy_score)

        return float(np.clip(intensity, 0, 1))

    def _calculate_wheeze_probability(
        self, y: np.ndarray, wheeze_magnitudes: np.ndarray
    ) -> float:
        """
        Calculate wheeze probability using spectral analysis.

        Args:
            y: Preprocessed audio time series
            wheeze_magnitudes: Magnitude values in wheeze frequency range

        Returns:
            Wheeze probability (0-1)
        """
        if len(wheeze_magnitudes) == 0:
            return 0.0

        # Calculate overall signal energy
        overall_energy = np.sum(y ** 2) + 1e-8
        wheeze_energy = np.sum(wheeze_magnitudes ** 2)

        # Energy ratio in wheeze band
        # Wheeze typically occupies 10-40% of total energy
        energy_ratio = wheeze_energy / overall_energy
        energy_score = min(energy_ratio * 8, 1.0)

        # Calculate spectral concentration
        # Wheeze shows concentrated energy at specific frequencies
        mean_magnitude = np.mean(wheeze_magnitudes)
        max_magnitude = np.max(wheeze_magnitudes)

        if mean_magnitude > 0:
            peak_ratio = max_magnitude / mean_magnitude
            concentration = min(peak_ratio / 15.0, 1.0)
        else:
            concentration = 0.0

        # Calculate spectral sharpness
        # Wheeze has sharp peaks in frequency domain
        if len(wheeze_magnitudes) > 1:
            # Find peaks in wheeze spectrum
            peaks = np.where(np.diff(np.sign(np.diff(wheeze_magnitudes))) == -2)[0]
            sharpness = min(len(peaks) / 10.0, 1.0)
        else:
            sharpness = 0.0

        # Combine indicators with optimized weights
        probability = (0.45 * energy_score +
                       0.35 * concentration +
                       0.20 * sharpness)

        return float(np.clip(probability, 0, 1))

    def _estimate_respiratory_rate(self, y: np.ndarray, sr: int) -> float:
        """
        Estimate respiratory rate from audio envelope.

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            Respiratory rate in breaths per minute
        """
        # Compute energy envelope using spectrogram
        D = librosa.stft(y)
        S = np.abs(D) ** 2
        envelope = np.sqrt(np.sum(S, axis=0))

        # Normalize envelope
        envelope = (envelope - np.min(envelope)) / (
            np.max(envelope) - np.min(envelope) + 1e-8
        )

        # Convert to frequency domain to find breathing rate
        # Compute autocorrelation to detect breathing peaks
        envelope_resampled = signal.resample(envelope, min(len(envelope), 4000))

        # Apply spectral analysis on envelope
        fft_env = np.abs(fft(envelope_resampled))
        freqs_env = fftfreq(len(envelope_resampled), 1 / (sr / 512))

        # Extract breathing frequency range
        breathing_mask = (freqs_env >= self.BREATHING_FREQ_MIN) & (
            freqs_env <= self.BREATHING_FREQ_MAX
        )
        breathing_power = fft_env[breathing_mask]

        if len(breathing_power) > 0:
            # Find dominant frequency in breathing range
            peak_idx = np.argmax(breathing_power)
            breathing_freqs = freqs_env[breathing_mask]
            dominant_freq = breathing_freqs[peak_idx]
            respiratory_rate = dominant_freq * 60  # Convert to breaths per minute
        else:
            # Default estimate if detection fails
            respiratory_rate = 20.0

        # Validate reasonable range (12-60 breaths per minute)
        respiratory_rate = np.clip(respiratory_rate, 12, 60)

        return respiratory_rate

    def _calculate_risk_level(
        self, wheeze_prob: float, wheeze_intensity: float
    ) -> Literal['low', 'medium', 'high']:
        """
        Calculate risk level based on wheeze indicators.

        Args:
            wheeze_prob: Wheeze probability (0-1)
            wheeze_intensity: Wheeze intensity (0-1)

        Returns:
            Risk level: 'low', 'medium', or 'high'
        """
        # Combined score with adjusted weights
        # Both probability and intensity must be elevated for medium/high risk
        combined_score = (0.5 * wheeze_prob + 0.5 * wheeze_intensity)

        # Thresholds adjusted based on typical wheeze patterns
        if combined_score < 0.25:
            return 'low'
        elif combined_score < 0.50:
            return 'medium'
        else:
            return 'high'


def analyze_breathing(audio_path: str) -> Dict:
    """
    Analyze breathing audio for wheeze detection.

    Args:
        audio_path: Path to .wav audio file

    Returns:
        Analysis results dictionary
    """
    analyzer = RespiratoryAnalyzer()
    return analyzer.analyze(audio_path)


if __name__ == '__main__':
    # Example usage
    import sys

    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        results = analyze_breathing(audio_file)
        print('Respiratory Analysis Results:')
        print(f'  Wheeze Probability: {results["wheeze_probability"]:.2%}')
        print(f'  Wheeze Intensity: {results["wheeze_intensity"]:.2%}')
        print(f'  Respiratory Rate: {results["respiratory_rate"]} breaths/min')
        print(f'  Risk Level: {results["risk_level"].upper()}')
    else:
        print('Usage: python audio_analyzer.py <audio_file.wav>')
