# multiscale-toolbox

Toolbox reutilizable para procesamiento multiescala de imagenes 2D y volumenes 3D.

Actualmente cubre dos frentes:

- utilidades para piramides gaussianas y laplacianas en 2D/3D;
- utilidades para la Tarea 2: `WavePsi`/`HaarPSI` aproximado y denoising con `DWT 2D`.

Incluye:

- filtros promedio, gaussianos, ideales y binomiales;
- filtros esfericos para volumenes 3D;
- construccion de piramides gaussianas y laplacianas en 2D y 3D;
- reconstruccion laplaciana;
- upsampling por insercion de ceros + convolucion;
- carga de volumenes NIfTI;
- metricas de reconstruccion y metricas con mascara;
- hard threshold y soft threshold;
- `WavePsi` y `HaarPSI` aproximado para 2D y 3D;
- denoising de imagenes 2D con wavelets;
- utilidades de visualizacion y carga de datos.

## Instalacion local

```bash
pip install -e .
```

## Funciones importantes para la Tarea 2

### Parte 1: MRI 3D y WavePsi

- `load_task2_mri_data(data_dir)`
  - Carga el volumen de referencia, la mascara y las reconstrucciones MRI.
  - Ademas recorta automaticamente al bounding box de la mascara para trabajar sobre la region util.

- `wavepsi(x, y, wavelet='haar', level=3, mask=None, return_maps=False)`
  - Implementa la metrica perceptual multiescala basada en wavelets no decimadas.
  - Si `return_maps=True`, tambien retorna mapas locales de similitud y pesos.

- `haarpsi(x, y, level=3, mask=None)`
  - Atajo para usar `wavepsi` con base `haar`.

- `compare_mri_reconstructions(gt, recon_volumes, mask, wavelet_families, level=3)`
  - Genera una tabla comparativa con `WavePsi`, `RMSE` y `SSIM` para todas las reconstrucciones.

### Parte 2: Denoising de imagenes astronomicas

- `load_task2_astronomy_images(data_dir)`
  - Carga `Moon.png` y `EX3_01.png` en escala de grises normalizada.

- `add_gaussian_noise(x, sigma=0.08, seed=None)`
  - Agrega ruido gaussiano aditivo.

- `add_uniform_noise(x, low=-0.14, high=0.14, seed=None)`
  - Agrega ruido uniforme aditivo.

- `denoise_dwt2(x, wavelet='haar', level=3, threshold_mode='soft')`
  - Descompone con `DWT 2D`, umbraliza coeficientes y reconstruye la imagen.

- `evaluate_denoising_grid(astro_images, noisy_images, wavelets_2d, levels_2d, threshold_modes)`
  - Evalua en bloque varias combinaciones de wavelet, nivel y metodo de umbralizacion.

## Funciones importantes del toolbox base

- `load_nifti_volume(path)`
- `create_default_filters(ndim=3)`
- `build_laplacian_predictive(x, scaling_fn, levels=5)`
- `reconstruct_laplacian(lap, residual)`
- `reconstruct_selected_layers(lap, residual, active_levels=None, include_residual=True)`
- `masked_rmse(a, b, mask=None)`
- `laplacian_energy(x, mask=None)`
- `show_volume_slices(volume, title, indices=None, cmap="gray", symmetric=False)`

## Nota sobre el notebook de la Tarea 2

El notebook de la tarea usa una estrategia `GitHub-first`:

- primero intenta importar desde este repositorio remoto;
- si el entorno local todavia no esta sincronizado, puede usar un mirror local temporal.

Una vez que el repositorio remoto tenga publicadas las funciones nuevas, el notebook podra importar directamente desde GitHub sin fallback.
