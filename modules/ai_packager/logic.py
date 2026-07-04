from __future__ import annotations

import datetime
import json
import os
import shutil
from pathlib import Path
from typing import Dict, List


AUDIT_LOG_NAME = "forge_audit.jsonl"
MODEL_EXTS = {".gguf", ".bin", ".pt", ".pth", ".safetensors", ".onnx"}
CONFIG_EXTS = {".json", ".yaml", ".yml", ".toml"}
SCRIPT_EXTS = {".py", ".sh", ".bat", ".ps1"}
SKIP_DIRS = {".git", "__pycache__", ".mypy_cache", ".pytest_cache", "venv", ".venv", "node_modules"}


def _timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def _scan_project(root: Path) -> Dict[str, List[Path]]:
    results: Dict[str, List[Path]] = {
        "models": [],
        "configs": [],
        "scripts": [],
    }
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            ext = path.suffix.lower()
            if ext in MODEL_EXTS:
                results["models"].append(path)
            elif ext in CONFIG_EXTS:
                results["configs"].append(path)
            elif ext in SCRIPT_EXTS:
                results["scripts"].append(path)
    return results


def _copy_preserve(root: Path, src: Path, dst_root: Path) -> Path:
    rel = src.relative_to(root)
    dst = dst_root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def _append_audit(root: Path, event: str, data: dict) -> Path:
    entry = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "event": event,
        "data": data,
    }
    log_path = root / AUDIT_LOG_NAME
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return log_path


def summarize_ai_project(project_path: str) -> str:
    """
    Inspect project for models, configs, and scripts.
    """
    root = Path(project_path).resolve()
    if not root.exists():
        return f"Project path not found: {project_path}"

    results = _scan_project(root)
    audit_path = _append_audit(
        root,
        "ai_summary",
        {
            "models": len(results["models"]),
            "configs": len(results["configs"]),
            "scripts": len(results["scripts"]),
        },
    )
    summary_lines = [
        f"Models found: {len(results['models'])}",
        f"Configs found: {len(results['configs'])}",
        f"Scripts found: {len(results['scripts'])}",
    ]

    if results["models"]:
        sample = ", ".join(p.name for p in results["models"][:5])
        summary_lines.append(f"Model samples: {sample}")
    if results["configs"]:
        sample = ", ".join(p.name for p in results["configs"][:5])
        summary_lines.append(f"Config samples: {sample}")
    if results["scripts"]:
        sample = ", ".join(p.name for p in results["scripts"][:5])
        summary_lines.append(f"Script samples: {sample}")

    summary_lines.append(f"Audit: {audit_path}")
    return "\n".join(summary_lines)


def create_ai_bundle(project_path: str, output_path: str) -> str:
    """
    Package models, configs, and scripts into a bundle folder with a manifest.
    """
    root = Path(project_path).resolve()
    out = Path(output_path).resolve()
    if not root.exists():
        return f"Project path not found: {project_path}"
    if not out.exists():
        out.mkdir(parents=True, exist_ok=True)

    bundle_root = out / f"{root.name}_ai_bundle_{_timestamp()}"
    models_dir = bundle_root / "models"
    configs_dir = bundle_root / "configs"
    scripts_dir = bundle_root / "scripts"

    models_dir.mkdir(parents=True, exist_ok=True)
    configs_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)

    results = _scan_project(root)
    audit_path = _append_audit(bundle_root, "ai_bundle_start", {"project_root": str(root)})

    copied = {
        "models": [],
        "configs": [],
        "scripts": [],
    }
    for path in results["models"]:
        copied["models"].append(str(_copy_preserve(root, path, models_dir)))
    for path in results["configs"]:
        copied["configs"].append(str(_copy_preserve(root, path, configs_dir)))
    for path in results["scripts"]:
        copied["scripts"].append(str(_copy_preserve(root, path, scripts_dir)))

    manifest = {
        "project_root": str(root),
        "bundle_root": str(bundle_root),
        "counts": {k: len(v) for k, v in copied.items()},
        "files": copied,
    }
    manifest_path = bundle_root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    _append_audit(
        bundle_root,
        "ai_bundle_complete",
        {"manifest": str(manifest_path), "counts": manifest["counts"]},
    )

    return (
        f"AI bundle created: {bundle_root}\n"
        f"Models: {len(copied['models'])}, "
        f"Configs: {len(copied['configs'])}, "
        f"Scripts: {len(copied['scripts'])}\n"
        f"Manifest: {manifest_path}\n"
        f"Audit: {audit_path}"
    )
