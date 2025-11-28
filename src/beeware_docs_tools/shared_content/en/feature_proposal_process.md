We're always open to suggestions and ideas for new features or documentation for {{ formal_name }}. The following details the process for submitting, and potentially implementing, your idea.

## Before you begin

We already have a very long list of features we'd like to implement, and very limited resources. If you've got an idea that you think would make {{ formal_name }} better, we'd love to hear about it. If enough people request the same thing, the core team might implement that idea. However, by itself, making a feature request is unlikely to result in that feature being implemented in the near future.

BeeWare is an Open Source community. The most effective way to ensure that a feature is implemented is to *implement it yourself*. We'll do anything we can to help contributors implement the features they want to see added. Demands that the core team implement a feature for you, for free, are unlikely to be well received.

### Suggesting new features

Keep in mind that the BeeWare suite of tools support multiple platforms, so any new feature needs to:

* Be suitable and implementable on all platforms (e.g. every platform has the concept of a "button"); or
* Be suitable for platforms of the same "type", and appropriate to ignore on other platforms (e.g. all mobile phones have accelerometers; not many desktops do, and therefore, it makes sense for an accelerometer API to exist for iOS and Android, but not for the desktop or web platforms); or
* Allow access to an internal platform feature without altering the public API (e.g. you can't add a feature that is clearly Android-specific, but you can open a door that makes it easier for end users to access an Android-specific feature from their own code).

This doesn't mean you need to be responsible for implementing a feature on every platform. If you don't have access to Apple hardware, it's not reasonable for us to expect you to provide a macOS or iOS implementation of a feature. However, as part of the design process, we need to establish that it would be *possible* to implement a feature in the way you describe.

### Suggesting new documentation

When you have an idea for documentation, you'll want to determine what type of documentation fits your idea. As a starting point, you can ask yourself the following questions:

* Does it detail the process for completing a task? You're probably looking to submit a *how-to guide*.
* Does it provide information about a particular subject? You're probably looking to submit a *topic guide*.
* Is it an activity that amounts to a coherent learning path with an achievable goal? You may be looking to submit a *tutorial*.

Most of the time, your idea is likely to fit a how-to guide or a topic guide.

Other considerations include:

* Does it overlap with existing documentation? Should your change be a new guide, or an addition to an existing guide?
* How does it fit into the rest of the BeeWare ecosystem? Is this project the right place to document the idea? Or should we document a feature in another project, and link to that documentation?
* Is there a high-level concept that needs explanation before any specific instructions will make sense?
* Does the topic make sense for us to explain, or has someone else already covered it somewhere we can refer to it?

If you're unsure about any of this, don't worry! Submit your idea, and let us know in the initial discussion what you're unsure of, and we can help shape the ideas that you have into a form that will fit BeeWare's documentation.

### Contributing a feature proposal

{% macro content(template) %}{% include template %}{% endmacro %}
{% macro indented(template) %}{{ content(template)|indent }}{% endmacro %}

??? abstract "Proposing a new feature"

    {{ indented("feature_proposal.md") }}
