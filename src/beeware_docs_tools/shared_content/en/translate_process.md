We want to provide our documentation in as many languages as possible, because availability of information in one's native language is an accessibility issue. The BeeWare core team is, for the most part, monolingual. We need your help to translate our content into other languages.

We use Weblate for all of our translation management. Weblate is a tool that lets us treat every untranslated string as a to-do list that we can work through, one at a time.

We use [DeepL](https://www.deepl.com/en/translator) for machine translation to produce a first pass at translations. The expectation is that these will be edited, reviewed, and improved as necessary.

TODO: More?

### Contributing translations

{% macro content(template) %}{% include template %}{% endmacro %}
{% macro indented(template) %}{{ content(template)|indent }}{% endmacro %}

??? abstract "Translate content"

    {{ indented("translate.md") }}
