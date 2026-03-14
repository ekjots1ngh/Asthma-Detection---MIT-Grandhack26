#!/usr/bin/env python3
"""
Batch Respiratory Rate Analysis
================================

Analyzes multiple audio files and generates a comprehensive
comparison report of respiratory rates and breathing patterns.

Usage:
    python batch_respiratory_analysis.py samples/*.wav

    or with directory scanning:

    python batch_respiratory_analysis.py --dir samples
    python batch_respiratory_analysis.py --dir samples --save report.csv
"""

import os
import csv
from pathlib import Path
from typing import List, Dict
import matplotlib.pyplot as plt
import numpy as np
from respiratory_rate_analyzer import RespiratoryRateEstimator
import argparse


class BatchRespiratoryAnalyzer:
    """Analyzes multiple respiratory audio files."""

    def __init__(self, sample_rate: int = 22050):
        """Initialize batch analyzer."""
        self.estimator = RespiratoryRateEstimator(sr=sample_rate)

    def analyze_files(self, audio_files: List[str]) -> List[Dict]:
        """
        Analyze multiple audio files.

        Args:
            audio_files: List of audio file paths

        Returns:
            List of analysis results
        """
        results = []

        for audio_file in audio_files:
            if not Path(audio_file).exists():
                print(f"⚠️  Skipping: {audio_file} (file not found)")
                continue

            try:
                result = self.estimator.estimate_rate(audio_file)
                result['filename'] = Path(audio_file).name
                result['filepath'] = audio_file
                results.append(result)
                print(f"✓ {Path(audio_file).name}: {result['respiratory_rate']:.1f} breaths/min")
            except Exception as e:
                print(f"❌ Error analyzing {audio_file}: {str(e)}")

        return results

    def generate_report(
        self,
        results: List[Dict],
        save_path: str = None
    ) -> str:
        """
        Generate text report of analysis results.

        Args:
            results: List of analysis results
            save_path: Optional CSV file to save results

        Returns:
            Formatted report string
        """
        if not results:
            return "No results to report."

        # Sort by respiratory rate
        results_sorted = sorted(results, key=lambda x: x['respiratory_rate'])

        # Generate report
        report = "\n" + "=" * 80 + "\n"
        report += "BATCH RESPIRATORY RATE ANALYSIS REPORT\n"
        report += "=" * 80 + "\n\n"

        report += f"Total Files Analyzed: {len(results)}\n\n"

        # Statistics
        rates = [r['respiratory_rate'] for r in results if r['respiratory_rate'] > 0]
        if rates:
            report += "RESPIRATORY RATE STATISTICS:\n"
            report += "-" * 80 + "\n"
            report += f"  Mean:              {np.mean(rates):.1f} breaths/min\n"
            report += f"  Median:            {np.median(rates):.1f} breaths/min\n"
            report += f"  Std Dev:           {np.std(rates):.1f} breaths/min\n"
            report += f"  Range:             {np.min(rates):.1f} - {np.max(rates):.1f} breaths/min\n\n"

        # Detailed results table
        report += "DETAILED RESULTS:\n"
        report += "-" * 80 + "\n"
        report += f"{'File':<30} {'RR (breaths/min)':<18} {'Cycles':<10} {'Confidence':<12}\n"
        report += "-" * 80 + "\n"

        for result in results_sorted:
            filename = Path(result['filename']).name[:28]
            rr = result['respiratory_rate']
            cycles = result['num_cycles']
            confidence = result['confidence'] * 100

            report += f"{filename:<30} {rr:>6.1f}".ljust(48)
            report += f"{cycles:>6}".ljust(16)
            report += f"{confidence:>5.1f}%\n"

        report += "\n" + "=" * 80 + "\n"

        # Save to CSV if requested
        if save_path:
            self._save_csv(results, save_path)
            report += f"\nResults saved to: {save_path}\n"

        return report

    @staticmethod
    def _save_csv(results: List[Dict], filepath: str) -> None:
        """Save results to CSV file."""
        if not results:
            return

        fieldnames = [
            'filename',
            'respiratory_rate',
            'num_cycles',
            'mean_cycle_time',
            'std_cycle_time',
            'confidence',
            'duration'
        ]

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for result in results:
                row = {key: result.get(key, '') for key in fieldnames}
                writer.writerow(row)

    def plot_comparison(self, results: List[Dict], save_path: str = None) -> None:
        """
        Plot respiratory rate comparison across files.

        Args:
            results: List of analysis results
            save_path: Optional path to save figure
        """
        if not results:
            print("No results to plot.")
            return

        # Extract data
        filenames = [Path(r['filename']).stem for r in results]
        rates = [r['respiratory_rate'] for r in results]
        confidences = [r['confidence'] * 100 for r in results]
        cycles = [r['num_cycles'] for r in results]

        # Create figure with 3 subplots
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        fig.suptitle('Batch Respiratory Rate Analysis Comparison', fontsize=14, fontweight='bold')

        # --- Plot 1: Respiratory Rate Bar Chart ---
        ax = axes[0]
        colors = ['green' if 18 <= r <= 30 else 'orange' if 12 <= r <= 40 else 'red' for r in rates]
        ax.bar(range(len(filenames)), rates, color=colors, alpha=0.7, edgecolor='black')

        # Add reference lines for normal ranges
        ax.axhline(y=20, color='green', linestyle='--', alpha=0.5, label='Typical adult (20 breaths/min)')
        ax.axhline(y=25, color='blue', linestyle='--', alpha=0.5, label='Typical child (25 breaths/min)')
        ax.axhline(y=35, color='orange', linestyle='--', alpha=0.5, label='Elevated (35 breaths/min)')

        ax.set_ylabel('Respiratory Rate (breaths/min)', fontweight='bold')
        ax.set_title('Respiratory Rate Comparison', fontweight='bold')
        ax.set_xticks(range(len(filenames)))
        ax.set_xticklabels(filenames, rotation=45, ha='right')
        ax.legend(fontsize=8, loc='upper right')
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim([0, max(rates) * 1.2 if rates else 1])

        # --- Plot 2: Confidence Scores ---
        ax = axes[1]
        ax.bar(range(len(filenames)), confidences, color='steelblue', alpha=0.7, edgecolor='black')
        ax.axhline(y=80, color='green', linestyle='--', alpha=0.5, label='High confidence (>80%)')
        ax.set_ylabel('Confidence (%)', fontweight='bold')
        ax.set_title('Detection Confidence', fontweight='bold')
        ax.set_xticks(range(len(filenames)))
        ax.set_xticklabels(filenames, rotation=45, ha='right')
        ax.legend(fontsize=8)
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim([0, 105])

        # --- Plot 3: Number of Detected Cycles ---
        ax = axes[2]
        ax.bar(range(len(filenames)), cycles, color='coral', alpha=0.7, edgecolor='black')
        ax.set_ylabel('Number of Cycles', fontweight='bold')
        ax.set_title('Breathing Cycles Detected', fontweight='bold')
        ax.set_xticks(range(len(filenames)))
        ax.set_xticklabels(filenames, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Comparison plot saved to: {save_path}")

        plt.show()


def main():
    """Command-line interface for batch analysis."""
    parser = argparse.ArgumentParser(
        description='Batch analyze respiratory rates from multiple audio files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_respiratory_analysis.py samples/*.wav
  python batch_respiratory_analysis.py --dir samples
  python batch_respiratory_analysis.py samples/*.wav --save results.csv
  python batch_respiratory_analysis.py samples/*.wav --plot comparison.png
        """
    )

    parser.add_argument(
        'audio_files',
        nargs='*',
        help='Audio files to analyze'
    )
    parser.add_argument(
        '--dir',
        type=str,
        help='Directory containing audio files'
    )
    parser.add_argument(
        '--save',
        type=str,
        help='Save results to CSV file'
    )
    parser.add_argument(
        '--plot',
        type=str,
        help='Save comparison plot to image file'
    )
    parser.add_argument(
        '--no-report',
        action='store_true',
        help='Skip printing text report'
    )

    args = parser.parse_args()

    # Get list of audio files
    audio_files = []

    if args.dir:
        # Scan directory for WAV files
        audio_files = sorted(
            Path(args.dir).glob('*.wav')
        )
        audio_files = [str(f) for f in audio_files]
    else:
        audio_files = args.audio_files

    if not audio_files:
        print("Error: No audio files specified.")
        print("Usage: python batch_respiratory_analysis.py [files...] or --dir [directory]")
        return 1

    # Create analyzer and analyze files
    analyzer = BatchRespiratoryAnalyzer()

    print(f"\nAnalyzing {len(audio_files)} file(s)...")
    print("-" * 80)

    results = analyzer.analyze_files(audio_files)

    print("-" * 80)

    # Generate report
    if not args.no_report:
        report = analyzer.generate_report(results, save_path=args.save)
        print(report)

    # Generate plot if requested
    if args.plot and results:
        print("\nGenerating comparison plot...")
        analyzer.plot_comparison(results, save_path=args.plot)

    return 0


if __name__ == "__main__":
    exit(main())
