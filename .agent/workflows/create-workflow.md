---
description: Create a new workflow with complete folder structure and template files
---

# Create New Workflow

Tạo workflow mới với đầy đủ cấu trúc folders và files, dựa trên templates có sẵn.

## ⚠️ Required Inputs - PHẢI HỎI TRƯỚC KHI THỰC HIỆN

> **DỪNG LẠI!** Nếu chưa có đủ thông tin dưới đây, HỎI USER ngay.
> KHÔNG tự đoán hoặc bỏ qua bất kỳ input nào.

| #   | Input             | Mô tả                   | Ví dụ                                              |
| --- | ----------------- | ----------------------- | -------------------------------------------------- |
| 1   | **workflow_name** | Tên folder (kebab-case) | `image-resizer`                                    |
| 2   | **title**         | Tiêu đề tool            | `Image Resizer Pro`                                |
| 3   | **description**   | Mô tả ngắn (1 câu)      | `Batch resize images to specific dimensions`       |
| 4   | **pain_point**    | Vấn đề cần giải quyết   | `Manually resizing hundreds of images takes hours` |
| 5   | **solution**      | Giải pháp tool cung cấp | `Smart batch resize with progress tracking`        |
| 6   | **input_files**   | User cần cung cấp gì    | `Folder chứa ảnh, file config`                     |
| 7   | **output_files**  | Tool tạo ra gì          | `Ảnh đã resize trong folder output`                |
| 8   | **key_features**  | 3-4 tính năng chính     | `Smart resize, Batch processing, Progress bar`     |

**Câu hỏi mẫu:**
```
Để tạo workflow mới, tôi cần các thông tin sau:

1. Tên workflow (kebab-case, ví dụ: image-resizer)?
2. Tiêu đề hiển thị (ví dụ: Image Resizer Pro)?
3. Mô tả ngắn về tool này làm gì?
4. Vấn đề/pain point mà tool giải quyết?
5. Giải pháp tool cung cấp?
6. Input files user cần cung cấp?
7. Output files tool sẽ tạo ra?
8. 3-4 key features chính?
```

---

## Execution Steps

### Step 1: Tạo cấu trúc folder
// turbo
```bash
mkdir -p projects/{workflow_name}/scripts
mkdir -p projects/{workflow_name}/tools
mkdir -p projects/{workflow_name}/workflows
mkdir -p projects/{workflow_name}/sample-data/input
mkdir -p projects/{workflow_name}/sample-data/output
```

### Step 2: Tạo README.md

Tạo file `projects/{workflow_name}/README.md` với nội dung:
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

### Step 3: Tạo prompt-guide.md

Tạo file `projects/{workflow_name}/prompt-guide.md` với 2 phases:
- **Phase 1**: Core logic script prompt
- **Phase 2**: GUI desktop app prompt (PyQt6)

### Step 4: Tạo workflow execution file

Tạo file `projects/{workflow_name}/workflows/{workflow_name}.md` với:
- YAML frontmatter (description)
- Required inputs table
- Step-by-step execution commands
- Expected output
- Error handling table

### Step 5: Tạo scripts folder

Tạo các file trong `projects/{workflow_name}/scripts/`:
- `config.json` - Configuration template
- `requirements.txt` - Python dependencies
- `main_script.py` - Core logic script (implement theo Phase 1 prompt)

### Step 6: Tạo tools folder

Tạo các file trong `projects/{workflow_name}/tools/`:
- `main.py` - PyQt6 GUI app (implement theo Phase 2 prompt)
- `requirements.txt` - GUI dependencies
- `{AppName}.bat` - Windows launcher
- `{AppName}.command` - macOS launcher
- `README.md` - Tool documentation

### Step 7: Tạo sample-data

Tạo `projects/{workflow_name}/sample-data/README.md` mô tả:
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
