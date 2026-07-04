# FORGE

FORGE is a free Windows desktop toolkit for solo builders who need to turn a rough project folder into something they can share.

It is aimed at the last mile of small software releases: checking what is missing, generating basic docs, collecting screenshots, running simple build/package flows, and creating a clean release folder with a manifest.

## Current Status

FORGE is useful today as a release toolkit, but it is still early. The app now includes a Release Workspace audit screen that points users toward the existing tools:

- Release Workspace: scans a project folder and gives a readiness score.
- Screenshots: captures full screen, region, or centered window screenshots.
- Build & Package: detects common project types and runs simple build/package actions.
- AI Packager: gathers model/config/script files for AI or ML project releases.
- Docs & Changelog: generates README, CHANGELOG, PRIVACY, and architecture notes with templates or optional AI.
- Release Creator: creates a release folder with docs, screenshots, build outputs, and a manifest.
- LLM Assistant: optional helper for generated copy and documentation.

## Who It Is For

FORGE is for solo builders using AI coding tools, small utilities, local apps, tiny games, and experiments that work on their machine but are not yet easy to hand to someone else.

The guiding question is simple:

Can this help a solo builder ship a real release faster?

## Install From Source

Requirements:

- Windows
- Python 3.8 or newer
- tkinter, usually included with Python

```powershell
cd F:\company\FORGE
python -m pip install -r requirements.txt
python main.py
```

You can also run:

```powershell
.\START_FORGE.bat
```

## Basic Workflow

1. Open FORGE.
2. In Release Workspace, choose a project folder.
3. Review the readiness score and checklist.
4. Use the Screenshots, Build, Docs, and Release tabs to fill the gaps.
5. Create a release folder.
6. Review the generated `manifest.json` and included files before sharing.

## AI Is Optional

FORGE works without AI. When AI is disabled, docs are generated from local templates.

If you enable AI, FORGE can use a local or compatible LLM endpoint for stronger summaries and generated text. The default endpoint is configured in `core/config/settings.py`.

## Build An Executable

```powershell
python -m pip install pyinstaller
pyinstaller FORGE.spec
```

Expected output:

```text
dist\FORGE.exe
```

To create the Windows installer, compile `installer\forge.iss` with Inno Setup after `dist\FORGE.exe` exists.

## Project Notes

- Settings are stored under `~/.forge`.
- Generated build folders, caches, and local release output are ignored by `.gitignore`.
- The previous product direction is retired. FORGE is now focused on release readiness for solo builders.

## License

MIT License. See `LICENSE`.

## Support And Feedback

FORGE is a free project from Forged By Fire Software LLC.

If you try it, useful feedback is:

- What project type you tested.
- What FORGE detected correctly.
- What it missed.
- Whether the release folder was understandable.
- Any error messages or confusing steps.
