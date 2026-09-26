#!/usr/bin/env python3
"""Validate palettes/community-overrides.json against Arkpedia's palette catalogue.

    python3 scripts/validate.py [--catalogue <path or https URL>]

The catalogue is data/color-palettes.json in arkpedia-data (source/data/color-palettes.json):
the one palette file, which Arkpedia's nightly content release rebuilds from the pinned
artwork and the site applies these overrides on top of. This repository used to carry a copy,
palettes/generated-palettes.json, which nothing refreshed, so a correction for any artwork
added since could not pass. It is read from arkpedia-data's main branch by default.
"""
import argparse
import json
import os
import re
import ssl
import urllib.request
from pathlib import Path

try:  # python.org's macOS builds ship no CA bundle; Actions' Ubuntu Python uses the system's.
    import certifi
    CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CONTEXT = ssl.create_default_context()

ROOT = Path(__file__).resolve().parents[1]
OVERRIDES = ROOT / "palettes/community-overrides.json"
RETIRED_COPY = ROOT / "palettes/generated-palettes.json"
CATALOGUE = "https://raw.githubusercontent.com/arkpedia/arkpedia-data/main/source/data/color-palettes.json"
KEY = re.compile(r"^/(one|two|three|four|five|six)-star-skins/.+ - (Base|Elite 2)\.webp$")
COLOR = re.compile(r"^#[0-9a-f]{6}$")


def load(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def load_catalogue(source):
    if source.startswith("https://"):
        request = urllib.request.Request(source, headers={"User-Agent": "arkpedia-color-palette-validate"})
        with urllib.request.urlopen(request, timeout=60, context=CONTEXT) as response:
            catalogue = json.load(response)
    else:
        catalogue = load(source)
    artworks = catalogue.get("artworks") if isinstance(catalogue, dict) else None
    if not isinstance(artworks, dict) or not artworks:
        raise SystemExit(f"{source} lists no palette artworks; refusing to validate against it")
    return artworks


def validate(overrides, catalog):
    errors = []
    if RETIRED_COPY.exists():
        errors.append(f"{RETIRED_COPY.relative_to(ROOT)}: the palette catalogue lives in arkpedia-data "
                      "(source/data/color-palettes.json); do not add a copy here")
    if overrides.get("version") != 1:
        errors.append("community-overrides.json version must be 1")
    rows = overrides.get("overrides")
    if not isinstance(rows, dict):
        return [*errors, "overrides must be an object"]
    for key, value in rows.items():
        if not KEY.fullmatch(key):
            errors.append(f"{key}: invalid artwork path")
        if key not in catalog:
            errors.append(f"{key}: artwork is not in Arkpedia's palette catalogue (arkpedia-data source/data/color-palettes.json)")
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
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--catalogue", default=os.environ.get("ARKPEDIA_PALETTE_CATALOGUE", CATALOGUE),
                        help="the palette catalogue: a local data/color-palettes.json or an https URL (default: arkpedia-data main)")
    args = parser.parse_args(argv)
    overrides = load(OVERRIDES)
    errors = validate(overrides, load_catalogue(args.catalogue))
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(overrides['overrides'])} community palette override(s) against {args.catalogue}.")


if __name__ == "__main__":
    main()
