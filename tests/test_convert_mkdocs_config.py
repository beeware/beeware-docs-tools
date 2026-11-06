import tomllib

import polib
import pytest

from beeware_docs_tools.build_config import load_config
from beeware_docs_tools.convert_mkdocs_config import (
    ConversionError,
    compare_configs,
    convert,
    extract_comments,
    toml_key,
    toml_string,
)
from beeware_docs_tools.nav_translations import NAV_CONTEXT

CONFIG_YML = """\
# yaml-language-server: $schema=https://squidfunk.github.io/mkdocs-material/schema.json
copyright: Someone

not_in_nav: |
  /index.md

extra:
  project_name: example  # The name of the project
  alternate:
    - name: English
      link: /en/
      lang: en

theme:
  name: material
  features:
    - navigation.tabs
  palette:
    # Light mode
    - media: "(prefers-color-scheme: light)"
      scheme: default
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode

markdown_extensions:
  - attr_list
  - toc:
      permalink: true
  - pymdownx.highlight: {}  # Highlights code
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
  - pymdownx.blocks.admonition:
      types:
        - note
  - markdown.extensions.smarty:
      smart_quotes: false

plugins:
  - search
  - literate-nav:
      nav_file: SUMMARY.md
  - macros:
      on_error_fail: true
"""

MKDOCS_EN_YML = """\
INHERIT: config.yml
site_name: Example
site_url: !ENV READTHEDOCS_CANONICAL_URL
docs_dir: en

theme:
  language: en
"""

MKDOCS_FR_YML = """\
INHERIT: config.yml
site_name: Exemple
site_url: !ENV READTHEDOCS_CANONICAL_URL
docs_dir: fr

theme:
  language: fr

extra:
  language_url: fr/
"""

SUMMARY_MD = """\
- [Home](index.md)
- Guide
    - [Guide](guide/index.md)
    - ./guide/*
- Reference
    <!-- A comment about the reference -->
    - [Reference](reference/index.md)
    - [API](reference/api.md)
"""


@pytest.fixture
def project(tmp_path, monkeypatch):
    monkeypatch.delenv("READTHEDOCS_CANONICAL_URL", raising=False)
    monkeypatch.delenv("READTHEDOCS", raising=False)
    docs = tmp_path / "docs"
    (docs / "en/guide").mkdir(parents=True)
    (docs / "en/reference").mkdir(parents=True)
    (docs / "config.yml").write_text(CONFIG_YML, encoding="utf-8")
    (docs / "mkdocs.en.yml").write_text(MKDOCS_EN_YML, encoding="utf-8")
    (docs / "mkdocs.fr.yml").write_text(MKDOCS_FR_YML, encoding="utf-8")
    (docs / "en/SUMMARY.md").write_text(SUMMARY_MD, encoding="utf-8")
    for page in [
        "index.md",
        "guide/index.md",
        "guide/b.md",
        "guide/a.md",
        "reference/index.md",
        "reference/api.md",
    ]:
        (docs / "en" / page).write_text(f"# {page}\n", encoding="utf-8")

    po = polib.POFile(wrapwidth=100000)
    po.metadata = {"Content-Type": "text/plain; charset=UTF-8"}
    for msgid, msgstr, flags in [
        ("[Home]{1}", "[Accueil]{1}", ["fuzzy"]),
        ("Guide", "Guide FR", []),
        ("[Guide]{1}", "[Le guide]{1}", []),
        ("./guide/*", "./guide/*", []),
        ("[Reference]{1}", "[Référence]{1}", []),
        ("[API]{1}", "", []),
    ]:
        po.append(
            polib.POEntry(
                msgid=msgid,
                msgstr=msgstr,
                flags=flags,
                occurrences=[("docs/en/SUMMARY.md", "1")],
            )
        )
    po.append(
        polib.POEntry(
            msgid="Reference",
            msgstr="",
            occurrences=[("docs/en/reference/index.md", "1")],
        )
    )
    (docs / "locales/fr").mkdir(parents=True)
    po.save(str(docs / "locales/fr/translations.po"))

    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_convert(project):
    """A project is converted, and the converted configuration is equivalent."""
    messages = []
    assert convert(project / "docs", out=messages.append)
    docs = project / "docs"

    output = "\n".join(messages)
    assert "en: the converted configuration is equivalent" in output
    assert "fr: the converted configuration is equivalent" in output

    # The original files have been removed.
    assert not (docs / "config.yml").exists()
    assert not (docs / "mkdocs.en.yml").exists()
    assert not (docs / "en/SUMMARY.md").exists()

    text = (docs / "zensical.toml").read_text(encoding="utf-8")
    base = tomllib.loads(text)["project"]

    # The navigation is resolved, including wildcards; HTML comments are
    # removed from titles, and kept as TOML comments.
    assert base["nav"] == [
        {"Home": "index.md"},
        {"Guide": [{"Guide": "guide/index.md"}, "guide/a.md", "guide/b.md"]},
        {
            "Reference": [
                {"Reference": "reference/index.md"},
                {"API": "reference/api.md"},
            ]
        },
    ]
    assert "# A comment about the reference" in text
    assert "literate-nav" not in base["plugins"]
    assert list(base["plugins"]) == ["search", "macros"]
    assert "[project.plugins.search]" in text

    # Markdown extensions use dotted keys, with Python names as strings.
    assert "pymdownx.highlight = {}  # Highlights code" in text
    assert 'pymdownx.emoji.emoji_index = "zensical.extensions.emoji.twemoji"' in text
    assert '"markdown.extensions.smarty".smart_quotes = false' in text
    assert "toc.permalink = true" in text

    # Comments are carried over, except YAML editor directives.
    assert "yaml-language-server" not in text
    assert 'project_name = "example"  # The name of the project' in text
    assert "# Light mode\n[[project.theme.palette]]" in text
    assert 'toggle.icon = "material/brightness-7"' in text

    # The language files only contain the language settings.
    fr = tomllib.loads((docs / "zensical.fr.toml").read_text(encoding="utf-8"))
    assert fr == {
        "project": {
            "site_name": "Exemple",
            "docs_dir": "fr",
            "theme": {"language": "fr"},
            "extra": {"language_url": "fr/"},
        }
    }

    # The result can be loaded.
    config = load_config(project, "fr", env={})
    assert config["site_name"] == "Exemple"
    assert config["theme"]["features"] == ["navigation.tabs"]


def test_convert_translations(project):
    """Navigation title translations are migrated to navigation entries."""
    messages = []
    assert convert(project / "docs", out=messages.append)

    po = polib.pofile(str(project / "docs/locales/fr/translations.po"))
    nav = {e.msgid: e for e in po if not e.obsolete and e.msgctxt == NAV_CONTEXT}
    plain = {e.msgid: e for e in po if not e.obsolete and not e.msgctxt}

    # Link titles become navigation entries, keeping their flags.
    assert nav["Home"].msgstr == "Accueil"
    assert nav["Home"].fuzzy
    assert nav["Home"].occurrences == [("docs/en/titles.md", "")]
    # The link text translation is used, as that's what the navigation showed.
    assert nav["Guide"].msgstr == "Le guide"
    assert not nav["Guide"].fuzzy
    # A navigation title gets the link text translation, even though the page
    # heading with the same text is untranslated; the heading is unchanged.
    assert nav["Reference"].msgstr == "Référence"
    assert plain["Reference"].msgstr == ""
    assert plain["Reference"].occurrences == [("docs/en/reference/index.md", "1")]
    # An untranslated link title becomes an untranslated navigation entry.
    assert nav["API"].msgstr == ""
    # Entries that were only used by the navigation file are removed.
    assert not any("{1}" in msgid for msgid in plain)
    assert "./guide/*" not in plain
    assert "Guide" not in plain

    output = "\n".join(messages)
    assert "3 navigation titles migrated, 1 untranslated" in output


def test_check_doesnt_write(project):
    """In check mode, nothing is changed."""
    messages = []
    assert convert(project / "docs", write=False, out=messages.append)
    assert (project / "docs/config.yml").exists()
    assert not (project / "docs/zensical.toml").exists()


def test_keep_old(project):
    """The original files can be kept."""
    assert convert(project / "docs", keep_old=True, out=lambda msg: None)
    assert (project / "docs/config.yml").exists()
    assert (project / "docs/en/SUMMARY.md").exists()
    assert (project / "docs/zensical.toml").exists()


def test_unsupported_env(project):
    """!ENV can only be used for site_url."""
    config = project / "docs/config.yml"
    config.write_text(
        config.read_text(encoding="utf-8") + "repo_url: !ENV REPO_URL\n",
        encoding="utf-8",
    )
    with pytest.raises(ConversionError, match="repo_url uses !ENV"):
        convert(project / "docs", out=lambda msg: None)


def test_compare_configs_detects_differences():
    """Unintended differences are reported."""
    old = {
        "site_name": "A",
        "plugins": {"search": None},
        "markdown_extensions": ["toc"],
        "theme": {"features": ["a", "b"]},
    }
    new = {
        "site_name": "A",
        "plugins": {"search": {}},
        "markdown_extensions": {"toc": {}},
        "theme": {"features": ["a"]},
    }
    diffs, _ = compare_configs(old, new, set(), set())
    assert diffs == ["theme.features: ['a', 'b'] became ['a']"]


def test_extract_comments():
    """Comments are attached to the setting they describe."""
    comments, unplaced = extract_comments(
        "# Before a\na: 1  # After a\nb:\n  # Before c\n  - c  # After c\n# Dangling\n"
    )
    assert comments[("a",)] == {"before": ["Before a"], "trailing": "After a"}
    assert comments[("b", 0)] == {"before": ["Before c"], "trailing": "After c"}
    assert unplaced == ["Dangling"]


@pytest.mark.parametrize(
    "value, expected",
    [
        ("simple", '"simple"'),
        ('quote " and \\ backslash', '"quote \\" and \\\\ backslash"'),
        ("line\nbreak\n", '"""\nline\nbreak\n"""'),
    ],
)
def test_toml_string(value, expected):
    assert toml_string(value) == expected
    assert tomllib.loads(f"x = {expected}")["x"] == value


def test_toml_key():
    assert toml_key("bare_key-1") == "bare_key-1"
    assert toml_key("needs quotes") == '"needs quotes"'
    assert toml_key("multi\nline") == '"multi\\nline"'
