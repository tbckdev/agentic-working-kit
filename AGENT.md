# Instructions for AI Agents

This repository contains agentic resources for AgenticWorking.io workflows.

## How to use this repo

1. Each folder is a standalone workflow.
2. Read the `README.md` in the workflow folder first.
3. Check `workflows/*.md` for step-by-step AI-executable instructions.
4. Use `scripts/` to run automation.

## Workflow folder structure

```
workflow-name/
├── README.md           # Overview
├── prompt-guide.md     # Prompting tips
├── workflows/          # AI-executable instructions
├── scripts/            # Python/Node scripts
├── sample-data/        # Test data
└── tools/              # GUI applications
```

## Important rules

- Always check `requirements.txt` before running scripts.
- Sample data is for testing only.
- Follow the workflow order in `workflows/*.md`.
