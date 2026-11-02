# Guided Lab Expansion Plan

**Goal:** Expand the ten employee lab briefs into guided walkthroughs using the agreed structure.

**Approach:** Keep one Markdown page per module and reuse the existing common setup. Write instructions from the pinned source evidence, then test each exercise before claiming that its outputs or screenshots are verified.

## Constraints

- Cover modules 9, 10, 14, and 24–30 only.
- Use Devom and BugBazaar where each fits; module 27 uses the repository's local Firebase Storage emulator.
- Preserve isolated-lab safety limits, optional hints, and the source and runtime verification status.
- Do not invent screenshots, expected results, commands, or setup steps.

## Tasks

**Status (2 November 2026):** All tasks are complete. Internal links and images resolve, the strict MkDocs build and site tests pass, and every page states its tested result or environment requirement. All ten labs were tested end to end; Lab 27 runs against the repository's local Firebase Storage emulator.

- [x] Document the agreed reusable lab structure: overview, prerequisites, scenario, guided stages, hints, evidence, cleanup, and review.
- [x] Expand Devom labs 9, 10, 14, 24, 25, 26 and 28 with source-backed steps, expected observations, and lab-specific cleanup; replace source-derived expectations with observed results after each test run.
- [x] Expand BugBazaar labs 29 and 30 using inspected source; module 27 uses the local emulator variant and its synthetic fixtures.
- [x] Check all guides for coverage, source fidelity, safety, working links, and consistency; run the MkDocs site test and record the verification status.
