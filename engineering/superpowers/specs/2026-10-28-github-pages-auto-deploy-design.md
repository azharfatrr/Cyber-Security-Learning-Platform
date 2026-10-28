# GitHub Pages Auto-Deployment

## Intent

Publish the MkDocs site automatically whenever `main` receives a push, so the GitHub Pages site stays current without a manual deploy command.

## Goals and constraints

- Run a strict MkDocs build in GitHub Actions, then publish its output to GitHub Pages.
- Deploy only from `main`; other branches must not update the public site.
- Use the repository's existing `requirements.txt` and MkDocs configuration.
- Keep deployment notes accurate and do not publish internal design notes as site pages.

## Non-goals

- Preview deployments for pull requests or other branches.
- Custom domains or alternate hosting providers.

## Approaches

- **GitHub Actions with the Pages artifact workflow (chosen):** builds and deploys automatically on `main` pushes, with a strict build as a gate. This directly meets the request and avoids maintaining a generated `gh-pages` branch.
- **Manual `mkdocs gh-deploy`:** simple, but requires a person to publish after every push, so it does not meet the automatic-update requirement.

## Decisions and implementation notes

- Add a workflow triggered by pushes to `main`, with minimum Pages deployment permissions and serialized deployments.
- Use the official GitHub Pages configure, upload-artifact, and deploy actions.
- Update `PUBLISHING.txt` to describe automatic publishing and the required one-time repository setting: Pages source must be GitHub Actions.
- Push the current pending site changes along with the workflow so the first successful deployment contains them.

## Verification and remaining dependency

- Run the existing site tests and strict build locally before pushing.
- Confirm the workflow run and published URL after the push. The first run depends on GitHub Pages being enabled with the GitHub Actions source in repository settings.
