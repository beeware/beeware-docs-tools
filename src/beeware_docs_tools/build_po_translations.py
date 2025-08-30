import shutil
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

import subprocess

SOURCE_DIR = Path.cwd()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("language_code", nargs="*")
    args = parser.parse_args()

    for language_code in args.language_code:
        if not (SOURCE_DIR / "docs" / "locales" / f"{language_code}").is_dir():
            raise RuntimeError(
                f'Language code "{language_code}" does not match an existing translation'
            )

    return args


def merge_translation_files(
    source_dir: Path, template_dir: Path, destination_dir: Path
) -> None:
    destination_dir.mkdir(parents=True)
    subprocess.run(
        [
            "pot2po",
            f"--template={source_dir}",
            f"--input={template_dir}",
            f"--output={destination_dir}",
        ],
        check=True,
    )


def main():
    args = parse_args()

    with TemporaryDirectory() as final_dir:
        final_dir = Path(final_dir)

        for language in args.language_code:
            print(f"Processing primary {language} content")
            merge_translation_files(
                source_dir=SOURCE_DIR / "docs" / "locales" / language / "LC_MESSAGES",
                template_dir=SOURCE_DIR / "docs" / "locales" / "templates",
                destination_dir=final_dir / language / "LC_MESSAGES",
            )

            shutil.copytree(
                final_dir / language,
                SOURCE_DIR / "docs" / "locales" / language,
                dirs_exist_ok=True,
            )

            print(f"Processing shared {language} content")
            merge_translation_files(
                source_dir=Path(__file__).parent
                / "shared_content"
                / "locales"
                / language
                / "LC_MESSAGES",
                template_dir=Path(__file__).parent
                / "shared_content"
                / "locales"
                / "templates",
                destination_dir=final_dir / "shared_content" / language / "LC_MESSAGES",
            )

            shutil.copytree(
                final_dir / "shared_content",
                Path(__file__).parent / "shared_content" / "locales",
                dirs_exist_ok=True,
            )


if __name__ == "__main__":
    main()
