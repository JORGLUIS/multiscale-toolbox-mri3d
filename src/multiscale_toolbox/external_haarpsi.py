from __future__ import annotations

import numpy as np
from scipy import signal


# Minimal grayscale NumPy adaptation of rgcda/haarpsi/haarPsi.py (MIT).
# Original Python implementation by David Neumann; adapted here as a local,
# dependency-light base for the Task 2 WavePsi/HaarPSI workflow.


def repo_sigmoid(value: np.ndarray | float, alpha: float = 4.2) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-alpha * value))


def repo_logit(value: np.ndarray | float, alpha: float = 4.2) -> np.ndarray:
    value = np.clip(value, 1e-6, 1 - 1e-6)
    return np.log(value / (1 - value)) / alpha


def repo_convolve2d(data: np.ndarray, kernel: np.ndarray, mode: str = "same") -> np.ndarray:
    rotated_data = np.rot90(data, 2)
    rotated_kernel = np.rot90(kernel, 2)
    result = signal.convolve2d(rotated_data, rotated_kernel, mode=mode)
    return np.rot90(result, 2)


def repo_subsample(image: np.ndarray) -> np.ndarray:
    subsampled = repo_convolve2d(image, np.ones((2, 2), dtype=float) / 4.0, mode="same")
    return subsampled[::2, ::2]


def repo_haar_wavelet_decompose(image: np.ndarray, number_of_scales: int = 3) -> np.ndarray:
    coefficients = np.zeros((*image.shape, 2 * number_of_scales), dtype=float)
    for scale in range(1, number_of_scales + 1):
        haar_filter = 2 ** (-scale) * np.ones((2**scale, 2**scale), dtype=float)
        haar_filter[: haar_filter.shape[0] // 2, :] *= -1
        coefficients[:, :, scale - 1] = repo_convolve2d(image, haar_filter, mode="same")
        coefficients[:, :, scale + number_of_scales - 1] = repo_convolve2d(
            image, haar_filter.T, mode="same"
        )
    return coefficients


def haarpsi_repo(
    reference_image: np.ndarray,
    distorted_image: np.ndarray,
    preprocess_with_subsampling: bool = True,
) -> tuple[float, np.ndarray, np.ndarray]:
    reference_image = np.asarray(reference_image, dtype=np.float64)
    distorted_image = np.asarray(distorted_image, dtype=np.float64)

    if reference_image.shape != distorted_image.shape:
        raise ValueError("The shapes of the reference image and the distorted image do not match.")
    if reference_image.ndim == 3 and reference_image.shape[2] == 1:
        reference_image = reference_image[:, :, 0]
        distorted_image = distorted_image[:, :, 0]
    if reference_image.ndim != 2:
        raise ValueError("haarpsi_repo only supports grayscale 2D images.")

    c = 30.0
    alpha = 4.2
    number_of_scales = 3

    if preprocess_with_subsampling:
        reference_image = repo_subsample(reference_image)
        distorted_image = repo_subsample(distorted_image)

    coeffs_ref = repo_haar_wavelet_decompose(reference_image, number_of_scales)
    coeffs_dist = repo_haar_wavelet_decompose(distorted_image, number_of_scales)

    local_similarities = np.zeros((*reference_image.shape, 2), dtype=float)
    weights = np.zeros((*reference_image.shape, 2), dtype=float)

    for orientation in range(2):
        weights[:, :, orientation] = np.maximum(
            np.abs(coeffs_ref[:, :, 2 + orientation * number_of_scales]),
            np.abs(coeffs_dist[:, :, 2 + orientation * number_of_scales]),
        )
        ref_mag = np.abs(
            coeffs_ref[:, :, (orientation * number_of_scales, 1 + orientation * number_of_scales)]
        )
        dist_mag = np.abs(
            coeffs_dist[:, :, (orientation * number_of_scales, 1 + orientation * number_of_scales)]
        )
        local_similarities[:, :, orientation] = np.sum(
            (2 * ref_mag * dist_mag + c) / (ref_mag**2 + dist_mag**2 + c),
            axis=2,
        ) / 2.0

    score = float(
        repo_logit(
            np.sum(repo_sigmoid(local_similarities, alpha=alpha) * weights) / np.sum(weights),
            alpha=alpha,
        )
        ** 2
    )
    return score, local_similarities, weights
