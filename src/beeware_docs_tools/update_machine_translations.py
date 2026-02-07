import os
import re
import textwrap
from argparse import ArgumentParser, Namespace
from pathlib import Path

import deepl
import polib


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description=(
            "Update translations for a documentation set. Uses the DeepL API "
            "to provide a machine translation of every untranslated string "
            "for the given language. Machine translations are marked 'fuzzy' "
            "as an indicator that additional translation work is required."
        )
    )
    parser.add_argument(
        "--soft-fail",
        action="store_true",
        help="Fail without raising an error if the API key cannot be found",
    )
    parser.add_argument(
        "-d",
        "--docs-directory",
        dest="docs_path",
        type=Path,
        default="docs",
        help=(
            "The path to a documentation set. The provided location should "
            "contain a 'locales' subdirectory. Defaults to `./docs`"
        ),
    )
    parser.add_argument("language_code", nargs="+", help="The language to translate.")

    args = parser.parse_args()

    if not (args.docs_path / "locales").is_dir():
        raise RuntimeError(
            f"Input path {args.docs_path} should contain a 'locales' directory"
        )

    for language_code in args.language_code:
        if not (args.docs_path / "locales" / language_code).exists():
            raise RuntimeError(
                f'A translation for "{language_code}" does not exist in {args.docs_path}'
            )

    return args


def translate(client, path, language):
    # 78 is 80, allowing for an open and closing "
    po = polib.pofile(path, wrapwidth=100000)
    changes = 0
    # DeepL uses some slightly different language variant descriptors.
    # Map those, using the input languages as a default.
    deepl_lang = {
        "pt": "pt-BR",
        "zh_CN": "zh-HANS",
        "zh_TW": "zh-HANT",
    }.get(language, language)

    untranslated_count = len(po.untranslated_entries())
    print(
        f"  {language}: Translate {path.relative_to(Path.cwd())} "
        f"({untranslated_count} untranslated entries)"
    )
    for i, entry in enumerate(po.untranslated_entries(), start=1):
        print(
            f"    {language}:{path.name} "
            f"| {entry.msgid[:50]}{'...' if len(entry.msgid) > 50 else ''}"
        )
        # If there are any untranslated entries, the translation is dirty, and
        # will need to be saved.
        changes += 1

        if entry.msgid.startswith("///"):
            parts = entry.msgid.split("|")
            # Special case - don't attempt to translate "///" markers, and make
            # sure that well known product-based tab labels aren't translated.
            if len(parts) == 1 or parts[1] in {
                " Windows",
                " macOS",
                " Linux",
                " iOS",
                " Android",
            }:
                translated = entry.msgid
                fuzzy = False
            else:
                # Only translate the content after the |
                translated = "|".join(
                    [
                        parts[0],
                        client.translate_text(parts[1], target_lang=deepl_lang).text,
                    ]
                )
                fuzzy = True
        elif entry.msgid.startswith("(.venv)"):
            # A string starting with `(.venv)` is clearly part of a
            # multiline code literal.
            translated = entry.msgid
            fuzzy = False
        elif match := re.match(r"(.*)( { #[-\w]* })", entry.msgid):
            # A title with an explicit anchor should only translate the title
            title = client.translate_text(match.group(1), target_lang=deepl_lang).text
            translated = f"{title}{match.group(2)}"
            fuzzy = True
        elif (
            any((jinja in entry.msgid) for jinja in ["{{", "}}", "{%", "%}"])
            or "`" in entry.msgid
        ):
            # If a string contains Jinja content, build a version of the string where
            # Jinja content has been replaced with {}. Translate *that* string, then
            # use format() to push the Jinja tag content back in.
            # We also need to catch [links]{1} so that the .format() approach to
            # reconstruct the string works, and `code samples` (including code samples
            # that contain ```).
            between = []
            tags = []
            last = 0
            jinja_re = re.compile(r"{\d+}|`(?:[^`]|```)+`|\({%.*?%}\)|{{.*?}}|{%.*?%}")
            while match := jinja_re.search(entry.msgid, pos=last):
                between.extend([entry.msgid[last : match.start()], "{}"])
                last = match.end()
                tags.append(match.group())

            between.append(entry.msgid[last:])
            between = "".join(between)
            if between == "{}":
                # If a string *only* contains Jinja content, use the string verbatim,
                # and mark the string as fully translated.
                translated = entry.msgid
                fuzzy = False
            else:
                # Translate the text with dummy placeholders
                raw_trans = client.translate_text(between, target_lang=deepl_lang).text
                # Substitute back in the tag content
                try:
                    translated = raw_trans.format(*tags)
                    fuzzy = True
                except (KeyError, ValueError):
                    # DeepL sometimes fails to return {} unmodified. This breaks
                    # the substitution process, but it's near impossible to recover,
                    # so ignore the string and move on.
                    print("        DeepL failed to handle this correctly...")
                    print("        input: ", entry.msgid)
                    print("        raw: ", raw_trans)
                    translated = None

                except Exception:
                    print("input: ", entry.msgid)
                    print("raw: ", raw_trans)
                    raise
        else:
            translated = client.translate_text(entry.msgid, target_lang=deepl_lang).text
            fuzzy = True
        if translated:
            entry.msgstr = translated
            entry.fuzzy = fuzzy

        # Save every 10 translations in case of a crash.
        if changes % 10 == 0:
            print(f"      ... saving progress ({i}/{untranslated_count})")
            po.save(path)

    # Only save if there are new translations.
    if changes:
        print(f"Saving {changes} new machine translations.")
        po.save(path)
    else:
        print("No new machine translations.")


def main():
    args = parse_args()
    try:
        client = deepl.DeepLClient(os.environ["DEEPL_API_KEY"])
    except KeyError:
        if args.soft_fail:
            print(
                textwrap.dedent("""
                    *******************************************************
                    *         WARNING: No DeepL API key found.            *
                    *******************************************************

                        Machine translations will be skipped. If you want
                        to update machine translations, ensure that the
                        environment variable DEEPL_API_KEY has been set.

                    *******************************************************
                    """)
            )
        else:
            raise RuntimeError(
                "No DeepL API key found; set the DEEPL_API_KEY environment variable."
            ) from None
    else:
        for language in args.language_code:
            print(f"Translating {language}:")
            for po_path in (args.docs_path / "locales" / language).glob("**/*.po"):
                translate(client, po_path.resolve(), language)
            if (po_path := args.docs_path / "locales" / f"{language}.po").is_file():
                translate(client, po_path.resolve(), language)


if __name__ == "__main__":
    main()
