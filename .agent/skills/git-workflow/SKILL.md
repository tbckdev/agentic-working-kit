---
name: git-workflow
description: Git workflow patterns, commit conventions, and edge case handling for Antigravity projects
---

# Git Workflow Skill

Hướng dẫn quy trình Git chuẩn khi làm việc với Antigravity, bao gồm commit conventions, branching strategies, và xử lý edge cases.

## 📋 Commit Message Convention

### Format
```
<type>: <short description>

[optional body]
[optional footer]
```

### Types
| Type       | Khi nào dùng                         | Ví dụ                                                |
| ---------- | ------------------------------------ | ---------------------------------------------------- |
| `feat`     | Thêm tính năng mới                   | `feat: Add output folder selection to Excel Merge`   |
| `fix`      | Sửa bug                              | `fix: Handle corrupt Excel files gracefully`         |
| `docs`     | Chỉ thay đổi documentation           | `docs: Update README with installation guide`        |
| `refactor` | Code changes không thay đổi behavior | `refactor: Extract merge logic to separate function` |
| `style`    | Formatting, không thay đổi logic     | `style: Fix indentation in main.py`                  |
| `test`     | Thêm/sửa tests                       | `test: Add unit tests for excel_merge.py`            |
| `chore`    | Build, tools, dependencies           | `chore: Update requirements.txt`                     |

### Quy tắc
- **Viết thường** cho type
- **Không dấu chấm** ở cuối description
- Description ngắn gọn, **≤50 ký tự**
- Dùng **imperative mood**: "Add feature" không phải "Added feature"

---

## 🌿 Branching Strategy

### Simple Flow (Solo/Small Team)
```
main ──────────────────────────────────
       └── feature-x ──┘
```

- Làm việc trên `main` hoặc short-lived feature branches
- Merge/push thường xuyên

### Git Flow (Team/Production)
```
main ─────────────────────────────────────────
  └── develop ────────────────────────────────
        ├── feature/add-watermark ──┤
        └── feature/batch-resize ───┘
```

---

## 🔧 Quy trình làm việc

### 1. Trước khi code
```bash
git status                    # Kiểm tra trạng thái
git pull origin main          # Lấy code mới nhất
```

### 2. Trong khi code
```bash
git add <files>               # Stage specific files
git add -A                    # Stage all changes
git status                    # Verify staged files
```

### 3. Commit
```bash
git commit -m "feat: Add new feature"
```

### 4. Push
```bash
git push origin main          # Push to remote
```

---

## ⚠️ Edge Cases & Xử lý

### 1. Push bị reject (remote có commits mới)
```
! [rejected] main -> main (fetch first)
error: failed to push some refs
```

**Giải pháp:**
```bash
git pull --rebase origin main    # Preferred: rebase local commits
git push origin main
```

Hoặc:
```bash
git pull origin main             # Merge remote changes
git push origin main
```

---

### 2. Conflict khi pull/merge
```
CONFLICT (content): Merge conflict in main.py
```

**Giải pháp:**
1. Mở file conflict, tìm markers:
```python
<<<<<<< HEAD
your_code()
=======
their_code()
>>>>>>> origin/main
```

2. Chọn code đúng, xóa markers
3. Stage và commit:
```bash
git add main.py
git commit -m "fix: Resolve merge conflict in main.py"
```

---

### 3. Commit nhầm file (chưa push)
```bash
git reset --soft HEAD~1          # Undo commit, giữ changes staged
git reset HEAD <file>            # Unstage file
git commit -m "correct message"  # Commit lại
```

---

### 4. Commit message sai (chưa push)
```bash
git commit --amend -m "feat: Correct message"
```

---

### 5. Đã push commit sai
> ⚠️ **Cẩn thận với force push trên shared branches!**

```bash
git revert HEAD                  # Tạo commit mới đảo ngược thay đổi
git push origin main
```

---

### 6. Muốn bỏ qua file đã track
```bash
# Thêm vào .gitignore
echo "file_to_ignore.txt" >> .gitignore

# Remove from git but keep local
git rm --cached file_to_ignore.txt
git commit -m "chore: Stop tracking file_to_ignore.txt"
```

---

### 7. Large file bị reject
```
remote: error: File xyz.exe is 123.00 MB; this exceeds the file size limit
```

**Giải pháp:**
1. Thêm vào `.gitignore`:
```
*.exe
*.app
*.dmg
```

2. Remove from history:
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/large-file" \
  --prune-empty -- --all
```

Hoặc dùng BFG Repo-Cleaner (nhanh hơn):
```bash
bfg --delete-files "*.exe"
git push --force
```

---

### 8. Xem lịch sử commits
```bash
git log --oneline -10            # 10 commits gần nhất, 1 dòng
git log --graph --oneline        # Với biểu đồ branch
git log --author="name"          # Theo tác giả
git log -- path/to/file          # Theo file cụ thể
```

---

### 9. Quay lại phiên bản cũ
```bash
# Xem file ở commit cũ (không thay đổi gì)
git show abc123:path/to/file.py

# Checkout file từ commit cũ
git checkout abc123 -- path/to/file.py

# Quay lại toàn bộ project (⚠️ dangerous)
git reset --hard abc123
```

---

## 📝 Quick Reference Commands

| Tình huống       | Command                           |
| ---------------- | --------------------------------- |
| Xem status       | `git status`                      |
| Xem diff         | `git diff`                        |
| Stage tất cả     | `git add -A`                      |
| Commit           | `git commit -m "msg"`             |
| Push             | `git push origin main`            |
| Pull             | `git pull origin main`            |
| Xem log          | `git log --oneline -5`            |
| Undo last commit | `git reset --soft HEAD~1`         |
| Amend message    | `git commit --amend -m "new msg"` |
| Discard changes  | `git checkout -- file.py`         |
| Create branch    | `git checkout -b feature-x`       |
| Switch branch    | `git checkout main`               |
| Merge branch     | `git merge feature-x`             |
| Delete branch    | `git branch -d feature-x`         |

---

## 🤖 Antigravity Integration

Khi Antigravity thực hiện git operations, nó sẽ:

1. **Verify trước khi commit**: `git status` để check staged files
2. **Dùng semantic commits**: Type + description theo convention
3. **Không force push** trừ khi user yêu cầu
4. **Hỏi user** khi gặp conflict hoặc edge cases

### Ví dụ yêu cầu tốt:
- "Commit và push với message 'feat: Add excel merge'"
- "Tạo branch feature/add-watermark và push"
- "Xem 5 commits gần nhất"

### Ví dụ yêu cầu cần clarification:
- "Undo commit" → "Commit đã push chưa? Nếu chưa dùng reset, nếu rồi dùng revert"
- "Reset all" → "Bạn muốn reset soft (giữ changes) hay hard (mất changes)?"
