from pathlib import Path

import numpy as np

from src.case_map import get_case_info, get_case_path
from src.io_h5 import load_case
from src.metrics import compute_oaspl, fit_velocity_scaling, oaspl_to_pressure_rms
from src.spectra import compute_array_average_psd, compute_psd


def main():
	out_dir = Path("outputs") / "task4_cases11112"
	out_dir.mkdir(parents=True, exist_ok=True)

	case_ids = [1, 11, 12]

	velocities = []
	oaspl_400_6300 = []
	oaspl_1000_6300 = []

	for case_id in case_ids:
		case_info = get_case_info(case_id)
		signals, fs, meta = load_case(get_case_path(case_id))
		freqs, psd = compute_psd(signals, fs, nperseg=4096, overlap=0.5)
		avg_psd = compute_array_average_psd(psd)

		L1 = float(compute_oaspl(freqs, avg_psd, f_low=400.0, f_high=6300.0))
		L2 = float(compute_oaspl(freqs, avg_psd, f_low=1000.0, f_high=6300.0))

		velocities.append(case_info["U_mps_nominal"])
		oaspl_400_6300.append(L1)
		oaspl_1000_6300.append(L2)

		print(
			f"Case {case_id}: U={meta['flow_speed_mps']:.2f} m/s, "
			f"U_nominal={case_info['U_mps_nominal']:.1f} m/s, "
			f"OASPL[400,6300]={L1:.2f} dB, OASPL[1000,6300]={L2:.2f} dB"
		)

	velocities = np.asarray(velocities)
	p_rms_1 = oaspl_to_pressure_rms(np.asarray(oaspl_400_6300))
	p_rms_2 = oaspl_to_pressure_rms(np.asarray(oaspl_1000_6300))

	fit_1 = fit_velocity_scaling(velocities, p_rms_1)
	fit_2 = fit_velocity_scaling(velocities, p_rms_2)

	print("\nVelocity scaling fit p_rms = A * U^m")
	print(f"Band [400,6300] Hz:  m = {fit_1['m']:.3f}, R^2 = {fit_1['r2']:.4f}")
	print(f"Band [1000,6300] Hz: m = {fit_2['m']:.3f}, R^2 = {fit_2['r2']:.4f}")
	print("Reference note: aeroacoustic dipole-like trends are often close to U^5 in acoustic power.")


if __name__ == "__main__":
	main()
