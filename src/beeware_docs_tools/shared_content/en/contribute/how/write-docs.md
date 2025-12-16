
These are the steps to follow to write your documentation contribution to {{ formal_name }}.

{% block front_matter %}
{% endblock %}

### Updating existing documentation

If you're editing the existing docs, you'll need to locate the file in the `/docs/en` directory. The file structure follows the page structure, so you can locate the file using the documentation URL.

### Adding new documentation

If you're adding a new document, there are a few more steps involved.

You'll need to create the document in the appropriate location within the `docs/en` directory. For discussion, we'll say you're adding a new document with the filename `new_doc.md`.

Then, you'll need to update the `docs/en/SUMMARY.md` file to include your new file. `SUMMARY.md` is organized to basically reflect the `docs/en` directory structure, but, more importantly, directly determines the structure of the left sidebar. If you locate the section where you intend to include `new_doc.md`, you do not need to change anything in `SUMMARY.md` if you see a wildcard path listed. For example:

```markdown
- ./path/to/directory/*
```

If the section where you intend to include `new_doc.md` is a list of individual Markdown links, you'll need to add an explicit link to yours. For example:

```markdown
- [My new document](new_doc.md)
```

### Writing your documentation

You can now open the desired file into your editor, and begin writing.

We have a [documentation style guide](../style/docs-style-guide.md) that outlines our guidelines for writing documentation for BeeWare.

{% block end_matter %}
{% endblock %}
