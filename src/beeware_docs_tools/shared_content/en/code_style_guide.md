This guide includes information and guidelines for writing code for {{ formal_name }}.

### Code style

We follow [PEP8](https://peps.python.org/pep-0008/). Keep in mind, the most important part is [section 0: A Foolish Consistency is the Hobgoblin of Little Minds](https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds). There are situations where remaining consistent with PEP8 doesn't make sense, and it is important to understand that, when applicable, it is acceptable, and sometimes preferred, to write code that isn't in line with the rules listed. Knowing *when to be inconsistent* with those rules is as important as maintaining consistency in most situations.

In most cases, we use Ruff. When you commit your code, pre-commit will run its checks, including Ruff. This will autoformat your code to bring it in line with our standards. You can set up some IDEs to automatically run Ruff on save, which can help with the process.

We follow US spelling for API naming, variables, etc.

{% block code_style %}

{% endblock %}

### Things to avoid

We try to avoid `utils` modules as much as possible, with the understanding that sometimes they are unavoidable. The preferred alternative is to find somewhere for the feature elsewhere in the source code, instead of using a `utils` module.
