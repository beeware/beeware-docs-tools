This guide includes information and guidelines for writing code for {{ formal_name }}.

### Code style { #code-style }

BeeWare follows [PEP 8](https://peps.python.org/pep-0008/) in our codebase, except with the line length expanded from 79 to 88 characters. We use [Ruff](https://docs.astral.sh/ruff/) to enforce PEP 8 conventions where possible. When you commit your code, pre-commit will run checks, including Ruff. Where possible, this will autoformat your code to ensure it meets our formatting and style standards. You can set up some IDEs to automatically run Ruff on save, which can help with the process.

Keep in mind that the most important part of PEP 8 is [Section 0: A Foolish Consistency is the Hobgoblin of Little Minds](https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds). There are situations where remaining consistent with PEP 8 doesn't make sense, and it is important to understand that, when applicable, it is acceptable, and sometimes preferred, to write code that isn't in line with the rules listed. Knowing *when to be inconsistent* with those rules is as important as maintaining consistency in most situations.

One manifestation of this can be seen in naming conventions. BeeWare libraries frequently need to bridge to other languages. When building wrappers to other languages, it is desirable (and in some cases, required) to follow the naming conventions of the target language, rather than Python. For example, when calling or referencing Java code, functions should follow Java's preference of `mixedCase`, rather than the PEP 8 preference for `snake_case`.

We follow US spelling for API naming, variables, etc.

{% block code_style %}
{% endblock %}

There are also some BeeWare-specific additions to PEP 8:

#### Splitting long function calls { #split-long-function-calls }

When a function call with more than one argument cannot fit on a single line, place each argument on its own line with a trailing comma on the last argument. Ruff permits (and will suggest) a format of multiple arguments on one wrapped line:

```py
my_function(
    arg1, arg2, arg3
)
```

This style should not be used. Instead, spread arguments to one per line by adding a trailing comma on the last argument:

```py
my_function(
    arg1,
    arg2,
    arg3,
)
```

#### Splitting long strings { #split-long-strings }

When a string argument must be split across lines to satisfy line length requirements, wrap the concatenated string literals in parentheses so it is clear the string is a single argument. That is, we prefer:

```py
my_function(
    (
        "this is a very long string "
        "that is wrapped over two lines"
    ),
    second_argument,
)
```

over:

```py
my_function(
    "this is a very long string "
    "that is wrapped over two lines",
    second_argument,
)
```

### Things to avoid

We try to avoid `utils` modules as much as possible, with the understanding that sometimes they are unavoidable. The preferred alternative is to find somewhere for the feature elsewhere in the source code, instead of using a `utils` module.

As a general rule, we try to avoid or defer any expensive initialization code, in order to achieve faster app startup. For instance, modules in the toga-core package are "lazy loaded" — they're only imported once requested, rather than all up front. This speeds up startup, and only spends time on what the app is actually using.
