#!/usr/bin/env python3
"""Verify FSOT scientific audio stack (analysis + optional GPU)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_audio_lib import analyze_waveform, mel_spectrogram_summary, synthesize_calibration_tone  # noqa: E402


def main() -> int:
    deps: dict[str, str] = {}
    for mod in ("torch", "torchaudio", "soundfile", "librosa", "scipy"):
        try:
            m = __import__(mod)
            deps[mod] = getattr(m, "__version__", "ok")
        except ImportError:
            deps[mod] = "missing"

    tone = synthesize_calibration_tone(frequency_hz=440.0)
    stats = analyze_waveform(tone)
    mel = mel_spectrogram_summary(tone)

    try:
        import torchaudio  # noqa: WPS433

        ta_ok = True
    except Exception as exc:
        ta_ok = False
        deps["torchaudio_load"] = str(exc)[:80]

    report = {
        "dependencies": deps,
        "torchaudio_import_ok": ta_ok,
        "calibration_440hz": stats,
        "mel_summary": mel,
    }
    print(json.dumps(report, indent=2))

    if deps.get("soundfile") == "missing":
        print("\nInstall: pip install soundfile librosa scipy torchaudio --index-url https://download.pytorch.org/whl/cu128")
        return 1
    if stats.get("backend") not in {"torch_cuda", "numpy_cpu"}:
        return 2
    if abs(stats.get("spectral_centroid_hz", 0) - 440.0) > 50.0:
        print("\nSpectral centroid drift too high for 440 Hz tone")
        return 3
    print("\nFSOT audio verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())