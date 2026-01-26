# Workflow Template

This folder contains templates for creating new workflows in the agentic-working-kit repository.

## Folder Structure

```
workflow-name/
├── README.md               # Workflow description (required)
├── prompt-guide.md         # AI prompts for building the tool (required)
├── workflows/
│   └── workflow-name.md    # Step-by-step execution guide (required)
├── scripts/
│   ├── main_script.py      # Core logic script
│   ├── config.json         # Configuration file
│   └── requirements.txt    # Python dependencies
├── tools/
│   ├── main.py             # GUI application (if applicable)
│   ├── requirements.txt    # GUI dependencies
│   ├── README.md           # Tool documentation
│   ├── Launcher.bat        # Windows launcher
│   └── Launcher.command    # macOS launcher
└── sample-data/
    ├── input-file.xlsx     # Sample input data
    ├── template.png        # Sample template
    └── output/             # Generated output folder
```

## Templates Included

| File                       | Description                 |
| -------------------------- | --------------------------- |
| `README.template.md`       | Workflow README template    |
| `prompt-guide.template.md` | AI prompt guide template    |
| `workflow.template.md`     | Execution workflow template |
| `script.template.py`       | Python script template      |
| `tool-main.template.py`    | GUI tool template           |
| `config.template.json`     | Configuration template      |

## How to Use

1. Copy the entire `workflow-template/` folder
2. Rename to your workflow name (kebab-case, e.g., `media-processor`)
3. Replace `{{WORKFLOW_NAME}}` placeholders with your workflow name
4. Fill in the specific content for each file
5. Add sample data files
6. Test the workflow
