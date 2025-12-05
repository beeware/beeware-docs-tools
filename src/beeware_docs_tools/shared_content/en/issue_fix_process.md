{{ formal_name }} tracks a list of [known issues]({% if config.extra.website %}https://github.com/search?q=org%3Abeeware%20is%3Aopen%20is%3Aissue%20label%3Abug&type=issues{% else %}https://github.com/beeware/{{ project_name }}/issues?q=is%3Aopen+is%3Aissue+label%3Abug{% endif %}). Any of these issues are candidates to be worked on. This list can be filtered in various ways, to help narrow down an option for you. You can filter by platform, so you can focus on issues that affect the platforms you're able to test on. There's also a filter for [good first issues]({% if config.extra.website %}https://github.com/search?q=org%3Abeeware+is%3Aopen+is%3Aissue+label%3Abug+label%3A%22good+first+issue%22&type=issues{% else %}https://github.com/beeware/{{ project_name }}/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22{% endif %}). These issues have been identified as problems that have a known cause, and we believe the fix *should* be relatively straightforward (although we might be wrong in our analysis).

If an issue is more than 6 months old, it's entirely possible that the issue has been resolved, so the first step is to verify that you can reproduce the problem. Use the information provided in the bug report to try and reproduce the problem. If you can't reproduce the problem, report what you have found as a comment on the ticket, and pick another ticket.

If you can reproduce the problem - try to fix it! Work out what combination of code is implementing the feature, and see if you can work out what isn't working correctly.

Even if you can't fix the problem, reporting anything you discover as a comment on the ticket is worthwhile. If you can find the source of the problem, but not the fix, that knowledge will often be enough for someone who knows more about a platform to solve the problem. A good reproduction case (a sample app that does nothing but reproduce the problem) can be a huge help.

## Contributing an issue fix

{% macro content(template) %}{% include template %}{% endmacro %}
{% macro indented(template) %}{{ content(template)|indent }}{% endmacro %}

TODO: blurb.

??? abstract "Set up a development environment"

    {{ indented("dev_environment.md") }}

??? abstract "Work from a branch"

    {{ indented("git_feature_branch.md") }}

??? abstract "Reproduce the issue"

    {{ indented("issue_reproduce.md") }}

??? abstract "Write, run, and test code"

    {{ indented("code_run_test.md") }}

??? abstract "Submit a pull request"

    {{ indented("pr_submit.md") }}

??? abstract "Add a change note"

    {{ indented("pr_change_note.md") }}
