# Android intermediate class: coverage and readiness analysis

**Analysis date:** 28 October 2026  
**Scope:** The ten gray modules (9, 10, 14, 24–30), their existing employee guides, Devom, and BugBazaar.  
**Method:** Static inspection of selected upstream source and configuration at the pinned revisions below. No APK execution, Gradle build, Docker deployment, proxy interception, or end-to-end exploitation was performed. Source evidence supports hypotheses, not a claim that an employee can complete a lab on a particular device.

## Executive assessment

Devom is the stronger foundation for the selected backend and API scenarios: its server source contains direct candidates for seven modules. BugBazaar is the stronger candidate for Android components and local runtime manipulation. The remaining cloud database module is blocked until a separately authorized, isolated cloud database or emulator is supplied and the application integration is verified.

**Pilot status (29 October 2026):** The seven Devom labs (09, 10, 14, 24, 25, 26, 28) and Lab 29 have since been run end to end in isolated environments, and their guides now include observed output and screenshots. Lab 30's Frida hook ran, but the same-PIN before/after comparison remains incomplete. Lab 27 remains blocked. The assessment below records the original static review and is kept for traceability; each lab page now states what its pilot actually observed.

**None of the ten guides was ready for production delivery at the time of this static review.** The guides were challenge briefs, not fully tested step-by-step labs: they lacked verified device setup, expected outputs, instructor preparations, time estimates, reproducible reset procedures and answer keys. Module 27 is not runnable on the material currently available. Modules 29–30 had concrete source candidates, but their build and runtime prerequisites were unverified; Lab 29 has since been piloted, and Lab 30 is partly piloted.

## Sources and versions

- Devom revision [`af4290ce8d2178765bfc2bd96cf233f6d3d03161`](https://github.com/memohk/Devom/tree/af4290ce8d2178765bfc2bd96cf233f6d3d03161): [server.py](https://github.com/memohk/Devom/blob/af4290ce8d2178765bfc2bd96cf233f6d3d03161/server.py), [admin_routes.py](https://github.com/memohk/Devom/blob/af4290ce8d2178765bfc2bd96cf233f6d3d03161/admin_routes.py), [Compose](https://github.com/memohk/Devom/blob/af4290ce8d2178765bfc2bd96cf233f6d3d03161/docker-compose.yml), [Dockerfile](https://github.com/memohk/Devom/blob/af4290ce8d2178765bfc2bd96cf233f6d3d03161/Dockerfile), and requirements.
- BugBazaar revision [`fef6a899a684245eb70b2ab4be926f62be849ed9`](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9): [manifest](https://github.com/payatu/BugBazaar/blob/fef6a899a684245eb70b2ab4be926f62be849ed9/app/src/main/AndroidManifest.xml), [AddressContentProvider.java](https://github.com/payatu/BugBazaar/blob/fef6a899a684245eb70b2ab4be926f62be849ed9/app/src/main/java/com/BugBazaar/ui/addresses/AddressContentProvider.java), [PasscodeActivity.java](https://github.com/payatu/BugBazaar/blob/fef6a899a684245eb70b2ab4be926f62be849ed9/app/src/main/java/com/BugBazaar/ui/PasscodeActivity.java), [Signin.java](https://github.com/payatu/BugBazaar/blob/fef6a899a684245eb70b2ab4be926f62be849ed9/app/src/main/java/com/BugBazaar/ui/Signin.java), build files and README.

**Evidence labels:** “Source-backed” means the relevant logic is visible in inspected source, not that the exercise has passed. “Claim only” means the project advertises a scenario but the specific implementation and environment have not been verified.

## Module-by-module assessment

The “Pilot requirements” and “Guide gap” lines below describe what was missing at the time of the static review. The lab pages now record the pilot results and how each gap was addressed; Lab 27 and the unfinished part of Lab 30 are the exceptions.

### 9 — JWT-based account state bypass: Devom, source-backed

- `/login` derives `locked` from database status, generates a token and returns it even for a blocked account. `validate_jwt` verifies the HS256 signature and then checks the token's `locked` claim; it does not consult current database status. The signing key is initialized by Compose, and `admin_routes.py` provides an authenticated user-status update.
- There are two distinct tests: a previously issued token after the account is blocked tests stale state, while a newly issued blocked token modified and re-signed tests trust in a signed claim and key compromise. Rewriting an unsigned payload alone is not sufficient.
- **Pilot requirements:** disposable account, establish active baseline, record old token, block account, confirm old and new token behavior, restore state. Verify whether APK flow permits the intended setup and whether JWT expiry affects results.
- **Guide gap:** explicitly distinguish both approaches and avoid implying a signature can be bypassed. The existing guide does not yet specify setup of a dedicated account or reliable reset.

### 10 — OTP authentication logic: Devom, source-backed

- `/login` returns `session_token` before OTP verification and includes `debug_token`. `/verify_login_2fa` accepts either a fixed value or the pending code. The `token_required` decorator checks the token but not OTP completion.
- These are separate findings: disclosure, predictable/fixed bypass, and protected access without an OTP-bound session. A successful OTP response alone does not demonstrate a protected session.
- **Pilot requirements:** demonstrate login-issued token against `/profile/<id>` before verification, compare invalid and accepted OTP, and establish which condition the Android client actually uses.
- **Guide gap:** require a time-ordered sequence and ensure students do not mistake an isolated `success` response for authenticated access.

### 14 — Command injection via file input: Devom, source-backed

- `/upload_profile_pic` builds a filename from the user ID and submitted filename, saves the upload, then interpolates the filename into an `echo` command executed with `shell=True`; `server_debug` exposes output.
- **Pilot requirements:** verify that the exact multipart filename survives client, proxy, Werkzeug and filesystem handling, and that the harmless output marker appears. The file must save successfully before the command runs.
- **Constraint:** command execution occurs in the service container, which has bind mounts; containment is therefore essential. Use only a benign marker with no network calls, file modification or unrelated host access.
- **Guide gap:** specify a validated benign test and what output counts as success only after an isolated pilot.

### 24 — Unrestricted file upload: Devom, source-backed

- `/upload_profile_pic` saves provided file contents without an apparent extension, content or authorization check; `/view_upload` serves paths from uploads. This supports a validation and access-control exercise, not a claim of uploaded code execution.
- **Pilot requirements:** compare a real image with a small harmless non-image file; verify actual content retrieved, response headers, and whether expected ownership checks exist.
- **Guide gap:** distinguish “stored despite unsuitable type” from executable upload, and ensure all comparisons use synthetic content.

### 25 — Server-side path traversal: Devom, source-backed

- `/download_pdf/<path:filename>` and `/view_upload/<path:filename>` use `send_file(os.path.join(UPLOAD_FOLDER, filename))` without an explicit canonical containment check. Whether a traversal reaches the route depends on the HTTP client, URL normalization and the deployment stack.
- **Pilot requirements:** instructor creates a uniquely marked harmless file inside the disposable container, outside uploads; confirm normal retrieval and marker-only traversal, including exact raw request behavior.
- **Guide gap:** define marker provisioning and cleanup in instructor material; a source-code observation alone does not prove an HTTP exploit works.

### 26 — Insufficient transaction validation: Devom, source-backed

- `/transfer` checks a token but directly uses supplied `from_id`, `to_id`, and `amount` in balance updates and creates a transaction without apparent amount, source ownership or sufficient-funds validation. Negative amounts and a mismatched sender are separate issues.
- **Pilot requirements:** two known test users with measured initial balances, one normal transaction, then one controlled invalid-value test. Verify the two balances and stored transaction, not just the response. Prefer a fresh dataset per participant.
- **Guide gap:** define account provisioning and isolation; note that the two seed accounts include an administrative demo user and should not be assumed suitable for multi-user training without instructor preparation.

### 27 — Cloud database misconfiguration: BugBazaar, claim only; blocked

- BugBazaar's README lists misconfigured Firebase Firestore, and the repository contains `app/google-services.json` and Firebase dependencies. This is not evidence that an upstream cloud service is owned by the training organization, reachable, intentionally open today, or authorized for testing. The examined app build file does not itself establish the Firestore exercise's implementation or emulator compatibility.
- **Required before pilot:** an organization-owned disposable project or local emulator, an explicit authorization boundary, synthetic data and intentionally weak rules, plus proof that the app actually targets that environment. Configuration changes or a dedicated fixture may be necessary; none has been designed or approved.
- **Guide status:** correctly marked blocked. Never use the upstream Firebase configuration as a target merely because it appears in source.

### 28 — Broken object-level authorization: Devom, source-backed

- `/profile/<user_id>` requires a valid token but fetches the requested user ID without comparing it to the token subject. The returned user row includes sensitive fields, so evidence must be sanitized even for synthetic records.
- **Pilot requirements:** create two authorized disposable users; capture account A's request for its own profile, then request B's profile using A's same token. Verify identity and response body; compare against an expected denial.
- **Guide gap:** provide an instructor-supplied second user, and redact secrets and lab passwords from artifacts.

### 29 — Unauthorized Android components: BugBazaar, source-backed candidate

- The manifest declares `AddressContentProvider` exported with authority `com.bugbazaar.provider.addresses` and no explicit permission. Its `query` and `insert` methods access the address database. This is a concrete candidate but accessibility and impact must be checked on an actual Android build.
- Other exported components exist; export alone does not prove a vulnerability. ADB shell's identity and privileges differ from a normal third-party app, so a second, ordinary app is preferable to establish cross-app impact.
- **Pilot requirements:** build/install, seed a synthetic address, verify access from a separate unprivileged test app, record baseline and result, and evaluate Android version effects.
- **Guide gap:** select and document one verified component and establish a reproducible synthetic fixture and non-shell caller.

### 30 — Client-side login bypass through runtime manipulation: BugBazaar, source-backed candidate

- `PasscodeActivity` compares the entered value against `UserAuthSave.getpasscode()` in the button click listener; a match opens `NavigationDrawer_Dashboard`, while a mismatch displays an error. This supports investigation of a local passcode gate, not proof of bypassing remote authentication.
- `Signin.java` has navigation paths that can reach the dashboard independently; therefore dashboard visibility alone is not conclusive evidence that instrumentation changed the PIN check. Prove the instrumented code path against an incorrect-PIN baseline and distinguish other navigation routes.
- **Pilot requirements:** establish a logged-in state and PIN, reproduce rejection, verify process and Frida compatibility, demonstrate the changed local branch and rule out alternate navigation.
- **Guide gap:** clarify that this is a local app passcode bypass and specify a reliable branch-level success criterion after testing.

## Cross-cutting environment findings

1. **Network exposure:** Devom's `server.py` binds to `0.0.0.0:8080`, runs in debug mode, and enables ad-hoc TLS. Compose publishes container port 8080 on host port 8443 on all host interfaces by default. Bind Compose to loopback and verify host firewall rules; emulator networking differs by emulator and operating system.
2. **Persistence and separation:** Compose bind-mounts database, uploaded files, keys and templates and names the container `dvom-lab-v1`. Shared instances can collide or leak changes across participants. Provide separate disposable environments or controlled unique copies and cleanup; do not delete existing user data.
3. **Encryption affects observation:** Devom's middleware accepts JSON and normally encrypts JSON responses, except when the User-Agent contains `Postman` or the path is exempt. App traffic may need separate handling. API-only exercises do not, by themselves, prove an Android client was tested.
4. **Prebuilt APK and network risk:** use the hash-verified BugBazaar release APK instead of building from source for learner setup. The app requests sensitive permissions and includes Firebase/external SDKs; use a disposable emulator with synthetic data and keep it offline where the lab requires.
5. **Tooling here:** at the time of the static review, `git` and `java` were detected, while Docker and ADB were not found. Python 3.14 is installed but Flask and `Crypto` were not detected; Devom's Dockerfile instead specifies Python 3.12. The later pilots used a loopback Python 3.14/Flask 3.1.3 backend and ADB against an Android 14 emulator, without Docker. These observations do not establish the state of a future training host.
6. **Dependency and license risk:** Devom's Python dependencies are unpinned. The README describes a custom educational license but points to a LICENSE file not visible in the root listing; BugBazaar's repository tree did not show an obvious LICENSE file in the inspected tree. Confirm usage and redistribution rights with the owners before training or packaging; absence of a file is not permission.

## Recommended preparation and acceptance gates

1. **Environment gate:** an instructor-owned disposable isolated environment, documented permitted endpoints, synthetic accounts, restricted egress, and tested restoration. Record host, emulator, Android version, image, tools and revision hashes.
2. **Setup gate:** pilot Devom's manual Python backend and install the hash-verified BugBazaar release APK in the selected environment. Confirm the backend/certificate and first-launch behavior; keep setup claims labeled unverified until confirmed. Learners do not build either Android app from source.
3. **Scenario gate:** pilot each source-backed exercise from a clean state and record prerequisites, exact benign success evidence and cleanup. Validate both positive and negative controls. Treat failure to reproduce as a finding, not an invitation to invent results.
4. **Cloud gate:** independently provision and authorize a disposable cloud environment or emulator and validate the app connection. If unavailable, omit module 27 from delivery and record it as an unmet requirement.
5. **Materials gate:** update employee guides based on pilot evidence. Create separately controlled instructor notes and solutions only if requested; the present deliverable is employee-facing. Add expected duration, starting state and clear completion criteria.

## What remains unknown

Devom manual-backend compatibility and app trust of its ad-hoc certificate; BugBazaar behavior outside the Android 14/API 34 pilot; availability of an approved instrumentable emulator; the same-PIN before/after comparison in Lab 30; ownership and configuration of a cloud database; exact participant count, lab isolation model, training duration, and instructor infrastructure. These require actual deployment or stakeholder decisions and are not resolved by static source review.
