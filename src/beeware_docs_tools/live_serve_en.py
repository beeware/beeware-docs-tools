import subprocess
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from .build_config import (
    BASE_CONFIG,
    SHARED_CONTENT_PATH,
    clean_build_files,
    language_config_name,
    load_config,
    work_path,
    write_build_config,
)

# This script generates the build configuration for the English documentation,
# and serves a live build of it. The English content is served directly from
# `docs/en`, so edits are picked up as they are made.

PROJECT_PATH = Path.cwd()
# The live server has its own working directory, so a build can run at the same
# time.
RUN = "live"


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "watch_directories",
        nargs="*",
        help="Additional directories (relative to the project root) to watch for changes.",
    )
    parser.add_argument("--strict", action="store_true")
    # Retained for compatibility. The API documentation source paths in the
    # mkdocstrings configuration are resolved relative to the project root, so
    # there's no longer any need to identify them separately.
    parser.add_argument("--source-code", action="append")
    parser.add_argument("--port", type=int, default=8037)
    parser.add_argument(
        "--no-open",
        dest="open_browser",
        action="store_false",
        help="Don't open the live build in a web browser.",
    )
    args = parser.parse_args()

    return args


def watch_paths(project_path: Path, watch_directories: list[str]) -> list[Path]:
    """The paths to watch for changes, in addition to the English content.

    :param project_path: The root of the project being documented.
    :param watch_directories: Additional directories, relative to the project
        root, to watch for changes.
    """
    paths = [
        project_path / "docs" / BASE_CONFIG,
        project_path / "docs" / language_config_name("en"),
        SHARED_CONTENT_PATH / "en",
    ]
    paths.extend(project_path / directory for directory in watch_directories)
    return [path for path in paths if path.exists()]


def serve_command(
    config_file: Path,
    port: int,
    strict: bool,
    open_browser: bool,
) -> list[str]:
    """The command used to serve the live build.

    :param config_file: The path to the build configuration file.
    :param port: The port to serve on.
    :param strict: If True, request strict mode.
    :param open_browser: If True, open the live build in a web browser.
    """
    command = [
        sys.executable,
        "-m",
        "zensical",
        "serve",
        "--config-file",
        str(config_file),
        "--dev-addr",
        f"localhost:{port}",
    ]

    if open_browser:
        command.append("--open")

    if strict:
        command.append("--strict")

    return command


def main():
    args = parse_args()

    config = load_config(PROJECT_PATH, "en")

    try:
        clean_build_files(PROJECT_PATH, ["en"], run=RUN)
        config_file = write_build_config(
            PROJECT_PATH,
            config,
            "en",
            md_path=PROJECT_PATH / "docs/en",
            shared_content_path=SHARED_CONTENT_PATH / "en",
            site_path=work_path(PROJECT_PATH, RUN) / "site" / "en",
            run=RUN,
            watch=watch_paths(PROJECT_PATH, args.watch_directories),
        )

        subprocess.run(
            serve_command(config_file, args.port, args.strict, args.open_browser),
            check=True,
        )
    except KeyboardInterrupt:
        pass
    finally:
        clean_build_files(PROJECT_PATH, ["en"], run=RUN)


if __name__ == "__main__":
    main()
