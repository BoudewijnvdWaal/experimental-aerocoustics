"""Plotting helpers for assignment deliverables."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def _finalize(fig, save_path=None, show=False):
	fig.tight_layout()
	if save_path:
		out = Path(save_path)
		out.parent.mkdir(parents=True, exist_ok=True)
		fig.savefig(out, dpi=150)
	if show:
		plt.show()
	plt.close(fig)


def plot_time_signal(signal, fs, title="Time Signal", seconds=0.2, save_path=None, show=False):
	n = min(len(signal), int(seconds * fs))
	t = np.arange(n) / fs
	fig, ax = plt.subplots(figsize=(8, 3))
	ax.plot(t, signal[:n], lw=0.8)
	ax.set_xlabel("Time [s]")
	ax.set_ylabel("Pressure [Pa]")
	ax.set_title(title)
	ax.grid(True, alpha=0.3)
	_finalize(fig, save_path=save_path, show=show)


def plot_case_avg_vs_center(freqs, spl_avg, spl_center, title, save_path=None, show=False):
	fig, ax = plt.subplots(figsize=(9, 4.5))
	ax.semilogx(freqs, spl_avg, label="Array average", lw=1.6)
	ax.semilogx(freqs, spl_center, label="Center mic (ch 41)", lw=1.2)
	ax.set_xlabel("Frequency [Hz]")
	ax.set_ylabel("SPL [dB re 20 uPa]")
	ax.set_title(title)
	ax.grid(True, which="both", alpha=0.3)
	ax.legend()
	_finalize(fig, save_path=save_path, show=show)


def plot_multiple_spectra(freqs, spectra_dict, title, save_path=None, show=False):
	fig, ax = plt.subplots(figsize=(9, 4.8))
	for label, y in spectra_dict.items():
		ax.semilogx(freqs, y, lw=1.3, label=label)
	ax.set_xlabel("Frequency [Hz]")
	ax.set_ylabel("SPL [dB re 20 uPa]")
	ax.set_title(title)
	ax.grid(True, which="both", alpha=0.3)
	ax.legend()
	_finalize(fig, save_path=save_path, show=show)


def plot_tone_case(freqs, spl, peak_freq, peak_level, title, save_path=None, show=False):
	fig, ax = plt.subplots(figsize=(9, 4.5))
	ax.semilogx(freqs, spl, lw=1.4)
	ax.scatter([peak_freq], [peak_level], color="red", zorder=3)
	ax.annotate(
		f"Tone: {peak_freq:.1f} Hz",
		xy=(peak_freq, peak_level),
		xytext=(1.15 * peak_freq, peak_level + 4),
		arrowprops={"arrowstyle": "->", "lw": 1.0},
	)
	ax.set_xlabel("Frequency [Hz]")
	ax.set_ylabel("SPL [dB re 20 uPa]")
	ax.set_title(title)
	ax.grid(True, which="both", alpha=0.3)
	_finalize(fig, save_path=save_path, show=show)
