"""
Documentation Generator Logic
Uses local LLM + project map to generate structured documentation.
Falls back to templates when AI is disabled.
"""

import os
import datetime
from pathlib import Path
from modules.llm_assistant import logic as llm_logic


# ---------------------------------------------------------
# Template helpers
# ---------------------------------------------------------

def _load_template(template_name: str) -> str:
    """Load a template file from core/templates/"""
    template_dir = Path(__file__).parent.parent.parent / "core" / "templates"
    template_path = template_dir / template_name
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return f"# {template_name.replace('.md', '')}\n\nTemplate not found.\n"


def _fill_template(template: str, **kwargs) -> str:
    """Replace placeholders in template with provided values"""
    result = template
    for key, value in kwargs.items():
        placeholder = f"{{{{{key}}}}}"
        result = result.replace(placeholder, str(value))
    return result


def _detect_project_info(project_path: str) -> dict:
    """Extract basic project information"""
    root = Path(project_path)
    project_name = root.name
    
    # Try to detect tech stack
    tech_stack = []
    if (root / "package.json").exists():
        tech_stack.append("Node.js")
    if (root / "requirements.txt").exists() or (root / "pyproject.toml").exists():
        tech_stack.append("Python")
    if (root / "Cargo.toml").exists():
        tech_stack.append("Rust")
    if (root / "go.mod").exists():
        tech_stack.append("Go")
    if (root / ".csproj").exists() or list(root.glob("*.csproj")):
        tech_stack.append(".NET")
    
    return {
        "PROJECT_NAME": project_name,
        "DESCRIPTION": "A software project",
        "TECH_STACK": ", ".join(tech_stack) if tech_stack else "To be determined",
        "VERSION": "1.0.0",
        "DATE": datetime.datetime.now().strftime("%Y-%m-%d"),
        "LICENSE": "See LICENSE file",
        "CONTACT": "Contact information here",
        "PROJECT_STRUCTURE": "See project files",
    }


# ---------------------------------------------------------
# Helper: run a prompt through your streaming LLM system
# ---------------------------------------------------------

def _run_llm(system_prompt: str, user_prompt: str, temperature: float = 0.2):
    chunks = []
    settings = llm_logic.load_local_llm_settings()

    if not settings.enabled:
        return None  # Return None to signal AI disabled
    if not llm_logic.check_llm_available(settings.base_url):
        return None  # Return None to signal LLM unavailable

    def on_chunk(text: str):
        chunks.append(text)

    def on_done(final_text: str):
        pass

    def on_error(message: str):
        chunks.append(f"\nError: {message}")

    llm_logic.stream_llm_response(
        model=settings.model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=temperature,
        base_url=settings.base_url,
        on_chunk=on_chunk,
        on_done=on_done,
        on_error=on_error,
    )

    return "".join(chunks)


# ---------------------------------------------------------
# README Generator
# ---------------------------------------------------------

def generate_readme_stub(project_path: str) -> str:
    """Generate README using AI or template fallback"""
    # Try AI first if enabled
    try:
        project_map = llm_logic.build_project_map_for_path(project_path, max_files=50)
    except Exception as e:
        # Fall back to template on error
        template = _load_template("README.md")
        info = _detect_project_info(project_path)
        return _fill_template(template, **info)

    system_prompt = (
        "You are a documentation assistant. Generate a clean, professional README.md "
        "based on the project structure. Include sections like Overview, Features, "
        "Installation, Usage, Tech Stack, and Contribution if appropriate."
    )

    user_prompt = (
        f"Project path: {project_path}\n\n"
        f"Project map:\n{project_map}\n\n"
        "Generate a complete README.md."
    )

    ai_result = _run_llm(system_prompt, user_prompt)
    
    # If AI failed or disabled, use template
    if ai_result is None:
        template = _load_template("README.md")
        info = _detect_project_info(project_path)
        return _fill_template(template, **info)
    
    return ai_result


# ---------------------------------------------------------
# Changelog Generator
# ---------------------------------------------------------

def generate_changelog_stub(project_path: str) -> str:
    """Generate CHANGELOG using AI or template fallback"""
    try:
        project_map = llm_logic.build_project_map_for_path(project_path, max_files=50)
    except Exception as e:
        template = _load_template("CHANGELOG.md")
        info = _detect_project_info(project_path)
        return _fill_template(template, **info)

    system_prompt = (
        "You are a release assistant. Generate a Markdown changelog entry using the "
        "Added / Changed / Fixed / Removed format. Keep it concise and developer-friendly."
    )

    user_prompt = (
        f"Project path: {project_path}\n\n"
        f"Project map:\n{project_map}\n\n"
        "Generate a changelog entry for the next version."
    )

    ai_result = _run_llm(system_prompt, user_prompt)
    
    if ai_result is None:
        template = _load_template("CHANGELOG.md")
        info = _detect_project_info(project_path)
        return _fill_template(template, **info)
    
    return ai_result


# ---------------------------------------------------------
# Architecture Summary
# ---------------------------------------------------------

def generate_architecture_doc(project_path: str) -> str:
    """Generate architecture doc using AI or template fallback"""
    try:
        project_map = llm_logic.build_project_map_for_path(project_path, max_files=100)
    except Exception as e:
        template = _load_template("ARCHITECTURE.md")
        info = _detect_project_info(project_path)
        return _fill_template(template, **info)

    system_prompt = (
        "You are a senior software architect. Generate a clear, structured architecture "
        "summary for the project. Include modules, responsibilities, data flow, "
        "important classes/functions, and any notable patterns."
    )

    user_prompt = (
        f"Project path: {project_path}\n\n"
        f"Project map:\n{project_map}\n\n"
        "Generate a full architecture.md summary."
    )

    ai_result = _run_llm(system_prompt, user_prompt)
    
    if ai_result is None:
        template = _load_template("ARCHITECTURE.md")
        info = _detect_project_info(project_path)
        return _fill_template(template, **info)
    
    return ai_result


# ---------------------------------------------------------
# Feature List
# ---------------------------------------------------------

def generate_feature_list(project_path: str) -> str:
    try:
        project_map = llm_logic.build_project_map_for_path(project_path, max_files=100)
    except Exception as e:
        return f"# Features\n\nFailed to analyze project: {e}"

    system_prompt = (
        "You are a product writer. Generate a clean, user-friendly feature list "
        "based on the project structure. Use bullet points and short descriptions."
    )

    user_prompt = (
        f"Project path: {project_path}\n\n"
        f"Project map:\n{project_map}\n\n"
        "Generate a feature list."
    )

    return _run_llm(system_prompt, user_prompt)


# ---------------------------------------------------------
# Privacy Statement
# ---------------------------------------------------------

def generate_privacy_doc(project_path: str) -> str:
    try:
        project_map = llm_logic.build_project_map_for_path(project_path, max_files=50)
    except Exception as e:
        return f"# Privacy\n\nFailed to analyze project: {e}"

    system_prompt = (
        "You are a privacy and compliance writer. Generate a simple, clear privacy "
        "statement describing what data the app processes, what it does NOT store, "
        "and how it respects user control. Keep it friendly and transparent. "
        "Limit to 250-300 words and avoid boilerplate."
    )

    user_prompt = (
        f"Project path: {project_path}\n\n"
        f"Project map:\n{project_map}\n\n"
        "Generate a privacy statement."
    )

    return _run_llm(system_prompt, user_prompt)


# ---------------------------------------------------------
# Website Copy
# ---------------------------------------------------------

def generate_website_copy(project_path: str) -> str:
    try:
        project_map = llm_logic.build_project_map_for_path(project_path, max_files=50)
    except Exception as e:
        return f"# Website Copy\n\nFailed to analyze project: {e}"

    system_prompt = (
        "You are a marketing writer. Generate website copy including a hero section, "
        "short pitch, feature highlights, and a call to action. Tone: confident, "
        "developer-friendly, trustworthy."
    )

    user_prompt = (
        f"Project path: {project_path}\n\n"
        f"Project map:\n{project_map}\n\n"
        "Generate website copy."
    )

    return _run_llm(system_prompt, user_prompt)


# ---------------------------------------------------------
# Printable Overview
# ---------------------------------------------------------

def generate_printable_overview(project_path: str) -> str:
    try:
        project_map = llm_logic.build_project_map_for_path(project_path, max_files=50)
    except Exception as e:
        return f"# Overview\n\nFailed to analyze project: {e}"

    system_prompt = (
        "You are a technical writer. Generate a printable overview suitable for PDF "
        "or handouts. Include title, summary, features, architecture highlights, and "
        "intended audience."
    )

    user_prompt = (
        f"Project path: {project_path}\n\n"
        f"Project map:\n{project_map}\n\n"
        "Generate a printable overview."
    )

    return _run_llm(system_prompt, user_prompt)
