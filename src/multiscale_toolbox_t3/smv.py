import numpy as np
from .transforms import starlet_decomp_3d

def get_HJ_filter(shape, levels, filter_name='b3'):
    """Calcula la respuesta en frecuencia HJ del low-pass c_J."""
    impulse = np.zeros(shape)
    # Impulso en el centro 
    center = tuple([s//2 for s in shape])
    impulse[center] = 1.0
    
    coeffs = starlet_decomp_3d(impulse, levels=levels, filter_name=filter_name)
    cJ_impulse = coeffs[-1]
    
    # FFT shifted ya que el impulso esta en el centro
    HJ_fft = np.fft.fftn(np.fft.ifftshift(cJ_impulse))
    return HJ_fft

def smv_deconv_direct(gJ, HJ_fft, thr=0.1):
    """Deconvolucion directa en Fourier truncando denominadores pequenos."""
    G_fft = np.fft.fftn(gJ)
    Denom = 1.0 - HJ_fft
    
    # Truncacion
    mask = np.abs(Denom) >= thr
    B_loc_fft = np.zeros_like(G_fft)
    B_loc_fft[mask] = G_fft[mask] / Denom[mask]
    
    b_loc = np.fft.ifftn(B_loc_fft).real
    return b_loc

def smv_deconv_tikhonov(gJ, HJ_fft, alpha=1e-2):
    """Deconvolucion regularizada tipo Tikhonov."""
    G_fft = np.fft.fftn(gJ)
    H_pass = 1.0 - HJ_fft
    
    B_loc_fft = (G_fft * np.conj(H_pass)) / (np.abs(H_pass)**2 + alpha)
    b_loc = np.fft.ifftn(B_loc_fft).real
    return b_loc
