#!/usr/bin/env python3
"""Inline a simple Vite/static dist folder into one self-contained HTML file.

Best results require a single JS bundle and a single CSS bundle. The script inlines
local stylesheets, local scripts, common media/font assets, and CSS url(...) values.
It intentionally fails when unresolved local JS/CSS references remain.
"""
from __future__ import annotations

import argparse
import base64
import mimetypes
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

STYLE_LINK_RE = re.compile(
    r'<link\b(?=[^>]*\brel=["\']stylesheet["\'])(?=[^>]*\bhref=["\']([^"\']+)["\'])[^>]*>',
    re.IGNORECASE,
)
SCRIPT_RE = re.compile(
    r'<script\b([^>]*?)\bsrc=["\']([^"\']+)["\']([^>]*)>\s*</script>',
    re.IGNORECASE | re.DOTALL,
)
MODULE_PRELOAD_RE = re.compile(
    r'<link\b(?=[^>]*\brel=["\']modulepreload["\'])[^>]*>', re.IGNORECASE
)
ASSET_ATTR_RE = re.compile(
    r'(?P<prefix>\b(?:src|poster|href)=["\'])(?P<url>[^"\']+)(?P<suffix>["\'])',
    re.IGNORECASE,
)
CSS_URL_RE = re.compile(r'url\(\s*(["\']?)([^)"\']+)\1\s*\)', re.IGNORECASE)
LOCAL_CSS_JS_RE = re.compile(
    r'(?:src|href)=["\'](?:\.?\.?/|/)?[^"\']+\.(?:js|css)(?:\?[^"\']*)?["\']',
    re.IGNORECASE,
)
DYNAMIC_IMPORT_RE = re.compile(r'import\(\s*["\'][^"\']+\.js(?:\?[^"\']*)?["\']\s*\)')


def is_external(url: str) -> bool:
    stripped = url.strip()
    return (
        not stripped
        or stripped.startswith(("data:", "blob:", "http://", "https://", "//", "#", "mailto:", "tel:"))
    )


def local_path(url: str, base_dir: Path, dist_dir: Path) -> Path | None:
    if is_external(url):
        return None
    path_part = unquote(urlsplit(url).path)
    if path_part.startswith("/"):
        candidate = dist_dir / path_part.lstrip("/")
    else:
        candidate = base_dir / path_part
    try:
        resolved = candidate.resolve()
        resolved.relative_to(dist_dir.resolve())
    except (ValueError, OSError):
        return None
    return resolved


def as_data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    mime = mime or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def inline_css_urls(css: str, css_file: Path, dist_dir: Path) -> str:
    def repl(match: re.Match[str]) -> str:
        url = match.group(2).strip()
        path = local_path(url, css_file.parent, dist_dir)
        if path and path.is_file():
            return f'url("{as_data_uri(path)}")'
        return match.group(0)

    return CSS_URL_RE.sub(repl, css)


def strip_src_attribute(attrs_before: str, attrs_after: str) -> str:
    attrs = (attrs_before + " " + attrs_after).strip()
    attrs = re.sub(r'\s+', ' ', attrs)
    return f" {attrs}" if attrs else ""


def build_single_html(dist_dir: Path, output: Path) -> None:
    index = dist_dir / "index.html"
    if not index.is_file():
        raise FileNotFoundError(f"Missing {index}")

    html = index.read_text(encoding="utf-8")

    def style_repl(match: re.Match[str]) -> str:
        url = match.group(1)
        path = local_path(url, dist_dir, dist_dir)
        if not path or not path.is_file():
            raise FileNotFoundError(f"Stylesheet not found: {url}")
        css = inline_css_urls(path.read_text(encoding="utf-8"), path, dist_dir)
        return f"<style>\n{css}\n</style>"

    html = STYLE_LINK_RE.sub(style_repl, html)
    html = MODULE_PRELOAD_RE.sub("", html)

    def script_repl(match: re.Match[str]) -> str:
        attrs_before, url, attrs_after = match.groups()
        path = local_path(url, dist_dir, dist_dir)
        if not path or not path.is_file():
            raise FileNotFoundError(f"Script not found: {url}")
        script = path.read_text(encoding="utf-8")
        attrs = strip_src_attribute(attrs_before, attrs_after)
        return f"<script{attrs}>\n{script}\n</script>"

    html = SCRIPT_RE.sub(script_repl, html)

    def asset_repl(match: re.Match[str]) -> str:
        url = match.group("url")
        path = local_path(url, dist_dir, dist_dir)
        if path and path.is_file() and path.suffix.lower() not in {".html", ".js", ".css"}:
            return match.group("prefix") + as_data_uri(path) + match.group("suffix")
        return match.group(0)

    html = ASSET_ATTR_RE.sub(asset_repl, html)

    unresolved = LOCAL_CSS_JS_RE.findall(html)
    dynamic = DYNAMIC_IMPORT_RE.findall(html)
    if unresolved or dynamic:
        details = []
        if unresolved:
            details.append("unresolved local JS/CSS references: " + ", ".join(unresolved[:8]))
        if dynamic:
            details.append("dynamic JS imports remain: " + ", ".join(dynamic[:8]))
        raise RuntimeError(
            "Cannot make a reliable single-file preview; configure a single Vite bundle first. "
            + " | ".join(details)
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist_dir", type=Path, help="Directory containing index.html")
    parser.add_argument("output", type=Path, help="Output standalone HTML path")
    args = parser.parse_args()

    try:
        build_single_html(args.dist_dir.resolve(), args.output.resolve())
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Created standalone preview: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
