# GitHub README Separation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the repository's GitHub README render cleanly while preserving the styled MkDocs catalog homepage.

**Architecture:** Move the existing MkDocs homepage source from `docs/README.md` to `docs/index.md` and update the explicit Home navigation entry. Add a separate root `README.md` written in plain GitHub-Flavored Markdown with project, setup, and safety information.

**Tech Stack:** Markdown, MkDocs 1.6.1, Material for MkDocs 9.7.7, Python unittest.

**Spec:** `engineering/superpowers/specs/2026-10-28-github-readme-separation-design.md`

## Global Constraints

- The root README must not contain MkDocs-only HTML or attribute-list syntax.
- Preserve the existing styled catalog and its links as the MkDocs homepage.
- Do not change lab instructions, visual styles, or deployment behavior in this task.
- Keep internal design and plan notes outside the publishable `docs/` directory.

## Review Focus

- Root README missing: test that the root README exists and contains the project title.
- MkDocs Home still points to the old filename: test the `Home: index.md` navigation entry.
- Homepage styling/content lost in the move: test generated home HTML still has the catalog hero and lab cards.
- GitHub-only README accidentally contains MkDocs syntax: test it excludes `<div` and `.md-button` attribute-list markup.
- Local setup commands become inaccurate: assert the README contains the existing `python3 -m mkdocs serve` command.

---

### Task 1: Separate the GitHub README and MkDocs home source

**Files:**
- Create: `README.md`
- Move: `docs/README.md` to `docs/index.md`
- Modify: `mkdocs.yml`
- Modify: `test_site.py`

**Interfaces:**
- Consumes: current MkDocs home source, `requirements.txt`, and existing site test.
- Produces: a plain root README and an unchanged styled MkDocs Home sourced from `docs/index.md`.

- [x] **Step 1: Add a failing regression test**

Add `test_github_readme_is_plain_markdown_and_site_home_is_preserved` to `test_site.py`. Assert that root `README.md` exists, contains `Cyber Security Learning Platform` and `python3 -m mkdocs serve`, contains neither `<div` nor `.md-button` attribute-list syntax, and that `mkdocs.yml` maps Home to `index.md`. Retain the existing generated-home assertions for the catalog hero and cards.

- [x] **Step 2: Run the test and verify it fails for the missing root README**

Run: `python -m unittest -v test_site`
Expected: FAIL because there is no root `README.md` yet.

- [x] **Step 3: Move the site home, add the root README, and update navigation**

Move `docs/README.md` unchanged to `docs/index.md`. Write a concise GitHub-Flavored Markdown root README with project summary, local installation/serve/build commands, a pointer to the GitHub Pages site, and the existing authorized/synthetic-data and untested-lab warning. Change `mkdocs.yml` to use `Home: index.md`.

- [x] **Step 4: Run the site test and strict build**

Run: `python -m unittest -v test_site`
Expected: PASS.

Run: `python -m mkdocs build --strict --site-dir <temporary-directory>`
Expected: build completes with exit code 0 and the home page retains the catalog.

- [ ] **Step 5: Keep the README split for the automatic Pages deployment push**

Do not push this change separately before the approved Pages workflow exists. Update the auto-deployment plan's pending-file list from `docs/README.md` to `docs/index.md` plus root `README.md`, then include these files in the initial workflow push.
