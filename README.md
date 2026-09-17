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
{"mPrimary": "{{ dark[theme.stone].hex }}"}
```

`filename` is itself a template. `theme` carries `identifier`, `name` and `stone`, the slot name of the theme's headline colour. `matrix` defaults to `["theme"]`, one output per theme with `dark` and `light` in scope, each holding the slots plus `ansi`. With `matrix = ["theme", "mode"]` there is one output per theme and mode, `mode.identifier` is `dark` or `light`, and the slots sit at the top level.

Slots carry `name` and `hex`. `ansi.<colour>` carries `normal` and `bright`, each with `hex` and `code`.

```sh
uvx --from git+https://github.com/orikalk/gild gild render
uvx --from git+https://github.com/orikalk/gild gild check
```

`render` writes changed outputs, `check` exits 1 if any committed output differs from what the template produces. `--palette path/to/palette.json` uses a local build of the palette instead of the pinned release. Releases are cached under `~/.cache/orikalk/palette/<tag>/`.

## Licence

[MIT](LICENSE), copyright Orikalk.
