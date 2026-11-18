import shutil
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from .api_directives import restore_api_blocks
from .build_config import (
    SHARED_CONTENT_PATH,
    clean_build_files,
    load_config,
    work_path,
    write_build_config,
)

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
    # Retained for compatibility. The API documentation source paths in the
    # mkdocstrings configuration are resolved relative to the project root, so
    # there's no longer any need to identify them separately.
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
            # Don't wrap the output content (it can break translated links)
            "--maxlinelength=0",
        ],
        check=True,
    )


def build_command(config_file: Path, build_with_warnings: bool) -> list[str]:
    """
    The command used to build the documentation for a given language.

    The site is built into the ``site_dir`` defined by the configuration file.

    :param config_file: The path to the language-specific configuration file.
    :param build_with_warnings: If False, the build fails on any warning.
    """
    command = [
        sys.executable,
        "-m",
        "zensical",
        "build",
        "--clean",
        "--config-file",
        str(config_file),
    ]

    if not build_with_warnings:
        command.append("--strict")

    return command


def copy_resources(en_md_path: Path, md_path: Path) -> list[Path]:
    """Make the non-Markdown files of the English content available to a translation.

    If the documentation includes images or other resources, they must be
    available in the translated content directory for the relative links in the
    translated Markdown to function the same way they do in the original
    Markdown files. This copies every file in the English content that isn't
    Markdown (including hidden files, such as ``.authors.yml``) into the
    translated content directory, unless the translation already contains it.

    The files are copied, rather than symlinked, because Zensical doesn't
    follow symlinked directories when it copies files into the built site.

    :param en_md_path: The directory containing the English content.
    :param md_path: The directory containing the translated content.
    :returns: The paths (relative to the content directory) that were copied.
    """
    copied = []
    for path in sorted(en_md_path.rglob("*")):
        if not path.is_file() or path.suffix == ".md" or path.name == ".DS_Store":
            continue
        relative_path = path.relative_to(en_md_path)
        target = md_path / relative_path
        if target.exists() or target.is_symlink():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied.append(relative_path)
    return copied


def publish_site(site_path: Path, output_path: Path, keep: list[str]) -> None:
    """Copy a built site into its final output location.

    Any existing content in the output location is removed first, apart from
    any directories named in ``keep``.

    :param site_path: The directory containing the built site.
    :param output_path: The final output location.
    :param keep: Names of directories in the output location to preserve (the
        output location for the English site contains the other languages).
    """
    if output_path.is_dir():
        for child in output_path.iterdir():
            if child.name in keep and child.is_dir():
                continue
            if child.is_dir() and not child.is_symlink():
                shutil.rmtree(child)
            else:
                child.unlink()
    shutil.copytree(site_path, output_path, dirs_exist_ok=True)


def prune_site(output_path: Path, language: str, languages: list[str]) -> None:
    """Remove build artefacts that aren't needed in the final site."""
    # If a SUMMARY folder has been created, it is unnecessary; prune it.
    summary = output_path / "SUMMARY"
    if summary.is_dir():
        print(f"Prune {summary}", flush=True)
        shutil.rmtree(summary)

    # If a non-English language contains a language folder (in any capitalization),
    # it is an artefact of redirects; prune it.
    if language != "en":
        for lang in languages:
            # Also try zh-cn variant of zh_CN (et al)
            for name in {lang, lang.replace("_", "-").lower()}:
                lang_dir = output_path / name
                if lang_dir.is_dir():
                    print(f"Prune {lang_dir}", flush=True)
                    shutil.rmtree(lang_dir)


def main():
    args = parse_args()

    output = Path(args.output).resolve()
    work = work_path(PROJECT_PATH)
    en_md_path = PROJECT_PATH / "docs/en"

    # Any language that has been (or could be) built into a subdirectory of the
    # output directory.
    all_languages = sorted(
        {
            *args.language_code,
            *(
                path.name
                for path in (PROJECT_PATH / "docs/locales").glob("*")
                if path.is_dir()
            ),
        }
    )

    try:
        # Make sure there is nothing left over from a previous build.
        clean_build_files(PROJECT_PATH, args.language_code)

        for language in args.language_code:
            print(f"Processing {language}", flush=True)

            if language != "en":
                # Generate translated content in the working directory
                md_path = work / "md" / language
                shared_content_path = work / "shared_content" / language
                md_path.mkdir(parents=True)
                shared_content_path.mkdir(parents=True)

                # Generate translated primary content
                generate_translated_md(
                    docs_path=PROJECT_PATH / "docs",
                    language=language,
                    output_path=md_path,
                )

                # Generate translated shared content
                generate_translated_md(
                    docs_path=SHARED_CONTENT_PATH,
                    language=language,
                    output_path=shared_content_path,
                )

                # po2md breaks mkdocstrings API directives that have options;
                # put the English originals back.
                restore_api_blocks(en_md_path, md_path)
                restore_api_blocks(SHARED_CONTENT_PATH / "en", shared_content_path)

                copy_resources(en_md_path, md_path)

                # Final output path is language-specific
                output_path = output / language
            else:
                md_path = en_md_path
                shared_content_path = SHARED_CONTENT_PATH / "en"

                # EN content is always output into the root build path
                output_path = output

            site_path = work / "site" / language
            config = load_config(PROJECT_PATH, language)
            config_file = write_build_config(
                PROJECT_PATH,
                config,
                language,
                md_path=md_path,
                shared_content_path=shared_content_path,
                site_path=site_path,
            )

            # Build documentation in provided language.
            subprocess.run(
                build_command(config_file, args.build_with_warnings), check=True
            )

            publish_site(
                site_path,
                output_path,
                keep=(
                    [
                        name
                        for lang in all_languages
                        for name in {lang, lang.replace("_", "-").lower()}
                    ]
                    if language == "en"
                    else []
                ),
            )
            prune_site(output_path, language, args.language_code)
    finally:
        clean_build_files(PROJECT_PATH, args.language_code)


if __name__ == "__main__":
    main()
