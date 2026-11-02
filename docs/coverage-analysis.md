# Android intermediate class: coverage and readiness analysis

**Analysis date:** 28 October 2026  
**Scope:** The ten gray modules (9, 10, 14, 24–30), their existing employee guides, Devom, and BugBazaar.  
**Method:** Static inspection of selected upstream source and configuration at the pinned revisions below, followed by the isolated test runs recorded on each lab page. The static review itself did not perform APK execution, Docker deployment, proxy interception, or end-to-end exploitation. Source evidence supports the scenario descriptions; the lab pages record what the test runs observed.

## Executive assessment

Devom is the stronger foundation for the selected backend and API scenarios: its server source contains direct candidates for seven modules. BugBazaar is the stronger candidate for Android components and local runtime manipulation. The cloud module is now served by a repository-built BugBazaar variant and a committed local Firebase Storage emulator with synthetic fixtures, verified end to end on 2 November 2026.

**Verification status (2 November 2026):** All ten labs were re-executed end to end in isolated environments, and their guides include observed output and fresh screenshots. Lab 27 used the local Firebase Storage emulator; the other nine used the pinned Devom or BugBazaar targets described on their pages. The assessment below records the original static review and is kept for traceability; each lab page states what its test run observed.

**At the time of this static review, the ten guides were challenge briefs rather than tested walkthroughs.** They lacked verified device setup, expected outputs, lab preparations, time estimates, reproducible reset procedures and answer keys. The guides have since been expanded and tested as recorded above. Module 27 now has a committed local emulator and a verified app connection; Modules 29 and 30 have tested build and runtime steps.

## Sources and versions

- Devom revision [`af4290ce8d2178765bfc2bd96cf233f6d3d03161`](https://github.com/memohk/Devom/tree/af4290ce8d2178765bfc2bd96cf233f6d3d03161): [server.py](https://github.com/memohk/Devom/blob/af4290ce8d2178765bfc2bd96cf233f6d3d03161/server.py), [admin_routes.py](https://github.com/memohk/Devom/blob/af4290ce8d2178765bfc2bd96cf233f6d3d03161/admin_routes.py), [Compose](https://github.com/memohk/Devom/blob/af4290ce8d2178765bfc2bd96cf233f6d3d03161/docker-compose.yml), [Dockerfile](https://github.com/memohk/Devom/blob/af4290ce8d2178765bfc2bd96cf233f6d3d03161/Dockerfile), and requirements.
- BugBazaar revision [`fef6a899a684245eb70b2ab4be926f62be849ed9`](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9): [manifest](https://github.com/payatu/BugBazaar/blob/fef6a899a684245eb70b2ab4be926f62be849ed9/app/src/main/AndroidManifest.xml), [AddressContentProvider.java](https://github.com/payatu/BugBazaar/blob/fef6a899a684245eb70b2ab4be926f62be849ed9/app/src/main/java/com/BugBazaar/ui/addresses/AddressContentProvider.java), [PasscodeActivity.java](https://github.com/payatu/BugBazaar/blob/fef6a899a684245eb70b2ab4be926f62be849ed9/app/src/main/java/com/BugBazaar/ui/PasscodeActivity.java), [Signin.java](https://github.com/payatu/BugBazaar/blob/fef6a899a684245eb70b2ab4be926f62be849ed9/app/src/main/java/com/BugBazaar/ui/Signin.java), build files and README.

**Evidence labels:** “Source-backed” means the relevant logic is visible in inspected source and, where a lab page says so, was exercised in the test run. “Claim only” means the project advertises a scenario but the specific implementation and environment were not part of the test runs.

## Module-by-module assessment

The “Verification points” and “Guide gap” lines below record the checks the static review identified. The lab pages record the tested results and how each gap was addressed.

### 9 — JWT-based account state bypass: Devom, source-backed

- `/login` derives `locked` from database status, generates a token and returns it even for a blocked account. `validate_jwt` verifies the HS256 signature and then checks the token's `locked` claim; it does not consult current database status. The signing key is initialized by Compose, and `admin_routes.py` provides an authenticated user-status update.
- There are two distinct tests: a previously issued token after the account is blocked tests stale state, while a newly issued blocked token modified and re-signed tests trust in a signed claim and key compromise. Rewriting an unsigned payload alone is not sufficient.
- **Verification points:** disposable account, establish active baseline, record old token, block account, confirm old and new token behavior, restore state. Verify whether APK flow permits the intended setup and whether JWT expiry affects results.
- **Guide gap:** explicitly distinguish both approaches and avoid implying a signature can be bypassed. The existing guide does not yet specify setup of a dedicated account or reliable reset.

### 10 — OTP authentication logic: Devom, source-backed

- `/login` returns `session_token` before OTP verification and includes `debug_token`. `/verify_login_2fa` accepts either a fixed value or the pending code. The `token_required` decorator checks the token but not OTP completion.
- These are separate findings: disclosure, predictable/fixed bypass, and protected access without an OTP-bound session. A successful OTP response alone does not demonstrate a protected session.
- **Verification points:** demonstrate login-issued token against `/profile/<id>` before verification, compare invalid and accepted OTP, and establish which condition the Android client actually uses.
- **Guide gap:** require a time-ordered sequence and ensure students do not mistake an isolated `success` response for authenticated access.

### 14 — Command injection via file input: Devom, source-backed

- `/upload_profile_pic` builds a filename from the user ID and submitted filename, saves the upload, then interpolates the filename into an `echo` command executed with `shell=True`; `server_debug` exposes output.
- **Verification points:** verify that the exact multipart filename survives client, proxy, Werkzeug and filesystem handling, and that the harmless output marker appears. The file must save successfully before the command runs.
- **Constraint:** command execution occurs in the service container, which has bind mounts; containment is therefore essential. Use only a benign marker with no network calls, file modification or unrelated host access.
- **Guide gap:** specify a validated benign test and what output counts as success; the lab page now records that output.

### 24 — Unrestricted file upload: Devom, source-backed

- `/upload_profile_pic` saves provided file contents without an apparent extension, content or authorization check; `/view_upload` serves paths from uploads. This supports a validation and access-control exercise, not a claim of uploaded code execution.
- **Verification points:** compare a real image with a small harmless non-image file; verify actual content retrieved, response headers, and whether expected ownership checks exist.
- **Guide gap:** distinguish “stored despite unsuitable type” from executable upload, and ensure all comparisons use synthetic content.

### 25 — Server-side path traversal: Devom, source-backed

- `/download_pdf/<path:filename>` and `/view_upload/<path:filename>` use `send_file(os.path.join(UPLOAD_FOLDER, filename))` without an explicit canonical containment check. Whether a traversal reaches the route depends on the HTTP client, URL normalization and the deployment stack.
- **Verification points:** create a uniquely marked harmless file inside the disposable container, outside uploads; confirm normal retrieval and marker-only traversal, including exact raw request behavior.
- **Guide gap:** define marker provisioning and cleanup in the lab material; a source-code observation alone does not prove an HTTP exploit works.

### 26 — Insufficient transaction validation: Devom, source-backed

- `/transfer` checks a token but directly uses supplied `from_id`, `to_id`, and `amount` in balance updates and creates a transaction without apparent amount, source ownership or sufficient-funds validation. Negative amounts and a mismatched sender are separate issues.
- **Verification points:** two known test users with measured initial balances, one normal transaction, then one controlled invalid-value test. Verify the two balances and stored transaction, not just the response. Prefer a fresh dataset per participant.
- **Guide gap:** define account provisioning and isolation; note that the two seed accounts include an administrative demo user and should not be assumed suitable for multi-user training without lab preparation.

### 27 — Cloud storage misconfiguration: BugBazaar local emulator, source-backed and verified

- BugBazaar's README lists misconfigured Firebase Firestore, and the repository contains `app/google-services.json` and Firebase dependencies. The pinned source, however, implements Firebase **Storage**, not Firestore: `MyProfile` uploads `<device-name>/userinfo.txt` through `FirebaseStorage`. The exercise was therefore designed around the Storage flow, not the README wording.
- The upstream configuration points at a project the training organization does not own. It is never used as a target.
- **Environment built:** a separate `com.BugBazaar.lab27` variant from the same pinned source, configured for the local Firebase Storage emulator at `127.0.0.1:9199` through the Android host alias `10.0.2.2`. The committed fixture contains a project ID, bucket, deliberately permissive Storage rule, and synthetic seed objects; `engineering/lab27/` rebuilds and runs it.
- **Guide status:** verified end to end on 2 November 2026. The app wrote `Google sdk_gphone64_x86_64/userinfo.txt`, and an unauthenticated read returned the saved synthetic profile. Never use the upstream Firebase configuration as a target merely because it appears in source.

### 28 — Broken object-level authorization: Devom, source-backed

- `/profile/<user_id>` requires a valid token but fetches the requested user ID without comparing it to the token subject. The returned user row includes sensitive fields, so evidence must be sanitized even for synthetic records.
- **Verification points:** create two authorized disposable users; capture account A's request for its own profile, then request B's profile using A's same token. Verify identity and response body; compare against an expected denial.
- **Guide gap:** provide a second lab user, and redact secrets and lab passwords from artifacts.

### 29 — Unauthorized Android components: BugBazaar, source-backed candidate

- The manifest declares `AddressContentProvider` exported with authority `com.bugbazaar.provider.addresses` and no explicit permission. Its `query` and `insert` methods access the address database. This is a concrete candidate but accessibility and impact must be checked on an actual Android build.
- Other exported components exist; export alone does not prove a vulnerability. ADB shell's identity and privileges differ from a normal third-party app, so a second, ordinary app is preferable to establish cross-app impact.
- **Verification points:** build/install, seed a synthetic address, verify access from a separate unprivileged test app, record baseline and result, and evaluate Android version effects.
- **Guide gap:** select and document one verified component and establish a reproducible synthetic fixture and non-shell caller.

### 30 — Client-side login bypass through runtime manipulation: BugBazaar, source-backed candidate

- `PasscodeActivity` compares the entered value against `UserAuthSave.getpasscode()` in the button click listener; a match opens `NavigationDrawer_Dashboard`, while a mismatch displays an error. This supports investigation of a local passcode gate, not proof of bypassing remote authentication.
- `Signin.java` has navigation paths that can reach the dashboard independently; therefore dashboard visibility alone is not conclusive evidence that instrumentation changed the PIN check. Prove the instrumented code path against an incorrect-PIN baseline and distinguish other navigation routes.
- **Verification points:** establish a logged-in state and PIN, reproduce rejection, verify process and Frida compatibility, demonstrate the changed local branch and rule out alternate navigation.
- **Guide gap:** clarify that this is a local app passcode bypass and specify a reliable branch-level success criterion after testing.

## Cross-cutting environment findings

1. **Network exposure:** Devom's `server.py` binds to `0.0.0.0:8080`, runs in debug mode, and enables ad-hoc TLS. Compose publishes container port 8080 on host port 8443 on all host interfaces by default. Bind Compose to loopback and verify host firewall rules; emulator networking differs by emulator and operating system.
2. **Persistence and separation:** Compose bind-mounts database, uploaded files, keys and templates and names the container `dvom-lab-v1`. Shared instances can collide or leak changes across participants. Provide separate disposable environments or controlled unique copies and cleanup; do not delete existing user data.
3. **Encryption affects observation:** Devom's middleware accepts JSON and normally encrypts JSON responses, except when the User-Agent contains `Postman` or the path is exempt. App traffic may need separate handling. API-only exercises do not, by themselves, prove an Android client was tested.
4. **Prebuilt APK and network risk:** use the hash-verified BugBazaar release APK instead of building from source for your setup. The app requests sensitive permissions and includes Firebase/external SDKs; use a disposable emulator with synthetic data and restrict egress to the paths your selected lab requires.
5. **Tooling here:** at the time of the static review, `git` and `java` were detected, while Docker and ADB were not found. Python 3.14 is installed but Flask and `Crypto` were not detected; Devom's Dockerfile instead specifies Python 3.12. The later test runs used a loopback Python 3.14/Flask 3.1.3 backend and ADB against an Android 14 emulator, without Docker. These observations do not establish the state of a future training host.
6. **Dependency and license risk:** Devom's Python dependencies are unpinned. The README describes a custom educational license but points to a LICENSE file not visible in the root listing; BugBazaar's repository tree did not show an obvious LICENSE file in the inspected tree. Confirm usage and redistribution rights with the owners before training or packaging; absence of a file is not permission.

## Recommended preparation and acceptance gates

1. **Environment gate:** an organization-owned disposable isolated environment, documented permitted endpoints, synthetic accounts, restricted egress, and tested restoration. Record host, emulator, Android version, image, tools and revision hashes.
2. **Setup gate:** test Devom's manual Python backend and install the hash-verified BugBazaar release APK in your selected environment. Confirm the backend certificate and first-launch behavior. You do not build either Android app from source.
3. **Scenario gate:** run each source-backed exercise from a clean state and record prerequisites, exact benign success evidence and cleanup. Validate both positive and negative controls. Treat failure to reproduce as a finding, not an invitation to invent results.
4. **Cloud gate:** the lab must target an environment the training organization controls. Lab 27 meets this with a committed local Firebase Storage emulator, a separate application ID, and synthetic fixtures; the app connection was validated end to end. The upstream Firebase configuration is never a target.
5. **Materials gate:** update these guides from test evidence. Use them to run the labs. Include the expected duration, starting state, and completion criteria. Keep solution notes separate and access-controlled; add them only at your request.

## What remains unknown

Devom manual-backend compatibility and app trust of its ad-hoc certificate; BugBazaar behavior outside the tested Android 14 / API 34 environment; availability of an approved instrumentable emulator; exact participant count, lab isolation model, training duration, and lab infrastructure. The Lab 27 emulator is verified on the tested host and emulator image only; other hosts may need different port or firewall handling. These require actual deployment or stakeholder decisions and are not resolved by static source review.
