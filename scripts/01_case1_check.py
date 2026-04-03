from pathlib import Path

from src.case_map import get_case_info, get_case_path
from src.io_h5 import load_case, print_case_summary
from src.plotting import plot_case_avg_vs_center, plot_time_signal
from src.spectra import compute_array_average_psd, compute_channel_spl, compute_psd, psd_to_spl


def main():
	case_number = 1
	center_channel_index = 40  # Channel 41 in 1-based numbering.

	case_info = get_case_info(case_number)
	case_path = get_case_path(case_number)

	print(f"Running first test with case {case_number}: {case_path}")
	signals, fs, meta = load_case(case_path)
	print_case_summary(meta, fs, signals)
	print(f"Assignment nominal U_inf = {case_info['U_mps_nominal']:.1f} m/s")

	freqs, psd = compute_psd(signals, fs, nperseg=4096, overlap=0.5)
	df = freqs[1] - freqs[0]

	avg_psd = compute_array_average_psd(psd)
	avg_spl = psd_to_spl(avg_psd, df)
	_, center_spl = compute_channel_spl(signals, fs, center_channel_index, nperseg=4096, overlap=0.5)

	out_dir = Path("outputs") / "task0_case1_check"
	plot_time_signal(
		signals[center_channel_index],
		fs,
		title="Case 1 - Center microphone time signal",
		save_path=out_dir / "case1_time_signal_center_mic.png",
	)
	plot_case_avg_vs_center(
		freqs,
		avg_spl,
		center_spl,
		title=(
			f"Case 1 ({case_info['type']}) - Array average vs center mic\n"
			f"U={case_info['U_mps_nominal']:.1f} m/s, AoA={case_info['aoa_deg']:.1f} deg"
		),
		save_path=out_dir / "case1_avg_vs_center_spl.png",
	)

	print(f"Saved figures to: {out_dir}")


if __name__ == "__main__":
	main()
