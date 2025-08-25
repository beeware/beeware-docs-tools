import subprocess
from argparse import ArgumentParser, Namespace
from importlib.metadata import metadata
from pathlib import Path
import yaml
from tempfile import TemporaryDirectory


SOURCE_DIR = Path.cwd()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("language_code", nargs="*")
    parser.add_argument("--output", default=SOURCE_DIR / "_build" / "html")
    parser.add_argument("--build-with-errors", action="store_true")
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

    if not args.build_with_errors:
        serve_command.extend(["--strict"])

    subprocess.run(
        serve_command,
        check=True,
    )


def main():
    args = parse_args()

    with TemporaryDirectory() as temp_md_directory:
        temp_md_directory = Path(temp_md_directory)

        # Load the config.yml file, add the version number to extra,
        # and dump the updated copy to the temp directory so it is
        # available relative to the build.
        config_file = yaml.load(
            open(SOURCE_DIR / "docs" / "config.yml"), Loader=yaml.SafeLoader
        )
        try:
            version = metadata(config_file["extra"]["package_name"])["version"]
            config_file["extra"]["version"] = version
        except KeyError:
            pass

        with (temp_md_directory / "config.yml").open(
            "w", encoding="utf-8"
        ) as config_temp:
            yaml.dump(config_file, config_temp)

        # If source code directory or directories provided, symlink.
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
            output_directory = temp_md_directory / language

            # Symlink language config to temp directory. docs_dir and INHERIT paths are
            # relative, so to build translations successfully while allowing English
            # to build on its own, files must be available relative to the build.
            (temp_md_directory / f"mkdocs.{language}.yml").symlink_to(
                SOURCE_DIR / "docs" / f"mkdocs.{language}.yml"
            )
            if language != "en":
                output_directory.mkdir(parents=True, exist_ok=True)
                generate_translated_md(
                    input_dir=SOURCE_DIR
                    / "docs"
                    / "locales"
                    / language
                    / "LC_MESSAGES",
                    template_dir=SOURCE_DIR / "docs" / "en",
                    output_dir=temp_md_directory / language,
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
                # Symlink English Markdown files for en build.
                (temp_md_directory / "en").symlink_to(
                    SOURCE_DIR / "docs" / "en", target_is_directory=True
                )

            output = Path(args.output).resolve()
            build_docs(
                config_file=(temp_md_directory / f"mkdocs.{language}.yml"),
                build_dir=output
                if (len(args.language_code) == 1)
                else (output / language),
            )


if __name__ == "__main__":
    main()
