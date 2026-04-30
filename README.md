# multiscale-toolbox

Toolbox reutilizable para procesamiento multiescala de imagenes 2D y volumenes 3D.

Este repositorio concentra el trabajo desarrollado para las tareas del curso:

- `multiscale_toolbox`: utilidades base de piramides, MRI 3D, `WavePsi`, `HaarPSI` y denoising `DWT 2D`.
- `multiscale_toolbox_t3`: utilidades especificas de la Tarea 3 para Starlets 2D/3D, transformada multiescala de mediana y aproximaciones tipo SMV.

## Contenido relevante para la Tarea 3

La package `src/multiscale_toolbox_t3` incluye las funciones usadas por el notebook `Tarea3_JorgeMedina.ipynb`:

- `starlet_decomp_2d`, `starlet_recon_2d`
- `mmt_decomp_2d`, `mmt_recon_2d`
- `starlet_decomp_3d`, `starlet_recon_3d`
- `threshold_coeffs`, `mad_sigma`
- `add_gaussian_noise`, `add_uniform_noise`
- `rmse`, `evaluate_sim`
- `get_HJ_filter`, `smv_deconv_direct`, `smv_deconv_tikhonov`
- `load_nifti_volume`, `load_grayscale_image`, `central_slice`

## Flujo esperado de uso

Los notebooks del curso pueden clonar este repositorio en una carpeta local `github_repo` e importar los modulos directamente desde `src`.

En particular, la version actual de `Tarea3_JorgeMedina.ipynb`:

- clona o actualiza `JORGLUIS/multiscale-toolbox-mri3d`,
- agrega `github_repo/src` al `sys.path`,
- e importa `multiscale_toolbox_t3` unicamente desde ese clon.

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
