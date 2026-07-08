#!/usr/bin/env python3
"""Backward-compatible entrypoint for SMILES precision outlier patches."""

from patch_smiles_precision_outliers import main

if __name__ == "__main__":
    raise SystemExit(main())