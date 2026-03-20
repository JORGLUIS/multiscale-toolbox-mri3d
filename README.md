# multiscale-toolbox

Toolbox reusable para procesamiento multiescala de imágenes 2D y volúmenes 3D, orientado a la Tarea 1 de Procesamiento Multiescala de Imágenes.

Incluye:

- filtros promedio, gaussianos, ideales y binomiales.
- filtros esféricos para volúmenes 3D.
- construcción de pirámides gaussianas y laplacianas en 2D y 3D.
- reconstrucción laplaciana.
- upsampling por inserción de ceros + convolución.
- carga de volúmenes NIfTI.
- métricas de reconstrucción y métricas con máscara.
- reponderación de capas.
- hard threshold y soft threshold.
- utilidades simples de visualización 2D y 3D.

## Instalación local

```bash
pip install -e .
```

## Uso rápido

```python
from pathlib import Path
from multiscale_toolbox import (
    build_laplacian_predictive,
    create_default_filters,
    load_grayscale_image,
    load_nifti_volume,
    masked_correlation,
    psnr,
    reconstruct_laplacian,
)

img = load_grayscale_image(Path("example1.png"))
filters = create_default_filters()
lap, residual, _ = build_laplacian_predictive(img, filters["Gauss sigma=1"], levels=5)
rec = reconstruct_laplacian(lap, residual)
print(psnr(img, rec))

volume, affine, header = load_nifti_volume(Path("unwrapped_seguetotalphase.nii"))
filters_3d = create_default_filters(ndim=3)
lap3d, residual3d, _ = build_laplacian_predictive(volume, filters_3d["Esferico r=2"], levels=5)
background_like = reconstruct_laplacian([], residual3d)
print(background_like.shape, masked_correlation(volume, background_like))
```
