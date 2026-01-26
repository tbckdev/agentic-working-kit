# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-26

### 🚀 Added

- **invitation-maker**: Workflow generator for bulk personalized invitations.
  - Supports Excel/CSV input.
  - QR code generation.
  - Custom fonts and image templates.
  
- **media-processor**: Batch image processing workflow.
  - Smart resize with padding.
  - Watermark overlay with auto-scaling.
  - Drag & Drop watermark positioning GUI.

- **excel-merge**: Excel consolidation workflow.
  - Merges .xlsx/.xls files into one Master report.
  - Adds `Source_File` column for traceability.
  - Handles locked and corrupted files gracefully.

- **Agentic Skills**:
  - `git-workflow`: Commit conventions and branching strategies.
  - `pyqt6-patterns`: Best practices for GUI apps.
  - `python-packaging`: PyInstaller guides.
  - `excel-processing`: Robust data handling patterns.

- **Workflow Generator**:
  - `/create-workflow` command to scaffold new tools automatically.

### 📚 Documentation

- Comprehensive `README.md` with usage guides.
- Detailed `prompt-guide.md` for each workflow (Phase 1 & 2).
- `SKILL.md` files for all agentic skills.
