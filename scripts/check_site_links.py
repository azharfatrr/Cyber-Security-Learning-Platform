#!/usr/bin/env python3
"""Check local links and assets in a rendered MkDocs site."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


LABKIT_PATH = Path("assets/labkit/LabKit-linux-x86_64.zip")


class HtmlReferences(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        for name in ("href", "src"):
            value = attributes.get(name)
            if value:
                self.references.append(value.strip())
        if attributes.get("id"):
            self.anchors.add(attributes["id"] or "")
        if tag == "a" and attributes.get("name"):
            self.anchors.add(attributes["name"] or "")


def parse_html(path: Path) -> HtmlReferences:
    parser = HtmlReferences()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def configured_site_url() -> str | None:
    config = Path("mkdocs.yml")
    if not config.is_file():
        return None
    match = re.search(r"(?m)^site_url:\s*[\"']?([^\"'\s]+)", config.read_text())
    return match.group(1) if match else None


def main() -> int:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()
    if len(sys.argv) > 2:
        print("Usage: check_site_links.py [rendered-site-directory]", file=sys.stderr)
        return 2
    if not site.is_dir():
        print(f"Rendered site directory not found: {site}", file=sys.stderr)
        return 2

    site_url = configured_site_url()
    site_address = urlsplit(site_url) if site_url else None
    base_path = site_address.path if site_address else "/"
    base_path = base_path if base_path.endswith("/") else f"{base_path}/"
    failures: list[str] = []
    archive = site / LABKIT_PATH
    if not archive.is_file() or archive.stat().st_size == 0:
        failures.append(f"LabKit archive missing or empty: {LABKIT_PATH.as_posix()}")

    html_files = sorted(site.rglob("*.html"))
    if not html_files:
        failures.append("No rendered HTML pages found")
    parsed_pages = {path: parse_html(path) for path in html_files}
    external_urls: set[str] = set()
    local_references = 0

    for source, page in parsed_pages.items():
        for value in page.references:
            parsed = urlsplit(value)
            same_site = (
                site_address is not None
                and parsed.scheme == site_address.scheme
                and parsed.netloc == site_address.netloc
                and parsed.path.startswith(base_path)
            )
            if (parsed.scheme or parsed.netloc) and not same_site:
                external_urls.add(value)
                continue

            raw_path = unquote(parsed.path)
            rooted_path = raw_path.startswith("/") or same_site
            if rooted_path and base_path != "/" and raw_path.startswith(base_path):
                raw_path = raw_path[len(base_path):]
            target = source if not raw_path else (site / raw_path.lstrip("/") if rooted_path else source.parent / raw_path)
            target = target.resolve()
            if not target.is_relative_to(site):
                failures.append(f"{source.relative_to(site)}: {value!r} escapes the rendered site")
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                failures.append(f"{source.relative_to(site)}: missing target for {value!r}")
                continue

            local_references += 1
            if parsed.fragment and target.suffix.lower() in (".html", ".htm"):
                target_page = parsed_pages.get(target)
                if target_page is None:
                    target_page = parse_html(target)
                    parsed_pages[target] = target_page
                if unquote(parsed.fragment) not in target_page.anchors:
                    failures.append(f"{source.relative_to(site)}: missing fragment for {value!r}")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        print(f"Local-site check failed: {len(failures)} issue(s).")
        return 1

    for url in sorted(external_urls):
        print(f"External URL not fetched: {url}")
    print(
        f"Local-site check passed: {local_references} local references resolved; "
        f"{len(external_urls)} external URLs not fetched."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
