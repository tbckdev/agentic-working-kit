---
name: git-workflow
description: Git workflow patterns, commit conventions, and edge case handling for Antigravity projects
---

# Git Workflow Skill

Standard Git workflow guidelines for working with Antigravity, including commit conventions, branching strategies, and handling edge cases.

## 📋 Commit Message Convention

### Format
```
<type>: <short description>

[optional body]
[optional footer]
```

### Types
| Type       | When to use                                           | Example                                              |
| ---------- | ----------------------------------------------------- | ---------------------------------------------------- |
| `feat`     | New feature                                           | `feat: Add output folder selection to Excel Merge`   |
| `fix`      | Bug fix                                               | `fix: Handle corrupt Excel files gracefully`         |
| `docs`     | Documentation only                                    | `docs: Update README with installation guide`        |
| `refactor` | Code changes that neither fix a bug nor add a feature | `refactor: Extract merge logic to separate function` |
| `style`    | Formatting, missing semi-colons, etc; no code change  | `style: Fix indentation in main.py`                  |
| `test`     | Adding missing tests or correcting existing tests     | `test: Add unit tests for excel_merge.py`            |
| `chore`    | Build process or auxiliary tool changes               | `chore: Update requirements.txt`                     |

### Rules
- Use **lowercase** for type
- **No dot** at the end of the description
- Description must be short, **≤50 chars**
- Use **imperative mood**: "Add feature" not "Added feature"

---

## 🌿 Branching Strategy

### Simple Flow (Solo/Small Team)
```
main ──────────────────────────────────
       └── feature-x ──┘
```

- Work on `main` or short-lived feature branches
- Merge/push frequently

### Git Flow (Team/Production)
```
main ─────────────────────────────────────────
  └── develop ────────────────────────────────
        ├── feature/add-watermark ──┤
        └── feature/batch-resize ───┘
```

---

## 🔧 Workflow Process

### 1. Before Coding
```bash
git status                    # Check status
git pull origin main          # Get latest code
```

### 2. During Coding
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

## ⚠️ Edge Cases & Solutions

### 1. Push Rejected (Remote has new commits)
```
! [rejected] main -> main (fetch first)
error: failed to push some refs
```

**Solution:**
```bash
git pull --rebase origin main    # Preferred: rebase local commits
git push origin main
```

Or:
```bash
git pull origin main             # Merge remote changes
git push origin main
```

---

### 2. Conflict on Pull/Merge
```
CONFLICT (content): Merge conflict in main.py
```

**Solution:**
1. Open conflicted file, look for markers:
```python
<<<<<<< HEAD
your_code()
=======
their_code()
>>>>>>> origin/main
```

2. Choose correct code, remove markers
3. Stage and commit:
```bash
git add main.py
git commit -m "fix: Resolve merge conflict in main.py"
```

---

### 3. Committed Wrong File (Not Pushed)
```bash
git reset --soft HEAD~1          # Undo commit, keep changes staged
git reset HEAD <file>            # Unstage file
git commit -m "correct message"  # Commit again
```

---

### 4. Wrong Commit Message (Not Pushed)
```bash
git commit --amend -m "feat: Correct message"
```

---

### 5. Pushed Wrong Commit
> ⚠️ **Be careful with force push on shared branches!**

```bash
git revert HEAD                  # Create new commit reverting changes
git push origin main
```

---

### 6. Ignore Tracked File
```bash
# Add to .gitignore
echo "file_to_ignore.txt" >> .gitignore

# Remove from git but keep local
git rm --cached file_to_ignore.txt
git commit -m "chore: Stop tracking file_to_ignore.txt"
```

---

### 7. Large File Rejected
```
remote: error: File xyz.exe is 123.00 MB; this exceeds the file size limit
```

**Solution:**
1. Add to `.gitignore`:
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

Or use BFG Repo-Cleaner (faster):
```bash
bfg --delete-files "*.exe"
git push --force
```

---

### 8. View Commit History
```bash
git log --oneline -10            # 10 latest commits, one line
git log --graph --oneline        # With branch graph
git log --author="name"          # By author
git log -- path/to/file          # By specific file
```

---

### 9. Revert to Old Version
```bash
# View file at old commit (no changes made)
git show abc123:path/to/file.py

# Checkout file from old commit
git checkout abc123 -- path/to/file.py

# Reset entire project (⚠️ dangerous)
git reset --hard abc123
```

---

## 📝 Quick Reference Commands

| Situation        | Command                           |
| ---------------- | --------------------------------- |
| Check status     | `git status`                      |
| View diff        | `git diff`                        |
| Stage all        | `git add -A`                      |
| Commit           | `git commit -m "msg"`             |
| Push             | `git push origin main`            |
| Pull             | `git pull origin main`            |
| View log         | `git log --oneline -5`            |
| Undo last commit | `git reset --soft HEAD~1`         |
| Amend message    | `git commit --amend -m "new msg"` |
| Discard changes  | `git checkout -- file.py`         |
| Create branch    | `git checkout -b feature-x`       |
| Switch branch    | `git checkout main`               |
| Merge branch     | `git merge feature-x`             |
| Delete branch    | `git branch -d feature-x`         |

---

## 🤖 Antigravity Integration

When Antigravity performs git operations, it will:

1. **Verify before commit**: `git status` to check staged files
2. **Use semantic commits**: Type + description according to convention
3. **No force push** unless requested by user
4. **Ask user** when encountering conflicts or edge cases

### Good Request Examples:
- "Commit and push with message 'feat: Add excel merge'"
- "Create branch feature/add-watermark and push"
- "Show 5 latest commits"

### Clarification Needed Examples:
- "Undo commit" → "Has the commit been pushed? If no use reset, if yes use revert"
- "Reset all" → "Do you want soft reset (keep changes) or hard reset (lose changes)?"

---

## 🤖 Agentic Protocol

### Skill Metadata
- **Version**: 1.0.0
- **Last Updated**: 2026-01-27

### 1. Activation Log
When activating this skill, print:
"🎯 [SKILL ACTIVATED] git-workflow v1.0.0"
"📋 Parameters:"
"   - Action: [commit|push|pull|rebase]"
"   - Branch: [branch_name]"
"   - Message: [commit_message_preview]"

### 2. User Confirmation
Before pushing or destructive actions:
"I'll execute 'git [command]' on branch '[branch]'. Proceed? [Y/n]"

### 3. Completion Log
- Success: "✅ [git-workflow] Git operation successful. Hash: [short_hash]"
- Error: "❌ [git-workflow] Git Error: [output_tail]"

