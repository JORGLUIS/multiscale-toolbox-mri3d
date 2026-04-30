import numpy as np
from skimage.metrics import structural_similarity as ssim

def rmse(v_ref, v_cmp, mask=None):
    """Calcula el RMSE (Root Mean Squared Error). Mismo que en clase."""
    diff = np.abs(v_ref - v_cmp) ** 2
    if mask is not None:
        diff = diff[mask > 0]
    return np.sqrt(np.mean(diff))

def evaluate_sim(v_ref, v_cmp, mask=None):
    """Evalua usando SSIM (skimage). Si requiere HaarPSI importarlo del toolbox original si esta disponible."""
    # Para ssim en imagenes medicas se ajusta data_range
    drange = v_ref.max() - v_ref.min()
    val = ssim(v_ref, v_cmp, data_range=drange)
    return val
