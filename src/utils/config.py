from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_yaml(relative_path: str) -> dict:
    with (PROJECT_ROOT / relative_path).open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_params() -> dict:
    return load_yaml("params.yaml")


def project_path(relative_path: str) -> Path:
    return PROJECT_ROOT / relative_path

