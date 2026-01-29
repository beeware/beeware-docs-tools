import re
import sys
from pathlib import Path

# A major caveat: if the links in the translations are not properly formatted, this
# script will not function as expected, and will likely result in half-updated links
# or links that are missed entirely. Link issues I encountered: links wrapped in double
# quotes instead of backticks, links with spaces in them, links missing one of the
# backticks, links missing both backticks, and links followed by only one underscore.
# There are endless ways links can be misformatted. I went through the PO files and
# manually fixed as many of the issues as I could find by searching for various link
# syntax pieces in the files. This method is not guaranteed to find everything, for
# obvious reasons, but it was a good start.


def doc_links(string):
    """
    Update doc links to Markdown formatting.
    """
    return re.subn(
        r":doc:(?<!`)`(?!`)([\d\D']*?) <([a-zA-Z0-9-:\/\.# _]+)(?:>`)",
        r"[\1][\2]",
        string,
    )


def download_links(string):
    """
    Update download links to Markdown formatting, add note to manually verify path, as
    the relative link needed for the Markdown to be happy may not match.
    """
    return re.subn(
        r":download:(?<!`)`(?!`)([\d\D']*?) <([a-zA-Z0-9-:\/\.# _]+)(?:>`)",
        r"[\1](\2) (TODO: Verify path.)",
        string,
    )


def ref_links(string):
    """
    Update rST reference links to MkDocs autorefs format.
    """
    return re.subn(r":ref:`([\d\D]+?)<([\d\D]+?)(>`?)", r"[\1][\2]", string)


def double_colon(string):
    """
    Update double-colon rST code directive to single for Markdown formatting.
    """
    return re.subn(r"::", r":", string)


def links_rst_to_markdown(string):
    """
    Convert rST links to Markdown links in translation files.

    Test strings:
    string = 'msgid "Si no se siente cómodo con el inglés, las traducciones de este tutorial están disponibles en `Alemán <https://docs.beeware.org/de>`__, `Español <https://docs.beeware.org/es>`__, `Français <https://docs.beeware.org/fr>`__, `Italiano <https://docs.beeware.org/it>`__, `Português <https://docs.beeware.org /pt>`__, `中文(简体) <https://docs.beeware.org/zh-cn>`__ y `中文(繁體) <https://docs.beeware.org/zh-tw>`__."'
    string = 'msgstr "**Git**, a version control system `git-scm.com <https://git-scm.com/downloads/>`__. You can download Git from from `git-scm.com <https://git-scm.com/downloads/>`__."'
    string = "`Toga <https://toga.beeware.org>`__, a cross platform widget toolkit;"
    string = "Cuando esté listo para publicar una aplicación real, consulte la guía práctica de Briefcase sobre `Cómo configurar una identidad de firma de código de macOS <https://briefcase.readthedocs.io/en/latest/how-to/code-signing/macOS.html>`__"
    string = "`Toga <https://toga.beeware.org>`__"
    string = "`Toga <https://toga.beeware.org>`__ `Toga <https://toga.beeware.org>`__"
    """

    return re.subn(
        r"(?<!`)`(?!`)([\d\D']*?) <([a-zA-Z0-9-:\/\.#` `_=\?\+\%]+)(?:>`_{1,2})",
        r"[\1](\2)",
        string,
    )


def inline_code_rst_to_markdown(string):
    """
    Convert rST inline code formatting to Markdown inline code formatting.

    TODO: RUN LINK UPDATES FIRST.
    """

    return re.subn(r"``([\d\D]*?)``", r"`\1`", string)


def link_placeholders(string):
    """
    Replaces all link URLs with `{1}` placeholder.

    TODO: This requires manual intervention afterward to update all strings with
          multiple links to have sequential numbers.

    TODO: RUN LAST.

    Links are represented in the PO files with `{#}` placeholders. The first link would
    be `[Link text]{1}`, for example. In a string with multiple links, each
    subsequent value is incremented by one. A string with four links would have `[]{1}`,
    `[]{2}`, `[]{3}`, and `[]{4}` within it.

    I was unable to sort out how to successfully do this programmatically. So I replaced
    them all with {1}, and searched for `{#}` beginning with 6, as the English Markdown
    was accurately numbered. I continued searching one less each time through 2 to
    ensure I updated all the placeholders properly; most of the strings contained only
    one link, so I concluded that it would be faster to do it manually than to continue
    trying to sort out the code to do it.

    NOTE: I could have simply replaced the link targets with `{#}` in the
    links_rst_to_markdown() function, however, leaving the links intact initially meant
    it was easier to identify the broken links. Running this separately was basically a
    safeguard.
    """
    return re.subn(r"((\(https:\/\/)([\d\D]*?)(\)))", r"{1}", string)


def convert(path):
    content = path.read_text()

    for method in [
        doc_links,
        download_links,
        ref_links,
        double_colon,
        links_rst_to_markdown,
        inline_code_rst_to_markdown,
        link_placeholders,
    ]:
        print(method.__name__, end=" ")

        content, subs = method(content)
        print("." * subs)

    Path(path.parent / path.name).write_text(content)


if __name__ == "__main__":
    for path in Path(sys.argv[1]).glob("**/*.po"):
        print("=" * 5 + str(path) + "=" * 20)
        convert(path)
