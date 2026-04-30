import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def load_nifti_volume(filepath):
    img = nib.load(str(filepath))
    return img.get_fdata(), img.affine, img.header

def load_grayscale_image(filepath):
    img = plt.imread(str(filepath))
    if img.ndim == 3:
        img = img.mean(axis=2)
    return img

def central_slice(vol, axis=2):
    """Retorna el corte central de un volumen a lo largo de un eje."""
    if axis == 0:
        return vol[vol.shape[0]//2, :, :]
    elif axis == 1:
        return vol[:, vol.shape[1]//2, :]
    else:
        return vol[:, :, vol.shape[2]//2]
