# FORGE Roadmap

## Current Mission

Convert the older toolkit into the focused FORGE product for AI-assisted solo builders.

The goal is not more features. The goal is a guided path from "folder full of code" to "release I can share."

## Phase 0 - Orientation

Status: active

- [x] Choose FORGE as the company focus.
- [x] Identify the renamed `F:\company\FORGE` codebase as the starting point.
- [x] Define the product niche.
- [x] Create focus, roadmap, and future-ideas documents.
- [x] Run the existing app locally and note what works.
- [ ] Capture screenshots of the current UI.
- [x] Identify the current main entry point and module wiring.
- [x] Decide the visible brand: FORGE.

## Phase 1 - Release Readiness Audit

Goal: FORGE should inspect a project folder and tell the user what is needed before release.

- [x] Create a project scanner service.
- [x] Detect project type: Python, Node, static web markers, and generic source.
- [x] Detect existing docs: README, CHANGELOG, PRIVACY, LICENSE.
- [x] Detect build files: requirements, pyproject, package.json, spec files.
- [x] Detect release assets: icons, screenshots, installer scripts.
- [x] Detect obvious stale artifacts from the retired app direction.
- [x] Produce a release-readiness score.
- [ ] Group checklist by Required, Recommended, Optional.

## Phase 2 - Guided Release Workspace

Goal: Replace scattered tabs with one clear workflow.

- [x] Add a "Release Workspace" screen.
- [x] Project folder selector at the top.
- [x] Audit checklist panel.
- [x] Action buttons for the major tool tabs.
- [ ] Keep existing tabs accessible as tools, but make the guided workflow primary.
- [ ] Save project state so returning to a folder remembers progress.

## Phase 3 - Documentation Finisher

Goal: Generate useful docs from the actual project, not generic filler.

- [ ] Improve project metadata extraction.
- [ ] Generate README from detected commands, folders, and app purpose.
- [ ] Generate CHANGELOG from manual notes first, Git later.
- [ ] Generate PRIVACY based on local/cloud/network behavior.
- [ ] Generate RELEASE_NOTES for the current bundle.
- [ ] Add "Review required" markers where FORGE is unsure.

## Phase 4 - Build And Bundle

Goal: Produce a clean release folder for at least one project type reliably.

- [ ] Pick first supported lane: Python desktop app.
- [ ] Support PyInstaller build flow.
- [ ] Collect executable, docs, screenshots, license, and manifest.
- [ ] Create portable zip.
- [ ] Write release manifest with version, date, included files, and build notes.
- [ ] Add failure diagnostics and manual fallback instructions.

## Phase 5 - Polish The First Demo

Goal: Make FORGE impressive in one repeatable demo.

- [ ] Use PC Purifier or QR Studio as the first demo project.
- [ ] Run FORGE against the demo project from scratch.
- [ ] Record missing-item checklist before fixing.
- [ ] Generate docs and release folder.
- [ ] Capture before/after screenshots.
- [ ] Write a short product page draft.

## Success Criteria For The First Milestone

FORGE is ready for a first public demo when it can:

- Open a project folder.
- Explain what is missing for release.
- Generate at least README, CHANGELOG, PRIVACY, and RELEASE_NOTES.
- Build or bundle one project type.
- Create a clean release folder with a manifest.
- Produce a result a non-technical friend could download and understand.
