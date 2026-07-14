"""FSOT scientific audio analysis — GPU-capable spectral pipeline for hardware research."""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def _torch_cuda_usable() -> bool:
    try:
        import torch  # noqa: WPS433

        if not torch.cuda.is_available():
            return False
        x = torch.zeros(1, device="cuda")
        _ = x + 1
        return True
    except Exception:
        return False


def synthesize_calibration_tone(
    *,
    sample_rate: int = 48000,
    duration_s: float = 1.0,
    frequency_hz: float = 440.0,
) -> np.ndarray:
    """Credential-free calibration tone for FSOT audio hardware verification."""
    n = int(sample_rate * duration_s)
    t = np.linspace(0.0, duration_s, n, endpoint=False, dtype=np.float32)
    return (0.25 * np.sin(2.0 * math.pi * frequency_hz * t)).astype(np.float32)


def analyze_waveform(wave: np.ndarray, *, sample_rate: int = 48000) -> dict[str, Any]:
    """Compute RMS, peak, spectral centroid — torch CUDA when available."""
    wave = np.asarray(wave, dtype=np.float32).reshape(-1)
    rms = float(np.sqrt(np.mean(wave**2))) if wave.size else 0.0
    peak = float(np.max(np.abs(wave))) if wave.size else 0.0

    try:
        import librosa  # noqa: WPS433

        centroid = float(librosa.feature.spectral_centroid(y=wave, sr=sample_rate).mean())
        bandwidth = float(librosa.feature.spectral_bandwidth(y=wave, sr=sample_rate).mean())
    except Exception:
        spectrum = np.abs(np.fft.rfft(wave))
        freqs = np.fft.rfftfreq(wave.size, d=1.0 / sample_rate)
        centroid = float((spectrum * freqs).sum() / (spectrum.sum() + 1e-12))
        bandwidth = float(np.sqrt(((freqs - centroid) ** 2 * spectrum).sum() / (spectrum.sum() + 1e-12)))

    backend = "numpy_cpu"
    if _torch_cuda_usable():
        import torch  # noqa: WPS433

        gpu = torch.from_numpy(wave).cuda()
        rms = float(torch.sqrt((gpu**2).mean()).item())
        peak = float(gpu.abs().max().item())
        backend = "torch_cuda"

    return {
        "sample_rate_hz": sample_rate,
        "sample_count": int(wave.size),
        "rms_amplitude": round(rms, 8),
        "peak_amplitude": round(peak, 8),
        "spectral_centroid_hz": round(centroid, 4),
        "spectral_bandwidth_hz": round(bandwidth, 4),
        "backend": backend,
    }


def analyze_file(path: str, *, sample_rate: int = 48000) -> dict[str, Any]:
    """Load WAV/FLAC/OGG via soundfile and analyze."""
    import soundfile as sf  # noqa: WPS433

    wave, sr = sf.read(path, dtype="float32", always_2d=False)
    if wave.ndim > 1:
        wave = wave.mean(axis=1)
    if sr != sample_rate and wave.size:
        try:
            import librosa  # noqa: WPS433

            wave = librosa.resample(wave, orig_sr=sr, target_sr=sample_rate)
            sr = sample_rate
        except Exception:
            pass
    stats = analyze_waveform(wave, sample_rate=sr)
    stats["source_file"] = path
    return stats


def mel_spectrogram_summary(wave: np.ndarray, *, sample_rate: int = 48000) -> dict[str, Any]:
    """Mel-band energy summary for FSOT audio panels."""
    wave = np.asarray(wave, dtype=np.float32).reshape(-1)
    try:
        import librosa  # noqa: WPS433

        mel = librosa.feature.melspectrogram(y=wave, sr=sample_rate, n_mels=64)
        mel_db = librosa.power_to_db(mel, ref=np.max)
        return {
            "mel_bands": int(mel_db.shape[0]),
            "mel_mean_db": round(float(mel_db.mean()), 4),
            "mel_std_db": round(float(mel_db.std()), 4),
            "backend": "librosa_cpu",
        }
    except Exception:
        return {"mel_bands": 0, "mel_mean_db": 0.0, "mel_std_db": 0.0, "backend": "fallback"}