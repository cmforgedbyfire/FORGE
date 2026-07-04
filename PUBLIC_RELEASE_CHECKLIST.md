# Public Release Checklist

Use this before putting a FORGE installer or zip on the website.

- Run `python -m compileall -q main.py core modules`.
- Launch `python main.py` and confirm the app opens.
- Audit FORGE itself in the Release Workspace.
- Build `dist\FORGE.exe` with `pyinstaller FORGE.spec`.
- Launch `dist\FORGE.exe`.
- Compile `installer\forge.iss` with Inno Setup.
- Install and uninstall once on Windows.
- Confirm the website download points to a FORGE installer, not an old ShipStudio binary.
- Confirm README, LICENSE, and QUICKSTART are included in the release.
- Capture two or three screenshots for the software detail page.
