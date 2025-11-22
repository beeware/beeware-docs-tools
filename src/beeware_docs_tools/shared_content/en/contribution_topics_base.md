## What can I do?

There are many ways to contribute to {{ formal_name }}. You can choose the option that works best for you based on your areas of interest, and level of expertise.

### Triage a bug

If a bug report has no comments from anyone other than the original reporter, the issue needs to be triaged. Triaging a bug involves taking the information provided by the reporter, and trying to reproduce it. If you can't reproduce the problem, report what you have found as a comment on the ticket, and pick another ticket.

### Fix a bug

{{ formal_name }} tracks a list of [known issues]({% if config.extra.website %}https://github.com/search?q=org%3Abeeware%20is%3Aopen%20is%3Aissue%20label%3Abug&type=issues{% else %}https://github.com/beeware/{{ project_name }}/issues?q=is%3Aopen+is%3Aissue+label%3Abug{% endif %}). Any of these issues are candidates to be worked on. This list can be filtered by platform, so you can focus on issues that affect the platforms you're able to test on. There's also a filter for [good first issues]({% if config.extra.website %}https://github.com/search?q=org%3Abeeware+is%3Aopen+is%3Aissue+label%3Abug+label%3A%22good+first+issue%22&type=issues{% else %}https://github.com/beeware/{{ project_name }}/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22{% endif %}). These issues have been identified as problems that have a known cause, and we believe the fix *should* be relatively straightforward (although we might be wrong in our analysis).

If an issue is more than 6 months old, it's entirely possible that the issue has been resolved, so the first step is to verify that you can reproduce the problem. Use the information provided in the bug report to try and reproduce the problem. If you can't reproduce the problem, report what you have found as a comment on the ticket, and pick another ticket.

If you can reproduce the problem - try to fix it! Work out what combination of code is implementing the feature, and see if you can work out what isn't working correctly.

Even if you can't fix the problem, reporting anything you discover as a comment on the ticket is worthwhile. If you can find the source of the problem, but not the fix, that knowledge will often be enough for someone who knows more about a platform to solve the problem. A good reproduction case (a sample app that does nothing but reproduce the problem) can be a huge help.

### Review a pull request



### Add a new feature

Can you think of a feature that {{ formal_name }} should have? Propose a new API or feature, and provide a sample implementation. If you'd like some help coming up with an idea, the there is a list of [existing feature suggestions]({% if config.extra.website %}https://github.com/search?q=org%3Abeeware+is%3Aopen+is%3Aissue+label%3Aenhancement&type=issues{% else %}https://github.com/beeware/{{ project_name }}/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement{% endif %}) that you could try to implement.

### Contribute improvements to documentation

If you're looking for specific areas to improve, there are [issues tagged "documentation"]({% if config.extra.website %}https://github.com/search?q=org%3Abeeware+is%3Aopen+is%3Aissue+label%3Adocumentation&type=issues{% else %}https://github.com/beeware/{{ project_name }}/issues?q=is%3Aopen+is%3Aissue+label%3Adocumentation{% endif %}). However, you don't need to be constrained by these issues. If you can identify a gap in {{ formal_name }}'s documentation, or an improvement that can be made, make a proposal! Anything that improves the experience of the end user is a welcome change.

We've got a [documentation contribution guide][contribute-docs] to walk you through that process.

### Translate content



### Platform usage



### Build an application
