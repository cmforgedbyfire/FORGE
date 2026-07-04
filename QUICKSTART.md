# FORGE Quick Start

## 1. Launch

From PowerShell:

```powershell
cd F:\company\FORGE
python main.py
```

Or double-click `START_FORGE.bat`.

## 2. Audit A Project

1. Open the Release Workspace tab.
2. Click Browse.
3. Choose the project folder you want to ship.
4. Review the readiness score and checklist.

The audit checks for common release basics such as README, license, changelog, screenshots, build markers, installer scripts, and stale old artifacts.

## 3. Fill The Gaps

Use the action buttons at the bottom of Release Workspace:

- Screenshots: capture images for docs or the website.
- Build: detect project type and run supported build/package steps.
- Docs: generate README, CHANGELOG, PRIVACY, and architecture notes.
- Release: create a clean release folder with manifest.

## 4. Create A Release

1. Open Release Creator.
2. Select the project folder.
3. Select a release output folder.
4. Keep docs, screenshots, and build outputs checked if available.
5. Click One-Click Ship or Create Release Structure.

Review the generated release folder before sharing it.

## 5. Optional AI Setup

FORGE works without AI. If you want AI-generated docs:

1. Open LLM Assistant.
2. Set your endpoint and model.
3. Enable AI.
4. Test the connection.

When AI is disabled or unavailable, FORGE uses templates.

## Good First Test

Try FORGE on a small local utility first. The best feedback comes from seeing whether the readiness checklist matches what the project actually needs before release.
