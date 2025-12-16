
Fixing a bug or implementing a feature will require you to write some new code.

{% block front_matter %}
{% endblock %}

We have a [code style guide](../style/code-style-guide.md) that outlines our guidelines for writing code for BeeWare.

### Test-driven development

A good way to ensure your code is going to do what you expect it to, is to first write a test case to test for it. This test case should fail initially, as the code it is testing for is not yet present. You can then write the code changes needed to make the test pass, and know that what you've written is solving the problem you are expecting it to.

### Run your code

Once your code is written, you need to ensure it runs. You'll need to manually run your code to verify it is doing what you expect. If you haven't already, you'll want to write a test case for your changes; as mentioned above, this test should fail if your code is commented out or not present.

You'll add your test case to the test suite, so it can be run alongside the other tests. The next step is to run the test suite.

### Running tests {% if not config.extra.hide_coverage %}and coverage{% endif %} { #run-test-suite }

{{ formal_name }} uses [`tox`](https://tox.wiki/en/latest/) to manage the testing process and [`pytest`](https://docs.pytest.org/en/latest) for its own test suite.

The default `tox` command includes running:

- pre-commit hooks
- `towncrier` release note check
- documentation linting

{% block testing_tox_command %}

- test suite for available Python versions

{% if not config.extra.hide_coverage %}

- code coverage reporting

{% endif %}

{% endblock %}

This is essentially what is run by CI when you submit a pull request.

To run the full test suite, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ tox
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ tox
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox
```

///

{% endif %}

The full test suite can take a while to run. You can speed it up considerably by running `tox` in parallel, by running `tox p` (or `tox run-parallel`). When you run the test suite in parallel, you'll get less feedback on the progress of the test suite as it runs, but you'll still get a summary of any problems found at the end of the test run. You should get some output indicating that tests have been run. You may see `SKIPPED` tests, but shouldn't ever get any `FAIL` or `ERROR` test results. We run our full test suite before merging every patch. If that process discovers any problems, we don't merge the patch. If you do find a test error or failure, either there's something odd in your test environment, or you've found an edge case that we haven't seen before - either way, let us know!

{% if not config.extra.hide_coverage %}

In addition to the tests passing, this should report [100% test coverage][code-coverage].

{% endif %}

{% block testing_running_additional %}
{% endblock %}

### Running test variations

#### Run tests for multiple versions of Python

By default, many of the `tox` commands will attempt to run the test suite multiple times, once for each Python version supported by {{ formal_name }}. To do this, though, each of the Python versions must be installed on your machine and available to `tox`'s Python [discovery](https://virtualenv.pypa.io/en/latest/user_guide.html#python-discovery) process. In general, if a version of Python is available via `PATH`, then `tox` should be able to find and use it.

#### Run only the test suite

If you're rapidly iterating on a new feature, you don't need to run the full test suite; you can run *only* the unit tests. To do this, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ tox -e py
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ tox -e py
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox -e py
```

///

{% endif %}

#### Run a subset of tests { #test-subset }

By default, `tox` will run all tests in the unit test suite. When you're developing your new test, it may be helpful to run *just* that one test. To do this, you can pass in [any `pytest` specifier](https://docs.pytest.org/en/latest/how-to/usage.html#specifying-which-tests-to-run) as an argument to `tox`. These test paths are relative to the `briefcase` directory. For example, to run only the tests in a single file, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ tox -e py -- tests/path_to_test_file/test_some_test.py
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ tox -e py -- tests/path_to_test_file/test_some_test.py
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox -e py -- tests/path_to_test_file/test_some_test.py
```

///

{% endif %}

{% block testing_subset_additional %}
{% endblock %}

{% if not config.extra.hide_coverage %}

You'll still get a coverage report when running a part of the test suite - but the coverage results will only report the lines of code that were executed by the specific tests you ran.

{% endif %}

#### Run the test suite for a specific Python version { #test-py-version }

By default `tox -e py` will run using whatever interpreter resolves as `python` on your machine. If you have multiple Python versions installed, and want to test a specific Python version from the versions you have installed, you can specify a specific Python version to use. For example, to run the test suite on Python {{ min_python_version }}, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ tox -e py{{ min_python_version_tag }}
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ tox -e py{{ min_python_version_tag }}
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox -e py{{ min_python_version_tag }}
```

///

{% endif %}

A [subset of tests][test-subset] can be run by adding `--` and a test specification to the command line.

{% if not config.extra.hide_coverage %}

#### Run the test suite without coverage (fast)

By default, `tox` will run the pytest suite in single threaded mode. You can speed up the execution of the test suite by running the test suite in parallel. This mode does not produce coverage files due to complexities in capturing coverage within spawned processes. To run a single python version in "fast" mode, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ tox -e py-fast
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ tox -e py-fast
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox -e py-fast
```

///

{% endif %}

A [subset of tests][test-subset] can be run by adding `--` and a test specification to the command line; a [specific Python version][test-py-version] can be used by adding the version to the test target (e.g., `py{{ min_python_version_tag }}-fast` to run fast on Python {{ min_python_version }}).

### Code coverage

{{ formal_name }} maintains 100% branch coverage in its codebase. When you add or modify code in the project, you must add test code to ensure coverage of any changes you make.

However, {{ formal_name }} targets multiple platforms, as well as multiple versions of Python, so full coverage cannot be verified on a single platform and Python version. To accommodate this, several conditional coverage rules are defined in the `tool.coverage.coverage_conditional_plugin.rules` section of `pyproject.toml` (e.g., `no-cover-if-is-windows` can be used to flag a block of code that won't be executed when running the test suite on Windows). These rules are used to identify sections of code that are only covered on particular platforms or Python versions.

Of note, coverage reporting across Python versions can be a bit quirky. For instance, if coverage files are produced using one version of Python but coverage reporting is done on another, the report may include false positives for missed branches. Because of this, coverage reporting should always use the oldest version Python used to produce the coverage files.

#### Understanding coverage results

At the end of the coverage test output there should be a report of the coverage data that was gathered:

```console
Name    Stmts   Miss Branch BrPart   Cover   Missing
----------------------------------------------------
TOTAL    7540      0   1040      0  100.0%
```

This tells us that the test suite has executed every possible branching path in the code. This isn't a 100% guarantee that there are no bugs, but it does mean that we're exercising every line of code in the codebase.

If you make changes to the codebase, it's possible you'll introduce a gap in this coverage. When this happens, the coverage report will tell you which lines aren't being executed. For example, lets say we made a change to `some/interesting_file.py`, adding some new logic. The coverage report might look something like:

```console
Name                                 Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------------------
src/some/interesting_file.py           111      1     26      0  98.1%   170, 302-307, 320->335
--------------------------------------------------------------------------------
TOTAL                                 7540      1   1726      0  99.9%
```

This tells us that line 170, lines 302-307, and a branch jumping from line 320 to line 335, are not being executed by the test suite. You'll need to add new tests (or modify an existing test) to restore this coverage.

#### Coverage report for host platform and Python version

You can generate a coverage report for your platform and version of Python. For example, to run the test suite and generate a coverage report on Python {{ min_python_version }}, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ tox -m test{{ min_python_version_tag }}
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ tox -m test{{ min_python_version_tag }}
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox -m test{{ min_python_version_tag }}
```

///

{% endif %}

#### Coverage report for host platform

If all supported versions of Python are available to `tox`, then coverage for the host platform can be reported by running:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ tox p -m test-platform
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ tox p -m test-platform
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox p -m test-platform
```

///

{% endif %}

#### Coverage reporting in HTML

A HTML coverage report can be generated by appending `-html` to any of the coverage `tox` environment names, for instance:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ tox -e coverage-platform-html
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ tox -e coverage-platform-html
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox -e coverage-platform-html
```

///

{% endif %}

{% endif %}

{% block testing_additional %}
{% endblock %}

### It's not just about writing tests!

Although we ensure that we test all of our code, the task isn't *just* about maintaining that level of testing. Part of the task is to audit the code as you go. You could write a comprehensive set of tests for a concrete life jacket... but a concrete life jacket would still be useless for the purpose it was intended!

As you develop tests, you should be checking that the core module is internally **consistent** as well. If you notice any method names that aren't internally consistent (e.g., something called `on_select` in one module, but called `on_selected` in another), or where the data isn't being handled consistently, flag it and bring it to our attention by raising a ticket. Or, if you're confident that you know what needs to be done, create a pull request that fixes the problem you've found.

{% block end_matter %}
{% endblock %}
