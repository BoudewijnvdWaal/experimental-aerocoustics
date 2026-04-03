### Here the h5 should be read and it should return signals, sample rate and metadata 

from pathlib import Path
import h5py
import numpy as np


def _read_dataset_value(h5file, path):
    """
    Read an HDF5 dataset and return a clean Python scalar if it only contains one value.
    Otherwise return the full numpy array.
    """
    value = h5file[path][()]
    if isinstance(value, np.ndarray) and value.size == 1:
        return value.item()
    return value


def _read_attribute(dataset, attr_name, default=None):
    """
    Safely read an HDF5 attribute.
    """
    if attr_name in dataset.attrs:
        value = dataset.attrs[attr_name]
        if isinstance(value, np.ndarray) and value.size == 1:
            value = value.item()
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        return value
    return default


def load_case(filepath):
    """
    Load one aeroacoustic measurement case from an HDF5 file.

    Parameters
    ----------
    filepath : str or Path
        Path to the .h5 measurement file.

    Returns
    -------
    signals : np.ndarray
        Microphone pressure data in Pa, shape (n_channels, n_samples).
    fs : float
        Sampling frequency in Hz.
    meta : dict
        Dictionary with useful metadata.
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with h5py.File(filepath, "r") as h5file:
        # Main pressure dataset
        signals = h5file["AcousticData/Measurement"][()].astype(np.float64)

        # Acquisition info
        fs = float(_read_dataset_value(h5file, "Acquisition/SampleRate"))
        n_channels = int(_read_dataset_value(h5file, "Acquisition/NumberOfChannels"))
        n_samples = int(_read_dataset_value(h5file, "Acquisition/NumberOfSamples"))
        duration_s = float(_read_dataset_value(h5file, "Acquisition/DurationInSeconds"))

        microphone_ids = h5file["Acquisition/MicrophoneID"][()]
        mic_cartesian_position = h5file["Acquisition/MicrophoneCartesianPosition"][()]
        mic_spherical_position = h5file["Acquisition/MicrophoneSphericalPosition"][()]

        # Conditions
        angle_of_attack_deg = float(_read_dataset_value(h5file, "Conditions/AngleOfAttack"))
        flow_speed_mps = float(_read_dataset_value(h5file, "Conditions/FlowSpeed"))
        mach = float(_read_dataset_value(h5file, "Conditions/Mach"))
        reynolds = float(_read_dataset_value(h5file, "Conditions/Reynolds"))
        temperature_degC = float(_read_dataset_value(h5file, "Conditions/Temperature"))
        density_kgpm3 = float(_read_dataset_value(h5file, "Conditions/Density"))
        speed_of_sound_mps = float(_read_dataset_value(h5file, "Conditions/SpeedOfSound"))
        viscosity = float(_read_dataset_value(h5file, "Conditions/Viscosity"))

        # Model/configuration info
        configuration_dataset = h5file["Model/Configuration"]
        comment_dataset = h5file["Model/Comment"]

        configuration = _read_attribute(configuration_dataset, "Configuration", "Unknown")
        comment = _read_attribute(comment_dataset, "Comment", "None")

        # Signal unit
        measurement_dataset = h5file["AcousticData/Measurement"]
        signal_unit = _read_attribute(measurement_dataset, "Unity", "Unknown")

    meta = {
        "filepath": str(filepath),
        "filename": filepath.name,
        "signal_unit": signal_unit,
        "n_channels": n_channels,
        "n_samples": n_samples,
        "duration_s": duration_s,
        "microphone_ids": microphone_ids,
        "mic_cartesian_position": mic_cartesian_position,
        "mic_spherical_position": mic_spherical_position,
        "angle_of_attack_deg": angle_of_attack_deg,
        "flow_speed_mps": flow_speed_mps,
        "mach": mach,
        "reynolds": reynolds,
        "temperature_degC": temperature_degC,
        "density_kgpm3": density_kgpm3,
        "speed_of_sound_mps": speed_of_sound_mps,
        "viscosity": viscosity,
        "configuration": configuration,
        "comment": comment,
    }

    return signals, fs, meta


def print_case_summary(meta, fs, signals):
    """
    Print a short summary of a loaded case.
    """
    print("\n--- CASE SUMMARY ---")
    print(f"Filename:           {meta['filename']}")
    print(f"Signal shape:       {signals.shape}")
    print(f"Signal unit:        {meta['signal_unit']}")
    print(f"Sampling rate:      {fs:.1f} Hz")
    print(f"Duration:           {meta['duration_s']:.2f} s")
    print(f"Channels:           {meta['n_channels']}")
    print(f"Samples:            {meta['n_samples']}")
    print(f"Flow speed:         {meta['flow_speed_mps']:.3f} m/s")
    print(f"Angle of attack:    {meta['angle_of_attack_deg']:.1f} deg")
    print(f"Mach number:        {meta['mach']:.5f}")
    print(f"Reynolds number:    {meta['reynolds']:.0f}")
    print(f"Temperature:        {meta['temperature_degC']:.1f} °C")
    print(f"Configuration:      {meta['configuration']}")
    print(f"Comment:            {meta['comment']}")
    print(f"Microphone IDs:     {meta['microphone_ids'][:10]} ...")


if __name__ == "__main__":
    filepath = "Archive_1_4/NACA0018_U15_AA0_REF.h5"
    signals, fs, meta = load_case(filepath)
    print_case_summary(meta, fs, signals)