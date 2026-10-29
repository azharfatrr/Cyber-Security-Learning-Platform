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

All ten walkthroughs are complete. Nine were tested end to end on 29 October 2026, and their pages include observed output and screenshots. The cloud database lab (27) requires an authorized, disposable Firebase environment. Use only an isolated, authorized environment with synthetic data; do not use production systems, real accounts, personal data, or upstream cloud services.

## Lab guides

- [Common setup](docs/00-common-setup.md)
- [JWT account state](docs/09-jwt-account-state.md)
- [OTP authentication](docs/10-otp-bypass.md)
- [Command injection](docs/14-command-injection.md)
- [File upload](docs/24-file-upload.md)
- [Path traversal](docs/25-path-traversal.md)
- [Transaction validation](docs/26-transactions.md)
- [Cloud database](docs/27-cloud-database.md) — requires an authorized Firebase environment
- [Object authorization](docs/28-bola.md)
- [Android components](docs/29-components.md)
- [Runtime bypass](docs/30-runtime-bypass.md)
- [Coverage analysis](docs/coverage-analysis.md)
