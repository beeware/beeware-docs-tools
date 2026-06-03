Once the [proposal process](propose-feature.md) has concluded, you should have a complete design for a new feature. That means it's time to start writing!

{% if not config.extra.macos_only %}

If your feature requires a platform-specific implementation, the proposal process should have validated that the idea *could* be implemented on all platforms. However, as the person implementing a new feature for the first time, you are not responsible for implementing the new feature for all platforms. You need to provide a complete implementation for *at least* one platform, including tests. For any other platforms, you will need to provide a "stub" implementation - an implementation that provides the bare interface definition, but raises a `NotImplementedError` or outputs a log message that the behavior isn't implemented on that platform.

An important part of implementing a new feature is ensuring that feature is fully documented. At a minimum this means ensuring that there is API documentation; but it may also require adding a how-to or topic guide.

{% block specific_feature_ideas %}
{% endblock %}

{% endif %}

## Contributing new functionality

/// details-abstract | Set up a development environment

{% include "how/dev-environment.md" %}

///

/// details-abstract | Work from a branch

{% include "how/branches.md" %}

///

/// details-abstract | Avoid scope creep

{% include "how/scope-creep.md" %}

///

/// details-abstract | Implement the new feature

{% include "how/write-code.md" %}

///

/// details-abstract | Build documentation

{% include "how/build-docs.md" %}

///

/// details-abstract | Write documentation

{% include "how/write-docs.md" %}

///

/// details-abstract | Add a change note

{% include "how/change-note.md" %}

///

/// details-abstract | Submit a pull request

{% include "how/submit-pr.md" %}

///
