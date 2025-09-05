import shutil
from argparse import ArgumentParser, Namespace
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

# This tool is used to generate updated PO files from updated PO template (POT)
# files, which are based on the English Markdown content.
#
# The Markdown content can optionally contain external shared content included
# using the PyMdown Snippets extension. To facilitate translation of the shared
# content, it is included as part of BeeWare Docs Tools, along with the
# associated `locales` directory containing the shared content POT and
# translated PO files. This content is then processed separately from the
# primary content, and the resulting files are stored within the `docs-tools`
# repo `src` directory. When BeeWare Docs Tools is installed into a
# documentation repo, it includes the shared Markdown and PO files. They are
# then made available to the other translation- and build-tools, so when they
# are run, they are able to access the translated shared content and build each
# translated site in a given language.


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("language_code", nargs="*")
    args = parser.parse_args()

    for language in args.language_code:
        if not (Path.cwd() / f"docs/locales/{language}").is_dir():
            raise RuntimeError(
                f'Language code "{language}" does not match an existing translation'
            )

    return args


def pot_to_po(
    root_path: Path,
    docs: str,
    language: str,
    output_path: Path,
) -> None:
    """
    Run `pot2po` with the provided directories.

    :param root_path: The root directory of the documentation content.
    :param docs: The directory fragment, relative to the root path, containing
        the `locales` directory.
    :param language: The language code to convert.
    :param output_path: The root of the output folder where the updated PO file
        will be written.
    """
    (output_path / docs / language).mkdir(parents=True)
    subprocess.run(
        [
            "pot2po",
            f"--template={root_path / docs / f'locales/{language}/translations.po'}",
            f"--input={root_path / docs / 'locales/template/translations.pot'}",
            f"--output={output_path / docs / language}",
        ],
        check=True,
    )


def generate_po_files(root_path: Path, docs: str) -> None:
    """
    Generate PO files from PO template (POT) files.

    :param root_path: The root directory of the documentation content.
    :param docs: The directory fragment, relative to the root path, containing
        the `locales` translation files directories.
    """
    args = parse_args()

    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for language in args.language_code:
            print(f"Processing {language} content from {docs}")

            # Generates PO files from POT files into a temporary destination
            # directory.
            pot_to_po(
                root_path=root_path,
                docs=docs,
                language=language,
                output_path=temp_path,
            )

            # Copies the updated PO file to the `docs` directory.
            shutil.copyfile(
                (temp_path / docs / language / "translations.po"),
                (root_path / docs / f"locales/{language}/translations.po"),
            )


def main():
    # Generate primary content PO files
    generate_po_files(Path.cwd(), "docs")
    # Generate shared content PO files
    generate_po_files(Path(__file__).parent, "shared_content")


if __name__ == "__main__":
    main()
