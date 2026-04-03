"""Metrics used in assignment tasks."""

import numpy as np


P_REF = 20e-6


def find_fundamental_tone(freqs, spl, f_min=100.0, f_max=10000.0):
	"""Return dominant peak frequency and level in a chosen band."""
	f = np.asarray(freqs)
	l = np.asarray(spl)
	if f.shape != l.shape:
		raise ValueError("freqs and spl must have identical shapes")

	mask = (f >= f_min) & (f <= f_max)
	if not np.any(mask):
		raise ValueError("No frequency bins in requested range")

	idx_local = np.argmax(l[mask])
	idx_global = np.where(mask)[0][idx_local]
	return float(f[idx_global]), float(l[idx_global])


def compute_oaspl(freqs, psd, f_low=400.0, f_high=6300.0, pref=P_REF):
	"""Compute OASPL over a frequency band from PSD.

	Parameters
	----------
	freqs : ndarray shape (n_freq,)
	psd : ndarray shape (n_freq,) or (n_channels, n_freq)
	"""
	f = np.asarray(freqs)
	s = np.asarray(psd)
	if f.ndim != 1:
		raise ValueError("freqs must be 1D")

	mask = (f >= f_low) & (f <= f_high)
	if not np.any(mask):
		raise ValueError("No frequency bins in requested OASPL band")

	if s.ndim == 1:
		p2 = np.trapezoid(s[mask], f[mask])
	elif s.ndim == 2:
		p2 = np.trapezoid(s[:, mask], f[mask], axis=1)
	else:
		raise ValueError("psd must be 1D or 2D")

	p2 = np.maximum(p2, 1e-30)
	oaspl = 10.0 * np.log10(p2 / (pref ** 2))
	return oaspl


def oaspl_to_pressure_rms(oaspl_db, pref=P_REF):
	"""Convert OASPL dB to RMS acoustic pressure."""
	return pref * (10.0 ** (np.asarray(oaspl_db) / 20.0))


def fit_velocity_scaling(velocities_mps, pressure_rms):
	"""Fit p_rms = A * U^m and return exponent m and fit quality."""
	u = np.asarray(velocities_mps, dtype=np.float64)
	p = np.asarray(pressure_rms, dtype=np.float64)

	if u.shape != p.shape:
		raise ValueError("velocities_mps and pressure_rms must have identical shapes")
	if np.any(u <= 0) or np.any(p <= 0):
		raise ValueError("velocities and pressure_rms must be strictly positive")

	x = np.log(u)
	y = np.log(p)
	m, b = np.polyfit(x, y, deg=1)
	y_hat = m * x + b

	ss_res = np.sum((y - y_hat) ** 2)
	ss_tot = np.sum((y - np.mean(y)) ** 2)
	r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0

	return {
		"m": float(m),
		"A": float(np.exp(b)),
		"r2": float(r2),
	}
