from __future__ import annotations

from pathlib import Path
import zipfile

import nibabel as nib
import numpy as np
from PIL import Image

from .task2_utils import crop_to_mask, ensure_dir


def ensure_extracted(zip_path: str | Path, output_dir: str | Path) -> Path:
    zip_path = Path(zip_path)
    output_dir = ensure_dir(output_dir)
    if zip_path.exists() and not any(output_dir.iterdir()):
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(output_dir)
    return output_dir


def load_gray_image(path: str | Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("L"), dtype=float) / 255.0


def load_task2_astronomy_images(data_dir: str | Path) -> dict[str, np.ndarray]:
    data_dir = Path(data_dir)
    return {
        "Moon": load_gray_image(data_dir / "Moon.png"),
        "DeepSky": load_gray_image(data_dir / "EX3_01.png"),
    }


def load_task2_mri_data(data_dir: str | Path) -> dict[str, object]:
    data_dir = Path(data_dir)
    mri_files = {
        "gt": data_dir / "gt.nii",
        "mask": data_dir / "mask.nii",
        "reconNDI1": data_dir / "reconNDI1.nii",
        "reconNDI2": data_dir / "reconNDI2.nii",
        "recontv1": data_dir / "recontv1.nii",
        "recontv2": data_dir / "recontv2.nii",
        "recontv3": data_dir / "recontv3.nii",
    }

    mask_full = nib.load(str(mri_files["mask"])).get_fdata() > 0
    gt_full = nib.load(str(mri_files["gt"])).get_fdata()
    recon_full = {
        name: nib.load(str(path)).get_fdata()
        for name, path in mri_files.items()
        if name not in {"gt", "mask"}
    }
    gt, mask, bbox_slices = crop_to_mask(gt_full, mask_full)
    recon = {name: vol[bbox_slices] for name, vol in recon_full.items()}
    return {
        "gt_full": gt_full,
        "mask_full": mask_full,
        "gt": gt,
        "mask": mask,
        "bbox_slices": bbox_slices,
        "recon_volumes_full": recon_full,
        "recon_volumes": recon,
    }
