# Lab clarity and layout follow-up

## Scope and evidence

This follow-up keeps the ten tested app walkthroughs and their safety limits, adds a short scenario plus a numbered "You will:" goal to each lab, and separates host prerequisites from optional LabKit preparation. At the user's request, there is no separate "Complete when" section; observable checks stay in the walkthroughs and Evidence sections.

All 16 public lab screenshots retain their original bytes. Six portrait Android images display at 300 CSS pixels or the available article width, whichever is smaller. All evidence images link directly to their full-resolution originals. Terminal, browser-console and source evidence keep their wider rendering. A mobile header overflow exposed by the browser regression was also corrected without changing hero styles.

The private authoring contract remains at `engineering/qa/lab-structure.md`. No public authoring page or navigation entry was added. Setup still starts with downloads, Coverage analysis remains in navigation, and the homepage readiness notice stays absent.

## Lab 27 download readiness

The expanded archive contains the verified variant APK, configuration, rules, lifecycle scripts, fixtures, official Firebase CLI 15.34.2 Linux executable, Storage runtime 1.1.3 and emulator UI 1.15.0. The pinned release bytes are fetched during the site build, SHA-256 checked and cached outside Git. Readers using the archive do not need a separate Lab 27 dependency download or npm installation. Independent repository preparation retains the npm-lock path.

The archive is approximately 147 MiB, up from approximately 41 MiB. This is an intentional change to the archive contents, not digest drift. The archive SHA-256 is `2113cc896dde71761e32d4f1c01eefe6cb8b8e5d371b8aaa070d03d7221e9b88`; downloads and release-readiness metadata match it. The four APK hashes are unchanged.

The host-service smoke test extracts the actual archive into a fresh directory and starts it inside a Linux user/network namespace with only loopback enabled and no default route. It verifies both fixtures, a credential-free synthetic-record read, the UI response and cleanup. No `node_modules` or existing Firebase cache is present. This tests the expanded download's host service; it does not re-execute the Android app or replace the earlier end-to-end app evidence.

Offline tests caught three real issues: the standalone CLI replaces its own HOME cache on first launch, the UI needs its local extracted entry point rather than only a ZIP, and the default standalone launcher does not forward termination signals to its CLI child. The emulator files now live outside that cache, startup verifies their hashes and extracts the pinned UI locally, and the initialized CLI runs directly through its embedded Node runtime. The strengthened smoke test observed the lingering-service failure before the fix and verifies that both Storage and UI ports are closed after stopping. A PID namespace prevents the test from leaving orphan processes behind even on failure.

## Verification

- `python3 -m unittest -v test_site`: 30/30 passed in 150.596 seconds, including deterministic archive contents/checksums, independent preparation contracts and introductory structure. The helper-free ADB recipe is executed against controlled absent-package, existing-package and transport-error fixtures; the fresh-package failure was observed before fixing the query.
- `python3 labkit/build.py --fetch-vendor` and `python3 labkit/build.py`: pinned assets verified and archive built.
- `.venv/bin/python -m mkdocs build --strict`: successful. Material prints its upstream MkDocs 2 announcement; no strict-build failure.
- `python3 scripts/check_site_links.py site`: 1,066 local references, fragments and linked archive passed. Fifteen external URLs are listed, not fetched by that checker.
- `node engineering/qa/accessibility_audit.mjs site /tmp/opencode/lab-clarity-accessibility.json`: 18 pages, 0 critical, 0 serious, 13 moderate and 0 minor findings. The moderate findings are non-unique code-tab navigation landmarks, the existing finding type; no severe release-gate failures.
- `node engineering/qa/evidence_layout.mjs site /tmp/opencode/lab-evidence-layout.json`: 10 labs and all 16 originals at 1440- and 360-pixel viewports; portrait bounds, aspect ratios, wider terminal/source evidence, no horizontal overflow, descriptive links and keyboard access to the full-size PIN screenshot checked. Desktop/mobile captures were visually inspected.
- `python3 engineering/qa/lab27_download_smoke.py docs/assets/labkit/LabKit-linux-x86_64.zip`: passed with no external network route; Storage, UI, fixtures, unauthenticated read and stop verified.

Portrait widths measured 300 CSS pixels on desktop and 288 on mobile. Wider evidence measured about 836 pixels on desktop and remained responsive on mobile. Captures: [desktop](screenshots/lab-clarity-desktop.png), [mobile](screenshots/lab-clarity-mobile.png).

## Redistribution review

The CLI project's MIT license and the UI's Apache license are retained, and the unchanged runtime JAR retains its embedded third-party notices. The runtime notices identify Google-owned code without establishing a redistribution grant for all of it. This was raised separately because the earlier four-APK authorization did not automatically cover the new dependencies. In response, the repository owner explicitly confirmed permission to publicly redistribute the additional Firebase binaries. `NOTICE` records that confirmation without claiming the technical review independently established the grant or that the project license relicenses third-party code.

This is a separate follow-up PR. The user subsequently authorized merging once verification succeeds and separately confirmed the required redistribution permission. Merge must still follow protected-main checks without a bypass.

## Branch review

A fresh-context read-only review found one important issue: Android's absent-package `pm path` status stopped the manual recipe under `set -euo pipefail`. The recipe now uses a successful package-list query, exact package matching and a fail-closed transport path. Its execution regression failed before the fix and passed afterward.

The review also suggested running the image-layout check in CI; that step had already been added to the validation workflow during review. No deferred minor findings remain.

Review boundaries: updated introductory formatting follows the user's latest instructions; the expanded bundle's Android app was not freshly re-executed; final suite results are recorded by the implementing session rather than inferred from review. Permission is based on the repository owner's explicit confirmation, not an independent legal opinion. The user's later conditional merge authorization is recorded above.
