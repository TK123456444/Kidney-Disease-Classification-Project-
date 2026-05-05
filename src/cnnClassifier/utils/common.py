import os
import yaml
import json
import joblib
import base64
from pathlib import Path
from typing import Any

from ensure import ensure_annotations
from box import ConfigBox
from cnnClassifier import logger


# =========================
# YAML READER (FIXED)
# =========================
@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    path_to_yaml = Path(path_to_yaml)

    if not path_to_yaml.exists():
        raise FileNotFoundError(f"YAML file not found: {path_to_yaml}")

    try:
        with open(path_to_yaml, "r") as f:
            content = yaml.safe_load(f)

        if content is None:
            raise ValueError(f"YAML file is empty: {path_to_yaml}")

        logger.info(f"yaml file: {path_to_yaml} loaded successfully")

        return ConfigBox(content, convert=True)

    except Exception as e:
        raise e


# =========================
# DIRECTORY CREATION
# =========================
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


# =========================
# JSON SAVE
# =========================
@ensure_annotations
def save_json(path: Path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")


# =========================
# JSON LOAD
# =========================
@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    with open(path, "r") as f:
        content = json.load(f)

    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)


# =========================
# BINARY SAVE
# =========================
@ensure_annotations
def save_bin(data: Any, path: Path):
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


# =========================
# BINARY LOAD
# =========================
@ensure_annotations
def load_bin(path: Path) -> Any:
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data


# =========================
# FILE SIZE
# =========================
@ensure_annotations
def get_size(path: Path) -> str:
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"


# =========================
# IMAGE ENCODE / DECODE
# =========================
def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, "wb") as f:
        f.write(imgdata)


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())