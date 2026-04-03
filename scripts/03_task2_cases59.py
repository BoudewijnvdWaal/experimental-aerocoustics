from pathlib import Path

from src.case_map import get_case_info, get_case_path
from src.io_h5 import load_case
from src.metrics import find_fundamental_tone
from src.plotting import plot_multiple_spectra, plot_tone_case
from src.spectra import compute_array_average_psd, compute_psd, psd_to_spl


def semi_empirical_laminar_tone_frequency(u_mps, model_alpha=None):
	"""Return model tone frequency with f = alpha * U if alpha is provided.

	Replace this with the exact formula from assignment reference [1].
	"""
	if model_alpha is None:
		return None
	return model_alpha * u_mps


def main():
	out_dir = Path("outputs") / "task2_cases59"
	out_dir.mkdir(parents=True, exist_ok=True)

	case_ids = [5, 9]
	spectra = {}

	for case_id in case_ids:
		info = get_case_info(case_id)
		signals, fs, _meta = load_case(get_case_path(case_id))
		freqs, psd = compute_psd(signals, fs, nperseg=4096, overlap=0.5)
		df = freqs[1] - freqs[0]

		avg_spl = psd_to_spl(compute_array_average_psd(psd), df)
		tone_freq_hz, tone_level_db = find_fundamental_tone(freqs, avg_spl, f_min=200.0, f_max=10000.0)
		model_freq_hz = semi_empirical_laminar_tone_frequency(info["U_mps_nominal"], model_alpha=None)

		spectra[f"Case {case_id} ({info['file'].split('/')[-1]})"] = avg_spl

		plot_tone_case(
			freqs,
			avg_spl,
			peak_freq=tone_freq_hz,
			peak_level=tone_level_db,
			title=f"Task 2 - Case {case_id}: tone identification",
			save_path=out_dir / f"case_{case_id}_tone.png",
		)

		if model_freq_hz is None:
			print(
				f"Case {case_id}: U={info['U_mps_nominal']:.1f} m/s, AoA={info['aoa_deg']:.1f} deg, "
				f"measured tone = {tone_freq_hz:.1f} Hz "
				f"(level {tone_level_db:.1f} dB). Model value not set yet."
			)
		else:
			print(
				f"Case {case_id}: U={info['U_mps_nominal']:.1f} m/s, AoA={info['aoa_deg']:.1f} deg, "
				f"measured tone = {tone_freq_hz:.1f} Hz (level {tone_level_db:.1f} dB), "
				f"model tone = {model_freq_hz:.1f} Hz, delta = {tone_freq_hz - model_freq_hz:.1f} Hz"
			)

	plot_multiple_spectra(
		freqs,
		spectra,
		title="Task 2 - Cases 5 and 9 average SPL",
		save_path=out_dir / "cases59_avg_spl_comparison.png",
	)

	print("Model note: insert the exact semi-empirical equation from reference [1] in semi_empirical_laminar_tone_frequency().")
	print(f"Task 2 outputs saved to: {out_dir}")


if __name__ == "__main__":
	main()
