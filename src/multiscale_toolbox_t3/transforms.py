import numpy as np
from scipy import signal, ndimage

def get_starlet_filter_1d(name='b3'):
    if name == 'b3':
        h = np.array([1, 4, 6, 4, 1]) / 16.0
    elif name == 'linear':
        h = np.array([1, 2, 1]) / 4.0
    elif name == 'haar':
        h = np.array([1, 1]) / 2.0
    else:
        raise ValueError("Filter no soportado")
    return h

def upsample_filter(h, step):
    """Upsample filter h by inserting step-1 zeros between elements."""
    if step == 1:
        return h
    h_up = np.zeros(len(h) + (len(h) - 1) * (step - 1))
    h_up[::step] = h
    return h_up

def starlet_decomp_2d(img, levels=5, filter_name='b3'):
    """Descomposicion Starlets 2D."""
    h1 = get_starlet_filter_1d(filter_name)
    coeffs = []
    c = img.astype(float)
    for j in range(levels):
        step = 2**j
        hj = upsample_filter(h1, step)
        # Separable convolution
        c_next = ndimage.convolve1d(c, hj, axis=0, mode='reflect')
        c_next = ndimage.convolve1d(c_next, hj, axis=1, mode='reflect')
        w = c - c_next
        coeffs.append(w)
        c = c_next
    coeffs.append(c) # residual
    return coeffs

def starlet_recon_2d(coeffs):
    """Reconstruccion Starlets 2D."""
    # Como w_j = c_{j-1} - c_j, x = c_J + sum_j w_j
    recon = np.zeros_like(coeffs[0])
    for w in coeffs:
        recon += w
    return recon

def create_footprint(radius, shape='square'):
    """Crea footprint 2D para filtro de mediana."""
    s = 2 * radius + 1
    fp = np.zeros((s, s), dtype=int)
    y, x = np.ogrid[-radius:radius+1, -radius:radius+1]
    
    if shape == 'square':
        fp[:, :] = 1
    elif shape == 'circle':
        fp[x**2 + y**2 <= radius**2] = 1
    elif shape == 'diamond':
        fp[np.abs(x) + np.abs(y) <= radius] = 1
    else:
        raise ValueError("Shape no soportado")
    return fp

def mmt_decomp_2d(img, levels=5, kernel_shape='square'):
    """Transformada Multiescala de Mediana 2D."""
    coeffs = []
    c = img.astype(float)
    radius = 1
    for j in range(levels):
        fp = create_footprint(radius, shape=kernel_shape)
        c_next = ndimage.median_filter(c, footprint=fp, mode='reflect')
        w = c - c_next
        coeffs.append(w)
        c = c_next
        radius *= 2 # doblamos el radio
    coeffs.append(c) # residual
    return coeffs

def mmt_recon_2d(coeffs):
    """Reconstruccion MMT 2D."""
    recon = np.zeros_like(coeffs[0])
    for w in coeffs:
        recon += w
    return recon

def starlet_decomp_3d(vol, levels=3, filter_name='b3'):
    """Descomposicion Starlets 3D."""
    h1 = get_starlet_filter_1d(filter_name)
    coeffs = []
    c = vol.astype(float)
    for j in range(levels):
        step = 2**j
        hj = upsample_filter(h1, step)
        c_next = ndimage.convolve1d(c, hj, axis=0, mode='reflect')
        c_next = ndimage.convolve1d(c_next, hj, axis=1, mode='reflect')
        c_next = ndimage.convolve1d(c_next, hj, axis=2, mode='reflect')
        w = c - c_next
        coeffs.append(w)
        c = c_next
    coeffs.append(c)
    return coeffs

def starlet_recon_3d(coeffs):
    recon = np.zeros_like(coeffs[0])
    for w in coeffs:
        recon += w
    return recon

def threshold_coeffs(coeffs, threshold_val, mode='soft'):
    """Aplica umbralizacion a los coeficientes de detalle."""
    n_levels = len(coeffs) - 1
    new_coeffs = []
    for j in range(n_levels):
        w = coeffs[j]
        # threshold puede ser un escalar o una lista
        thr = threshold_val[j] if isinstance(threshold_val, (list, np.ndarray)) else threshold_val
        if mode == 'soft':
            new_w = np.sign(w) * np.maximum(np.abs(w) - thr, 0)
        elif mode == 'hard':
            new_w = np.where(np.abs(w) > thr, w, 0)
        new_coeffs.append(new_w)
    new_coeffs.append(coeffs[-1]) # residual sin cambio
    return new_coeffs

def mad_sigma(w):
    """Estimacion robusta de sigma mediante MAD."""
    return np.median(np.abs(w - np.median(w))) / 0.6745
