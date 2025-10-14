import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory


from .temp_md import symlink_from_temp, load_config, save_config

# The theme overrides directory in config.yml is relative to the docs directory.
# Therefore, the live build expects there to be an overrides directory in the
# local docs directory. This script symlinks all the necessary directories and
# config files to a temp directory and serves the live build from the temp
# directory.

PROJECT_PATH = Path.cwd()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("watch_directory", nargs="*")
    parser.add_argument("--build-with-warnings", action="store_true")
    parser.add_argument("--source-code", action="append")
    args = parser.parse_args()

    return args


def serve_docs(output_path, build_with_warnings: bool, watch_directory: str) -> None:
    serve_command = [
        "python",
        "-m",
        "mkdocs",
        "serve",
        "--clean",
        "--config-file",
        str(output_path / "mkdocs.en.yml"),
        "--watch",
        "docs",
    ]

    if not build_with_warnings:
        serve_command.append("--strict")

    for directory in watch_directory:
        serve_command.extend(["--watch", directory])

    subprocess.run(
        serve_command,
        check=True,
    )


def main():
    args = parse_args()

    with TemporaryDirectory() as temp_md_directory:
        temp_md_path = Path(temp_md_directory)

        config_file = load_config(PROJECT_PATH)
        symlink_from_temp(PROJECT_PATH, temp_md_path, args.source_code, config_file)
        save_config(PROJECT_PATH, temp_md_path, config_file)

        (temp_md_path / "en").symlink_to(
            PROJECT_PATH / "docs/en",
            target_is_directory=True,
        )
        print("Symlink created")

        serve_docs(temp_md_path, args.build_with_warnings, args.watch_directory)


if __name__ == "__main__":
    main()
