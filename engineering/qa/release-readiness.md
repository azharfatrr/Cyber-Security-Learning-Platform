# Release readiness QA

**Reviewed:** 2 November 2026

**Browser:** Playwright 1.64.1 with bundled Chromium

**Viewport:** 1440 × 1000 CSS pixels

**Theme:** Material `slate` (dark), background `rgb(11, 16, 24)`

**Serving path:** `/Cyber-Security-Learning-Platform/` to match the configured GitHub Pages project base path

## Results

- All 18 rendered HTML pages loaded successfully. No browser page errors or horizontal overflow were observed.
- Search for `LabKit` returned 8 results. The theme toggle switched from dark to light and back to dark.
- All 10 lab hint disclosures opened and closed. All 82 code-copy controls copied their expected text to the clipboard.
- The custom root `404.html` rendered with the dark theme and linked to the Pages home and downloads paths under the project base URL.
- The download page presents one LabKit archive CTA and no individual APK links.
- axe-core audited all 18 pages: 0 critical, 0 serious, 12 moderate, and 0 minor findings. The moderate `landmark-unique` findings occur on code-tab navigation controls on 12 pages; they do not fail the configured release gate.
- The linked archive was rebuilt for the clarity/layout follow-up with pinned Lab 27 dependencies included. SHA-256: `2113cc896dde71761e32d4f1c01eefe6cb8b8e5d371b8aaa070d03d7221e9b88`. See [the follow-up evidence](lab-clarity-and-layout.md) for its separate verification and publication caveat; the visual sweep below describes the earlier release.

Screenshots are full-page captures at the viewport above. The following page-by-page visual sweep passed:

| Rendered page | Result | Hints | Code-copy controls | Screenshot |
| --- | --- | ---: | ---: | --- |
| `index.html` | Pass | 0 | 0 | [index.png](screenshots/index.png) |
| `00-common-setup/index.html` | Pass | 0 | 1 | [00-common-setup](screenshots/00-common-setup__index.png) |
| `01-devom-setup/index.html` | Pass | 0 | 6 | [01-devom-setup](screenshots/01-devom-setup__index.png) |
| `02-bugbazaar-setup/index.html` | Pass | 0 | 4 | [02-bugbazaar-setup](screenshots/02-bugbazaar-setup__index.png) |
| `09-jwt-account-state/index.html` | Pass | 1 | 8 | [09-jwt-account-state](screenshots/09-jwt-account-state__index.png) |
| `10-otp-bypass/index.html` | Pass | 1 | 5 | [10-otp-bypass](screenshots/10-otp-bypass__index.png) |
| `14-command-injection/index.html` | Pass | 1 | 7 | [14-command-injection](screenshots/14-command-injection__index.png) |
| `24-file-upload/index.html` | Pass | 1 | 5 | [24-file-upload](screenshots/24-file-upload__index.png) |
| `25-path-traversal/index.html` | Pass | 1 | 5 | [25-path-traversal](screenshots/25-path-traversal__index.png) |
| `26-transactions/index.html` | Pass | 1 | 7 | [26-transactions](screenshots/26-transactions__index.png) |
| `27-cloud-database/index.html` | Pass | 1 | 17 | [27-cloud-database](screenshots/27-cloud-database__index.png) |
| `28-bola/index.html` | Pass | 1 | 5 | [28-bola](screenshots/28-bola__index.png) |
| `29-components/index.html` | Pass | 1 | 3 | [29-components](screenshots/29-components__index.png) |
| `30-runtime-bypass/index.html` | Pass | 1 | 8 | [30-runtime-bypass](screenshots/30-runtime-bypass__index.png) |
| `404.html` (GitHub Pages fallback) | Pass | 0 | 0 | [404](screenshots/404.png) |
| `404/index.html` | Pass | 0 | 0 | [404 source page](screenshots/404__index.png) |
| `coverage-analysis/index.html` | Pass | 0 | 0 | [coverage analysis](screenshots/coverage-analysis__index.png) |
| `downloads/index.html` | Pass | 0 | 1 | [downloads](screenshots/downloads__index.png) |

## Archive verification

The same archive is linked from the rendered downloads page and present in the built site. The generated archive remains a local build output; it is ignored by Git.

```text
LabKit-linux-x86_64.zip
SHA-256  2113cc896dde71761e32d4f1c01eefe6cb8b8e5d371b8aaa070d03d7221e9b88
```

The automated browser sweep uses a loopback server mounted at the configured Pages base path and blocks external requests. No live deployment has been verified by this pre-merge report; that check is recorded after the protected-main PR deploys.
