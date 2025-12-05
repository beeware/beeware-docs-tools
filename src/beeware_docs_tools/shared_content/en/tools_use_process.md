TODO: finish?

One of the most valuable pieces of feedback we can get is from people trying to use the BeeWare tools, and discovering there is a point of friction or a missing feature. It's incredibly useful to us to understand any difficulties you might experience when using the tools for real-world purposes.

Think of the thing you've always wanted to build, and try building it. You may not be successful, and letting us know why is extremely helpful. Was there a missing feature? Is the documentation confusing or lacking in some aspect? You sharing facing a complexity we haven't considered helps us improve the experience for everyone.

If it turns out you are able to build your project, congratulations! You have the thing you always wanted.

If you do experience any problems, start a discussion. It may be the start of a new issue or feature proposal.

### Contributing tool usage

{% macro content(template) %}{% include template %}{% endmacro %}
{% macro indented(template) %}{{ content(template)|indent }}{% endmacro %}

??? abstract "Submit a new issue"

    {{ indented("issue_submit.md") }}

??? abstract "Propose a new feature"

    {{ indented("feature_proposal.md") }}
