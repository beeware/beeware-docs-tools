We're always open to suggestions and ideas for new features or documentation for {{ formal_name }}. But how you do you go about submitting your idea for consideration?

## Before you begin

We already have a very long list of features we'd like to implement, and very limited resources. If you've got an idea that you think would make {{ formal_name }} better, we'd love to hear about it. If enough people request the same thing, the core team might implement that idea. However, by itself, making a feature request is unlikely to result in that feature being implemented in the near future.

BeeWare is an Open Source community. The most effective way to ensure that a feature is implemented is to *implement it yourself*. We'll do anything we can to help contributors implement the features they want to see added. Demands that the core team implement a feature for you, for free, are unlikely to be well received.

If you're not in a position to implement a feature yourself, the other way to accelerate the development of your feature is to pay someone to implement it for you.If you'd like to discuss paying to have the development of a specific feature prioritized, please [contact the BeeWare team](mailto:consulting@beeware.org).

### Suggesting new functionality

The most obvious thing to suggest is a new API or capability. If you have a use case that {{ formal_name }} doesn't currently support, or there's a native platform capability that {{ formal_name }} can't currently utilize, you might want to propose a change to address that gap.

When proposing a new feature, keep in mind that the BeeWare suite of tools support multiple platforms. This means any new feature must:

* Be suitable and implementable on all platforms (e.g. every GUI toolkit has the concept of a "button"); or
* Be suitable for platforms of the same "type", and appropriate to ignore on other platforms (e.g. all mobile phones have accelerometers; not many desktops do, and therefore, it makes sense for an accelerometer API to exist for iOS and Android, but not for the desktop or web platforms); or
* Allow access to an internal platform feature without altering the public API (e.g. you can't add a feature that is clearly Android-specific, but you could make it easier for end users to access an Android-specific feature from their own code).

This doesn't mean you need to be responsible for implementing a feature on every platform. If you don't have access to Apple hardware, it's not reasonable for us to expect you to provide a macOS or iOS implementation of a feature. However, as part of the design process, we need to establish that it would be *possible* to implement a feature in the way you describe.

{% block suggesting_new_features %}
{% endblock %}

### Suggesting new documentation { #suggesting-new-docs }

Another thing you might want to suggest is an improvement to documentation. If you have an idea for improving the documentation for {{ formal_name }}, considerations include:

* Does your suggestion overlap with existing documentation? Are you proposing a new guide, or an addition to an existing guide?
* How does it fit into the rest of the BeeWare ecosystem? Is this project the right place to document the idea? Or should we document a feature in another project, and link to that documentation?
* Is there a high-level concept that needs explanation before any specific instructions will make sense?
* Does the topic make sense for us to explain, or has someone else already covered it somewhere that we can refer to?

If you're unsure about any of this, don't worry! Submit your idea, and let us know in the initial discussion what you're unsure of, and we can help shape the ideas that you have into a form that will fit BeeWare's documentation.

## Contributing a feature proposal

/// details-abstract | Proposing a new feature

{% include "contribute/how/propose-feature.md" %}

///
