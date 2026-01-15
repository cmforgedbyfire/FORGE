from __future__ import annotations

import json
import os
import subprocess
import zipfile
import datetime
from pathlib import Path
from typing import Iterable, Tuple


AUDIT_LOG_NAME = "ship_studio_audit.jsonl"


def _has_any(root: Path, names: Iterable[str]) -> bool:
    return any((root / name).exists() for name in names)


def _has_ext(root: Path, exts: Iterable[str], max_files: int = 200) -> bool:
    exts = {e.lower() for e in exts}
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {"__pycache__", ".git", ".venv", "venv", "node_modules"}]
        for name in filenames:
            count += 1
            if count > max_files:
                return False
            if Path(name).suffix.lower() in exts:
                return True
    return False


def detect_project_type(project_path: str) -> str:
    """
    Detect a basic project type using common file markers.
    Returns a single string type.
    """
    root = Path(project_path)
    if not root.exists():
        return "unknown"

    has_python = _has_any(
        root,
        ["pyproject.toml", "setup.py", "requirements.txt", "Pipfile", "poetry.lock"],
    ) or _has_ext(root, [".py"])
    has_node = _has_any(
        root,
        ["package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "tsconfig.json"],
    ) or _has_ext(root, [".js", ".jsx", ".ts", ".tsx"])

    has_dotnet = _has_ext(root, [".csproj", ".fsproj", ".vbproj", ".sln"]) or _has_any(root, ["global.json"])
    has_go = _has_any(root, ["go.mod"])
    has_rust = _has_any(root, ["Cargo.toml"])
    has_java = _has_any(root, ["pom.xml", "build.gradle", "build.gradle.kts"])
    has_ruby = _has_any(root, ["Gemfile"])
    has_php = _has_any(root, ["composer.json"])
    has_cpp = _has_any(root, ["CMakeLists.txt", "Makefile"]) or _has_ext(root, [".c", ".cc", ".cpp", ".h", ".hpp"])

    if has_python and has_node:
        return "python+node"
    if has_python:
        return "python"
    if has_node:
        return "node"
    if has_dotnet:
        return "dotnet"
    if has_go:
        return "go"
    if has_rust:
        return "rust"
    if has_java:
        return "java"
    if has_ruby:
        return "ruby"
    if has_php:
        return "php"
    if has_cpp:
        return "cpp"
    return "unknown"


def _run_command(cmd: list[str], cwd: Path) -> Tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as e:
        return 1, f"Failed to run command: {cmd}\nError: {e}"
    output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, output.strip()


def _save_build_log(root: Path, content: str) -> Path:
    log_path = root / "ship_studio_build_log.txt"
    log_path.write_text(content, encoding="utf-8")
    return log_path


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


def run_build(project_path: str, project_type: str | None = None) -> str:
    """
    Run a simple build based on project type and return a summary.
    """
    root = Path(project_path).resolve()
    if not root.exists():
        return f"Project path not found: {project_path}"

    ptype = project_type or detect_project_type(str(root))
    if ptype == "python":
        if (root / "pyproject.toml").exists():
            cmd = ["python", "-m", "build"]
        elif (root / "setup.py").exists():
            cmd = ["python", "setup.py", "sdist", "bdist_wheel"]
        else:
            return "No Python build configuration found."
    elif ptype == "node":
        if not (root / "package.json").exists():
            return "package.json not found."
        try:
            data = json.loads((root / "package.json").read_text(encoding="utf-8"))
        except Exception:
            data = {}
        scripts = data.get("scripts", {}) if isinstance(data, dict) else {}
        if "build" not in scripts:
            return "No npm build script found in package.json."
        cmd = ["npm", "run", "build"]
    elif ptype == "python+node":
        return "Mixed Python + Node project. Run the build from the relevant tab or module."
    else:
        return f"Build not supported for project type: {ptype}."

    audit_path = _append_audit(root, "build_start", {"cmd": cmd, "project_type": ptype})
    code, output = _run_command(cmd, root)
    log_path = _save_build_log(root, output or "No output.")
    _append_audit(
        root,
        "build_complete",
        {"exit_code": code, "log_path": str(log_path)},
    )
    if code == 0:
        return f"Build succeeded.\nLog: {log_path}\nAudit: {audit_path}"
    return f"Build failed (exit {code}).\nLog: {log_path}\nAudit: {audit_path}\n\nOutput:\n{output}"


def create_package(project_path: str, output_path: str, project_type: str | None = None) -> str:
    """
    Create a zip of the project (excluding common junk) at output_path.
    """
    root = Path(project_path).resolve()
    out = Path(output_path).resolve()
    if not root.exists():
        return f"Project path not found: {project_path}"
    if not out.exists():
        out.mkdir(parents=True, exist_ok=True)

    audit_path = _append_audit(root, "package_start", {"output_path": str(out), "project_type": project_type})
    archive_path = out / f"{root.name}_package.zip"
    skip_dirs = {".git", "__pycache__", ".mypy_cache", ".pytest_cache", "venv", ".venv", "node_modules"}

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
            for name in filenames:
                full_path = Path(dirpath) / name
                rel = full_path.relative_to(root)
                zf.write(full_path, rel.as_posix())

    if project_type:
        return f"Package created: {archive_path}\nProject type: {project_type}\nAudit: {audit_path}"
    return f"Package created: {archive_path}\nAudit: {audit_path}"
