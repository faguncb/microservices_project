# Cursor AI Usage Guide

## How to Prevent Cursor AI from Automatically Committing Code

Cursor AI is a powerful coding assistant, but you should maintain control over your git commits. Here's how to prevent unwanted commits:

---

## 1. Cursor Settings Configuration

### Disable Auto-commit (if available)
1. Open Cursor
2. Go to **Cursor Settings** (Cmd/Ctrl + ,)
3. Search for "git" or "commit"
4. Ensure any auto-commit features are **disabled**

### Privacy & Safety Settings
1. In Cursor Settings, check the "Privacy" section
2. Review what data Cursor can access
3. Consider disabling automatic code indexing for sensitive projects

---

## 2. Use .cursorignore File

This project includes a `.cursorignore` file that tells Cursor to ignore certain files:

```
# Ignore Python cache
__pycache__/
*.pyc

# Ignore environment files
.env
.venv/
venv/

# Ignore build artifacts
build/
dist/
*.egg-info/
```

You can add more patterns as needed.

---

## 3. Manual Git Workflow (Recommended)

**Always use manual git commands** instead of relying on AI:

```bash
# 1. Check what changed
git status

# 2. Review the changes
git diff

# 3. Add only specific files you want to commit
git add product_service.py
git add products_data.json

# 4. Commit with a meaningful message
git commit -m "Add feature X: description of changes"

# 5. Push to remote (only when ready)
git push origin main
```

---

## 4. Best Practices When Using Cursor AI

### ✅ DO:
- **Review all AI suggestions** before accepting
- **Read generated code** to understand what it does
- **Test changes** before committing
- **Use git diff** to see exactly what changed
- **Commit frequently** with small, logical changes
- **Write your own commit messages** (don't let AI do it)

### ❌ DON'T:
- Don't blindly accept all AI suggestions
- Don't let AI commit code without your review
- Don't commit without testing
- Don't push to main/master without reviewing changes
- Don't commit sensitive data (API keys, passwords, etc.)

---

## 5. Git Hooks for Extra Protection

You can add a pre-commit hook to review changes:

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "===================="
echo "PRE-COMMIT CHECK"
echo "===================="
echo "Files to be committed:"
git diff --cached --name-only
echo ""
echo "Please review the changes above."
read -p "Continue with commit? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Commit aborted."
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## 6. Working with Cursor AI Safely

### When Asking AI to Make Changes:

1. **Be specific**: "Add a function to validate email addresses"
2. **Review the diff**: Check what files were changed
3. **Test the changes**: Run your tests and manually verify
4. **Stage selectively**: Only add files you've reviewed

### If AI Makes Unwanted Changes:

```bash
# Undo unstaged changes to a file
git restore product_service.py

# Undo staged changes
git restore --staged product_service.py

# Discard all local changes (careful!)
git reset --hard HEAD
```

---

## 7. Project-Specific Settings

This project includes:

- **`.gitignore`** - Prevents cache files, virtual environments from being committed
- **`.cursorignore`** - Tells Cursor to ignore certain directories
- **`products_data.json`** - Separate data file (easy to track changes)

---

## 8. Checklist Before Every Commit

- [ ] Run `git status` to see what changed
- [ ] Run `git diff` to review the actual changes
- [ ] Test the code locally
- [ ] Run tests if available (`python -m unittest test_product_service.py`)
- [ ] Stage only the files you want (`git add <specific-file>`)
- [ ] Write a clear commit message
- [ ] Review one more time before pushing

---

## 9. Emergency: Undo a Commit

### If you committed but haven't pushed:
```bash
# Undo the last commit but keep changes
git reset --soft HEAD~1

# Undo the last commit and discard changes
git reset --hard HEAD~1
```

### If you already pushed:
```bash
# Create a new commit that undoes the previous one
git revert HEAD
git push
```

---

## Summary

**Key Principle**: YOU are in control, not the AI.

- Always review changes manually
- Use explicit git commands
- Test before committing
- Never commit without understanding what changed

Cursor AI is a tool to help you code faster, but **you** make the final decisions about what goes into your repository.

