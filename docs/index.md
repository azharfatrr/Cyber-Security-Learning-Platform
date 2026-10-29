---
hide:
  - toc
---

<div class="catalog-hero" markdown="1">

<span class="catalog-kicker">CYBER SECURITY LEARNING PLATFORM</span>

# Android <span class="hero-gradient">Security Labs</span>

Guides for testing Android applications and APIs in an isolated lab.

<div class="hero-facts"><span>10 lab guides</span><span>Devom + BugBazaar</span><span>Linux setup</span></div>

[Start with setup](00-common-setup.md){ .md-button .md-button--primary }
[Browse the catalog](#lab-catalog){ .md-button }

<div class="hero-visual"><img class="hero-device" src="assets/android-lab.svg" alt="" /></div>

</div>

<div class="catalog-notice" markdown="1">
**Before you start:** All ten walkthroughs are complete. Nine were tested end to end on 29 October 2026 and include observed output and screenshots. Lab 27 requires an authorized Firebase environment; its page states what that environment must provide. Use only an isolated, authorized environment with synthetic data. [Review the common prerequisites](00-common-setup.md), then follow the setup module for the target used by your lab.
</div>

## Lab catalog

Choose a topic and open a lab. The numbers match the training curriculum.

<nav class="catalog-jump" aria-label="Jump to a lab category">
  <a href="#authentication">Authentication</a>
  <a href="#file-handling">File handling</a>
  <a href="#api-security">API security</a>
  <a href="#android-components">Android components</a>
</nav>

<div class="category-heading auth-heading" markdown="1">

<span class="category-icon" aria-hidden="true">01</span>

### Authentication

Test account state and second-factor checks.

</div>

<div class="grid cards auth-cards" markdown>

- **09 · [JWT account state](09-jwt-account-state.md)**  
  <span class="card-meta">Devom</span><br>
  Check how a suspended account's session is handled.

- **10 · [OTP authentication](10-otp-bypass.md)**  
  <span class="card-meta">Devom</span><br>
  Trace token issuance and second-factor verification.

</div>

<div class="category-heading file-heading" markdown="1">

<span class="category-icon" aria-hidden="true">02</span>

### File handling

Investigate upload processing and file retrieval.

</div>

<div class="grid cards file-cards" markdown>

- **14 · [Command injection](14-command-injection.md)**  
  <span class="card-meta">Devom</span><br>
  Follow a filename into server-side processing.

- **24 · [File upload](24-file-upload.md)**  
  <span class="card-meta">Devom</span><br>
  Test how the application handles an unexpected file type.

- **25 · [Path traversal](25-path-traversal.md)**  
  <span class="card-meta">Devom</span><br>
  Check a retrieval boundary using a harmless marker.

</div>

<div class="category-heading api-heading" markdown="1">

<span class="category-icon" aria-hidden="true">03</span>

### API security

Examine transactions, object access, and database permissions.

</div>

<div class="grid cards api-cards" markdown>

- **26 · [Transaction validation](26-transactions.md)**  
  <span class="card-meta">Devom</span><br>
  Compare the results of valid and invalid transfers.

- **27 · [Cloud database](27-cloud-database.md)**  
  <span class="card-meta">BugBazaar · Requires Firebase environment</span><br>
  Requires an authorized, disposable cloud environment.

- **28 · [Object authorization](28-bola.md)**  
  <span class="card-meta">Devom</span><br>
  Test access between two assigned lab accounts.

</div>

<div class="category-heading android-heading" markdown="1">

<span class="category-icon" aria-hidden="true">04</span>

### Android components

Inspect app components and client-side decisions.

</div>

<div class="grid cards android-cards" markdown>

- **29 · [Android components](29-components.md)**  
  <span class="card-meta">BugBazaar</span><br>
  Test access to an exported component.

- **30 · [Runtime bypass](30-runtime-bypass.md)**  
  <span class="card-meta">BugBazaar</span><br>
  Inspect a local passcode check at runtime.

</div>

The [coverage analysis](coverage-analysis.md) lists source evidence and gaps. Do not contact upstream cloud services or use real accounts, production systems, or personal data.
