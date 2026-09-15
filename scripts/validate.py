#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERRIDES = ROOT / "palettes/community-overrides.json"
GENERATED = ROOT / "palettes/generated-palettes.json"
KEY = re.compile(r"^/(one|two|three|four|five|six)-star-skins/.+ - (Base|Elite 2)\.webp$")
COLOR = re.compile(r"^#[0-9a-f]{6}$")


def load(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main():
    overrides = load(OVERRIDES)
    generated = load(GENERATED)
    assert overrides.get("version") == 1, "community-overrides.json version must be 1"
    rows = overrides.get("overrides")
    assert isinstance(rows, dict), "overrides must be an object"
    catalog = generated.get("artworks", {})
    errors = []
    for key, value in rows.items():
        if not KEY.fullmatch(key):
            errors.append(f"{key}: invalid artwork path")
        if key not in catalog:
            errors.append(f"{key}: artwork is not in generated-palettes.json")
        if not isinstance(value, dict):
            errors.append(f"{key}: override must be an object")
            continue
        unexpected = set(value) - {"colors", "reason", "source"}
        if unexpected:
            errors.append(f"{key}: unexpected fields {sorted(unexpected)}")
        colors = value.get("colors")
        if not isinstance(colors, list) or len(colors) != 5 or any(
            not isinstance(color, str) or not COLOR.fullmatch(color) for color in colors
        ):
            errors.append(f"{key}: colors must contain exactly five lowercase #rrggbb values")
        if not isinstance(value.get("reason"), str) or len(value["reason"].strip()) < 3:
            errors.append(f"{key}: explain the correction in reason")
        if value.get("source") is not None and not str(value["source"]).startswith(("https://", "http://")):
            errors.append(f"{key}: source must be an http(s) URL")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(rows)} community palette override(s).")


if __name__ == "__main__":
    main()
