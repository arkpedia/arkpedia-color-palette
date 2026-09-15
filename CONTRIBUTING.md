# Correct a palette

1. Find the artwork path in `palettes/generated-palettes.json`.
2. Add that exact path to `palettes/community-overrides.json`.
3. Supply five lowercase hex colors in this order: hair, primary outfit, secondary outfit, outfit detail, standout feature.
4. Add a short reason. A screenshot or source URL is optional but useful.
5. Run `python3 scripts/validate.py` and open a pull request.

Example:

```json
"/six-star-skins/Example - Elite 2.webp": {
  "colors": ["#c0c0c0", "#20242a", "#506070", "#f0e8dc", "#b43a42"],
  "reason": "The generated fifth swatch sampled the background instead of the red accessory."
}
```

Please change one operator or a small related group per pull request. This makes the visual review quick and lets corrections ship independently.
