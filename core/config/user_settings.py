from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict

from core.config.settings import (
    DEFAULT_LLM_BASE_URL,
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_TEMPERATURE,
    DEFAULT_AI_ENABLED,
)


SETTINGS_DIR = Path.home() / ".ship_studio"
SETTINGS_PATH = SETTINGS_DIR / "settings.json"


@dataclass
class LLMSettings:
    base_url: str = DEFAULT_LLM_BASE_URL
    model: str = DEFAULT_LLM_MODEL
    temperature: float = DEFAULT_LLM_TEMPERATURE
    enabled: bool = DEFAULT_AI_ENABLED


def _coerce_llm_settings(raw: Dict[str, Any]) -> LLMSettings:
    return LLMSettings(
        base_url=str(raw.get("base_url", DEFAULT_LLM_BASE_URL)),
        model=str(raw.get("model", DEFAULT_LLM_MODEL)),
        temperature=float(raw.get("temperature", DEFAULT_LLM_TEMPERATURE)),
        enabled=bool(raw.get("enabled", DEFAULT_AI_ENABLED)),
    )


def load_llm_settings() -> LLMSettings:
    if not SETTINGS_PATH.exists():
        return LLMSettings()
    try:
        raw = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return LLMSettings()
    if not isinstance(raw, dict):
        return LLMSettings()
    return _coerce_llm_settings(raw.get("llm", raw))


def save_llm_settings(settings: LLMSettings) -> None:
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"llm": asdict(settings)}
    SETTINGS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
