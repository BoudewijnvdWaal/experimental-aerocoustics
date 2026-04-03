"""Spectral utilities for aeroacoustic analysis."""

import numpy as np


P_REF = 20e-6


def _as_2d_signals(signals):
	data = np.asarray(signals, dtype=np.float64)
	if data.ndim == 1:
		return data[np.newaxis, :]
	if data.ndim != 2:
		raise ValueError("signals must be 1D or 2D")
	return data


def compute_psd(signals, fs, nperseg=4096, overlap=0.5):
	"""Compute single-sided PSD using a manual Welch implementation.

	Returns
	-------
	freqs : ndarray, shape (n_freq,)
	psd : ndarray, shape (n_channels, n_freq)
	"""
	x = _as_2d_signals(signals)
	n_channels, n_samples = x.shape

	if nperseg > n_samples:
		nperseg = n_samples
	if nperseg < 8:
		raise ValueError("nperseg is too small")

	step = int(nperseg * (1.0 - overlap))
	if step <= 0:
		raise ValueError("overlap too high; resulting step <= 0")

	starts = np.arange(0, n_samples - nperseg + 1, step, dtype=int)
	if starts.size == 0:
		starts = np.array([0], dtype=int)

	window = np.hanning(nperseg)
	window_norm = np.sum(window ** 2)
	scale = fs * window_norm

	n_freq = nperseg // 2 + 1
	psd_acc = np.zeros((n_channels, n_freq), dtype=np.float64)

	for s in starts:
		seg = x[:, s : s + nperseg]
		seg = seg - np.mean(seg, axis=1, keepdims=True)
		seg_win = seg * window[np.newaxis, :]
		spec = np.fft.rfft(seg_win, axis=1)
		p = (np.abs(spec) ** 2) / scale

		# Single-sided correction except DC and Nyquist (if present).
		if nperseg % 2 == 0:
			p[:, 1:-1] *= 2.0
		else:
			p[:, 1:] *= 2.0
		psd_acc += p

	psd = psd_acc / starts.size
	freqs = np.fft.rfftfreq(nperseg, d=1.0 / fs)
	return freqs, psd


def psd_to_spl(psd, df, pref=P_REF):
	"""Convert PSD to per-bin SPL levels in dB re 20 uPa."""
	p2_bin = np.asarray(psd) * df
	p2_bin = np.maximum(p2_bin, 1e-30)
	return 10.0 * np.log10(p2_bin / (pref ** 2))


def compute_channel_spl(signals, fs, channel_index, nperseg=4096, overlap=0.5):
	"""Compute one-channel narrowband SPL spectrum."""
	data = _as_2d_signals(signals)
	if not (0 <= channel_index < data.shape[0]):
		raise IndexError(f"channel_index {channel_index} out of range")
	freqs, psd = compute_psd(data[channel_index], fs, nperseg=nperseg, overlap=overlap)
	df = freqs[1] - freqs[0]
	spl = psd_to_spl(psd[0], df)
	return freqs, spl


def compute_array_average_psd(psd):
	"""Average PSD across channels."""
	data = np.asarray(psd)
	if data.ndim != 2:
		raise ValueError("psd must be 2D with shape (n_channels, n_freq)")
	return np.mean(data, axis=0)