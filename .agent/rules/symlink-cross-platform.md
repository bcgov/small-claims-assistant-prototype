---
description: Cross-platform symlink creation rules for Windows/macOS/Linux compatibility. Prevent hardlink trap and broken file symlinks.
globs: ["plugins/**/scripts/*.py", "plugins/**/skills/*/scripts/*"]
---

## 🔗 Cross-Platform Symlink Creation Rules

**Context:** Git symlinks behave differently across platforms. Hardlinks and plain-text file stand-ins silently break workflows when switching between Windows and macOS/Linux.

### Non-Negotiables

1. **Always Use Real Symlinks, Never Hardlinks**
   - Real symlinks commit to Git as symlink objects (`ln -s target link`)
   - Hardlinks commit as regular files and break cross-platform workflows
   - Plain-text file stand-ins (Git fallback on Windows with `core.symlinks=false`) are NOT acceptable for committed code
   - Use `/link-checker:symlink-manager` skill to diagnose and fix broken links

2. **Windows Prerequisites (Must Do First)**
   - Enable Developer Mode: Settings → System → For Developers → toggle ON
   - Set git config: `git config core.symlinks true`
   - This allows unprivileged symlink creation without admin elevation
   - Without this, Git checks out symlinks as plain-text files — automatic failure

3. **How to Create Symlinks Correctly**
   - **Interactive (Recommended):** Use the `/link-checker:symlink-manager` skill command `/create-sym-link`
     ```
     /create-sym-link
     ```
     Prompts for source and destination, validates, creates proper symlink, suggests commit message
   
   - **Manual (When `/create-sym-link` unavailable):** Use real `ln -s` command
     ```bash
     cd destination-directory
     ln -s relative/path/to/source link-name
     ```

4. **Validation After Creation**
   - Verify with: `ls -la <link>` should show `-> <target>` (symlink arrow)
   - NOT a regular file with link count > 1 (that's a hardlink)
   - NOT a plain-text file containing the target path
   - Run symlink-manager audit: `python ./scripts/symlink_manager.py audit`

5. **If You Find Hardlinks or Plain-Text Files**
   - These MUST be replaced with real symlinks
   - Delete: `rm <hardlink-path>`
   - Recreate: Use `/create-sym-link` command or `ln -s` after enabling Developer Mode
   - Commit: Git will now see them as symlink objects, not files
   - Verify: `git show <commit>` should show symlink marker, not file contents

6. **Committing Symlinks**
   - `git add <symlink>` stages the symlink object
   - `git commit -m "feat: add symlink <name> for cross-platform compatibility"`
   - On macOS: symlink always works
   - On Windows: symlink works ONLY if Developer Mode is enabled + `git config core.symlinks true`
   - On Linux: symlink always works

7. **When Pulling / After `git reset --hard`**
   - If symlinks break (become plain-text files), restore them:
     ```bash
     python ./scripts/symlink_manager.py restore
     ```
   - If `symlinks.json` exists, it contains the manifest for all links in the repo
   - Run this after fresh clone on Windows to recreate links correctly

### Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ls -la` shows hardlink (link count > 1) | Created without Developer Mode or with hardlink fallback | Delete, enable Developer Mode, use `ln -s` |
| `ls -la` shows regular file with path contents | Git checked out as `core.symlinks=false` | `git config core.symlinks true`, `git reset --hard`, use `/create-sym-link` |
| `ls -la` shows `L` prefix (broken link) | Target doesn't exist or wrong relative path | Fix target path or delete and recreate |
| Symlink works on macOS but not Windows | Windows has `core.symlinks=false` or no Developer Mode | Enable Dev Mode, set git config, re-create |

### Examples

**❌ WRONG — Hardlink (fails cross-platform):**
```bash
cp source.py dest.py  # or hardlink via fallback
ls -la dest.py        # shows "-rw-r--r--  3  user  ..." (link count = 3)
# Commits as regular file, breaks on macOS
```

**✅ RIGHT — Real Symlink (works everywhere):**
```bash
ln -s ../../../scripts/source.py dest.py
ls -la dest.py        # shows "lrwxr-xr-x  -> ../../../scripts/source.py"
git add dest.py
git commit -m "feat: add symlink to shared script"
# Commits as symlink object, works on all platforms
```

**✅ BEST — Using `/create-sym-link` Command:**
```
/create-sym-link
# Interactive prompts guide you through validation and creation
# Handles relative paths, validates targets, suggests commit message
```
