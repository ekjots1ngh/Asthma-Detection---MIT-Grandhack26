#!/usr/bin/env python3
"""
Cough Detection Algorithm
=========================

Detects cough events in audio recordings by analyzing energy spikes
and spectral characteristics. Returns cough count, timestamps, and
duration estimates.

Features:
  - Onset detection (sudden amplitude spikes)
  - Spectral analysis (distinguish cough from wheeze/speech)
  - Temporal filtering (merge/separate adjacent events)
  - Cough classification (probability scoring)
  - Automatic cough counting and rate estimation

Usage:
    python cough_detector.py samples/coughing.wav

    or programmatically:

    from cough_detector import CoughDetector

    detector = CoughDetector()
    results = detector.detect_coughs('audio.wav')
    detector.plot_results('audio.wav')

Theory:
    Coughs are characterized by:
    - Sudden onset (sharp amplitude spike)
    - Broadband spectrum (all frequencies, unlike wheeze)
    - Duration: typically 100-500 ms per cough
    - Bursts: often 2-5 coughs in rapid sequence
    - No periodic harmonics (unlike speech)

    Detection approach:
    1. Compute energy envelope
    2. Find energy flux (time derivative) peaks
    3. Analyze spectrum of detected events
    4. Calculate spectral entropy (flat = cough, peaked = wheeze)
    5. Filter by duration and spacing
    6. Classify as likely coughs

Author: Health Hackathon Team
License: MIT
"""

import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import find_peaks, hilbert
from typing import Dict, List, Tuple
from pathlib import Path
import argparse


class CoughDetector:
    """Detects cough events in audio recordings."""

    def __init__(self, sr: int = 22050):
        """
        Initialize cough detector.

        Args:
            sr: Sample rate in Hz (default 22050)
        """
        self.sr = sr

        # Cough characteristics (empirically determined)
        self.min_cough_duration = 0.05  # 50 ms minimum
        self.max_cough_duration = 1.0   # 1000 ms maximum
        self.min_cough_energy_ratio = 5.0  # 5x above background (stricter)
        self.max_frequency_range = 4000  # Hz, cough typically <4 kHz

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

    def _compute_energy_envelope(self, y: np.ndarray, hop_length: int = 512) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute energy envelope using STFT.

        Args:
            y: Audio time series
            hop_length: Samples between frames

        Returns:
            Tuple of (envelope, time_axis)
        """
        # Compute STFT
        D = librosa.stft(y, hop_length=hop_length)
        S = np.abs(D) ** 2

        # Sum across frequency axis
        envelope = np.sqrt(np.sum(S, axis=0))

        # Time axis in seconds
        time_axis = np.arange(len(envelope)) * hop_length / self.sr

        # Normalize
        envelope = envelope / (np.max(envelope) + 1e-8)

        return envelope, time_axis

    def _compute_onset_strength(
        self, y: np.ndarray, hop_length: int = 512
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute onset strength (energy flux) using librosa.

        Detects sudden changes in energy (sharp attacks).

        Args:
            y: Audio time series
            hop_length: Samples between frames

        Returns:
            Tuple of (onset_strength, time_axis)
        """
        # Use librosa's onset detection
        onset_env = librosa.onset.onset_strength(y=y, sr=self.sr, hop_length=hop_length)

        # Time axis
        time_axis = np.arange(len(onset_env)) * hop_length / self.sr

        return onset_env, time_axis

    def _detect_onset_peaks(
        self, onset_env: np.ndarray, time_axis: np.ndarray, threshold: float = 0.5
    ) -> Tuple[List[int], List[float]]:
        """
        Find peaks in onset strength (potential cough events).

        Args:
            onset_env: Onset strength
            time_axis: Time axis in seconds
            threshold: Peak height threshold (0-1)

        Returns:
            Tuple of (peak_indices, peak_times_seconds)
        """
        # Normalize to 0-1
        onset_norm = onset_env / (np.max(onset_env) + 1e-8)

        # Find peaks
        min_height = threshold * np.max(onset_norm)
        min_distance = int(0.1 * self.sr / 512)  # At least 100 ms between peaks

        peaks, _ = find_peaks(onset_norm, height=min_height, distance=min_distance)

        # Convert to time
        peak_times = time_axis[peaks]

        return peaks, peak_times

    def _analyze_cough_spectrum(
        self, y: np.ndarray, start_sample: int, end_sample: int
    ) -> Dict:
        """
        Analyze spectral characteristics of a potential cough.

        Measures:
        - Spectral flatness (flat = cough, peaked = wheeze)
        - Dominant frequency (lower for cough, higher for wheeze)
        - Spectral entropy

        Args:
            y: Audio time series
            start_sample: Start sample of event
            end_sample: End sample of event

        Returns:
            Dictionary with spectral metrics
        """
        # Extract event segment
        segment = y[start_sample:end_sample]

        if len(segment) < 256:
            return {
                'spectral_flatness': 0.0,
                'spectral_entropy': 0.0,
                'dominant_frequency': 0.0,
                'is_likely_cough': False
            }

        # Compute FFT
        fft_magnitude = np.abs(np.fft.rfft(segment))
        frequencies = np.fft.rfftfreq(len(segment), 1 / self.sr)

        # Filter to cough frequency range (50-4000 Hz)
        freq_mask = frequencies < self.max_frequency_range
        magnitude_filtered = fft_magnitude[freq_mask]
        frequencies_filtered = frequencies[freq_mask]

        if len(magnitude_filtered) == 0:
            return {
                'spectral_flatness': 0.0,
                'spectral_entropy': 0.0,
                'dominant_frequency': 0.0,
                'is_likely_cough': False
            }

        # Spectral flatness (Wiener entropy)
        # Flat spectrum → high flatness → likely cough
        # Peaked spectrum → low flatness → likely wheeze
        geometric_mean = np.exp(np.mean(np.log(magnitude_filtered + 1e-10)))
        arithmetic_mean = np.mean(magnitude_filtered)
        spectral_flatness = geometric_mean / (arithmetic_mean + 1e-10)

        # Spectral entropy
        # Normalize to probability distribution
        magnitude_norm = magnitude_filtered / (np.sum(magnitude_filtered) + 1e-10)
        spectral_entropy = -np.sum(magnitude_norm * np.log(magnitude_norm + 1e-10))

        # Dominant frequency
        dominant_idx = np.argmax(magnitude_filtered)
        dominant_frequency = frequencies_filtered[dominant_idx]

        # Cough classification
        # Coughs: high flatness (>0.5), low dominant freq (<2000 Hz)
        # Wheezes: low flatness (<0.3), peaked frequency
        is_likely_cough = (spectral_flatness > 0.3 and dominant_frequency < 2500)

        return {
            'spectral_flatness': float(spectral_flatness),
            'spectral_entropy': float(spectral_entropy),
            'dominant_frequency': float(dominant_frequency),
            'is_likely_cough': is_likely_cough
        }

    def _classify_event(
        self,
        onset_strength: float,
        duration: float,
        spectrum_info: Dict,
        background_energy: float,
        peak_energy: float
    ) -> Tuple[bool, float]:
        """
        Classify event as likely cough based on multiple features.

        Strict criteria to avoid false positives:
        - Duration must be in valid range (50-500 ms)
        - Energy must rise sharply (5x+ above background for strict, 2x+ for loose)
        - Spectrum must be broadband (not peaked like wheeze)
        - Onset must be sharp

        Returns: (is_cough, cough_probability)

        Args:
            onset_strength: Peak onset strength
            duration: Event duration in seconds
            spectrum_info: Spectral analysis results
            background_energy: Background noise level
            peak_energy: Peak energy of event

        Returns:
            Tuple of (is_cough, probability_0_to_1)
        """
        score = 0.0
        max_score = 0.0

        # Feature 1: Duration (50-500 ms typical) - STRICT
        max_score += 1.5
        if self.min_cough_duration < duration < self.max_cough_duration:
            score += 1.5
        else:
            # Outside typical range = very unlikely
            score += 0.1

        # Feature 2: Energy rise (strong spike) - STRICT
        max_score += 1.5
        energy_ratio = peak_energy / (background_energy + 1e-8)
        if energy_ratio > 10:
            # Very sharp spike = strong cough indicator
            score += 1.5
        elif energy_ratio > 5:
            # Strong spike
            score += 1.0
        elif energy_ratio > self.min_cough_energy_ratio:
            # Moderate rise
            score += 0.5
        else:
            # Weak rise
            score += 0.1

        # Feature 3: Spectral characteristics (broadband) - IMPORTANT
        max_score += 1.5
        if spectrum_info['is_likely_cough'] and spectrum_info['spectral_flatness'] > 0.4:
            # Broadband spectrum with low dominant freq AND high flatness
            score += 1.5
        elif spectrum_info['spectral_flatness'] > 0.5:
            # Very broadband (flat spectrum)
            score += 1.0
        elif spectrum_info['spectral_flatness'] > 0.4:
            # Reasonably broadband
            score += 0.5
        else:
            # Peaked spectrum (wheeze, breathing-like)
            score += 0.0

        # Feature 4: Onset strength (sharp attack)
        max_score += 1.0
        if onset_strength > 0.7:
            score += 1.0
        elif onset_strength > 0.5:
            score += 0.5
        else:
            score += 0.1

        # Feature 5: Dominant frequency (coughs <2500 Hz, wheezes >2000 Hz)
        max_score += 0.5
        if spectrum_info['dominant_frequency'] < 2000:
            score += 0.5
        elif spectrum_info['dominant_frequency'] < 3000:
            score += 0.2

        # Normalize probability
        probability = score / max_score if max_score > 0 else 0.0
        probability = np.clip(probability, 0.0, 1.0)

        # Decision threshold (stricter) - require higher probability
        is_cough = probability > 0.70

        return is_cough, probability

    def detect_coughs(self, audio_path: str, threshold: float = 0.5) -> Dict:
        """
        Detect cough events in audio file.

        Args:
            audio_path: Path to WAV file
            threshold: Detection threshold (0-1, higher = stricter)

        Returns:
            Dictionary with cough detection results:
            {
                'cough_count': int,
                'coughs_per_minute': float,
                'coughs': [
                    {
                        'timestamp': float (seconds),
                        'duration': float (seconds),
                        'onset_strength': float,
                        'probability': float,
                        'spectrum': dict
                    },
                    ...
                ],
                'duration': float (seconds),
                'background_energy': float,
                'sample_rate': int
            }
        """
        # Load audio
        y, sr = self.load_audio(audio_path)
        duration = len(y) / sr

        # Compute energy envelope
        hop_length = 512
        envelope, time_axis = self._compute_energy_envelope(y, hop_length=hop_length)

        # Compute onset strength
        onset_env, onset_time = self._compute_onset_strength(y, hop_length=hop_length)

        # Find onset peaks
        peaks, peak_times = self._detect_onset_peaks(onset_env, onset_time, threshold=threshold)

        # Calculate background energy (median)
        background_energy = np.median(envelope)

        # Detect coughs at each peak
        coughs = []
        hop_samples = hop_length

        for peak_idx, peak_time in zip(peaks, peak_times):
            # Find window around peak
            peak_sample = int(peak_time * sr)

            # Estimate event duration by finding energy boundaries
            # Look before and after peak for significant energy drop
            before_idx = max(0, peak_idx - 20)  # ~260 ms before
            after_idx = min(len(envelope), peak_idx + 20)  # ~260 ms after

            # Find edges of event (where energy drops below threshold)
            threshold_energy = background_energy * 1.5

            start_idx = before_idx
            for i in range(peak_idx - 1, before_idx - 1, -1):
                if envelope[i] < threshold_energy:
                    start_idx = i + 1
                    break

            end_idx = after_idx
            for i in range(peak_idx + 1, after_idx + 1):
                if envelope[i] < threshold_energy:
                    end_idx = i
                    break

            # Convert to sample indices
            start_sample = int(start_idx * hop_samples)
            end_sample = int(end_idx * hop_samples)

            # Ensure valid range
            start_sample = max(0, start_sample)
            end_sample = min(len(y), end_sample)

            if end_sample <= start_sample:
                continue

            # Event metrics
            event_duration = (end_sample - start_sample) / sr
            peak_energy = envelope[peak_idx]
            onset_strength = onset_env[peak_idx]

            # Spectral analysis
            spectrum_info = self._analyze_cough_spectrum(y, start_sample, end_sample)

            # Classification
            is_cough, probability = self._classify_event(
                onset_strength,
                event_duration,
                spectrum_info,
                background_energy,
                peak_energy
            )

            if is_cough:
                coughs.append({
                    'timestamp': float(peak_time),
                    'duration': float(event_duration),
                    'start_time': float(start_sample / sr),
                    'end_time': float(end_sample / sr),
                    'onset_strength': float(onset_strength),
                    'energy_ratio': float(peak_energy / (background_energy + 1e-8)),
                    'probability': float(probability),
                    'spectrum': spectrum_info
                })

        # Sort by timestamp
        coughs = sorted(coughs, key=lambda x: x['timestamp'])

        # Merge nearby coughs (cough bursts: <200 ms apart)
        merged_coughs = self._merge_cough_bursts(coughs, merge_threshold=0.2)

        # Calculate statistics
        cough_count = len(merged_coughs)
        coughs_per_minute = (cough_count / duration) * 60 if duration > 0 else 0.0

        return {
            'cough_count': int(cough_count),
            'coughs_per_minute': float(coughs_per_minute),
            'coughs': merged_coughs,
            'duration': float(duration),
            'background_energy': float(background_energy),
            'sample_rate': int(sr),
            'threshold': float(threshold)
        }

    @staticmethod
    def _merge_cough_bursts(coughs: List[Dict], merge_threshold: float = 0.2) -> List[Dict]:
        """
        Merge coughs that occur in bursts (within merge_threshold seconds).

        Typical cough bursts: 2-5 coughs within 1-2 seconds.

        Args:
            coughs: List of detected cough events
            merge_threshold: Time window in seconds

        Returns:
            Merged list of cough events
        """
        if not coughs:
            return []

        merged = []
        current_burst = [coughs[0]]

        for cough in coughs[1:]:
            # Check if cough is close to last cough in burst
            if cough['timestamp'] - current_burst[-1]['timestamp'] < merge_threshold:
                # Part of current burst
                current_burst.append(cough)
            else:
                # Start new burst
                # Average burst coughs into single entry
                burst_cough = {
                    'timestamp': current_burst[0]['timestamp'],
                    'duration': sum(c['duration'] for c in current_burst),
                    'start_time': current_burst[0]['start_time'],
                    'end_time': current_burst[-1]['end_time'],
                    'onset_strength': np.mean([c['onset_strength'] for c in current_burst]),
                    'energy_ratio': np.mean([c['energy_ratio'] for c in current_burst]),
                    'probability': np.mean([c['probability'] for c in current_burst]),
                    'burst_count': len(current_burst),
                    'spectrum': current_burst[0]['spectrum']
                }
                merged.append(burst_cough)
                current_burst = [cough]

        # Add last burst
        burst_cough = {
            'timestamp': current_burst[0]['timestamp'],
            'duration': sum(c['duration'] for c in current_burst),
            'start_time': current_burst[0]['start_time'],
            'end_time': current_burst[-1]['end_time'],
            'onset_strength': np.mean([c['onset_strength'] for c in current_burst]),
            'energy_ratio': np.mean([c['energy_ratio'] for c in current_burst]),
            'probability': np.mean([c['probability'] for c in current_burst]),
            'burst_count': len(current_burst),
            'spectrum': current_burst[0]['spectrum']
        }
        merged.append(burst_cough)

        return merged

    def plot_results(
        self,
        audio_path: str,
        figsize: Tuple[int, int] = (14, 10),
        save_path: str = None
    ) -> None:
        """
        Plot cough detection results.

        Creates a 3-panel figure showing:
        1. Waveform with detected coughs highlighted
        2. Energy envelope and onset strength
        3. Cough statistics and metrics

        Args:
            audio_path: Path to WAV file
            figsize: Figure size
            save_path: Optional path to save figure
        """
        # Load audio
        y, sr = self.load_audio(audio_path)
        duration = len(y) / sr
        time_axis = np.arange(len(y)) / sr

        # Detect coughs
        results = self.detect_coughs(audio_path)

        # Compute envelopes
        hop_length = 512
        envelope, envelope_time = self._compute_energy_envelope(y, hop_length=hop_length)
        onset_env, onset_time = self._compute_onset_strength(y, hop_length=hop_length)

        # Create figure
        fig, axes = plt.subplots(3, 1, figsize=figsize)
        fig.suptitle(
            f'Cough Detection Analysis: {Path(audio_path).name}',
            fontsize=16,
            fontweight='bold'
        )

        # --- Panel 1: Waveform ---
        ax = axes[0]
        ax.plot(time_axis, y, color='steelblue', linewidth=0.5, alpha=0.7)

        # Highlight detected coughs
        for cough in results['coughs']:
            cough_start = cough['start_time']
            cough_end = cough['end_time']
            ax.axvspan(cough_start, cough_end, alpha=0.3, color='red')
            ax.text(
                cough_start,
                np.max(y) * 0.9,
                f"{cough['burst_count']}",
                fontsize=8,
                color='red',
                fontweight='bold'
            )

        ax.set_ylabel('Amplitude', fontsize=10, fontweight='bold')
        ax.set_title('Audio Waveform with Detected Coughs (highlighted in red)', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, duration])

        # --- Panel 2: Energy envelope and onset strength ---
        ax = axes[1]
        ax.plot(envelope_time, envelope, color='navy', linewidth=1.5, label='Energy Envelope')
        ax.plot(onset_time, onset_env / np.max(onset_env + 1e-8), color='darkgreen', linewidth=1.5, label='Onset Strength (normalized)')

        # Mark detected cough peaks
        cough_times = [c['timestamp'] for c in results['coughs']]
        for cough_time in cough_times:
            ax.axvline(cough_time, color='red', alpha=0.4, linestyle='--', linewidth=2)

        ax.set_ylabel('Normalized Energy', fontsize=10, fontweight='bold')
        ax.set_title('Energy Envelope and Onset Detection', fontsize=11, fontweight='bold')
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, duration])
        ax.set_ylim([0, 1.1])

        # --- Panel 3: Statistics ---
        ax = axes[2]
        ax.axis('off')

        # Statistics text
        stats_text = self._format_statistics(results)
        ax.text(
            0.05, 0.95, stats_text,
            transform=ax.transAxes,
            fontsize=11,
            verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )

        # Cough list
        cough_list_text = "DETECTED COUGHS:\n" + "-" * 40 + "\n"
        for i, cough in enumerate(results['coughs'], 1):
            cough_list_text += (
                f"Cough {i}: {cough['timestamp']:.2f}s "
                f"({cough['burst_count']} in burst) "
                f"Prob: {cough['probability']*100:.0f}%\n"
            )

        ax.text(
            0.50, 0.95, cough_list_text,
            transform=ax.transAxes,
            fontsize=10,
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
    def _format_statistics(results: Dict) -> str:
        """Format cough statistics as text."""
        return (
            f"COUGH DETECTION RESULTS\n"
            f"{'='*40}\n"
            f"Total Coughs:       {results['cough_count']}\n"
            f"Coughs/Minute:      {results['coughs_per_minute']:.1f}\n"
            f"Duration:           {results['duration']:.1f} seconds\n"
            f"Detection Threshold: {results['threshold']:.1f}\n"
            f"\nStatistics:\n"
            f"  Mean Probability:  {np.mean([c['probability'] for c in results['coughs']])*100:.1f}% " if results['coughs'] else f"\nNo coughs detected\n"
            f"  Mean Energy Rise:  {np.mean([c['energy_ratio'] for c in results['coughs']]):.1f}x" if results['coughs'] else ""
        )

    def print_summary(self, results: Dict) -> None:
        """Print cough detection summary."""
        print("\n" + "=" * 60)
        print("COUGH DETECTION RESULTS")
        print("=" * 60)
        print(f"\nTotal Coughs:       {results['cough_count']}")
        print(f"Coughs per Minute:  {results['coughs_per_minute']:.1f}")
        print(f"Duration:           {results['duration']:.1f} seconds")
        print(f"Detection Threshold: {results['threshold']:.2f}")

        if results['coughs']:
            print(f"\nDetailed Results:")
            print("-" * 60)
            for i, cough in enumerate(results['coughs'], 1):
                print(f"\nCough {i}:")
                print(f"  Time:        {cough['timestamp']:.2f} seconds")
                print(f"  Duration:    {cough['duration']:.3f} seconds")
                print(f"  Probability: {cough['probability']*100:.1f}%")
                print(f"  Energy Rise: {cough['energy_ratio']:.1f}x background")
                if 'burst_count' in cough:
                    print(f"  Burst Size:  {cough['burst_count']} coughs")
        else:
            print("\nNo coughs detected.")

        print("\n" + "=" * 60 + "\n")


def main():
    """Command-line interface for cough detection."""
    parser = argparse.ArgumentParser(
        description='Detect cough events in audio recordings',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cough_detector.py samples/coughing.wav
  python cough_detector.py samples/coughing.wav --save output.png
  python cough_detector.py samples/coughing.wav --threshold 0.3
  python cough_detector.py samples/coughing.wav --no-plot
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
        '--threshold',
        type=float,
        default=0.5,
        help='Detection threshold (0-1, default 0.5)'
    )
    parser.add_argument(
        '--sample-rate',
        type=int,
        default=22050,
        help='Sample rate in Hz (default 22050)'
    )

    args = parser.parse_args()

    # Check file exists
    if not Path(args.audio_file).exists():
        print(f"Error: File not found - {args.audio_file}")
        return 1

    # Create detector
    detector = CoughDetector(sr=args.sample_rate)

    # Detect coughs
    print(f"\nAnalyzing: {args.audio_file}")
    results = detector.detect_coughs(args.audio_file, threshold=args.threshold)

    # Print summary
    detector.print_summary(results)

    # Plot if requested
    if not args.no_plot:
        print("Generating visualization...")
        detector.plot_results(args.audio_file, save_path=args.save)

    return 0


if __name__ == "__main__":
    exit(main())
