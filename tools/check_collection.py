#!/usr/bin/env python3
"""Check skill metadata, bundled files and local Markdown links; never run skills."""

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


REQUIRED = {
    "software-factory", "new-feature", "code-structure",
    "evidence-driven-testing", "unslop",
}
MANUAL_ONLY = {"software-factory", "new-feature"}
REMOVED = {"before-and-after", "greploop", "greploop-apps"}
BUNDLED = {"software-factory/WORKFLOW.md", "software-factory/PREREQUISITES.md"}
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys rather than silently replacing values."""

    def construct_mapping(self, node, deep=False):
        keys = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in keys:
                raise ValueError(f"duplicate frontmatter key: {key}")
            keys.add(key)
        return super().construct_mapping(node, deep=deep)


def without_fences(text):
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def anchors(text):
    result = set()
    counts = {}
    for line in without_fences(text).splitlines():
        heading = re.match(r"^#{1,6}\s+(.+?)(?:\s+#+)?$", line)
        if not heading:
            continue
        title = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", heading.group(1))
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        number = counts.get(slug, 0)
        counts[slug] = number + 1
        result.add(f"{slug}-{number}" if number else slug)
    return result


def check(root):
    errors = []
    skill_files = sorted(root.glob("*/SKILL.md"))
    installed = {path.parent.name for path in skill_files}
    for name in sorted(REQUIRED - installed):
        errors.append(f"missing required skill: {name}/SKILL.md")
    for name in sorted(REMOVED):
        if (root / name).exists():
            errors.append(f"removed skill directory: {name}")
    for relative in sorted(BUNDLED):
        if not (root / relative).is_file():
            errors.append(f"missing bundled reference: {relative}")

    for path in skill_files:
        label = str(path.relative_to(root))
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        try:
            if not lines or lines[0] != "---":
                raise ValueError("missing YAML frontmatter")
            end = lines.index("---", 1)
            data = yaml.load("\n".join(lines[1:end]), Loader=UniqueLoader)
            if not isinstance(data, dict):
                raise ValueError("frontmatter must be a mapping")
            name = data.get("name")
            if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
                errors.append(f"{label}: invalid skill name")
            if name != path.parent.name:
                errors.append(f"{label}: name must match directory")
            description = data.get("description")
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                errors.append(f"{label}: description must contain 1-1024 characters")
            if "disable-model-invocation" in data and not isinstance(data["disable-model-invocation"], bool):
                errors.append(f"{label}: disable-model-invocation must be a YAML boolean")
            if path.parent.name in MANUAL_ONLY and data.get("disable-model-invocation") is not True:
                errors.append(f"{label}: must remain manual-only")
        except (ValueError, TypeError, yaml.YAMLError) as exc:
            errors.append(f"{label}: invalid frontmatter: {exc}")

    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        label = str(path.relative_to(root))
        for name in sorted(REMOVED):
            if re.search(r"/skill:" + re.escape(name) + r"\b", text):
                errors.append(f"{label}: invocation of removed skill: {name}")
        for match in LINK.finditer(without_fences(text)):
            destination = match.group(1).strip("<>")
            url = urlsplit(destination)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.exists():
                errors.append(f"{label}: missing link target: {destination}")
            elif url.fragment and target.is_file() and target.suffix == ".md":
                if unquote(url.fragment) not in anchors(target.read_text(encoding="utf-8")):
                    errors.append(f"{label}: missing heading anchor: {destination}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    errors = check(root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Collection checks passed. Agent behavior and external dependencies were not tested.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
