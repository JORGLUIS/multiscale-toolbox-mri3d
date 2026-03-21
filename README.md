# multiscale-toolbox

Toolbox reutilizable para procesamiento multiescala de imÃ¡genes 2D y volÃºmenes 3D, orientado a la Tarea 1 de Procesamiento Multiescala de ImÃ¡genes.

Incluye:

- filtros promedio, gaussianos, ideales y binomiales;
- filtros esfÃ©ricos para volÃºmenes 3D;
- construcciÃ³n de pirÃ¡mides gaussianas y laplacianas en 2D y 3D;
- reconstrucciÃ³n laplaciana;
- upsampling por inserciÃ³n de ceros + convoluciÃ³n;
- carga de volÃºmenes NIfTI;
- mÃ©tricas de reconstrucciÃ³n y mÃ©tricas con mÃ¡scara;
- reponderaciÃ³n de capas;
- hard threshold y soft threshold;
- utilidades simples de visualizaciÃ³n 2D y 3D.

## InstalaciÃ³n local

```bash
pip install -e .
```

## Uso rÃ¡pido

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

## Funciones Ãºtiles para la Parte 3

La Parte 3 de la tarea pide extender la descomposiciÃ³n/reconstrucciÃ³n a 3D y usar una pirÃ¡mide laplaciana para analizar la fase total en RM. Las funciones mÃ¡s importantes para eso son estas:

- `load_nifti_volume(path)`
  - Carga un volumen NIfTI y retorna `volume`, `affine` y `header`.
  - Se usa para leer volÃºmenes como `unwrapped_seguetotalphase.nii` y `mask4.nii`.

- `create_default_filters(ndim=3)`
  - Construye el conjunto de funciones de escalamiento para 3D.
  - Entrega filtros como `Promedio 3x3x3`, `Gauss sigma=1`, `Gauss sigma=2`, `Binomial [1,2,1]` y `Esferico r=2`.

- `build_laplacian_predictive(x, scaling_fn, levels=5)`
  - Hace la descomposiciÃ³n multiescala.
  - Retorna:
    - `lap`: lista de capas laplacianas de detalle;
    - `residual`: componente mÃ¡s suave al final de la pirÃ¡mide;
    - `gauss`: niveles gaussianos intermedios.
  - Esta es la funciÃ³n principal de descomposiciÃ³n para la Parte 3.

- `reconstruct_laplacian(lap, residual)`
  - Reconstruye el volumen completo a partir de las capas de detalle y el residual.
  - Sirve para verificar que la extensiÃ³n a 3D sea correcta y que el error de reconstrucciÃ³n sea pequeÃ±o.

- `reconstruct_selected_layers(lap, residual, active_levels=None, include_residual=True)`
  - Reconstruye solo ciertas partes de la pirÃ¡mide.
  - Es Ãºtil para analizar por separado:
    - solo el residual;
    - solo los detalles;
    - el detalle fino `L0`;
    - los detalles `L1..fin`.

- `masked_rmse(a, b, mask=None)`
  - Calcula RMSE opcionalmente restringido a una mÃ¡scara.
  - En la Parte 3 es Ãºtil para cuantificar el error de reconstrucciÃ³n dentro del objeto y no fuera de Ã©l.

- `laplacian_energy(x, mask=None)`
  - Calcula la energÃ­a del Laplaciano de un volumen o imagen.
  - Sirve como indicador prÃ¡ctico de quÃ© tan â€œsuaveâ€ u â€œarmÃ³nicoâ€ es un residual.
  - En la Parte 3 ayuda a comparar filtros y ver si el residual se acerca a un comportamiento mÃ¡s armÃ³nico.

- `show_volume_slices(volume, title, indices=None, cmap="gray", symmetric=False)`
  - Muestra cortes axial, coronal y sagital de un volumen 3D.
  - Se usa para inspeccionar visualmente el campo total, el residual y las reconstrucciones parciales.

## Flujo tÃ­pico para la Parte 3

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
print("RMSE reconstrucciÃ³n:", masked_rmse(total_phase, rec, mask_bool))
print("EnergÃ­a laplaciana residual:", laplacian_energy(residual))

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
