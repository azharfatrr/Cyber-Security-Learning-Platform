# Cyber Security Learning Platform

Guided Android application and API security labs for an isolated training environment.

[Open the lab website](https://azharfatrr.github.io/Cyber-Security-Learning-Platform/)

## What's inside

- Ten guided labs covering authentication, file handling, API security, and Android components.
- Linux/Bash setup and walkthrough instructions.
- Coverage notes that identify source evidence and gaps.

## Run the site locally

From the repository root:

```bash
python3 -m pip install -r requirements.txt
python3 -m mkdocs serve
```

Open the local URL printed by MkDocs. To check a production build:

```bash
python3 -m mkdocs build --strict
```

## Lab readiness and safety

All ten walkthroughs are complete and were tested end to end. Labs 09, 10, 14, 24–26, and 28–30 were tested on 29 October 2026; Lab 27 was tested on 2 November 2026 against the repository's local Firebase Storage emulator. Every page includes observed output, and each one states what its run covered. Use only an isolated, disposable environment with synthetic data; do not use production systems, real accounts, personal data, or upstream cloud services.

## Lab guides

- [Common setup](docs/00-common-setup.md)
- [JWT account state](docs/09-jwt-account-state.md)
- [OTP authentication](docs/10-otp-bypass.md)
- [Command injection](docs/14-command-injection.md)
- [File upload](docs/24-file-upload.md)
- [Path traversal](docs/25-path-traversal.md)
- [Transaction validation](docs/26-transactions.md)
- [Cloud storage](docs/27-cloud-database.md) — local Firebase Storage emulator and synthetic data
- [Object authorization](docs/28-bola.md)
- [Android components](docs/29-components.md)
- [Runtime bypass](docs/30-runtime-bypass.md)
- [Coverage analysis](docs/coverage-analysis.md)
