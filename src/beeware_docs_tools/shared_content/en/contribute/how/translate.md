### Getting started with translating

If you'd like to contribute to BeeWare's translation efforts, you'll need an account on [Weblate](https://hosted.weblate.org). [Create a new account](https://hosted.weblate.org/accounts/register/) if you don't currently have one; then let us know you're interested in helping out with translations.

There are two options for letting us know that you'd like to help out with translations:

* If you're on Discord, join the [BeeWare server](https://beeware.org/bee/chat/), and head to the `#translations` channel.
* If you're not on Discord, you can create a new issue on the {{ formal_name }} repository.

In both cases, leave a message including the following information:

* Your Weblate username
* The language you are planning to which you are planning to translate content

Once we have this info, we'll get you added to the team.

### Adding a new translation

If the language you plan to help out with doesn't already exist, there are some additional steps required before you can get started:

* Create the `/docs/mkdocs.language-code.yml` file, with language-specific content.
* Update `tox.ini` to include the new language build commands.
* Update `/docs/config.yml` to include the language under `extra: alternate:`.

The following demonstrates the necessary changes using German as an example; a German translation already exists; replace the references to German, `de`, or other content for the language you're targeting.

#### A new MkDocs configuration file

First, create a new file named `mkdocs.de.yml` in the `docs` directory, with the following content:

```yaml
INHERIT: config.yml
site_name: {{ formal_name }} Dokumentation
site_url: {% if config.extra.website %}https://beeware.org/de{% else %}https://{{ project_name }}.beeware.org/de{% endif %}
docs_dir: de

theme:
  language: de

extra:
  translation_type: machine
```

Here's what is going on in this file:

* This file inherits the configuration content from `config.yml`.
* The `site_name` value is translated.
* The `site_url` value is the project site URL, followed by the language code.
* The `docs_dir` should be the language code.
* The `theme: language:` value should be the language code, as [specified by the MkDocs Material theme](https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/). For most languages, this will be the same as the `docs_dir` language code; but for some (in particular languages with locale variants like `zh_CN`), there are differences.
* The `extra: translation_type:` should be `machine` until the translation reaches 100% for the first time, at which point it should be `human`. It will revert to `machine` from `human` if it regresses to below 90%.

#### Update `tox.ini`

You'll need to make several changes to the `tox.ini` file.

You would add the following:

* The new language code environment flag to the header line which begins `[testenv:docs`, with the language code preceded by a `-`, with no spaces included, e.g. `-de`.
* The new language code exclusion to the first command, which begins with `!lint`, preceded by `-!`, with no spaces included, e.g. `-!de`.
* The new language code to the end of the line beginning with `translate : build_po_translations`.
* The new language code to the end of the line beginning with `translate : update_machine_translations`
* A new command, beginning with, for example, `de : build_md_translations` for German, after the other existing language-specific commands that matches the content those commands with the new language code.
* The new language code to the end of the line beginning with `all,serve :`.

#### Update `config.yml`

Add the language to `config.yml` so it will show up in the language selector in the header. Find the section beginning with `extra:`, and then locate the subsection beginning with `alternate:`. For German, you would add the following:

```yaml
    - name: Deutsch
      link: /de/
      lang: de
```

The language name should be translated into the language. The link must include the `/`s.

The new language is now ready to begin translation.

### Translation guidelines

Once you've been added to the team, it's time to log into [Weblate](https://hosted.weblate.org/projects/beeware/) and begin working through translating strings.

#### Tone versus word-for-word translation

It's more important to maintain the tone of the English text than to strive for a word-for-word translation. We try to be friendly and a bit colloquial in our content; try to maintain the spirit of that in your translations.

If the English text contains a strong English idiom, don't feel beholden to maintain the idiom, if there is an analog in your language that would work equally well. If the term or phrase in the English text is a particularly idiomatic or slang term, don't be afraid to tell us we should consider making a change. Even for English speakers, idioms and slang can pose difficulty. Sometimes we need to change the English text to make it more straightforward for translators and readers alike.

#### Should I translate it?

The following items should _not_ be translated or updated:

* **Commands**. For example, in "You should run \`briefcase create\`.", only "You should run" should be translated.
* **Namespaces**, such as class, method, or attribute names.
* **Link URLs**. Standard Markdown links should appear in Weblate as `[Link text]{1}`, where `1` is the position of the link in the string with reference to other possible links. If the full URL is included in the string, as `[Link text](https://example.com)`, the URL should be skipped for translation.
* **Reference links containing class, method or attribute names**. These should be left as-is, including the backticks. Every part of the example link shown here would not be translated.

    ```markdown
    [`Class.attribute`][Class.attribute]
    ```

* **The link content of a Reference link**. For example, `link-content` would be skipped in the following:

    ```markdown
    [Link text][link-content]
    ```

* **Jinja directives**. This is any content wrapped inside two pairs of matching curly braces, or a matching pair of single curly braces with percent signs inside each end. Note: Including an example of the syntax here causes the Macros plugin to attempt to render it; see the [Macros documentation](https://mkdocs-macros-plugin.readthedocs.io/en/latest/pages/) for examples.
* **Custom anchors**. They are found after headers or above some content, and are formatted as `{ #anchor }`.
* **Admonition syntax**. In the following example, the word "admonition" should not be translated. This goes for all styles of admonitions, including notes, warnings, etc. See the next section for information on translating the rest of the content.

    ```markdown
    /// admonition | Page Title

    Content.

    ///
    ```

* **Backticks**. They are meant to stay as backticks; they are used for formatting both inline code and code blocks.
* **The syntax for including external content**. This is anything on the same line as `-8<-`, or on the lines between two `-8<-` on separate lines.

The following items _should_ be translated:

* **Link text**. In link syntax, the text comes before the URL, and is enclosed in brackets, as in `[Link text](URL)`. Standard Markdown links should appear in Weblate as `[Link text]{1}`, where `1` is the position of the link in the string with reference to other possible links.
* **Reference link text**. For example, `Link text` would be translated in the following:

    ```markdown
    [Link text][link-content]
    ```

* **Admonition titles and content**. In the previous admonition example, "Page Title" and "Content." should be translated.

### Weblate

We use [Weblate](https://hosted.weblate.org/projects/beeware/) for our content translation. When we add a new translation, we use [DeepL](https://www.deepl.com/en/translator) for machine translation to produce a first pass at translations. That means, typically, the content you'll be translating is already machine translated. The expectation is that you, as a translator, will review, edit, and improve the existing machine translation.

Weblate processes everything on a string-by-string basis. It batches changes, and every couple of hours, it will submit a bulk commit with all the strings that have changed in that interval. So, it may take a couple of hours for your changes to show up on the website, but you can expect the update to appear within four hours.

If after that time, your changes still haven't appeared, the likely cause is a markup error, resulting in a failure in the docs build for that language. Any markup problem in any string will block the entire translation from being public. You can keep an eye on the build page for your language to see whether it has successfully built. The link is formatted similarly to this link to the French build page {% if config.extra.website %}[https://app.readthedocs.org/projects/beewareorg-fr/](https://app.readthedocs.org/projects/beewareorg-fr/){% else %}[https://app.readthedocs.org/projects/{{ project_name }}-fr/](https://app.readthedocs.org/projects/{{ project_name }}-fr/){% endif %}; change the language code to your language to view the appropriate build page. This will show the state of the most recent build of the site. If the build fails, look at the build log, and see if you can identify the source of the problem.
