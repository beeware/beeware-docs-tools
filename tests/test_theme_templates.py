from pathlib import Path

OVERRIDES = (
    Path(__file__).parents[1]
    / "src"
    / "beeware_docs_tools"
    / "overrides"
)


def test_mobile_sidebar_includes_main_site_links():
    sidebar = (OVERRIDES / "partials" / "nav.html").read_text(encoding="utf-8")

    assert "mobile-main-nav" in sidebar
    for section in ["about", "docs", "community", "contributing", "news", "membership"]:
        assert f"{section}\"" in sidebar
