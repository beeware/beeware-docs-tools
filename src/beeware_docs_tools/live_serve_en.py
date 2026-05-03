import http.client
import subprocess
import threading
import time
import webbrowser
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

from .md_tempdir import load_config, save_config, symlink_from_temp

# The theme overrides directory in config.yml is relative to the docs directory.
# Therefore, the live build expects there to be an overrides directory in the
# local docs directory. This script symlinks all the necessary directories and
# config files to a temp directory and serves the live build from the temp
# directory.

PROJECT_PATH = Path.cwd()


def launch_browser(port: int, timeout: int = 30) -> None:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            conn = http.client.HTTPConnection("localhost", port, timeout=1)
            try:
                conn.request("HEAD", "/")
                response = conn.getresponse()
                # Mkdocs might return various 2xx or 3xx status codes when ready
                if response.status < 400:
                    break
            finally:
                conn.close()
        except (OSError, http.client.HTTPException):
            time.sleep(0.1)
    else:
        print(
            f"\nWarning: Live server did not come up on port {port} within {timeout} seconds. "
            "Browser will not be launched automatically."
        )
        return

    webbrowser.open(f"http://localhost:{port}/")


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("watch_directories", nargs="*")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--source-code", action="append")
    parser.add_argument("--port", type=int, default=8037)
    args = parser.parse_args()

    return args


def serve_docs(
    output_path: Path,
    strict: bool,
    watch_directories: list[str],
    port: int,
) -> None:
    serve_command = [
        "python",
        "-m",
        "mkdocs",
        "serve",
        "--clean",
        "--livereload",
        "--config-file",
        str(output_path / "mkdocs.en.yml"),
        "--watch",
        "docs",
        "--dev-addr",
        f"localhost:{port}",
    ]

    if strict:
        serve_command.append("--strict")

    for directory in watch_directories:
        serve_command.extend(["--watch", directory])

    threading.Thread(target=launch_browser, args=(port,), daemon=True).start()

    subprocess.run(
        serve_command,
        check=True,
    )


def main():
    args = parse_args()

    with TemporaryDirectory() as temp_md_directory:
        temp_md_path = Path(temp_md_directory)

        config = load_config(PROJECT_PATH)
        symlink_from_temp(PROJECT_PATH, temp_md_path, args.source_code, config)
        save_config(PROJECT_PATH, temp_md_path, config)

        (temp_md_path / "en").symlink_to(
            PROJECT_PATH / "docs/en",
            target_is_directory=True,
        )

        serve_docs(temp_md_path, args.strict, args.watch_directories, args.port)


if __name__ == "__main__":
    main()
