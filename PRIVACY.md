# Privacy

FORGE is a local Windows desktop application.

## What FORGE Reads

FORGE reads project folders that you choose inside the app. It may inspect filenames, folder structure, documentation files, screenshots, build outputs, and common project metadata so it can create a release-readiness checklist or release bundle.

## What FORGE Writes

FORGE may write generated documentation, screenshots, package files, release folders, manifests, logs, and local settings.

Settings and logs are stored under `~/.forge`.

## Network Use

FORGE does not require network access for its core workflow.

If you enable optional AI features, FORGE sends your prompt and selected project context to the LLM endpoint you configure. If AI is disabled, FORGE uses local templates instead.

## User Control

FORGE only works with folders you select. Review generated release folders before sharing them.
