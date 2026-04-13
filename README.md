# multiscale-toolbox

Toolbox reutilizable para procesamiento multiescala en 2D y 3D, alineado con el estado actual de `Tarea2_.ipynb`.

Este repositorio cubre dos frentes de la Tarea 2:

- `WavePsi` y `HaarPSI` para comparacion perceptual en imagenes 2D y volumenes MRI 3D.
- Denoising con `DWT 2D` para imagenes astronomicas.

## Instalacion local

```bash
pip install -e .
```

## Funciones principales para la Tarea 2

### Parte 1: MRI 3D y WavePsi

- `load_task2_mri_data(data_dir)`
- `haarpsi_repo(x, y, preprocess_with_subsampling=True)`
- `wavepsi(x, y, wavelet='haar', level=3, mask=None, return_maps=False)`
- `haarpsi(x, y, level=3, mask=None, return_maps=False)`
- `compare_mri_reconstructions(gt, recon_volumes, mask, wavelet_families, level=3)`

Notas:

- `haarpsi_repo` es un wrapper local adaptado desde la implementacion abierta `rgcda/haarpsi` (MIT).
- `wavepsi` usa esa base exacta para el caso 2D con Haar y generaliza el calculo a otras wavelets y a volumenes 3D.
- `return_maps=True` entrega mapas locales de similitud y pesos direccionales.

### Parte 2: Denoising de imagenes astronomicas

- `load_task2_astronomy_images(data_dir)`
- `add_gaussian_noise(x, sigma=0.08, seed=None)`
- `add_uniform_noise(x, low=-0.14, high=0.14, seed=None)`
- `denoise_dwt2(x, wavelet='haar', level=3, threshold_mode='soft')`
- `evaluate_denoising_grid(astro_images, noisy_images, wavelets_2d, levels_2d, threshold_modes)`

## Toolbox base reutilizable

El paquete tambien mantiene utilidades para:

- piramides gaussianas y laplacianas en 2D y 3D;
- filtros promedio, gaussianos, ideales y binomiales;
- filtros esfericos para volumenes 3D;
- reconstruccion laplaciana y seleccion de capas;
- carga de volumenes NIfTI;
- metricas con y sin mascara;
- visualizacion de cortes y niveles multiescala.

## Compatibilidad con `Tarea2_.ipynb`

El notebook actual:

- importa el paquete `multiscale_toolbox`;
- espera encontrar `load_task2_mri_data`, `load_task2_astronomy_images`, `wavepsi`, `haarpsi_repo`, `denoise_dwt2` y `evaluate_denoising_grid`;
- trabaja en modo local-first y deja GitHub como referencia remota del toolbox.

La referencia remota esperada por el notebook es:

- `https://raw.githubusercontent.com/JORGLUIS/multiscale-toolbox-wavepsi-dwt2d/main`
