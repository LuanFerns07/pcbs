# Repository instructions

## Organization

- Keep each independent hardware effort under `projects/<project>/` with its own context, documentation, libraries and boards.
- Put a resource in `shared/` only when it is reusable without a project-specific dependency. Repository-wide conventions belong in `docs/`.
- Preserve native KiCad source files; do not version generated caches or temporary lock files.

## Git

- Inspect `git status`, existing files, branch and remotes before editing. Preserve user changes and never run destructive Git operations.
- Do not commit without explicit maintainer authorization. If authorized, write every commit message in English, preferably Conventional Commits, inspect the staged diff, and do not include pre-existing user changes.
- Never change remotes unnecessarily or force-push. Do not push without explicit authorization.

## Engineering and documentation

- Target KiCad 10 where supported, but check the installed version before using version-specific features. Prefer native source and CLI; use `pcbnew` or IPC only after checking version compatibility.
- For electrical changes, consult component datasheets and inspect ERC, DRC, connectivity, polarity, board outline, holes and manufacturing exports. A clean DRC alone does not prove function.
- Never claim validation, fabrication or physical testing without reproducible evidence. Record unavailable tools as limitations.
- Keep educational explanations accessible in Portuguese and technical identifiers in English where useful. Explain electrical decisions in each project's `PROJECT_CONTEXT.md`.
- Use deterministic local scripts for repeated work and report summaries rather than flooding context with generated output. Use MCP or GUI interactions only when they materially help inspection or editing.
- Preserve official SVGs and colors. Until supplied, label any visual identity as provisional; do not invent an official logo.
