import subprocess
from argparse import ArgumentParser, Namespace
from importlib.metadata import metadata
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

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


def build_docs(config_file: Path, output_path: Path) -> None:
    """
    Run `mkdocs build` for a given language.

    :param config_file: The path to the language-specific configuration file.
    :param output_path: The output directory for the site content.
    """
    args = parse_args()

    build_command = [
        "python",
        "-m",
        "mkdocs",
        "build",
        "--clean",
        "--config-file",
        f"{config_file}",
        "--site-dir",
        f"{output_path}",
    ]

    if not args.build_with_warnings:
        build_command.extend(["--strict"])

    subprocess.run(build_command, check=True)


def main():
    args = parse_args()

    # If the script fails in the middle, it can leave this symlink in place
    # which leads to it failing when the script runs again. This check is
    # meant to deal with that possibility.
    if (PROJECT_PATH / "docs/en/shared_content").exists():
        Path(PROJECT_PATH / "docs/en/shared_content").unlink(missing_ok=True)

    with TemporaryDirectory() as temp_md_directory:
        temp_md_path = Path(temp_md_directory)

        # If source code directory or directories provided, symlink to the
        # temp directory, so it is available relative to the build.
        if args.source_code:
            for source in args.source_code:
                # If source includes subdirectories, the parent directory
                # must be created. If a single directory is provided, this
                # will rely on `exists_ok=True` to avoid failing.
                (temp_md_path / source).parent.mkdir(parents=True, exist_ok=True)
                (temp_md_path / source).symlink_to(
                    PROJECT_PATH / source, target_is_directory=True
                )

        # Symlink overrides directory to the temp directory, so it is
        # available relative to the build.
        (temp_md_path / "overrides").symlink_to(
            Path(__file__).parent / "overrides", target_is_directory=True
        )

        for language in args.language_code:
            print(f"Processing {language}")

            # Load the config.yml file, add the version_number to extra,
            # add the base_path to Snippets, and dump the updated copy to
            # the temp directory, so it is available relative to the build.
            with (PROJECT_PATH / "docs/config.yml").open() as f:
                config_file = yaml.load(f, Loader=yaml.SafeLoader)

            try:
                version = metadata(config_file["extra"]["package_name"])["version"]
                config_file["extra"]["version"] = version
            except KeyError:
                pass

            shared_content_path = (
                temp_md_path / f"{language}/shared_content"
            ).resolve()
            config_file["markdown_extensions"]["pymdownx.snippets"]["base_path"] = [
                "docs",
                str(shared_content_path),
            ]

            with (temp_md_path / "config.yml").open(
                "w", encoding="utf-8"
            ) as config_temp:
                yaml.dump(config_file, config_temp)

            # Symlink language config to temp directory. docs_dir and INHERIT
            # paths are relative, so to build translations successfully while
            # allowing English to build on its own, files must be available
            # relative to the build.
            (temp_md_path / f"mkdocs.{language}.yml").symlink_to(
                PROJECT_PATH / f"docs/mkdocs.{language}.yml"
            )

            if language != "en":
                # Create temp output directories for primary and shared content.
                output_path = temp_md_path / language
                sc_output_path = output_path / "shared_content"
                output_path.mkdir(parents=True, exist_ok=True)
                sc_output_path.mkdir(parents=True, exist_ok=True)

                # Symlink shared content directory to the temp directory, so it is
                # available relative to the build.
                (temp_md_path / f"shared_content_{language}").symlink_to(
                    Path(__file__).parent / "shared_content" / "en",
                    target_is_directory=True,
                )

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
                # Symlink primary English Markdown files for en build.
                (temp_md_path / "en").symlink_to(
                    PROJECT_PATH / "docs/en", target_is_directory=True
                )
                # Symlink shared content English Markdown files for en build.
                (temp_md_path / "en/shared_content").symlink_to(
                    Path(__file__).parent / "shared_content/en",
                    target_is_directory=True,
                )

            # Build documentation in provided language.
            output = Path(args.output).resolve()
            build_docs(
                config_file=temp_md_path / f"mkdocs.{language}.yml",
                output_path=(
                    output if (len(args.language_code) == 1) else (output / language)
                ),
            )

            if language == "en":
                Path(temp_md_path / "en/shared_content").unlink(missing_ok=True)


if __name__ == "__main__":
    main()
