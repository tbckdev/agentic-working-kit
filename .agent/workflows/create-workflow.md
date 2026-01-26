---
description: Create a new workflow with complete folder structure and template files
---

# Create New Workflow
Create a new workflow with a complete folder structure and template files, based on available templates.

## ⚠️ Required Inputs - ASK BEFORE PROCEEDING

> **STOP!** If you do not have the information below, ASK THE USER immediately.
> DO NOT guess or skip any input.

| #   | Input             | Description                    | Example                                            |
| --- | ----------------- | ------------------------------ | -------------------------------------------------- |
| 1   | **workflow_name** | Folder name (kebab-case)       | `image-resizer`                                    |
| 2   | **title**         | Tool Title                     | `Image Resizer Pro`                                |
| 3   | **description**   | Short description (1 sentence) | `Batch resize images to specific dimensions`       |
| 4   | **pain_point**    | Problem needed to solve        | `Manually resizing hundreds of images takes hours` |
| 5   | **solution**      | Tool solution provided         | `Smart batch resize with progress tracking`        |
| 6   | **input_files**   | Input required from user       | `Folder containing images, config file`            |
| 7   | **output_files**  | Tool output                    | `Resized images in output folder`                  |
| 8   | **key_features**  | 3-4 key features               | `Smart resize, Batch processing, Progress bar`     |

**Sample Question:**
```
To create a new workflow, I need the following information:

1. Workflow name (kebab-case, e.g., image-resizer)?
2. Display Title (e.g., Image Resizer Pro)?
3. Short description of what this tool does?
4. Problem/pain point this tool solves?
5. Solution the tool provides?
6. Input files the user needs to provide?
7. Output files the tool will create?
8. 3-4 Key features?
```

---

## Execution Steps

### Step 1: Create Folder Structure
// turbo
```bash
mkdir -p projects/{workflow_name}/scripts
mkdir -p projects/{workflow_name}/tools
mkdir -p projects/{workflow_name}/workflows
mkdir -p projects/{workflow_name}/sample-data/input
mkdir -p projects/{workflow_name}/sample-data/output
```

### Step 2: Create README.md

Create file `projects/{workflow_name}/README.md` with content:
```markdown
# {title}

{description}

## Features

- {feature_1}
- {feature_2}
- {feature_3}
- {feature_4}

## Requirements

- Python 3.10+
- Dependencies listed in `scripts/requirements.txt`

## Quick Start

### Option 1: Run Script Directly
\`\`\`bash
cd scripts
pip install -r requirements.txt
python main_script.py
\`\`\`

### Option 2: Use GUI Tool
\`\`\`bash
cd tools
pip install -r requirements.txt
# Windows: double-click {AppName}.bat
# macOS: double-click {AppName}.command
\`\`\`

### Option 3: Use AI Agent
Follow the prompts in `prompt-guide.md` or use the workflow in `workflows/{workflow_name}.md`.

## License

MIT License
```

### Step 3: Create prompt-guide.md

Create file `projects/{workflow_name}/prompt-guide.md` with 2 phases:
- **Phase 1**: Core logic script prompt
- **Phase 2**: GUI desktop app prompt (PyQt6)

### Step 4: Create Workflow Execution File

Create file `projects/{workflow_name}/workflows/{workflow_name}.md` with:
- YAML frontmatter (description)
- Required inputs table
- Step-by-step execution commands
- Expected output
- Error handling table

### Step 5: Create Scripts Folder

Create files in `projects/{workflow_name}/scripts/`:
- `config.json` - Configuration template
- `requirements.txt` - Python dependencies
- `main_script.py` - Core logic script (implement according to Phase 1 prompt)

### Step 6: Create Tools Folder

Create files in `projects/{workflow_name}/tools/`:
- `main.py` - PyQt6 GUI app (implement according to Phase 2 prompt)
- `requirements.txt` - GUI dependencies
- `{AppName}.bat` - Windows launcher
- `{AppName}.command` - macOS launcher
- `README.md` - Tool documentation

### Step 7: Create Sample Data

Create `projects/{workflow_name}/sample-data/README.md` describing:
- Input folder structure
- Output folder structure
- Sample files needed

### Step 8: Verify
// turbo
```bash
ls -la projects/{workflow_name}/
ls -la projects/{workflow_name}/scripts/
ls -la projects/{workflow_name}/tools/
ls -la projects/{workflow_name}/workflows/
```

---

## Output Structure

```
projects/{workflow_name}/
├── README.md
├── prompt-guide.md
├── workflows/
│   └── {workflow_name}.md
├── scripts/
│   ├── config.json
│   ├── main_script.py
│   └── requirements.txt
├── tools/
│   ├── main.py
│   ├── requirements.txt
│   ├── {AppName}.bat
│   ├── {AppName}.command
│   └── README.md
└── sample-data/
    ├── README.md
    ├── input/
    └── output/
```

## References

- Template files: `_templates/`
- Example workflows: `invitation-maker/`, `media-processor/`
