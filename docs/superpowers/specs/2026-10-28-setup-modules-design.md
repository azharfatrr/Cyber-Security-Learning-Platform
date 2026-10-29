# Setup modules and objective-focused labs

**Status:** Approved for implementation  
**Date:** 2026-10-28

## Purpose

Separate environment preparation from the ten learning exercises. Learners should be able to prepare the selected target once, then use lab guides that focus on their security objective and link to setup instructions instead of repeating installation steps.

## Agreed constraints

- Use prebuilt application APKs; learners do not build Devom or BugBazaar from source.
- Make Devom's manual Python backend setup the primary path. Keep Docker as an optional alternative.
- Keep shared safety and tooling prerequisites separate from target-specific setup.
- Make setup pages visually scannable: use real, relevant screenshots only when available; otherwise make command-driven instructions polished and easy to follow.
- Prepare BugBazaar's prebuilt Module 29 caller APK in BugBazaar setup. It is a separate ordinary app needed to demonstrate cross-app provider access; learners install the provided APK and do not build it.
- Labs retain exercise-specific preparation and evidence, but link to setup modules for environment and app installation.
- Preserve the existing pilot's claims and limitations, including its use of only the synthetic Module 29 record.
- Preserve the user's pending removal of `test_site.py` and its CI invocation. Do not run tests.

## Information architecture

Add a **Setup** navigation group before **Labs**, with these entries:

1. **Common prerequisites** — retain `docs/00-common-setup.md`, narrowing it to shared isolation, emulator/ADB and command-line prerequisites, and safety guidance. It links to the target-specific setup pages.
2. **Devom setup** — add `docs/01-devom-setup.md`.
3. **BugBazaar setup** — add `docs/02-bugbazaar-setup.md`.

The **Labs** group and existing lab URLs remain unchanged. The existing home-page setup button and notice link to Common prerequisites, which directs learners to the setup module for their selected target. `docs/lab-structure.md` will describe this shared-prerequisite plus target-setup pattern.

## Setup module responsibilities

### Common prerequisites

Describe the disposable, isolated lab environment; synthetic-data and network-safety requirements; shared ADB and command-line tools; and how to select the target setup module. Avoid prescribing app-specific setup here. Do not require Android Studio or Docker merely to install the prebuilt apps.

### Devom setup

Document the pinned Devom revision, the included prebuilt `Dvom.apk`, and a manual Python backend setup using the pinned checkout's `server.py` and `requirements.txt` as the primary route. Include the app-to-backend configuration and lab-only credentials where appropriate. Present Docker Compose as an optional alternative, not the default.

The pinned server runs in debug mode, listens on all interfaces, and enables ad-hoc TLS for both manual and Docker launches. Make isolation and host firewall requirements prominent, and do not expose it to public or corporate networks. Correct the current Common setup's stale HTTP scheme, and explain that the generated certificate may require environment-specific trust handling; do not tell learners to disable certificate checks globally. Clearly distinguish source-inspected instructions from runtime-verified setup; do not claim the manual path has been piloted unless it is actually validated. Retain the relevant Devom revision and behavior caveats currently in Common setup.

### BugBazaar setup

Use the official prebuilt BugBazaar `v1.2.1` release tied to the documented source revision, and retain its expected APK SHA-256 and embedded-version caveat. Do not direct learners to build from source or require Android Studio for installation.

Include the offline/network-isolation and first-launch downloader safeguards currently needed before launching the app. Include the instructor-supplied prebuilt Module 29 caller APK, its expected SHA-256, and safe verification/install guidance. Treat the caller as a separate APK/package/UID; do not publish it with the site or instruct learners to compile it. Preserve fail-closed guidance for checksum mismatches and unknown existing emulator state.

Make installation steps easy to scan with concise step headings, titled command blocks, and clear expected-result notes. Use screenshots only for actual, relevant setup states; the existing Module 29 exercise screenshots remain with that lab.

## Lab and landing-page changes

- Update every lab's opening/setup reference to link to Common prerequisites and the relevant target setup: Devom for Labs 09, 10, 14, 24, 25, 26, and 28; BugBazaar for Labs 27, 29, and 30.
- Keep lab-specific accounts, scenario data, safety limits, exercise steps, interpretation, evidence, and cleanup in the lab pages.
- In Lab 29, remove target/caller download and installation, APK checksum/install verification, first-run guard setup, and general emulator network-isolation instructions after they are documented in BugBazaar setup. Replace them with a concise readiness check and links to both setup pages. Keep creation/reuse of the synthetic address, the read-only query from the distinct caller, result interpretation, evidence, and cleanup in Lab 29.
- Clarify in Lab 29 that an ADB shell query is not a substitute for an ordinary-app query. The caller APK setup requirement remains because its distinct UID is essential to the stated cross-app learning objective.
- Update `docs/lab-structure.md` to say app installation belongs in target setup modules, while lab pages retain only exercise-specific prerequisites.
- Update the home-page setup CTA and notice so learners can reach shared prerequisites and then the appropriate target setup.

## Acceptance criteria

1. MkDocs navigation shows Setup (Common prerequisites, Devom setup, BugBazaar setup) before Labs.
2. Common prerequisites no longer contain Devom or BugBazaar installation procedures and clearly route learners to each target setup.
3. Devom setup presents the manual Python backend as primary and Docker as optional, uses the pinned prebuilt APK, and prominently explains debug mode, all-interface binding, ad-hoc TLS, and the isolation/certificate-trust risks.
4. BugBazaar setup uses the verified prebuilt target APK and covers the prebuilt caller APK; neither setup instructs learners to compile the target app.
5. Setup instructions use relevant real screenshots when available, and otherwise present command-driven steps in titled blocks with clear success cues; no exercise screenshot is repurposed as installation evidence.
6. Every lab links to Common prerequisites and its target setup without changing its learning objective or exercise-specific findings.
7. Lab 29 assumes target and caller installation is complete, but retains the synthetic-record cross-app exercise and its evidence limitations.
8. Home-page and lab-structure guidance reflect the new separation, and a strict MkDocs build succeeds. Do not run the removed unit-test suite.

## Scope boundaries and risks

This change reorganizes setup documentation; it does not validate either app's setup end-to-end, make the blocked cloud database exercise runnable, alter app artifacts, or broaden Lab 29's claims. Devom's manual server exposure and unpinned Python dependencies remain operational risks to communicate, not to silently fix as part of the documentation restructure. The instructor must supply the caller APK separately; its absence from the published site is intentional.
