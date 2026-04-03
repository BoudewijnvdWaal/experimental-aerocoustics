"""CLI entrypoint for the Experimental Aeroacoustics assignment."""

import argparse
import runpy
from pathlib import Path


SCRIPT_BY_MODE = {
	"case-check": "scripts/01_case1_check.py",
	"task1": "scripts/02_task1_cases123.py",
	"task2": "scripts/03_task2_cases59.py",
	"task3": "scripts/04_task3_cases461078.py",
	"task4": "scripts/05_task4_cases11112.py",
}


def main():
	parser = argparse.ArgumentParser(description="Run assignment analyses.")
	parser.add_argument(
		"--mode",
		choices=list(SCRIPT_BY_MODE) + ["all"],
		default="case-check",
		help="Which analysis to run",
	)
	args = parser.parse_args()

	if args.mode == "all":
		modes = ["case-check", "task1", "task2", "task3", "task4"]
	else:
		modes = [args.mode]

	for mode in modes:
		script = Path(SCRIPT_BY_MODE[mode])
		print(f"\n=== Running {mode}: {script} ===")
		runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
	main()
