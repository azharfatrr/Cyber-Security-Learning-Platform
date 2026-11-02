# Learner-material read-through

**Date:** 2 November 2026
**Branch:** `production-ready-lab-site`
**Scope:** `docs/lab-structure.md`, the ten lab pages, and the three setup pages.
**Method:** each page was read in full against the structure contract in `docs/lab-structure.md`, then edited where it differed. This is a structural and internal-consistency review. Labs 09, 10, 14, 24–26, and 28–30 were **not re-executed** in this pass; their recorded outputs remain from the 29 October 2026 runs stated on each page. Lab 27 was re-executed end to end during this pass.

## Contract checks applied

For every lab page:

1. `What this lab does` states target, scenario, completion criteria, and verification status.
2. `Before you begin` holds lab-specific accounts, tools, starting state, and safety limits; a tool list appears as `### Tools needed`.
3. `Understand the scenario` exists and describes the feature and the security boundary.
4. `Guided walkthrough` uses numbered `###` steps, each beginning with a `**Where:**` line and containing an action plus an expected result or stop condition.
5. `Troubleshooting` covers the obstacles that the walkthrough can realistically hit.
6. `Evidence` is a `- [ ]` checklist whose items map to named steps, followed by the collapsible `Hints` block.
7. `Vulnerability and Impact` separates what was demonstrated from what remains potential.
8. `Cleanup and review` restores state and asks remediation questions.

## Findings and dispositions

| Page | Finding | Disposition |
| --- | --- | --- |
| `lab-structure.md` | The contract described sections but not the step, placeholder, or Evidence conventions that the pages needed. | Added the `**Where:**` rule, the `<placeholder>` / `$VARIABLE` rule, the expected-result callout rule, the labelling of source-derived results, and the Evidence checklist format. |
| `00-common-setup.md` | Told learners Lab 27 needed a separately authorized cloud environment, contradicting the verified local emulator. | Replaced with the local emulator path and a pointer to `downloads.md` and `NOTICE`. |
| `01-devom-setup.md` | Told learners to install `Dvom.apk` from a local checkout that the page no longer creates, with no hash check. | Points at the repository-hosted file and verifies its SHA-256 before install. |
| `02-bugbazaar-setup.md` | Downloaded the target APK from the upstream release and had no Lab 27 variant section. | Uses the repository-hosted APK, adds the side-by-side Lab 27 install with its own hash check, and separates the two network paths. |
| `09-jwt-account-state.md` | `## Tools needed` was a top-level section; no `Understand the scenario`; steps had no `**Where:**` lines; Evidence was a prose list. | Converted to `###`; added the boundary description; added all six `**Where:**` lines; converted Evidence to a mapped checklist. |
| `10-otp-bypass.md` | Same four gaps. | Same four fixes. |
| `14-command-injection.md` | Same four gaps. | Same four fixes. |
| `24-file-upload.md` | Same four gaps. | Same four fixes. |
| `25-path-traversal.md` | Same four gaps, and the walkthrough steps sat directly under `Understand` after the edit. | Same four fixes, plus restoring the `## Guided walkthrough` heading. |
| `26-transactions.md` | Same four gaps. | Same four fixes. |
| `27-cloud-database.md` | Claimed the lab required an external, authorized Firebase environment; described a Firestore exercise; the pinned source actually implements Firebase Storage; the page title and nav label said "Cloud database". | Rewrote the page around the verified local Storage emulator, the exact commands and outputs from the 2 November run, and the committed rule. Retitled to "Cloud storage" in the page and nav. |
| `28-bola.md` | Same four gaps. | Same four fixes. |
| `29-components.md` | Same four gaps. | Same four fixes. |
| `30-runtime-bypass.md` | No `Understand the scenario`, no `### Tools needed`, no `**Where:**` lines, Evidence was a prose list. | Added all four. |
| `README.md` | Said nine labs were tested and Lab 27 needed an authorized Firebase environment. | States that all ten were tested, with the two run dates, and links Lab 27 as local-emulator material. |
| `docs/coverage-analysis.md` | Said the cloud module still needed an authorized environment and left the cloud gate open. | Records the verified local-emulator design, the Storage-not-Firestore correction, and the closed cloud gate, while keeping the original static review for traceability. |

## Lab 27 re-run evidence

Run on the test host with the AVD `RootAVD34` (Android 14 / API 34, `sdk_gphone64_x86_64`), Frida not required:

1. `./engineering/lab27/reset.sh` stopped any instance, cleared `.runtime/`, started the emulator, and seeded `alice-lab27/userinfo.txt` and `bob-lab27/userinfo.txt`.
2. The object list returned bucket `lab27-local.appspot.com` with exactly those two objects.
3. An unauthenticated read of `alice-lab27/userinfo.txt` returned the five synthetic lines documented on the page.
4. The installed `com.BugBazaar.lab27` app signed in, created a passcode, and saved a synthetic profile.
5. A third object, `Google sdk_gphone64_x86_64/userinfo.txt`, appeared in the same bucket.
6. An unauthenticated read of that object returned the values entered in the app.

One obstacle is now recorded in the page's troubleshooting: the Android emulator needed a live route to `10.0.2.2` for the upload to succeed. With its Wi-Fi interface down, logcat showed `StorageUtil: no auth token for request` and `ExponentialBackoff: network unavailable`, and no object appeared. The page tells learners to confirm the route and the loopback port before retrying.

## Residual risks not resolved here

- Labs 09, 10, 14, 24–26, and 28–30 were not re-executed in this pass. Their recorded output and screenshots are from the 29 October 2026 runs and were not revalidated by this review.
- The Lab 27 emulator bind and the `10.0.2.2` path were verified on this host and emulator image only. A different host or emulator may need different port or firewall handling.
- The published BugBazaar and Devom binaries have no established upstream redistribution permission. They are hosted under the explicit `NOTICE` recorded in the repository; obtaining permission from the upstream authors remains an open action for any broader distribution.
- `mkdocs build --strict` must run from the pinned environment in `requirements.txt`; the system Python lacks `mkdocs-material`.
