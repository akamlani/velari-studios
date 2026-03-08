# Makefile for setting up environment
#################### Read Environment
RUNTIME_FILE := ./config/runtime/runtime.env
include $(RUNTIME_FILE)

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
