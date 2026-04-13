# multiscale-toolbox

Repositorio local preparado para sincronizarse con `JORGLUIS/multiscale-toolbox-mri3d`.

En esta tarea agrego utilidades centradas en dos frentes:

- `WavePsi` y `HaarPSI` aproximado para comparación perceptual en 2D y 3D.
- denoising con `DWT 2D` para imágenes astronómicas.

Funciones principales agregadas para la Tarea 2:

- `ensure_extracted`
- `load_task2_mri_data`
- `load_task2_astronomy_images`
- `wavepsi`
- `haarpsi`
- `compare_mri_reconstructions`
- `add_gaussian_noise`
- `add_uniform_noise`
- `denoise_dwt2`
- `evaluate_denoising_grid`

El notebook `Tarea2_2026_WavePsi_y_DWT2D.ipynb` usa una estrategia `GitHub-first`:

- primero intenta descargar `JORGLUIS/multiscale-toolbox-mri3d` desde GitHub;
- si ese repo todavía no contiene los módulos de la Tarea 2, usa este mirror local en `toolbox_repo/src/multiscale_toolbox`.

Así, una vez que el repo remoto se sincronice, el notebook pasará a importar desde GitHub sin cambiar el flujo del análisis.
