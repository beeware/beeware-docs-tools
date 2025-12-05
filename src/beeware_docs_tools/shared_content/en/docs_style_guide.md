TODO: Consider reordering content

This guide includes information on expected style, MkDocs-specific syntax, various required tools, and documentation translation, with regard to writing new content and translating existing content.

## General style

* Headers and titles should have only the first word capitalized.
* We prefer US spelling, with some liberties for programming-specific colloquialism (e.g., "apps") and verbing of nouns (e.g., "scrollable").
* The spelling of "artefact" and "artefacts" is as shown.
* Any reference to a product name should use the product’s preferred capitalization. (e.g., <nospell>"macOS", "GTK", "pytest", "Pygame", "PyScript"</nospell>).
* If a term is being used "as code", then it should be quoted as inline code, by wrapping it in single backticks, rather than being added to the dictionary.

## Reference links

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

Attributes are the same as above, with the attribute name included. The following displays the namespace:

```markdown
[`module.ClassName.attributename`][]
```

As with classes, displaying only the attribute name is formatted as follows:

```markdown
[`attributename`][module.ClassName.attributename]
```

Methods should be displayed with `()` after the namespace, and therefore must be handled differently than attributes. The following is the appropriate way to link to a method:

```markdown
[`module.ClassName.methodname()`][module.ClassName.methodname]
```

The following displays the class and method name only. This also requires including the parentheses after the name:

```markdown
[`Classname.methodname()`][module.Classname.methodname]
```

You can link to a class, method, or attribute while displaying arbitrary text, using the same method with the applicable namespace. Doing this with a class is formatted as follows:

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

Markdown generates anchors for all headers (anything on a single line starting with between one and six `#` symbols), based on the content of the header. For example, the anchor generated for this section is `custom-markdown-anchors`. There are situations where it makes sense to instead set a custom anchor, such as, if you are using the anchor in a reference link, or if the header is overly verbose, and you need something more memorable available for reuse.

/// danger | Reference links and custom anchors

Any header that is referenced in text content via a MkDocs reference link *must* have a custom anchor attached. Otherwise, there is the potential to break links when header content is translated.

MkDocs reference links are any links formatted as follows:

```markdown
[Link text][anchor-name]
```

Therefore, an example related header must be formatted as follows:

```markdown
# Header { #anchor-name }
```

///

The general syntax for setting a custom anchor is as follows:

```markdown
# Header text { #anchor }
```

For example, customizing the anchor for this section to `custom-anchors` would be done with the following formatting:

```markdown
## Custom Markdown anchors { #custom-anchors }
```

You can also create an anchor on general content, including text and codeblocks. The following formatting, with newlines above and below, should be included above the content you wish to link to:

```markdown
Content above.

[](){ #anchor-name }

Content below, that is now attached to the anchor above.
```

## Markdown elements that require specific formatting

Due to the way the translation files are generated, it is important to include required newlines in the Markdown syntax for admonitions, notes, tabs, Jinja directives, image captions and alignment, etc.

### Admonitions and notes

Admonitions must be formatted as follows, including ensuring a newline before and after the admonition start and end:

```markdown
Content above.

/// admonition | Title

Admonition text, including
multi-line text.

A second paragraph.

///

Content below.
```

Note admonitions require the same formatting and newlines:

```markdown
Content above.

/// note | Note

Note text here.

///

Content below.
```

This format also works for danger, tip, and warning admonition types.

### Tabbed content

Tabbed content is formatted as follows, including a newline included before the start and after the end of the content block:

```markdown
Content above.

/// tab | Tab one title

Tab one text

///

/// tab | Tab two title

Tab two text.

///

/// tab | Tab three title

Tab three text.

///

Content below.
```

A tab with a nested admonition would be formatted as follows, including a newline before and after the content block:

```markdown
Content above.

/// tab | Windows

Tab text.

/// admonition | Admonition

Admonition text.

///

///

Content below.
```

### Jinja directives

There are a few features of the documentation that use Jinja directives in the text. Anything using the Jinja directive features needs to be wrapped in newlines. For example, the BeeWare tutorial contains Jinja conditionals based on variables to determine what admonition to show on the main page. Those are formatted as follows:

```markdown
Content above.

{% if config.extra.translation_type == "original" %}

/// admonition | Admonition title

Text

///

{% endif %}

Content below.
```

There is also syntax for substituting symbols or text. This syntax is a variable wrapped in a pair of matching double curly braces, and, if on its own line, must include a newline before and after.

```markdown
Content above.

{{ variable }}

Content below.
```

### Images with caption syntax

Whether the caption syntax is being utilized for the purposes of centering an image, or for providing an image caption, it must include newlines between each section.

For example, when adding an empty caption to center an image, you should format it as follows, with a newline before and after the content block:

```markdown
Content above.

![Alt text](/path/to/image.png)

/// caption

///

Content below.
```

Adding a caption to an image also requires a newline before and after, and is formatted as follows:

```markdown
Content above.

![Alt text](/path/to/image.png)

/// caption

Caption content.

///

Content below.
```

## Code block tips

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

## Using Snippets to include external content

For details on how to include external content from a local file or a URL, see the [Snippets extension documentation](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/). Snippets should be used as long as the document does not contain Jinja directives that need to be executed (the Jinja execution happens alongside the Snippets processing, and therefore any Jinja in the file will not be processed). Snippets is necessary if you want to be able to use delimiters that allow you to include specific parts of a file separately, e.g. the source document is divided up into sections to be injected separately from each other.

Important notes:

* We use `-8<-` as the Snippets identifier. The documentation shows several options; please follow our style.
* Files found in BeeWare Docs Tools shared content are treated as "local" content, and should be added using only the filename, i.e. this style guide would be included using `-8<- "docs_style_guide.md"`.
* If you are including external content from a file on GitHub via a URL, you _must_ use the raw content URL, or it will render the full webpage embedded wherever you include it.

## Using Macros to include content from BeeWare Docs Tools shared content

You can also include content from the BeeWare Docs tools shared content directory using the [Macros MkDocs plugin](https://mkdocs-macros-plugin.readthedocs.io/en/latest/pages/). This method is necessary if the document contains Jinja directives that need to be executed, and should only be used in this situation. It will not work with external content via a URL. The [Macros variable-replacement mechanism](https://mkdocs-macros-plugin.readthedocs.io/en/latest/pages/#1-variable) works with this method.

There are options for including content using Macros:

1. Use `include`. If you want to include the document with no other manual changes to it, you can use the following:

    ```markdown
    {% include "filename.md" %}
    ```

2. Use `extends`. If you have included Jinja in the document that allows you to override specific sections, you will need to include the content using the following:

    ```markdown
    {% extends "filename.md" %}
    ```

    This allows you to use Jinja's `block` mechanism to override sections of a document.
