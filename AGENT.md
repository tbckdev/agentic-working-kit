# Instructions for AI Agents

**SYSTEM PROMPT ADDENDUM:**
If you are an AI Agent (Antigravity, Claude Code, Cursor, Windsurf) working in this repository, you **MUST** read and follow these instructions.

## 📂 Repository Structure

This repository follows a strict structure to organize workflows and build artifacts.

```text
root/
├── .agent/                 # Agent resources (Rules, Skills, Workflows)
│   ├── rules/              # MANDATORY project rules
│   ├── skills/             # Knowledge base (Git, PyQt6, Packaging)
│   └── workflows/          # Meta-workflows (e.g. create-workflow)
├── projects/               # SOURCE CODE for all tools/workflows
│   ├── invitation-maker/
│   ├── media-processor/
│   └── ...
├── packages/               # BUILD ARTIFACTS (Executables & Specs)
│   ├── ToolName.exe
│   └── ToolName.spec
├── CHANGELOG.md            # Version history
├── DISTRIBUTION.md         # Download links
└── README.md               # User documentation
```

## 🚨 Critical Rules

Before performing any actions, you must read:
**[.agent/rules/project-structure-rules.md](file:///.agent/rules/project-structure-rules.md)**

**Summary:**
1.  **Projects**: All source code MUST go into `projects/{project-name}/`. NEVER in root.
2.  **Packages**: All binaries (`.exe`, `.zip`) and `.spec` files MUST go into `packages/`.
3.  **Clean Root**: Keep the root directory clean. Only documentation and configuration files belong there.

## 🧠 Available Skills

Use these skills to enhance your coding capabilities. Read the relevant `SKILL.md` before starting work.

-   **Git Workflow** (`.agent/skills/git-workflow`): Commit conventions (`feat:`, `fix:`), branching strategies, and error handling.
-   **PyQt6 Patterns** (`.agent/skills/pyqt6-patterns`): Architecture for GUI apps, threading with `QThread`, and error handling.
-   **Python Packaging** (`.agent/skills/python-packaging`): Building `.exe` files with PyInstaller, handling assets, and cross-platform rules.
-   **Excel Processing** (`.agent/skills/excel-processing`): Robust reading/writing of Excel files using `pandas` and `openpyxl`.

## 🛠️ Common Tasks

### 1. Create a New Workflow
Run the following slash command to scaffold a new project:
```bash
/create-workflow
```
*Follow the interactive prompt to generate the correct folder structure in `projects/`.*

### 2. Build an Executable
Refer to **Python Packaging Skill**.
1.  Run `pyinstaller` command.
2.  **Move** the resulting `.exe` from `dist/` to `packages/`.
3.  **Move** the `.spec` file to `packages/`.
4.  **Delete** `build/` and `dist/` folders.

### 3. Release a Version
1.  Update `CHANGELOG.md` with new features.
2.  Commit with message `release: vX.Y.Z`.
3.  Tag the commit: `git tag vX.Y.Z`.
4.  Push: `git push origin vX.Y.Z`.

---
**Note:** This file is for YOU (the Agent). The user documentation is in `README.md`.
