# PARADOX III — Installation

This ZIP is an overlay for the existing `EthicalMaster/EthicalMaster` profile repository. It includes all assets, source code and workflow. It does not delete your old ORIGIN files. Your current branch should be `main` with a clean working tree. Back up the current version before extracting.

```powershell
cd "$HOME\Downloads\EthicalMaster"
git status
git pull --ff-only origin main
git branch backup/paradox-v2
Expand-Archive -Path "$HOME\Downloads\ethical-paradox-v3.zip" -DestinationPath "." -Force
git add README.md STATIC.md APPLY.md assets tools .github/workflows/paradox-contributions.yml
git diff --cached --stat
git commit -m "feat: complete PARADOX III exhibition"
git push origin main
```

If the branch already exists, choose another backup name. Stop if the pull or any Git command fails. If another contribution workflow from v2 was activated, disable it to avoid competing updates. GitHub may require authentication with workflow-file permissions to push the new workflow. Do not share credentials.

## Activate activity artwork

Open the repository's **Actions** tab. Select **PARADOX — refresh contribution landscape**, then **Run workflow** on `main`. The workflow also runs every Monday at 03:23 UTC. If required, enable Actions and allow the workflow to write repository contents in Settings → Actions → General. No personal access token is needed by the workflow. The job uses the built-in scoped token; it may be denied by account/repository policies or GraphQL availability. If it fails, the existing artwork remains in place; inspect the run logs. The displayed data is the calendar visible to this token, which can differ from your personal view. No fabricated counts are displayed. The initial panel is explicitly marked awaiting data. The native GitHub graph stays authoritative.

## Artwork regeneration

The shipped assets work without Python. To regenerate locally, use Python 3.11+, install `tools/requirements.txt`, and set `PARADOX_FONT_DIR` to a directory containing InterDisplay-Black.otf and InterDisplay-Regular.otf, and `PARADOX_MONO_FONT` to a DejaVu Sans Mono TTF if your environment differs from the renderer defaults. Font files are not included.

```powershell
python -m pip install -r tools/requirements.txt
python tools/render.py
python tools/render_exhibition.py
```

The original hero and project GIFs loop continuously. The new exhibition panels play once (approximately 3.84 seconds). The static edition uses PNGs plus an unanimated contribution SVG. GitHub's native README renderer has no built-in animation pause control; the standalone preview provides one. No web-hosted animation dependencies, generated fake metrics or extra service accounts are required.
