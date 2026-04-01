# Experimental Aeroacoustics Analysis

Aeroacoustic analysis and data processing for NACA0018 airfoil experiments at various wind speeds and angles of attack.

## Project Structure

```
experimental-aerocoustics/
├── Archive_1_4/          # U15, U20, U25 (baseline conditions)
│   ├── NACA0018_U15_AA0_REF.h5
│   ├── NACA0018_U20_AA0_REF.h5
│   └── NACA0018_U25_AA0_REF.h5
├── Archive_2_4/          # U25 at AA4, AA8, AA10 (poststall)
│   ├── NACA0018_U25_AA4_REF.h5
│   ├── NACA0018_U25_AA8_REF.h5
│   └── NACA0018_U25_AA10_poststall_REF.h5
├── Archive_3_4/          # U25 at AA10, AA12 (poststall)
│   ├── NACA0018_U25_AA10_REF.h5
│   ├── NACA0018_U25_AA12_REF.h5
│   └── NACA0018_U25_AA12_poststall_REF.h5
├── Archive_4_4/          # U25 at AA14, AA18, AA24 (high angle of attack)
│   ├── NACA0018_U25_AA14_poststall_REF.h5
│   ├── NACA0018_U25_AA18_REF.h5
│   └── NACA0018_U25_AA24_REF.h5
├── Mic_poses_rel_13032020.xlsx  # Microphone position reference data
├── main.py                       # Main analysis entry point
└── README.md                     # This file
```

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Git (with Git LFS support)
- ~3 GB free disk space (for .h5 data files)

### Install Git LFS

**Windows (PowerShell):**
```powershell
choco install git-lfs
# OR download from https://git-lfs.github.com/ and install manually
```

**macOS (Homebrew):**
```bash
brew install git-lfs
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install git-lfs
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/BoudewijnvdWaal/experimental-aerocoustics.git
cd experimental-aerocoustics
```

### 2. Install Git LFS and Download Data

```bash
git lfs install
git lfs pull
```

⏱️ **This will take 10–20 minutes** (downloads ~2.93 GB of .h5 files).

### 3. Verify Data Download

Check that .h5 files are downloaded (not pointer files):

**Windows (PowerShell):**
```powershell
(Get-Item Archive_1_4/NACA0018_U15_AA0_REF.h5).Length
# Should show ~262 MB, not a few bytes
```

**macOS/Linux:**
```bash
ls -lh Archive_1_4/NACA0018_U15_AA0_REF.h5
# Should show ~262 MB
```

### 4. Set Up Python Environment (Optional but Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies (once you create requirements.txt)
pip install -r requirements.txt
```

## Working with .h5 Files

The .h5 files contain experimental data and are **read-only** in this repository. Do not modify them directly.

### Reading .h5 Files in Python

```python
import h5py

# Open an .h5 file
with h5py.File('Archive_1_4/NACA0018_U15_AA0_REF.h5', 'r') as f:
    # List all datasets and groups
    def print_structure(name, obj):
        print(name)
    
    f.visititems(print_structure)
    
    # Access specific data
    # Example (adjust keys based on actual file structure):
    # data = f['dataset_name'][:]
```

## Collaboration Workflow

### For Team Members

Each team member should follow the Quick Start section above.

**Important:** If you pull the latest code and .h5 files show as placeholder files (pointer files), run:
```bash
git lfs pull
```

### Adding Analysis Code

1. Create analysis scripts in the root directory or in an `analysis/` subdirectory.
2. Commit and push your code:
   ```bash
   git add your_analysis_script.py
   git commit -m "Add analysis for [description]"
   git push origin main
   ```
3. **Do not commit changes to .h5 files.** They are tracked by Git LFS and should not be modified.

### Using Branches (Optional)

For larger analyses, consider creating a feature branch:

```bash
git checkout -b feature/my-analysis
# Work on your analysis
git push origin feature/my-analysis
# When ready, create a Pull Request on GitHub
```

## File Structure Best Practices

- **Analysis scripts:** `*.py` files in root or `analysis/` folder
- **Notebooks:** `*.ipynb` files in `notebooks/` folder (if using Jupyter)
- **Outputs:** Create `outputs/` directory for results (add to `.gitignore` if large)
- **Data:** Leave `.h5` files as-is; do not modify

## Troubleshooting

### .h5 Files Show as Pointer Files After Pull

Run:
```bash
git lfs pull
```

### Permission Denied When Trying to Push

Make sure you have **Write** access to the repository. Contact the repository owner.

### LFS Quota Issues

If you see "LFS quota exceeded" during clone, the repository owner may need to enable LFS overage billing. Contact them.

## Data Attribution

**File naming convention:**
- `NACA0018`: Airfoil profile
- `U##`: Wind speed (m/s) – e.g., U15 = 15 m/s, U25 = 25 m/s
- `AA##`: Angle of attack (degrees)
- `poststall`: Indicates measurement in poststall regime
- `REF`: Reference measurement

## References

- **Airfoil:** NACA0018 symmetric airfoil
- **Mic Positions:** `Mic_poses_rel_13032020.xlsx` contains reference coordinates

## Contact

For questions about data access or repository setup, contact the repository owner.

---

**Last updated:** April 2026
