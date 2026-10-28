# GitHub README and MkDocs Home Separation

## Intent

Make the repository's GitHub landing page readable while preserving the custom MkDocs catalog homepage.

## Goals and constraints

- Provide a plain GitHub-Flavored Markdown `README.md` at the repository root with a project overview, local run/build instructions, and safety note.
- Keep the existing styled catalog as the MkDocs home page, using `docs/index.md` as its source.
- Avoid MkDocs-only HTML and attribute syntax in the root README.
- Keep the existing site design, lab content, and navigation behavior unchanged.

## Approaches

- **Separate repository README from site home (chosen):** move the existing `docs/README.md` source to `docs/index.md` and add a root README. This gives GitHub and MkDocs appropriate Markdown without sacrificing the styled site.
- **Rewrite the current homepage as plain Markdown:** would render on GitHub but lose the custom hero, cards, and category styling on the site.

## Verification

- Update MkDocs navigation to use `index.md` as Home.
- Test that the generated homepage still contains the hero and lab catalog, and that the root README contains no MkDocs-only HTML attributes.
- Run `python -m unittest -v test_site` and a strict MkDocs build.
