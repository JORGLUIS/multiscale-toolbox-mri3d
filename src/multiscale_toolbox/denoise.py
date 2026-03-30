from __future__ import annotations

import numpy as np
import pandas as pd
import pywt
from skimage.metrics import structural_similarity as ssim

from .task2_utils import rmse
from .wavepsi import haarpsi


def add_gaussian_noise(x: np.ndarray, sigma: float = 0.08, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    y = np.asarray(x, dtype=float) + rng.normal(0, sigma, np.asarray(x).shape)
    return np.clip(y, 0, 1)


def add_uniform_noise(
    x: np.ndarray,
    low: float = -0.14,
    high: float = 0.14,
    seed: int | None = None,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    y = np.asarray(x, dtype=float) + rng.uniform(low, high, np.asarray(x).shape)
    return np.clip(y, 0, 1)


def estimate_sigma_from_details(details) -> float:
    hh1 = details[-1][-1]
    return float(np.median(np.abs(hh1)) / 0.6745)


def denoise_dwt2(
    x: np.ndarray,
    wavelet: str = "haar",
    level: int = 3,
    threshold_mode: str = "soft",
) -> tuple[np.ndarray, float]:
    coeffs = pywt.wavedec2(x, wavelet=wavelet, level=level)
    cA = coeffs[0]
    details = coeffs[1:]

    sigma_est = estimate_sigma_from_details(details)
    uthresh = sigma_est * np.sqrt(2 * np.log(np.asarray(x).size))

    filtered_details = []
    for cH, cV, cD in details:
        filtered_details.append(
            tuple(pywt.threshold(c, value=uthresh, mode=threshold_mode) for c in (cH, cV, cD))
        )

    rec = pywt.waverec2([cA] + filtered_details, wavelet=wavelet)
    rec = rec[: x.shape[0], : x.shape[1]]
    return np.clip(rec, 0, 1), float(uthresh)


def evaluate_denoising_grid(
    astro_images: dict[str, np.ndarray],
    noisy_images: dict[tuple[str, str], np.ndarray],
    wavelets_2d: list[str],
    levels_2d: list[int],
    threshold_modes: list[str],
) -> pd.DataFrame:
    rows = []
    for image_name, clean in astro_images.items():
        for noise_name in ["gaussian", "uniform"]:
            noisy = noisy_images[(image_name, noise_name)]
            for w in wavelets_2d:
                for level in levels_2d:
                    for thr_mode in threshold_modes:
                        rec, thr = denoise_dwt2(noisy, wavelet=w, level=level, threshold_mode=thr_mode)
                        rows.append(
                            {
                                "imagen": image_name,
                                "ruido": noise_name,
                                "wavelet": w,
                                "nivel": level,
                                "threshold": thr_mode,
                                "umbral": thr,
                                "RMSE": rmse(clean, rec),
                                "SSIM": float(ssim(clean, rec, data_range=1.0)),
                                "HaarPSI": haarpsi(clean, rec, level=3),
                            }
                        )
    return pd.DataFrame(rows)
