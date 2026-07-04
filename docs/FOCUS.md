# FORGE Focus

## Working Product Name

FORGE

## One-Sentence Product

FORGE turns a messy AI-built project folder into a clean, documented, packaged Windows release.

## Primary User

Solo builders using AI coding tools who can get an app working, but struggle to finish the last mile:

- project cleanup
- README and changelog
- screenshots
- build/package steps
- release folder
- installer or portable zip
- confidence that the project is shareable

## Product Promise

Bring FORGE a project folder. FORGE tells you what is missing, helps fix it, and creates a release bundle you can send to another person.

## What We Are Not Building Right Now

- A general DevOps suite
- A full IDE
- A GitHub replacement
- A cloud build service
- A PC cleaner
- A generic AI chat app
- A marketplace
- A multi-game overlay platform

Those may be useful later, but they are not the current fight.

## The First Killer Workflow

1. Choose a project folder.
2. FORGE detects the project type.
3. FORGE runs a release-readiness audit.
4. FORGE shows a checklist of missing or weak items.
5. FORGE helps create the required docs.
6. FORGE captures or imports screenshots.
7. FORGE runs the correct build/package flow.
8. FORGE creates a clean release folder.
9. FORGE writes a release manifest and next-step notes.

## Starting Place

Use the existing FORGE codebase as the foundation:

- Existing modules already cover screenshots, build/package, docs, release creation, AI packaging, and LLM assistance.
- The near-term work is not to invent more modules.
- The near-term work is to unify the existing modules around one guided release workflow.

## Guiding Rule

Every feature must answer this question:

Can this help a solo AI builder ship a real release faster?

If the answer is no, it goes in `FUTURE_IDEAS.md`.

