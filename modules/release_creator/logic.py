from __future__ import annotations

import json
import os
import shutil
import datetime
from pathlib import Path
from typing import Callable, List, Dict

from core.config.settings import DEFAULT_SCREENSHOT_DIR_NAME
from core.utils.helpers import ensure_dir
from modules.build_packager import logic as build_logic
from modules.docs_generator import logic as docs_logic
from modules.llm_assistant import logic as llm_logic


DOC_FILENAMES = [
    "README.md",
    "README.txt",
    "CHANGELOG.md",
    "CHANGELOG.txt",
    "PRIVACY.md",
    "PRIVACY.txt",
    "LICENSE",
    "LICENSE.txt",
    "ARCHITECTURE.md",
    "FEATURES.md",
    "OVERVIEW.md",
]

BUILD_DIR_NAMES = ["dist", "build", "out"]
BUILD_LOG_NAME = "ship_studio_build_log.txt"
AUDIT_LOG_NAME = "audit_log.jsonl"


def _timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def _copy_file(src: Path, dst_dir: Path) -> str | None:
    if not src.exists() or not src.is_file():
        return None
    ensure_dir(str(dst_dir))
    dst = dst_dir / src.name
    shutil.copy2(src, dst)
    return str(dst)


def _copy_tree(src: Path, dst: Path) -> int:
    if not src.exists() or not src.is_dir():
        return 0
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", ".git"))
    count = 0
    for _, _, files in os.walk(dst):
        count += len(files)
    return count


def create_release_structure(
    project_path: str,
    target_path: str,
    release_name: str | None = None,
    version: str | None = None,
    include_docs: bool = True,
    include_screenshots: bool = True,
    include_build: bool = True,
    on_status: Callable[[str], None] | None = None,
) -> str:
    """
    Create a release folder with docs, screenshots, and build outputs.
    """
    project_root = Path(project_path).resolve()
    target_root = Path(target_path).resolve()

    if not project_root.exists() or not project_root.is_dir():
        return f"Project path not found: {project_path}"

    ensure_dir(str(target_root))

    base_name = release_name.strip() if release_name else project_root.name
    version_suffix = f"_v{version.strip()}" if version else ""
    release_root = target_root / f"{base_name}{version_suffix}_release_{_timestamp()}"
    docs_dir = release_root / "docs"
    screenshots_dir = release_root / "screenshots"
    build_dir = release_root / "build"

    _append_audit(release_root, "release_created", {"release_root": str(release_root)})

    if include_docs:
        ensure_dir(str(docs_dir))
    if include_screenshots:
        ensure_dir(str(screenshots_dir))
    if include_build:
        ensure_dir(str(build_dir))

    copied_docs: List[str] = []
    if include_docs:
        if on_status:
            on_status("Copying docs...")
        for name in DOC_FILENAMES:
            path = project_root / name
            copied = _copy_file(path, docs_dir)
            if copied:
                copied_docs.append(copied)
        _append_audit(release_root, "docs_copied", {"count": len(copied_docs)})

    screenshots_count = 0
    if include_screenshots:
        if on_status:
            on_status("Copying screenshots...")
        screenshots_src = project_root / DEFAULT_SCREENSHOT_DIR_NAME
        screenshots_count = _copy_tree(screenshots_src, screenshots_dir)
        _append_audit(release_root, "screenshots_copied", {"count": screenshots_count})

    build_copied: Dict[str, int] = {}
    build_log_path = None
    if include_build:
        if on_status:
            on_status("Copying build outputs...")
        for name in BUILD_DIR_NAMES:
            src = project_root / name
            if src.exists() and src.is_dir():
                dst = build_dir / name
                build_copied[name] = _copy_tree(src, dst)
        build_log_src = project_root / BUILD_LOG_NAME
        if build_log_src.exists() and build_log_src.is_file():
            build_log_dst = build_dir / BUILD_LOG_NAME
            ensure_dir(str(build_dir))
            shutil.copy2(build_log_src, build_log_dst)
            build_log_path = str(build_log_dst)
        _append_audit(
            release_root,
            "build_outputs_copied",
            {"dirs": list(build_copied.keys()), "log_copied": bool(build_log_path)},
        )

    manifest = {
        "project_root": str(project_root),
        "release_root": str(release_root),
        "options": {
            "include_docs": include_docs,
            "include_screenshots": include_screenshots,
            "include_build": include_build,
        },
        "docs_copied": copied_docs,
        "screenshots_copied": screenshots_count,
        "build_copied": build_copied,
        "build_log": build_log_path,
        "llm_available": None,
        "docs_generated": [],
        "audit_log": str(release_root / AUDIT_LOG_NAME),
    }
    manifest_path = release_root / "manifest.json"
    _write_json_atomic(manifest_path, manifest)
    _append_audit(release_root, "manifest_written", {"path": str(manifest_path)})

    summary_lines = [
        f"Release created: {release_root}",
        f"Docs copied: {len(copied_docs)}" if include_docs else "Docs copied: skipped",
        f"Screenshots copied: {screenshots_count}" if include_screenshots else "Screenshots copied: skipped",
        f"Build folders copied: {len(build_copied)}" if include_build else "Build folders copied: skipped",
        f"Manifest: {manifest_path}",
    ]
    return "\n".join(summary_lines)


def _write_doc(path: Path, content: str) -> None:
    ensure_dir(str(path.parent))
    path.write_text(content.strip() + "\n", encoding="utf-8")

def _write_json_atomic(path: Path, payload: dict) -> None:
    ensure_dir(str(path.parent))
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    os.replace(tmp_path, path)

def _append_audit(release_root: Path, event: str, data: dict) -> None:
    ensure_dir(str(release_root))
    entry = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "event": event,
        "data": data,
    }
    log_path = release_root / AUDIT_LOG_NAME
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def _basic_doc_templates(project_name: str) -> dict[str, str]:
    return {
        "README.md": (
            f"# {project_name}\n\n"
            "## Overview\n\n"
            "Add a short description of the project.\n\n"
            "## Features\n\n"
            "- Feature 1\n"
            "- Feature 2\n\n"
            "## Installation\n\n"
            "Add install steps here.\n\n"
            "## Usage\n\n"
            "Add usage examples here.\n"
        ),
        "CHANGELOG.md": (
            "## [Unreleased]\n\n"
            "### Added\n"
            "- \n\n"
            "### Changed\n"
            "- \n\n"
            "### Fixed\n"
            "- \n\n"
            "### Removed\n"
            "- \n"
        ),
        "PRIVACY.md": (
            "# Privacy\n\n"
            "This app runs locally and does not transmit data by default.\n\n"
            "## Data Processed\n"
            "- Describe any data the app reads or writes.\n\n"
            "## Data Stored\n"
            "- List any files or settings stored locally.\n"
        ),
        "WEBSITE_COPY.md": (
            "# Website Copy\n\n"
            "## Hero\n"
            "Headline goes here.\n\n"
            "## Subheadline\n"
            "Short product pitch goes here.\n\n"
            "## Features\n"
            "- Feature 1\n"
            "- Feature 2\n\n"
            "## Call to Action\n"
            "Add a clear CTA here.\n"
        ),
    }


def _run_llm_summary(system_prompt: str, user_prompt: str) -> str:
    chunks = []

    def on_chunk(text: str):
        chunks.append(text)

    def on_done(final_text: str):
        pass

    def on_error(message: str):
        chunks.append(f"\nError: {message}")

    settings = llm_logic.load_local_llm_settings()
    llm_logic.stream_llm_response(
        model=settings.model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=settings.temperature,
        base_url=settings.base_url,
        on_chunk=on_chunk,
        on_done=on_done,
        on_error=on_error,
    )

    return "".join(chunks).strip()


def generate_project_summary(project_path: str) -> str:
    settings = llm_logic.load_local_llm_settings()
    if not settings.enabled:
        return "AI disabled."
    if not llm_logic.check_llm_available(settings.base_url):
        return "LLM unavailable."

    try:
        project_map = llm_logic.build_project_map_for_path(project_path, max_files=30)
    except Exception as e:
        return f"Summary failed: {e}"

    system_prompt = (
        "You are a concise product analyst. Summarize the project in 3-4 sentences. "
        "Mention what it does, who it's for, and a standout feature if visible."
    )
    user_prompt = f"Project map:\n```json\n{project_map}\n```\n\nWrite the summary."
    return _run_llm_summary(system_prompt, user_prompt)

def preview_release_contents(project_path: str) -> dict:
    project_root = Path(project_path).resolve()
    if not project_root.exists():
        return {"error": f"Project path not found: {project_path}"}

    project_type = build_logic.detect_project_type(str(project_root))

    docs_found = []
    for name in DOC_FILENAMES:
        path = project_root / name
        if path.exists():
            docs_found.append(str(path))

    docs_dir = project_root / "docs"
    docs_dir_files = []
    if docs_dir.exists() and docs_dir.is_dir():
        for _, _, files in os.walk(docs_dir):
            for name in files:
                if name.lower().endswith((".md", ".txt")):
                    docs_dir_files.append(str(docs_dir / name))

    screenshot_folders = {}
    image_exts = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    for dirpath, dirnames, filenames in os.walk(project_root):
        dirnames[:] = [d for d in dirnames if d not in {"__pycache__", ".git", ".venv", "venv", "node_modules"}]
        folder = Path(dirpath)
        if folder.name.lower() in {"screenshots", "screen", "images", "assets", "img"}:
            count = sum(1 for f in filenames if Path(f).suffix.lower() in image_exts)
            if count:
                screenshot_folders[str(folder)] = count

    screenshots_count = sum(screenshot_folders.values())

    build_dirs = []
    build_counts = {}
    for name in BUILD_DIR_NAMES:
        src = project_root / name
        if src.exists() and src.is_dir():
            build_dirs.append(str(src))
            count = 0
            for _, _, files in os.walk(src):
                count += len(files)
            build_counts[name] = count

    ext_counts = {}
    scanned = 0
    max_files = 300
    for dirpath, dirnames, filenames in os.walk(project_root):
        dirnames[:] = [d for d in dirnames if d not in {"__pycache__", ".git", ".venv", "venv", "node_modules"}]
        for name in filenames:
            scanned += 1
            if scanned > max_files:
                break
            ext = Path(name).suffix.lower()
            if not ext:
                continue
            ext_counts[ext] = ext_counts.get(ext, 0) + 1
        if scanned > max_files:
            break

    return {
        "project_root": str(project_root),
        "project_type": project_type,
        "docs_found": docs_found,
        "docs_dir_files": docs_dir_files,
        "screenshots_count": screenshots_count,
        "screenshot_folders": screenshot_folders,
        "build_dirs": build_dirs,
        "build_counts": build_counts,
        "ext_counts": ext_counts,
    }


def create_one_click_ship(
    project_path: str,
    target_path: str,
    release_name: str | None = None,
    version: str | None = None,
    include_docs: bool = True,
    include_screenshots: bool = True,
    include_build: bool = True,
    generate_docs: bool = True,
    on_status: Callable[[str], None] | None = None,
) -> str:
    """
    One-click ship: generate docs (optional) and build a release bundle.
    """
    project_root = Path(project_path).resolve()
    if on_status:
        on_status("Creating release structure...")
    base_summary = create_release_structure(
        project_path=project_path,
        target_path=target_path,
        release_name=release_name,
        version=version,
        include_docs=include_docs,
        include_screenshots=include_screenshots,
        include_build=include_build,
        on_status=on_status,
    )

    release_root_line = base_summary.splitlines()[0] if base_summary else ""
    release_root = None
    if release_root_line.startswith("Release created: "):
        release_root = Path(release_root_line.replace("Release created: ", "").strip())

    generated = {}
    llm_available = llm_logic.is_ai_enabled() and llm_logic.check_llm_available()
    if generate_docs and release_root and include_docs:
        if on_status:
            on_status("Generating docs...")
        docs_dir = release_root / "docs"
        ensure_dir(str(docs_dir))
        if llm_available:
            generated["README.md"] = docs_logic.generate_readme_stub(project_path)
            generated["CHANGELOG.md"] = docs_logic.generate_changelog_stub(project_path)
            generated["PRIVACY.md"] = docs_logic.generate_privacy_doc(project_path)
            generated["WEBSITE_COPY.md"] = docs_logic.generate_website_copy(project_path)
        else:
            if on_status:
                on_status("LLM unavailable; creating doc stubs...")
            generated = _basic_doc_templates(project_root.name)
        for name, content in generated.items():
            _write_doc(docs_dir / name, content)
        _append_audit(release_root, "docs_generated", {"files": list(generated.keys())})

    if release_root:
        if on_status:
            on_status("Updating manifest and report...")
        manifest_path = release_root / "manifest.json"
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except Exception:
                manifest = {}
        else:
            manifest = {}
        manifest["llm_available"] = llm_available
        manifest["docs_generated"] = list(generated.keys())
        _write_json_atomic(manifest_path, manifest)
        _append_audit(
            release_root,
            "manifest_updated",
            {"llm_available": llm_available, "docs_generated": len(generated)},
        )

        report_lines = [
            f"# Release Report",
            "",
            f"- Project: `{project_root.name}`",
            f"- Release folder: `{release_root}`",
            f"- LLM available: `{llm_available}`",
            f"- Docs generated: `{len(generated)}`",
            f"- Screenshots copied: `{manifest.get('screenshots_copied', 0)}`",
            f"- Build folders copied: `{len(manifest.get('build_copied', {}))}`",
        ]
        if manifest.get("build_log"):
            report_lines.append(f"- Build log: `{manifest.get('build_log')}`")
        report_path = release_root / "docs" / "RELEASE_REPORT.md"
        _write_doc(report_path, "\n".join(report_lines))
        _append_audit(release_root, "report_written", {"path": str(report_path)})

    if on_status:
        on_status("Done.")
    summary_lines = [base_summary]
    if generate_docs:
        summary_lines.append(f"LLM available: {llm_available}")
        summary_lines.append(f"Generated docs: {len(generated)}")
    else:
        summary_lines.append("Generated docs: skipped")
    return "\n".join(summary_lines)
