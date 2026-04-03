from pathlib import Path

from src.case_map import get_case_info, get_case_path
from src.io_h5 import load_case
from src.plotting import plot_multiple_spectra
from src.spectra import compute_array_average_psd, compute_psd, psd_to_spl


def dominant_band(freqs, spl, f_min=200.0):
	mask = freqs >= f_min
	if not mask.any():
		max_idx = spl.argmax()
		return float(freqs[max_idx]), float(spl[max_idx])
	idx_local = spl[mask].argmax()
	idx_global = (mask.nonzero()[0])[idx_local]
	return float(freqs[idx_global]), float(spl[idx_global])


def main():
	out_dir = Path("outputs") / "task3_cases461078"
	out_dir.mkdir(parents=True, exist_ok=True)

	case_ids = [4, 6, 7, 8, 10]
	spectra = {}

	for case_id in case_ids:
		info = get_case_info(case_id)
		signals, fs, _meta = load_case(get_case_path(case_id))
		freqs, psd = compute_psd(signals, fs, nperseg=4096, overlap=0.5)
		df = freqs[1] - freqs[0]
		avg_spl = psd_to_spl(compute_array_average_psd(psd), df)

		f_dom, l_dom = dominant_band(freqs, avg_spl)
		label = f"Case {case_id} ({info['type']}, AoA {info['aoa_deg']:.0f} deg)"
		spectra[label] = avg_spl

		print(
			f"Case {case_id}: type={info['type']}, U={info['U_mps_nominal']:.1f} m/s, "
			f"AoA={info['aoa_deg']:.1f} deg, strongest bin at {f_dom:.1f} Hz ({l_dom:.1f} dB)"
		)

	plot_multiple_spectra(
		freqs,
		spectra,
		title="Task 3 - Cases 4,6,7,8,10 average SPL comparison",
		save_path=out_dir / "cases461078_avg_spl_comparison.png",
	)

	print(f"Task 3 outputs saved to: {out_dir}")


if __name__ == "__main__":
	main()
