from __future__ import annotations

from pathlib import Path

import numpy as np


def rmse(x: np.ndarray, y: np.ndarray, mask: np.ndarray | None = None) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if mask is not None:
        m = np.asarray(mask).astype(bool)
        return float(np.sqrt(np.mean((x[m] - y[m]) ** 2)))
    return float(np.sqrt(np.mean((x - y) ** 2)))


def normalize_to_unit(
    x: np.ndarray,
    mask: np.ndarray | None = None,
    p_low: float = 1,
    p_high: float = 99,
) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    values = x[np.asarray(mask).astype(bool)] if mask is not None else x.ravel()
    lo = np.percentile(values, p_low)
    hi = np.percentile(values, p_high)
    if hi <= lo:
        hi = float(values.max())
        lo = float(values.min())
    return np.clip((x - lo) / (hi - lo + 1e-12), 0, 1)


def normalize_to_255(x: np.ndarray, mask: np.ndarray | None = None) -> np.ndarray:
    return 255.0 * normalize_to_unit(x, mask=mask)


def crop_to_mask(x: np.ndarray, mask: np.ndarray) -> tuple[np.ndarray, np.ndarray, tuple[slice, ...]]:
    coords = np.argwhere(mask > 0)
    mins = coords.min(axis=0)
    maxs = coords.max(axis=0) + 1
    slices = tuple(slice(a, b) for a, b in zip(mins, maxs))
    return x[slices], mask[slices], slices


def pad_for_swtn(x: np.ndarray, level: int) -> tuple[np.ndarray, list[tuple[int, int]]]:
    mult = 2**level
    pads: list[tuple[int, int]] = []
    for n in x.shape:
        target = int(np.ceil(n / mult) * mult)
        pads.append((0, target - n))
    return np.pad(x, pads, mode="reflect"), pads


def central_slice(volume: np.ndarray, axis: int = 2) -> np.ndarray:
    idx = volume.shape[axis] // 2
    return np.take(volume, idx, axis=axis)


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
