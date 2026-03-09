# velari-studios

Studio Suite of AI Prototyping Components.

## Project Overview
- **Package**: `velari-studios-ai`
- **Python**: `>=3.12`, managed via `uv`
- **Source**: `velari/` — main package with `core`, `ai`, `data`, `integrations`, `services`
- **Config**: `config/` — YAML configs + `config/runtime/` for env vars
- **Stores**: `stores/{contextlib,artifactlib,promptlib}` — symlinked from Obsidian vault

## Setup
```shell
make install          # core setup: dotfiles, vaultspace, directory structure, symlinks
make install_python   # python installation and virtual environment setup via uv
make install_agent    # coding agent setup: links .claude, .gemini, agent config
make clean            # remove build artifacts
```

## Key Structure
| Path                        | Purpose                                      |
|-----------------------------|----------------------------------------------|
| `velari/core/`              | Core types, experiment tracking, I/O, utils  |
| `velari/ai/`                | AI prototyping components                    |
| `velari/data/`              | Data components                              |
| `velari/integrations/`      | Third-party integrations                     |
| `velari/services/`          | Service components                           |
| `config/runtime/runtime.env`| Runtime environment variables                |
| `examples/`                 | Usage examples                               |
| `stores/contextlib/`        | Rules and style guides (Obsidian vault)      |
| `logs/`                     | Runtime logs                                 |
| `.claude/`                  | Claude agent config: skills, commands, rules |
| `.claude/skills/`           | Agent skills (symlinked from `_build/`)      |
| `AGENTS.md`                 | Shared agent context (source of truth)       |
| `CLAUDE.md`                 | Claude entrypoint → `@AGENTS.md`            |
| `GEMINI.md`                 | Gemini entrypoint → `@AGENTS.md`            |
| `_build/`                   | Cloned external repos (separate repositories)|

## Development Best Practices
- Styling guidelines: `stores/contextlib/_rules/styles/`
  - Python:   `styling-python.md`
  - Frontend: `styling-frontend.md`
  - Makefile: `styling-makefile.md`
- Typecheck after a series of code changes
- Run single tests rather than the full test suite
