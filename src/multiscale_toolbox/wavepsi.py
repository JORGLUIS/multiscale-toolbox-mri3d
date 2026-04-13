from __future__ import annotations

import numpy as np
import pandas as pd
import pywt
from skimage.metrics import structural_similarity as ssim

from .external_haarpsi import haarpsi_repo, repo_logit, repo_sigmoid
from .task2_utils import normalize_to_255, pad_for_swtn, rmse


def logistic(x: np.ndarray, alpha: float = 4.2) -> np.ndarray:
    return repo_sigmoid(x, alpha=alpha)


def logistic_inv(y: float | np.ndarray, alpha: float = 4.2) -> np.ndarray:
    return repo_logit(y, alpha=alpha)


def directional_keys(ndim: int) -> list[str]:
    keys = []
    for axis in range(ndim):
        chars = ["a"] * ndim
        chars[axis] = "d"
        keys.append("".join(chars))
    return keys


def wavepsi(
    x: np.ndarray,
    y: np.ndarray,
    wavelet: str = "haar",
    level: int = 3,
    mask: np.ndarray | None = None,
    c: float = 30.0,
    alpha: float = 4.2,
    return_maps: bool = False,
):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask_bool = np.asarray(mask).astype(bool) if mask is not None else None

    # For the exact 2D Haar case, use the open-source rgcda/haarpsi implementation
    # as the task's requested base and return its maps directly.
    if wavelet == "haar" and x.ndim == 2 and y.ndim == 2 and mask_bool is None and level == 3:
        score, similarity_maps, weight_maps = haarpsi_repo(
            normalize_to_255(x),
            normalize_to_255(y),
            preprocess_with_subsampling=True,
        )
        if return_maps:
            return score, {"horizontal": similarity_maps[:, :, 0], "vertical": similarity_maps[:, :, 1]}, {
                "horizontal": weight_maps[:, :, 0],
                "vertical": weight_maps[:, :, 1],
            }
        return score

    x255 = normalize_to_255(x, mask=mask_bool)
    y255 = normalize_to_255(y, mask=mask_bool)

    x_pad, pads = pad_for_swtn(x255, level)
    y_pad, _ = pad_for_swtn(y255, level)
    mask_pad = np.pad(mask_bool.astype(float), pads, mode="constant") > 0 if mask_bool is not None else None

    coeffs_x = pywt.swtn(x_pad, wavelet=wavelet, level=level, trim_approx=False)
    coeffs_y = pywt.swtn(y_pad, wavelet=wavelet, level=level, trim_approx=False)

    hs_maps: dict[str, np.ndarray] = {}
    weight_maps: dict[str, np.ndarray] = {}
    numerator = 0.0
    denominator = 0.0

    for key in directional_keys(x.ndim):
        sims = []
        for j in range(level):
            dx = np.abs(coeffs_x[j][key])
            dy = np.abs(coeffs_y[j][key])
            sims.append((2 * dx * dy + c) / (dx**2 + dy**2 + c))

        hs = logistic(np.mean(sims, axis=0), alpha=alpha)
        w = np.maximum(np.abs(coeffs_x[0][key]), np.abs(coeffs_y[0][key]))

        if mask_pad is not None:
            hs = np.where(mask_pad, hs, 0.0)
            w = np.where(mask_pad, w, 0.0)

        hs_maps[key] = hs
        weight_maps[key] = w
        numerator += float(np.sum(hs * w))
        denominator += float(np.sum(w))

    score = float(logistic_inv(numerator / denominator, alpha=alpha) ** 2)
    if return_maps:
        return score, hs_maps, weight_maps
    return score


def haarpsi(
    x: np.ndarray,
    y: np.ndarray,
    level: int = 3,
    mask: np.ndarray | None = None,
    return_maps: bool = False,
):
    return wavepsi(
        x,
        y,
        wavelet="haar",
        level=level,
        mask=mask,
        return_maps=return_maps,
    )


def compare_mri_reconstructions(
    gt: np.ndarray,
    recon_volumes: dict[str, np.ndarray],
    mask: np.ndarray,
    wavelet_families: list[str],
    level: int = 3,
) -> pd.DataFrame:
    rows = []
    gt_norm = normalize_to_255(gt, mask)
    for recon_name, recon_vol in recon_volumes.items():
        recon_norm = normalize_to_255(recon_vol, mask)
        rmse_value = rmse(gt_norm, recon_norm, mask=mask)
        ssim_value = float(ssim(gt_norm, recon_norm, data_range=255.0))
        for wavelet_name in wavelet_families:
            score = wavepsi(gt, recon_vol, wavelet=wavelet_name, level=level, mask=mask)
            rows.append(
                {
                    "reconstruccion": recon_name,
                    "wavelet": wavelet_name,
                    "WavePsi": score,
                    "RMSE": rmse_value,
                    "SSIM": ssim_value,
                }
            )
    return pd.DataFrame(rows)
