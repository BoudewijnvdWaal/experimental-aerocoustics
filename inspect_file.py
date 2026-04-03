import sys
from pathlib import Path
import h5py
import numpy as np


def format_value(value):
    """Make HDF5 values easier to print."""
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except Exception:
            return str(value)

    if isinstance(value, np.ndarray):
        if value.size == 1:
            return format_value(value.item())
        return f"array shape={value.shape}, dtype={value.dtype}"

    if np.isscalar(value):
        return value

    return str(value)


def print_attributes(obj, indent="    "):
    """Print attributes of a group or dataset."""
    if len(obj.attrs) == 0:
        return

    print(f"{indent}Attributes:")
    for key, value in obj.attrs.items():
        print(f"{indent}  - {key}: {format_value(value)}")


def inspect_item(name, obj):
    """Function used by h5py visititems."""
    indent_level = name.count("/")
    indent = "    " * indent_level
    short_name = name.split("/")[-1]

    if isinstance(obj, h5py.Group):
        print(f"{indent}[GROUP] {short_name}")
        print_attributes(obj, indent + "    ")

    elif isinstance(obj, h5py.Dataset):
        print(f"{indent}[DATASET] {short_name}")
        print(f"{indent}    Shape: {obj.shape}")
        print(f"{indent}    Dtype: {obj.dtype}")

        try:
            if obj.shape == ():
                value = obj[()]
                print(f"{indent}    Value: {format_value(value)}")
            elif obj.size <= 10:
                value = obj[()]
                print(f"{indent}    Value: {format_value(value)}")
        except Exception as e:
            print(f"{indent}    Could not read dataset value: {e}")

        print_attributes(obj, indent + "    ")


def print_summary(h5file):
    """Print likely useful metadata if it exists."""
    print("\n" + "=" * 60)
    print("QUICK SUMMARY")
    print("=" * 60)

    possible_paths = [
        "AcousticData/Acquisition/SampleRate",
        "AcousticData/Acquisition/NumberOfChannels",
        "AcousticData/Acquisition/NumberOfSamples",
        "AcousticData/Acquisition/DurationInSeconds",
        "AcousticData/Conditions/AngleOfAttack",
        "AcousticData/Conditions/FlowSpeed",
        "AcousticData/Conditions/Temperature",
        "AcousticData/Conditions/Mach",
        "AcousticData/Conditions/Reynolds",
        "AcousticData/Conditions/Density",
        "AcousticData/Conditions/Viscosity",
        "AcousticData/Conditions/SpeedOfSound",
    ]

    for path in possible_paths:
        if path in h5file:
            try:
                value = h5file[path][()]
                print(f"{path}: {format_value(value)}")
            except Exception as e:
                print(f"{path}: could not read ({e})")

    print("\nPotential signal datasets:")
    for name, obj in h5file.items():
        pass

    def find_large_datasets(name, obj):
        if isinstance(obj, h5py.Dataset):
            if len(obj.shape) >= 2:
                print(f"  - {name}: shape={obj.shape}, dtype={obj.dtype}")

    h5file.visititems(find_large_datasets)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("python scripts/inspect_file.py <path_to_h5_file>")
        sys.exit(1)

    filepath = Path(sys.argv[1])

    if not filepath.exists():
        print(f"File not found: {filepath}")
        sys.exit(1)

    print("=" * 60)
    print(f"INSPECTING FILE: {filepath}")
    print("=" * 60)

    with h5py.File(filepath, "r") as h5file:
        print("\nFULL HDF5 TREE")
        print("-" * 60)
        h5file.visititems(inspect_item)

        print_summary(h5file)


if __name__ == "__main__":
    main()