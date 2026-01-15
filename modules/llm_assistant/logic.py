import os
import json
import threading
import queue
import requests
from pathlib import Path
from typing import Callable, Optional, Dict, Any, List, Iterable

from core.config.user_settings import LLMSettings, load_llm_settings, save_llm_settings

DEFAULT_TIMEOUT_SECONDS = 15


# ----------------------------
# Internal helpers
# ----------------------------

def _llm_stream_request(
    model: str,
    prompt: str,
    system: Optional[str] = None,
    temperature: float = 0.2,
    base_url: Optional[str] = None,
) -> Iterable[str]:
    """
    Call a generic LLM endpoint with streaming enabled and yield chunks of text as they arrive.
    Compatible with Ollama, OpenAI-compatible APIs, and custom endpoints.
    """
    if base_url is None:
        base_url = load_llm_settings().base_url
    url = f"{base_url}/api/generate"
    payload: Dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": temperature,
        },
    }
    if system:
        payload["system"] = system

    with requests.post(url, json=payload, stream=True, timeout=DEFAULT_TIMEOUT_SECONDS) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "error" in data:
                raise RuntimeError(data["error"])
            token = data.get("response", "")
            if token:
                yield token
            if data.get("done"):
                break


def _walk_project_files(root: Path, exts: Optional[List[str]] = None, max_files: int = 200) -> List[Path]:
    """
    Walk a project directory and collect files matching extensions.
    Defaults to Python + common text docs.
    """
    if exts is None:
        exts = [".py", ".md", ".txt", ".toml", ".yaml", ".yml", ".json"]

    found: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # skip some noisy dirs
        skip_dirs = {".git", "__pycache__", ".mypy_cache", ".pytest_cache", "venv", ".venv", "node_modules"}
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for name in filenames:
            p = Path(dirpath) / name
            if p.suffix.lower() in exts:
                found.append(p)
                if len(found) >= max_files:
                    return found
    return found


def _summarize_python_file(path: Path, max_lines: int = 400) -> Dict[str, Any]:
    """
    Very lightweight summary: grab the first N lines and treat them as context.
    We avoid real parsing to keep things simple and robust.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"path": str(path), "kind": "python", "preview": ""}

    lines = text.splitlines()
    head = "\n".join(lines[:max_lines])
    return {
        "path": str(path),
        "kind": "python",
        "preview": head,
    }


def _build_project_map(root: Path, max_files: int = 50) -> Dict[str, Any]:
    """
    Build a compact 'project map' suitable for sending to an LLM.
    We include a list of files and a small preview of key files.
    """
    root = root.resolve()
    files = _walk_project_files(root, max_files=max_files)
    entries: List[Dict[str, Any]] = []

    for p in files:
        rel = str(p.relative_to(root))
        if p.suffix == ".py":
            summary = _summarize_python_file(p, max_lines=200)
            summary["relative_path"] = rel
            entries.append(summary)
        else:
            entries.append({
                "path": str(p),
                "relative_path": rel,
                "kind": p.suffix.lstrip(".") or "file",
            })

    return {
        "root": str(root),
        "entries": entries,
    }


# ----------------------------
# Public API for UI
# ----------------------------

def stream_llm_response(
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    base_url: Optional[str],
    on_chunk: Callable[[str], None],
    on_done: Callable[[Optional[str]], None],
    on_error: Callable[[str], None],
) -> threading.Thread:
    """
    Start a background thread that streams a response from Ollama and calls
    UI callbacks.

    - on_chunk(text) is called as new text arrives
    - on_done(final_text) is called once at the end
    - on_error(message) is called on failure

    Returns the Thread so the caller can manage or join if needed.
    """
    def worker():
        try:
            full_text_parts: List[str] = []
            for chunk in _llm_stream_request(
                model=model,
                prompt=user_prompt,
                system=system_prompt,
                temperature=temperature,
                base_url=base_url,
            ):
                full_text_parts.append(chunk)
                on_chunk(chunk)
            final = "".join(full_text_parts)
            on_done(final)
        except Exception as e:
            on_error(str(e))

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return t


def check_llm_available(base_url: Optional[str] = None) -> bool:
    settings = load_llm_settings()
    if not settings.enabled:
        return False
    if base_url is None:
        base_url = settings.base_url
    if not base_url:
        return False
    try:
        resp = requests.get(f"{base_url}/api/tags", timeout=DEFAULT_TIMEOUT_SECONDS)
        return resp.status_code == 200
    except Exception:
        return False


def load_local_llm_settings() -> LLMSettings:
    return load_llm_settings()


def save_local_llm_settings(settings: LLMSettings) -> None:
    save_llm_settings(settings)


def is_ai_enabled() -> bool:
    return load_llm_settings().enabled


def build_preset_prompt(
    preset_key: str,
    project_map_json: Optional[str],
    raw_input: str,
) -> Dict[str, str]:
    """
    Given a preset key and optional project map, build system + user prompts.
    Returns dict with 'system' and 'user' strings.
    """
    base_system = (
        "You are a concise, practical assistant helping a developer ship software.\n"
        "You specialize in:\n"
        "- clear documentation\n"
        "- product descriptions\n"
        "- feature outlines\n"
        "- privacy and data-handling summaries\n"
        "- changelogs and how-to guides.\n"
        "You respond in clean Markdown unless instructed otherwise."
    )

    if preset_key == "product_description":
        system = base_system + (
            "\n\nTask: Given a description of an app or project, write:\n"
            "- A 1-2 sentence tagline\n"
            "- A short app store style description\n"
            "- A longer website-ready description\n"
            "Use a friendly, professional tone."
        )
        user = raw_input

    elif preset_key == "readme_overview":
        system = base_system + (
            "\n\nTask: Draft a README-style overview for this project.\n"
            "Include:\n"
            "- Project description\n"
            "- Key features\n"
            "- Basic installation steps\n"
            "- Basic usage examples\n"
            "Do NOT invent impossible features; infer cautiously from the info given."
        )
        if project_map_json:
            user = f"Here is a project map:\n```json\n{project_map_json}\n```\n\nAdditional notes:\n{raw_input}"
        else:
            user = raw_input

    elif preset_key == "function_outline":
        system = base_system + (
            "\n\nTask: Analyze the provided project map and produce:\n"
            "- A high-level architecture summary\n"
            "- A module-by-module outline\n"
            "- Key classes and functions with 1-2 line descriptions\n"
            "Write it as if for internal technical documentation."
        )
        if project_map_json:
            user = f"Project map:\n```json\n{project_map_json}\n```\n\nOptional notes:\n{raw_input}"
        else:
            user = raw_input or "The project map was not provided."

    elif preset_key == "privacy_statement":
        system = base_system + (
            "\n\nTask: Draft a privacy and data-handling section for this app.\n"
            "Assume the developer does NOT want to collect unnecessary data.\n"
            "Explain in simple language:\n"
            "- What data is processed (if known)\n"
            "- What is NOT stored\n"
            "- How users' data is protected\n"
            "- Any relevant configuration notes.\n"
            "Keep it under 300 words. Be conservative; if details are missing, "
            "clearly say they must be defined by the developer."
        )
        user = raw_input

    elif preset_key == "changelog_entry":
        system = base_system + (
            "\n\nTask: Turn the following notes into a clean changelog entry.\n"
            "Use a version header placeholder (e.g. `## [Unreleased]`) and bullet points.\n"
            "Group items into Added / Changed / Fixed / Removed when possible."
        )
        user = raw_input

    elif preset_key == "how_to_guide":
        system = base_system + (
            "\n\nTask: Write a HOW-TO guide for a user of this app.\n"
            "Structure it with headings and numbered steps.\n"
            "Assume the user is somewhat technical but not a developer.\n"
            "Focus on one primary flow (e.g. \"How to capture and save screenshots\")."
        )
        if project_map_json:
            user = (
                f"Project map:\n```json\n{project_map_json}\n```\n\n"
                f"Focus of this guide:\n{raw_input}"
            )
        else:
            user = raw_input

    elif preset_key == "website_copy":
        system = base_system + (
            "\n\nTask: Write website copy for a landing page of this tool.\n"
            "Include sections:\n"
            "- Hero (headline + subheadline)\n"
            "- Key benefits (bullets)\n"
            "- Features (short list)\n"
            "- Who it's for\n"
            "- Call to action\n"
            "Tone: calm, confident, not salesy. Keep it under 200 words."
        )
        user = raw_input

    elif preset_key == "printable_pdf":
        system = base_system + (
            "\n\nTask: Produce content suitable for a printable 1-2 page PDF overview.\n"
            "Organize:\n"
            "- Title\n"
            "- Short summary\n"
            "- Key features\n"
            "- How it works\n"
            "- Contact or links placeholder.\n"
            "Do NOT include page numbers or printer marks."
        )
        if project_map_json:
            user = f"Project map:\n```json\n{project_map_json}\n```\n\nExtra notes:\n{raw_input}"
        else:
            user = raw_input

    else:
        # Fallback: generic chat
        system = base_system + "\n\nTask: Answer the user's request directly."
        user = raw_input

    return {"system": system, "user": user}


def build_project_map_for_path(path_str: str, max_files: int = 50) -> str:
    """
    Given a path string, build and return a JSON string representing the project map.
    """
    root = Path(path_str)
    if not root.exists():
        raise FileNotFoundError(f"Path does not exist: {path_str}")
    project_map = _build_project_map(root, max_files=max_files)
    return json.dumps(project_map, indent=2)
