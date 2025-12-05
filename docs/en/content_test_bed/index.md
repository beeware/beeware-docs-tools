# Shared content test bed

This section is included for the purposes of verifying the shared content provided from this repo for use in the rest of the BeeWare documentation. "Shared content" refers to documents or sections of documents that are common to multiple other repos. They are stored here for inclusion across those repos. This means there is a single source when updates are required, and that change will populate across all repos using that shared content.

If you are updating existing content, the following steps are not necessary. You can simply build the test site, and see your updates rendered.

If you are creating a new shared documentation file in the `shared-content` directory, that is NOT meant to be included in the `how-to` directory, complete the following:

1. Create a file in the `content_test_bed` that is the same filename as your new content file, with "_include" appended to the end.
   * For `style_guide.md`, you would add `style_guide_include.md`.
2. Using the Snippets syntax, add the filename to `filename_include.md`. The Snippets syntax for including content is `-8<- "filename.md"`.
   * For `style_guide.md`, you would add `-8<- "style_guide.md"` to `style_guide_include.md`.
3. Update the `Shared content test bed` section in `/docs/SUMMARY.md` to include the new `_include` file and path, at the same indentation level as the other items in that section.
   * For `style_guide_include.md`, you would add `- [Style guide](content_test_bed/style_guide_include.md)`.

Once these steps are completed, you can build the test site and view your new documentation rendered.
