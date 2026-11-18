import tomllib

import polib
import pytest

from beeware_docs_tools.build_config import (
    OVERRIDES_PATH,
    build_config_path,
    canonical_url,
    clean_build_files,
    load_config,
    merge_config,
    merge_include_dirs,
    unexpected_language_keys,
    work_path,
    write_build_config,
)
from beeware_docs_tools.build_md_translations import copy_resources


def test_merge_config():
    """Tables are merged recursively; lists and scalars are replaced."""
    base = {
        "site_name": "Base",
        "theme": {"name": "material", "features": ["a", "b"]},
        "extra": {"alternate": [1, 2]},
    }
    override = {
        "site_name": "Override",
        "theme": {"language": "fr", "features": ["c"]},
    }

    merged = merge_config(base, override)

    assert merged == {
        "site_name": "Override",
        "theme": {"name": "material", "features": ["c"], "language": "fr"},
        "extra": {"alternate": [1, 2]},
    }
    # The base configuration isn't modified.
    assert base["theme"] == {"name": "material", "features": ["a", "b"]}


def test_unexpected_language_keys():
    """Only per-language settings are expected in a language file."""
    assert (
        unexpected_language_keys(
            {
                "site_name": "Docs",
                "docs_dir": "fr",
                "theme": {"language": "fr", "direction": "ltr"},
                "extra": {
                    "language_url": "fr/",
                    "translation_type": "machine",
                    "header": {"About": "À propos"},
                },
            }
        )
        == []
    )
    # An empty header table is allowed.
    assert unexpected_language_keys({"extra": {"header": {}}}) == []
    assert unexpected_language_keys(
        {"site_url": "https://example.com", "theme": {"features": ["x"]}}
    ) == ["site_url", "theme.features"]


@pytest.mark.parametrize(
    "env, expected",
    [
        ({}, None),
        (
            {"READTHEDOCS_CANONICAL_URL": "https://example.com/en/stable/"},
            "https://example.com/en/stable/",
        ),
        (
            {
                "READTHEDOCS": "True",
                "READTHEDOCS_PROJECT": "toga",
                "READTHEDOCS_VERSION": "latest",
                "READTHEDOCS_LANGUAGE": "fr",
            },
            "https://toga.readthedocs.io/fr/latest/",
        ),
        ({"READTHEDOCS": "True"}, None),
    ],
)
def test_canonical_url(env, expected):
    """The canonical URL comes from Read the Docs, if available."""
    assert canonical_url(env) == expected


def make_project(path, base, language_files):
    docs = path / "docs"
    (docs / "en").mkdir(parents=True)
    (docs / "zensical.toml").write_text(base, encoding="utf-8")
    for language, content in language_files.items():
        (docs / f"zensical.{language}.toml").write_text(content, encoding="utf-8")
    return path


BASE = """\
[project]
nav = [{ "Home" = "index.md" }, { "Section" = ["section/index.md"] }]

[project.extra]
package_name = "this-package-does-not-exist"
contribution_guide_root = "how-to/contribute"

[project.theme]
features = ["a"]

[project.markdown_extensions]
pymdownx.snippets.base_path = ["docs"]
pymdownx.snippets.check_paths = true

[project.plugins.macros]
include_yaml = { team = "en/news/.authors.yml" }

[project.plugins.mkdocstrings.handlers.python]
paths = ["src"]
"""


def test_load_config(tmp_path):
    """The language file is merged over the base configuration."""
    project = make_project(
        tmp_path,
        BASE,
        {"en": '[project]\nsite_name = "Docs"\ndocs_dir = "en"\n'},
    )

    config = load_config(project, "en", env={})

    assert config["site_name"] == "Docs"
    assert config["docs_dir"] == "en"
    assert config["theme"]["features"] == ["a"]
    assert "site_url" not in config


def test_load_config_site_url(tmp_path):
    """The site URL is set from the environment, unless it's configured."""
    env = {"READTHEDOCS_CANONICAL_URL": "https://example.com/"}
    project = make_project(
        tmp_path,
        BASE,
        {
            "en": '[project]\nsite_name = "Docs"\n',
            "fr": '[project]\nsite_name = "Docs"\nsite_url = "https://fr.example.com/"\n',
        },
    )

    assert load_config(project, "en", env=env)["site_url"] == "https://example.com/"
    with pytest.warns(UserWarning, match="sets 'site_url'"):
        config = load_config(project, "fr", env=env)
    assert config["site_url"] == "https://fr.example.com/"


@pytest.mark.parametrize(
    "base, env, expected",
    [
        # From the environment (Read the Docs)
        (
            BASE,
            {"READTHEDOCS_CANONICAL_URL": "https://example.com/en/latest/"},
            "https://example.com/en/latest/zh_CN/",
        ),
        # Configured in the base file, with and without a trailing slash
        (
            '[project]\nsite_url = "https://beeware.org/"\n',
            {},
            "https://beeware.org/zh_CN/",
        ),
        (
            '[project]\nsite_url = "https://beeware.org"\n',
            {},
            "https://beeware.org/zh_CN/",
        ),
        # No site URL at all
        (BASE, {}, None),
    ],
)
def test_load_config_translated_site_url(tmp_path, base, env, expected):
    """A translation's site URL is in the language's subdirectory."""
    project = make_project(
        tmp_path,
        base,
        {
            "en": '[project]\nsite_name = "Docs"\n',
            "zh_CN": '[project]\nsite_name = "Docs"\ndocs_dir = "zh_CN"\n',
        },
    )

    assert load_config(project, "zh_CN", env=env).get("site_url") == expected
    # English is published at the root of the site, so its URL is unchanged.
    english = load_config(project, "en", env=env).get("site_url")
    if expected:
        assert english.rstrip("/") == expected.removesuffix("/zh_CN/")
    else:
        assert english is None


def test_load_config_unexpected_key(tmp_path):
    """A setting that isn't a per-language setting produces a warning."""
    project = make_project(
        tmp_path,
        BASE,
        {"fr": '[project]\nsite_name = "Docs"\n[project.theme]\nfeatures = ["b"]\n'},
    )

    with pytest.warns(UserWarning, match="sets 'theme.features'.*replaces"):
        config = load_config(project, "fr", env={})

    # The setting is still applied.
    assert config["theme"]["features"] == ["b"]


def test_merge_include_dirs(tmp_path):
    """Include directories are merged; the first directory wins."""
    first = tmp_path / "first"
    second = tmp_path / "second"
    (first / "how").mkdir(parents=True)
    (second / "how").mkdir(parents=True)
    (first / "how/branches.md").write_text("first", encoding="utf-8")
    (second / "how/branches.md").write_text("second", encoding="utf-8")
    (second / "how/local.md").write_text("local", encoding="utf-8")
    (first / "_shared").mkdir()
    (first / "_shared/content.md").write_text("shared", encoding="utf-8")

    target = tmp_path / "merged"
    merge_include_dirs([first, second], target)

    assert (target / "how/branches.md").read_text(encoding="utf-8") == "first"
    assert (target / "how/local.md").read_text(encoding="utf-8") == "local"
    assert (target / "_shared/content.md").read_text(encoding="utf-8") == "shared"
    assert (target / "how/branches.md").is_symlink()


def test_write_build_config(tmp_path):
    """The build configuration includes the location of the build content."""
    project = make_project(
        tmp_path,
        BASE,
        {"en": '[project]\nsite_name = "Docs"\ndocs_dir = "en"\n'},
    )
    shared = tmp_path / "shared"
    shared.mkdir()
    config = load_config(project, "en", env={})

    config_file = write_build_config(
        project,
        config,
        "en",
        md_path=project / "docs/en",
        shared_content_path=shared,
        site_path=work_path(project) / "site/en",
    )

    assert config_file == build_config_path(project, "en")
    with config_file.open("rb") as f:
        written = tomllib.load(f)["project"]

    assert written["docs_dir"] == "en"
    assert written["site_dir"] == "_build/build/site/en"
    assert written["theme"]["custom_dir"] == str(OVERRIDES_PATH.resolve())
    snippets = written["markdown_extensions"]["pymdownx"]["snippets"]
    assert snippets == {
        "base_path": ["docs", str(shared.resolve())],
        "check_paths": True,
    }
    macros = written["plugins"]["macros"]
    assert macros["include_dir"] == str((work_path(project) / "includes/en").resolve())
    # The English data files aren't changed.
    assert macros["include_yaml"] == {"team": "en/news/.authors.yml"}
    assert written["plugins"]["mkdocstrings"]["handlers"]["python"]["paths"] == [
        str((project / "src").resolve())
    ]
    assert written["nav"] == [{"Home": "index.md"}, {"Section": ["section/index.md"]}]
    # mkdocstrings uses the theme language for its labels.
    assert written["plugins"]["mkdocstrings"]["locale"] == "en"
    # The classic theme variant is used, and macro errors fail the build.
    assert written["theme"]["variant"] == "classic"
    assert macros["on_error_fail"] is True

    clean_build_files(project, ["en"])
    assert not config_file.exists()
    assert not (project / "docs/_build").exists()


def test_build_and_live_are_separate(tmp_path):
    """A build and a live server use separate files."""
    assert build_config_path(tmp_path, "en") == tmp_path / "docs/_build.en.toml"
    assert build_config_path(tmp_path, "en", "live") == (
        tmp_path / "docs/_build.live.en.toml"
    )
    live = work_path(tmp_path, "live")
    (live / "site").mkdir(parents=True)
    (work_path(tmp_path) / "site").mkdir(parents=True)

    clean_build_files(tmp_path, ["en"])

    # The live server's files are untouched.
    assert live.is_dir()
    assert not work_path(tmp_path).exists()


def test_write_build_config_translation(tmp_path):
    """A translated build uses translated content, data files and navigation."""
    project = make_project(
        tmp_path,
        BASE.replace(
            'pymdownx.snippets.base_path = ["docs"]',
            '"pymdownx.snippets".base_path = ["docs"]',
        )
        .replace("pymdownx.snippets.check_paths", '"pymdownx.snippets".check_paths')
        .replace('features = ["a"]', 'features = ["a"]\nvariant = "modern"')
        .replace(
            "[project.plugins.macros]\n",
            "[project.plugins.macros]\non_error_fail = false\n",
        ),
        {"fr": '[project]\nsite_name = "Documents"\ndocs_dir = "fr"\n'},
    )
    po = polib.POFile()
    po.append(polib.POEntry(msgid="Home", msgstr="Accueil"))
    po.append(polib.POEntry(msgid="Section", msgstr=""))
    (project / "docs/locales/fr").mkdir(parents=True)
    po.save(str(project / "docs/locales/fr/translations.po"))
    md_path = work_path(project) / "md/fr"
    md_path.mkdir(parents=True)
    config = load_config(project, "fr", env={})

    config_file = write_build_config(
        project,
        config,
        "fr",
        md_path=md_path,
        shared_content_path=tmp_path,
        site_path=work_path(project) / "site/fr",
    )
    with config_file.open("rb") as f:
        written = tomllib.load(f)["project"]

    assert written["docs_dir"] == "_build/build/md/fr"
    # Explicit settings aren't overridden.
    assert written["theme"]["variant"] == "modern"
    assert written["plugins"]["macros"]["on_error_fail"] is False
    # The quoted key form of the extension is preserved.
    assert written["markdown_extensions"]["pymdownx.snippets"]["base_path"] == [
        "docs",
        str(tmp_path.resolve()),
    ]
    assert "pymdownx" not in written["markdown_extensions"]
    assert written["plugins"]["macros"]["include_yaml"] == {
        "team": "_build/build/md/fr/news/.authors.yml"
    }
    assert written["nav"] == [
        {"Accueil": "index.md"},
        {"Section": ["section/index.md"]},
    ]
    clean_build_files(project, ["fr"])


def test_copy_resources(tmp_path):
    """The non-Markdown files of the English content are copied to a translation."""
    en = tmp_path / "en"
    fr = tmp_path / "fr"
    for name in [
        "index.md",
        "images/logo.png",
        "reference/images/diagram.svg",
        "reference/canvas-images/canvas.png",
        "reference/resources/index.md",
        "reference/resources/icon.png",
        "news/.authors.yml",
        "news/.team.yml",
        "stylesheets/extra.css",
        ".DS_Store",
    ]:
        (en / name).parent.mkdir(parents=True, exist_ok=True)
        (en / name).write_text(name, encoding="utf-8")
    # po2md has already generated the translated Markdown, including in a
    # content directory named `resources`.
    (fr / "reference/resources").mkdir(parents=True)
    (fr / "index.md").write_text("translated", encoding="utf-8")
    (fr / "reference/resources/index.md").write_text("translated", encoding="utf-8")

    copied = copy_resources(en, fr)

    assert sorted(str(p) for p in copied) == [
        "images/logo.png",
        "news/.authors.yml",
        "news/.team.yml",
        "reference/canvas-images/canvas.png",
        "reference/images/diagram.svg",
        "reference/resources/icon.png",
        "stylesheets/extra.css",
    ]
    # Files are real copies, not symlinks.
    assert not (fr / "images/logo.png").is_symlink()
    assert (fr / "images/logo.png").read_text(encoding="utf-8") == "images/logo.png"
    # Translated Markdown isn't overwritten.
    assert (fr / "index.md").read_text(encoding="utf-8") == "translated"
    assert not (fr / ".DS_Store").exists()
