from pathlib import Path

from gild.main import contexts, render, split

PALETTE = {
    "version": "0.0.0",
    "lapis": {
        "name": "Lapis",
        "dark": {"colors": {"base": {"hex": "#000001"}}, "ansiColors": {}},
        "light": {"colors": {"base": {"hex": "#fffffe"}}, "ansiColors": {}},
    },
}


def test_split() -> None:
    meta, body = split(source='---\nfilename = "x"\n---\nbody\n')
    assert meta == {"filename": "x"}
    assert body == "body\n"


def test_matrix() -> None:
    paired = contexts(palette=PALETTE, matrix=["theme"])
    assert len(paired) == 1
    assert paired[0]["dark"]["base"]["hex"] == "#000001"
    per_mode = contexts(palette=PALETTE, matrix=["theme", "mode"])
    assert [c["mode"]["identifier"] for c in per_mode] == ["dark", "light"]
    assert per_mode[1]["base"]["hex"] == "#fffffe"


def test_render(tmp_path: Path) -> None:
    (tmp_path / "templates").mkdir()
    head = '---\nmatrix = ["theme", "mode"]\nfilename = "{{ mode.identifier }}"\n'
    (tmp_path / "templates" / "t.j2").write_text(head + "---\n{{ base.hex }}\n")
    out = render(root=tmp_path, palette=PALETTE)
    assert out == {tmp_path / "dark": "#000001\n", tmp_path / "light": "#fffffe\n"}
