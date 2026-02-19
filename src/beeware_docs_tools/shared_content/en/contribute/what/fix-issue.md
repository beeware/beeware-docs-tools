{{ formal_name }} tracks a list of [known issues]({% if config.extra.website %}https://github.com/search?q=org%3Abeeware%20is%3Aopen%20is%3Aissue%20label%3Abug&type=issues{% else %}https://github.com/beeware/{{ project_name }}/issues?q=is%3Aopen+is%3Aissue+label%3Abug{% endif %}). Any of these issues are candidates to be worked on.

This list can be filtered in various ways. For example, you can filter by platform, so you can focus on issues that affect the platforms you're able to test on; or you can filter by issue type, such as [documentation bugs]({% if config.extra.website %}https://github.com/search?q=org%3Abeeware+is%3Aopen+is%3Aissue+label%3Abug+label%3Adocumentation&type=issues{% else %}https://github.com/beeware/{{ project_name }}/issues?q=is%3Aopen%20is%3Aissue%20label%3Abug%20label%3Adocumentation{% endif %}). There's also a filter for [good first issues]({% if config.extra.website %}https://github.com/search?q=org%3Abeeware+is%3Aopen+is%3Aissue+label%3Abug+label%3A%22good+first+issue%22&type=issues{% else %}https://github.com/beeware/{{ project_name }}/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22{% endif %}) - these are issues that have been identified as problems that have a known cause, and we believe the fix *should* be relatively straightforward (although we might be wrong in our analysis).

If an issue is more than 6 months old, it's entirely possible that the issue has been resolved, so the first step is to verify that you can reproduce the problem. Use the information provided in the bug report to try and reproduce the problem. If you can't reproduce the problem, report what you have found as a comment on the issue, and pick another issue.

If you can reproduce the problem - try to fix it! Work out what combination of code is implementing the feature, and see if you can work out what isn't working correctly.

Even if you can't fix the problem, reporting anything you discover during the process as a comment on the issue is worthwhile. If you can find the source of the problem, but not the fix, that knowledge will often be enough for someone who knows more about a platform to solve the problem. If the issue doesn't already provide a good reproduction case (a small sample app that does nothing but reproduce the problem), providing one can be a huge help.

## Contributing an issue fix

/// details-abstract | Set up a development environment

{% include "contribute/how/dev-environment.md" %}

///

/// details-abstract | Work from a branch

{% include "contribute/how/branches.md" %}

///

/// details-abstract | Reproduce the issue

{% include "contribute/how/reproduce-issue.md" %}

///

**If fixing the issue requires changes to code:**

/// details-abstract | Write, run, and test code

{% include "contribute/how/write-code.md" %}

///

**If fixing the issue requires changes to documentation:**

/// details-abstract | Build documentation

{% include "contribute/how/build-docs.md" %}

///

/// details-abstract | Write documentation

{% include "contribute/how/write-docs.md" %}

///

**When you're ready to submit your contribution:**

/// details-abstract | Add a change note

{% include "contribute/how/change-note.md" %}

///

/// details-abstract | Submit a pull request

{% include "contribute/how/submit-pr.md" %}

///
