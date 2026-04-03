from pathlib import Path

from src.case_map import get_case_info, get_case_path
from src.io_h5 import load_case
from src.plotting import plot_case_avg_vs_center, plot_multiple_spectra
from src.spectra import compute_array_average_psd, compute_channel_spl, compute_psd, psd_to_spl


def main():
	center_channel_index = 40  # Channel 41.
	out_dir = Path("outputs") / "task1_cases123"
	out_dir.mkdir(parents=True, exist_ok=True)

	case_ids = [1, 2, 3]
	avg_spl_for_compare = {}

	for case_id in case_ids:
		info = get_case_info(case_id)
		signals, fs, meta = load_case(get_case_path(case_id))

		freqs, psd = compute_psd(signals, fs, nperseg=4096, overlap=0.5)
		df = freqs[1] - freqs[0]
		avg_spl = psd_to_spl(compute_array_average_psd(psd), df)
		_, center_spl = compute_channel_spl(signals, fs, center_channel_index, nperseg=4096, overlap=0.5)

		avg_spl_for_compare[f"Case {case_id} (AoA {info['aoa_deg']:.0f} deg)"] = avg_spl

		plot_case_avg_vs_center(
			freqs,
			avg_spl,
			center_spl,
			title=f"Task 1 - Case {case_id}: array average vs center mic",
			save_path=out_dir / f"case_{case_id}_avg_vs_center.png",
		)

		print(
			f"Case {case_id}: U={info['U_mps_nominal']:.1f} m/s, "
			f"AoA={info['aoa_deg']:.1f} deg, type={info['type']}"
		)

	plot_multiple_spectra(
		freqs,
		avg_spl_for_compare,
		title="Task 1 - Cases 1/2/3 array-averaged SPL comparison",
		save_path=out_dir / "cases123_avg_spl_comparison.png",
	)

	print(f"Task 1 outputs saved to: {out_dir}")


if __name__ == "__main__":
	main()
