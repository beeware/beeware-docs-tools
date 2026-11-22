import shutil
import subprocess

import polib
import pytest

from beeware_docs_tools.api_directives import (
    api_blocks,
    blank_api_blocks,
    restore_api_blocks,
)
from beeware_docs_tools.build_pot_translations import generate_pot_files

ENGLISH = """\
# Colors

Some text to translate.

::: toga.colors.Color
    options:
      show_root_heading: false

      members_order: source

::: toga.colors.rgb

1. A list item.

    ::: toga.colors.hsl
        options:
          heading_level: 4

```markdown
::: example.in_a.code_block
    options:
      show_source: true
```

::: toga.colors.Color
    options:
      members: [rgb]

More text.
"""

needs_translate_toolkit = pytest.mark.skipif(
    not (shutil.which("md2po") and shutil.which("po2md")),
    reason="translate-toolkit is not installed",
)


def directives(text):
    """The API directives in some Markdown content, with their indentation removed."""
    lines = text.splitlines()
    return [
        (identifier, [line.removeprefix(indent) for line in lines[start:end]])
        for start, end, indent, identifier in api_blocks(lines)
    ]


def test_api_blocks():
    """API directives are found with their options, but not in code blocks."""
    lines = ENGLISH.splitlines()

    assert [
        (indent, identifier, lines[start:end])
        for start, end, indent, identifier in api_blocks(lines)
    ] == [
        (
            "",
            "toga.colors.Color",
            [
                "::: toga.colors.Color",
                "    options:",
                "      show_root_heading: false",
                "",
                "      members_order: source",
            ],
        ),
        ("", "toga.colors.rgb", ["::: toga.colors.rgb"]),
        (
            "    ",
            "toga.colors.hsl",
            [
                "    ::: toga.colors.hsl",
                "        options:",
                "          heading_level: 4",
            ],
        ),
        (
            "",
            "toga.colors.Color",
            ["::: toga.colors.Color", "    options:", "      members: [rgb]"],
        ),
    ]


def test_blank_api_blocks(tmp_path):
    """API directives are blanked out, keeping the line numbers the same."""
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub/colors.md").write_text(ENGLISH, encoding="utf-8")
    (tmp_path / "plain.md").write_text("# Plain\n", encoding="utf-8")

    assert [str(path) for path in blank_api_blocks(tmp_path)] == ["sub/colors.md"]

    blanked = (tmp_path / "sub/colors.md").read_text(encoding="utf-8")
    assert len(blanked.splitlines()) == len(ENGLISH.splitlines())
    assert directives(blanked) == []
    # Translatable text and code blocks are untouched.
    assert "Some text to translate." in blanked
    assert "::: example.in_a.code_block\n    options:" in blanked
    assert (tmp_path / "plain.md").read_text(encoding="utf-8") == "# Plain\n"


def test_restore_api_blocks(tmp_path):
    """API directives are restored, keeping the translation's indentation."""
    en = tmp_path / "en"
    fr = tmp_path / "fr"
    en.mkdir()
    fr.mkdir()
    (en / "colors.md").write_text(ENGLISH, encoding="utf-8")
    (en / "plain.md").write_text("# Plain\n", encoding="utf-8")
    (fr / "plain.md").write_text("# Simple\n", encoding="utf-8")
    # This is what po2md produces from ENGLISH (with the text translated).
    (fr / "colors.md").write_text(
        """\
# Couleurs

Du texte à traduire.

::: toga.colors.Color options: show_root_heading: false

    members_order: source

::: toga.colors.rgb

1. Un élément de liste.

   ::: toga.colors.hsl options: heading_level: 4

```markdown
::: example.in_a.code_block
    options:
      show_source: true
```

::: toga.colors.Color options: members: [rgb]

Plus de texte.
""",
        encoding="utf-8",
    )

    assert [str(path) for path in restore_api_blocks(en, fr)] == ["colors.md"]

    restored = (fr / "colors.md").read_text(encoding="utf-8")
    assert directives(restored) == directives(ENGLISH)
    # The list item keeps the indentation that po2md gave it.
    assert "\n   ::: toga.colors.hsl\n       options:\n         heading_level: 4\n" in (
        restored
    )
    # The translation and the code block are untouched.
    assert "Du texte à traduire." in restored
    assert "::: example.in_a.code_block\n    options:" in restored
    assert (fr / "plain.md").read_text(encoding="utf-8") == "# Simple\n"
    # A second run changes nothing.
    assert restore_api_blocks(en, fr) == []


@needs_translate_toolkit
def test_round_trip(tmp_path, monkeypatch):
    """API directives don't reach the POT file, and survive a po2md round trip."""
    monkeypatch.chdir(tmp_path)
    docs = tmp_path / "docs"
    (docs / "en/api").mkdir(parents=True)
    (docs / "en/api/colors.md").write_text(ENGLISH, encoding="utf-8")
    (docs / "en/api/image.png").write_bytes(b"not really a PNG")

    generate_pot_files(docs.relative_to(tmp_path), excludes=[])

    pot = docs / "locales/template/translations.pot"
    msgids = [entry.msgid for entry in polib.pofile(pot)]
    assert "Some text to translate." in msgids
    assert not [
        msgid for msgid in msgids if "toga.colors" in msgid or "members_order" in msgid
    ]
    # Locations still point at the original content and line numbers.
    entry = polib.pofile(pot).find("More text.")
    assert entry.occurrences == [
        ("docs/en/api/colors.md", str(ENGLISH.splitlines().index("More text.") + 1))
    ]
    # The English content itself wasn't modified.
    assert (docs / "en/api/colors.md").read_text(encoding="utf-8") == ENGLISH

    fr = tmp_path / "fr"
    subprocess.run(
        [
            "po2md",
            f"--input={pot}",
            f"--template={docs / 'en'}",
            f"--output={fr}",
            "--fuzzy",
            "--maxlinelength=0",
            "--progress=none",
        ],
        check=True,
    )
    # po2md squashes the directives...
    assert "::: toga.colors.Color options:" in (fr / "api/colors.md").read_text(
        encoding="utf-8"
    )

    restore_api_blocks(docs / "en", fr)

    # ... and they are restored.
    assert directives((fr / "api/colors.md").read_text(encoding="utf-8")) == (
        directives(ENGLISH)
    )
