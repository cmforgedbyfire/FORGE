from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from modules.build_packager.logic import detect_project_type


SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
}


def _exists_any(root: Path, names: list[str]) -> bool:
    return any((root / name).exists() for name in names)


def _find_matching_dirs(root: Path, names: set[str], max_dirs: int = 200) -> list[str]:
    matches: list[str] = []
    scanned = 0
    for dirpath, dirnames, _filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        scanned += 1
        if scanned > max_dirs:
            break
        folder = Path(dirpath)
        if folder.name.lower() in names:
            matches.append(str(folder))
    return matches


def _find_files(root: Path, patterns: tuple[str, ...], max_files: int = 400) -> list[str]:
    matches: list[str] = []
    scanned = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            scanned += 1
            if scanned > max_files:
                return matches
            lower = name.lower()
            if any(lower.endswith(pattern) or lower == pattern for pattern in patterns):
                matches.append(str(Path(dirpath) / name))
    return matches


def _item(title: str, status: str, detail: str, weight: int, action: str) -> dict[str, Any]:
    return {
        "title": title,
        "status": status,
        "detail": detail,
        "weight": weight,
        "action": action,
    }


def audit_project(project_path: str) -> dict[str, Any]:
    root = Path(project_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        return {
            "ok": False,
            "error": f"Project folder not found: {project_path}",
            "score": 0,
            "items": [],
        }

    project_type = detect_project_type(str(root))
    docs = {
        "README": _exists_any(root, ["README.md", "README.txt"]),
        "CHANGELOG": _exists_any(root, ["CHANGELOG.md", "CHANGELOG.txt"]),
        "PRIVACY": _exists_any(root, ["PRIVACY.md", "PRIVACY.txt"]),
        "LICENSE": _exists_any(root, ["LICENSE", "LICENSE.txt", "LICENSE.md"]),
    }
    build_markers = _exists_any(
        root,
        [
            "pyproject.toml",
            "setup.py",
            "requirements.txt",
            "package.json",
            "Cargo.toml",
            "go.mod",
            "FORGE.spec",
        ],
    )
    source_files = _find_files(root, (".py", ".js", ".ts", ".html", ".csproj", ".sln"), max_files=150)
    screenshots = _find_matching_dirs(root, {"screenshots", "screen", "images", "img"})
    icons = _find_files(root, (".ico", ".png"), max_files=250)
    installers = _find_files(root, (".iss", ".nsi", ".wxs"), max_files=250)
    release_outputs = [str(root / name) for name in ("dist", "build", "releases") if (root / name).exists()]
    stale_shipstudio = _find_files(root, ("shipstudio.exe", "shipstudio_v1.0.0.exe", "ship_studio.iss"), max_files=500)

    items = [
        _item(
            "Project type detected",
            "pass" if project_type != "unknown" else "warn",
            project_type if project_type != "unknown" else "Could not identify a known project type.",
            10,
            "build",
        ),
        _item(
            "Runnable or packageable source",
            "pass" if build_markers or source_files else "fail",
            "Build markers or source files found." if build_markers or source_files else "No obvious source or build files found.",
            15,
            "build",
        ),
        _item(
            "README",
            "pass" if docs["README"] else "fail",
            "Found." if docs["README"] else "Missing public overview and usage notes.",
            12,
            "docs",
        ),
        _item(
            "License",
            "pass" if docs["LICENSE"] else "fail",
            "Found." if docs["LICENSE"] else "Missing license file.",
            10,
            "docs",
        ),
        _item(
            "Changelog",
            "pass" if docs["CHANGELOG"] else "warn",
            "Found." if docs["CHANGELOG"] else "Missing change history.",
            6,
            "docs",
        ),
        _item(
            "Privacy note",
            "pass" if docs["PRIVACY"] else "warn",
            "Found." if docs["PRIVACY"] else "Missing simple privacy statement.",
            6,
            "docs",
        ),
        _item(
            "Screenshots or visuals",
            "pass" if screenshots or icons else "warn",
            f"{len(screenshots)} screenshot folders, {len(icons)} image/icon files." if screenshots or icons else "No screenshots or visual assets found.",
            8,
            "screenshots",
        ),
        _item(
            "Build or release output",
            "pass" if release_outputs else "warn",
            ", ".join(Path(p).name for p in release_outputs) if release_outputs else "No build/dist/release folder found yet.",
            10,
            "release",
        ),
        _item(
            "Installer script",
            "pass" if installers else "warn",
            f"{len(installers)} installer script(s) found." if installers else "No installer script found.",
            5,
            "release",
        ),
        _item(
            "Retired app artifacts",
            "pass" if not stale_shipstudio else "warn",
            "None found." if not stale_shipstudio else f"{len(stale_shipstudio)} stale artifact(s) found.",
            8,
            "cleanup",
        ),
    ]

    possible = sum(item["weight"] for item in items)
    earned = sum(item["weight"] for item in items if item["status"] == "pass")
    earned += sum(item["weight"] * 0.4 for item in items if item["status"] == "warn")
    score = round((earned / possible) * 100) if possible else 0

    return {
        "ok": True,
        "project_root": str(root),
        "project_type": project_type,
        "score": score,
        "items": items,
        "counts": {
            "source_files_sampled": len(source_files),
            "screenshots_dirs": len(screenshots),
            "image_or_icon_files_sampled": len(icons),
            "installer_scripts": len(installers),
            "release_outputs": len(release_outputs),
            "stale_shipstudio_artifacts": len(stale_shipstudio),
        },
    }
