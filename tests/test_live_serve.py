import sys
from pathlib import Path

from beeware_docs_tools.live_serve_en import serve_command, watch_paths


def test_serve_command():
    """The live server is started with Zensical, on the requested port."""
    command = serve_command(
        Path("/project/docs/_build.en.toml"), 8037, strict=False, open_browser=True
    )
    assert command == [
        sys.executable,
        "-m",
        "zensical",
        "serve",
        "--config-file",
        "/project/docs/_build.en.toml",
        "--dev-addr",
        "localhost:8037",
        "--open",
    ]


def test_serve_command_no_open_strict():
    """The browser can be suppressed, and strict mode requested."""
    command = serve_command(
        Path("/project/docs/_build.en.toml"), 9000, strict=True, open_browser=False
    )
    assert "--open" not in command
    assert command[-1] == "--strict"
    assert "localhost:9000" in command


def test_watch_paths(tmp_path):
    """Configuration files and requested directories are watched, if they exist."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/zensical.toml").write_text("[project]\n", encoding="utf-8")
    (tmp_path / "docs/zensical.en.toml").write_text("[project]\n", encoding="utf-8")
    (tmp_path / "src").mkdir()

    paths = watch_paths(tmp_path, ["src", "missing"])

    assert tmp_path / "docs/zensical.toml" in paths
    assert tmp_path / "docs/zensical.en.toml" in paths
    assert tmp_path / "src" in paths
    assert tmp_path / "missing" not in paths
