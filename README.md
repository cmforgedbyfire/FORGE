# Ship Studio v1.0.0

**Release Engineering Toolkit by Forged By Fire Software LLC**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)

---

## 🔥 Overview

**Ship Studio** is a comprehensive desktop toolkit designed to streamline the entire software release process. From capturing screenshots and building packages to generating documentation and creating polished release bundles—Ship Studio handles it all in one unified interface.

Ship Studio v1.0.0 represents a major leap forward with AI-optional features, template-based generation, and a robust architecture ready for production use.

---

## ✨ Key Features

### 📸 **Screenshots Module**
- Capture full screen, custom regions, or window-centered screenshots
- Automated timestamping and organization
- Drag-and-drop folder selection
- Perfect for app stores, documentation, and marketing materials

### 🔨 **Build & Package Module**
- Multi-language project support (Python, Node.js, .NET, Go, Rust, etc.)
- Automated build execution with detailed logging
- Dependency installation and environment detection
- Build artifact collection and organization

### 🤖 **AI Packager Module**
- Scan and bundle AI/ML model files (.gguf, .pt, .safetensors, .onnx)
- Organize configs, scripts, and model artifacts
- Audit logging for AI project releases
- Ideal for shipping trained models

### 📝 **Docs & Changelog Generator**
- **AI-Powered**: Generate professional docs with LLM assistance
- **Template Mode**: Use smart templates when AI is disabled
- Auto-generate README, CHANGELOG, PRIVACY, ARCHITECTURE docs
- Smart project detection and placeholder filling

### 🚀 **Release Creator**
- One-click release bundle creation
- Automated folder structure generation
- Collect docs, screenshots, and build artifacts
- Version tracking and manifest generation

### 🧠 **LLM Assistant** *(Optional)*
- AI-powered content generation for product descriptions, guides, and more
- Support for Ollama, OpenAI API, Anthropic, and custom endpoints
- **Fully optional**: Disable AI and use template-based alternatives
- Preset workflows for common documentation tasks

---

## 🎯 What's New in v1.0.0 "FORGE"

### Major Changes
- ✅ **Rebranded** from Ship Studio to FORGE
- ✅ **AI-Optional Architecture**: Full functionality without requiring AI
- ✅ **Template System**: Professional doc templates as AI fallback
- ✅ **Generic LLM Support**: No longer tied to Ollama—use any compatible endpoint
- ✅ **AI Mode Indicator**: Real-time status showing AI enabled/disabled
- ✅ **Settings Migration**: Moved from `~/.ship_studio/` to `~/.forge/`
- ✅ **Production Ready**: Stable, tested, and ready for serious use

### Technical Improvements
- Removed Ollama hardcoding
- Added template-based doc generation
- Improved error handling and user feedback
- Enhanced LLM configuration flexibility
- Better project type detection

---

## 📦 Installation

### Windows

1. **Download** the installer: `Forge_1.0.0_Setup.exe`
2. **Run** the installer
3. **Launch** FORGE from your Start Menu or Desktop shortcut

### From Source

```bash
# Clone the repository
git clone https://github.com/YourOrg/forge.git
cd forge

# Install dependencies
pip install -r requirements.txt

# Run FORGE
python main.py
```

---

## 🚀 Quick Start

### First Launch

1. **Open FORGE** and familiarize yourself with the tabs
2. **Configure AI** (optional):
   - Navigate to "LLM Assistant" tab
   - Enter your LLM endpoint URL (Ollama, OpenAI, custom)
   - Enter your model name
   - Enable "AI Enabled" checkbox
   - Click "Check LLM" to verify connection

### Creating Your First Release

1. **Screenshots Tab**:
   - Set output directory
   - Capture screenshots of your app
   
2. **Build & Package Tab**:
   - Select your project folder
   - Choose project type (or use auto-detect)
   - Click "Run Build" to compile/package
   
3. **Docs & Changelog Tab**:
   - Select project folder
   - Generate README, CHANGELOG, PRIVACY docs
   - Edit and customize as needed
   
4. **Release Creator Tab**:
   - Select project folder
   - Choose release destination
   - Enable docs, screenshots, and build outputs
   - Click "Create Release" to bundle everything

---

## 🛠️ Configuration

### AI Configuration

**Location**: LLM Assistant tab

- **API Endpoint**: URL of your LLM server (e.g., `http://localhost:11434` for Ollama)
- **Model**: Name of your model (e.g., `your-model-name`, `gpt-4`, `claude-3-5-sonnet`)
- **Temperature**: 0.0 (deterministic) to 1.0 (creative)
- **AI Enabled**: Toggle AI features on/off

### Settings Files

- **Location**: `~/.forge/settings.json`
- **Logs**: `~/.forge/logs/` *(coming soon)*

### Template Customization

Templates are located in `core/templates/`:
- `README.md`
- `CHANGELOG.md`
- `PRIVACY.md`
- `ARCHITECTURE.md`

Edit these files to customize the output when AI is disabled.

---

## 🤖 AI Features (Optional)

FORGE works perfectly **without AI**. When AI is disabled:
- Documentation uses smart templates with project detection
- Placeholders are filled based on project structure
- All core features remain fully functional

When AI is **enabled**:
- Docs are generated with contextual awareness
- LLM Assistant provides interactive help
- Content is tailored to your specific project

### Supported LLM Providers

- **Ollama** (local): `http://localhost:11434`
- **OpenAI API**: `https://api.openai.com/v1`
- **Anthropic**: Via compatible proxy
- **Custom Endpoints**: Any OpenAI-compatible API

---

## 📚 Documentation

### Module Guides

- **Screenshots**: Capture professional screenshots with flexible options
- **Build & Package**: Multi-language build automation
- **AI Packager**: Bundle ML models and configs
- **Docs Generator**: Create documentation with AI or templates
- **Release Creator**: Assemble complete release packages
- **LLM Assistant**: Interactive AI-powered content generation

### Supported Project Types

- Python (pip, poetry, conda)
- Node.js (npm, yarn, pnpm)
- .NET (C#, F#)
- Go
- Rust
- Generic/Custom

---

## 🏗️ Building from Source

### Requirements

- Python 3.8+
- tkinter (usually included with Python)
- See `requirements.txt` for all dependencies

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run FORGE
python main.py
```

### Building Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build with spec file
pyinstaller ShipStudio.spec

# Find executable in dist/Forge.exe
```

### Creating Installer

```bash
# Install Inno Setup (Windows)
# Open installer/ship_studio.iss in Inno Setup Compiler
# Click Build → Compile
# Find installer in installer/output/
```

---

## 🔧 Troubleshooting

### AI Not Working

1. Verify LLM server is running
2. Check API endpoint URL is correct
3. Click "Check LLM" to test connection
4. Enable "AI Enabled" checkbox
5. If issues persist, disable AI and use template mode

### Build Failures

1. Check project type is correct (or use auto-detect)
2. Verify all dependencies are installed
3. Review build log for specific errors
4. Try manual build first to identify issues

### Missing Files in Release

1. Ensure folders exist (docs/, screenshots/, build/)
2. Check file permissions
3. Review release manifest after creation

---

## 📄 License

Copyright © 2026 Forged By Fire Software LLC. All rights reserved.

This software is proprietary. Unauthorized copying, distribution, or modification is prohibited.

---

## 🤝 Support

For issues, questions, or feature requests:

- **Email**: support@forgedbyfirellc.com
- **Documentation**: See `/docs` folder
- **GitHub Issues**: (if applicable)

---

## 🗺️ Roadmap

### Coming Soon
- ✨ Git integration (auto-tagging, commit-based changelogs)
- ✨ Batch operations (process multiple projects)
- ✨ Theme system (dark mode, light mode)
- ✨ Plugin architecture for custom workflows
- ✨ Cross-platform builds (macOS, Linux)

---

## 🙏 Credits

**Developed by**: Forged By Fire Software LLC  
**Version**: 1.0.0 "FORGE"  
**Release Date**: January 2026

Built with ❤️ and 🔥

---

*Transform your release process. Ship with confidence. Forge ahead.*
