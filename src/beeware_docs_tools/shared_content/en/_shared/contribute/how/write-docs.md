
These are the steps to follow to write your documentation contribution to {{ formal_name }}.

{% block front_matter %}
{% endblock %}

### Updating existing documentation

If you're editing the existing docs, you'll need to locate the file in the `/docs/en` directory. The file structure follows the page structure, so you can locate the file using the documentation URL.

### Adding new documentation

If you're adding a new document, there are a few more steps involved.

You'll need to create the document in the appropriate location within the `docs/en` directory. For discussion, we'll say you're adding a new document with the filename `new_doc.md`.

Then, you'll need to add your new file to the `nav` setting in `docs/zensical.toml`. The `nav` setting is organized to basically reflect the `docs/en` directory structure, but, more importantly, directly determines the structure of the left sidebar. Locate the section where you intend to include `new_doc.md`, and add an entry for it, with the title you want to appear in the sidebar, and the path to the file, relative to `docs/en`. For example:

```toml
nav = [
    { "Existing section" = [
        { "Existing document" = "path/to/existing_doc.md" },
        { "My new document" = "path/to/new_doc.md" },
    ] },
]
```

The titles in the `nav` setting are translated along with the rest of the documentation.

### Writing your documentation

You can now open the desired file into your editor, and begin writing.

We have a [documentation style guide](../style/docs-style-guide.md) that outlines our guidelines for writing documentation for BeeWare.

{% block end_matter %}
{% endblock %}
