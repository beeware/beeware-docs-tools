import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

from .md_tempdir import symlink_from_temp, load_config, save_config

# This tool is used to generate translated Markdown, if a language other than
# English is provided, and build the documentation site for the provided
# language.
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

PROJECT_PATH = Path.cwd()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("language_code", nargs="*")
    parser.add_argument("--output", type=Path, default=PROJECT_PATH / "_build" / "html")
    parser.add_argument("--build-with-warnings", action="store_true")
    parser.add_argument("--source-code", type=Path, action="append")
    args = parser.parse_args()

    for language in args.language_code:
        if not (
            (PROJECT_PATH / f"docs/locales/{language}").is_dir() or language == "en"
        ):
            raise RuntimeError(
                f'Language code "{language}" does not match an existing translation'
            )

    return args


def generate_translated_md(
    docs_path: Path,
    language: str,
    output_path: Path,
) -> None:
    """
    Generate Markdown in a specific language from translated PO files.

    :param docs_path: The directory fragment, relative to the project root,
        containing the `locales` directory.
    :param language: The language code to convert.
    :param output_path: The directory for the translated Markdown content.
    """
    subprocess.run(
        [
            "po2md",
            f"--input={docs_path / f'locales/{language}/translations.po'}",
            f"--template={docs_path / 'en'}",
            f"--output={output_path}",
            "--fuzzy",
        ],
        check=True,
    )


def build_docs(config_file: Path, output_path: Path, build_with_warnings: bool) -> None:
    """
    Run `mkdocs build` for a given language.

    :param config_file: The path to the language-specific configuration file.
    :param output_path: The output directory for the site content.
    """
    build_command = [
        "python",
        "-m",
        "mkdocs",
        "build",
        "--clean",
        "--config-file",
        str(config_file),
        "--site-dir",
        str(output_path),
    ]

    if not build_with_warnings:
        build_command.append("--strict")

    subprocess.run(build_command, check=True)


def main():
    args = parse_args()

    with TemporaryDirectory() as temp_md_directory:
        temp_md_path = Path(temp_md_directory)

        config_file = load_config(PROJECT_PATH)
        symlink_from_temp(PROJECT_PATH, temp_md_path, args.source_code, config_file)

        for language in args.language_code:
            print(f"Processing {language}")

            save_config(PROJECT_PATH, temp_md_path, config_file, language)

            if language != "en":
                # Create temp output directories for primary and shared content.
                output_path = temp_md_path / language
                sc_output_path = temp_md_path / f"shared_content/{language}"
                output_path.mkdir(parents=True, exist_ok=True)
                sc_output_path.mkdir(parents=True, exist_ok=True)

                # Generate translated primary content
                generate_translated_md(
                    docs_path=PROJECT_PATH / "docs",
                    language=language,
                    output_path=output_path,
                )

                # Generate translated shared content
                generate_translated_md(
                    docs_path=Path(__file__).parent / "shared_content",
                    language=language,
                    output_path=sc_output_path,
                )

                # If the documentation includes images or resources, they must be
                # explicitly symlinked to the temporary language output directory
                # for the relative links in the translated Markdown to function the
                # same way they do in the original Markdown files. This finds all
                # images and resources subdirectories, and symlinks them.
                for name in ["images", "resources"]:
                    en_md_dir = PROJECT_PATH / "docs/en"
                    for path in en_md_dir.glob(f"**/{name}"):
                        if path.is_dir():
                            relative_path = path.relative_to(en_md_dir)
                            (temp_md_path / language / relative_path).symlink_to(path)
            else:
                # Symlink to en directory
                (temp_md_path / "en").symlink_to(
                    PROJECT_PATH / "docs/en",
                    target_is_directory=True,
                )

            # Build documentation in provided language.
            output = Path(args.output).resolve()
            build_docs(
                config_file=temp_md_path / f"mkdocs.{language}.yml",
                output_path=(
                    output if (len(args.language_code) == 1) else (output / language)
                ),
                build_with_warnings=args.build_with_warnings,
            )


if __name__ == "__main__":
    main()
