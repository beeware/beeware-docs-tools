import re
import sys
from pathlib import Path

# This was written with Toga in mind, which will be obvious looking through some of the
# code here. That said, it works on any Pandoc `commonmark_x` converted rST, as long as
# three changes are made to what Pandoc extensions are included with the command. It
# needs some work; running it on Toga highlighted some syntax that it's skipping.

# Run Pandoc with `commonmark_x-bracketed_spans-smart-alerts` as the output format.


def fenced_code_language_whitespace(string):
    """
    Removes the space between the initial code fence and the code language.

    Test string:
    string = "``` language"
    """
    return re.subn(r"``` (.+)\n", r"```\1\n", string)


def group_tabs(string):
    """
    Begins first tab in group tab content.

    Test string:
    string = ":::::::::: {.tabs}\n::: {.group-tab}\n"
    """
    return re.subn(r":+ {\.tabs}\n::: {\.group-tab}\n", r"/// tab | ", string)


def intermediate_group_tabs(string):
    """
    In group tab content, terminates the first and second tab, and begins
    the second and third tab.

    Test string:
    string = ":::\n\n:::: {.group-tab}\n"
    """
    return re.subn(r":{3,4}\n\n:{3,4} {.group-tab}\n", r"\n///\n\n/// tab | ", string)


def end_tab_nested_admonition(string):
    """
    Terminates tabbed section with nested admonition.

    Test string:
    string = "::::\n:::::::"
    """
    return re.subn(r":{4}\n:{7}", r"\n///\n\n///\n", string)


def end_group_tabs(string):
    """
    Terminates group tab sections.

    Test string:
    string = ":::\n::::::"
    """
    return re.subn(r":{3}\n:{6,10}", r"\n///", string)


def note(string):
    """
    Format `note` admonitions - will also work with attention,
    caution, danger, error, tip, hint, warning admonition types.

    Test string:
    # string = ":::: {.note}\n::: {.title}\nNote\n:::\n\nIf you're using a recent version of Android, you may notice that the app\nicon has been changed to a green snake, but the background of the icon\nis *white*, rather than light blue. We'll fix this in the next step.\n::::"
    """
    return re.subn(
        r":::: \{\.([a-z]+)}\n::: \{\.title}\n([a-zA-Z]+)\n:::\n\n([\d\D]*?)\n::::",
        r"/// \1 | \2\n\n\3\n\n///",
        string,
    )


def admonition(string):
    """
    Format admonitions.

    Test string:
    # string = "::: {.admonition}\nText that is sometimes multiple words\n\nContent - often\nmultiline\n:::"
    """
    return re.subn(
        r"::: \{\.(admonition)}\n([\d\D]*?)\n\n([\d\D]*?):::",
        r"/// \1 | \2\n\n\3\n\n///",
        string,
    )


def header_anchors(string):
    """
    Formats headers and header anchors. If anchor text matches header text, anchor is
    removed, as Markdown generates matching anchors by default. If anchor text does
    not match header text, anchor is replaced with attr-plugin formatted version.

    Some of these text strings aren't applicable anymore; the initial Pandoc run was
    adding custom anchors to everything, not only where they already existed. I
    excluded that extension from the Pandoc command.

    TODO: UPDATE THIS TO MATCH PROPER FORMATTING
    TODO: RUN BEFORE docs_links_header_and_text.

    Test strings:
    string = {
    "string_one": "# Header text {#foo}",
    "string_two": "# Header text {#header-text}",
    "string_three": "# Header text - with dash... {#header-text---with-dash...}",
    "string_four": '# `~header.Text.FOO`{.interpreted-text role="attr"} {#header.text.foo}',
    "string_five": '# `~header.text`{.interpreted-text role="class"} {#header.text}',
    }
    """
    matches = re.findall(
        r"((#+) ([`~]*)([A-Za-z0-9\- .]*)(?:`*)(?:{.interpreted-text role=\")?([A-Za-z]*)?(?:\"})?(?: )?(?:\{)?(#+)?([a-z0-9\-.]*)(?:\})?)",
        string,
    )

    subs = 0
    for match in matches:
        comparison_string = (
            match[3].lower().rstrip(" ").replace(".", "-").replace(" ", "-")
        )
        if "..." in match[6]:
            replacement_string = f"{match[0]} {match[3]}"
        elif match[2] == "" and match[6] != "" and comparison_string == match[6]:
            replacement_string = f"{match[1]} {match[2]}"
        elif match[2] == "" and match[6] != "" and comparison_string != match[6]:
            replacement_string = f'{match[1]} {match[3]} {{ id="{match[6]}" }}'
        elif match[2] == "`~" and match[6] == match[3].lower():
            replacement_string = f"{match[1]} `{match[3]}`"
            print(f"{replacement_string} is type {match[4]}")
        elif match[2] == "`~" and match[6] != match[3].lower():
            replacement_string = f'{match[1]} `{match[3]}` {{ "id={match[6]}" }}'
            print(f"{replacement_string} is type {match[4]}")
        else:
            replacement_string = None

        if replacement_string:
            string = string.replace(match[0], replacement_string)
            subs += 1

    return string, subs


def external_doc_links(string):
    """
    Update external to autorefs format.

    Links list below no longer needed as autorefs automatically links to the
    Python/Pillow docs.

    TODO: RUN BEFORE docs_links_header_and_text.

    Test strings:
    strings = [
        '`pathlib.Path`{.interpreted-text role="any"}',
        '`list`{.interpreted-text role="any"}',
        '`memoryview`{.interpreted-text role="any"}',
        '`bytearray`{.interpreted-text role="any"}',
        '`bytes`{.interpreted-text role="any"}',
        '`str`{.interpreted-text role="any"}',
        '`tuple`{.interpreted-text role="any"}',
        '`None`{.interpreted-text role="any"}',
        '`datetime.date`{.interpreted-text role="any"}',
        '`datetime.datetime`{.interpreted-text role="any"}',
        '`~decimal.Decimal`{.interpreted-text role="class"}',
        '`int`{.interpreted-text role="any"}',
        '`float`{.interpreted-text role="any"}',
        '`importlib.metadata`{.interpreted-text role="any"}',
        '`PermissionError`{.interpreted-text role="any"}',
        '`asyncio.Task`{.interpreted-text role="any"}',
        '`PIL.Image.Image`{.interpreted-text role="any"}',
    ]
    """
    # links = {
    #     "`pathlib.Path`": "https://docs.python.org/3/library/pathlib.html#pathlib.Path",
    #     "`list`": "https://docs.python.org/3/library/stdtypes.html#list",
    #     "`memoryview`": "https://docs.python.org/3/library/stdtypes.html#memoryview",
    #     "`bytearray`": "https://docs.python.org/3/library/stdtypes.html#bytearray",
    #     "`bytes`": "https://docs.python.org/3/library/stdtypes.html#bytes",
    #     "`str`": "https://docs.python.org/3/library/stdtypes.html#str",
    #     "`tuple`": "https://docs.python.org/3/library/stdtypes.html#tuple",
    #     "`None`": "https://docs.python.org/3/library/constants.html#None",
    #     "`datetime.date`": "https://docs.python.org/3/library/datetime.html#datetime.date",
    #     "`datetime.datetime`": "https://docs.python.org/3/library/datetime.html#datetime.datetime",
    #     "`Decimal`": "https://docs.python.org/3/library/decimal.html#decimal.Decimal",
    #     "`int`": "https://docs.python.org/3/library/functions.html#int",
    #     "`float`": "https://docs.python.org/3/library/functions.html#float",
    #     "`importlib.metadata`": "https://docs.python.org/3/library/importlib.metadata.html#module-importlib.metadata",
    #     "`PermissionError`": "https://docs.python.org/3/library/exceptions.html#PermissionError",
    #     "`asyncio.Task`": "https://docs.python.org/3/library/asyncio-task.html#asyncio.Task",
    #     "`PIL.Image.Image`": "https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image",
    # }

    strings = [
        '`pathlib.Path`{.interpreted-text role="any"}',
        '`list`{.interpreted-text role="any"}',
        '`memoryview`{.interpreted-text role="any"}',
        '`bytearray`{.interpreted-text role="any"}',
        '`bytes`{.interpreted-text role="any"}',
        '`str`{.interpreted-text role="any"}',
        '`tuple`{.interpreted-text role="any"}',
        '`None`{.interpreted-text role="any"}',
        '`datetime.date`{.interpreted-text role="any"}',
        '`datetime.datetime`{.interpreted-text role="any"}',
        '`~decimal.Decimal`{.interpreted-text role="class"}',
        '`int`{.interpreted-text role="any"}',
        '`float`{.interpreted-text role="any"}',
        '`importlib.metadata`{.interpreted-text role="any"}',
        '`PermissionError`{.interpreted-text role="any"}',
        '`asyncio.Task`{.interpreted-text role="any"}',
        '`PIL.Image.Image`{.interpreted-text role="any"}',
    ]

    matches = re.findall(
        r'((`)(~decimal.)?([A-Za-z.`]+){.interpreted-text(?:[ \n]*)?role="(?:[a-z]+)"})',
        string,
    )

    subs = 0
    for match in matches:
        if match[3] in "".join(strings) and match[3] != "Image`":
            replacement_string = f"[{match[1]}{match[3]}][]"
        elif match[3] == "Image`":
            replacement_string = "[`toga.Image`][]"
        elif match[3] == "ImageConverter`":
            replacement_string = "[`toga.images.ImageConverter`][]"
        elif match[2] == "~decimal.":
            replacement_string = "[`Decimal`][]"
        else:
            replacement_string = None
        if replacement_string:
            string = string.replace(match[0], replacement_string)
            subs += 1

    return string, subs


def doc_links_header_and_text(string):
    """
    Convert doc, ref, method, etc. links. Where applicable, strip leading `/` and `/index`.

    For `role="ref"`, if anchor and header do not match, replace anchor with
    attr-plugin formatted version.

    TODO: Get actual test strings, and sort out the autoref formats for them.

    Test strings:
    strings = {
        "string_one": '`a hands-on introduction to Toga </tutorial/index>`{.interpreted-text role="doc"}',
        "string_two": '## `How-to guides <how-to/index>`{.interpreted-text role="ref"}',
        "string_three": '`overall architectural details </reference/internals/index>`{.interpreted-text role="doc"}',
        "string_four": '`the \ndocumentation on document handling <./resources/document>`{.interpreted-text\n role="doc"}',
        "string_five": '`~toga.Bar.baz`{.interpreted-text role="meth"}',
        "string_six": '`Foo <path/bar>`{.interpreted-text role="buzz"}',
        "string_seven": '`Foo <bar>`{.interpreted-text role="baz"}',
        "string_eight": '## `Text <ref-header-name>`{.interpreted-text role="ref"}',
        "string_nine": '## `Ref header name <ref-header-name>`{.interpreted-text role="ref"}',
        "string_ten": '`installed all the platform pre-requisites\n<install-dependencies>`{.interpreted-text role="ref"}'
    }
    """
    matches = re.findall(
        r"((#*)?( )?`(~)?([A-Za-z0-9\n. \-_!'\"]*)(?:\(\))?(?:<)?(?:\/)?([.a-z0-9\/\-]*)?>?`{.interpreted-text(?:\n)?(?: )?role=\"([a-z]+)\"})",
        string,
    )

    subs = 0
    replacement_string = None
    for match in matches:
        trimmed_content = match[4].rstrip()
        print(trimmed_content)
        if (
            match[6] == "download"
        ):  # There's a download link that gets wrapped up in a different block if not dealt with here
            replacement_string = f"[{trimmed_content}]({match[5]})"
        elif (match[6] == "ref" or match[6] == "doc") and match[
            6
        ] != "download":  # If the type is `ref` or `doc`, but not `download`
            comparison_string = match[5].replace(
                "-", " "
            )  # Pull the path to compare to the link text
            if (
                comparison_string == match[4].rstrip().lower() and "#" in match[1]
            ):  # Does the header link text match the path
                replacement_string = (
                    f"{match[1]}{trimmed_content}"  # Header is all that is needed
                )
            elif (
                comparison_string != match[4].rstrip().lower()
                and "/index" not in match[5]
            ):  # Link text does not match path and no index in path
                if match[1] and "#" in match[1]:  # It's a header
                    replacement_string = f'{match[1]}[{trimmed_content}] {{ id="{match[5]}" }}'  # Update custom header anchor to autodoc format
                elif match[5] and "/" in match[5]:  # Text with a path that is not index
                    replacement_string = f"{match[2]}[{match[4].replace('\n', ' ').rstrip()}]({match[5]})"  # Made into link format
                else:  # Text with a non-matching anchor
                    replacement_string = f"{match[2]}[{match[4].replace('\n', ' ').rstrip()}][{match[5]}]"  # Made into autodoc format
            elif (
                match[1] and "#" in match[1] and "/index" in match[5]
            ):  # Header with index in the path
                comparison_string = (
                    match[5].removesuffix("/index").replace("-", " ")
                )  # Strip `/index` off path, and prepare for comparison to header text
                if (
                    comparison_string != trimmed_content.lower()
                ):  # If the header text doesn't match the path without `/index`
                    replacement_string = f'{match[1]}[{trimmed_content}] {{ id="{match[5].removesuffix("/index")}" }}'  # Create header link with reference ID
                else:  # If header text matches path
                    replacement_string = (
                        f"{match[1]}[{trimmed_content}]"  # Create bare header
                    )
            elif not match[1] and "/index" in match[5]:  # Not a header, index in path
                replacement_string = f"{match[2]}[{match[4].replace('\n', ' ').rstrip()}]({match[5].removesuffix('/index')})"  # Create link without `/index`
        elif "toga" in match[4] and match[6] == "meth":  # Type `meth`
            if match[3] == "~":  # `~` name only
                class_name = match[4].split(
                    "."
                )  # Split the method name to generate `~` name
                replacement_string = f"{match[2]}[`{class_name[(len(class_name) - 1)]}()`][{trimmed_content}]"  # `~` name in autoref format with `()`
            else:  # Full name
                replacement_string = f"{match[2]}[`{trimmed_content}()`][{trimmed_content}]"  # Autoref format with `()`
        elif (
            "toga" in match[4] and match[6] != "meth"
        ):  # Class name but not type `meth`
            if match[3] == "~":  # ~ name only
                class_name = match[4].split(
                    "."
                )  # Split the method name to generate `~` name
                replacement_string = f"{match[2]}[`{class_name[(len(class_name) - 1)]}`][{trimmed_content}]"  # `~` name in autoref format
            else:  # Full class name
                replacement_string = (
                    f"{match[2]}[`{trimmed_content}`][]"  # autoref format
                )
        elif "/" not in match[5]:  # The link is a reference ID, not a URL
            replacement_string = f"{match[2]}[{trimmed_content}][{match[5]}]"  # Autoref format with reference ID
        elif (
            "toga" not in match[4] and match[4][0].islower()
        ):  # This is most likely a missed external reference
            replacement_string = f"{match[2]}[{trimmed_content}][]<!-- TODO: Verify this is an accurate link -->"  # Verify whatever this was is accurate
        elif (
            "toga" not in match[4] and (match[4][0].isupper() or match[4][1].isupper())
        ):  # A Toga reference without the full name, beginning with `.` or not (49 at time of writing)
            replacement_string = f"{match[2]}[{trimmed_content}][{trimmed_content}]<!-- TODO: Update to full reference -->"  # Manually fix afterwards.

        if replacement_string:
            string = string.replace(match[0], replacement_string)
            subs += 1

    return string, subs


def literal_include(string):
    """
    Convert rST literal includes to Markdown using Macros plugin format.

    Test string:
    string = ' {.literalinclude language="python"}\n/../examples/tutorial4/tutorial/app.py\n'
    """
    return re.subn(
        r"::: {.literalinclude language=\"([a-z]+)\"}\n/../examples/([a-z0-9]+)/tutorial/app.py\n:::",
        r'```\1\n{% include "../../examples/\2/tutorial/app.py" %}\n```',
        string,
    )


def auto_module_function_class(string):
    """
    Convert autodoc directives to mkdocstrings. In special cases,
    includes instructions on adding appropriate members list.

    Test strings:
    strings = [
        '::: {.autoclass}\ntoga.Foo\n:::',
        '::: {.autoprotocol}\ntoga.Foo\n:::',
        '::: {.namedtuple}\ntoga.Foo\n:::',
        '::: {.autoclass exclude-members="bar, baz"}\ntoga.Foo\n:::',
        '::: {.autoclass special-members="bar, baz"}\ntoga.Foo\n:::',
    ]
    """

    matches = re.findall(
        r"((:{3,6} {\.)([a-z]*?)( )?([a-zA-Z\-=]*?)?([a-zA-Z, \"_\n]*?)?(}\n)([a-zA-Z.]*?)?(\n:::))",
        string,
        flags=re.MULTILINE,
    )

    subs = 0
    for match in matches:
        if match[4]:
            if "exclude-members" in match[4]:
                replacement_string = f"::: {match[7]}\n    options:\n        members:\n            TODO: Add explicit members list excluding {match[5]}"
            elif "member-order" in match[4]:
                replacement_string = f"::: {match[7]}\n    options:\n        members:\n            TODO: Add explicit members list in the following order {match[5]}"
            elif "special-members" in match[4]:
                replacement_string = f"::: {match[7]}\n    options:\n        members:\n            TODO: Add explicit members list *excluding* special members *except* for {match[5]}"
            elif "inherited-members" in match[4]:
                replacement_string = f"::: {match[7]}\n    options:\n        members:\n            TODO: Do I need to add inherited members list including {match[5]}?"
        elif "namedtuple" in match[3]:
            replacement_string = f"::: {match[7]}\n    options:\n        members:\n            TODO: Add full members list"
        else:
            replacement_string = f"::: {match[7]}"

        if replacement_string:
            string = string.replace(match[0], replacement_string)
            subs += 1

    return string, subs


def spelling_ignore(string):
    """
    TODO: Update this for pyspelling syntax.
    Tag inline `codespell:ignore` directives to be shifted to the ignore words file.

    Test string:
    string = '`foo`{.interpreted-text role="spelling:ignore"}'
    """
    return re.subn(
        r"`([A-Za-z]+)(.+)(spelling:ignore)",
        r"\1<!-- TODO: Add to spelling_wordlist.txt file -->",
        string,
    )


def toctree(string):
    """
    Generates list of links from toctree entries. Removes hidden toctree entries
    as the toctrees are automatically generated by MkDocs and Material theme.
    Includes instructions to verify links, and add page headings if `maxdepth=2`.

    Test strings:
    strings = [
        '::: {.toctree maxdepth="1"}\nfoo bar baz\n:::',
        '::: {.toctree maxdepth="2" glob=""}\nfoo bar baz\n:::',
        '::: {.toctree}\nfoo bar/index baz/page\n:::',
        '::: {.toctree maxdepth="2" hidden="" titlesonly=""}\nfoo bar/index baz/page\n:::',
    ]
    """

    matches = re.findall(
        r"(::: {.toctree([A-Za-z0-9=\" ]+)?}\n([a-zA-Z0-9_\/ \-\n]+)\n:::)", string
    )

    subs = 0
    for match in matches:
        if match[1] and "hidden" not in match[1]:
            if match[1] and 'maxdepth="2"' in match[1]:
                todo = "TODO: Check on links, add page headings?"
            else:
                todo = "TODO: Check text on links."
            toctree_string = []
            split_links = f"{match[2]}"
            split_link_list = split_links.split(" ")
            for link in split_link_list:
                if "/" in link:
                    link_name = link.split("/")[1]
                    if link_name == "index":
                        link_name = link.split("/")[0]
                        link_string = f"[{link_name.title()}](./{link}.md)"
                        toctree_string.append(link_string)
                    else:
                        link_string = f"[{link_name.title()}](./{link}.md)"
                        toctree_string.append(link_string)
                else:
                    link_string = f"[{link.title()}](./{link})"
                    toctree_string.append(link_string)
            replacement_string = f"{'\n'.join(toctree_string)}\n{todo}"
        else:
            replacement_string = "\n"

        if replacement_string:
            string = string.replace(match[0], replacement_string)
            subs += 1

    return string, subs


def platform_support_indicators(string):
    """
    Update platform support indicators on support tables to current format.

    Test strings contain invalid escape sequences.
    See toga/docs/reference/api/widgets/table.md for instances of no and beta examples.
    """

    matches = re.findall(r"(\[\\\|([a-z]+)\\\|\]\(##SUBST##\|(?:[a-z]+)\|\))", string)

    subs = 0
    for match in matches:
        if match[1] == "beta":
            replacement_string = "{{ beta_support }}"
        elif match[1] == "no":
            replacement_string = "{{ not_supported }}"
        else:
            replacement_string = None

        if replacement_string:
            string = string.replace(match[0], replacement_string)
            subs += 1

    return string, subs


def text_above_mkdocstrings(string):
    """
    In the event of text occurring above current autodoc directives,
    add instructions to verify that the text block is not intended to
    be part of the source code. Example: ImageContentT.

    Test string:
    string = ## Reference

    > An item of `OptionContainer`{.interpreted-text role="any"} content can
    > be:
    >
    > - a 2-tuple, containing the title for the tab, and the content widget;
    > - a 3-tuple, containing the title, content widget, and
    >   `icon <IconContentT>`{.interpreted-text role="any"} for the tab;
    > - a 4-tuple, containing the title, content widget,
    >   `icon <IconContentT>`{.interpreted-text role="any"} for the tab, and
    >   enabled status; or
    > - an `toga.OptionItem`{.interpreted-text role="any"} instance.

    :::
    """

    result = re.search(r"(## Reference\n)\n([\d\D]*?):::", string)
    if result and result.group(2):
        return re.subn(
            r"(## Reference\n)\n([\d\D]*?):::",
            r"\1TODO: Verify the below text is not meant to be in the source code:\n\2:::",
            string,
        )
    return string, 0


def remove_rst_class_from_widget_pages(string):
    """
    Remove rst-class directive from widget tables.

    Test strings:
    """
    #     strings = [
    #         """::: {.rst-class}
    # widget-support
    # :::""",
    #         """::: {.rst-class}
    # widget-descriptions
    # :::"""
    #         ]

    return re.subn(r"\n::: {.rst-class}\nwidget-([a-z]+)\n:::\n", r"", string)


def csv_table_widget_pages(string):
    """Convert CSV tables on individual widget pages to updated format.

    TODO: Update .csv to have Markdown reference links, rename first
        column to "Component Name", replace "stable"/"etc" with the
        graphic dots. Partial update in toga-mkdocs.

    Test string:
    string = ::: {.csv-filter header-rows="1" file="../../data/widgets_by_platform.csv" included_cols="0,1,2,3,4,5" include="{0: '^Foo$'}"}
    Availability (`Key <api-status-key>`{.interpreted-text role="ref"})
    :::
    """

    replacement_string = r'Availability ([Key][api-status-key])\n\n{{ pd_read_csv("reference/data/widgets_by_platform.csv", na_filter=False, usecols=[\1])[pd_read_csv("reference/data/widgets_by_platform.csv")[["ComponentName"]].isin(["\2"]).all(axis=1)] | convert_to_md_table }}'

    return re.subn(
        r"::: \{.csv-filter header-rows=\"1\" file=\"(?:[\.\/a-z_]+)\" included_cols=\"([0-9,]+)\" include=\"\{0: '\^([A-Za-z ]+)\$'\}\"\}\nAvailability \(`Key <api-status-key>`\{.interpreted-text role=\"ref\"\}\)\n:::",
        replacement_string,
        string,
    )


def csv_table_widgets_by_platform(string):
    """Convert CSV tables on Widgets by Platform page to updated format.

    TODO: Update .csv to have Markdown reference links, rename first
        column to "Component Name", replace "stable"/"etc" with the
        graphic dots. Partial update in toga-mkdocs.

    Test string:
    string = ::: {.csv-filter .longtable file="data/widgets_by_platform.csv" header-rows="1" exclude="{1: '(?!(Type|Layout Widget))'}" included_cols="2,4,5,6,7,8,9,10" stub-columns="1" widths="3 1 1 1 1 1 1 1"}
    :::
    """

    replacement_string = r'{{ pd_read_csv("reference/data/widgets_by_platform.csv", na_filter=False, usecols=[\2])[pd_read_csv("reference/data/widgets_by_platform.csv")[["Type"]].isin(["\1"]).all(axis=1)] | convert_to_md_table }}'
    return re.subn(
        r"::: \{.csv-filter .longtable file=\"(?:[\.\/a-z_]+)\" header-rows=\"1\" exclude=\"\{1: \'\(\?\!\(Type\|([a-zA-Z ]+)\)\)\'\}\" included_cols=\"([0-9,]+)\" stub-columns=\"1\" widths=\"3 1 1 1 1 1 1 1\"\}\n:::",
        replacement_string,
        string,
    )


def aligned_image(string):
    """Convert Markdown image with align specified to HTML figure.

    Test strings:
    strings = [
        "![Hello World Tutorial 8 dialog, on Linux](images/linux/tutorial-8.png){.align-center}",
        "![Hello World Tutorial 8 dialog, on Windows](images/windows/tutorial-8.png){.align-center}",
    ]
    """

    return re.subn(
        r"(![\d\D]*?)(\([\d\D]*?\))\{\.align-center\}",
        r"\1\2\n\n\\\\\\ caption\n\n\\\\\\\n\n",
        string,
    )


def markdown_image_with_width(string):
    """
    Convert Markdown image with width specified to HTML figure.

    Test strings:
    """
    #     strings = [
    #         """![image](/reference/screenshots/winforms.png){.align-center
    # width="300px"}""",
    #         '![image](/reference/screenshots/gtk.png){.align-center width="300px"}'
    #     ]

    return re.subn(
        r"(![\d\D]*?)(\([\d\D]*?\))\{\.(?:[a-z\-]+)(?: )?(?:\n)?(?:width=\")([0-9a-z]+)?\"\}",
        r'\1\2{ width="\3" }\n<!-- TODO: Update alt text -->',
        string,
    )


def figure(string):
    """
    Convert HTML figure to Markdown image syntax. Add note to update alt-text if it is
    set to be the image path.

    Test strings:
    """
    # """
    # <figure class="align-center">
    # <img src="/reference/images/canvas-cocoa.png" width="300"
    # alt="/reference/images/canvas-cocoa.png" />
    # </figure>
    # """
    # """
    # <figure class="align-center">
    # <img src="screenshots/tutorial-3.png" width="300"
    # alt="screenshots/tutorial-3.png" />
    # </figure>
    # """

    matches = re.findall(
        r'(<figure( class="align\-center")?>\n<img src="([\d\D]*?)"( width="([0-9]*)")?\nalt="([\d\D]*?)" \/>\n<\/figure>)',
        string,
    )

    subs = 0
    for match in matches:
        if match[2] == match[5]:
            todo = "\n<!-- TODO: Update alt text -->"
        else:
            todo = ""
        if "align-center" in match[1] and "width" not in match[3]:
            replacement_string = (
                f"![{match[5]}]({match[2]})\n\n/// caption\n\n///n\n{todo}"
            )
        elif "width" in match[3] and "align-center" not in match[1]:
            replacement_string = (
                f'![{match[5]}]({match[2]}){{ width="{match[4]}" }}{todo}'
            )
        elif "align-center" in match[1] and "width" in match[3]:
            replacement_string = f'![{match[5]}]({match[2]}){{ width="{match[4]}" }}\n\n/// caption\n\n///\n\n{todo}'

        if replacement_string:
            string = string.replace(match[0], replacement_string)
            subs += 1

    return string, subs


def dash_item(string):
    """
    Remove directive notation on -item blocks.

    Test strings:
    """
    #     strings = [
    #         """::: {#treesource-item}
    # When creating a single Node for a TreeSource (e.g., when inserting a new
    # item), the data for the Node can be specified as:
    # :::""",
    #         """::: {#listsource-item}
    # The ListSource manages a list of `~toga.sources.Row`{.interpreted-text
    # role="class"} objects. Each Row has all the attributes described by the
    # source's `accessors`. A Row object will be constructed for each item
    # that is added to the ListSource, and each item can be:
    # :::"""
    #     ]

    return re.subn(r"::: \{#(?:[a-z\-]+)\}\n([\d\D]*?):::", r"\1", string)


def doc_ref_any(string):
    """
    TODO: Fix this so it actually converts all of them.
    Grabs the last of the :notation: links that were missed above, including `doc`,
    `ref` and `any` links. Doesn't work on all of them due to the regex, so those that
    are still left are tagged with "Manually fix this".
    """
    matches = re.findall(
        r'(`([\d\D]*?)(?: )?(?:\n)?<([\d\D]*?)>`{.interpreted-text(?:\n)?(?:[ ]*)?role="([a-z]+)"})',
        string,
    )

    subs = 0
    for match in matches:
        if "`" in match[1]:
            replacement_string = f"{match[0]} - TODO: Manually fix this"
        elif "/" in match[2]:
            replacement_string = f"[{match[1]}]({match[2]})"
        else:
            replacement_string = f"[{match[1]}][{match[2]}]"

        if replacement_string:
            string = string.replace(match[0], replacement_string)
            subs += 1

    return string, subs


def markdown_reference_fix(string):
    """
    Initially forgot to include backticks on the code reference autoref links.
    This fixes that. Leaving it in here in case the update to the method above
    that handles the autoref links missed anything.
    """
    matches = re.findall(r"(\[([\d\D]*?)\]\[([\d\D]*?)\])", string)
    subs = 0
    for match in matches:
        if "toga" in match[1] and match[2] == "":
            replacement_string = f"[`{match[1]}`][]"
        elif "toga" not in match[1] and "." in match[2]:
            replacement_string = f"[`{match[1]}`][{match[2]}]"
        else:
            replacement_string = f"{match[0]}"

        if replacement_string:
            string = string.replace(match[0], replacement_string)
            subs += 1

    return string, subs


def convert(path):
    content = path.read_text()

    for method in [
        # remove_rst_class_from_widget_pages,
        # csv_table_widget_pages,
        # csv_table_widgets_by_platform,
        # fenced_code_language_whitespace,
        # group_tabs,
        # intermediate_group_tabs,
        # end_tab_nested_admonition,
        # end_group_tabs,
        # header_anchors,
        # note,
        # admonition,
        # literal_include,
        # auto_module_function_class,
        # external_doc_links,
        # doc_links_header_and_text,
        # toctree,
        # platform_support_indicators,
        # text_above_mkdocstrings,
        # aligned_image,
        # markdown_image_with_width,
        # figure,
        # dash_item,
        # doc_ref_any,
    ]:
        print(method.__name__, end=" ")

        content, subs = method(content)
        print("." * subs)

    Path(path.parent / (path.name)).write_text(content)


if __name__ == "__main__":
    for path in Path(sys.argv[1]).glob("**/*.md"):
        print("=" * 5 + str(path) + "=" * 20)
        convert(path)
