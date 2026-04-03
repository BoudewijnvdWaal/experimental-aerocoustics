"""Case-to-file mapping and metadata for the assignment matrix."""

from pathlib import Path


CASE_TABLE = {
	1: {
		"file": "Archive_1_4/NACA0018_U25_AA0_REF.h5",
		"U_mps_nominal": 25.0,
		"aoa_deg": 0.0,
		"type": "Broadband",
	},
	2: {
		"file": "Archive_2_4/NACA0018_U25_AA4_REF.h5",
		"U_mps_nominal": 25.0,
		"aoa_deg": 4.0,
		"type": "Broadband",
	},
	3: {
		"file": "Archive_2_4/NACA0018_U25_AA8_REF.h5",
		"U_mps_nominal": 25.0,
		"aoa_deg": 8.0,
		"type": "Tone",
	},
	4: {
		"file": "Archive_3_4/NACA0018_U25_AA10_REF.h5",
		"U_mps_nominal": 25.0,
		"aoa_deg": 10.0,
		"type": "Tone",
	},
	5: {
		"file": "Archive_3_4/NACA0018_U25_AA12_REF.h5",
		"U_mps_nominal": 25.0,
		"aoa_deg": 12.0,
		"type": "Tone",
	},
	6: {
		"file": "Archive_4_4/NACA0018_U25_AA18_REF.h5",
		"U_mps_nominal": 25.0,
		"aoa_deg": 18.0,
		"type": "Broadband",
	},
	7: {
		"file": "Archive_4_4/NACA0018_U25_AA24_REF.h5",
		"U_mps_nominal": 25.0,
		"aoa_deg": 24.0,
		"type": "Separation",
	},
	8: {
		"file": "Archive_4_4/NACA0018_U25_AA14_poststall_REF.h5",
		"U_mps_nominal": 25.0,
		"aoa_deg": 14.0,
		"type": "Separation",
	},
	9: {
		"file": "Archive_3_4/NACA0018_U25_AA12_poststall_REF.h5",
		"U_mps_nominal": 25.0,
		"aoa_deg": 12.0,
		"type": "Tone",
	},
	10: {
		"file": "Archive_2_4/NACA0018_U25_AA10_poststall_REF.h5",
		"U_mps_nominal": 25.0,
		"aoa_deg": 10.0,
		"type": "Tone",
	},
	11: {
		"file": "Archive_1_4/NACA0018_U20_AA0_REF.h5",
		"U_mps_nominal": 20.0,
		"aoa_deg": 0.0,
		"type": "Broadband",
	},
	12: {
		"file": "Archive_1_4/NACA0018_U15_AA0_REF.h5",
		"U_mps_nominal": 15.0,
		"aoa_deg": 0.0,
		"type": "Broadband",
	},
}


def get_case_info(case_number):
	"""Return mapping information for one assignment case."""
	if case_number not in CASE_TABLE:
		raise KeyError(f"Unknown case number: {case_number}")
	return CASE_TABLE[case_number].copy()


def get_case_path(case_number, root_dir="."):
	"""Return absolute path for a case file."""
	case_info = get_case_info(case_number)
	return Path(root_dir) / case_info["file"]


def list_cases():
	"""Return sorted available case numbers."""
	return sorted(CASE_TABLE)