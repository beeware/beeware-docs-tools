# BeeWare Docs Tools

Tools for building BeeWare's documentation with a common theme and translations.

## Adding a new language

Weblate is able to generate a new language, however, adding a new language also requires a few changes to the documentation repository.

Once a new language is generated, you'll need to add a new `mkdocs.<language-code>.yml` file and update the `tox.ini` file.

The following example outlines how you would go about adding German to this repo. The concepts are the same for any language in any of the docs repos. However, in order to support a language on another repo, you'll generally need to add support to *this* repository first - we can't support a language if `beeware-docs-tools` doesn't support it first.

### The new MkDocs configuration file

The first thing to do is create a new file named `mkdocs.de.yml` in the `docs` directory, with the following content:

```yaml
INHERIT: config.yml
site_name: BeeWare Demo zu Docs Tools
site_url: https://tutorial.beeware.org/de
docs_dir: de

theme:
  language: de

extra:
  translation_type: machine
  header:
    About: Über
    Documentation: Dokumentation
    Community: Gemeinschaft
    Contributing: Mitwirken
    News: Neuigkeiten
    Sponsor: Förderer
```

Here's what is going on in this file:

* This file inherits the configuration content from `config.yml`.
* The `site_name` value is translated.
* The `site_url` value is the project site URL, followed by the language code.
* The `docs_dir` should be the language code.
* The `theme: language:` value should be the language code, as [specified by the MkDocs Material theme](https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/). For most languages, this will be the same as the `docs_dir` language code; but for some (in particular languages with locale variants like `zh_CN`), there are differences.
* The `extra: translation_type:` should be `machine` until the translation reaches 100% for the first time, at which point it should be `human`. It will revert to `machine` from `human` if it regresses to below 90%.
* The content under `extra: header` are the translations for titles that appear in the header bar. This definition is *not* required on the main BeeWare website; it is only required on *other* sites (such as the tutorial, or project documentation)

### The update to `tox.ini`

You'll need to make several changes to this file.

You'll need to add the following:

* The language code environment flag to the header line which begins `[testenv:docs`, preceded by a `-`, with no spaces included.
* The language code exclusion to the first command, which begins with `!lint`, preceded by `-!`, with no spaces included.
* The language code to the end of the second line beginning with `translate :`.
* The language code to the end of the line beginning with `all :`.
* A new line at the end that matches the other language-specific lines with the new language code.

Note that this repository is slightly different to other docs repositories that *use* docs tools. This repository only publishes English, French and German translations; however, it has *support* for "shared content" content in many other languages. As a result, there's lots of entries for languages in *this* repository that aren't actually used by this repository.

### Run tox-translate

You can now run `tox -e docs-translate`. This will generate an empty translations file; if you have a DeepL account, you can use that account to populate initial machine translations. If you don't have a DeepL account, that's fine - we'll run initial translations ourselves before accepting the pull request.
