# Changelog

## Unreleased

### Added

- Added the Release Workspace tab with a lightweight release-readiness audit.
- Added project checks for docs, license, screenshots, build outputs, installer scripts, and stale retired-app artifacts.
- Added `.gitignore` for generated Python caches, build output, dist output, installer output, and local releases.

### Changed

- Cleaned public README and quickstart text for the free FORGE direction.
- Simplified AI status bar text to plain ASCII.
- Made the Release Workspace the first tab so users start with an audit instead of scattered tools.

### Fixed

- Removed duplicate AI status scheduling that could create repeated background updates.
- Removed broken backup UI modules that prevented full source compilation.

## 1.0.0 - 2026-01-14

### Added

- Initial FORGE-branded release toolkit direction.
- Screenshot capture module.
- Build and package module.
- AI packager module.
- Docs and changelog generator.
- Release creator.
- Optional LLM assistant.
