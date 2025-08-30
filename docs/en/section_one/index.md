# BeeWare Docs Tools Demo section one

## Non-homepage sidebar logo

The logo icon in the left sidebar should be small on all pages other than the homepage. The site title and version number should be rendered next to it with the site title in slightly larger font, and the version number in smaller font.

This verifies that the theme is being properly applied.

## Include external markdown from a local file

The following section should have only a header, and a paragraph with inline code followed by a code block. There should be no text between the code block and the next header. This verifies that the external include extension is working with local files.

-8<- "include_content.md:local-content"

## Include external markdown from a URL

The following section should have only a header, some text and a Markdown list. This verifies that the external include extension is working, and that `url_download` is enabled.

-8<-
https://raw.githubusercontent.com/beeware/beeware-docs-tools/refs/heads/main/docs/include_content.md:remote-content
-8<-

## Footer navigation

Navigate to *Section One - Page Two* for the final check.
