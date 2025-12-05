The first step following an initial issue report is to triage the issue.

If a issue report has no comments from anyone other than the original reporter, the issue needs to be triaged. Triaging an issue involves taking the information provided by the reporter, and trying to reproduce it.

The fact of the matter is, bug reports are usually well-intentioned, but often incomplete. Triaging may involve asking for more information about how the problem was actually happening in the first place.

Triaging an issue does not mean you are expected to fix it. You can triage an issue with very little knowledge of {{ formal_name }}, as you should be able to follow the steps included in the report, and reproduce the issue.

If you are able to reproduce it, leave a comment on the ticket letting us know.

If you can't reproduce the problem, that information is still incredibly helpful. Report what you have found as a comment on the ticket, and pick another ticket.

Bug reports are often well-intentioned but incoherent or incomplete. If it comes to I tried to reproduce it, and couldn't. This is useful triage information.

Triage can be prompting the question to ask for more information about how the problem was actually happening in the first place.

## Contributing triaging an issue

{% macro content(template) %}{% include template %}{% endmacro %}
{% macro indented(template) %}{{ content(template)|indent }}{% endmacro %}

TODO: blurb.

??? abstract "Triage the issue"

    {{ indented("issue_reproduce.md") }}
