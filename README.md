# Experimental Aeroacoustics Assignment

Python workflow for the TU Delft experimental aeroacoustics assignment on NACA0018 trailing-edge noise.

## Current Status

- Implemented: first-case check and Tasks 1 to 4.
- Not implemented yet: bonus beamforming task (Task e in assignment).

## Project Structure

```text
experimental-aerocoustics/
    Archive_1_4/ ... Archive_4_4/   # HDF5 measurement data (Git LFS)
    outputs/                        # Generated plots/results per task
    scripts/
        01_case1_check.py             # First validation run (case 1)
        02_task1_cases123.py          # Task 1: cases 1,2,3
        03_task2_cases59.py           # Task 2: cases 5,9
        04_task3_cases461078.py       # Task 3: cases 4,6,7,8,10
        05_task4_cases11112.py        # Task 4: cases 1,11,12
    src/
        case_map.py                   # Assignment case mapping
        io_h5.py                      # HDF5 loading utilities
        spectra.py                    # PSD/SPL computations
        metrics.py                    # Tone, OASPL, scaling metrics
        plotting.py                   # Figure helpers
    inspect_file.py                 # HDF5 structure inspector
    main.py                         # CLI entrypoint
    README.md
```

## Requirements

- Python 3.10+
- Git + Git LFS
- About 3 GB free disk space for data

## Git LFS Setup (Keep This)

After cloning, always pull LFS files before analysis.

```bash
git lfs install
git lfs pull
```

If `.h5` files are only a few KB, they are pointer files and were not pulled correctly. Run `git lfs pull` again.

Quick file size check (Windows PowerShell):

```powershell
(Get-Item Archive_1_4/NACA0018_U15_AA0_REF.h5).Length
```

It should be hundreds of MB, not a tiny text-like file.

## Environment Setup

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install numpy matplotlib h5py pandas
```

## How To Run

Run from repository root.

First test case:

```bash
python main.py --mode case-check
```

Individual tasks:

```bash
python main.py --mode task1
python main.py --mode task2
python main.py --mode task3
python main.py --mode task4
```

Run all implemented tasks in sequence:

```bash
python main.py --mode all
```

## Outputs

- Figures are saved under `outputs/task0_case1_check`, `outputs/task1_cases123`, etc.
- Scripts also print key numerical values in terminal.

## Notes Per Task

- Task 1: compares array-averaged SPL with center microphone (channel 41).
- Task 2: detects fundamental tone for cases 5 and 9.
- Task 3: compares spectra for cases 4,6,7,8,10 and reports dominant peaks.
- Task 4: computes OASPL bands and fits velocity scaling exponent.

## Beamforming

Beamforming from the course is not yet implemented in this repository.
If needed, add a new module and script for assignment bonus Task e.

## Last Updated

April 2026
