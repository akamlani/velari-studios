# Makefile for setting up environment
#################### Read Environment
RUNTIME_FILE := ./config/runtime/runtime.env
PYTHON_FILE  := ./config/runtime/python.env
include $(RUNTIME_FILE)
include $(PYTHON_FILE)

#################### Makefile Configuration
GIT_ROOT ?= $(shell git rev-parse --show-toplevel)
# e.g., Darwin for MacOS
PLATFORM_TYPE = $(shell uname)
# dynamically detect shell type as bash or zsh
ifeq ($(shell basename $(SHELL)), zsh)
        SHELL := zsh
		SHELL_CONFIG := $(HOME)/.zshrc
else
        SHELL := bash
		SHELL_CONFIG := $(HOME)/.bashrc
endif

#################### Makefile Context
.DEFAULT_GOAL := info

.PHONY: help info info_dotfiles
help:
	@echo "Commands  : "
	@echo "download  : downloads dependencies distribution"
	@echo "system    : Installs System Libraries per $(PLATFORM_TYPE)"
	@echo "install   : create environment based on project $(PACKAGE_INSTALL_NAME)"
	@echo "verify_agents: compare $(COMPONENT_DIR) vs .claude trees"
	@echo "format    : formatting and linting of project $(PACKAGE_NAME)"
	@echo "clean     : cleans all files or project $(PACKAGE_INSTALL_NAME)"
	@echo "test      : execute unit testing"

info:
	@echo "Package:        $(PACKAGE_INSTALL_NAME) - $(PACKAGE_NAME)"
	@echo "Platform:       ${PLATFORM_TYPE}"
	@echo "Architecture:   $$(uname -m)"
	@echo "Shell:          $(SHELL)"

info_dotfiles:
	@echo "Dotfiles Repo:      $(DOTFILES_REPO)"
	@echo "Dotfiles Remote:    $(DOTFILES_REMOTE)"
	@echo "Dotfiles Branch:    $(BRANCH)"

#################### Installation
.PHONY: install install_setup install_dotfiles link_dotfiles link_vaultspace

install:
	@echo "Installing package $(PACKAGE_INSTALL_NAME) for development..."
	$(MAKE) install_setup
	$(MAKE) install_dotfiles
	$(MAKE) link_vaultspace

install_setup:
	@echo "Installing Setup for $(PACKAGE_NAME)..."
	mkdir -p .velari
	mkdir -p _build config docs
	touch .env.template
	touch docs/.gitkeep

install_dotfiles:
	@echo "Installing Dotfiles from $(DOTFILES_REPO)..."
	@if [ ! -d $(DOTFILES_DIR) ]; then \
		git clone $(DOTFILES_REPO) $(DOTFILES_DIR) && $(MAKE) link_dotfiles; \
	fi

# links to dotfiles: e.g., .vscode, .github for project configuration and templates
link_dotfiles:
	@echo "Linking Dotfiles..."
	ln -sf $(DOTFILES_DIR)/.vscode .vscode
	ln -sf $(DOTFILES_DIR)/.github .github

# links to obsidian vaults for contextlib, artifactlib, promptlib
link_vaultspace:
	@echo "Linking Vaultspace..."
	mkdir -p stores
	ln -sfn $(VAULTSPACE_ROOT)/contextlib 	stores/contextlib
	ln -sfn $(VAULTSPACE_ROOT)/artifactlib 	stores/artifactlib
	ln -sfn $(VAULTSPACE_ROOT)/promptlib 	stores/promptlib

#################### Install Python Environment and Dependencies
.PHONY: conda_config uv_download uv_install uv_sync install_python

install_python:
	@echo "Installing Python with uv..."
	$(MAKE) conda_config
	$(MAKE) uv_download
	$(MAKE) uv_install
	$(MAKE) uv_sync

conda_config:
	@if command -v conda >/dev/null 2>&1; then \
		echo "Configuration of Conda Environment..."; \
		conda config --set ssl_verify false; \
		conda config --set auto_activate_base false; \
		conda deactivate; \
	else \
		echo "Conda Environment not present; skipping conda_config."; \
	fi

uv_download:
	@echo "Installing UV package manager..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv   self update
	echo "UV version: $$(uv --version)"


# UV uses .python-version (or system default). Set it first so uv init and venv
# use PYTHON_VERSION; pass --python to uv venv so the venv is pinned explicitly.
uv_install:
	@echo "UV env $(PACKAGE_INSTALL_NAME)..."
	@echo "$(PYTHON_VERSION)" > .python-version
	@if [ ! -f pyproject.toml ]; then uv init; fi
	@uv python install $(PYTHON_VERSION)
	@if [ ! -d "$(PYTHON_VENV_DIR)" ]; then uv venv "$(PYTHON_VENV_DIR)" --python $(PYTHON_VERSION); fi
	@rm -f main.py

.ONESHELL:
uv_sync:
	@echo "Syncing UV Environment for project $(PACKAGE_INSTALL_NAME)..."
	source $(PYTHON_VENV_DIR)/bin/activate && \
	uv sync --active && uv pip install --upgrade pip ipykernel ipython && uv sync --active;
#	uv pip install -e .;
