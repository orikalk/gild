import argparse
import json
import sys
import tomllib
import urllib.request
import zipfile
from pathlib import Path

from jinja2 import Environment, StrictUndefined

RELEASE = "https://github.com/orikalk/palette/releases/download/{tag}/orikalk.zip"
CACHE = Path.home() / ".cache" / "orikalk" / "palette"
MODES = ("dark", "light")


def fetch(*, tag: str) -> dict:
    path = CACHE / tag / "palette.json"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        archive = path.with_name("orikalk.zip")
        urllib.request.urlretrieve(RELEASE.format(tag=tag), archive)
        with zipfile.ZipFile(archive) as zf:
            path.write_bytes(zf.read("palette.json"))
    return json.loads(path.read_text())


def mode_context(*, mode: dict) -> dict:
    return {**mode["colors"], "ansi": mode["ansiColors"]}


def contexts(*, palette: dict, matrix: list[str]) -> list[dict]:
    out = []
    for key, theme in palette.items():
        if not isinstance(theme, dict):
            continue
        base = {"theme": {"identifier": key, "name": theme["name"], "stone": theme["stone"]}}
        if "mode" in matrix:
            for name in MODES:
                mode = {"identifier": name, "name": name.capitalize()}
                out.append({**base, "mode": mode, **mode_context(mode=theme[name])})
        else:
            out.append({**base, **{name: mode_context(mode=theme[name]) for name in MODES}})
    return out


def split(*, source: str) -> tuple[dict, str]:
    prefix, marker, rest = source.partition("---\n")
    header, marker, body = rest.partition("---\n")
    if prefix or not marker:
        msg = "template must start with --- front matter"
        raise ValueError(msg)
    return tomllib.loads(header), body


def render(*, root: Path, palette: dict) -> dict[Path, str]:
    env = Environment(
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
    )
    outputs = {}
    for template in sorted((root / "templates").glob("*.j2")):
        meta, body = split(source=template.read_text())
        for ctx in contexts(palette=palette, matrix=meta.get("matrix", ["theme"])):
            name = env.from_string(meta["filename"]).render(ctx)
            outputs[root / name] = env.from_string(body).render(ctx)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(prog="gild")
    parser.add_argument("command", choices=["render", "check"])
    parser.add_argument("--root", type=Path, default=Path())
    parser.add_argument("--palette", type=Path, help="local palette.json instead of the release")
    args = parser.parse_args()

    config = tomllib.loads((args.root / "orikalk.toml").read_text())
    palette = json.loads(args.palette.read_text()) if args.palette else fetch(tag=config["palette"])
    outputs = render(root=args.root, palette=palette)

    stale = [p for p, text in outputs.items() if not p.exists() or p.read_text() != text]
    if args.command == "check":
        for p in stale:
            print(f"stale: {p}", file=sys.stderr)
        return 1 if stale else 0
    for p in stale:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(outputs[p])
        print(f"wrote: {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
