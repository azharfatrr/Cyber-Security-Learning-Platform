# Single-download LabKit and production release

## Goal

After the already completed first deployment, publish a follow-up that gives a learner one LabKit download for all ten labs, keeps maintainer guidance off the public learner site, and closes the remaining production-release gaps identified in the final review.

## User direction and decisions

- The user explicitly authorized public redistribution of the APKs previously identified in `NOTICE`.
- Learners should have one download action for the complete LabKit, rather than separate APK downloads or a repository checkout for Lab 27 files.
- `docs/lab-structure.md` is authoring guidance, not learner content; move it out of `docs/` and remove it from the public navigation/site.
- Use best judgment without asking the user further questions. The selected package boundary is one Linux x86_64 LabKit archive plus standard host/emulator prerequisites already installed. A bootstrap inside the kit fetches pinned project dependencies automatically from explicit upstreams; learners do not manually fetch or install per-lab artifacts.
- The Android emulator/SDK image is an installed prerequisite and will not be redistributed inside the LabKit. Runtime exercises remain restricted to disposable lab environments with synthetic data and the documented egress boundaries.

## Scope

1. Build one deterministic `LabKit-linux-x86_64.zip` containing the four verified APKs, SHA-256 manifest, Lab 27 Firebase configuration/rules/fixtures/lifecycle scripts, Lab 30 hook source, and learner-facing quick-start/bootstrap material.
2. Provide a single LabKit download link on the learner-facing downloads page. Keep per-artifact identity, source and hash information as an inventory, but do not expose individual APK download links from the site.
3. Keep the original APK inputs in a tracked, non-published directory. Generate the LabKit archive into the MkDocs build output as a build artifact; do not commit generated archives or `site/`.
4. Provide a bootstrap that checks the supported host and installed emulator prerequisites, verifies the archive manifest, prepares the pinned Devom checkout and Python environment, installs the locked Firebase CLI and prefetches the Storage emulator, and provisions the matching Frida/JADX tools from pinned sources. Do not silently weaken network controls. Bootstrap egress is limited to the documented pinned sources; runtime lab traffic follows each lab's existing local/restricted paths.
5. Document the unavoidable baseline prerequisites: Linux x86_64 disposable host, Bash, Python, Git, curl, Node/npm, Java, ADB, and an already installed instrumentable Android 14/API 34 x86_64 emulator. The kit is a single manual download, not a full Android SDK/emulator image and not a network-free image.
6. Move the lab authoring contract from `docs/lab-structure.md` into `engineering/qa/` and remove it from the public MkDocs navigation/output.
7. Update attribution to record the repository owner's confirmation of separate public educational redistribution authorization for the APKs, without representing that confirmation as an upstream open-source license.
8. Add a project-owned MIT `LICENSE` and a custom learner-facing 404 page.
9. Expand CI to pull requests and pushes to `main`. Build the LabKit, run existing unit tests and strict MkDocs, validate local links/assets in rendered HTML, and run an HTML/accessibility audit with no serious or critical violations.
10. Configure `main` to require PRs and the release checks. Visually inspect every published page in dark desktop mode and exercise search, theme switch, hints, and code-copy; retain a QA report and screenshots outside the public docs unless intentionally linked.
11. Publish the follow-up through a PR and verify its deployment, public LabKit download, checksum, 404 handling, and release commit on Pages.

## Explicit exclusions

- Do not bundle an Android SDK, Android system image, emulator, or personal/production data.
- Do not direct learners to third-party APK download sites or provide standalone APK links on the site.
- Do not copy Devom source into the public archive without source redistribution authorization. The bootstrap fetches the pinned upstream revision automatically, so the learner does not need a separate manual download.
- Do not expose emulator ports, relax egress boundaries, contact cloud services, or deploy the deliberately open Firebase Storage rules.
- Do not alter observed lab outcomes except where a fresh rerun demonstrates a required correction.
- Do not force-push, delete unfamiliar branches/worktrees, or discard unrelated changes.

## LabKit contract

- Filename: `LabKit-linux-x86_64.zip`.
- One download contains all four APKs and every repository-owned lab configuration/script/fixture required by the ten walkthroughs.
- `manifest.sha256` covers all APK inputs and the completed archive is separately hashed on the downloads page and in release verification output.
- `setup.sh` is safe to rerun, checks OS/architecture and required tools before changes, checks the selected ADB device before installation, and fails closed if a version/hash/egress prerequisite differs.
- Project-specific dependencies are pinned and installed by the kit bootstrap. External bootstrap destinations and their file hashes are documented. No runtime lab command fetches remote code or artifacts.
- Lab 27 starts, resets, and stops using only the bundled rules and synthetic fixtures. The emulator remains bound to host loopback and Android emulator host routing.
- Lab 30 uses a matching pinned Frida client/server for the supported AVD and the bundled hook script. The setup does not change or clear existing app/device state without an explicit safe precondition.

## Acceptance criteria

- A learner can follow the Lab Downloads page, download one archive, verify it, extract it, run one setup command, and find all ten labs' artifact/configuration files without cloning this repository or manually downloading an APK/tool.
- The host/emulator prerequisites and one-time network bootstrap are prominent; the package is not described as offline or as bundling an Android image.
- All APK bytes and hashes remain unchanged and match the existing verified identities.
- No standalone APK links or public `lab-structure` page remain in the generated site.
- The archive can be built reproducibly from a clean checkout; its contents and manifest are validated by tests.
- The custom 404 is served by Pages; the root license covers project-owned material only; NOTICE describes the user's confirmed APK authorization separately.
- PR and push workflow checks tests, strict build, local links/assets, and accessibility; the `main` rule requires PR and all named checks.
- Every page has a recorded visual QA result in the specified dark desktop context and the requested controls are exercised.
- All ten labs retain their 2 November 2026 observed evidence unless any affected setup is rerun and updated.
- The follow-up Pages deployment succeeds and serves the new LabKit with the verified checksum.

## Known limits

- The single archive is for Linux x86_64 hosts and assumes a separately installed Android 14/API 34 x86_64 instrumentable emulator. It cannot make an unrooted or incompatible device suitable for Lab 30.
- First-time bootstrap retrieves pinned upstream source/dependencies over restricted egress; the downloaded dependencies are cached in the kit workspace. The learners perform one manual download, but the bootstrap is not offline.
- Public visibility of the archive does not change any upstream source license; permission for APK redistribution is the separate authorization confirmed by the user.
