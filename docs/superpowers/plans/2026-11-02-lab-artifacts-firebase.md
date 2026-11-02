# Lab Artifacts and Firebase Emulator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Provide four verified repository-hosted APKs and make Lab 27 reproducible against a permanent local Firebase Emulator Suite with synthetic data.

**Architecture:** Verify provenance and redistribution facts before adding binaries. Build a separate Lab 27 variant from the pinned BugBazaar source, configure it for a committed local emulator/fixture setup, and verify the complete app-to-emulator exercise before publishing its hash and instructions.

**Tech Stack:** Android Gradle build, pinned BugBazaar source, Firebase Emulator Suite, Git LFS status to be checked, SHA-256 utilities, MkDocs Markdown.

**Spec:** `docs/superpowers/specs/2026-11-02-production-ready-lab-site-design.md`

## Global Constraints

- Use disposable, isolated environments only; no public or corporate exposure.
- Restrict network egress to the exact paths required by the documented exercise; Firebase for Lab 27 is local emulator traffic only.
- Use synthetic data only, including deterministic Lab 27 fixtures.
- Preserve redaction of tokens, keys, service-account material, personal data, and unrelated device content.
- The four APKs are official BugBazaar v1.2.1 unchanged, Devom's `Dvom.apk`, the module-29 caller, and the new repo-built Lab 27 APK.
- Store all four APKs under `docs/assets/apk/`; do not send learners to external download sites.
- Do not publish guessed hashes, unverified provenance, or unverified redistribution claims.
- The Lab 27 APK must be built from the pinned BugBazaar source and must not contact upstream Firebase.
- Implementation must happen in a new branch/worktree based on the branch containing the approved spec.

## Review Focus

- Upstream APK differs from the named version/revision or hash: verify artifact identity before mirroring; reject mismatches.
- Redistribution terms are unclear: do not mirror until the source/license facts are established.
- Emulator host routing differs between Android emulator and host OS: verify the exact endpoint from the app and runtime traffic; do not guess.
- Emulator reset leaves non-deterministic documents/accounts: compare a reset run to the committed synthetic baseline.
- Firebase SDK/build configuration cannot target the emulator without changing the lab scenario: stop after documented attempts and report the exact failure and smallest unblock input.

---

## File map

- Create `docs/assets/apk/` files for all four mirrored/distributable APKs.
- Create `engineering/lab27/firebase.json` and only the emulator/rules/fixture files the verified source and Firebase CLI require.
- Create or modify the pinned BugBazaar source/build configuration only in a clearly isolated Lab 27 build fixture; retain an auditable source revision and build command.
- Create `engineering/lab27/README.md` for maintainer-level reproducibility if the learner-facing guide needs a shorter version.
- Update `docs/02-bugbazaar-setup.md`, `docs/01-devom-setup.md`, and add `docs/downloads.md` with repo-local artifact paths and verified SHA-256 values.
- Add verified artifact provenance and licensing entries in root `NOTICE` (shared with publication plan).

## Interfaces

- Produces four APKs, their verified SHA-256 values, provenance/licensing facts, and a runnable Lab 27 emulator fixture for the learner-content and release-QA plans.
- Learner docs consume the exact filenames, local paths, app IDs/versions, emulator identifiers/ports, commands, and outputs established by these tasks; no value is invented ahead of verification.

### Task 1: Verify the four APK sources and distribution facts

**Files:**
- Inspect: `docs/assets/apk/module-29-caller.apk`
- Inspect/modify: `engineering/references.md`, `docs/01-devom-setup.md`, `docs/02-bugbazaar-setup.md`
- Create later: `docs/downloads.md`, `NOTICE`

- [ ] **Step 1: Record current repository artifact identity**

Run `sha256sum docs/assets/apk/module-29-caller.apk` and inspect its package/version/signature metadata with the available Android SDK tools. Record observed values in the working provenance notes; do not yet edit learner-facing hashes.

- [ ] **Step 2: Verify upstream source and version for each requested artifact**

For BugBazaar official v1.2.1 and Devom `Dvom.apk`, identify the canonical upstream release/source URL, version/revision and applicable license/redistribution statement. For the caller APK, trace the checked-in fixture source and build provenance. Save source URLs and source revision/release evidence.

- [ ] **Step 3: Compare local and upstream artifact checksums**

Download only from verified upstream sources in a temporary location, compute SHA-256, inspect package/version, and compare. Confirm official BugBazaar v1.2.1 is byte-for-byte identical to its official release. If any source or license cannot be verified, do not mirror that file and stop this task for a precise report.

- [ ] **Step 4: Stage verified files under `docs/assets/apk/`**

Use stable descriptive filenames; keep the official BugBazaar file unchanged. Recompute every staged hash and compare against the verified source hash.

- [ ] **Step 5: Verify staged artifacts**

Run `sha256sum docs/assets/apk/*.apk` and inspect package/version metadata for all four. Expected: exactly the four intended APKs, with each file matching its recorded source identity and checksum.

### Task 2: Build the Lab 27 APK against a local Firebase emulator

**Files:**
- Create: `engineering/lab27/` emulator configuration, rules, deterministic synthetic seed/fixture and build instructions
- Create: `docs/assets/apk/bugbazaar-lab27-emulator.apk`
- Modify: isolated BugBazaar source/build configuration at the pinned revision, if required

**Interfaces:** Consumes the pinned BugBazaar source revision and emulator configuration. Produces one installable app whose Firebase endpoint is the documented local emulator and whose synthetic fixture starts from a known baseline.

- [ ] **Step 1: Inspect the pinned app's Firebase integration and build requirements**

Record the source revision, Firebase product(s), initialization/configuration path, security rules/queries used by the Lab 27 scenario, Android SDK/Gradle/JDK requirements, and any hard-coded upstream project identifiers. Confirm no source is modified yet.

- [ ] **Step 2: Create a deterministic Firebase Emulator Suite configuration**

Add the minimum `engineering/lab27/` config, local-only rules and synthetic fixture. Pin Firebase CLI/tool versions using the repository's chosen reproducible mechanism. Use stable local identifiers and explicit port bindings that are not exposed beyond the disposable lab environment.

- [ ] **Step 3: Start the emulator and verify the synthetic baseline**

Run the committed start procedure. Verify the emulator reports ready, the configured synthetic documents/rules are present, and no cloud project is contacted. Record actual output. Run the reset procedure and repeat the baseline check.

- [ ] **Step 4: Configure the Lab 27 build for the emulator**

Make the smallest isolated build-variant/configuration change needed to point the app at the local emulator. Preserve the pinned source behavior and lab scenario. Search the resulting build configuration and APK for upstream project endpoints; any remaining endpoint that can receive Firebase traffic must be removed or cause a stop/report.

- [ ] **Step 5: Build and verify the Lab 27 APK**

Run the recorded build command from a clean build state. Install on a disposable Android emulator, verify package/version, and verify app-to-Firebase traffic reaches only the local emulator. Run the Lab 27 baseline and lower-privilege scenario, capture observed output, then stop and reset the suite and confirm baseline restoration.

- [ ] **Step 6: Record the APK hash and build provenance**

Copy the verified APK to `docs/assets/apk/bugbazaar-lab27-emulator.apk`, run `sha256sum`, and record the exact source revision, build command/tool versions, and artifact hash. Do not use a prior or generated hash before the final APK is in place.

- [ ] **Step 7: Verify documented emulator lifecycle procedures**

Run the final start, stop, and reset commands from a clean state and capture their actual output. Verify reset restores the known synthetic baseline and stop leaves no emulator process/listener running.

- [ ] **Step 8: Apply the prescribed stop condition if needed**

After documented attempts, if the pinned Android build cannot work, Firebase Emulator Suite cannot run, or the app cannot target it without invalidating the scenario, stop Lab 27 implementation and report attempts, exact errors/output, and the smallest unblock input. Do not substitute an externally supplied Firebase environment.

### Task 3: Publish verified download and attribution details

**Files:**
- Create: `docs/downloads.md`
- Create/update: `NOTICE`
- Modify: `docs/01-devom-setup.md`, `docs/02-bugbazaar-setup.md`

- [ ] **Step 1: Write the downloads table from verified artifact records**

List each file, repository-relative download link, SHA-256, upstream source/version/revision and verified attribution/license facts. Do not include any external download CTA.

- [ ] **Step 2: Switch setup guides to repo-local artifacts**

Replace learner download locations with links to the files under `docs/assets/apk/`. Preserve or add complete SHA-256 verification commands using the exact verified hashes. Keep target setup responsibilities in setup pages and link to the downloads page.

- [ ] **Step 3: Add third-party NOTICE entries**

Identify upstream owners and verified terms for each mirrored APK, distinguish project-built artifact from upstream binaries, and state that the repository MIT license does not relicense third-party binaries.

- [ ] **Step 4: Verify all download references and hashes**

Run the repo's existing content tests and `sha256sum -c` against a manifest or explicit recorded values. Expected: all four links resolve to committed APKs and every computed digest matches the downloads page and provenance record.

## Final verification

- Run `python3 -m unittest -v test_site` and `python3 -m mkdocs build --strict` after artifact/download page changes.
- Recompute hashes from the final staged/committed APK bytes and verify values match `docs/downloads.md` and `NOTICE` provenance.
- Save fresh app/emulator run output for the final QA plan; stale evidence does not count.
