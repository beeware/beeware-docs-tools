import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

# This tool is used to generate PO template (POT) files from English Markdown
# content.
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


def markdown_to_pot(root_path: Path, docs: str, working_path: Path) -> None:
    """
    Run `md2po` with provided input and output directories, with `--pot` flag to
    generate PO template (POT) files.

    When invoking `md2po`:

    * `--duplicates=merge` enforces multiple copies of the same string being
      shown once with multiple locations.
    * `--timestamp` ensures that new files are only generated when there is new
      content.

    :param root_path: The root directory of the documentation content.
    :param docs: The directory fragment, relative to the root path, containing
        the `en` Markdown content and `locales` translation files directories.
    :param working_path: The directory considered `/` for the input file call.
        This ensures that the location strings are accurate in the POT and PO
        files.
    """
    # Ensure the output directory exists
    output_path = root_path / docs / "locales/template"
    output_path.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "md2po",
            f"--input={Path(docs) / 'en'}",
            f"--output={output_path / 'translations.pot'}",
            "--pot",
            "--timestamp",
            "--duplicates=merge",
            "--multifile=onefile",
        ],
        check=True,
        cwd=working_path,
    )


def generate_pot_files(root_path: Path, docs: str) -> None:
    """
    Generate the PO template (POT) files for the content in the provided
    directory.

    :param root_path: The root directory of the documentation content.
    :param docs: The directory fragment, relative to the root path, containing
        the `en` Markdown content and `locales` translation files directories.
        This will become the msg* string location prefix in the generated POT
        files.
    """
    with TemporaryDirectory() as temp_working_directory:
        temp_working_path = Path(temp_working_directory)

        (temp_working_path / docs).parent.mkdir(parents=True, exist_ok=True)

        try:
            (temp_working_path / docs).symlink_to(
                root_path / docs,
                target_is_directory=True,
            )
        except FileExistsError:
            pass

        markdown_to_pot(
            root_path=root_path,
            docs=docs,
            working_path=temp_working_path,
        )


def main():
    # Generate primary content POT files.
    generate_pot_files(Path.cwd(), "docs")
    # Generate shared content POT files.
    generate_pot_files(Path(__file__).parent, "shared_content")


if __name__ == "__main__":
    main()
