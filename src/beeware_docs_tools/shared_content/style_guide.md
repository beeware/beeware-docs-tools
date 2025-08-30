# BeeWare documentation style guide

This guide includes information on expected style, MkDocs-specific syntax, various required tools, and documentation translation, with regard to writing new content and translating existing content.

## General style

* Headers and titles should have only the first word capitalized.
* We prefer US spelling, with some liberties for programming-specific colloquialism (e.g., "apps") and verbing of nouns (e.g., "scrollable").
* The spelling of "artefact" and "artefacts" is as shown.
* Any reference to a product name should use the product’s preferred capitalization. (e.g., <nospell>"macOS", "GTK", "pytest", "Pygame", "PyScript"</nospell>).
* If a term is being used "as code", then it should be quoted as inline code, by wrapping it in single backticks, rather than being added to the dictionary.

## Reference Links

MkDocs renders standard Markdown formatted links. It also supports rendering a reference link syntax that allows you to link to various other elements in the documentation using a modified Markdown link. This includes linking to, among other things, standard Markdown header anchors, custom Markdown header and text anchors, custom reference IDs, documented classes and class methods or attributes, and specific external documentation references.

Standard Markdown formatted links are as follows:

```markdown
[Link text](https://example.com/)
```

You can also use this format to link to a local file:

```markdown
[Link text](path/to/file.md)
```

Linking to an anchor _in the same file_ is formatted as follows:

```markdown
[Link text](#anchor-name)
```

Linking to an anchor _in a different_ file is formatted as follows:

```markdown
[Link text][anchor-name]
```

If you need to link to an anchor in a different file, and the anchor name is duplicated in multiple files, you can generate a custom anchor for the intended content (as shown in the next section), and link to that using the reference link formatting:

```markdown
[Link text][custom-anchor-name]
```

There are multiple options for linking to a documented class, or a class method or attribute, regardless of whether you are linking from the same file or a separate file. When linking to classes, etc., you must include backticks in the first set of square brackets to render the name as inline code. The backticks are not necessary only if you are using custom text that should not be rendered as inline code. Backticks should never be included in the second set of square brackets.

Linking to a class while displaying the namespace is formatted as follows:

```markdown
[`module.ClassName`][]
```

Linking to a class while displaying only the class name is formatted as follows:

```markdown
[`ClassName`][module.ClassName]
```

Methods and attributes are the same as above, with the method or attribute name included. You must include the parentheses after the namespace. The following displays the namespace:

```markdown
[`module.ClassName.methodname()`][]
```

The following displays the class and method name only. This also requires including the parentheses after the name:

```markdown
[`Classname.methodname()`][module.Classname.methodname]
```

Linking to a class (or method) while displaying arbitrary text is formatted as follows:

```markdown
[link text][module.ClassName]
```

It is also possible to link directly to Python core documentation, as well as Pillow documentation. For example, to link to the documentation for `int`:

```markdown
[`int`][]
```

To link to the Pillow `Image` documentation:

```markdown
[`PIL.Image.Image`][]
```

## Custom Markdown anchors

Markdown generates anchors for all headers (anything on a single line starting with between one and six `#` symbols), based on the content of the header. For example, the anchor generated for this section is `custom-markdown-anchors`. There are situations where it makes sense to instead set a custom anchor, such as, if the header is overly verbose, or you need something more memorable available for reuse.

Changing the anchor for this section to `custom-anchors` would be done with the following formatting:

```markdown
## Custom Markdown anchors { id="custom-anchors" }
```

You can also create an anchor on general content, including text and codeblocks. The following formatting, with newlines above and below, should be included above the content you wish to link to:

```markdown
[](){ id="anchor-name" }
```

/// note | Note

The reference linking that allows for linking to anchors in separate files requires that all anchors be unique. If you are creating a custom anchor, ensure that you are choosing a name that isn't used elsewhere in the documentation.

///

## Translating existing content

The following items should _not_ be translated or updated:

* Commands. For example, in "You should run \`briefcase create\`.", only "You should run" should be translated.
* Namespaces; class, method, or attribute names. Reference links containing class, method or attribute names should be left as-is, including the backticks.
* Jinja directives. This is any content wrapped inside two pairs of matching curly braces, or a matching pair of single curly braces followed by a percent sign. Note: Including an example of the syntax here causes the Macros plugin to attempt to render it; see the [Macros documentation](https://mkdocs-macros-plugin.readthedocs.io/en/latest/pages/) for examples.
* Custom anchors. They are found after headers or above some content, and are formatted as `{ id="anchor" }`.
* Admonition _syntax_. As shown below, the word "admonition" should not be translated. This goes for all styles of admonitions, including notes, warnings, etc. See below for information on translating the rest of the content.

    ```markdown
    /// admonition | Title

    Content.

    ///
    ```

* Backticks are meant to stay as backticks; they are used for formatting both inline code and code blocks.
* The syntax for including external content. This is anything on the same line as `-8<-`, or on the lines between two `-8<-` on separate lines.

The following items _should_ be translated:

* The admonition titles and content. As shown below, "Title" and "Content." should be translated. See above for information on the syntax.

    ```markdown
    /// admonition | Title

    Content.

    ///
    ```

## Translations and writing new content

Due to the way the translation files are generated, it is important to include required newlines in the Markdown syntax for admonitions, notes, tabs, Jinja directives, image captions and alignment, etc.

### Admonitions and notes

Admonitions must be formatted as follows, including ensuring a newline before and after the admonition start and end:

```markdown
/// admonition | Title

Admonition text, including
multi-line text.

A second paragraph.

///
```

Note admonitions require the same formatting and newlines:

```markdown
/// note | Note

Note text here.

///
```

This format also works for attention, caution, danger, error, tip, hint, warning admonition types.

### Tabbed content

Tabbed content is formatted as follows, including a newline included before the start and after the end of the content block:

```markdown
/// tab | Tab one title

Tab one text

///

/// tab | Tab two title

Tab two text.

///

/// tab | Tab three title

Tab three text.

///
```

A tab with a nested admonition would be formatted as follows, including a newline before and after the content block:

```markdown
/// tab | Windows

Tab text.

/// admonition | Admonition

Admonition text.

///

///
```

### Jinja directives

There are a few features of the documentation that use Jinja directives in the text. Anything using the Jinja directive features needs to be wrapped in newlines. For example, the BeeWare tutorial contains Jinja conditionals based on variables to determine what admonition to show on the main page. Those are formatted as follows:

```markdown
{% if config.extra.translation_type == "original" %}

/// admonition | Admonition title

Text

///

{% endif %}
```

There is also syntax for substituting symbols or text. This syntax is a variable wrapped in a pair of matching double curly braces, and must include a newline before and after.

```markdown
{{ variable }}
```

### Images with caption syntax

Whether the caption syntax is being utilized for the purposes of centering an image, or for providing an image caption, it must include newlines between each section.

For example, when adding an empty caption to center an image, you should format it as follows, with a newline before and after the content block:

```markdown
![Alt text](/path/to/image.png)

/// caption

///
```

Adding a caption to an image also requires a newline before and after, and is formatted as follows:

```markdown
![Alt text](/path/to/image.png)

/// caption

Caption content.

///
```

## Custom header anchors using reference IDs

By default, Markdown generates an anchor for every header that is the text of the header with spaces and punctuation replaced with `-`. However, if you want something shorter, more memorable, or customized for whatever reason, this is possible using Jinja-formatted attribute IDs.

The syntax is as follows:

```markdown
# Header text { id="anchor" }
```

For example, if you wanted to be able to link to this section using `custom-anchors`, you would format the header as follows:

```markdown
## Custom header anchors and reference IDs { id="custom-anchors" }
```

Once added, you can link to the section from within the same file using a standard Markdown link, or from another file using the reference link syntax.

## Code block tricks

### Language and code highlighting

You can specify the language for the code contained within the codeblock by including the language name after the first three backticks, with no space between. This results in appropriate code highlighting when the code rendered. For example, to specify Python, you would begin the codeblock with ` ```python`.

### Console commands and the copy button

If you are including console commands, or commands with output, if you label it as `console` or `doscon`, depending on what operating system you are referencing, you can include the prompt, and only the command will be copied when clicking the copy button. For example, if you begin a codeblock with ` ```console `, and include the following content:

```console
$ mkdir test
$ ls
test
```

Then, clicking the copy button on the codeblock will copy only the commands, and ignore the prompts and the output. This allows you to indicate that they are console commands, while still allowing users to use the copy button effectively.

### Highlighting specific lines of code

You can highlight specific lines of code. For example, to highlight line 2, you would add a space after the language, followed by `{hl_lines="2"}`. So, your codeblock would begin with ` ```python {hl_lines="2"} `. The result is:

```python {hl_lines="2"}
import toga
from toga.style.pack import COLUMN, ROW
```

You can highlight multiple different lines. For example, `python {hl_lines="3 5 9"}` would highlight lines 3, 5 and 9. You can also highlight a range of lines. For example, `python {hl_lines="3-8"}` highlights lines 3 through 8. You can highlight multiple ranges with, for example, `python {hl_lines="9-18 23-44"}`.

## Using Snippets to include external content

For details on how to include external content from a local file or a URL, see the [Snippets documentation](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/).

Two important notes:

* We use `-8<-` as the Snippets identifier. The documentation shows several options; please follow our style.
* If you are including external content from a file on GitHub via a URL, you _must_ use the raw content URL, or it will render the webpage embedded wherever you include it.

## Image formatting

Images can have the width set, and can be aligned left, right, and center (with a caveat on "center").

Setting the width of <nospell>300px</nospell> on an image would be formatted as follows:

```markdown
![Image alt text](../path/to/image.png){ width="300px" }
```

Aligning an image left (or right) would be formatted as follows:

```markdown
![Image alt text](../path/to/image.png){ align=left }
```

Aligning an image center is not possible with the `align` attribute. The workaround is to follow the image with an empty caption, and it will be centered. You must include newlines between each section, and before and after. It is formatted as follows:

```markdown
![Image alt text](../path/to/image.png)

/// caption

///
```

## `pyspelling`

We use the `pyspelling` spellchecker. It is run during the lint-checks.

When `pyspelling` identifies a misspelled word, in most cases, it should be fixed in the documentation content.

In the rare case that it identifies a valid word that isn't in the `pyspelling` dictionary, you have two options:

1. If it is a word that is likely to be reused multiple times, you should add the word to the `spelling_wordlist` document in the `docs` directory, in alphabetical order.
2. If it is a word that is unlikely to be used again, you can wrap it in a `<nospell>` / `</nospell>` tag, and `pyspelling` will ignore it inline.
