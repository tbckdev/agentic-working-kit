# Project Structure Rules

Các quy tắc BẮT BUỘC về cấu trúc thư mục của dự án Agentic Working Kit.
Agent phải TUÂN THỦ TUYỆT ĐỐI các quy tắc này khi tạo file hoặc folder mới.

## 1. Projects Folder (`projects/`)
Mọi workflow/tool/dự án con đều phải nằm trong folder `projects/`.
KHÔNG tạo folder dự án ở root.

**✅ Đúng:**
- `projects/excel-merge/`
- `projects/image-resizer/`

**❌ Sai:**
- `excel-merge/`
- `image-resizer/`

## 2. Packages Folder (`packages/`)
Mọi file binary (`.exe`, `.app`, `.dmg`, `.zip`) và file build config (`.spec`) phải được lưu hoặc move vào `packages/`.
KHÔNG để file build ở root hoặc trong folders dự án sau khi build xong.

**✅ Đúng:**
- `packages/ExcelMerge.exe`
- `packages/ExcelMerge.spec`

**❌ Sai:**
- `dist/ExcelMerge.exe`
- `projects/excel-merge/tools/dist/ExcelMerge.exe`

## 3. Workflow Generator
Khi chạy lệnh `/create-workflow` hoặc tạo tool mới, agent phải tự động prefix `projects/` vào tên folder dự án.
Ví dụ: User đặt tên `pdf-merger` -> Agent tạo `projects/pdf-merger/`.

## 4. PyInstaller Output
Sau khi build xong bằng PyInstaller (`python -m PyInstaller ...`), agent phải thực hiện bước dọn dẹp:
1. Move file `.exe` từ `dist/` vào `packages/`.
2. Move file `.spec` từ root vào `packages/`.
3. Xóa folder `build/` và `dist/` rác.
