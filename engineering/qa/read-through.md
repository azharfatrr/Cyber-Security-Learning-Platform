# Learner-material read-through

**Date:** 2 November 2026
**Branch:** `production-ready-lab-site`
**Scope:** `docs/lab-structure.md`, the ten lab pages, and the three setup pages.
**Method:** each page was read in full against the structure contract in `docs/lab-structure.md`, then edited where it differed. All ten labs were re-executed on 2 November 2026 and their observed outcomes and screenshots were refreshed. This is a learner-material structure and internal-consistency review; it does not claim the website governance or release-QA gates were run.

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

## Lab re-execution evidence

All outcomes below were observed on 2 November 2026. Devom ran from the pinned revision on loopback with Python 3.14 and Flask 3.1.3. The BugBazaar tests used an Android 14 / API 34 x86_64 emulator; Lab 30 used Frida 17.4.2. Terminal evidence was captured in QTerminal on the real X display because `xfce4-terminal` was not installed.

| Lab | Re-execution result |
| --- | --- |
| 09 | The pre-block profile request returned `200`; while `cala` was blocked, the old token returned `200`, the newly issued blocked token returned `403`, and the lab-key re-signed token returned `200`. The account was restored to `ACTIVE`. |
| 10 | Profile access before OTP returned `200`; wrong code `0000` returned `401`; the disclosed code was redacted and verified with `200`; fixed value `1293` for user `999999` returned `200`. |
| 14 | Baseline and harmless injected uploads returned `200`; the injected response contained `LAB14_MARKER_7f3a` on its own line. |
| 24 | Synthetic text and HTML uploads succeeded; both reads returned `200` without an `Authorization` header, as `text/plain` and `text/html`. |
| 25 | The contract baseline returned `200`; both `/view_upload/../lab25-marker.txt` and `/download_pdf/../lab25-marker.txt` returned `200` with the synthetic marker. |
| 26 | Starting balances were `1000/999999`; normal, negative, cross-account, and restoring transfers returned `200`, with final balances restored to `1000/999999`. |
| 27 | Reset seeded the two synthetic records; the app saved a synthetic profile and wrote `Google sdk_gphone64_x86_64/userinfo.txt`; an unauthenticated read returned the saved fields. The Lab 27 APK hash and local project/package identifiers also matched. |
| 28 | The same `cala` token read profiles `100500` and `133700` with `200`; the read-only account and transaction routes for `133700` also returned `200`. |
| 29 | On Android 14 / API 34, BugBazaar UID `10197` and caller UID `10198` were distinct; the ordinary caller read only the uniquely marked synthetic address. |
| 30 | The stored PIN was `2468`; wrong PIN `0000` was rejected, `2468` opened the dashboard, and the Frida hook made `0000` open the dashboard. Frida showed the hook install and method call; the server was stopped afterward. |

Fresh evidence is stored under `docs/images/lab-09/` through `docs/images/lab-30/`, including the Lab 27 profile-save screen and Lab 30's source, Frida output, baseline, and hooked result. One Lab 27 obstacle remains documented in its troubleshooting: the emulator needs a live route to `10.0.2.2` for the upload to succeed. With its Wi-Fi interface down, logcat showed `StorageUtil: no auth token for request` and `ExponentialBackoff: network unavailable`, and no object appeared.

The repository checks completed after the documentation and image updates: `python3 -m unittest -v test_site` passed all six tests, and `.venv/bin/python -m mkdocs build --strict` completed successfully. The build emitted the Material for MkDocs upstream MkDocs 2.0 advisory, but no strict-build documentation warnings.

## Residual risks not resolved here

- The Lab 27 emulator bind and the `10.0.2.2` path were verified on this host and emulator image only. A different host or emulator may need different port or firewall handling.
- The published BugBazaar and Devom binaries have no established upstream redistribution permission. They are hosted under the explicit `NOTICE` recorded in the repository; obtaining permission from the upstream authors remains an open action for any broader distribution.
- Site CI and governance, and release QA, remain out of scope for this read-through.
