import numpy as np

def add_gaussian_noise(img, mean=0.0, var=0.01):
    """Agrega ruido gaussiano usando media y varianza especificadas."""
    sigma = np.sqrt(var)
    noise = np.random.normal(mean, sigma, img.shape)
    return img + noise

def add_uniform_noise(img, low=-0.1, high=0.1):
    """Agrega ruido uniforme en un rango definido."""
    noise = np.random.uniform(low, high, img.shape)
    return img + noise
