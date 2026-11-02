# Single LabKit Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Give learners one verified LabKit download for all ten labs and publish a follow-up site release with the missing production gates in place.

**Architecture:** Store APK inputs outside MkDocs' published `docs/` tree. A deterministic builder creates one Linux x86_64 archive under the generated site assets; the archive includes all APKs, lab-owned scripts/config/fixtures, a checksum manifest, and a setup bootstrap that fetches pinned project dependencies. Move the lab authoring contract to `engineering/`, then add license/404, CI validation, hosted branch protection, and visual QA before merging through a PR.

**Tech Stack:** Python 3 standard library for archive construction and local-link checks, Bash bootstrap, Firebase CLI/npm lock, existing unittest/MkDocs, Playwright + axe-core for accessibility and visual QA, GitHub Actions/Pages.

**Spec:** `docs/superpowers/specs/2026-11-02-single-labkit-release-design.md`

## Global Constraints

- The learner manually downloads one `LabKit-linux-x86_64.zip` for all ten labs.
- Require Linux x86_64, Bash, Python, Git, curl, Node/npm, Java, ADB, and an already installed disposable Android 14/API 34 x86_64 emulator; do not bundle an Android SDK/emulator image.
- Preserve the verified APK bytes and their hashes; keep inputs outside the published MkDocs source tree.
- Bootstrap only pinned sources/dependencies from documented upstream hosts; runtime lab traffic remains restricted as documented.
- Do not package Devom source; bootstrap fetches the pinned upstream revision automatically.
- Do not include separate APK links on the public site or expose `lab-structure` in the built site.
- Do not commit generated `site/` output or the generated LabKit zip.
- Keep synthetic data, host-loopback binding, local Firebase rules, and all existing lab safety boundaries.
- Merge and deploy the follow-up through a PR; no force push or deletion of unrelated branches/worktrees.

## Review Focus

- Missing/changed APK input: builder and manifest tests must fail closed on a missing file or digest mismatch.
- Unsafe archive paths or duplicate members: builder tests must reject traversal, duplicate paths, and untracked payload files.
- Unsupported host or absent prerequisite: bootstrap preflight must stop before installing or changing device state.
- External dependency drift: bootstrap must use pinned versions and hashes and must not perform remote requests during lab runtime.
- Broken MkDocs references after moving the authoring guide or APKs: built-site link/asset check must report zero local failures.

## File Map

- Move `docs/assets/apk/*.apk` to `labkit/input/apk/`; these are private build inputs, not standalone published downloads.
- Create `labkit/build.py`, `labkit/manifest.sha256`, `labkit/README.md`, `labkit/setup.sh`, and a `labkit/payload/` source tree for scripts, fixtures, rules, and the Lab 30 hook.
- Create `scripts/check_site_links.py` and `engineering/qa/package.json`, lockfile, and `accessibility_audit.mjs` for CI validation.
- Move `docs/lab-structure.md` to `engineering/qa/lab-structure.md`; update the read-through record.
- Modify `test_site.py`, `.gitignore`, `mkdocs.yml`, `README.md`, `PUBLISHING.txt`, downloads/setup/lab pages, `NOTICE`, and `.github/workflows/deploy.yml`.
- Create root `LICENSE`, `docs/404.md`, and `engineering/qa/release-readiness.md` with real visual QA results and screenshot paths.

---

### Task 1: Build and verify the one-download LabKit

**Files:**
- Move: `docs/assets/apk/*.apk` to `labkit/input/apk/`
- Create: `labkit/build.py`, `labkit/manifest.sha256`, `labkit/README.md`, `labkit/payload/`
- Modify: `test_site.py`, `.gitignore`

**Interfaces:** `python3 labkit/build.py --output docs/assets/labkit/LabKit-linux-x86_64.zip` builds the generated archive. `python3 labkit/build.py --check <archive>` validates its exact members, paths, and SHA-256 manifest. The output path is ignored by Git and consumed by MkDocs/CI.

- [x] Add failing tests for expected archive name/member list, exact APK hashes, deterministic bytes across two builds, and archive traversal/duplicate rejection.
- [x] Run `python3 -m unittest -v test_site`; confirm the new tests fail for missing builder/artifact contract.
- [x] Move APK inputs outside `docs/` without changing bytes and implement deterministic archive/manifest generation with safe relative paths.
- [x] Build the archive; run builder check and `sha256sum` against the existing four documented digests.
- [x] Run the full unit suite and `git diff --check`.

### Task 2: Add the LabKit bootstrap and make setup consume it

**Files:**
- Create: `labkit/setup.sh`, pinned dependency/version metadata, bundled Lab 27 config/fixtures/scripts, Lab 30 hook file
- Modify: `docs/00-common-setup.md`, `docs/01-devom-setup.md`, `docs/02-bugbazaar-setup.md`, `docs/27-cloud-database.md`, `docs/29-components.md`, `docs/30-runtime-bypass.md`, `engineering/lab27/README.md`
- Test: `test_site.py` and bootstrap preflight checks

**Interfaces:** `./setup.sh --check` performs read-only OS/tool/device preflight; `./setup.sh` verifies the archive manifest and provisions pinned project dependencies under the extracted kit workspace. `./lab27/reset.sh` remains the Lab 27 lifecycle interface after setup.

- [x] Add failing tests for setup preflight, clear missing-prerequisite failures, kit-relative APK paths, and absence of manual `git clone`/`npm install` instructions on the learner path.
- [x] Run the focused tests and confirm failure before implementation.
- [x] Implement fail-closed Linux x86_64 preflight and idempotent bootstrap; pin Devom checkout revision and Python dependency constraints, Firebase CLI lock, Frida client/server, and JADX downloads with verified hashes.
- [x] Build the kit, extract it into a clean temporary directory, run `./setup.sh --check`, then perform the bootstrap in a temporary extracted kit; ADB was read-only and no apps were installed.
- [x] Verify all ten setup guides consume kit-relative assets and Lab 27 runs from bundled config without a repository checkout or a manual CLI installation.
- [x] Run unit tests, Lab 27 reset/seed/start/stop checks, and the existing APK hash checks.

### Task 3: Make the public site expose one download and hide authoring material

**Files:**
- Move: `docs/lab-structure.md` to `engineering/qa/lab-structure.md`
- Create: `docs/404.md`, root `LICENSE`
- Modify: `mkdocs.yml`, `docs/downloads.md`, `README.md`, `PUBLISHING.txt`, `NOTICE`, `engineering/qa/read-through.md`, `test_site.py`

- [x] Add failing tests that assert exactly one LabKit archive download CTA, no individual APK links, no public lab-structure navigation/page, and correct license/404 source.
- [x] Run focused tests and confirm failure.
- [x] Move authoring guidance out of the publishing tree; update internal references; add the project-owned MIT license and custom 404.
- [x] Replace individual download links with the LabKit link and included-file/hash inventory; record the user's confirmed separate public educational APK authorization without calling third-party APKs MIT-licensed.
- [x] Build the archive before MkDocs; build with `--strict` and verify `site/404.html`, no lab-structure output, one LabKit archive, and zero individual APK URLs.
- [x] Run full unit tests and local link checks.

### Task 4: Add pull-request, link, and accessibility gates

**Files:**
- Create: `scripts/check_site_links.py`, `engineering/qa/package.json`, lockfile, `engineering/qa/accessibility_audit.mjs`
- Modify: `.github/workflows/deploy.yml`, `test_site.py`, `PUBLISHING.txt`

- [x] Add failing tests for internal links/assets, fragments, generated LabKit presence, PR trigger, deploy-only-on-main behavior, and required validation jobs.
- [x] Run focused tests and observe the expected failure.
- [x] Implement local rendered-site link/asset checking with external URLs reported but not fetched.
- [x] Implement axe-core audit of each built HTML page; fail on serious/critical findings and save a machine-readable report.
- [x] Update CI to run on pull requests and pushes to main: build LabKit, run unit tests, strict MkDocs, local-link checks, then accessibility audit; deploy only on a successful main push.
- [x] Run the full CI-equivalent command sequence locally and confirm zero broken local links and zero serious/critical accessibility findings.

### Task 5: Complete visual QA and release through protected main

**Files:**
- Create: `engineering/qa/release-readiness.md` and dark-theme QA screenshots
- Modify: repository `main` protection settings (GitHub), as needed after the validation context names are confirmed

- [x] Serve the built site and inspect every published page at desktop width in dark theme; exercise search, theme toggle, each hints disclosure, and code-copy controls.
- [x] Save screenshots and record page-by-page status, viewport, date, browser, interactions, and findings in the QA report.
- [x] Confirm the successful LabKit archive and checksum are the ones linked by the built site.
- [x] Configure `main` to require PRs and the successful validation status; verify the actual GitHub API state before creating/merging the PR.
- [ ] Push the feature branch, open a PR, wait for all required gates, merge without bypassing protection, and verify the main deployment run.
- [ ] Fetch the public Pages home, Lab Downloads, LabKit asset, custom 404 behavior, and compare deployed SHA-256 with the report; ensure the generated zip and `site/` remain untracked.

## Final verification

- `python3 -m unittest -v test_site`
- Build LabKit from a clean checkout, run its manifest verifier, and verify the four original APK hashes.
- `.venv/bin/python -m mkdocs build --strict` after LabKit generation.
- `python3 scripts/check_site_links.py site`
- `npm ci --prefix engineering/qa && npx playwright install chromium && node engineering/qa/accessibility_audit.mjs site`
- Verify protected-main required-check state, passing PR workflow, successful post-merge Pages deployment, public archive download/hash, and clean Git status.
