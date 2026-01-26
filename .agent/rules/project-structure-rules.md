# Project Structure Rules

MANDATORY rules for the Agentic Working Kit project structure.
Agents must STRICTLY ADHERE to these rules when creating new files or folders.

## 1. Projects Folder (`projects/`)
All workflows, tools, and sub-projects must be located inside the `projects/` folder.
DO NOT create project folders in the root directory.

**✅ Correct:**
- `projects/excel-merge/`
- `projects/image-resizer/`

**❌ Incorrect:**
- `excel-merge/`
- `image-resizer/`

## 2. Packages Folder (`packages/`)
All binary files (`.exe`, `.app`, `.dmg`, `.zip`) and build config files (`.spec`) must be saved or moved to `packages/`.
DO NOT leave build files in the root or inside project folders after building.

**✅ Correct:**
- `packages/ExcelMerge.exe`
- `packages/ExcelMerge.spec`

**❌ Incorrect:**
- `dist/ExcelMerge.exe`
- `projects/excel-merge/tools/dist/ExcelMerge.exe`

## 3. Workflow Generator
When running the `/create-workflow` command or creating a new tool, the agent must automatically prefix `projects/` to the project folder name.
Example: User names it `pdf-merger` -> Agent creates `projects/pdf-merger/`.

## 4. PyInstaller Output
After building with PyInstaller (`python -m PyInstaller ...`), the agent must perform the following cleanup steps:
1. Move the `.exe` file from `dist/` to `packages/`.
2. Move the `.spec` file from root to `packages/`.
3. Delete the `build/` and `dist/` folders.
