"""
operators.py — Tarea 4 (IEE3787)
Operador de desenfoque gaussiano circular via FFT y su adjunto.
"""

import numpy as np


def gaussian_psf(shape, sigma):
    """PSF gaussiano normalizado, centrado en el origen."""
    ny, nx = shape
    yy = np.arange(ny) - ny // 2
    xx = np.arange(nx) - nx // 2
    Y, X = np.meshgrid(yy, xx, indexing='ij')
    psf = np.exp(-(X**2 + Y**2) / (2.0 * sigma**2))
    psf /= psf.sum()
    return psf


def psf2otf(psf):
    """Convierte un PSF centrado a su OTF (convolucion circular via fft2)."""
    psf = np.fft.ifftshift(psf)
    return np.fft.fft2(psf)


class BlurOperator:
    """Operador de desenfoque H (FFT) y su adjunto H^T.

    Como el PSF es real y simetrico, H ~ H^T; se usa conjugado de la OTF
    para exactitud numerica.

    Parameters
    ----------
    shape : tuple (ny, nx)
    sigma : float — desviacion estandar del PSF gaussiano en pixeles
    """

    def __init__(self, shape, sigma):
        self.shape = shape
        self.sigma = sigma
        self.psf = gaussian_psf(shape, sigma)
        self.otf = psf2otf(self.psf)
        self.otf_conj = np.conj(self.otf)
        self.otf_abs2 = np.abs(self.otf) ** 2

    def forward(self, x):
        """H x — aplica el desenfoque."""
        return np.real(np.fft.ifft2(self.otf * np.fft.fft2(x)))

    def adjoint(self, x):
        """H^T x — adjunto del desenfoque."""
        return np.real(np.fft.ifft2(self.otf_conj * np.fft.fft2(x)))
