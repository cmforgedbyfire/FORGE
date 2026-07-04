# FORGE Polish Notes

This file records the current polish state after the project moved fully to FORGE.

## Completed

- FORGE branding is present in the app title, icon, spec file, and installer script.
- Release Workspace is now the first screen.
- The app can audit a project folder and show a readiness score.
- Public README and quickstart docs are clean, plain text, and aligned with the free software direction.
- Broken backup UI modules were removed.
- Generated caches and stale retired-app artifacts were removed from the local project folder.
- `.gitignore` now excludes local caches, build output, installer output, and release output.

## Still Needed

- Rebuild the Windows executable as `FORGE.exe`.
- Compile the installer as `FORGE_v1.0.0_Setup.exe`.
- Launch-test both the source app and built executable.
- Capture screenshots for the website.
- Improve the Release Workspace so it can guide fixes without forcing users through separate tabs.
