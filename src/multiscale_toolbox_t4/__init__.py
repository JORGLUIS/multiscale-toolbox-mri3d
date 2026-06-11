"""
multiscale_toolbox_t4 — Tarea 4 (IEE3787)
Deconvolucion de imagenes con regularizacion multiescala.

Uso rapido
----------
>>> from multiscale_toolbox_t4 import BlurOperator, make_prox, projected_gradient, admm
>>> from multiscale_toolbox_t4 import rmse, ssim_metric, add_gaussian
"""

from .operators import BlurOperator, gaussian_psf, psf2otf
from .transforms import (
    starlet_decomp, starlet_recon,
    mmt_decomp, mmt_recon,
    prox_starlet, prox_mmt, prox_dwt,
    make_prox,
)
from .optim import projected_gradient, admm
from .metrics import rmse, ssim_metric, add_gaussian, add_uniform, add_impulse

__version__ = "0.1.0"
__all__ = [
    "BlurOperator", "gaussian_psf", "psf2otf",
    "starlet_decomp", "starlet_recon",
    "mmt_decomp", "mmt_recon",
    "prox_starlet", "prox_mmt", "prox_dwt", "make_prox",
    "projected_gradient", "admm",
    "rmse", "ssim_metric", "add_gaussian", "add_uniform", "add_impulse",
]
