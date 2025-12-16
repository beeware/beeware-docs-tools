So you've got an idea about an improvement for {{ formal_name }} - how do you submit that idea for consideration?

### Do your research

The first step is to search the {{ formal_name }} issue tracker for existing [feature issues (issues tagged "enhancement")]({% if config.extra.website %}https://github.com/search?q=org%3Abeeware+is%3Aopen+is%3Aissue+label%3Aenhancement&type=issues{% else %}https://github.com/beeware/{{ project_name }}/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement{% endif %}), [documentation issues (issues tagged "documentation")]({% if config.extra.website %}https://github.com/search?q=org%3Abeeware+is%3Aopen+is%3Aissue+label%3Adocumentation&type=issues{% else %}https://github.com/beeware/{{ project_name }}/issues?q=is%3Aopen+is%3Aissue+label%3Adocumentation{% endif %}), or [Discussion threads](https://github.com/beeware/{{ project_name }}/discussions) to see if the idea has been suggested before. If it has, and you have new context or ideas to add, include them in the existing thread. If you would like assistance with your research, you can ask in the #dev channel on the [BeeWare Discord](https://beeware.org/bee/chat/). We may be able to point you in the direction of existing threads, provide context of which you may not be aware, or connect your idea to another idea that might not immediately seem related.

### Discuss the idea

If you don't find any existing references to your idea, start a [Discussion thread](https://github.com/beeware/{{ project_name }}/discussions). Provide a high-level description of the purpose and use case for your idea. Include any thoughts you have on what the feature would look like, if implemented, such as the general shape of an API, the visual appearance of a capability, or the document that would be added. If applicable, you should also include any research you have done on how your idea would manifest on different platforms.

Once the Discussion thread is opened, the BeeWare team and the rest of the community will respond. The core team will aim to provide at least an initial impression of your idea within two business days. If an idea is especially complex, a more detailed analysis might take up to a week. Events like holidays and conferences might cause those timelines to be slightly longer.

This is your opportunity to participate in a conversation about your idea. We may ask for more details or context. Other members of the community may also get involved in the discussion, providing other perspectives, suggestions or counter-proposals. The outcome of this discussion will determine the next steps.

It's important to understand that not all ideas will be accepted. The reason this process starts with a proposal is to avoid you putting in all the work, only to find out there is a reason your change won't be accepted.

This doesn't mean it wasn't a good idea! There may be technical reasons it can't be implemented. For example, we might reject an idea if:

* It would be difficult or impossible to implement reliably across all supported platforms; or
* It would be difficult to maintain, or maintenance would require access to technology or software that isn't widely available; or
* It serves a niche audience, but imposes significant overhead on other users.

If we determine that your idea isn't a good fit, it doesn't necessarily mean you should give up on it. While we may reject a *specific* idea, we may be a lot more amenable to adding a plugin interface or other extension point that would allow you to maintain the same feature as an external library. That way you can have the feature, but without the specific maintenance concerns or limitations of the feature becoming a constraint on the project itself.

### Convert to a formal feature request

Once the discussion has reached a consensus on the form of a feature, you can create a new [feature request issue](https://github.com/beeware/{{ project_name }}/issues/new/choose), in the {{ formal_name }} issue tracker, that summarizes the discussion, linking to the discussion for context.

You don't have to implement your feature proposal yourself; you can open an issue with the details of what you're proposing. However, simply posting the issue doesn't mean it's going to be implemented for you. You'll need to wait for it to potentially get picked up by someone else interested in the same feature, whether that means another community member or the core team; however this is not guaranteed to happen. If you want the guarantee implementation, you'll need to implement it yourself, or pay someone else to implement it for you.

{% block end_matter %}
{% endblock %}
