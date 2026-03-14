#!/usr/bin/env python3
"""
Synthetic Respiratory Audio Generator
======================================

Generates synthetic .wav files for testing wheeze detection algorithms.
Creates realistic audio samples of normal breathing, wheezing, and coughing.

Usage:
    python generate_synthetic_audio.py

Output:
    - samples/normal_breathing.wav (clear breathing)
    - samples/mild_wheeze.wav (subtle wheeze patterns)
    - samples/severe_wheeze.wav (pronounced wheeze)
    - samples/coughing.wav (cough sequences)

Theory:
    - Breathing frequency: 0.3-0.8 Hz (18-48 breaths/min)
    - Wheeze frequency: 100-1000 Hz (musical continuous tone)
    - Cough frequency: Broadband noise (50-5000 Hz)

Author: Health Hackathon Team
License: MIT
"""

import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wavfile
from pathlib import Path
from typing import Tuple


# Configuration
SAMPLE_RATE = 22050  # Hz (standard for mobile audio)
DURATION = 10  # seconds (matches app recording duration)
SAMPLES = SAMPLE_RATE * DURATION


class RespiratoryAudioGenerator:
    """Generate synthetic respiratory audio samples."""

    def __init__(self, sample_rate: int = 22050, duration: float = 10.0):
        """
        Initialize audio generator.

        Args:
            sample_rate: Sample rate in Hz
            duration: Duration in seconds
        """
        self.sample_rate = sample_rate
        self.duration = duration
        self.t = np.linspace(0, duration, int(sample_rate * duration))
        self.output_dir = Path("samples")
        self.output_dir.mkdir(exist_ok=True)

    def _breathing_envelope(self, rate: float = 0.4) -> np.ndarray:
        """
        Create breathing envelope (inhalation/exhalation cycle).

        Args:
            rate: Breathing rate in Hz (0.3-0.8 Hz = 18-48 breaths/min)

        Returns:
            Envelope array for amplitude modulation
        """
        # Smooth sine wave for breathing motion
        envelope = np.sin(2 * np.pi * rate * self.t) ** 2
        envelope = (envelope + 0.5) / 1.5  # Scale to 0.33-1.0 range
        return envelope

    def _normalize_audio(self, audio: np.ndarray, target_db: float = -20) -> np.ndarray:
        """
        Normalize audio to target loudness.

        Args:
            audio: Audio signal
            target_db: Target loudness in dB (relative to 0 dB = max amplitude)

        Returns:
            Normalized audio
        """
        # Prevent clipping
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            # Scale to -20 dB (typical for breathing sounds)
            scale_factor = (10 ** (target_db / 20)) / max_val
            audio = audio * scale_factor

        # Soft clipping for any remaining peaks
        audio = np.tanh(audio)

        return audio

    def _save_audio(self, audio: np.ndarray, filename: str) -> str:
        """
        Save audio to .wav file.

        Args:
            audio: Audio signal (float32, range -1 to 1)
            filename: Output filename

        Returns:
            Path to saved file
        """
        # Convert to int16 for standard WAV format
        audio_int16 = np.int16(audio * 32767)

        filepath = self.output_dir / filename
        wavfile.write(filepath, self.sample_rate, audio_int16)

        return str(filepath)

    # ========== SAMPLE GENERATORS ==========

    def generate_normal_breathing(self) -> str:
        """
        Generate normal, clear breathing without wheezing.

        Characteristics:
        - Breathing frequency: 0.4 Hz (24 breaths/min, typical child)
        - Minimal high-frequency content
        - Smooth amplitude modulation
        - Light air/friction noise

        Returns:
            Path to saved .wav file
        """
        print("Generating normal breathing...")

        # Breathing envelope (inhalation/exhalation)
        breathing_rate = 0.4  # Hz
        envelope = self._breathing_envelope(breathing_rate)

        # Soft rustling noise from air movement (0.5 kHz)
        # This represents the normal sound of air moving through airways
        noise = np.random.normal(0, 0.1, len(self.t))
        filtered = signal.butter(4, 800, btype='low', fs=self.sample_rate)[0]
        filtered = signal.butter(4, 800, btype='low', fs=self.sample_rate)[1]
        noise = signal.lfilter(filtered, [1], noise)

        # Main breathing signal: very low frequency base tone with noise
        base_tone = 0.05 * np.sin(2 * np.pi * 80 * self.t)  # Very subtle tone at 80 Hz

        # Combine: breathing envelope modulates the noise and base tone
        audio = envelope * (base_tone + noise)

        # Add subtle frequency variation (natural variation in breathing)
        frequency_variation = 0.02 * np.sin(2 * np.pi * 0.1 * self.t)
        audio *= (1 + frequency_variation)

        # Normalize
        audio = self._normalize_audio(audio, target_db=-20)

        # Save
        filepath = self._save_audio(audio, "normal_breathing.wav")
        print(f"  ✓ Saved: {filepath}")
        print(f"    Duration: {self.duration}s, Peak amplitude: {np.max(np.abs(audio)):.3f}")

        return filepath

    def generate_mild_wheeze(self) -> str:
        """
        Generate mild wheezing (moderate asthma symptoms).

        Characteristics:
        - Breathing frequency: 0.4 Hz
        - Wheeze frequencies: 250-450 Hz (mild wheeze band)
        - Wheeze probability: ~35-45%
        - Intermittent wheeze bursts (only during exhalation)

        Returns:
            Path to saved .wav file
        """
        print("Generating mild wheeze...")

        # Breathing envelope
        breathing_rate = 0.4
        envelope = self._breathing_envelope(breathing_rate)

        # Heavy breathing noise (dominates over wheeze)
        noise = np.random.normal(0, 0.14, len(self.t))
        base_tone = 0.05 * np.sin(2 * np.pi * 80 * self.t)

        # Create sparse wheeze (only 25% of the time, very quiet)
        wheeze = np.zeros_like(self.t)
        cycle_samples = int(self.sample_rate / breathing_rate)  # Samples per breathing cycle

        # Only every 2nd exhalation has wheeze, and only partially
        for cycle_num, cycle_start in enumerate(range(0, len(self.t), cycle_samples)):
            if cycle_num % 2 == 0:  # Alternate cycles
                wheeze_burst_start = int(cycle_start + cycle_samples * 0.6)
                wheeze_burst_end = int(cycle_start + cycle_samples * 0.85)

                if wheeze_burst_start < len(self.t):
                    burst_slice = slice(wheeze_burst_start, min(wheeze_burst_end, len(self.t)))
                    wheeze_signal = 0.03 * np.sin(2 * np.pi * 320 * self.t[burst_slice])
                    wheeze[burst_slice] = wheeze_signal

        # Combine all components with dominant noise
        audio = envelope * (base_tone + 0.8 * noise + wheeze)

        # Normalize
        audio = self._normalize_audio(audio, target_db=-20)

        # Save
        filepath = self._save_audio(audio, "mild_wheeze.wav")
        print(f"  ✓ Saved: {filepath}")
        print(f"    Duration: {self.duration}s, Peak amplitude: {np.max(np.abs(audio)):.3f}")
        print(f"    Wheeze frequency: 300 Hz, Intermittent during exhalation (~40% duty cycle)")

        return filepath

    def generate_severe_wheeze(self) -> str:
        """
        Generate severe wheezing (acute asthma exacerbation).

        Characteristics:
        - Breathing frequency: 0.6 Hz (elevated, 36 breaths/min - signs of distress)
        - Wheeze frequencies: 200-600 Hz (multiple harmonic components)
        - Wheeze probability: >70%
        - Continuous wheeze throughout recording
        - Higher amplitude

        Returns:
            Path to saved .wav file
        """
        print("Generating severe wheeze...")

        # Elevated breathing rate due to respiratory distress
        breathing_rate = 0.6  # 36 breaths/min
        envelope = self._breathing_envelope(breathing_rate)

        # More pronounced base breathing sound
        noise = np.random.normal(0, 0.12, len(self.t))
        base_tone = 0.08 * np.sin(2 * np.pi * 80 * self.t)

        # Severe wheeze: multiple frequency components (fundamental + harmonics)
        # Fundamental wheeze tone
        wheeze_fundamental = 250
        wheeze_1 = 0.25 * np.sin(2 * np.pi * wheeze_fundamental * self.t)

        # First harmonic (more prominent in severe wheeze)
        wheeze_2 = 0.15 * np.sin(2 * np.pi * (wheeze_fundamental * 2) * self.t)

        # Second harmonic
        wheeze_3 = 0.10 * np.sin(2 * np.pi * (wheeze_fundamental * 2.5) * self.t)

        # Frequency modulation for natural variation
        freq_mod = 0.05 * np.sin(2 * np.pi * 1.5 * self.t)

        # Wheeze is more continuous in severe cases
        wheeze_continuous = 0.8  # More wheeze presence

        # Combine all components
        wheeze = wheeze_continuous * (wheeze_1 + wheeze_2 + wheeze_3)
        audio = envelope * (base_tone + 0.5 * noise + wheeze) * (1 + freq_mod)

        # Normalize
        audio = self._normalize_audio(audio, target_db=-18)  # Slightly louder for severe

        # Save
        filepath = self._save_audio(audio, "severe_wheeze.wav")
        print(f"  ✓ Saved: {filepath}")
        print(f"    Duration: {self.duration}s, Peak amplitude: {np.max(np.abs(audio)):.3f}")
        print(f"    Wheeze frequencies: 250-625 Hz, Continuous pattern")

        return filepath

    def generate_coughing(self) -> str:
        """
        Generate coughing sounds.

        Characteristics:
        - Cough bursts: broadband noise (100-4000 Hz)
        - Duration: 0.5-1.0 second per cough
        - Multiple coughs: 3-5 coughs in sequence
        - Sharp attack and decay
        - Often follows or precedes breathing

        Returns:
            Path to saved .wav file
        """
        print("Generating coughing...")

        audio = np.zeros_like(self.t)

        # Parameters for coughs
        cough_count = 4
        coughs_per_interval = 2
        time_between_intervals = self.duration / (cough_count / coughs_per_interval + 1)

        # Generate coughs
        cough_index = 0
        for interval in range(cough_count + 1):
            if interval % 2 == 0:  # First and third intervals: cough
                cough_start = interval * time_between_intervals

                for i in range(coughs_per_interval):
                    cough_time = cough_start + (i * 0.6)  # Space coughs 0.6s apart

                    if cough_time >= self.duration:
                        break

                    cough_start_idx = int(cough_time * self.sample_rate)
                    cough_duration = 0.7  # seconds
                    cough_samples = int(cough_duration * self.sample_rate)
                    cough_end_idx = min(cough_start_idx + cough_samples, len(self.t))

                    # Cough is broadband noise
                    cough_noise = np.random.normal(0, 0.3, cough_end_idx - cough_start_idx)

                    # Envelope: sharp attack, slower decay
                    cough_len = len(cough_noise)
                    attack_len = int(0.05 * cough_len)  # 50ms attack
                    attack = np.linspace(0, 1, attack_len)
                    decay = np.exp(-3 * np.linspace(0, 1, cough_len - attack_len))

                    cough_envelope = np.concatenate([attack, decay])

                    # Apply envelope and filter
                    cough = cough_noise * cough_envelope

                    # Bandpass filter to realistic cough frequencies
                    sos = signal.butter(4, [100, 3000], btype='band', fs=self.sample_rate, output='sos')
                    cough = signal.sosfilt(sos, cough)

                    # Add to audio
                    audio[cough_start_idx:cough_end_idx] += cough[:cough_end_idx - cough_start_idx]

        # Add some breathing between coughs
        breathing_rate = 0.35
        envelope = 0.3 * self._breathing_envelope(breathing_rate)
        noise = 0.05 * np.random.normal(0, 0.1, len(self.t))
        audio += envelope * noise

        # Normalize
        audio = self._normalize_audio(audio, target_db=-18)

        # Save
        filepath = self._save_audio(audio, "coughing.wav")
        print(f"  ✓ Saved: {filepath}")
        print(f"    Duration: {self.duration}s, Peak amplitude: {np.max(np.abs(audio)):.3f}")
        print(f"    Pattern: {cough_count} coughs in sequence, broadband noise (100-3000 Hz)")

        return filepath

    def generate_all(self) -> dict:
        """
        Generate all sample types.

        Returns:
            Dictionary mapping sample names to file paths
        """
        print("\n" + "=" * 60)
        print("RESPIRATORY AUDIO SAMPLE GENERATOR")
        print("=" * 60)
        print(f"Sample Rate: {self.sample_rate} Hz")
        print(f"Duration: {self.duration} seconds")
        print(f"Output Directory: {self.output_dir.absolute()}")
        print("=" * 60 + "\n")

        samples = {
            'normal_breathing': self.generate_normal_breathing(),
            'mild_wheeze': self.generate_mild_wheeze(),
            'severe_wheeze': self.generate_severe_wheeze(),
            'coughing': self.generate_coughing(),
        }

        print("\n" + "=" * 60)
        print("GENERATION COMPLETE")
        print("=" * 60)
        print("\nGenerated files:")
        for name, filepath in samples.items():
            print(f"  • {name}: {filepath}")

        return samples


def main():
    """Main entry point."""
    generator = RespiratoryAudioGenerator(
        sample_rate=SAMPLE_RATE,
        duration=DURATION
    )

    samples = generator.generate_all()

    print("\n" + "=" * 60)
    print("TESTING INSTRUCTIONS")
    print("=" * 60)
    print("""
To test with the wheeze detection algorithm:

1. Run the audio analyzer on each sample:

   from audio_analyzer import RespiratoryAnalyzer
   analyzer = RespiratoryAnalyzer()

   for sample in ['normal_breathing.wav', 'mild_wheeze.wav',
                  'severe_wheeze.wav', 'coughing.wav']:
       result = analyzer.analyze(f'samples/{sample}')
       print(f'{sample}: {result}')

2. Expected results:

   normal_breathing.wav:
     - wheeze_probability: < 0.15 (very low)
     - risk_level: 'low'

   mild_wheeze.wav:
     - wheeze_probability: 0.40-0.55
     - risk_level: 'medium'

   severe_wheeze.wav:
     - wheeze_probability: > 0.70
     - risk_level: 'high'

   coughing.wav:
     - wheeze_probability: < 0.20 (cough != wheeze)
     - risk_level: 'low'

3. Verify algorithm accuracy:
   - Normal should score LOW
   - Mild should score MEDIUM
   - Severe should score HIGH
   - Cough should score LOW (coughs are not wheezes)

4. Fine-tune thresholds if needed in audio_analyzer.py
""")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
