# Gild

Renders [Orikalk](https://github.com/orikalk/palette) ports from Jinja2 templates.

## Usage

In a port, `orikalk.toml` pins the palette release:

```toml
palette = "v0.2.0"
```

Every `templates/*.j2` starts with TOML front matter between `---` lines, then the template body:

```text
---
filename = "themes/Orikalk {{ theme.name }}/Orikalk {{ theme.name }}.json"
---
{"mPrimary": "{{ dark.yellow.hex }}"}
```

`filename` is itself a template. `matrix` defaults to `["theme"]`, one output per theme with `dark` and `light` in scope, each holding the 26 slots plus `ansi`. With `matrix = ["theme", "mode"]` there is one output per theme and mode, `mode.identifier` is `dark` or `light`, and the slots sit at the top level.

Slots carry `name`, `hex`, `rgb`, `hsl`, `oklch`, `accent`. `ansi.<colour>` carries `normal` and `bright`, each with `code` and the same colour fields.

```sh
uvx --from git+https://github.com/orikalk/gild gild render
uvx --from git+https://github.com/orikalk/gild gild check
```

`render` writes changed outputs, `check` exits 1 if any committed output differs from what the template produces. `--palette path/to/palette.json` uses a local build of the palette instead of the pinned release. Releases are cached under `~/.cache/orikalk/palette/<tag>/`.

## Licence

[MIT](LICENSE), copyright Orikalk.
