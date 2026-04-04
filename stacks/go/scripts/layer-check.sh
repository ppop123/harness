#!/usr/bin/env bash
# layer-check.sh — Structural dependency test for Go
#
# Enforces: Domain → Repository → Service → Handler → Router
# Lower layers MUST NOT depend on higher layers.
# This script performs language-aware dependency extraction where possible.
#
# Usage: bash scripts/layer-check.sh [src_dir]
#
# Exit code 0 = pass, 1 = violations found, 2 = runtime error

set -euo pipefail

SRC_DIR="${1:-.}"
RED='\033[0;31m'
NC='\033[0m'

PYTHON_BIN="$(command -v python3 || command -v python || true)"
if [[ -z "$PYTHON_BIN" ]]; then
  echo -e "${RED}python3 or python is required for language-aware layer checks.${NC}"
  exit 2
fi

"$PYTHON_BIN" - "$SRC_DIR" <<'PY'
import ast
import json
import pathlib
import re
import sys

SRC_DIR = pathlib.Path(sys.argv[1]).resolve()
LANG = 'Go'
EXT = 'go'
RULES = json.loads('[{"layer": "Domain", "source_aliases": ["internal/domain", "domain"], "forbidden": ["internal/repository", "repository", "internal/service", "service", "internal/handler", "handler", "router", "cmd/server", "routes"]}, {"layer": "Repository", "source_aliases": ["internal/repository", "repository"], "forbidden": ["internal/service", "service", "internal/handler", "handler", "router", "cmd/server", "routes"]}, {"layer": "Service", "source_aliases": ["internal/service", "service"], "forbidden": ["internal/handler", "handler", "router", "cmd/server", "routes"]}, {"layer": "Handler", "source_aliases": ["internal/handler", "handler"], "forbidden": ["router", "cmd/server", "routes"]}]')

RED = "\033[0;31m"
GREEN = "\033[0;32m"
NC = "\033[0m"
FALLBACK_SCAN_LANGS = ("Swift",)


def iter_source_files(source_aliases):
    seen = set()
    results = []
    for alias in source_aliases:
        alias_parts = tuple(part for part in alias.split("/") if part)
        if not alias_parts:
            continue
        for directory in SRC_DIR.rglob(alias_parts[-1]):
            if not directory.is_dir():
                continue
            try:
                rel_parts = directory.relative_to(SRC_DIR).parts
            except ValueError:
                continue
            if len(rel_parts) < len(alias_parts):
                continue
            if rel_parts[-len(alias_parts):] != alias_parts:
                continue
            for path in directory.rglob("*." + EXT):
                if not path.is_file():
                    continue
                key = str(path.resolve())
                if key in seen:
                    continue
                seen.add(key)
                results.append(path)
    return sorted(results)


def strip_c_like_comments(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"//.*", "", text)


def strip_hash_comments(text):
    return re.sub(r"#.*", "", text)


def strip_strings(text):
    return re.sub(r'("([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')', '""', text)


def extract_python_targets(text):
    tree = ast.parse(text)
    targets = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            targets.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            targets.append(("." * node.level) + node.module)
    return targets


def extract_typescript_targets(text):
    clean = strip_c_like_comments(text)
    patterns = [
        r'(?m)^\s*import\s+(?:type\s+)?(?:[^"\']+\s+from\s+)?["\']([^"\']+)["\']',
        r'(?m)^\s*export\s+[^"\']+\s+from\s+["\']([^"\']+)["\']',
        r'(?m)(?:^|[=\s(])require\(\s*["\']([^"\']+)["\']\s*\)',
        r'(?m)\bimport\(\s*["\']([^"\']+)["\']\s*\)',
    ]
    targets = []
    for pattern in patterns:
        targets.extend(re.findall(pattern, clean))
    return targets


def extract_dart_targets(text):
    clean = strip_c_like_comments(text)
    patterns = [
        r'(?m)^\s*import\s+["\']([^"\']+)["\']',
        r'(?m)^\s*export\s+["\']([^"\']+)["\']',
        r'(?m)^\s*part(?:\s+of)?\s+["\']([^"\']+)["\']',
    ]
    targets = []
    for pattern in patterns:
        targets.extend(re.findall(pattern, clean))
    return targets


def extract_go_targets(text):
    clean = strip_c_like_comments(text)
    targets = []
    in_block = False
    for raw_line in clean.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("import ("):
            in_block = True
            continue
        if in_block:
            if line.startswith(")"):
                in_block = False
                continue
            match = re.match(r'(?:[A-Za-z_][A-Za-z0-9_]*\s+)?\"([^\"]+)\"', line)
            if match:
                targets.append(match.group(1))
            continue
        match = re.match(r'import\s+(?:[A-Za-z_][A-Za-z0-9_]*\s+)?\"([^\"]+)\"', line)
        if match:
            targets.append(match.group(1))
    return targets


def extract_rust_targets(text):
    clean = strip_c_like_comments(text)
    return re.findall(r'(?m)^\s*use\s+([^;]+);', clean)


def extract_java_like_targets(text):
    clean = strip_c_like_comments(text)
    return re.findall(r'(?m)^\s*import\s+([^\s;]+)', clean)


def extract_csharp_targets(text):
    clean = strip_c_like_comments(text)
    return re.findall(r'(?m)^\s*using\s+([^\s;=]+)\s*;', clean)


def extract_swift_targets(text):
    clean = strip_c_like_comments(text)
    return re.findall(r'(?m)^\s*import\s+([^\s]+)', clean)


EXTRACTORS = {
    "Python": extract_python_targets,
    "TypeScript": extract_typescript_targets,
    "Dart": extract_dart_targets,
    "Go": extract_go_targets,
    "Rust": extract_rust_targets,
    "Java": extract_java_like_targets,
    "Kotlin": extract_java_like_targets,
    "C#": extract_csharp_targets,
    "Swift": extract_swift_targets,
}


def normalize_target(target):
    normalized = target.replace("\\", "/")
    normalized = normalized.replace("::", "/")
    normalized = normalized.replace(".", "/")
    normalized = re.sub(r"^(package:|crate/|self/|super/|global/)", "", normalized)
    normalized = re.sub(r"^[@~]/", "", normalized)
    normalized = normalized.lstrip("./")
    normalized = re.sub(r"^src/", "", normalized)
    parts = [
        part.lower()
        for part in normalized.split("/")
        if part and part.lower() not in {"src", "crate", "self", "super", "global"}
    ]
    return "/".join(parts)


def target_matches(target, forbidden):
    normalized_target = normalize_target(target)
    normalized_forbidden = normalize_target(forbidden)
    if not normalized_target or not normalized_forbidden:
        return False
    if normalized_target == normalized_forbidden:
        return True

    target_parts = [part for part in normalized_target.split("/") if part]
    if len(target_parts) <= 1:
        return False

    directory_blob = "/" + "/".join(target_parts[:-1]) + "/"
    needle = "/" + normalized_forbidden + "/"
    return needle in directory_blob


def extract_dependency_view(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    extractor = EXTRACTORS.get(LANG)
    try:
        targets = extractor(text) if extractor else []
    except SyntaxError as exc:
        return None, None, "parse error: %s" % exc

    fallback_blob = None
    if LANG in FALLBACK_SCAN_LANGS:
        fallback_blob = normalize_target(strip_strings(strip_c_like_comments(text)))
    return targets, fallback_blob, None


def print_violation(message, detail):
    print("%sVIOLATION%s: %s" % (RED, NC, message))
    print(detail)


violations = 0
for rule in RULES:
    files = iter_source_files(rule["source_aliases"])
    if not files:
        continue
    for path in files:
        relative = path.relative_to(SRC_DIR)
        targets, fallback_blob, error = extract_dependency_view(path)
        if error is not None:
            print_violation(
                "%s could not be parsed" % relative,
                "  -> %s" % error,
            )
            violations += 1
            continue

        for forbidden in rule["forbidden"]:
            matched_target = None
            for target in targets:
                if target_matches(target, forbidden):
                    matched_target = target
                    break
            if matched_target is not None:
                print_violation(
                    "'%s' imports higher-layer dependency '%s'" % (rule["layer"], forbidden),
                    "  -> %s via %s" % (relative, matched_target),
                )
                violations += 1
                continue

            if fallback_blob and target_matches(fallback_blob, forbidden):
                print_violation(
                    "'%s' references higher-layer dependency '%s' (fallback scan)" % (
                        rule["layer"],
                        forbidden,
                    ),
                    "  -> %s" % relative,
                )
                violations += 1

if violations == 0:
    print("%s✅ Layer check passed — no dependency violations found.%s" % (GREEN, NC))
    sys.exit(0)

print("\n%s❌ Found %s layer violation(s). Fix before committing.%s" % (RED, violations, NC))
sys.exit(1)
PY
