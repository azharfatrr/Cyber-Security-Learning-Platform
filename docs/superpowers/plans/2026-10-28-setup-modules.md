# Setup Modules Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move target installation into setup modules and keep the ten lab guides focused on their exercise objectives.

**Architecture:** Keep `00-common-setup.md` as shared prerequisites, add one setup page per target, and put the three pages under a Setup navigation group before Labs. Link each lab and the home page to the appropriate setup pages; move Lab 29's app installation safeguards into BugBazaar setup while retaining the synthetic-record cross-app exercise in the lab.

**Tech Stack:** Markdown, MkDocs Material navigation, existing Bash/ADB instructions.

**Spec:** `docs/superpowers/specs/2026-10-28-setup-modules-design.md`

## Global Constraints

- Learners use prebuilt application APKs and do not build Devom or BugBazaar from source.
- Devom's manual Python backend setup is the primary path; Docker is optional.
- Shared prerequisites remain separate from target-specific setup.
- BugBazaar setup covers the separate instructor-supplied, prebuilt Module 29 caller APK; learners do not build it.
- Setup pages use real, relevant screenshots only if available; otherwise use titled, scannable command blocks with clear success cues.
- Preserve the Module 29 synthetic-record scope and evidence limitations.
- Preserve the pending removal of `test_site.py` and its CI invocation. Do not run tests.

## Review Focus

- **Setup links and nav:** pages exist at every new link and Setup precedes Labs; verify through the strict MkDocs build and inspect navigation.
- **App artifact integrity:** preserve BugBazaar and caller APK hashes, revisions, and embedded version caveat exactly; compare against the current Lab 29 source during review.
- **Devom exposure and transport:** manual/Docker instructions state debug mode, all-interface binding, ad-hoc TLS, isolation requirements, and certificate-trust uncertainty; inspect the final section before commit.
- **Setup visuals:** no existing image is an installation screenshot; keep Module 29 images with that lab and style command-based setup steps with titled code blocks.
- **Lab 29 scope:** setup extraction does not remove marker handling, distinct-UID proof, query limits, or cleanup caveats; compare the retained walkthrough with the spec.
- **Lab objective focus:** every numbered lab links to Common prerequisites and its target setup without moving scenario-specific preparation out of the lab; inspect all ten opening sections.

---

### Task 1: Create target setup modules and update setup entry points

**Files:**
- Modify: `docs/00-common-setup.md`
- Create: `docs/01-devom-setup.md`
- Create: `docs/02-bugbazaar-setup.md`
- Modify: `mkdocs.yml`
- Modify: `docs/index.md`

**Interfaces:**
- Produces the setup page paths and navigation labels consumed by the lab pages: `00-common-setup.md` (Common prerequisites), `01-devom-setup.md` (Devom setup), and `02-bugbazaar-setup.md` (BugBazaar setup).

- [ ] **Step 1: Narrow Common setup to shared prerequisites**

Keep the disposable environment, shared safety, emulator/ADB, command-line tool and licensing guidance in `docs/00-common-setup.md`. Remove the Devom and BugBazaar installation procedures, and add direct links to both target setup pages. Do not make Docker or Android Studio a universal prerequisite for installing prebuilt APKs.

- [ ] **Step 2: Add the Devom setup page**

Create `docs/01-devom-setup.md` with the pinned revision, included prebuilt `Dvom.apk`, manual Python backend setup as the primary path, app/backend URL configuration, lab credentials and source-derived caveats. State prominently that the pinned server runs in debug mode, listens on all interfaces, and uses ad-hoc TLS for manual and Docker launches; require an isolated disposable host and firewall controls. Correct the current HTTP scheme to HTTPS, note that certificate trust and app connectivity are environment-specific and unverified, and do not advise disabling certificate checks globally. Present command-driven installation in titled, clearly labeled blocks with concise success cues. Keep Docker Compose as an optional path and do not label either path runtime-verified.

- [ ] **Step 3: Add the BugBazaar setup page**

Create `docs/02-bugbazaar-setup.md` with the official prebuilt `v1.2.1` asset, pinned source revision, target APK SHA-256, embedded app version caveat, offline/network-isolation checks, and the first-run downloader guard. Add the instructor-supplied prebuilt caller APK verification and installation steps, preserving caller SHA-256 `eedfec951335a8ed876241d86bc9e6c53a7dff4833b98fa522f8cbfc1168900e`. Keep fail-closed behavior for mismatches and unknown existing state. Use titled, scannable command blocks and clear success cues; do not present existing exercise captures as installation screenshots. Do not publish the APK or instruct students to build it.

- [ ] **Step 4: Add the Setup navigation group and update the home links**

In `mkdocs.yml`, place Setup before Labs and list Common prerequisites, Devom setup, then BugBazaar setup. In `docs/index.md`, direct the setup CTA and notice to Common prerequisites, and make clear that learners should continue to the target setup for their chosen lab.

- [ ] **Step 5: Review setup content and commit Task 1**

Inspect the new pages against the current `docs/00-common-setup.md` and `docs/29-components.md`; verify all revisions and hashes are unchanged and no target-build instructions were introduced. Stage and commit only the Task 1 files.

---

### Task 2: Refocus lab setup references and extract Module 29 installation

**Files:**
- Modify: `docs/lab-structure.md`
- Modify: `docs/09-jwt-account-state.md`
- Modify: `docs/10-otp-bypass.md`
- Modify: `docs/14-command-injection.md`
- Modify: `docs/24-file-upload.md`
- Modify: `docs/25-path-traversal.md`
- Modify: `docs/26-transactions.md`
- Modify: `docs/27-cloud-database.md`
- Modify: `docs/28-bola.md`
- Modify: `docs/29-components.md`
- Modify: `docs/30-runtime-bypass.md`

**Interfaces:**
- Consumes the setup page paths established in Task 1.
- Produces opening setup references that send Labs 09, 10, 14, 24, 25, 26, and 28 to Devom setup; and Labs 27, 29, and 30 to BugBazaar setup.

- [ ] **Step 1: Update the lab-structure guidance**

Change `docs/lab-structure.md` to distinguish shared prerequisites and target installation from lab-specific prerequisites. State that lab guides link to setup pages rather than repeat app installation.

- [ ] **Step 2: Add target setup links to all lab openings**

Update the opening setup references in Labs 09, 10, 14, 24, 25, 26, 27, 28, and 30 to link to both Common prerequisites and the appropriate target setup. Keep all existing scenario-specific accounts, markers, authorization requirements, and caveats in place.

- [ ] **Step 3: Move Lab 29 installation readiness into BugBazaar setup**

In `docs/29-components.md`, replace general emulator network isolation, target APK download/checksum/install, first-run guard, and caller APK checksum/install instructions with a concise readiness check and links to Common prerequisites and BugBazaar setup. Retain synthetic address creation/reuse, the distinct ordinary caller query, evidence, interpretation, troubleshooting, and cleanup. Explicitly preserve the warning that an ADB shell query is not proof of ordinary-app access.

- [ ] **Step 4: Review all ten lab openings and commit Task 2**

Check that each lab links to Common prerequisites and exactly its target setup; ensure Lab 29 still explains the caller APK's distinct UID and makes no broader data-exposure claim. Stage and commit only Task 2 files.

---

### Task 3: Validate, review, and publish the documentation restructure

**Files:**
- Review: all Task 1 and Task 2 files.
- Preserve: `.github/workflows/deploy.yml` and deletion of `test_site.py` as already pending user-requested changes.

**Interfaces:**
- Consumes the complete setup navigation and lab links from Tasks 1 and 2.
- Produces a strict MkDocs build and a manually reviewed documentation change ready to publish.

- [ ] **Step 1: Run the strict site build (not the test suite)**

Run: `python -m mkdocs build --strict`

Expected: successful site build with no missing-page or strict-mode warnings. Do not invoke `unittest`, `test_site.py`, or other tests.

- [ ] **Step 2: Manually audit scope and references**

Review the generated navigation and the source diff. Confirm there are no stale references to app installation in lab openings, all ten labs point to the correct setup module, the exact APK hashes/revisions remain intact, and user-requested test removal remains untouched.

- [ ] **Step 3: Commit the remaining requested user change if still uncommitted**

If `.github/workflows/deploy.yml` and `test_site.py` remain modified/deleted and are confirmed as the earlier user-requested test removal, stage only those two paths and commit them separately from documentation changes.

- [ ] **Step 4: Push the completed commits to `main`**

Inspect the remote and current `main` first. Publish the completed task commits to `main` without force-pushing or overwriting remote work. If remote `main` has advanced incompatibly or the push is rejected, stop and report the specific blocker rather than rewriting remote history.
