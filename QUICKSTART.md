# 🚀 FORGE Quick Start Guide

Get up and running with FORGE in 5 minutes!

---

## Step 1: Launch FORGE

- **Windows**: Double-click the FORGE desktop icon or find it in Start Menu
- **From Source**: Run `python main.py` in the project directory

---

## Step 2: Choose Your Mode

FORGE offers two modes of operation:

### 🤖 **AI-Powered Mode** (Optional)
**Best for**: Dynamic content generation, context-aware documentation

**Setup**:
1. Navigate to **LLM Assistant** tab
2. Enter your LLM **API Endpoint**:
   - Ollama (local): `http://localhost:11434`
   - OpenAI: `https://api.openai.com/v1`
   - Custom: Your endpoint URL
3. Enter your **Model** name (e.g., `your-model-name`)
4. Check **"AI Enabled"** checkbox
5. Click **"Check LLM"** to verify connection
6. Click **"Save LLM Settings"**

### 📝 **Template Mode** (Default)
**Best for**: Quick starts, offline use, consistent formatting

**Setup**: Nothing! Just use FORGE as-is. Templates are already configured.

*Check the status bar (bottom-right) to see your current mode.*

---

## Step 3: Create Your First Release

### A. Capture Screenshots

1. Go to **Screenshots** tab
2. Click **"Browse"** to set output folder
3. Choose capture method:
   - **Full Screen**: Captures entire display
   - **Region**: Drag to select area
   - **Window**: Click to center on mouse position
4. Screenshots saved with timestamps!

### B. Build Your Project

1. Go to **Build & Package** tab
2. Click **"Browse"** to select your project folder
3. Choose **Project Type** (or use "auto" for detection)
4. Click **"Run Build"** to compile/package
5. Review build log in output area

### C. Generate Documentation

1. Go to **Docs & Changelog** tab
2. Click **"Browse"** to select project folder
3. Click one of:
   - **Generate README** - Full project documentation
   - **Generate CHANGELOG** - Release notes
   - **Generate PRIVACY** - Data handling policy
   - **Generate ARCHITECTURE** - Technical overview
4. Review and edit the generated content
5. Click **"Save As..."** to export

*In Template Mode: Docs use smart templates with auto-detected project info*  
*In AI Mode: Docs are generated with contextual understanding*

### D. Create Release Bundle

1. Go to **Release Creator** tab
2. Set **Project Path** (your source project)
3. Set **Target Path** (where to create release)
4. Enter **Release Name** (optional)
5. Check desired components:
   - ✅ Include Docs
   - ✅ Include Screenshots
   - ✅ Include Build
6. Click **"Create Release"**

Your complete release package is ready! 🎉

---

## Step 4: Use Advanced Features

### 🎨 LLM Assistant (AI Mode Only)

1. Go to **LLM Assistant** tab
2. Select a **Preset** for quick templates:
   - Product Description
   - README Overview
   - Privacy Statement
   - Changelog Entry
   - And more!
3. Enter your instructions in **Input** area
4. Optionally: Click **"Insert Project..."** to analyze project structure
5. Click **"Send to Assistant"**
6. Review AI-generated content
7. Click **"Save As..."** to export

### 📦 AI Packager (For ML Projects)

1. Go to **AI Packager** tab
2. Select your AI/ML project folder
3. Click **"Summarize Project"** to scan for:
   - Model files (.gguf, .pt, .safetensors)
   - Config files (.json, .yaml, .toml)
   - Scripts (.py, .sh, .bat)
4. Click **"Create Bundle"** to package everything
5. Includes audit logs for traceability

---

## Tips & Tricks

### 💡 Keyboard Shortcuts
- `Ctrl+Tab` / `Ctrl+Shift+Tab`: Switch between tabs
- `Alt+F4`: Close FORGE

### 💡 Drag & Drop
- **Screenshots tab**: Drag folder to set output directory
- **LLM Assistant tab**: Drag project folder to analyze

### 💡 Status Bar
- **Left**: Current operation status
- **Right**: AI mode indicator (🤖 Enabled / 📝 Template Mode)

### 💡 Template Customization
Edit templates in `core/templates/`:
- `README.md` - Main documentation template
- `CHANGELOG.md` - Release notes template
- `PRIVACY.md` - Privacy policy template
- `ARCHITECTURE.md` - Technical docs template

### 💡 Settings
- Location: `~/.forge/settings.json`
- Manually edit for advanced configuration
- Backup before experimenting!

---

## Common Workflows

### 📱 Mobile App Release
1. Screenshots → Capture app screens
2. Build & Package → Build APK/IPA
3. Docs Generator → README, PRIVACY
4. Release Creator → Bundle everything
5. Upload to app store!

### 🖥️ Desktop Software Release
1. Screenshots → Capture feature demos
2. Build & Package → Create installer
3. Docs Generator → Full documentation
4. Release Creator → Create release folder
5. Distribute via website/GitHub!

### 🤖 AI Model Release
1. AI Packager → Scan and bundle model files
2. Docs Generator → Model documentation
3. Screenshots → Example outputs (optional)
4. Release Creator → Complete model package

---

## Troubleshooting

### ❓ AI Not Working?
- Verify LLM server is running
- Check endpoint URL is correct
- Click "Check LLM" to test
- **Fallback**: Disable AI and use Template Mode

### ❓ Build Fails?
- Check project type selection
- Verify dependencies installed
- Review build log for errors
- Try manual build first

### ❓ Empty Release?
- Ensure source folders exist (docs/, screenshots/, build/)
- Check file permissions
- Review release manifest

### ❓ Settings Not Saving?
- Check `~/.forge/` folder permissions
- Manually create folder if needed
- Review error messages

---

## Next Steps

- 📖 Read full [README.md](README.md) for detailed documentation
- 📝 Review [CHANGELOG.md](CHANGELOG.md) for version history
- 🛠️ Customize templates in `core/templates/`
- 🤖 Configure your preferred LLM provider
- 🚀 Start shipping releases!

---

**Welcome to FORGE! Let's build something amazing. 🔥**

*For support: See README.md or contact Forged By Fire Software LLC*
