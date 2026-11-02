# Production-Ready Public Lab Site

## Goal

Make the public MkDocs lab site dependable for first-time learners, with every learner-facing claim supported by fresh content, runtime, build, CI, artifact, accessibility, and visual-QA evidence. Keep all exercises within a disposable isolated environment, expose no lab targets to public or corporate networks, restrict egress to required paths, and use synthetic data only.

## Current context

- The repository contains ten lab pages (labs 9, 10, 14, and 24–30), a lab structure guide, setup pages, structural content tests, a MkDocs Material site, and a publishing guide.
- The current structure guide already calls for numbered walkthrough steps with location, action, and expected check, but all pages and Evidence checklists still need reconciliation against that contract.
- Lab 27 currently says it requires an authorized external Firebase environment and supplies no runnable commands. The approved direction replaces that design with a permanent local Firebase Emulator Suite, synthetic seed data, and a Lab 27 APK built from the pinned BugBazaar source and configured for that emulator.
- `docs/assets/apk/` already contains the module-29 caller APK. The requested published artifact set is four APKs: unchanged official BugBazaar v1.2.1, Devom's `Dvom.apk`, the module-29 caller, and the new repo-built Lab 27 APK.
- `test_site.py` contains structural checks; those remain. No tests will be added to judge prose, spelling, or wording quality.
- The current publishing notes describe main-branch deployment. Repository branch protection and required-check settings are hosted GitHub state and must be verified separately from repository files.
- The checkout has generated MkDocs output and Android build output in its working tree; whether those outputs are tracked or ignored must be determined before cleanup. No unrelated user work may be discarded.

## Scope

### In scope

1. Reconcile the structure guide and all ten lab walkthroughs. Each step must state where the learner works, the action, and a check/expected observation. Define technical terms, variables, and placeholders at first use. Evidence sections must be fill-in checklists; each item must point to the step or command that produces it, be achievable with the documented setup alone, and follow existing redaction rules.
2. Preserve and state the safety boundary in setup and relevant lab content: disposable environment; no public or corporate exposure; egress restricted to required paths; synthetic data only; stop when the environment falls outside scope.
3. Verify upstream provenance, unchanged status where required, file identity, and SHA-256 for each of the four APKs. Store all four under `docs/assets/apk/`, document the hash and upstream source on a downloads page, and direct learners to those repository artifacts rather than third-party download sites. Add an attribution NOTICE that identifies the mirrored artifacts and their sources/licensing facts established during verification. Do not invent or assume licensing terms.
4. Pin the BugBazaar source used for the Lab 27 APK. Build a ready-to-install app that points only to the repository's permanent local Firebase Emulator Suite. Define stable local identifiers/ports, emulator configuration, synthetic fixtures, and reproducible start, stop, and reset procedures based on the actual source and tool behavior. Verify the app reaches the emulator and completes the documented scenario without contacting upstream Firebase. Preserve the intended lab scenario; do not substitute an unrelated mock result.
5. Run every lab end to end in the documented setup, including Lab 27. Record fresh, observed outputs and relevant context for every run. Do not reuse stale screenshots or infer execution results from source inspection.
6. Add pull-request and push CI that runs existing content tests, `mkdocs build --strict`, a dead-link and local-asset scan over built HTML with zero broken references, and an HTML/accessibility audit with zero serious or critical violations. Make diagnostic output and reports available as CI results/artifacts as appropriate.
7. Configure `main` to require pull requests and passing required checks, and capture the actual required-check/protection state. If available permissions cannot make or verify this hosted setting, report the exact missing capability rather than claiming it is enabled.
8. Visually inspect every published page in dark theme at desktop width. Exercise search, theme toggle, collapsible hints, and code-copy controls. Save QA screenshots and a durable report identifying the pages, viewport, interactions, findings, and date/context of the inspection.
9. Add an MIT LICENSE for project material with clear NOTICE treatment of third-party artifacts; a custom 404 page; and align README, index, PUBLISHING, coverage analysis, and lab-expansion plan with the evidence actually obtained.
10. Ensure the repository has no stale or diverged branches under project control and no committed generated build artifacts. Report branches that cannot be safely removed or controlled; do not force-delete or discard unowned work.

### Out of scope

- Using real accounts, personal information, production data, upstream cloud resources, or real Firebase projects in any lab.
- Sending learners to external APK download locations.
- Claiming runtime success based solely on source inspection, screenshots from another run, or a build completing.
- Rewriting the existing structural tests as prose-quality assertions.
- Deleting unfamiliar, user-owned, or untracked work to obtain a clean repository.
- Claiming GitHub branch protection, CI success, or live publication without direct fresh evidence.

## Intended workflow

1. Inventory repository state, all ten page structures, artifact sources, pinned app revisions, Android/Java/Gradle/Firebase tooling, CI, and remote branch/check configuration. Preserve pre-existing user changes.
2. Produce a content gap matrix against the structure contract. Update the guide and pages with learner instructions and mapped Evidence checklists, retaining the existing redaction/safety limits. Perform and record a human read-through; do not encode wording judgments as tests.
3. Resolve artifact provenance and redistribution/licensing facts before mirroring. Verify candidate files and hashes; mirror only files whose upstream identity and permitted redistribution are established. Add all four APKs, their hash/source metadata, downloads page, and NOTICE. Do not publish guessed hashes or unverified artifacts.
4. Inspect the pinned BugBazaar build and Firebase integration. Implement the smallest reproducible local emulator configuration and synthetic fixture that preserves the Lab 27 scenario. Build and install the configured APK, verify its Firebase endpoint is local, run documented reads/rules checks and any authorized in-scope writes, then stop/reset the emulator and verify reset behavior. If the pinned build cannot be built, the emulator cannot run, or the app cannot be pointed at it without invalidating the scenario, stop at that gate and report the attempted commands, exact failure, and smallest unblock input. Do not continue to claim Lab 27 is complete.
5. Execute the documented walkthrough for each of the ten labs. Capture exact observed output, environment/version context, and only screenshots created during that run. Repair each failure and rerun the affected lab/gate before recording it as passed.
6. Add CI checks for existing tests, strict MkDocs build, built-HTML link/asset resolution, and accessibility severity threshold. Exercise the workflow on both pull requests and pushes. Require all applicable checks for `main` through GitHub settings and verify the resulting protection/check state.
7. Run the strict build and all local CI-equivalent checks. Visually inspect every page in dark desktop mode and exercise the specified UI controls. Save screenshots and a durable QA report.
8. Update learner-facing and project status claims only from completed evidence. Add the custom 404 page and license/attribution material. Ensure generated `site/` and Android intermediate/build output are not committed; review branch divergence and clean only branches proven safe to remove.
9. Perform a final evidence audit: fresh CI run/logs, required-check state, strict build output, link/asset and accessibility reports, QA screenshots/report, committed APK SHA-256 values, and observed results for all ten lab runs. Re-run any gate affected by a subsequent change.

## Design details

### Learner documentation

The lab structure guide is the normative outline. Each lab page must match it, including sections for purpose/status, prerequisites and safety, scenario, numbered guided walkthrough, troubleshooting, Evidence and optional hints, vulnerability/impact and evidence limits, and cleanup/review. Setup pages own installation; labs link to setup and include only exercise-specific preparation. Evidence lists are learner-fillable and map each requested artifact/observation to its producing step or command. No Evidence item may require unprovided credentials, external authorization, an external download, or a tool omitted from setup.

The read-through report records clarity and completeness findings and disposition. It is a manual QA artifact, not an automated prose score.

### APKs and Firebase Emulator Suite

The downloads page is the learner-facing source of truth for the four repository-hosted APKs. For each file it records filename, SHA-256, upstream/source identity, version/revision where known, and applicable attribution/license notes. The official BugBazaar v1.2.1 binary remains byte-for-byte unchanged. The new Lab 27 APK is separately identified as a project-built variant from the pinned BugBazaar source and is configured for the local emulator, not an upstream Firebase service.

The emulator setup is committed and repeatable. Its data is synthetic and deterministic; its stable local identifiers and endpoint configuration are explicit. Start/stop/reset commands and successful output are demonstrated in the guide. Reset returns the emulator to the documented baseline. The app's endpoint and observed traffic must establish local-only behavior. Do not expose emulator ports beyond the local lab boundary or broaden egress.

### CI, access controls, and reports

CI runs on pull requests and pushes. The required gates include existing tests, strict MkDocs build, local link and asset checking against generated HTML, and accessibility/HTML validation. Broken local references must equal zero; serious and critical accessibility violations must equal zero. External-link availability is not silently treated as a local asset failure; reports distinguish local references from network-dependent links.

`main` requires a pull request and successful required checks. The repository may document intended policy, but acceptance requires a fresh observation of the actual GitHub rules/checks. A missing permission is a blocker to the hosted-setting portion, not grounds to assert success.

### Visual and runtime QA

The durable QA record identifies each inspected page and states that the inspection was performed in dark theme at desktop width. Search, theme toggle, each collapsible hint, and code-copy are explicitly exercised. Screenshots show actual UI and are stored under a QA/report location that is not accidentally published as learner content unless intentionally selected. Lab run records identify the exact documented steps, setup/app versions, observed outputs, and sanitized evidence. Do not invent timestamps, screenshots, output, or hashes.

### Licensing and repository hygiene

The MIT LICENSE applies to project-owned material as stated in the license. Third-party APKs and other mirrored materials are called out separately in NOTICE with only verified attribution and licensing information; the repository's MIT license does not purport to relicense them. A 404 page is included in the MkDocs source and verified in built output. Generated MkDocs and Android build products are build outputs, not source artifacts, and are not committed. APKs intentionally distributed to learners under `docs/assets/apk/` are release inputs, not build output.

## Safety and evidence requirements

- Use disposable, isolated environments only; no public or corporate exposure.
- Restrict network egress to the exact paths required by the documented exercise; Firebase for Lab 27 is local emulator traffic only.
- Use synthetic data only, including deterministic Lab 27 fixtures.
- Preserve redaction of tokens, keys, service-account material, personal data, and unrelated device content.
- Record only observations actually made. Every claimed pass is backed by fresh output or a report from the corresponding run.
- After a failure, fix its cause and rerun the affected gate. Stop and report only for the Lab 27 feasibility blockers defined above, or where a required external permission/access input is unavailable.

## Acceptance criteria

- All ten lab pages follow the documented structure, and guide/pages agree.
- Every walkthrough step identifies where to work, what to do, and what to check; terms and placeholders are explained at first appearance.
- Every Evidence section is a fill-in checklist mapped to a producing step/command, achievable with the documented setup alone, and compliant with existing redaction rules.
- All ten labs, including Lab 27, have fresh end-to-end observed run records; no unverified run is described as working.
- All four APKs are in `docs/assets/apk/`; downloads documentation contains verified SHA-256 and upstream source for each; setup content uses repository-hosted files, retains hash verification, and does not direct learners to external download sites. NOTICE records verified attribution.
- Lab 27 APK is built from the pinned BugBazaar source, connects only to the permanent local Firebase Emulator Suite, and works with documented synthetic fixtures and verified start/stop/reset procedures.
- `mkdocs build --strict` passes.
- PR and push CI runs existing content tests, strict build, built-HTML dead-link/asset scan with zero broken references, and HTML/accessibility audit with no serious or critical violations.
- `main` requires a PR and passing checks, verified from GitHub's actual settings/check state.
- Every page is visually inspected in dark theme at desktop width; search, theme toggle, collapsible hints, and code-copy are exercised and recorded in a durable QA report with screenshots.
- MIT LICENSE, custom 404, NOTICE, README, index, PUBLISHING, coverage analysis, and lab-expansion plan accurately reflect verified state.
- No generated build output is committed; branch review finds no stale/diverged branches under project control, or safely unmanageable branches are explicitly reported.
- Fresh evidence is retained for CI logs/check state, strict build, link/asset and accessibility reports, QA screenshots, committed APK hashes, and observed output from each lab run.

## Stop conditions and reporting

The specified Lab 27 stop conditions are: (a) no working Android build for the pinned source after documented attempts, (b) Firebase Emulator Suite cannot run after documented attempts, or (c) the app cannot be configured to use the emulator without invalidating the lab scenario. Report attempted commands and environment, exact failure/output, and the smallest input or access needed to unblock. Do not replace the requested local emulator with an externally supplied Firebase environment.

Other required hosted configuration (such as GitHub branch protection) must also be reported precisely if permissions prevent it, without falsely declaring the overall goal complete.
