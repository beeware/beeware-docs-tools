from pathlib import Path
from importlib.metadata import metadata

import polib
import yaml


def load_config(project_path):
    """Load the config.yml file, and add the version_number to extra."""

    with (project_path / "docs/config.yml").open() as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    try:
        version = metadata(config["extra"]["package_name"])["version"]
        config["extra"]["version"] = version
    except KeyError:
        pass

    return config


def translate(po):
    """Generate a translator function using the provided PO file."""

    def _translate(entry):
        po_entry = po.find(entry)
        if po_entry:
            translated = po_entry.msgstr
            if translated:
                return translated
        return entry

    return _translate


def process_nav(entry, fn):
    """Recursively walk a nav definition, calling a function on human-readable strings.

    :param entry: A node in a navigation tree
    :param fn: A function that takes a single human-readable string, and returns
        a "processed" string.
    """
    if isinstance(entry, dict):
        # Recursively translate all keys, and all list values. otherwise return
        # values as is (as they will be a file reference)
        return {
            process_nav(child, fn): process_nav(value, fn)
            if isinstance(value, list)
            else value
            for child, value in entry.items()
        }
    elif isinstance(entry, list):
        # Recursively translate any dictionary in a list;
        # otherwise return as-is (as it will be a file reference)
        return [
            process_nav(child, fn) if isinstance(child, dict) else child
            for child in entry
        ]
    else:
        # The entry must be a string. Process it.
        return fn(entry)


def save_config(project_path, temp_md_path, config, language="en"):
    """Add the base_path to Snippets, and dump the updated copy to the temp directory"""
    # Necessary so that it's available relative to the build.

    base_path = config["markdown_extensions"]["pymdownx.snippets"].get("base_path", [])

    if language != "en":
        shared_content_path = temp_md_path.resolve() / f"shared_content/{language}"
    else:
        shared_content_path = (Path(__file__).parent / "shared_content/en").resolve()

    base_path.append(str(shared_content_path))
    config["markdown_extensions"]["pymdownx.snippets"]["base_path"] = base_path
    config["plugins"]["macros"]["include_dir"] = str(shared_content_path)

    with (temp_md_path / "config.yml").open("w", encoding="utf-8") as config_f:
        yaml.dump(config, config_f)

    # Build the language configuration into the temp directory. docs_dir and
    # INHERIT paths are relative, so to build translations successfully while
    # allowing English to build on its own, files must be available relative to
    # the build. For the main website, we also need to generate a translated
    # `nav` configuration.
    if language != "en" and "nav" in config:
        mkdocs_config = yaml.load(
            (project_path / f"docs/mkdocs.{language}.yml").read_text(),
            Loader=yaml.SafeLoader,
        )

        po = polib.pofile(project_path / f"docs/locales/{language}/translations.po")
        mkdocs_config["nav"] = process_nav(
            config["nav"],
            translate(po),
        )

        with (temp_md_path / f"mkdocs.{language}.yml").open(
            "w", encoding="utf-8"
        ) as mkdocs_f:
            yaml.dump(mkdocs_config, mkdocs_f)

    else:
        # On non-website builds, and for the English build of the website, we
        # can symlink the original language configuraton.
        (temp_md_path / f"mkdocs.{language}.yml").symlink_to(
            project_path / f"docs/mkdocs.{language}.yml"
        )


def symlink_from_temp(project_path, temp_md_path, source_code, config):
    """Symlink the relevant files so that they're available in the temp dir."""
    # If source code directory or directories provided, symlink from the temp directory,
    # so it is available relative to the build.
    if source_code:
        for source in source_code:
            # If source includes subdirectories, the parent directory must be created.
            # If a single directory is provided, this will rely on `exists_ok=True` to
            # avoid failing.
            (temp_md_path / source).parent.mkdir(parents=True, exist_ok=True)
            (temp_md_path / source).symlink_to(
                project_path / source, target_is_directory=True
            )

    # Symlink the overrides directory from the temp directory, so it is available
    # relative to the build.
    (temp_md_path / "overrides").symlink_to(
        Path(__file__).parent / "overrides", target_is_directory=True
    )

    # Symlink to the macros module, if there is one.
    try:
        module_name = config["plugins"]["macros"]["module_name"]
    except KeyError:
        module_name = "main"

    macros_path = project_path / f"docs/{module_name}.py"
    symlink_path = temp_md_path / f"{module_name}.py"
    if macros_path.is_file():
        symlink_path.parent.mkdir(parents=True, exist_ok=True)
        symlink_path.symlink_to(macros_path)
