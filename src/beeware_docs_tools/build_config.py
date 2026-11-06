"""Load the project configuration, and generate the configuration for a build.

The documentation configuration is stored in two kinds of file in the ``docs``
directory:

* ``zensical.toml``, the base configuration, shared by every language; and
* ``zensical.<lang>.toml``, the per-language overrides (``site_name``,
  ``docs_dir``, ``theme.language`` and so on).

Both files put their settings in a ``[project]`` table. The language file is
merged over the base configuration with the same rule MkDocs used for
``INHERIT``: tables are merged recursively, and any other value (including a
list) in the language file replaces the base value.

Zensical requires ``docs_dir`` and ``site_dir`` to be inside the directory that
contains the configuration file, and it resolves symlinks before checking. To
satisfy this, the complete configuration for a build is written as
``docs/_build.<lang>.toml``, next to the files it was generated from. This means
the English content in ``docs/en`` is used directly.

Everything else that is generated during a build (translated Markdown, the
merged macros include directory, and the built site) is written into
``docs/_build``. All of this is removed when the build finishes.
"""

import copy
import os
import shutil
import tomllib
import warnings
from importlib.metadata import PackageNotFoundError, metadata
from pathlib import Path

import polib
import tomli_w

PACKAGE_PATH = Path(__file__).parent
OVERRIDES_PATH = PACKAGE_PATH / "overrides"
SHARED_CONTENT_PATH = PACKAGE_PATH / "shared_content"

# The base configuration file, relative to the `docs` directory.
BASE_CONFIG = "zensical.toml"
# The working directory for generated content, relative to the `docs` directory.
# Each kind of run (a build, or a live server) has its own subdirectory, so they
# can be used at the same time.
WORK_DIR = "_build"

# The settings that a language file is expected to override. A key ending in
# `.*` allows anything under that key.
LANGUAGE_KEYS = {
    "site_name",
    "docs_dir",
    "theme.language",
    "theme.direction",
    "extra.language_url",
    "extra.translation_type",
    "extra.header.*",
}


def language_config_name(language):
    """The name of the configuration file for a language."""
    return f"zensical.{language}.toml"


def merge_config(base, override):
    """Merge one configuration over another, using MkDocs's `INHERIT` rule.

    Tables (dictionaries) are merged recursively; any other value in
    ``override`` (including a list) replaces the value in ``base``. ``base`` is
    not modified.

    :param base: The configuration to merge into.
    :param override: The configuration whose values take precedence.
    :returns: The merged configuration.
    """
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(merged.get(key), dict) and isinstance(value, dict):
            merged[key] = merge_config(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def _dotted_keys(table, prefix=""):
    """Yield the dotted name of every non-table value in a table."""
    for key, value in table.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict) and value:
            yield from _dotted_keys(value, f"{name}.")
        else:
            yield name


def unexpected_language_keys(language_config):
    """Find any settings in a language file that aren't per-language settings.

    :param language_config: The ``[project]`` table of a language file.
    :returns: A list of dotted key names.
    """
    unexpected = []
    for name in _dotted_keys(language_config):
        if name in LANGUAGE_KEYS:
            continue
        if any(
            key.endswith(".*") and (name == key[:-2] or name.startswith(key[:-1]))
            for key in LANGUAGE_KEYS
        ):
            continue
        unexpected.append(name)
    return unexpected


def read_toml(path):
    """Read the ``[project]`` table of a TOML configuration file."""
    with Path(path).open("rb") as f:
        return tomllib.load(f).get("project", {})


def canonical_url(env=None):
    """Determine the canonical URL of the site from the environment.

    ``READTHEDOCS_CANONICAL_URL`` is only populated for the version marked
    canonical in the Read the Docs project settings, so it's often empty for
    "latest" or PR-preview builds. Without a ``site_url``, it's not possible
    to generate correct absolute asset links for generated error pages (e.g.
    404.html), which are served for any missing URL regardless of their depth
    in the site. So, on Read the Docs, fall back to the URL of the version
    being built.

    :param env: The environment to use; defaults to ``os.environ``.
    :returns: The canonical URL, or None if it can't be determined.
    """
    if env is None:
        env = os.environ

    if url := env.get("READTHEDOCS_CANONICAL_URL"):
        return url

    if env.get("READTHEDOCS") == "True":
        project = env.get("READTHEDOCS_PROJECT")
        version = env.get("READTHEDOCS_VERSION")
        language = env.get("READTHEDOCS_LANGUAGE", "en")
        if project and version:
            return f"https://{project}.readthedocs.io/{language}/{version}/"

    return None


def load_config(project_path, language="en", env=None):
    """Load the configuration for a language.

    The language file is merged over the base configuration. If no site URL is
    configured, it is set from the environment (if available). The version of
    the documented package is added to ``extra``.

    :param project_path: The root of the project being documented.
    :param language: The language code to load.
    :param env: The environment to use; defaults to ``os.environ``.
    :returns: The merged ``[project]`` table.
    """
    docs = project_path / "docs"
    config = read_toml(docs / BASE_CONFIG)

    language_file = docs / language_config_name(language)
    language_config = read_toml(language_file)
    for name in unexpected_language_keys(language_config):
        warnings.warn(
            f"{language_file.relative_to(project_path)} sets {name!r}, which isn't "
            "a per-language setting. It will be applied, but note that a list "
            "in a language file replaces the base value, rather than being merged.",
            stacklevel=2,
        )
    config = merge_config(config, language_config)

    # A configured `site_url` takes precedence (as a literal `site_url` did in
    # the MkDocs configuration); otherwise, use the canonical URL (as
    # `site_url: !ENV READTHEDOCS_CANONICAL_URL` did).
    if "site_url" not in config and (url := canonical_url(env)):
        config["site_url"] = url

    try:
        version = metadata(config["extra"]["package_name"])["version"]
        config["extra"]["version"] = version
    except (KeyError, PackageNotFoundError):
        pass

    return config


def translate(po):
    """Generate a translator function using the provided PO file."""

    def _translate(entry):
        po_entry = po.find(entry)
        if po_entry:
            translated = po_entry.msgstr
            if translated:
                return translated
        return entry

    return _translate


def process_nav(entry, fn):
    """Recursively walk a nav definition, calling a function on human-readable strings.

    :param entry: A node in a navigation tree
    :param fn: A function that takes a single human-readable string, and returns
        a "processed" string.
    """
    if isinstance(entry, dict):
        # Recursively translate all keys, and all list values. otherwise return
        # values as is (as they will be a file reference)
        return {
            process_nav(child, fn): process_nav(value, fn)
            if isinstance(value, list)
            else value
            for child, value in entry.items()
        }
    elif isinstance(entry, list):
        # Recursively translate any dictionary in a list;
        # otherwise return as-is (as it will be a file reference)
        return [
            process_nav(child, fn) if isinstance(child, dict) else child
            for child in entry
        ]
    else:
        # The entry must be a string. Process it.
        return fn(entry)


def work_path(project_path, run="build"):
    """The directory that holds content generated during a run.

    :param project_path: The root of the project being documented.
    :param run: The kind of run: "build" or "live".
    """
    return project_path / "docs" / WORK_DIR / run


def build_config_path(project_path, language, run="build"):
    """The path of the generated configuration for a language.

    :param project_path: The root of the project being documented.
    :param language: The language code.
    :param run: The kind of run: "build" or "live".
    """
    name = f"{language}.toml" if run == "build" else f"{run}.{language}.toml"
    return project_path / "docs" / f"{WORK_DIR}.{name}"


def clean_build_files(project_path, languages, run="build"):
    """Remove the generated configurations and working directory of a run.

    :param project_path: The root of the project being documented.
    :param languages: The language codes whose configurations should be removed.
    :param run: The kind of run: "build" or "live".
    """
    for language in languages:
        build_config_path(project_path, language, run).unlink(missing_ok=True)

    shutil.rmtree(work_path(project_path, run), ignore_errors=True)

    # Only remove the shared working directory if nothing else is using it
    # (other than the metadata macOS's Finder may have added).
    work = project_path / "docs" / WORK_DIR
    (work / ".DS_Store").unlink(missing_ok=True)
    try:
        work.rmdir()
    except OSError:
        pass


def merge_include_dirs(include_dirs, target):
    """Merge several directories into one directory of symlinks.

    The macros ``include_dir`` setting accepts a single directory. This builds
    a directory tree in ``target`` that contains a symlink to every file in
    each of the ``include_dirs``. When the same relative path exists in more
    than one directory, the first directory wins; this matches how a Jinja
    loader with multiple search paths would find templates.

    :param include_dirs: The directories to merge, in priority order.
    :param target: The directory to create. Any existing content is removed.
    """
    shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True)
    for include_dir in include_dirs:
        include_dir = Path(include_dir)
        for source in sorted(include_dir.rglob("*")):
            if not source.is_file():
                continue
            dest = target / source.relative_to(include_dir)
            if dest.is_symlink() or dest.exists():
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.symlink_to(source.resolve())


def _relative_to_docs(project_path, path):
    """Express a path relative to the `docs` directory, as a POSIX string."""
    return (
        Path(path).resolve().relative_to((project_path / "docs").resolve()).as_posix()
    )


def _translate_include_yaml(include_yaml, project_path, md_path):
    """Point any `include_yaml` files in the English content at the translated content."""

    def _translate_path(path):
        parts = Path(path).parts
        if parts and parts[0] == "en":
            return (
                Path(_relative_to_docs(project_path, md_path)) / Path(*parts[1:])
            ).as_posix()
        return path

    if isinstance(include_yaml, dict):
        return {key: _translate_path(path) for key, path in include_yaml.items()}
    return [_translate_path(path) for path in include_yaml]


def build_settings(
    project_path,
    config,
    language,
    md_path,
    shared_content_path,
    site_path,
    watch=None,
    run="build",
):
    """The settings that depend on where the content for a build is.

    :param project_path: The root of the project being documented.
    :param config: The configuration for the language, as returned by
        ``load_config()``.
    :param language: The language code being built.
    :param md_path: The directory containing the Markdown content for the
        language. Must be inside the project's ``docs`` directory.
    :param shared_content_path: The directory containing the shared content for
        the language.
    :param site_path: The directory where the site will be built. Must be inside
        the project's ``docs`` directory.
    :param watch: Optional list of extra paths to watch when serving.
    :param run: The kind of run: "build" or "live".
    :returns: A configuration table, to be merged over ``config``.
    """
    md_path = Path(md_path)
    shared_content_path = Path(shared_content_path).resolve()

    settings = {
        "docs_dir": _relative_to_docs(project_path, md_path),
        "site_dir": _relative_to_docs(project_path, site_path),
        "theme": {"custom_dir": str(OVERRIDES_PATH.resolve())},
    }

    # The theme overrides are written for Zensical's classic variant (the look
    # of Material for MkDocs), rather than its default "modern" variant.
    if "variant" not in config.get("theme", {}):
        settings["theme"]["variant"] = "classic"

    # Shared content can be included using the Snippets extension. The
    # extension can be configured with a dotted key (`pymdownx.snippets.x = ...`,
    # which TOML reads as nested tables), or a quoted key
    # (`"pymdownx.snippets".x = ...`); preserve whichever form is in use.
    extensions = config.get("markdown_extensions", {})
    if "pymdownx.snippets" in extensions:
        snippets = extensions["pymdownx.snippets"] or {}
        wrap = lambda value: {"pymdownx.snippets": value}  # noqa: E731
    else:
        snippets = extensions.get("pymdownx", {}).get("snippets") or {}
        wrap = lambda value: {"pymdownx": {"snippets": value}}  # noqa: E731
    settings["markdown_extensions"] = wrap(
        {"base_path": [*snippets.get("base_path", []), str(shared_content_path)]}
    )

    # Shared content can also be included using the macros plugin. The local
    # contribution guide is an additional include root, so templates can be
    # included from either location.
    plugins = config.get("plugins", {})
    include_dirs = [shared_content_path]
    contribution_root = config.get("extra", {}).get("contribution_guide_root")
    if contribution_root:
        include_dirs.append((md_path / contribution_root).resolve())
    include_path = work_path(project_path, run) / "includes" / language
    merge_include_dirs(include_dirs, include_path)
    macros = {"include_dir": str(include_path.resolve())}
    # By default, a macro that fails to render only produces an error message in
    # the page; fail the build instead, unless configured otherwise.
    if "on_error_fail" not in (plugins.get("macros") or {}):
        macros["on_error_fail"] = True

    # Data files included by the macros plugin are referenced relative to the
    # `docs` directory; for a translation, use the copy in the translated content.
    include_yaml = (plugins.get("macros") or {}).get("include_yaml")
    if language != "en" and include_yaml:
        macros["include_yaml"] = _translate_include_yaml(
            include_yaml, project_path, md_path
        )
    settings["plugins"] = {"macros": macros}

    # Source code for API documentation is referenced relative to the project root.
    try:
        source_paths = plugins["mkdocstrings"]["handlers"]["python"]["paths"]
    except (KeyError, TypeError):
        pass
    else:
        settings["plugins"]["mkdocstrings"] = {
            "handlers": {
                "python": {
                    "paths": [
                        str((project_path / path).resolve()) for path in source_paths
                    ]
                }
            }
        }

    # mkdocstrings (as a MkDocs plugin) used the theme language for the labels
    # in API documentation, but Zensical defaults to English. Use the same rule
    # the plugin used, unless a locale has been configured.
    if "mkdocstrings" in plugins and not (plugins["mkdocstrings"] or {}).get("locale"):
        theme = config.get("theme", {})
        locale = theme.get("language") or theme.get("locale") or "en"
        settings["plugins"].setdefault("mkdocstrings", {})["locale"] = str(
            locale
        ).replace("_", "-")

    # Translate the navigation titles.
    if language != "en" and "nav" in config:
        po = polib.pofile(project_path / f"docs/locales/{language}/translations.po")
        settings["nav"] = process_nav(config["nav"], translate(po))

    if watch:
        settings["watch"] = [str(Path(path).resolve()) for path in watch]

    return settings


def write_build_config(project_path, config, language, run="build", **kwargs):
    """Write the complete configuration for a build.

    :param project_path: The root of the project being documented.
    :param config: The configuration for the language, as returned by
        ``load_config()``.
    :param language: The language code being built.
    :param run: The kind of run: "build" or "live".
    :param kwargs: The locations of the build content; see ``build_settings()``.
    :returns: The path of the generated configuration file.
    """
    build_config = merge_config(
        config, build_settings(project_path, config, language, run=run, **kwargs)
    )

    config_file = build_config_path(project_path, language, run)
    with config_file.open("wb") as f:
        f.write(
            b"# Generated by beeware-docs-tools; removed after the build. Do not edit.\n"
        )
        tomli_w.dump({"project": build_config}, f)

    return config_file
