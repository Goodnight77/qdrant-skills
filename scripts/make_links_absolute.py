#!/usr/bin/env python3
"""Convert relative markdown links to absolute URLs for the deployed site."""

import os
import re

BASE_URL = "https://skills.qdrant.tech"
PUBLIC_DIR = "public"

LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')


def make_absolute(filepath, url, public_dir):
    if url.startswith(("http://", "https://", "/", "#", "mailto:")):
        return url
    file_dir = os.path.relpath(os.path.dirname(filepath), public_dir)
    if file_dir == ".":
        abs_path = url
    else:
        abs_path = os.path.normpath(os.path.join(file_dir, url))
    return f"{BASE_URL}/{abs_path}"


def run(public_dir):
    for root, _dirs, files in os.walk(public_dir):
        for filename in files:
            if not filename.endswith(".md"):
                continue
            filepath = os.path.join(root, filename)
            with open(filepath) as f:
                content = f.read()
            new_content = LINK_RE.sub(
                lambda m: f"[{m.group(1)}]({make_absolute(filepath, m.group(2), public_dir)})",
                content,
            )
            if new_content != content:
                with open(filepath, "w") as f:
                    f.write(new_content)


if __name__ == "__main__":
    run(PUBLIC_DIR)
