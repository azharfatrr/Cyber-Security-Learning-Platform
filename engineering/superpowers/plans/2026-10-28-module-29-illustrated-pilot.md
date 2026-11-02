# Module 29 Illustrated Runtime Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn module 29 into a screenshot-led walkthrough grounded in a real ordinary-app caller test on the user's existing Android emulator.

**Architecture:** Use the official BugBazaar v1.2.1 release APK only after verifying that its release points to the revision pinned by the guide. Verify provider access from a separate app UID, using a small local caller fixture only if no suitable app exists; keep the fixture outside the published docs. Students download and install the APK with a short command and do not build it. Use only synthetic data, capture actual emulator evidence, and wire the guide and images into the existing MkDocs build.

**Tech Stack:** MkDocs 1.6.1, Material for MkDocs 9.7.7, Python `unittest`, Android SDK/ADB, Java, and the pinned BugBazaar Android/Gradle toolchain.

**Spec:** `engineering/superpowers/specs/2026-10-28-module-29-illustrated-pilot-design.md`

## Global Constraints

- Reuse the user's existing emulator; never factory-reset it or clear/uninstall existing app data as part of this work.
- Use a newly created synthetic address with a unique marker. Remove only that record if it can be safely identified and an agreed cleanup path exists; otherwise leave it intact and document cleanup for the user.
- Do not initiate cloud/database features or send test traffic to upstream services. If the app requires an external service for this local exercise, stop and report the dependency rather than redirecting traffic to an unapproved target.
- Keep the test local and read-only against the provider where possible. Any write operation requires a separate reason and an isolated synthetic record.
- Use BugBazaar revision `fef6a899a684245eb70b2ab4be926f62be849ed9`.
- Use the official `v1.2.1` APK release only if its tag is verified to point at the pinned source revision; publish a download link and SHA-256, not a copy of the APK.

## Review Focus

- **No ADB-visible emulator:** do not install or claim runtime validation; report the blocker and leave runtime status unverified (Task 1).
- **APK/revision mismatch:** do not install an artifact unless its release is verified against the pinned source revision (Task 2).
- **Existing installed app or data:** inspect package state first; do not replace, uninstall, or clear it (Task 2).
- **ADB shell identity:** require the query to run from an ordinary caller app before documenting cross-app access (Task 3).
- **Android version or provider behavior differs from source expectation:** record the actual version, caller, URI, and response; document the observed result, not the expected vulnerability (Tasks 3–4).

---

### Task 1: Preflight the existing emulator and pinned target

**Files:**
- Read: `docs/29-components.md`
- Read: pinned BugBazaar source at `fef6a899a684245eb70b2ab4be926f62be849ed9`

**Interfaces:**
- Produces: verified provider authority/path, exported and permission settings, package/build identifiers, safe way to create one synthetic address, and the available emulator/API version.
- Consumes: the module 29 design spec and the existing emulator/SDK supplied by the user.

- [x] **Step 1: Locate the existing SDK/emulator and inspect ADB visibility**

Run `adb devices -l`. If no device is attached, inspect the already-installed SDK and its AVD list; do not create an AVD or wipe one. Use an existing suitable AVD if available and bring it online without resetting it.

Expected: one identified emulator serial is in `device` state. If none is available, stop runtime testing and record that the guide remains runtime-unverified.

- [x] **Step 2: Check the device context without changing it**

Run `adb -s <serial> shell getprop ro.build.version.release`, `adb -s <serial> shell getprop ro.build.version.sdk`, and `adb -s <serial> shell pm path com.BugBazaar`.

Expected: record Android version/API level and whether BugBazaar is already installed. Do not clear or uninstall any package.

- [x] **Step 3: Inspect the pinned BugBazaar source**

Use an existing checkout only if `git rev-parse HEAD` equals the pinned revision; otherwise check out the pinned revision in `/tmp/opencode/bugbazaar-module29`. Read the manifest, provider implementation, app build files, and README/setup instructions. Record the exact provider URI and the supported, non-destructive synthetic-data setup. Also inspect launch-time network behavior before starting the app.

Expected: source facts are tied to the exact revision. If no safe local setup avoids real or cloud data, stop and report that prerequisite. In this pinned build, the dashboard's first-run path downloads an APK from GitHub; do not start that path.

---

### Task 2: Download and install the target without disturbing existing state

**Files:**
- Download outside this repository: `/tmp/opencode/BugBazaar_v1.2.1-fef6a89-verified.apk`

**Interfaces:**
- Consumes: Task 1's pinned source facts, emulator serial/API, and existing package state.
- Produces: a verified official APK matching the pinned revision, installed only if doing so will not replace an existing app or data.

- [x] **Step 1: Download and verify the official prebuilt APK**

Download `https://github.com/payatu/BugBazaar/releases/download/v1.2.1/BugBazaar_v1.2.1.apk`. Verify the release tag `v1.2.1` points to `fef6a899a684245eb70b2ab4be926f62be849ed9`, compute the downloaded file's SHA-256, and inspect its package/version/provider metadata with Android SDK tools.

Expected: the official release commit matches the pinned revision, the file is an APK for `com.BugBazaar`, and its provider metadata matches the inspected source. Record the exact hash. Do not use the repository's older v1.1 APK.

- [x] **Step 2: Inspect the destination package before install**

Re-check `adb -s <serial> shell pm path com.BugBazaar`. If absent, install the verified release APK with `adb -s <serial> install /tmp/opencode/BugBazaar_v1.2.1-fef6a89.apk`. If present, verify its version/build identity; do not replace it or clear its data unless the existing installation is already the pinned build and installation is unnecessary.

Expected: the installed package is `com.BugBazaar`, internal version name `1.0` (official release tag `v1.2.1`), from the pinned release, or installation is skipped and a mismatch is reported.

- [x] **Step 3: Suppress the first-run external downloader before launching the app**

The pinned dashboard checks `MyAppPreferences.isFirstRun` and, when true, starts a GitHub APK download. Before launching the fresh debug install, use `run-as com.BugBazaar` to create `shared_prefs/MyAppPreferences.xml` with `isFirstRun=false`, then read it back to verify. Do not open the app if this local setting cannot be verified.

Expected: the preference reads `false` before app launch, preventing the first-run downloader without making a network request or changing upstream code.

- [x] **Step 4: Create one synthetic address without touching existing records**

The `Address` screen is gated by the app's local demo login. Use its built-in local credentials, create an arbitrary synthetic four-digit app passcode, and deny unrelated SMS/storage permission prompts. Enable airplane mode before launch so target startup and the exercise cannot reach upstream services. Then add one uniquely marked synthetic address through the UI; the address screen writes to its local database and broadcasts only a local address-update event. Do not use real contact data, provider writes, cloud setup, or app-data clearing to seed it.

Expected: the app visibly contains the unique synthetic record, with enough information to identify it for later cleanup, while airplane mode remains enabled. If this cannot be done safely, stop before the provider test.

---

### Task 3: Verify provider access from an ordinary app caller

**Files:**
- Create only if needed: `engineering/fixtures/module-29-caller/` (minimal standalone caller app)
- Build/test against the user's existing emulator

**Interfaces:**
- Consumes: Task 1's exact URI and Task 2's installed app plus synthetic record.
- Produces: actual caller package/UID, provider query result, device/API context, and screenshots from the run.

- [x] **Step 1: Check for an existing suitable ordinary-app caller**

Inspect local test tooling and installed test apps. Do not use `adb shell content query` as proof of third-party access.

Expected: either identify an ordinary app caller suitable for the exact provider URI or proceed to the local fixture step.

- [x] **Step 2: Add a minimal read-only caller fixture only if required**

Create `engineering/fixtures/module-29-caller/` with a launchable Android activity that queries only the source-confirmed provider URI and displays the caller package plus result. Use the target's compatible SDK/Gradle versions, request no permissions, accept no arbitrary URI/input, and do not write or delete provider data.

Expected: the fixture builds and runs under its own application UID and displays the single synthetic result or an explicit denial/error.

- [x] **Step 3: Invoke the provider and record actual behavior**

Run the read-only query as the ordinary caller. Record the caller package/UID, exact URI, operation, Android version/API, app revision, and result. Capture a terminal or app screenshot showing the real result; include no unrelated emulator content.

Expected: the observed result is reproducible from the recorded state. Access is documented only if the ordinary app receives the synthetic row; a shell-only result is not sufficient.

- [x] **Step 4: Preserve unrelated emulator state**

Remove only the uniquely marked synthetic row if a verified safe cleanup route exists. Do not uninstall apps, clear app data, or delete any pre-existing record.

Expected: unrelated app state is untouched; if the synthetic record cannot be safely removed, record its marker and cleanup steps for the user.

---

### Task 4: Add a site regression test and write the illustrated guide

**Files:**
- Test/modify: `test_site.py`
- Modify: `docs/29-components.md`
- Create: `docs/images/lab-29/` with screenshots captured in Task 3

**Interfaces:**
- Consumes: Task 3's verified steps and actual observations (or its explicit blocker status).
- Produces: a screenshot-led guide and a regression test that verifies its images are present in the generated site.

- [x] **Step 1: Add `test_module_29_screenshots_are_copied_into_site` to `test_site.py`**

Build MkDocs into a temporary directory, inspect the generated module 29 HTML for image references under `images/lab-29/`, assert at least one such reference exists, and assert each referenced file exists in the generated output.

- [x] **Step 2: Run the focused test before updating the guide/assets**

Run: `python3 -m unittest -v test_site.SiteTest.test_module_29_screenshots_are_copied_into_site`

Expected: FAIL because the new module 29 screenshots/references have not yet been added.

- [x] **Step 3: Rewrite only `docs/29-components.md` around the observed pilot**

Keep the project's common structure, and add a target-install section with the official prebuilt APK download URL, pinned release/source revision, verified SHA-256, `adb install`, package verification, and pre-launch first-run download guard. Do not require students to build the APK or install Android Studio/CMake/NDK. Also add ordered baseline/setup/validation steps, exact tested commands, observed outputs, troubleshooting, finding criteria, evidence, and cleanup. Embed legible screenshots next to the steps they illustrate with descriptive alt text. Mark any step not exercised as unverified; do not assert cross-app exposure if the ordinary caller was denied.

- [x] **Step 4: Run the focused screenshot regression test again**

Run: `python3 -m unittest -v test_site.SiteTest.test_module_29_screenshots_are_copied_into_site`

Expected: PASS; every module 29 image reference resolves in the generated site.

---

### Task 5: Verify the complete site and review the change

**Files:**
- Verify: `test_site.py`, `docs/29-components.md`, `docs/images/lab-29/`

**Interfaces:**
- Consumes: Task 4's guide, screenshots, and test.
- Produces: verified site build and a concise report of runtime outcome and any remaining limitations.

- [x] **Step 1: Run the full site test suite**

Run: `python3 -m unittest -v test_site`

Expected: all tests pass. If `mkdocs-material` is missing from the active Python environment, install `requirements.txt` in the project environment and rerun; do not treat the missing theme as a content defect.

- [x] **Step 2: Run a strict MkDocs build**

Run: `python3 -m mkdocs build --strict`

Expected: build exits 0 with no warnings, and module 29 screenshots appear in the generated site.

- [x] **Step 3: Review the final diff for evidence fidelity and scope**

Check that only module 29, its screenshots, the focused site regression test, and any necessary non-published caller fixture changed. Confirm no secrets, real data, unverified claims, unrelated files, APKs, or upstream source copies were added.

- [ ] **Step 4: Commit the completed pilot**

Commit the guide, real screenshots, test, and any needed caller fixture with a message such as `Document tested module 29 walkthrough`.
