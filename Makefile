PACKAGE := icons-heroicons
VERSION := 1.0.0
PREFIX ?= /usr
DESTDIR ?=
BINDIR := $(DESTDIR)$(PREFIX)/bin
MANDIR := $(DESTDIR)$(PREFIX)/share/man
COMPLETIONDIR := $(DESTDIR)$(PREFIX)/share/bash-completion/completions
DATADIR := $(DESTDIR)$(PREFIX)/share/$(PACKAGE)

SCRIPTS :=
MANPAGES :=
COMPLETIONS :=

.PHONY: all install uninstall build-assets build-png clean help

all: help

help:
	@echo "Available targets:"
	@echo "  install       - Install data files"
	@echo "  uninstall     - Remove installed files"
	@echo "  build-assets  - Build PNG and JPG assets (default sizes)"
	@echo "  build-png     - Build PNG assets only"
	@echo "  clean         - Remove generated assets"
	@echo "  help          - Show this help message"

install: install-data
	@echo "Installation complete"

install-scripts:
	@echo "Installing scripts to $(BINDIR)..."
	@mkdir -p $(BINDIR)
	@for script in $(SCRIPTS); do \
		install -m 755 $$script $(BINDIR)/$$(basename $$script); \
	done

install-man:
	@echo "Installing man pages to $(MANDIR)..."
	@mkdir -p $(MANDIR)/man1
	@for manpage in $(MANPAGES); do \
		install -m 644 $$manpage $(MANDIR)/man1/$$(basename $$manpage); \
	done

install-completions:
	@echo "Installing bash completions to $(COMPLETIONDIR)..."
	@mkdir -p $(COMPLETIONDIR)
	@for completion in $(COMPLETIONS); do \
		install -m 644 $$completion $(COMPLETIONDIR)/$$(basename $$completion); \
	done

install-data: build-assets
	@echo "Installing data files to $(DATADIR)..."
	@mkdir -p $(DATADIR)
	@cp -r data/svg $(DATADIR)/
	@cp -r data/jsx $(DATADIR)/
	@cp -r data/png $(DATADIR)/
	@install -d $(BINDIR)
	@install -m 755 bin/icons-heroicons $(BINDIR)/

uninstall:
	@echo "Uninstalling..."
	@for script in $(SCRIPTS); do \
		rm -f $(BINDIR)/$$(basename $$script); \
	done
	@for manpage in $(MANPAGES); do \
		rm -f $(MANDIR)/man1/$$(basename $$manpage); \
	done
	@for completion in $(COMPLETIONS); do \
		rm -f $(COMPLETIONDIR)/$$(basename $$completion); \
	done
	@rm -rf $(DATADIR)
	@echo "Uninstallation complete"

build-assets: build-png
	@echo "Asset build complete"

build-png:
	@echo "Building PNG assets..."
	@if [ ! -f scripts/batch-convert.sh ]; then \
		echo "Error: scripts/batch-convert.sh not found"; \
		exit 1; \
	fi
	@bash scripts/batch-convert.sh -t png

clean:
	@echo "Cleaning generated assets..."
	@rm -rf data/png
	@echo "Clean complete"

.DEFAULT_GOAL := help

