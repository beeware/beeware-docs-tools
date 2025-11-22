You might have the best software in the world - but if nobody knows how to use it, what's the point? Documentation can always be improved - and we need your help!

{{ formal_name }}'s documentation is written using [MkDocs and Markdown](https://www.markdownguide.org/basic-syntax/). We aim to follow the [Diataxis](https://diataxis.fr) framework for structuring documentation.

## Building {{ formal_name }}'s documentation

To build {{ formal_name }}'s documentation, start by ensuring you [have the prerequisites][dev-environment-prereqs], and then [set up a development environment][dev-environment-tldr] (or, for a more detailed explanation of dev environment setup, [start here][setup-dev-environment]). You **must** have a Python 3.12 interpreter installed and available on your path (i.e., `python3.12` must start a Python 3.12 interpreter).

{{ formal_name }} uses `tox` for building documentation. The following `tox` commands must be run from the same location as the `tox.ini` file, which is in the root directory of the project.

### Live documentation preview

To support rapid editing of documentation, {{ formal_name }} has a "live preview" mode.

/// warning | The live preview will build with warnings!

The live serve is available for iterating on your documentation updates. While you're in the process of updating things, you may introduce a markup issue. Issues considered a `WARNING` would normally cause a build to fail, however, the live serve is set up to indicate warnings in the console output, while continuing to build. This allows you to iterate without needing to restart the live preview.

A `WARNING` is different from an `ERROR`. If you introduce an issue that is considered a error, the build will fail, and require a restart.

///

To start the live server:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(venv) $ tox -e docs-live
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(venv) $ tox -e docs-live
```

///

/// tab | Windows

```doscon
(venv) C:\...>tox -e docs-live
```

///

{% endif %}

This will build the documentation, start a web server to serve the documentation, and watch the file system for any changes to the documentation source.

Once the server is started, you'll see something like the following in the console output:

```console
INFO    -  [11:18:51] Serving on http://127.0.0.1:8000/
```

Open a browser, and navigate to the URL provided. Now you can begin iterating on the documentation. If a change is detected, the documentation will be rebuilt, and any browser viewing the modified page will be automatically refreshed.

/// note | `docs-live` is an initial step

Running `docs-live` to work with the live server is meant for initial iterating. You should *always* run a local build before submitting a pull request.

///

### Local build

Once you're done iterating, you'll want to do a local build of the documentation. This build process is designed to fail if there are any markup problems. This allows you to catch anything you might have missed with the live server.

#### Generating a local build

To generate a local build:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(venv) $ tox -e docs
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(venv) $ tox -e docs
```

///

/// tab | Windows

```doscon
(venv) C:\...>tox -e docs
```

///

The output of this build will be in the `_build` directory in the root of the project.

{% endif %}

{% if not config.extra.translated %}

#### Generating a local translated build

{{ formal_name }}'s documentation is translated into multiple languages. Updates to the English documentation have the potential lead to issues in the other language builds. It is important to verify all builds are working before submitting a pull request.

To generate a build of all available translations:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(venv) $ tox -e docs-all
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(venv) $ tox -e docs-all
```

///

/// tab | Windows

```doscon
(venv) C:\...>tox -e docs-all
```

///

{% endif %}

The output of each language build will be in the associated `_build/html/languagecode` directory, where `languagecode` is the two- or five-character language code associated with the specific language (e.g. `fr` for French, `it` for Italian, etc.).

If you find an issue with a single build, you can run that individual build separately by running `tox -e docs-languagecode`.

For example, to build the documentation in only French:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(venv) $ tox -e docs-fr
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(venv) $ tox -e docs-fr
```

///

/// tab | Windows

```doscon
(venv) C:\...>tox -e docs-fr
```

///

{% endif %}

The output of a single-language build will be in the `_build` directory.

{% endif %}

### Documentation linting

The build process will identify Markdown problems, but {{ formal_name }} performs some additional "lint" checks. To run the lint checks:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(venv) $ tox -e docs-lint
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(venv) $ tox -e docs-lint
```

///

/// tab | Windows

```doscon
(venv) C:\...>tox -e docs-lint
```

///

{% endif %}

This will validate the documentation does not contain:

- dead hyperlinks
- misspelled words

If a valid spelling of a word is identified as misspelled, then add the word to the list in `docs/spelling_wordlist`. This will add the word to the spellchecker's dictionary. When adding to this list, remember:

- We prefer US spelling, with some liberties for programming-specific colloquialism (e.g., "apps") and verbing of nouns (e.g., "scrollable")
- Any reference to a product name should use the product's preferred capitalization. (e.g., "macOS", "GTK", "pytest", "Pygame", "PyScript").
- If a term is being used "as code", then it should be quoted as a literal (`like this`) rather than being added to the dictionary.

## Submitting a pull request

Before you submit a pull request, there's a few bits of housekeeping to do. See the section on submitting a pull request in the [code contribution guide][pr-housekeeping] for details on our submission process.
