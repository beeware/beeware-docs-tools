import subprocess
from argparse import ArgumentParser, Namespace
from importlib.metadata import metadata
from pathlib import Path
import yaml
from tempfile import TemporaryDirectory

# This tool is used to generate translated Markdown, if a language other than English is provided,
# and build the documentation site for the provided language.

# The Markdown content can optionally contain external shared content included using the PyMdown
# Snippets extension. To facilitate translation of the shared content, it is included as part of
# BeeWare Docs Tools, along with the associated `locales` directory containing the shared content
# POT and translated PO files. This content is then processed separately from the primary content,
# and the resulting files are stored within the `docs-tools` repo `src` directory. When BeeWare
# Docs Tools is installed into a documentation repo, it includes the shared Markdown and PO files.
# They are then made available to the other translation- and build-tools, so when they are run,
# they are able to access the translated shared content and build each translated site in a given
# language.

SOURCE_DIR = Path.cwd()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("language_code", nargs="*")
    parser.add_argument("--output", default=SOURCE_DIR / "_build" / "html")
    parser.add_argument("--build-with-warnings", action="store_true")
    parser.add_argument("--source-code", action="append")
    args = parser.parse_args()
    for language_code in args.language_code:
        if not (
            (SOURCE_DIR / "docs" / "locales" / f"{language_code}").is_dir()
            or language_code == "en"
        ):
            raise RuntimeError(
                f'Language code "{language_code}" does not match an existing translation'
            )

    return args


def generate_translated_md(
    input_dir: Path, template_dir: Path, output_dir: Path
) -> None:
    """
    Generate Markdown in a specific language from translated PO files.

    :param input_dir: The directory containing the translated PO files.
    :param template_dir: The directory containing the original (English) Markdown content.
    :param output_dir: The directory for the translated Markdown content.
    :return:
    """
    subprocess.run(
        [
            "po2md",
            f"--input={input_dir}",
            f"--template={template_dir}",
            f"--output={output_dir}",
            "--fuzzy",
        ],
        check=True,
    )


def build_docs(config_file: Path, build_dir: Path) -> None:
    """
    Run `mkdocs build` for a given language.
    :param config_file: The path to the language-specific configuration file.
    :param build_dir: The output directory for the site content.
    :return:
    """
    args = parse_args()

    serve_command = [
        "python",
        "-m",
        "mkdocs",
        "build",
        "--clean",
        "--config-file",
        f"{config_file}",
        "--site-dir",
        f"{build_dir}",
    ]

    if not args.build_with_warnings:
        serve_command.extend(["--strict"])

    subprocess.run(
        serve_command,
        check=True,
    )


def main():
    args = parse_args()

    # If the script fails in the middle, it can leave this symlink in place
    # which leads to it failing when the script runs again. This check is
    # meant to deal with that possibility.
    if (SOURCE_DIR / "docs" / "en" / "shared_content").exists():
        Path(SOURCE_DIR / "docs" / "en" / "shared_content").unlink(missing_ok=True)

    with TemporaryDirectory() as temp_md_directory:
        temp_md_directory = Path(temp_md_directory)

        # If source code directory or directories provided, symlink to the
        # temp directory so it is available relative to the build.
        if args.source_code:
            for directory in args.source_code:
                if "/" in directory:
                    Path(temp_md_directory / directory).parent.mkdir(
                        parents=True, exist_ok=True
                    )
                (temp_md_directory / directory).symlink_to(
                    SOURCE_DIR / directory, target_is_directory=True
                )

        # Symlink overrides directory to the temp directory, so it is
        # available relative to the build.
        (temp_md_directory / "overrides").symlink_to(
            Path(__file__).parent / "overrides", target_is_directory=True
        )

        for language in args.language_code:
            print(f"Processing {language}")

            # Load the config.yml file, add the version_number to extra,
            # add the base_path to Snippets, and dump the updated copy to
            # the temp directory so it is available relative to the build.
            config_file = yaml.load(
                open(SOURCE_DIR / "docs" / "config.yml"), Loader=yaml.SafeLoader
            )

            try:
                version = metadata(config_file["extra"]["package_name"])["version"]
                config_file["extra"]["version"] = version
            except KeyError:
                pass

            shared_content_path = (
                temp_md_directory / language / "shared_content"
            ).resolve()
            config_file["markdown_extensions"]["pymdownx.snippets"]["base_path"] = [
                "docs",
                f"{shared_content_path}",
            ]

            with (temp_md_directory / "config.yml").open(
                "w", encoding="utf-8"
            ) as config_temp:
                yaml.dump(config_file, config_temp)

            # Symlink language config to temp directory. docs_dir and INHERIT paths are
            # relative, so to build translations successfully while allowing English
            # to build on its own, files must be available relative to the build.
            (temp_md_directory / f"mkdocs.{language}.yml").symlink_to(
                SOURCE_DIR / "docs" / f"mkdocs.{language}.yml"
            )

            if language != "en":
                # Create temp output directories for primary and shared content.
                output_directory = temp_md_directory / language
                sc_output_directory = output_directory / "shared_content"
                output_directory.mkdir(parents=True, exist_ok=True)
                sc_output_directory.mkdir(parents=True, exist_ok=True)

                # Symlink shared content directory to the temp directory, so it is
                # available relative to the build.
                (temp_md_directory / f"shared_content_{language}").symlink_to(
                    Path(__file__).parent / "shared_content" / "en",
                    target_is_directory=True,
                )

                # Generate translated primary content
                generate_translated_md(
                    input_dir=SOURCE_DIR
                    / "docs"
                    / "locales"
                    / language
                    / "translations.po",
                    template_dir=SOURCE_DIR / "docs" / "en",
                    output_dir=output_directory,
                )

                # Generate translated shared content
                generate_translated_md(
                    input_dir=Path(__file__).parent
                    / "shared_content"
                    / "locales"
                    / language
                    / "translations.po",
                    template_dir=temp_md_directory / f"shared_content_{language}",
                    output_dir=sc_output_directory,
                )

                # If the documentation includes images or resources, they must be
                # explicitly symlinked to the temporary language output directory
                # for the relative links in the translated Markdown to function the
                # same way they do in the original Markdown files. This finds all
                # images and resources subdirectories, and symlinks them.
                for name in ["images", "resources"]:
                    en_md_dir = SOURCE_DIR / "docs" / "en"
                    for path in en_md_dir.glob(f"**/{name}"):
                        if path.is_dir():
                            relative_path = path.relative_to(en_md_dir)
                            (temp_md_directory / language / relative_path).symlink_to(
                                path
                            )
            else:
                # Symlink primary English Markdown files for en build.
                (temp_md_directory / "en").symlink_to(
                    SOURCE_DIR / "docs" / "en", target_is_directory=True
                )
                # Symlink shared content English Markdown files for en build.
                (temp_md_directory / "en" / "shared_content").symlink_to(
                    Path(__file__).parent / "shared_content" / "en",
                    target_is_directory=True,
                )

            # Build documentation in provided language.
            output = Path(args.output).resolve()
            build_docs(
                config_file=(temp_md_directory / f"mkdocs.{language}.yml"),
                build_dir=output
                if (len(args.language_code) == 1)
                else (output / language),
            )

            if language == "en":
                Path(temp_md_directory / "en" / "shared_content").unlink(
                    missing_ok=True
                )


if __name__ == "__main__":
    main()
