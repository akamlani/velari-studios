# velari-studios
Velari Studios AI Studio Component development

---

*Quick links:* [Quick Start](#quick-start) · [Directory Structure](#directory-structure) · [Development Best Practices](#development-best-practices)

---
## Quick Start
### 1. Clone the Repository
```shell
git clone https://github.com/akamlani/velari-studios.git
cd velari-studios
```

### 2. Development Installation
```shell
# core setup for dotfiles, vaultspace, directory structure and symbolic links
make install
# python installation and virtual environment setup
make install_python
# coding agent specific setup and coding agent symbolic links
make install_agent
# clean up any files
make clean
```

---
## Directory Structure
```
velari-studios/
├── velari/                          # Main Python package
│   ├── __init__.py
│   ├── version.py
│   ├── ai/                          # AI components
│   ├── core/                        # Core utilities
│   │   ├── types.py                 # Shared type definitions
│   │   ├── experiment.py            # Experiment tracking
│   │   ├── io/                      # I/O utilities
│   │   │   ├── filesystem.py
│   │   │   └── partition/hydra.py   # Hydra config partitioning
│   │   └── utils/
│   │       └── env_utils.py         # Environment variable helpers
│   ├── data/                        # Data components
│   ├── integrations/                # Third-party integrations
│   └── services/                    # Service components
├── config/                          # Configuration files
│   ├── config.yaml                  # Main config
│   ├── logging.yaml                 # Logging config
│   ├── runtime/                     # Runtime environment vars
│   │   ├── runtime.env
│   │   └── python.env
│   ├── experimentation/             # Experiment configs
│   └── tracing/                     # Tracing configs (e.g. MLflow)
├── examples/                        # Usage examples
│   ├── imports_common.py            # Common imports helper
│   └── config/config_loader.py      # Config loading example
├── apps/                            # Application components
├── data/                            # Data files
├── docs/                            # Documentation
├── scripts/                         # Shell scripts
│   └── start_mlflow.sh
├── stores/                          # Symlinked from Obsidian vault
│   ├── contextlib/                  # Rules and style guides
│   ├── artifactlib/                 # Artifacts
│   └── promptlib/                   # Prompts
├── templates/                       # Project templates
├── logs/                            # Runtime logs
├── .claude/                         # Claude coding agent config (auto-generated)
│   ├── agents/                      # Subagent definitions
│   ├── commands/                    # Slash commands
│   ├── hooks/                       # Agent hook scripts
│   ├── rules/                       # Coding rules and guidelines
│   ├── skills/                      # Agent skills (symlinked)
│   │   ├── docgen/                  # Documentation generation skills
│   │   └── tasks/                   # Task management skills
│   └── settings.json                # Agent settings
├── _build/                          # Cloned external repos (not this repo)
├── AGENTS.md                        # Shared agent context (source of truth)
├── CLAUDE.md                        # Claude agent entrypoint → @AGENTS.md
├── GEMINI.md                        # Gemini agent entrypoint → @AGENTS.md
├── pyproject.toml                   # Project metadata and dependencies
├── uv.lock                          # Locked dependency manifest
└── Makefile                         # Dev automation
```


---
## Development Best Practices
- [ ] Styling Guidelines
    - Python:   `stores/contextlib/_rules/styles/styling-python.md`
    - Frontend: `stores/contextlib/_rules/styles/styling-frontend.md`
    - Makefile: `stores/contextlib/_rules/styles/styling-makefile.md`
- [ ] Typecheck when complete making a series of code changes
- [ ] Run Single Tests rather than entire Test Suite
---
