# multiscale-toolbox

Toolbox reutilizable para procesamiento multiescala de imágenes 2D y volúmenes 3D.

Este repositorio concentra el trabajo desarrollado para las tareas del curso:

- `multiscale_toolbox`: utilidades base de pirámides, MRI 3D, `WavePsi`, `HaarPSI` y denoising `DWT 2D`.
- `multiscale_toolbox_t3`: utilidades específicas de la Tarea 3 para Starlets 2D/3D, transformada multiescala de mediana y aproximaciones tipo SMV.
- `multiscale_toolbox_t4`: utilidades específicas de la Tarea 4 para deconvolución de imágenes con regularización multiescala.

## Contenido relevante para la Tarea 3

El paquete `src/multiscale_toolbox_t3` incluye las funciones usadas por el notebook `Tarea3_JorgeMedina.ipynb`:

- `starlet_decomp_2d`, `starlet_recon_2d`
- `mmt_decomp_2d`, `mmt_recon_2d`
- `starlet_decomp_3d`, `starlet_recon_3d`
- `threshold_coeffs`, `mad_sigma`
- `add_gaussian_noise`, `add_uniform_noise`
- `rmse`, `evaluate_sim`
- `get_HJ_filter`, `smv_deconv_direct`, `smv_deconv_tikhonov`
- `load_nifti_volume`, `load_grayscale_image`, `central_slice`

## Contenido relevante para la Tarea 4

El paquete `src/multiscale_toolbox_t4` incluye el código usado por el notebook `Tarea4_JorgeMedina.ipynb`.
Esta parte cubre la deconvolución de imágenes con regularización multiescala, comparando DWT, Starlet y MMT con PGD y ADMM.

Funciones principales:

- `BlurOperator`, `gaussian_psf`, `psf2otf`
- `starlet_decomp`, `starlet_recon`
- `mmt_decomp`, `mmt_recon`
- `prox_starlet`, `prox_mmt`, `prox_dwt`, `make_prox`
- `projected_gradient`, `admm`
- `rmse`, `ssim_metric`
- `add_gaussian`, `add_uniform`, `add_impulse`

## Flujo esperado de uso

Los notebooks del curso pueden clonar este repositorio en una carpeta local `github_repo` e importar los módulos directamente desde `src`.

En particular, la versión actual de `Tarea3_JorgeMedina.ipynb`:

- clona o actualiza `JORGLUIS/multiscale-toolbox-mri3d`,
- agrega `github_repo/src` al `sys.path`,
- e importa `multiscale_toolbox_t3` únicamente desde ese clon.

Para la Tarea 4, `Tarea4_JorgeMedina.ipynb` sigue el mismo flujo:

- clona o actualiza `JORGLUIS/multiscale-toolbox-mri3d`,
- agrega `github_repo/src` al `sys.path`,
- e importa `multiscale_toolbox_t4` para usar los operadores, regularizadores, algoritmos y métricas de la tarea.

## Dependencias

El proyecto requiere Python `>=3.10` y usa principalmente:

- `numpy`
- `scipy`
- `pandas`
- `matplotlib`
- `pillow`
- `nibabel`
- `PyWavelets`
- `scikit-image`
