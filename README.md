# Agentic Working Kit

Open-source resources for building AI Agent workflows, companion repository for [AgenticWorking.io](https://agenticworking.io).

## 🚀 Overview

**Turn AI into your digital colleague.**
This repository provides ready-to-use "kits" that allow you to work agentically with AI. Instead of using AI as a consultant (ask → do it yourself), you use AI as a colleague (assign task → AI executes).

- **Save 10+ hours per week** by automating repetitive tasks.
- **No coding required** to use the tools (download & run).
- **Fully customizable** using AI Agents (Claude, Gemini, Cursor).

## 📦 Available Workflows

| Workflow                                            | Description               | Key Features                                                                                                                                |
| :-------------------------------------------------- | :------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------ |
| **[invitation-maker](./projects/invitation-maker)** | Bulk invitation generator | • Generate 1000+ personalized image invitations from Excel<br>• Custom font support<br>• QR code integration                                |
| **[media-processor](./projects/media-processor)**   | Batch image processor     | • Smart resize with padding (no cropping)<br>• Watermark with auto-scaling<br>• Process thousands of images in seconds                      |
| **[excel-merge](./projects/excel-merge)**           | Excel consolidation tool  | • Merge hundreds of Excel files into one Master report<br>• Traceability (Source_File column)<br>• Handle locked/corrupted files gracefully |
| **[/create-workflow](./.agent/workflows)**          | Workflow Generator        | • Agent command to rapidly scaffold new tools<br>• Enforces consistent structure<br>• Generates `README`, `scripts`, and `GUI` templates    |

## 🛠️ Usage Guide

### Method 1: Download & Run (For Non-Coders)
Every workflow comes with pre-packaged tools for Windows and macOS.

1. Go to [Releases](https://github.com/egany/agentic-working-kit/releases/latest).
2. Download the tool you need (e.g., `ExcelMerge.zip`).
3. Extract and run the executable.

### Method 2: Use with AI Agent (For Builders)
Clone this repo to collaborate with your AI Agent (Antigravity, Claude Code, Cursor).

```bash
git clone https://github.com/egany/agentic-working-kit.git
cd agentic-working-kit
```

**Workflow Structure:**
Each tool follows a standardized structure for easy AI understanding:
```
projects/tool-name/
├── README.md           # Documentation
├── prompt-guide.md     # Prompts to build/modify the tool
├── workflows/          # Step-by-step AI execution guide
├── scripts/            # Core Python logic (Headless)
├── tools/              # GUI Desktop App (PyQt6)
└── sample-data/        # Test files
```

## 📝 Changelog

Latest updates (see [CHANGELOG.md](./CHANGELOG.md) for full history):

- **[v1.0.0]** - Initial Release (2026-01-26)
  - Added **invitation-maker**: Bulk personalized invitations with QR codes.
  - Added **media-processor**: Smart batch resize and watermark tool.
  - Added **excel-merge**: Consolidate Excel files with traceability.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repo
2. Create your feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
<p align="center">
  Built with ❤️ by the <a href="https://agenticworking.io">AgenticWorking.io</a> team
</p>
