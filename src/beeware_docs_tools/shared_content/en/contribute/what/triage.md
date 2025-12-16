{{ formal_name }} regularly receives issue reports from users who are experiencing problems. When a new issue is reported, that report needs to be *triaged* - that is, we need someone to read the report, take the information provided by the reporter, and try to reproduce the problem being described.

Unfortunately, while issue reports are usually well-intentioned, they are often incomplete or confusing. The purpose of the triage process is to fill in the gaps of the original report. This means either generating enough detail so that we can confirm how the issue can be reproduced; or to confirm that the original reporter was mistaken in their report.

Triaging an issue does not mean you are expected to fix it. Depending on the issue, triage may not even involve writing code. You can triage an issue with very little knowledge of {{ formal_name }}, as you should be able to follow the steps included in the report, and reproduce the issue that has been described.

## Contributing issue triage

{% macro content(template) %}{% include template %}{% endmacro %}
{% macro indented(template) %}{{ content(template)|indent }}{% endmacro %}

??? abstract "Reproduce the issue"

    {{ indented("contribute/how/reproduce-issue.md") }}
