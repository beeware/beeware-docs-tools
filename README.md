# BeeWare Docs Tools

Tools for building BeeWare's documentation with a common theme and translations.

## Adding a new language

Weblate is able to generate a new language, however, adding a new language also requires a few changes to the documentation repository.

For details, see [Adding a new translation](https://beeware.org/contributing/guide/how/translate/#adding-a-new-translation) in the Contribution guide.

The following example outlines how you would go about adding German to this repo. The concepts are the same for any language in any of the docs repos. However, in order to support a language on another repo, you'll generally need to add support to *this* repository first - we can't support a language if `beeware-docs-tools` doesn't support it first.

### A new MkDocs configuration file

The first thing to do is create a new file named `mkdocs.de.yml` in the `docs` directory.

For details, see [A new MkDocs configuration file](https://beeware.org/contributing/guide/how/translate/#a-new-mkdocs-configuration-file) in the Contribution guide.

### Update `tox.ini`

You'll need to make several changes to this file.

For details, see, [Update `tox.ini`](https://beeware.org/contributing/guide/how/translate/#update-toxini) in the Contribution guide.

Note that this repository is slightly different to other docs repositories that *use* docs tools. This repository includes documentation content, but also contains shared content that is used in other repositories. The tox file includes translation steps for *both* local content and shared content; other repositories will only have local content.

### Update `config.yml`

Add the language to `config.yml` so it will show up in the language selector in the header.

For details, see [Update `config.yml`](https://beeware.org/contributing/guide/how/translate/#update-configyml) in the Contribution guide.

### Run `tox translate`

You can now run `tox -e docs-translate` to generate an empty translation file.

For details, see [Run `tox translate`](https://beeware.org/contributing/guide/how/translate/#run-tox-translate) in the Contribution guide.
