This guide includes information and guidelines for writing code for {{ formal_name }}.

### Code style

BeeWare follows [PEP 8](https://peps.python.org/pep-0008/) in our codebase, except with the line length expanded from 79 to 88 characters. We use [Ruff](https://docs.astral.sh/ruff/) to enforce PEP 8 conventions where possible. When you commit your code, pre-commit will run checks, including Ruff. Where possible, this will autoformat your code to ensure it meets our formatting and style standards. You can set up some IDEs to automatically run Ruff on save, which can help with the process.

Keep in mind that the most important part of PEP 8 is [Section 0: A Foolish Consistency is the Hobgoblin of Little Minds](https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds). There are situations where remaining consistent with PEP 8 doesn't make sense, and it is important to understand that, when applicable, it is acceptable, and sometimes preferred, to write code that isn't in line with the rules listed. Knowing *when to be inconsistent* with those rules is as important as maintaining consistency in most situations.

We follow US spelling for API naming, variables, etc.

{% block code_style %}
{% endblock %}

### Things to avoid

We try to avoid `utils` modules as much as possible, with the understanding that sometimes they are unavoidable. The preferred alternative is to find somewhere for the feature elsewhere in the source code, instead of using a `utils` module.

Declaring an abstract base class as inheriting from [`ABC`](https://docs.python.org/3/library/abc.html) (and decorating its abstract methods with `@abstractmethod`) checks and enforces that subclasses implement the necessary methods. However, this checking introduces a small (but nonzero) overhead at runtime. Therefore, we only follow this pattern for base classes intended to be subclassed by users. When writing base classes intended only for internal use, there's no need to inherit from `ABC`, and abstract methods should raise `NotImplementedError` instead of being decorated.
