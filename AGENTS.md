# Immune Frontline project instructions

The user wants this game to remain a turn-based microbiology teaching game with continuous idle animation. Time, infection, tissue damage and cell abilities advance only after a player command. Biological signals must change the cells they activate/recruit rather than function as generic direct damage. Keep three selectable cell families and understandable feedback for new medical clerks.

## Project source and publishing

- Edit `outputs/immune-frontline.html`; it is the standalone canonical source. Drafts in `work/` are not the source of truth.
- The user authorizes publishing game changes to `sces5504/immune-frontline` on GitHub and updating its GitHub Pages site after completing a requested change.
- Only game files, version backups, checks, documentation and deployment configuration should be tracked/published. Keep unrelated presentations and personal files excluded.
- Use `request_permissions` for network access before diagnosing GitHub authentication. An API DNS failure in the sandbox does not mean the user's token is invalid. Request `.git` write access when required.
- Do not change or reauthenticate the user's credentials unless a real authentication failure is established after network access is available.

## Required version backups (user instruction)

- Before changing the game, verify the current published source has an exact immutable backup in `outputs/versions/manifest.json`. If not, create one before editing.
- Every completed user-facing change receives a new semantic version and standalone snapshot. Set the embedded version, then run `python3 scripts/release.py --version X.Y.Z --title '...' --notes '...'`.
- Never edit or delete earlier snapshots, alter their hashes, reuse an existing version number, overwrite a Git tag, force-push or reset away release history.
- The release script creates the snapshot, manifest and playable archive index. The Pages build verifies every archived hash and publishes all versions.
- Commit the new source, new snapshot, manifest/index and associated changes. Add a matching `vX.Y.Z` Git tag and push `main` plus the new tag. Confirm the Pages workflow succeeds.
- To restore an older source, copy its snapshot into the current source and publish a new version; preserve all prior history. The user can also dispatch the Pages workflow with an existing version number to temporarily deploy that backup without changing source/history.
- Run the meaningful gameplay checks with `node scripts/check_game.cjs` (use the bundled workspace Node runtime if system Node is broken). Changes to gameplay should preserve winnable starter teams for all mission/difficulty combinations, real failure paths and the idle-state invariants.
