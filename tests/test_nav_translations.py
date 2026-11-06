import polib

from beeware_docs_tools.build_config import translate
from beeware_docs_tools.nav_translations import (
    NAV_CONTEXT,
    add_nav_context,
    seed_nav_translations,
)


def catalog(*entries):
    po = polib.POFile(wrapwidth=100000)
    for entry in entries:
        po.append(entry)
    return po


def test_add_nav_context():
    """Navigation titles get their own context, split from page headings."""
    po = catalog(
        polib.POEntry(
            msgid="Building documentation",
            occurrences=[
                ("docs/en/how/build-docs.md", "1"),
                ("docs/en/titles.md", "7"),
            ],
        ),
        polib.POEntry(msgid="Section one", occurrences=[("docs/en/titles.md", "3")]),
        polib.POEntry(msgid="Some text.", occurrences=[("docs/en/index.md", "5")]),
    )

    assert add_nav_context(po) == 2

    assert [(e.msgctxt, e.msgid, e.occurrences) for e in po] == [
        (None, "Building documentation", [("docs/en/how/build-docs.md", "1")]),
        (NAV_CONTEXT, "Building documentation", [("docs/en/titles.md", "7")]),
        (NAV_CONTEXT, "Section one", [("docs/en/titles.md", "3")]),
        (None, "Some text.", [("docs/en/index.md", "5")]),
    ]
    # Running it again changes nothing.
    assert add_nav_context(po) == 0
    assert len(po) == 4


def test_seed_nav_translations():
    """Navigation entries are filled in from the translations they used before."""
    previous = catalog(
        # A literate-nav link: what the navigation displayed.
        polib.POEntry(msgid="[Section one]{1}", msgstr="[Section 1]{1}"),
        polib.POEntry(msgid="Section one", msgstr="Section un"),
        # A navigation title from before the context existed (or a heading).
        polib.POEntry(msgid="About", msgstr="À propos", flags=["fuzzy"]),
        # A link translation that has lost its markup isn't used.
        polib.POEntry(msgid="[Broken]{1}", msgstr="Cassé"),
        polib.POEntry(msgid="Untranslated", msgstr=""),
    )
    po = catalog(
        polib.POEntry(msgid="Section one", msgctxt=NAV_CONTEXT),
        polib.POEntry(msgid="About", msgctxt=NAV_CONTEXT),
        polib.POEntry(msgid="Broken", msgctxt=NAV_CONTEXT),
        polib.POEntry(msgid="Untranslated", msgctxt=NAV_CONTEXT),
        polib.POEntry(msgid="Kept", msgctxt=NAV_CONTEXT, msgstr="Gardé"),
        polib.POEntry(msgid="Section one", msgstr=""),
    )

    assert seed_nav_translations(po, previous) == ["Section one", "About"]

    nav = {e.msgid: e for e in po if e.msgctxt == NAV_CONTEXT}
    assert nav["Section one"].msgstr == "Section 1"
    assert nav["About"].msgstr == "À propos"
    assert nav["About"].fuzzy
    assert nav["Broken"].msgstr == ""
    assert nav["Untranslated"].msgstr == ""
    assert nav["Kept"].msgstr == "Gardé"
    # Entries without the navigation context aren't touched.
    assert po.find("Section one", msgctxt=None).msgstr == ""


def test_translate_prefers_nav_context():
    """The navigation translation is used, falling back to one without context."""
    po = catalog(
        polib.POEntry(msgid="Section one", msgstr="Section un"),
        polib.POEntry(msgid="Section one", msgctxt=NAV_CONTEXT, msgstr="Section 1"),
        polib.POEntry(msgid="About", msgstr="À propos"),
        polib.POEntry(msgid="Help", msgctxt=NAV_CONTEXT, msgstr=""),
        polib.POEntry(msgid="Help", msgstr="Aide"),
    )
    tr = translate(po)

    assert tr("Section one") == "Section 1"
    assert tr("About") == "À propos"
    assert tr("Help") == "Aide"
    assert tr("Missing") == "Missing"
