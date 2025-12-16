Once the [proposal process](propose-feature.md) has concluded, you should have a complete design for a new feature. That means it's time to start writing!

{% if not config.extra.macos_only %}

If your feature requires a platform-specific implementation, the proposal process should have validated that the idea *could* be implemented on all platforms. However, as the person implementing a new feature for the first time, you are not responsible for implementing the new feature for all platforms. You need to provide a complete implementation for *at least* one platform, including tests. For any other platforms, you will need to provide a "stub" implementation - an implementation that provides the bare interface definition, but raises a `NotImplementedError` or outputs a log message that the behavior isn't implemented on that platform.

An important part of implementing a new feature is ensuring that feature is fully documented. At a minimum this means ensuring that there is API documentation; but it may also require adding a how-to or topic guide.

{% block specific-feature_ideas %}
{% endblock %}

{% endif %}

## Contributing new functionality

{% macro content(template) %}{% include template %}{% endmacro %}
{% macro indented(template) %}{{ content(template)|indent }}{% endmacro %}

??? abstract "Set up a development environment"

    {{ indented("contribute/how/dev-environment.md") }}

??? abstract "Work from a branch"

    {{ indented("contribute/how/branches.md") }}

??? abstract "Avoid scope creep"

    {{ indented("contribute/how/scope-creep.md") }}

??? abstract "Implement the new feature"

    {{ indented("contribute/how/write-code.md") }}

??? abstract "Build documentation"

    {{ indented("contribute/how/build-docs.md") }}

??? abstract "Write documentation"

    {{ indented("contribute/how/write-docs.md") }}

??? abstract "Add a change note"

    {{ indented("contribute/how/change-note.md") }}

??? abstract "Submit a pull request"

    {{ indented("contribute/how/submit-pr.md") }}
