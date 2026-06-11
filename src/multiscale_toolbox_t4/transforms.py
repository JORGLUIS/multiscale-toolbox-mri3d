"""
transforms.py — Tarea 4 (IEE3787)
Transformadas multiescala no decimadas (Starlet, MMT) y DWT ortogonal,
mas sus operadores prox de regularizacion por umbral suave.
"""

import numpy as np
from scipy import ndimage
import pywt


# ---------------------------------------------------------------------------
# Starlet (a trous)
# ---------------------------------------------------------------------------

def _starlet_filter_1d(name='b3'):
    if name == 'b3':
        return np.array([1, 4, 6, 4, 1]) / 16.0
    if name == 'linear':
        return np.array([1, 2, 1]) / 4.0
    if name == 'haar':
        return np.array([1, 1]) / 2.0
    raise ValueError("Filtro Starlet no reconocido: %s" % name)


def _upsample_filter(h, step):
    if step == 1:
        return h
    h_up = np.zeros(len(h) + (len(h) - 1) * (step - 1))
    h_up[::step] = h
    return h_up


def starlet_decomp(img, levels=4, filter_name='b3'):
    """Transformada Starlet 2D no decimada (algoritmo a trous).

    Parameters
    ----------
    img : ndarray 2D
    levels : int — numero de escalas de detalle
    filter_name : str — 'b3' | 'linear' | 'haar'

    Returns
    -------
    list de (levels+1) arrays: [w_1, ..., w_J, c_J]
    """
    h1 = _starlet_filter_1d(filter_name)
    coeffs = []
    c = img.astype(float)
    for j in range(levels):
        hj = _upsample_filter(h1, 2 ** j)
        c_next = ndimage.convolve1d(c, hj, axis=0, mode='reflect')
        c_next = ndimage.convolve1d(c_next, hj, axis=1, mode='reflect')
        coeffs.append(c - c_next)
        c = c_next
    coeffs.append(c)
    return coeffs


def starlet_recon(coeffs):
    """Reconstruccion Starlet: suma directa de todos los planos."""
    out = np.zeros_like(coeffs[0])
    for w in coeffs:
        out += w
    return out


# ---------------------------------------------------------------------------
# MMT (Multiscale Median Transform)
# ---------------------------------------------------------------------------

def _footprint(radius, shape='square'):
    s = 2 * radius + 1
    fp = np.zeros((s, s), dtype=int)
    y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1]
    if shape == 'square':
        fp[:, :] = 1
    elif shape == 'circle':
        fp[x**2 + y**2 <= radius**2] = 1
    elif shape == 'diamond':
        fp[np.abs(x) + np.abs(y) <= radius] = 1
    else:
        raise ValueError("Kernel MMT no reconocido: %s" % shape)
    return fp


def mmt_decomp(img, levels=4, kernel_shape='square'):
    """Multiscale Median Transform (MMT) no decimada.

    Parameters
    ----------
    img : ndarray 2D
    levels : int
    kernel_shape : str — 'square' | 'circle' | 'diamond'

    Returns
    -------
    list de (levels+1) arrays: [w_1, ..., w_J, c_J]
    """
    coeffs = []
    c = img.astype(float)
    radius = 1
    for j in range(levels):
        fp = _footprint(radius, shape=kernel_shape)
        c_next = ndimage.median_filter(c, footprint=fp, mode='reflect')
        coeffs.append(c - c_next)
        c = c_next
        radius *= 2
    coeffs.append(c)
    return coeffs


def mmt_recon(coeffs):
    """Reconstruccion MMT (aditiva)."""
    out = np.zeros_like(coeffs[0])
    for w in coeffs:
        out += w
    return out


# ---------------------------------------------------------------------------
# Umbral suave y operadores prox
# ---------------------------------------------------------------------------

def _soft(x, thr):
    return np.sign(x) * np.maximum(np.abs(x) - thr, 0.0)


def prox_starlet(x, thr, levels=4, filter_name='b3'):
    """Prox de regularizacion Starlet: umbral suave en coeficientes de detalle."""
    c = starlet_decomp(x, levels=levels, filter_name=filter_name)
    c = [_soft(w, thr) for w in c[:-1]] + [c[-1]]
    return starlet_recon(c)


def prox_mmt(x, thr, levels=4, kernel_shape='square'):
    """Prox de regularizacion MMT: umbral suave en coeficientes de detalle."""
    c = mmt_decomp(x, levels=levels, kernel_shape=kernel_shape)
    c = [_soft(w, thr) for w in c[:-1]] + [c[-1]]
    return mmt_recon(c)


def prox_dwt(x, thr, levels=4, wavelet='db2'):
    """Prox via DWT ortogonal: umbraliza solo subcoeficientes de detalle."""
    coeffs = pywt.wavedec2(x, wavelet, level=levels, mode='periodization')
    new = [coeffs[0]]
    for det in coeffs[1:]:
        new.append(tuple(_soft(b, thr) for b in det))
    return pywt.waverec2(new, wavelet, mode='periodization')


def make_prox(reg, levels, **kw):
    """Fabrica un prox unificado prox(x, thr) segun el regularizador.

    Parameters
    ----------
    reg : str — 'starlet' | 'mmt' | 'dwt'
    levels : int — numero de escalas
    **kw : opciones especificas (filter_name, kernel_shape, wavelet)

    Returns
    -------
    callable(x, thr) -> ndarray
    """
    if reg == 'starlet':
        fname = kw.get('filter_name', 'b3')
        return lambda x, thr: prox_starlet(x, thr, levels=levels, filter_name=fname)
    if reg == 'mmt':
        ks = kw.get('kernel_shape', 'square')
        return lambda x, thr: prox_mmt(x, thr, levels=levels, kernel_shape=ks)
    if reg == 'dwt':
        wv = kw.get('wavelet', 'db2')
        return lambda x, thr: prox_dwt(x, thr, levels=levels, wavelet=wv)
    raise ValueError("Regularizador no soportado: %s" % reg)
