import os
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
    print(f"  {language}: Translate {path.relative_to(Path.cwd())}")
    # 78 is 80, allowing for an open and closing "
    po = polib.pofile(path, wrapwidth=78)
    changes = 0
    for entry in po.untranslated_entries():
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
                        client.translate_text(parts[1], target_lang=language).text,
                    ]
                )
                fuzzy = True
        else:
            translated = client.translate_text(entry.msgid, target_lang=language).text
            fuzzy = True
        entry.msgstr = translated
        entry.fuzzy = fuzzy

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
