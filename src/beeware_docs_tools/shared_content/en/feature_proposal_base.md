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

## The proposal process

So you've got an idea about an improvement for {{ formal_name }} - how do you submit that idea for consideration?

### Do your research

The first step is to search the {{ formal_name }} issue tracker for existing [feature issues (issues tagged "enhancement")](https://github.com/beeware/{{ project_name }}/issues?q=is%3Aissue%20state%3Aopen%20label%3Aenhancement), [documentation issues (issues tagged "documentation")](https://github.com/beeware/{{ project_name }}/issues?q=is%3Aissue%20state%3Aopen%20label%3Adocumentation), or [Discussion threads](https://github.com/beeware/{{ project_name }}/discussions) to see if the idea has been suggested before. If it has, and you have new context or ideas to add, include them in the existing thread. If you would like assistance with your research, you can optionally ask in the #dev channel on the [BeeWare Discord](https://beeware.org/bee/chat/). We may be able to point you in the direction of existing threads, provide context of which you may not be aware, or connect your idea to a separate idea that might not be immediately obvious.

### Discuss the idea

If you don't find any existing references to your idea, start a [Discussion thread](https://github.com/beeware/{{ project_name }}/discussions). Provide a high-level description of the purpose and use case for your idea. Include any thoughts you have on what the feature would look like, if implemented, such as the general shape of an API, or the visual appearance of the feature. If applicable, you should also include any research you have done on how your idea would manifest on different platforms.

Once the Discussion thread is opened, the team will respond. We will aim to provide at least an initial impression within one business day. If an idea is especially complex, a more detailed analysis might take up to a week. Events like holidays and conferences might cause those timelines to be slightly longer.

This is your opportunity to participate in a conversation about your idea. We may ask for more details or context. Other members of the community may also get involved in the discussion, providing other perspectives, suggestions or counter-proposals. The outcome of this discussion will determine the next steps.

It's important to understand that not all ideas will be accepted. The reason this process starts with a proposal is to avoid you putting in all the work, only to find out there is a reason your change won't be accepted.

This doesn't mean it wasn't a good idea! There may be technical reasons it can't be implemented. For example, we might reject an idea if:

* It would be difficult or impossible to implement reliably across all supported platforms; or
* It would be difficult to maintain, or maintenance would require access to technology or software that isn't widely available; or
* It serves a niche audience, but imposes significant overhead on other users.

If we determine that your idea isn't a good fit, it doesn't necessarily mean you should give up on it. While we may reject a *specific* idea, we may be a lot more amenable to adding a plugin interface or other extension point that would allow you to maintain the same feature as an external library. That way you can have the feature, but without the specific maintenance concerns or limitations of the feature becoming a constraint on the project itself.

### Convert to a formal feature request

Once the discussion has reached a consensus on the form of a feature, you can create a new [feature request issue](https://github.com/beeware/{{ project_name }}/issues/new/choose), in the {{ formal_name }} issue tracker, that summarizes the discussion, linking to the discussion for context.

## Implement your idea

You can now start implementing your idea. If your suggestion involves code, you can use [this guide][contribute-code] to walk you through the process of contributing code to {{ formal_name }}. If your suggestion involves documentation, you can use [this guide][contribute-docs] instead.
