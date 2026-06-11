"""
metrics.py — Tarea 4 (IEE3787)
Metricas de calidad de imagen y funciones para agregar ruido.
"""

import numpy as np


def rmse(a, b):
    """Root Mean Square Error entre dos arrays."""
    return float(np.sqrt(np.mean((np.asarray(a, float) - np.asarray(b, float)) ** 2)))


def ssim_metric(ref, cmp):
    """SSIM entre dos imagenes 2D (usa data_range = max-min de la referencia)."""
    from skimage.metrics import structural_similarity as ssim
    dr = float(np.asarray(ref).max() - np.asarray(ref).min())
    return float(ssim(ref, cmp, data_range=dr))


def add_gaussian(img, sigma, rng):
    """Agrega ruido gaussiano de desviacion estandar sigma."""
    return np.asarray(img, float) + rng.normal(0.0, sigma, np.shape(img))


def add_uniform(img, half, rng):
    """Agrega ruido uniforme en [-half, half]."""
    return np.asarray(img, float) + rng.uniform(-half, half, np.shape(img))


def add_impulse(img, p, rng):
    """Ruido impulsional (sal y pimienta) sobre fraccion p de pixeles."""
    out = np.array(img, float, copy=True)
    m = rng.random(np.shape(img))
    out[m < p / 2] = 0.0
    out[m > 1 - p / 2] = 1.0
    return out
