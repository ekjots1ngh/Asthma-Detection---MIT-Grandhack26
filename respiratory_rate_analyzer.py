#!/usr/bin/env python3
"""
Respiratory Rate Analyzer
=========================

Estimates respiratory rate from breathing audio recordings by detecting
inhale/exhale cycles using spectral envelope analysis.

Features:
  - Load audio from WAV files
  - Detect breathing cycles using STFT envelope
  - Calculate breaths per minute (BPM)
  - Visualize detected cycles
  - Export respiratory rate metrics

Usage:
    python respiratory_rate_analyzer.py samples/normal_breathing.wav

    or programmatically:

    from respiratory_rate_analyzer import RespiratoryRateEstimator

    estimator = RespiratoryRateEstimator()
    respiratory_rate, cycles = estimator.estimate_rate(audio_path)
    estimator.plot_analysis(audio_path, cycles)

Theory:
    Respiratory rate is estimated by:
    1. Computing Short-Time Fourier Transform (STFT)
    2. Extracting energy envelope of breathing band (0.2-0.8 Hz)
    3. Finding peaks in the envelope (inhale/exhale transitions)
    4. Measuring time between peaks
    5. Converting to breaths per minute

    Normal ranges:
    - Infant (0-3 months):  30-40 breaths/min
    - Infant (3-6 months):  25-35 breaths/min
    - Child (6-12 months):  25-35 breaths/min
    - Toddler (1-3 years):  20-30 breaths/min
    - Child (3-12 years):   18-25 breaths/min
    - Adolescent (12+ years): 12-20 breaths/min
    - Adult:                12-20 breaths/min

Author: Health Hackathon Team
License: MIT
"""

import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import find_peaks, savgol_filter
from typing import Tuple, Dict, List
import argparse
from pathlib import Path


class RespiratoryRateEstimator:
    """Estimates respiratory rate from breathing audio."""

    # Breathing frequency range in Hz
    BREATHING_FREQ_MIN = 0.15  # 9 breaths per minute
    BREATHING_FREQ_MAX = 1.0   # 60 breaths per minute

    # STFT parameters
    STFT_N_FFT = 2048      # FFT window size
    STFT_HOP_LENGTH = 512  # Samples between frames

    def __init__(self, sr: int = 22050):
        """
        Initialize respiratory rate estimator.

        Args:
            sr: Sample rate in Hz (default 22050)
        """
        self.sr = sr
        self.n_fft = self.STFT_N_FFT
        self.hop_length = self.STFT_HOP_LENGTH

    def load_audio(self, audio_path: str) -> Tuple[np.ndarray, int]:
        """
        Load audio file.

        Args:
            audio_path: Path to WAV file

        Returns:
            Tuple of (audio_time_series, sample_rate)
        """
        y, sr = librosa.load(audio_path, sr=self.sr)
        return y, sr

    def _compute_energy_envelope(self, y: np.ndarray) -> np.ndarray:
        """
        Compute energy envelope of audio signal.

        Uses Short-Time Fourier Transform (STFT) to extract
        the energy envelope, which represents breathing intensity
        over time.

        Args:
            y: Audio time series

        Returns:
            Energy envelope (normalized to 0-1 range)
        """
        # Compute STFT
        D = librosa.stft(y, n_fft=self.n_fft, hop_length=self.hop_length)

        # Compute power spectrogram
        S = np.abs(D) ** 2

        # Sum across frequency axis to get energy per frame
        envelope = np.sqrt(np.sum(S, axis=0))

        # Normalize to 0-1 range
        envelope_min = np.min(envelope)
        envelope_max = np.max(envelope)
        envelope_normalized = (envelope - envelope_min) / (
            envelope_max - envelope_min + 1e-8
        )

        return envelope_normalized

    def _extract_breathing_frequency(self, envelope: np.ndarray) -> np.ndarray:
        """
        Extract breathing frequency from energy envelope.

        Applies FFT to the envelope to find dominant frequencies
        in the breathing range (0.2-0.8 Hz).

        Args:
            envelope: Energy envelope (time domain)

        Returns:
            Frequency domain representation
        """
        # Apply FFT to envelope
        envelope_fft = np.abs(np.fft.fft(envelope))

        # Frequency axis
        freqs = np.fft.fftfreq(len(envelope), d=self.hop_length / self.sr)

        # Extract positive frequencies only
        positive_freqs_mask = freqs > 0
        freqs_positive = freqs[positive_freqs_mask]
        magnitude_positive = envelope_fft[positive_freqs_mask]

        # Mask breathing frequency range
        breathing_mask = (freqs_positive >= self.BREATHING_FREQ_MIN) & (
            freqs_positive <= self.BREATHING_FREQ_MAX
        )

        # Return magnitudes in breathing range
        return magnitude_positive[breathing_mask], freqs_positive[breathing_mask]

    def _detect_breathing_cycles(
        self, envelope: np.ndarray, sr: int
    ) -> Tuple[List[int], np.ndarray]:
        """
        Detect breathing cycles by finding peaks in envelope.

        Each peak represents a maximum intensity point in the
        breathing cycle (typically during inhalation peak or
        exhalation peak).

        Args:
            envelope: Energy envelope (normalized)
            sr: Sample rate

        Returns:
            Tuple of (peak_indices, peak_times_seconds)
        """
        # Convert frames to time
        time_axis = np.arange(len(envelope)) * self.hop_length / sr

        # Smooth envelope to reduce noise
        if len(envelope) > 5:
            envelope_smooth = savgol_filter(
                envelope, window_length=min(11, len(envelope) // 2 + 1), polyorder=3
            )
        else:
            envelope_smooth = envelope

        # Find peaks with minimum distance constraint
        # Minimum distance = 0.5 Hz → 2 seconds between peaks (minimum breathing interval)
        min_distance = int(2 * sr / self.hop_length)  # samples between frames

        peaks, properties = find_peaks(
            envelope_smooth, height=np.max(envelope_smooth) * 0.3, distance=min_distance
        )

        # Convert frame indices to time (seconds)
        peak_times = time_axis[peaks]

        return peaks, peak_times

    def estimate_rate(self, audio_path: str) -> Dict:
        """
        Estimate respiratory rate from audio file.

        Args:
            audio_path: Path to WAV file

        Returns:
            Dictionary with respiratory metrics:
            {
                'respiratory_rate': float (breaths/min),
                'num_cycles': int,
                'cycle_times': list of cycle durations (seconds),
                'mean_cycle_time': float (seconds),
                'std_cycle_time': float (seconds),
                'confidence': float (0-1),
                'duration': float (seconds),
                'sample_rate': int
            }
        """
        # Load audio
        y, sr = self.load_audio(audio_path)
        duration = len(y) / sr

        # Compute energy envelope
        envelope = self._compute_energy_envelope(y)

        # Detect breathing cycles
        peaks, peak_times = self._detect_breathing_cycles(envelope, sr)

        # Calculate respiratory rate from detected cycles
        if len(peak_times) < 2:
            # Not enough peaks to calculate rate
            return {
                'respiratory_rate': 0.0,
                'num_cycles': len(peaks),
                'cycle_times': [],
                'mean_cycle_time': 0.0,
                'std_cycle_time': 0.0,
                'confidence': 0.0,
                'duration': duration,
                'sample_rate': sr,
                'error': 'Insufficient breathing cycles detected'
            }

        # Calculate time between peaks (cycle durations)
        cycle_times = np.diff(peak_times)

        # Calculate respiratory rate
        # Each cycle represents one complete breath (inhale + exhale)
        mean_cycle_time = np.mean(cycle_times)
        respiratory_rate = 60.0 / mean_cycle_time  # Convert to breaths/min

        # Calculate confidence based on variance
        # Lower variance = higher confidence
        std_cycle_time = np.std(cycle_times)
        cv = std_cycle_time / mean_cycle_time if mean_cycle_time > 0 else 1.0
        confidence = np.exp(-cv)  # Exponential decay: low CV → high confidence

        return {
            'respiratory_rate': float(respiratory_rate),
            'num_cycles': int(len(peaks)),
            'cycle_times': cycle_times.tolist(),
            'mean_cycle_time': float(mean_cycle_time),
            'std_cycle_time': float(std_cycle_time),
            'confidence': float(confidence),
            'duration': float(duration),
            'sample_rate': int(sr),
            'peak_indices': peaks.tolist(),
            'peak_times': peak_times.tolist(),
            'envelope': envelope.tolist()
        }

    def plot_analysis(
        self,
        audio_path: str,
        figsize: Tuple[int, int] = (14, 10),
        save_path: str = None
    ) -> None:
        """
        Plot comprehensive respiratory rate analysis.

        Creates a 4-panel figure showing:
        1. Waveform with detected breathing cycles
        2. Energy envelope with peak detection
        3. Breathing frequency spectrum
        4. Respiratory rate metrics and confidence

        Args:
            audio_path: Path to WAV file
            figsize: Figure size (width, height)
            save_path: Optional path to save figure
        """
        # Load audio
        y, sr = self.load_audio(audio_path)
        duration = len(y) / sr
        time_axis = np.arange(len(y)) / sr

        # Estimate respiratory rate
        results = self.estimate_rate(audio_path)

        # Compute envelope
        envelope = self._compute_energy_envelope(y)
        envelope_time = np.arange(len(envelope)) * self.hop_length / sr

        # Detect cycles
        peaks, peak_times = self._detect_breathing_cycles(envelope, sr)

        # Get breathing frequency spectrum
        freq_mag, freq_axis = self._extract_breathing_frequency(envelope)

        # Create figure with 4 subplots
        fig, axes = plt.subplots(4, 1, figsize=figsize)
        fig.suptitle(
            f'Respiratory Rate Analysis: {Path(audio_path).name}',
            fontsize=16,
            fontweight='bold'
        )

        # --- Panel 1: Audio waveform ---
        ax = axes[0]
        ax.plot(time_axis, y, color='steelblue', linewidth=0.8, alpha=0.8)
        ax.set_ylabel('Amplitude', fontsize=10, fontweight='bold')
        ax.set_title('Audio Waveform (10-second recording)', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, duration])

        # --- Panel 2: Energy envelope with peak detection ---
        ax = axes[1]
        ax.plot(
            envelope_time, envelope, color='navy', linewidth=1.5, label='Energy Envelope'
        )
        ax.plot(
            peak_times,
            envelope[peaks],
            'o',
            color='red',
            markersize=8,
            label=f'Detected Peaks (n={len(peaks)})',
            zorder=5
        )

        # Add vertical lines at peaks
        for peak_time in peak_times:
            ax.axvline(peak_time, color='red', alpha=0.2, linestyle='--', linewidth=1)

        ax.set_ylabel('Normalized Energy', fontsize=10, fontweight='bold')
        ax.set_title('Energy Envelope with Detected Breathing Cycles', fontsize=11, fontweight='bold')
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, duration])
        ax.set_ylim([0, 1.05])

        # --- Panel 3: Breathing frequency spectrum ---
        ax = axes[2]
        ax.plot(freq_axis, freq_mag, color='darkgreen', linewidth=2)
        ax.fill_between(freq_axis, freq_mag, alpha=0.3, color='green')

        if len(freq_mag) > 0:
            dominant_freq_idx = np.argmax(freq_mag)
            dominant_freq = freq_axis[dominant_freq_idx]
            ax.plot(
                dominant_freq,
                freq_mag[dominant_freq_idx],
                'r*',
                markersize=15,
                label=f'Dominant Frequency: {dominant_freq:.2f} Hz'
            )
            ax.legend(loc='upper right', fontsize=9)

        ax.set_xlabel('Frequency (Hz)', fontsize=10, fontweight='bold')
        ax.set_ylabel('Magnitude', fontsize=10, fontweight='bold')
        ax.set_title('Breathing Frequency Spectrum (0.15-1.0 Hz)', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3, which='both')
        ax.set_xlim([self.BREATHING_FREQ_MIN, self.BREATHING_FREQ_MAX])

        # --- Panel 4: Respiratory rate metrics ---
        ax = axes[3]
        ax.axis('off')

        # Create metrics text
        metrics_text = self._format_metrics(results)
        ax.text(
            0.05, 0.95, metrics_text,
            transform=ax.transAxes,
            fontsize=11,
            verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )

        # Add cycle time distribution if available
        if len(results['cycle_times']) > 1:
            cycle_times = np.array(results['cycle_times'])
            cycle_durations_text = (
                f"\nCycle Time Distribution:\n"
                f"  Min: {np.min(cycle_times):.2f}s\n"
                f"  Max: {np.max(cycle_times):.2f}s\n"
                f"  Range: {np.max(cycle_times) - np.min(cycle_times):.2f}s"
            )
            ax.text(
                0.50, 0.95, cycle_durations_text,
                transform=ax.transAxes,
                fontsize=11,
                verticalalignment='top',
                fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5)
            )

        plt.tight_layout()

        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Plot saved to: {save_path}")

        plt.show()

    @staticmethod
    def _format_metrics(results: Dict) -> str:
        """Format respiratory metrics as text."""
        rr = results['respiratory_rate']
        num_cycles = results['num_cycles']
        confidence = results['confidence']
        duration = results['duration']
        mean_cycle = results['mean_cycle_time']
        std_cycle = results['std_cycle_time']

        # Determine age group classification
        if rr > 40:
            age_group = "Infant (0-6 months)"
        elif rr > 30:
            age_group = "Infant/Toddler (6-36 months)"
        elif rr > 25:
            age_group = "Child (3-12 years)"
        elif rr > 20:
            age_group = "Adolescent/Adult (12+ years)"
        else:
            age_group = "Slow breathing or adult"

        # Status indicator
        if rr == 0:
            status = "❌ FAILED - No cycles detected"
        elif rr < 9 or rr > 60:
            status = "⚠️  WARNING - Out of normal range"
        else:
            status = "✓ Normal range"

        return (
            f"RESPIRATORY RATE ANALYSIS\n"
            f"{'='*40}\n"
            f"Respiratory Rate:   {rr:.1f} breaths/min\n"
            f"Age Group:          {age_group}\n"
            f"Status:             {status}\n"
            f"\nCycle Information:\n"
            f"  Cycles Detected:  {num_cycles}\n"
            f"  Mean Cycle Time:  {mean_cycle:.2f} seconds\n"
            f"  Std Dev:          {std_cycle:.2f} seconds\n"
            f"\nAnalysis Quality:\n"
            f"  Confidence:       {confidence*100:.1f}%\n"
            f"  Duration:         {duration:.1f} seconds\n"
        )

    def print_summary(self, results: Dict) -> None:
        """Print respiratory rate analysis summary."""
        print("\n" + "=" * 60)
        print("RESPIRATORY RATE ESTIMATION RESULTS")
        print("=" * 60)
        print(f"\nRespiratory Rate:     {results['respiratory_rate']:.1f} breaths/min")
        print(f"Breathing Cycles:     {results['num_cycles']}")
        print(f"Duration:             {results['duration']:.1f} seconds")
        print(f"Confidence:           {results['confidence']*100:.1f}%")
        print(f"Mean Cycle Time:      {results['mean_cycle_time']:.3f} seconds")
        print(f"Cycle Time Std Dev:   {results['std_cycle_time']:.3f} seconds")

        # Age group classification
        rr = results['respiratory_rate']
        if rr > 40:
            print(f"Age Group:            Infant (0-6 months)")
        elif rr > 30:
            print(f"Age Group:            Infant/Toddler (6-36 months)")
        elif rr > 25:
            print(f"Age Group:            Child (3-12 years)")
        elif rr > 20:
            print(f"Age Group:            Adolescent/Adult (12+ years)")
        else:
            print(f"Age Group:            Slow breathing or adult")

        # Normality check
        if rr == 0:
            print(f"Status:               ❌ Failed - No cycles detected")
        elif rr < 9 or rr > 60:
            print(f"Status:               ⚠️  Outside normal range")
        else:
            print(f"Status:               ✓ Within normal range")

        print("\n" + "=" * 60 + "\n")


def main():
    """Command-line interface for respiratory rate estimation."""
    parser = argparse.ArgumentParser(
        description='Estimate respiratory rate from breathing audio',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python respiratory_rate_analyzer.py samples/normal_breathing.wav
  python respiratory_rate_analyzer.py samples/severe_wheeze.wav --save output.png
  python respiratory_rate_analyzer.py samples/mild_wheeze.wav --no-plot
        """
    )

    parser.add_argument('audio_file', help='Path to WAV audio file')
    parser.add_argument(
        '--save',
        type=str,
        default=None,
        help='Save plot to file (PNG/PDF)'
    )
    parser.add_argument(
        '--no-plot',
        action='store_true',
        help='Skip plot visualization'
    )
    parser.add_argument(
        '--sample-rate',
        type=int,
        default=22050,
        help='Sample rate in Hz (default: 22050)'
    )

    args = parser.parse_args()

    # Check file exists
    if not Path(args.audio_file).exists():
        print(f"Error: File not found - {args.audio_file}")
        return 1

    # Create estimator
    estimator = RespiratoryRateEstimator(sr=args.sample_rate)

    # Estimate respiratory rate
    print(f"\nAnalyzing: {args.audio_file}")
    results = estimator.estimate_rate(args.audio_file)

    # Print summary
    estimator.print_summary(results)

    # Plot if requested
    if not args.no_plot:
        print("Generating visualization...")
        estimator.plot_analysis(args.audio_file, save_path=args.save)

    return 0


if __name__ == "__main__":
    exit(main())
