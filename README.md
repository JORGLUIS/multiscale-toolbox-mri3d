# multiscale-toolbox

Toolbox reutilizable para procesamiento multiescala de imágenes 2D y volúmenes 3D, orientado a la Tarea 1 de Procesamiento Multiescala de Imágenes.

Incluye:

- filtros promedio, gaussianos, ideales y binomiales;
- filtros esféricos para volúmenes 3D;
- construcción de pirámides gaussianas y laplacianas en 2D y 3D;
- reconstrucción laplaciana;
- upsampling por inserción de ceros + convolución;
- carga de volúmenes NIfTI;
- métricas de reconstrucción y métricas con máscara;
- reponderación de capas;
- hard threshold y soft threshold;
- utilidades simples de visualización 2D y 3D.

## Instalación local

```bash
pip install -e .
```

## Funciones útiles para la Parte 3

La Parte 3 de la tarea pide extender la descomposición/reconstrucción a 3D y usar una pirámide laplaciana para analizar la fase total en RM. Las funciones más importantes para eso son estas:

- `load_nifti_volume(path)`
  - Carga un volumen NIfTI y retorna `volume`, `affine` y `header`.
  - Se usa para leer volúmenes como `unwrapped_seguetotalphase.nii` y `mask4.nii`.

- `create_default_filters(ndim=3)`
  - Construye el conjunto de funciones de escalamiento para 3D.
  - Entrega filtros como `Promedio 3x3x3`, `Gauss sigma=1`, `Gauss sigma=2`, `Binomial [1,2,1]` y `Esferico r=2`.

- `build_laplacian_predictive(x, scaling_fn, levels=5)`
  - Hace la descomposición multiescala.
  - Retorna:
    - `lap`: lista de capas laplacianas de detalle;
    - `residual`: componente más suave al final de la pirámide;
    - `gauss`: niveles gaussianos intermedios.
  - Esta es la función principal de descomposición para la Parte 3.

- `reconstruct_laplacian(lap, residual)`
  - Reconstruye el volumen completo a partir de las capas de detalle y el residual.
  - Sirve para verificar que la extensión a 3D sea correcta y que el error de reconstrucción sea pequeño.

- `reconstruct_selected_layers(lap, residual, active_levels=None, include_residual=True)`
  - Reconstruye solo ciertas partes de la pirámide.
  - Es útil para analizar por separado:
    - solo el residual;
    - solo los detalles;
    - el detalle fino `L0`;
    - los detalles `L1..fin`.

- `masked_rmse(a, b, mask=None)`
  - Calcula RMSE opcionalmente restringido a una máscara.
  - En la Parte 3 es útil para cuantificar el error de reconstrucción dentro del objeto y no fuera de él.

- `laplacian_energy(x, mask=None)`
  - Calcula la energía del Laplaciano de un volumen o imagen.
  - Sirve como indicador práctico de qué tan “suave” u “armónico” es un residual.
  - En la Parte 3 ayuda a comparar filtros y ver si el residual se acerca a un comportamiento más armónico.

- `show_volume_slices(volume, title, indices=None, cmap="gray", symmetric=False)`
  - Muestra cortes axial, coronal y sagital de un volumen 3D.
  - Se usa para inspeccionar visualmente el campo total, el residual y las reconstrucciones parciales.

## Flujo típico para la Parte 3

```python
from pathlib import Path
from multiscale_toolbox import (
    build_laplacian_predictive,
    create_default_filters,
    laplacian_energy,
    load_nifti_volume,
    masked_rmse,
    reconstruct_laplacian,
    reconstruct_selected_layers,
    show_volume_slices,
)

data_dir = Path("CLASES/1/Clase1_material")
total_phase, _, _ = load_nifti_volume(data_dir / "unwrapped_seguetotalphase.nii")
mask, _, _ = load_nifti_volume(data_dir / "mask4.nii")
mask_bool = mask > 0.5

filters_3d = create_default_filters(ndim=3)
lap, residual, gauss = build_laplacian_predictive(
    total_phase,
    filters_3d["Esferico r=2"],
    levels=5,
)

rec = reconstruct_laplacian(lap, residual)
print("RMSE reconstrucción:", masked_rmse(total_phase, rec, mask_bool))
print("Energía laplaciana residual:", laplacian_energy(residual))

residual_only = reconstruct_selected_layers(lap, residual, active_levels=[], include_residual=True)
details_only = reconstruct_selected_layers(
    lap,
    residual,
    active_levels=list(range(len(lap))),
    include_residual=False,
)

show_volume_slices(total_phase, "Campo total", symmetric=True)
show_volume_slices(residual_only, "Residual", symmetric=True)
show_volume_slices(details_only, "Detalles", symmetric=True)
```
