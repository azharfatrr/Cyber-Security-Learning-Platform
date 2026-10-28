# Module 29 Illustrated Runtime Pilot

## Goal

Turn the existing module 29 Android-components guide into a clear, screenshot-led walkthrough and test whether its provider-access exercise works on an Android emulator. The guide must report observed behavior, not treat source findings as proof of runtime impact.

## Current context

- This repository publishes MkDocs documentation; it does not contain the BugBazaar app source.
- `docs/29-components.md` is based on inspection of BugBazaar revision `fef6a899a684245eb70b2ab4be926f62be849ed9` and currently labels runtime behavior unverified.
- The user wants to reuse an existing emulator. At design time, this session's `adb devices -l` showed no attached device; the existing `RootAVD34` emulator is now online as Android 14/API 34.
- GitHub publishes `BugBazaar_v1.2.1.apk`; the official v1.2.1 release points to the same commit pinned by this project (`fef6a899a684245eb70b2ab4be926f62be849ed9`). The user wants students to download this prebuilt APK rather than build it.
- Runtime source inspection shows the address screen is gated by local session state. The built-in login validates locally; a login creates an on-device random session token and asks for a local four-digit passcode. The module guide should explain this setup and deny unrelated permission prompts.
- The linked Android Security Masterclass example provides a useful instructional model: baseline, ordered steps, exact commands, expected observations, screenshots, evidence criteria, hints, and explanation. Its screenshots or unobserved results will not be copied into this project.

## Scope

In scope:

1. Inspect the pinned BugBazaar source and available device environment before writing runtime claims.
2. Verify and install the official v1.2.1 release APK that matches the pinned revision, only after confirming the existing emulator is visible to ADB. Students must not need to build the app. Do not create, wipe, or reset an emulator.
3. Establish a synthetic address fixture and test the provider from an ordinary unprivileged caller app. An ADB shell command alone is not sufficient evidence of cross-app access because the shell has a different identity.
4. If no suitable caller app already exists, create the smallest local test fixture needed, outside `docs/` and not included in the published site.
5. Add a module 29 guide section that explains how to download the verified prebuilt APK, install it to the existing emulator, and verify the package/hash.
6. Capture screenshots from the actual run, update `docs/29-components.md`, and add the screenshots under a module-specific `docs/images/` directory.
7. Run the repository's site tests and strict MkDocs build.

Out of scope:

- Expanding or runtime-testing the other nine labs.
- Testing upstream Firebase or any other cloud service.
- Using real contacts, accounts, or personal data.
- Copying screenshots or inventing expected outputs from the reference tutorial.
- Clearing app data, uninstalling existing apps, resetting the emulator, or deleting data not created for this pilot.
- Claiming an exploit or a successful lab unless the ordinary-app caller test demonstrates the documented result.

## Intended workflow

1. Check ADB device visibility and identify the connected emulator and Android version. Stop runtime testing if no appropriate device is available; continue only with source inspection and clearly labeled unverified material until it is available.
2. Inspect the pinned BugBazaar manifest, provider implementation, build configuration, and any existing test fixtures. Identify how the application can create a synthetic address without disturbing existing state.
3. Download the official v1.2.1 APK, verify its release-to-source revision, SHA-256, package/version, and provider metadata, then inspect installed package state before installation. Do not overwrite or clear existing app state without explicit permission.
4. Invoke the provider from a separate ordinary app caller and record the caller identity, URI/operation, result, Android version, and app revision. Use only the synthetic record created for the pilot. Report access denied, partial behavior, build failure, and other deviations as observed.
5. Capture a small set of legible screenshots showing the relevant app state and actual command/result evidence. Redact any incidental personal information; do not include secrets or unrelated emulator content.
6. Revise the guide so each step includes prerequisites, action, expected observation grounded in the run, troubleshooting, evidence, and cleanup. Keep any unverified step explicitly labeled.
7. Add tested APK download/install instructions to module 29, including the official pinned release URL, SHA-256 verification, `adb install`, package verification, safe first-run procedure that avoids the app's external APK download, local-only demo login/passcode, and airplane-mode test setup.
8. Verify image references and run `python3 -m unittest -v test_site` plus `python3 -m mkdocs build --strict`.

## Documentation and fixture boundaries

- Primary content change: `docs/29-components.md`.
- The module 29 guide owns the target-specific prebuilt APK download/install steps; keep shared setup general unless a concrete reusable setup correction is needed.
- Runtime screenshots: `docs/images/lab-29/` (create only images captured during this pilot).
- Any necessary ordinary-app caller fixture stays outside `docs/` and is not deployed to GitHub Pages.
- Update `test_site.py` only if a focused assertion is needed to prevent the new guide's screenshot/content wiring from regressing.
- Do not alter the existing common setup or other lab pages unless a concrete dependency for this pilot requires it.
- Do not redistribute the third-party APK in this repository; link to the official release and provide its verified hash.

## Safety and state handling

- Reuse the user's existing emulator; never factory-reset it or clear/uninstall existing app data as part of this work.
- Use a newly created synthetic address with a unique marker. Remove only that record if it can be safely identified and an agreed cleanup path exists; otherwise leave it intact and document cleanup for the user.
- Do not initiate cloud/database features or send test traffic to upstream services. If the app requires an external service for this local exercise, stop and report the dependency rather than redirecting traffic to an unapproved target.
- Keep the test local and read-only against the provider where possible. Any write operation requires a separate reason and an isolated synthetic record.

## Acceptance criteria

- The guide's runtime status reflects what was actually tested.
- A successful cross-app finding is supported by an ordinary unprivileged app caller, not solely by an ADB shell result.
- Steps, commands, expected observations, and screenshots correspond to the observed run and identify pinned app/device context.
- Any test helper is outside the published site and does not broaden the lab to real or cloud data.
- The strict MkDocs build and site test suite pass. If emulator/build prerequisites prevent runtime testing, the guide clearly remains unverified and the blocker is reported; no runtime-success claim is made.
