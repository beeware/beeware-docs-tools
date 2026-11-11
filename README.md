# BeeWare Docs Tools

Tools for building BeeWare's documentation with a common theme and translations.

The documentation is built with [Zensical](https://zensical.org).

## Configuration files

A documentation repository has the following configuration files in its `docs` directory:

* `zensical.toml`: the configuration shared by every language.
* `zensical.<lang>.toml`: the settings for one language, for example `zensical.en.toml` and `zensical.de.toml`. There must be one for every language that is built, including English.

All settings in both files go in a `[project]` table and its subtables, as described in the [Zensical documentation](https://zensical.org/docs/setup/basics/). Some things to note:

* Markdown extensions are configured with dotted keys under `[project.markdown_extensions]`, for example `pymdownx.highlight = {}` or `toc.permalink = true`. Zensical reads the `pymdownx.*` extensions after all the other extensions.
* Plugins are configured under `[project.plugins.<name>]`.
* A Python object (for example, an emoji index) is given as a string with its full dotted name, for example `"zensical.extensions.emoji.twemoji"`.
* The navigation is defined by the `nav` setting in `zensical.toml`. Titles in `nav` are translated with the rest of the documentation. There is no `SUMMARY.md` file, and wildcards aren't supported; every page must be listed.
* `site_url` doesn't need to be set. It is set at build time from the `READTHEDOCS_CANONICAL_URL` environment variable or, on Read the Docs, the URL of the version being built.
* Settings that depend on where content is during a build (`docs_dir`, `site_dir`, `theme.custom_dir`, the macros `include_dir`, the shared content Snippets path, and the mkdocstrings source `paths`) are set by docs-tools. mkdocstrings `paths` are given relative to the root of the repository.
* Unless they are set in the configuration, docs-tools also sets `theme.variant = "classic"` (the theme overrides are written for the classic Material look, not Zensical's default "modern" variant), the macros plugin's `on_error_fail = true` (so a macro that fails to render fails the build), and mkdocstrings' `locale` to `theme.language`.
* In a translated build, every non-Markdown file in `docs/en` (images, data files, stylesheets and so on) is copied into the translated content.

A language file should only contain settings that are specific to the language:

* `site_name`
* `docs_dir`
* `theme.language`
* `theme.direction`
* `extra.language_url`
* `extra.translation_type`
* `extra.header` (and anything under it)

For example, `docs/zensical.de.toml`:

```toml
[project]
site_name = "BeeWare Dokumentation"
docs_dir = "de"

[project.theme]
language = "de"

[project.extra]
language_url = "de/"
translation_type = "machine"

[project.extra.header]
About = "Über"
```

The language file is merged over `zensical.toml` with the same rule MkDocs used for `INHERIT`: tables are merged, and any other value (including a list) replaces the value in `zensical.toml`. A language file can set other settings, but the build will warn about them, because a list in a language file replaces the list in `zensical.toml` instead of extending it.

During a build, docs-tools writes the complete configuration for each language to `docs/_build.<lang>.toml`, and generated content (translated Markdown, and the built site) to `docs/_build/build/`. The live server (`live_serve_en`) uses `docs/_build.live.en.toml` and `docs/_build/live/` instead, so a build can run while the live server is running. These are removed when the build or live server finishes; add `docs/_build.*.toml` and `_build` to `.gitignore` in case a build is interrupted. Zensical also keeps a cache in `docs/.cache`, which includes its own `.gitignore`.

## Adding a new language

Weblate is able to generate a new language, however, adding a new language also requires a few changes to the documentation repository.

For details, see [Adding a new translation](https://beeware.org/contributing/guide/how/translate/#adding-a-new-translation) in the Contribution guide.

The following example outlines how you would go about adding German to this repo. The concepts are the same for any language in any of the docs repos. However, in order to support a language on another repo, you'll generally need to add support to *this* repository first - we can't support a language if `beeware-docs-tools` doesn't support it first.

### A new language configuration file

The first thing to do is create a new file named `zensical.de.toml` in the `docs` directory.

For details, see [A new language configuration file](https://beeware.org/contributing/guide/how/translate/#a-new-language-configuration-file) in the Contribution guide.

### Update `tox.ini`

You'll need to make several changes to this file.

For details, see, [Update `tox.ini`](https://beeware.org/contributing/guide/how/translate/#update-toxini) in the Contribution guide.

Note that this repository is slightly different to other docs repositories that *use* docs tools. This repository includes documentation content, but also contains shared content that is used in other repositories. The tox file includes translation steps for *both* local content and shared content; other repositories will only have local content.

### Update `zensical.toml`

Add the language to `extra.alternate` in `zensical.toml` so it will show up in the language selector in the header.

For details, see [Update `zensical.toml`](https://beeware.org/contributing/guide/how/translate/#update-zensicaltoml) in the Contribution guide.

### Run `tox translate`

You can now run `tox -e docs-translate` to generate an empty translation file.

For details, see [Run `tox translate`](https://beeware.org/contributing/guide/how/translate/#run-tox-translate) in the Contribution guide.
