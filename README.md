# Arkpedia color palettes

Community-maintained corrections for the [Arkpedia Color Palette Guesser](https://arkpedia.net/games/color-palette).

The palettes themselves are Arkpedia's palette catalogue, `source/data/color-palettes.json` in [`arkpedia/arkpedia-data`](https://github.com/arkpedia/arkpedia-data/blob/main/source/data/color-palettes.json). Arkpedia's nightly content release rebuilds it from the operator artwork and adds a palette for every new artwork. If one of an artwork's five colors does not represent it well, add a keyed entry to `palettes/community-overrides.json`. Arkpedia applies approved overrides on top of the catalogue.

This repository intentionally contains palette corrections rather than copies of operator artwork or of the catalogue. Artwork previews are served by [`arkpedia/arkpedia-skin-assets`](https://github.com/arkpedia/arkpedia-skin-assets).

See [CONTRIBUTING.md](CONTRIBUTING.md) for the short correction workflow.
