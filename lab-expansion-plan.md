# Guided Lab Expansion Plan

**Goal:** Expand the ten employee lab briefs into guided walkthroughs using the agreed structure.

**Approach:** Keep one Markdown page per module and reuse the existing common setup. Write instructions from the pinned source evidence, then test each exercise before claiming that its outputs or screenshots are verified.

## Constraints

- Cover modules 9, 10, 14, and 24–30 only.
- Use Devom and BugBazaar where each fits; keep module 27 gated on an authorized cloud environment.
- Preserve isolated-lab safety limits, optional hints, and the source and runtime verification status.
- Do not invent screenshots, expected results, commands, or setup steps.

## Tasks

**Status (29 October 2026):** All tasks are complete. Internal links and images resolve, the strict MkDocs build and site tests pass in CI, and every page states its tested result or environment requirement. Lab 27 requires an authorized Firebase environment.

- [x] Document the agreed reusable lab structure: overview, prerequisites, scenario, guided stages, hints, evidence, cleanup, and review.
- [x] Expand Devom labs 9, 10, 14, 24, 25, 26 and 28 with source-backed steps, expected observations, and lab-specific cleanup; replace source-derived expectations with observed results after each test run.
- [x] Expand BugBazaar labs 29 and 30 using inspected source; module 27 requires an authorized cloud environment.
- [x] Check all guides for coverage, source fidelity, safety, working links, and consistency; run the MkDocs site test and record the verification status.
