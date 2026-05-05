#!/usr/bin/env python3
"""Markdown to HTML previewer using mistune."""

import argparse
import sys
from pathlib import Path

import mistune


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert Markdown file to a standalone HTML page"
    )
    parser.add_argument("input", type=Path, help="Input .md file")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Output .html file (default: <input>.html)"
    )
    return parser.parse_args()


def markdown_to_html(md_text: str) -> str:
    markdown = mistune.create_markdown(
        escape=False,
        hard_wrap=False,
        plugins=["table", "task_lists", "url"],
    )
    return markdown(md_text)


def wrap_html(body: str, title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body {{
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
}}
h1, h2, h3, h4, h5, h6 {{
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    line-height: 1.3;
}}
h1 {{ font-size: 2em; border-bottom: 2px solid #eee; padding-bottom: 0.3em; }}
h2 {{ font-size: 1.5em; border-bottom: 1px solid #eee; padding-bottom: 0.2em; }}
code {{
    background: #f4f4f4;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 0.9em;
}}
pre {{
    background: #2d2d2d;
    color: #f8f8f2;
    padding: 1em;
    border-radius: 6px;
    overflow-x: auto;
}}
pre code {{
    background: none;
    padding: 0;
    color: inherit;
}}
blockquote {{
    border-left: 4px solid #ddd;
    margin-left: 0;
    padding-left: 1em;
    color: #666;
}}
table {{
    border-collapse: collapse;
    width: 100%;
}}
th, td {{
    border: 1px solid #ddd;
    padding: 0.5em 1em;
    text-align: left;
}}
th {{ background: #f8f8f8; }}
img {{ max-width: 100%; height: auto; }}
a {{ color: #0366d6; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def main():
    args = parse_args()

    if not args.input.exists():
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    md_text = args.input.read_text(encoding="utf-8")
    body = markdown_to_html(md_text)

    output_path = args.output or args.input.with_suffix(".html")
    title = args.input.stem.replace("-", " ").replace("_", " ").title()

    html = wrap_html(body, title)
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
