"""Convert a project's MkDocs configuration to Zensical's native TOML format.

This converts:

* ``docs/config.yml`` into ``docs/zensical.toml``;
* each ``docs/mkdocs.<lang>.yml`` into ``docs/zensical.<lang>.toml``; and
* the literate-nav navigation file (``docs/en/SUMMARY.md``) into a ``nav``
  setting in ``docs/zensical.toml``.

Comments in the YAML files are carried over to the TOML files.

Before anything is written, the converted configuration for every language is
checked against the configuration Zensical reads from the original YAML files.
The only differences allowed are the intended ones (see ``compare_configs()``).
If there are any others, nothing is written.

Navigation titles that were translated as part of ``SUMMARY.md`` are migrated
in each ``docs/locales/<lang>/translations.po``, so the translations carry over
to the titles in the new ``nav`` setting.
"""

import datetime
import json
import math
import re
import sys
import tempfile
import tomllib
from argparse import ArgumentParser
from pathlib import Path

import polib
import yaml

from .build_config import (
    BASE_CONFIG,
    language_config_name,
    merge_config,
    process_nav,
    read_toml,
    unexpected_language_keys,
)

# The file that `build_pot_translations` generates the navigation titles into,
# relative to the `docs` directory.
TITLES_FILE = "en/titles.md"


class ConversionError(Exception):
    pass


###########################################################################
# Reading YAML
###########################################################################


class PythonName(str):
    """A reference to a Python object (a ``!!python/name:`` tag)."""


class EnvTag:
    """An ``!ENV`` tag, which has no equivalent in TOML."""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"!ENV {self.value!r}"


def _extension_alias(name):
    from zensical.config import _extension_alias

    return _extension_alias(name)


class _Loader(yaml.SafeLoader):
    pass


def _construct_env(loader, node):
    if isinstance(node, yaml.ScalarNode):
        return EnvTag(loader.construct_scalar(node))
    return EnvTag(loader.construct_sequence(node))


_Loader.add_constructor("!ENV", _construct_env)
_Loader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:",
    lambda loader, suffix, node: PythonName(_extension_alias(suffix)),
)


def _walk_nodes(node, path, starts, ends):
    """Record the lines on which each node of a YAML document starts and ends."""

    def note_end(n):
        line = n.end_mark.line
        ends[line] = max(ends.get(line, 0), n.end_mark.column)

    if isinstance(node, yaml.MappingNode):
        for key_node, value_node in node.value:
            child = (*path, key_node.value)
            starts.setdefault(key_node.start_mark.line, []).append(child)
            note_end(key_node)
            _walk_nodes(value_node, child, starts, ends)
        if node.flow_style:
            note_end(node)
    elif isinstance(node, yaml.SequenceNode):
        for index, item in enumerate(node.value):
            child = (*path, index)
            starts.setdefault(item.start_mark.line, []).append(child)
            _walk_nodes(item, child, starts, ends)
        if node.flow_style:
            note_end(node)
    else:
        note_end(node)


def extract_comments(text):
    """Find the comments in a YAML document, and the setting each describes.

    A comment on its own line describes the setting that follows it. A comment
    at the end of a line describes the setting on that line.

    :param text: The YAML document.
    :returns: A tuple of a dictionary mapping a key path (a tuple of keys and
        list indices) to ``{"before": [lines], "trailing": text}``, and a list
        of comments that couldn't be attached to a setting.
    """
    root = yaml.compose(text, Loader=_Loader)
    comments = {}
    unplaced = []
    if root is None:
        return comments, unplaced

    starts = {}
    ends = {}
    _walk_nodes(root, (), starts, ends)

    pending = []
    for number, line in enumerate(text.splitlines()):
        stripped = line.strip()
        if stripped.startswith("#"):
            comment = stripped[1:].removeprefix(" ").rstrip()
            # Editor directives for YAML (such as the MkDocs schema) don't
            # apply to TOML.
            if not comment.startswith("yaml-language-server:"):
                pending.append(comment)
            continue
        if not stripped:
            continue
        if number in starts and pending:
            comments.setdefault(starts[number][0], {}).setdefault("before", []).extend(
                pending
            )
            pending = []
        if number in ends:
            match = re.match(r"^[\s:]*#\s?(.*)$", line[ends[number] :])
            if match:
                if number in starts:
                    comments.setdefault(starts[number][-1], {})["trailing"] = (
                        match.group(1).rstrip()
                    )
                else:
                    unplaced.append(match.group(1))
    unplaced.extend(pending)
    return comments, unplaced


def load_yaml(path):
    """Load a YAML configuration file, and its comments."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        data = yaml.load(text, Loader=_Loader) or {}
    except yaml.YAMLError as e:
        raise ConversionError(f"Unable to read {path}: {e}") from e
    comments, unplaced = extract_comments(text)
    return data, comments, unplaced


###########################################################################
# Converting values
###########################################################################


def _rename_comments(comments, old_prefix, new_prefix):
    """Move the comments under one key path to another key path."""
    for path in list(comments):
        if path[: len(old_prefix)] == old_prefix:
            comments[(*new_prefix, *path[len(old_prefix) :])] = comments.pop(path)


def normalize_named_items(value, path, comments):
    """Convert a `markdown_extensions` or `plugins` setting to a table.

    MkDocs allows these settings to be a list of names, or of single-key
    mappings; TOML needs a table. A missing configuration becomes an empty
    table.
    """
    if value is None:
        return {}
    if isinstance(value, dict):
        return {name: {} if conf is None else conf for name, conf in value.items()}
    if not isinstance(value, list):
        raise ConversionError(f"{'.'.join(path)} must be a list or a mapping")

    result = {}
    for index, item in enumerate(value):
        if isinstance(item, str):
            name, conf = item, {}
            _rename_comments(comments, (*path, index), (*path, name))
        elif isinstance(item, dict) and len(item) == 1:
            [(name, conf)] = item.items()
            conf = {} if conf is None else conf
            # Comments on the item, and on its key, both describe the setting.
            item_comments = comments.pop((*path, index), {})
            _rename_comments(comments, (*path, index, name), (*path, name))
            if item_comments:
                merged = comments.setdefault((*path, name), {})
                merged["before"] = item_comments.get("before", []) + merged.get(
                    "before", []
                )
                if "trailing" in item_comments and "trailing" not in merged:
                    merged["trailing"] = item_comments["trailing"]
        else:
            raise ConversionError(f"Unexpected entry in {'.'.join(path)}: {item!r}")
        result[name] = conf
    return result


def to_toml_data(value, path, notes, python_names):
    """Convert a value loaded from YAML into a value that can be written as TOML.

    :param value: The value to convert.
    :param path: The key path of the value, for messages.
    :param notes: A list to which notes about the conversion are added.
    :param python_names: A set to which the strings converted from Python
        names are added.
    """
    name = ".".join(str(part) for part in path)
    if isinstance(value, PythonName):
        notes.append(f"{name}: Python name converted to the string {str(value)!r}")
        python_names.add(str(value))
        return str(value)
    if isinstance(value, EnvTag):
        raise ConversionError(
            f"{name} uses !ENV, which isn't supported in TOML. Remove it from the "
            "YAML configuration, and convert again."
        )
    if isinstance(value, dict):
        result = {}
        for key, child in value.items():
            if not isinstance(key, str):
                raise ConversionError(f"{name} has a non-string key: {key!r}")
            if child is None:
                notes.append(
                    f"{name}.{key}: dropped, because it has no value (null), which "
                    "Zensical treats the same as not setting it"
                )
                continue
            result[key] = to_toml_data(child, (*path, key), notes, python_names)
        return result
    if isinstance(value, list):
        if any(item is None for item in value):
            raise ConversionError(f"{name} contains a null value")
        return [
            to_toml_data(item, (*path, index), notes, python_names)
            for index, item in enumerate(value)
        ]
    if isinstance(value, (str, bool, int, float, datetime.date)):
        return value
    raise ConversionError(f"{name} has a value that can't be converted: {value!r}")


###########################################################################
# Navigation
###########################################################################


def resolve_literate_nav(docs_dir, plugin_config, yaml_nav, exclude_globs=()):
    """Resolve the navigation the literate-nav plugin would have generated.

    This uses literate-nav's own parser, so the result is the navigation that
    MkDocs used.

    :param docs_dir: The directory containing the (English) Markdown content.
    :param plugin_config: The configuration of the literate-nav plugin.
    :param yaml_nav: The `nav` setting from the configuration, if any.
    :param exclude_globs: Glob patterns (as used by the `exclude` plugin) of
        files that are removed from the site before literate-nav runs.
    :returns: A tuple of the resolved navigation, and the list of navigation
        files (relative to the docs directory) that were used.
    """
    try:
        from mkdocs.structure.files import Files, InclusionLevel, get_files
        from mkdocs_literate_nav.plugin import resolve_directories_in_nav
    except ImportError as e:
        raise ConversionError(
            "Converting a literate-nav navigation file requires mkdocs-literate-nav. "
            "Install it with `python -m pip install mkdocs-literate-nav==0.6.3`, or "
            "install beeware-docs-tools with the `convert` extra."
        ) from e

    unsupported = set(plugin_config) - {"nav_file", "implicit_index", "tab_length"}
    if unsupported:
        raise ConversionError(
            f"Unsupported literate-nav settings: {', '.join(sorted(unsupported))}"
        )

    import fnmatch

    with tempfile.TemporaryDirectory() as site_dir:
        files = get_files(
            {
                "docs_dir": str(docs_dir),
                "site_dir": site_dir,
                "use_directory_urls": True,
                "exclude_docs": None,
                "draft_docs": None,
                "not_in_nav": None,
            }
        )
    if exclude_globs:
        files = Files(
            [
                file
                for file in files
                if not any(fnmatch.fnmatch(file.src_path, g) for g in exclude_globs)
            ]
        )

    nav_file = plugin_config.get("nav_file", "SUMMARY.md")
    nav = resolve_directories_in_nav(
        yaml_nav,
        files,
        nav_file_name=nav_file,
        implicit_index=plugin_config.get("implicit_index", False),
        markdown_config={
            "extensions": [],
            "extension_configs": {},
            "tab_length": plugin_config.get("tab_length", 4),
        },
    )
    nav_files = [
        file.src_uri
        for file in files
        if file.name == Path(nav_file).stem
        and file.inclusion == InclusionLevel.NOT_IN_NAV
    ]
    nav_comments = {}
    return _clean_nav(nav, nav_comments), nav_files, nav_comments


_HTML_COMMENT = re.compile(r"<!--(.*?)-->", re.DOTALL)


def _clean_nav(nav, comments=None, path=()):
    """Convert a resolved navigation into plain lists, strings and mappings.

    literate-nav represents an untitled page as ``{None: path}``; in a `nav`
    setting, that is written as the bare path.

    An HTML comment in a navigation file becomes part of the title of the item
    it follows (where it isn't visible, because it's rendered as a comment).
    These are removed from the title, and recorded in ``comments``.

    :param nav: The resolved navigation.
    :param comments: A dictionary that will map the index path of an item to
        the comments that were removed from its title.
    :param path: The index path of ``nav``.
    """
    if comments is None:
        comments = {}
    result = []
    for index, item in enumerate(nav):
        if isinstance(item, dict):
            if len(item) != 1:
                raise ConversionError(f"Unexpected navigation entry: {item!r}")
            [(title, value)] = item.items()
            if isinstance(value, list):
                value = _clean_nav(value, comments, (*path, index))
            if title is not None:
                found = [c.strip() for c in _HTML_COMMENT.findall(title)]
                if found:
                    comments[(*path, index)] = found
                    title = " ".join(_HTML_COMMENT.sub(" ", title).split())
            result.append(value if title is None else {title: value})
        else:
            result.append(item)
    return result


def nav_titles(nav):
    """The set of titles in a `nav` setting."""
    titles = set()

    def accumulate(entry):
        titles.add(entry)
        return entry

    process_nav(nav, accumulate)
    return titles


###########################################################################
# Writing TOML
###########################################################################

_BARE_KEY = re.compile(r"^[A-Za-z0-9_-]+$")
_LINE_LENGTH = 88
_INDENT = "    "


def _escape(text):
    """Escape text for use in a TOML basic string."""
    text = json.dumps(text, ensure_ascii=False)[1:-1]
    return text.replace("\x7f", "\\u007f")


def toml_key(key):
    """Format a key, quoting it if necessary. Keys are always on a single line."""
    return key if _BARE_KEY.match(key) else f'"{_escape(key)}"'


def toml_string(value):
    """Format a string as a TOML basic string (multi-line if it contains newlines)."""
    if "\n" in value.rstrip("\n") or value.endswith("\n") and len(value) > 1:
        lines = value.split("\n")
        body = "\n".join(_escape(line) for line in lines)
        return f'"""\n{body}"""'
    return f'"{_escape(value)}"'


def toml_scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isnan(value):
            return "nan"
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        return repr(value)
    if isinstance(value, str):
        return toml_string(value)
    if isinstance(value, datetime.date):
        return value.isoformat()
    raise ConversionError(f"Can't write {value!r} as TOML")


def toml_inline(value):
    """Format a value on a single line."""
    if isinstance(value, dict):
        if not value:
            return "{}"
        items = ", ".join(f"{toml_key(k)} = {toml_inline(v)}" for k, v in value.items())
        return f"{{ {items} }}"
    if isinstance(value, list):
        return "[" + ", ".join(toml_inline(v) for v in value) + "]"
    return toml_scalar(value)


def _is_table(value):
    return isinstance(value, dict) and bool(value)


def _is_array_of_tables(value):
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, dict) for item in value)
        and any(any(isinstance(v, dict) for v in item.values()) for item in value)
    )


class TomlWriter:
    """Write configuration data as TOML, with comments.

    :param comments: The comments to include, keyed by key path, as returned
        by ``extract_comments()``.
    :param path_map: A function that maps a key path in the TOML data to the key
        path of the original YAML setting (for finding comments).
    :param nav_comments: Comments for items in the `nav` setting, keyed by
        the index path of the item.
    """

    def __init__(self, comments, path_map=lambda path: path, nav_comments=None):
        self.comments = comments
        self.path_map = path_map
        self.nav_comments = nav_comments or {}
        self.used = set()
        self.lines = []

    def _comments(self, path):
        yaml_path = self.path_map(path)
        found = self.comments.get(yaml_path)
        if found:
            self.used.add(yaml_path)
            return found
        return {}

    def _before(self, path, indent=""):
        for line in self._comments(path).get("before", []):
            self.lines.append(f"{indent}# {line}".rstrip())

    def _trailing(self, path):
        trailing = self._comments(path).get("trailing")
        return f"  # {trailing}" if trailing else ""

    def unused_comments(self):
        return {
            path: comment
            for path, comment in self.comments.items()
            if path not in self.used
        }

    def blank(self):
        if self.lines and self.lines[-1] != "":
            self.lines.append("")

    def text(self):
        while self.lines and self.lines[-1] == "":
            self.lines.pop()
        return "\n".join(self.lines) + "\n"

    # Values

    def key_value(self, key, value, path, indent=""):
        """Write `key = value`, where `key` may be a dotted key."""
        self._before(path, indent)
        trailing = self._trailing(path)
        if isinstance(value, list) and self._multiline_array(value, path, key, indent):
            line = f"{indent}{key} = ["
            self.lines.append(line + trailing)
            self._array_items(value, path, indent + _INDENT)
            self.lines.append(f"{indent}]")
            return
        if isinstance(value, str) and "\n" in value:
            self.lines.append(f"{indent}{key} = {toml_string(value)}{trailing}")
            return
        self.lines.append(f"{indent}{key} = {toml_inline(value)}{trailing}")

    def _multiline_array(self, value, path, key, indent):
        if not value:
            return False
        if any(isinstance(item, (dict, list)) for item in value):
            return True
        if any(self._comments((*path, index)) for index in range(len(value))):
            return True
        return len(f"{indent}{key} = {toml_inline(value)}") > _LINE_LENGTH

    def _array_items(self, value, path, indent):
        for index, item in enumerate(value):
            item_path = (*path, index)
            self._before(item_path, indent)
            if isinstance(item, list) and item:
                self.lines.append(f"{indent}[{self._trailing(item_path)}")
                self._array_items(item, item_path, indent + _INDENT)
                self.lines.append(f"{indent}],")
            else:
                self.lines.append(
                    f"{indent}{toml_inline(item)},{self._trailing(item_path)}"
                )

    def dotted_values(self, prefix, value, path, indent=""):
        """Write a table as dotted keys (`a.b.c = value`) in the current table."""
        if not _is_table(value):
            self.key_value(prefix, value, path, indent)
            return
        # Comments on the table itself go above its first value.
        comments = self._comments(path)
        for line in comments.get("before", []):
            self.lines.append(f"{indent}# {line}".rstrip())
        if "trailing" in comments:
            self.lines.append(f"{indent}# {comments['trailing']}".rstrip())
        for key, child in value.items():
            self.dotted_values(f"{prefix}.{toml_key(key)}", child, (*path, key), indent)

    def nav(self, key, nav, path):
        """Write a `nav` setting, as nested arrays of inline tables."""
        self._before(path)
        self.lines.append(f"{key} = [{self._trailing(path)}")
        self._nav_items(nav, _INDENT, ())
        self.lines.append("]")

    def _nav_items(self, items, indent, path):
        for index, item in enumerate(items):
            for comment in self.nav_comments.get((*path, index), []):
                for line in comment.splitlines():
                    self.lines.append(f"{indent}# {line.strip()}".rstrip())
            if isinstance(item, str):
                self.lines.append(f"{indent}{toml_string(item)},")
                continue
            if not isinstance(item, dict) or len(item) != 1:
                raise ConversionError(f"Unexpected navigation entry: {item!r}")
            [(title, value)] = item.items()
            # Titles are always quoted, for consistency.
            key = f'"{_escape(title)}"'
            if isinstance(value, list):
                self.lines.append(f"{indent}{{ {key} = [")
                self._nav_items(value, indent + _INDENT, (*path, index))
                self.lines.append(f"{indent}] }},")
            else:
                self.lines.append(f"{indent}{{ {key} = {toml_inline(value)} }},")

    # Tables

    def table(self, path, table, header_style=None):
        """Write a table, and all of its subtables.

        :param path: The key path of the table.
        :param table: The table's content.
        :param header_style: Optional function that takes a key path and returns
            the way to write that table: "dotted" (as dotted keys in the parent
            table), "nav", or None (as a table with a header).
        """
        header_style = header_style or (lambda path: None)
        if not isinstance(table, dict):
            raise ConversionError(f"{'.'.join(path)} must be a table")
        simple = []
        subtables = []
        for key, value in table.items():
            child = (*path, key)
            style = header_style(child)
            if style in {"dotted", "nav"} or (
                style != "table"
                and not (_is_table(value) or _is_array_of_tables(value))
            ):
                simple.append((key, value, style))
            else:
                subtables.append((key, value))

        header = ".".join(toml_key(key) for key in path)
        if path and (simple or not subtables or self._comments(path)):
            self.blank()
            self._before(path)
            self.lines.append(f"[{header}]{self._trailing(path)}")

        for key, value, style in simple:
            child = (*path, key)
            if style == "nav":
                self.nav(toml_key(key), value, child)
            elif style == "dotted":
                key_text = (
                    _extension_key(key)
                    if path[-1:] == ("markdown_extensions",)
                    else toml_key(key)
                )
                self.dotted_values(key_text, value, child)
            else:
                self.key_value(toml_key(key), value, child)

        for key, value in subtables:
            child = (*path, key)
            if isinstance(value, dict):
                self.table(child, value, header_style)
            else:
                self.array_of_tables(child, value)

    def array_of_tables(self, path, items):
        header = ".".join(toml_key(key) for key in path)
        self._before(path)
        for index, item in enumerate(items):
            item_path = (*path, index)
            self.blank()
            self._before(item_path)
            self.lines.append(f"[[{header}]]{self._trailing(item_path)}")
            for key, value in item.items():
                self.dotted_values(toml_key(key), value, (*item_path, key))


def _extension_key(name):
    """The TOML key for a Markdown extension.

    Zensical reads ``pymdownx.<name>`` and ``pymdownx.blocks.<name>`` (and the
    same for ``zensical``) as dotted keys. Any other name containing a dot must
    be quoted.
    """
    parts = name.split(".")
    if len(parts) == 1:
        return toml_key(name)
    if (
        parts[0] in {"pymdownx", "zensical"}
        and (len(parts) == 2 or (len(parts) == 3 and parts[1] == "blocks"))
        and all(_BARE_KEY.match(part) for part in parts)
    ):
        return name
    return toml_string(name)


def _extension_order(name):
    """The order Zensical reads dotted extension keys in.

    Zensical moves the ``pymdownx`` extensions (and then the ``zensical``
    extensions) after all the others.
    """
    key = _extension_key(name)
    if key.startswith("pymdownx."):
        return 1
    if key.startswith("zensical."):
        return 2
    return 0


def write_config_toml(project, comments, nav_key=False, nav_comments=None):
    """Format a ``[project]`` table as TOML.

    :param project: The configuration.
    :param comments: The comments from the YAML file.
    :param nav_key: True if the `nav` setting should be written as a navigation
        tree.
    :param nav_comments: Comments for items in the `nav` setting.
    :returns: A tuple of the TOML text, and the comments that weren't written.
    """
    project = dict(project)

    def path_map(path):
        # The TOML data is nested under "project"; the YAML isn't.
        return path[1:]

    writer = TomlWriter(comments, path_map, nav_comments)

    def header_style(path):
        if path == ("project", "nav") and nav_key:
            return "nav"
        if len(path) == 3 and path[1] == "markdown_extensions":
            return "dotted"
        # Each plugin is written as a table, even if it's empty.
        if len(path) == 3 and path[1] == "plugins":
            return "table"
        return None

    # Write the Markdown extensions in the order Zensical will read them in.
    extensions = project.get("markdown_extensions")
    if extensions:
        project["markdown_extensions"] = dict(
            sorted(extensions.items(), key=lambda item: _extension_order(item[0]))
        )

    writer.table(("project",), project, header_style)
    return writer.text(), writer.unused_comments()


###########################################################################
# Equivalence checks
###########################################################################


def _callable_name(value):
    return f"{value.__module__}.{value.__qualname__}"


def _normalize(value):
    """Normalize a loaded configuration value for comparison.

    Python objects (from ``!!python/name:`` tags) are represented by their
    dotted name, and null values (which can't be expressed in TOML, and which
    Zensical treats the same as a missing value) are removed.
    """
    if isinstance(value, dict):
        return {k: _normalize(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    if callable(value):
        return _callable_name(value)
    return value


def _resolve_names(value, names):
    """Resolve the strings that were converted from Python names to objects."""
    from zensical.config import _resolve

    if isinstance(value, dict):
        return {k: _resolve_names(v, names) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve_names(v, names) for v in value]
    if isinstance(value, str) and value in names:
        return _callable_name(_resolve(value))
    return value


def _differences(old, new, path=()):
    """List the differences between two normalized configuration values."""
    name = ".".join(str(p) for p in path) or "(root)"
    if isinstance(old, dict) and isinstance(new, dict):
        diffs = []
        for key in old.keys() | new.keys():
            if key not in new:
                diffs.append(f"{name}.{key}: missing from the converted configuration")
            elif key not in old:
                diffs.append(f"{name}.{key}: added by the conversion")
            else:
                diffs.extend(_differences(old[key], new[key], (*path, key)))
        return diffs
    if old != new:
        return [f"{name}: {old!r} became {new!r}"]
    return []


def _markdown_extensions(config):
    from zensical.config import _convert_markdown_extensions

    names, configs = _convert_markdown_extensions(
        config.pop("markdown_extensions", None)
    )
    return names, configs


def compare_configs(old, new, python_names, allowed):
    """Compare the configuration Zensical read from YAML with the converted one.

    The intended differences are:

    * `nav` is generated from the literate-nav navigation file (the
      literate-nav plugin and its navigation file are removed);
    * `site_url` is set from the environment, rather than with ``!ENV``;
    * Python names are strings, rather than ``!!python/name:`` tags; and
    * the Markdown extensions with dotted keys (``pymdownx.*``) are read after
      the others.

    :param old: The configuration from ``zensical.config._yaml_load()``.
    :param new: The merged TOML configuration.
    :param python_names: The strings that were converted from Python names.
    :param allowed: The intended differences that apply: a set containing any
        of "nav" and "site_url".
    :returns: A tuple of the list of unexpected differences, and a list of
        notes about intended differences.
    """
    # Named items with no configuration (`search:` or `- search`) are the same
    # as an empty configuration; resolve that before null values are removed.
    old = dict(old)
    for setting in ("plugins", "markdown_extensions"):
        value = old.get(setting)
        if isinstance(value, list):
            old[setting] = {
                (item if isinstance(item, str) else next(iter(item))): (
                    {} if isinstance(item, str) else next(iter(item.values()))
                )
                for item in value
            }
        if isinstance(old.get(setting), dict):
            old[setting] = {k: {} if v is None else v for k, v in old[setting].items()}

    old = _normalize(old)
    new = _normalize(_resolve_names(new, python_names))
    notes = []

    if "site_url" in allowed:
        old.pop("site_url", None)
        new.pop("site_url", None)

    old_plugins = old.get("plugins") or {}
    if "nav" in allowed:
        old_plugins.pop("literate-nav", None)
        old.pop("nav", None)
        new.pop("nav", None)
    old["plugins"] = old_plugins
    new.setdefault("plugins", {})
    if list(old_plugins) != list(new["plugins"]):
        message = (
            f"plugins: order or names changed from {list(old_plugins)} to "
            f"{list(new['plugins'])}"
        )
        return [message], notes

    old_names, old_configs = _markdown_extensions(old)
    new_names, new_configs = _markdown_extensions(new)
    diffs = []
    if old_names != new_names:
        if sorted(old_names) == sorted(new_names):
            notes.append(
                "Markdown extension order: "
                + ", ".join(new_names)
                + " (was "
                + ", ".join(old_names)
                + ")"
            )
        else:
            diffs.append(f"markdown_extensions: {old_names} became {new_names}")
    diffs.extend(
        _differences(
            _normalize(old_configs), _normalize(new_configs), ("markdown_extensions",)
        )
    )
    diffs.extend(_differences(old, new))
    return diffs, notes


###########################################################################
# Translations
###########################################################################

_LINK = re.compile(r"^\s*\[(?P<title>.*)\]\s*(\{\d+\}|\([^)]*\))\s*$", re.DOTALL)


def migrate_nav_translations(po_path, nav_sources, titles, titles_occurrence):
    """Migrate the navigation title translations in a PO file.

    Titles that were translated as part of a literate-nav navigation file have
    msgids like ``[Title]{1}`` (for a link) or ``Title`` (for a section). In a
    `nav` setting, all titles are extracted as plain text (``Title``). This
    adds (or fills in) an entry for each title, using the translation of the
    link text, keeping the fuzzy flag as it was, and removes the entries that
    were only used by the navigation file.

    :param po_path: The PO file to update.
    :param nav_sources: The source references (as used in the PO file) of the
        navigation files.
    :param titles: The titles in the new `nav` setting.
    :param titles_occurrence: The source reference to use for title entries.
    :returns: A dictionary of counts and messages describing the migration.
    """
    po = polib.pofile(str(po_path), wrapwidth=100000)
    report = {
        "moved": 0,
        "matched": 0,
        "kept": 0,
        "removed": 0,
        "conflicts": [],
        "unmapped": [],
    }

    nav_entries = [
        entry
        for entry in po
        if not entry.obsolete
        and any(source in nav_sources for source, _ in entry.occurrences)
    ]

    def is_nav_only(entry):
        return all(source in nav_sources for source, _ in entry.occurrences)

    for entry in nav_entries:
        link = _LINK.match(entry.msgid)
        title = link.group("title") if link else entry.msgid
        if title not in titles:
            continue

        if not link:
            # Already a plain title; it's kept, with a new source reference.
            report["kept"] += 1
            continue

        translated = ""
        if entry.msgstr:
            match = _LINK.match(entry.msgstr)
            if match:
                translated = match.group("title")
            else:
                report["unmapped"].append(f"{entry.msgid!r} -> {entry.msgstr!r}")
                continue

        target = po.find(title)
        if target is None or target.obsolete:
            po.append(
                polib.POEntry(
                    msgid=title,
                    msgstr=translated,
                    flags=list(entry.flags),
                    occurrences=[(titles_occurrence, "")],
                )
            )
            report["moved"] += 1
        elif not target.msgstr and translated:
            target.msgstr = translated
            target.flags = list(entry.flags)
            report["moved"] += 1
        elif target.msgstr and translated and target.msgstr != translated:
            report["conflicts"].append(
                f"{title!r}: kept {target.msgstr!r}, not {translated!r}"
            )
        else:
            report["matched"] += 1

    for entry in nav_entries:
        others = [o for o in entry.occurrences if o[0] not in nav_sources]
        link = _LINK.match(entry.msgid)
        is_title = not link and entry.msgid in titles
        if is_title:
            entry.occurrences = [*others, (titles_occurrence, "")]
        elif others:
            entry.occurrences = others
        elif is_nav_only(entry):
            po.remove(entry)
            report["removed"] += 1

    po.save(str(po_path))
    return report


###########################################################################
# Conversion
###########################################################################


def convert(docs, write=True, keep_old=False, out=print):
    """Convert the MkDocs configuration in a ``docs`` directory.

    :param docs: The ``docs`` directory.
    :param write: If False, check the conversion, but don't change any files.
    :param keep_old: If True, don't delete the original files.
    :param out: A function used to report progress.
    :returns: True if the conversion succeeded.
    """
    docs = Path(docs)
    base_file = docs / "config.yml"
    if not base_file.is_file():
        raise ConversionError(f"{base_file} doesn't exist")
    language_files = sorted(docs.glob("mkdocs.*.yml"))
    if not language_files:
        raise ConversionError(f"No mkdocs.<lang>.yml files in {docs}")
    languages = [path.name[len("mkdocs.") : -len(".yml")] for path in language_files]

    notes = []
    allowed = set()
    python_names = set()

    # Load the base configuration.
    base, base_comments, unplaced = load_yaml(base_file)
    for comment in unplaced:
        notes.append(f"{base_file.name}: comment not carried over: {comment!r}")
    if "INHERIT" in base:
        raise ConversionError(f"{base_file.name} uses INHERIT, which isn't supported")

    if isinstance(base.get("site_url"), EnvTag):
        del base["site_url"]
        allowed.add("site_url")
        notes.append(
            f"{base_file.name}: site_url (!ENV) removed; it's set from "
            "READTHEDOCS_CANONICAL_URL at build time"
        )

    for setting in ("markdown_extensions", "plugins"):
        if setting in base:
            base[setting] = normalize_named_items(
                base[setting], (setting,), base_comments
            )

    # Load the language configurations.
    language_configs = {}
    for language, path in zip(languages, language_files, strict=True):
        config, comments, unplaced = load_yaml(path)
        for comment in unplaced:
            notes.append(f"{path.name}: comment not carried over: {comment!r}")
        inherit = config.pop("INHERIT", None)
        if inherit != "config.yml":
            raise ConversionError(
                f"{path.name} must have `INHERIT: config.yml` (found {inherit!r})"
            )
        if isinstance(config.get("site_url"), EnvTag):
            del config["site_url"]
            allowed.add("site_url")
        for setting in ("markdown_extensions", "plugins"):
            if setting in config:
                raise ConversionError(
                    f"{path.name} sets {setting}, which isn't supported in a "
                    "language file"
                )
        language_configs[language] = (config, comments)

    # A literal `site_url` is kept. If every language file sets the same one,
    # it's moved into the base configuration.
    site_urls = {
        str(config.get("site_url"))
        for config, _ in language_configs.values()
        if "site_url" in config
    }
    if (
        len(site_urls) == 1
        and all("site_url" in config for config, _ in language_configs.values())
        and base.get("site_url", next(iter(site_urls))) == next(iter(site_urls))
    ):
        base["site_url"] = next(iter(site_urls))
        for config, comments in language_configs.values():
            del config["site_url"]
            _rename_comments(comments, ("site_url",), ("removed",))
        notes.append(
            f"site_url: the same value ({base['site_url']!r}) was set for every "
            f"language, so it was moved into {BASE_CONFIG}"
        )

    # Note any plugins that Zensical doesn't support (and will ignore).
    from zensical.config import _PLUGIN_UNSUPPORTED_OPTIONS

    for name in base.get("plugins", {}):
        canonical = name.removeprefix("material/").split("/", 1)[0]
        if canonical not in _PLUGIN_UNSUPPORTED_OPTIONS:
            notes.append(
                f"plugins.{name}: Zensical doesn't support this plugin, and will "
                "ignore it"
            )

    # Convert the literate-nav navigation file into a `nav` setting.
    nav_files = []
    nav_comments = {}
    plugins = base.get("plugins", {})
    if "literate-nav" in plugins:
        en_config = language_configs.get("en", ({}, {}))[0]
        docs_dir = docs / en_config.get("docs_dir", base.get("docs_dir", "docs"))
        exclude_globs = (plugins.get("exclude") or {}).get("glob", [])
        nav, nav_files, nav_comments = resolve_literate_nav(
            docs_dir,
            plugins.pop("literate-nav") or {},
            base.get("nav"),
            exclude_globs=exclude_globs,
        )
        nav_files = [docs_dir / path for path in nav_files]
        _rename_comments(base_comments, ("plugins", "literate-nav"), ("removed",))
        base["nav"] = nav
        allowed.add("nav")
        notes.append(
            "nav: generated from "
            + ", ".join(str(path.relative_to(docs.parent)) for path in nav_files)
            + "; the literate-nav plugin was removed"
        )

    # Convert the values to TOML-compatible data.
    def convert_values(config, label):
        conversion_notes = []
        data = to_toml_data(config, (), conversion_notes, python_names)
        for note in conversion_notes:
            notes.append(f"{label}: {note}")
        return data

    base = convert_values(base, base_file.name)
    language_data = {
        language: (convert_values(config, f"mkdocs.{language}.yml"), comments)
        for language, (config, comments) in language_configs.items()
    }

    # Write the TOML files.
    outputs = {}
    text, unused = write_config_toml(
        base, base_comments, nav_key=True, nav_comments=nav_comments
    )
    outputs[BASE_CONFIG] = text
    for path, comment in unused.items():
        if path and path[0] == "removed":
            continue
        notes.append(
            f"{base_file.name}: comment not carried over ({'.'.join(map(str, path))}): "
            f"{comment}"
        )
    for language, (config, comments) in language_data.items():
        text, unused = write_config_toml(config, comments)
        outputs[language_config_name(language)] = text
        for path, comment in unused.items():
            if path and path[0] == "removed":
                continue
            notes.append(
                f"mkdocs.{language}.yml: comment not carried over "
                f"({'.'.join(map(str, path))}): {comment}"
            )

    # Check the converted configuration against what Zensical reads from YAML.
    from zensical.config import _yaml_load

    failed = False
    with tempfile.TemporaryDirectory() as temp:
        temp_path = Path(temp)
        for name, text in outputs.items():
            (temp_path / name).write_text(text, encoding="utf-8")
            try:
                tomllib.loads(text)
            except tomllib.TOMLDecodeError as e:
                raise ConversionError(f"Generated invalid TOML for {name}: {e}") from e

        new_base = read_toml(temp_path / BASE_CONFIG)
        reported_notes = set()
        for language, path in zip(languages, language_files, strict=True):
            with path.open(encoding="utf-8") as f:
                old = _yaml_load(f)
            language_config = read_toml(temp_path / language_config_name(language))
            for key in unexpected_language_keys(language_config):
                notes.append(
                    f"{language_config_name(language)}: {key!r} isn't a per-language "
                    "setting; it will produce a warning at build time"
                )
            new = merge_config(new_base, language_config)
            diffs, check_notes = compare_configs(old, new, python_names, allowed)
            for note in check_notes:
                if note not in reported_notes:
                    reported_notes.add(note)
                    notes.append(note)
            if diffs:
                failed = True
                out(f"{language}: the converted configuration differs:")
                for diff in diffs:
                    out(f"    {diff}")
            else:
                out(f"{language}: the converted configuration is equivalent")

    for note in notes:
        out(f"Note: {note}")

    if failed:
        out("Conversion failed; no files were changed.")
        return False

    if not write:
        out("Check complete; no files were changed (--check).")
        return True

    for name, text in outputs.items():
        (docs / name).write_text(text, encoding="utf-8")
        out(f"Wrote {docs / name}")

    # Migrate the translations of the navigation titles.
    if nav_files:
        titles = nav_titles(base["nav"])
        project_root = docs.parent
        nav_sources = {path.relative_to(project_root).as_posix() for path in nav_files}
        titles_occurrence = (docs / TITLES_FILE).relative_to(project_root).as_posix()
        for po_path in sorted(docs.glob("locales/*/translations.po")):
            report = migrate_nav_translations(
                po_path, nav_sources, titles, titles_occurrence
            )
            out(
                f"{po_path}: {report['moved']} link titles migrated, "
                f"{report['matched']} already had the same translation, "
                f"{len(report['conflicts'])} already had a different translation, "
                f"{len(report['unmapped'])} couldn't be mapped; "
                f"{report['kept']} section titles kept; "
                f"{report['removed']} navigation-only entries removed"
            )
            for conflict in report["conflicts"]:
                out(f"    Conflict: {conflict}")
            for unmapped in report["unmapped"]:
                out(f"    Couldn't map: {unmapped}")

    if not keep_old:
        for path in [base_file, *language_files, *nav_files]:
            path.unlink()
            out(f"Removed {path}")

    return True


def main():
    parser = ArgumentParser(
        description=(
            "Convert docs/config.yml, docs/mkdocs.<lang>.yml and the literate-nav "
            "navigation file into docs/zensical.toml and docs/zensical.<lang>.toml."
        )
    )
    parser.add_argument(
        "-d",
        "--docs-directory",
        type=Path,
        default=Path("docs"),
        help="The documentation directory. Default: docs",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check the conversion, but don't change any files.",
    )
    parser.add_argument(
        "--keep-old",
        action="store_true",
        help="Don't delete the original YAML and navigation files.",
    )
    args = parser.parse_args()

    try:
        success = convert(
            args.docs_directory, write=not args.check, keep_old=args.keep_old
        )
    except ConversionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
