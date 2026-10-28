# GitHub Pages Auto-Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatically build and publish the MkDocs site whenever `main` receives a push.

**Architecture:** A GitHub Actions workflow runs the current unittest suite and a strict MkDocs build, uploads the `site/` artifact, and deploys it to GitHub Pages. Publishing is restricted to `main`; a serialized Pages deployment job uses the official GitHub Pages actions and minimum job permissions.

**Tech Stack:** GitHub Actions, Python 3.12, MkDocs 1.6.1, Material for MkDocs 9.7.7, GitHub Pages artifact deployment.

**Spec:** `engineering/superpowers/specs/2026-10-28-github-pages-auto-deploy-design.md`

## Global Constraints

- Trigger deployment only on pushes to `main`.
- Run the site tests and `python -m mkdocs build --strict` before deployment.
- Use the existing `requirements.txt` and MkDocs configuration.
- Do not add pull-request previews, alternate deployment branches, or custom-domain setup.
- Internal design and plan notes stay outside the publishable `docs/` directory.

## Review Focus

- A push to any branch other than `main` must not publish: test the workflow trigger lists only `main`.
- A failed test or strict build must prevent deployment: test the deploy job depends on the successful build job.
- The deploy job must not receive broad repository write access: test its Pages, OIDC, and artifact-read permissions.
- Concurrent pushes must not cancel an active production deploy: test Pages concurrency uses `cancel-in-progress: false`.
- First deployment requires Pages Actions source setup: test `PUBLISHING.txt` explains the one-time repository setting and confirm the workflow run.

---

### Task 1: Automate GitHub Pages deployment

**Files:**
- Create: `.github/workflows/deploy.yml`
- Modify: `PUBLISHING.txt`
- Modify: `test_site.py`
- Include existing pending site changes in root `README.md`, `docs/index.md`, `docs/stylesheets/extra.css`, `mkdocs.yml`, and `test_site.py`.

**Interfaces:**
- Consumes: `requirements.txt`, `mkdocs.yml`, and `test_site.py`.
- Produces: a `main`-push workflow that publishes the strict MkDocs build to GitHub Pages.

- [x] **Step 1: Add a failing workflow regression test**

Add `test_pages_workflow_builds_before_deploying_main` to `test_site.py`. Assert that the workflow triggers only on `main`, runs `python -m unittest -v test_site` and `python -m mkdocs build --strict`, gates deployment on the build job, grants only the needed deployment permissions, serializes Pages deployment without cancelling an active deploy, and uses the Pages deploy action. Also assert that `PUBLISHING.txt` documents the GitHub Actions Pages source setting.

- [x] **Step 2: Run the test and verify it fails for the missing workflow**

Run: `python -m unittest -v test_site`
Expected: FAIL because `.github/workflows/deploy.yml` does not exist yet.

- [x] **Step 3: Add the workflow and update publishing instructions**

Use `actions/checkout@v7`, `actions/setup-python@v7` with Python `3.12`, `actions/configure-pages@v6`, `actions/upload-pages-artifact@v5`, and `actions/deploy-pages@v5`. Run the unittest suite, install `requirements.txt`, and build with `--strict` before uploading `site/`. Run Pages configuration and deployment in a job dependent on build; grant it `pages: write`, `id-token: write`, and `actions: read`, while keeping build's repository contents permission read-only. Set Pages concurrency to `cancel-in-progress: false`. Update `PUBLISHING.txt` from the manual `gh-deploy` instructions to describe deployment on pushes to `main` and the one-time GitHub Pages source setting.

- [x] **Step 4: Run the full site test and strict build**

Run: `python -m unittest -v test_site`
Expected: PASS.

Run: `python -m mkdocs build --strict --site-dir <temporary-directory>`
Expected: build completes with exit code 0.

- [ ] **Step 5: Commit and push the deployment setup and pending site edits**

Include the approved deployment and README design notes, both plans, root `README.md`, `docs/index.md`, workflow, publishing instructions, tests, and pending metadata styling changes. Push to `origin main` to trigger the first workflow run.

- [ ] **Step 6: Verify the GitHub Actions deployment**

Confirm the workflow completes successfully and the Pages URL `https://azharfatrr.github.io/Cyber-Security-Learning-Platform/` serves the site. If GitHub reports that Pages is not configured for Actions, set **Settings → Pages → Build and deployment → Source → GitHub Actions**, then rerun the workflow.
