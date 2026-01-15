# Changelog

All notable changes to Ship Studio will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-01-14 - "Ship Studio" 🚀

### Major Release - Production Ready

This release represents the complete Ship Studio v1.0.0 with comprehensive polish, modern UI, and production-ready features.

### Added
- ✨ **AI-Optional Architecture**: Full functionality without requiring AI/LLM
- ✨ **Template System**: Professional documentation templates with smart placeholders
  - README.md template with project detection
  - CHANGELOG.md template with semantic versioning
  - PRIVACY.md template for data handling policies
  - ARCHITECTURE.md template for technical documentation
- ✨ **AI Mode Indicator**: Real-time status bar showing AI enabled/disabled state
- ✨ **Generic LLM Support**: Configure any OpenAI-compatible endpoint
  - Support for Ollama (local)
  - Support for OpenAI API
  - Support for Anthropic (via proxy)
  - Support for custom endpoints
- ✨ **Project Auto-Detection**: Smart detection of tech stack (Python, Node.js, .NET, Go, Rust)
- ✨ **Comprehensive Documentation**: Complete README with installation, usage, and troubleshooting

### Changed
- 🔄 **Rebranded** from "Ship Studio" to "FORGE"
- 🔄 **Version Jump**: 0.1.0 → 1.0.0 (production-ready milestone)
- 🔄 **Settings Location**: Moved from `~/.ship_studio/` to `~/.forge/`
- 🔄 **App Title**: Now displays "FORGE - Release Engineering Toolkit v1.0.0"
- 🔄 **Executable Name**: `ShipStudio.exe` → `Forge.exe`
- 🔄 **Installer Name**: `ShipStudio_Setup.exe` → `Forge_1.0.0_Setup.exe`
- 🔄 **LLM Configuration UI**: 
  - "Local LLM" → "LLM Configuration"
  - "Base URL" → "API Endpoint"
  - Removed Ollama-specific model suggestions
  - Added generic model placeholder suggestions
- 🔄 **AI Default State**: AI now disabled by default (enable when ready)
- 🔄 **Error Messages**: More helpful, generic messages instead of Ollama-specific

### Improved
- 💪 **Docs Generator**: Falls back to templates when AI unavailable
- 💪 **README Generator**: Uses templates with project info detection
- 💪 **CHANGELOG Generator**: Template-based with version/date placeholders
- 💪 **Architecture Doc Generator**: Smart template with structure detection
- 💪 **LLM Assistant**: Better error handling and connection feedback
- 💪 **User Experience**: Clear indication of AI vs template mode
- 💪 **Reliability**: No crashes when AI is disabled or unavailable

### Fixed
- 🐛 Fixed hard dependency on Ollama (now optional)
- 🐛 Fixed docs generator failures when LLM unavailable
- 🐛 Fixed confusing error messages about missing Ollama
- 🐛 Fixed AI status not updating after settings changes

### Removed
- ❌ Removed hardcoded Ollama URLs and model names
- ❌ Removed mandatory AI requirement
- ❌ Removed Ollama-specific quick start instructions

### Technical Details
- **Class Rename**: `ShipStudioApp` → `ForgeApp`
- **Settings Constants**: 
  - `DEFAULT_OLLAMA_BASE_URL` → `DEFAULT_LLM_BASE_URL`
  - `DEFAULT_OLLAMA_MODEL` → `DEFAULT_LLM_MODEL`
  - `DEFAULT_OLLAMA_TEMPERATURE` → `DEFAULT_LLM_TEMPERATURE`
- **Function Rename**: `_ollama_stream_request()` → `_llm_stream_request()`
- **Template Directory**: Added `core/templates/` with 4 base templates

### Migration Notes

If upgrading from Ship Studio 0.1.0:
1. Your old settings in `~/.ship_studio/` will not be automatically migrated
2. Reconfigure your LLM settings in the new FORGE UI
3. Icon file references updated from `ship_studio.ico` → `forge.ico`

---

## [0.1.0] - 2025-12-23 - "Ship Studio" (Legacy)

### Initial Release
- 📸 Screenshots module with full screen, region, and window capture
- 🔨 Build & Package module with multi-language support
- 🤖 AI Packager for ML model bundling
- 📝 Docs & Changelog generator (AI-powered, Ollama only)
- 🚀 Release Creator for bundling releases
- 🧠 LLM Assistant (Ollama integration)

---

## Future Releases

See [README.md](README.md#roadmap) for planned features.

---

*Keep forging ahead! 🔥*
