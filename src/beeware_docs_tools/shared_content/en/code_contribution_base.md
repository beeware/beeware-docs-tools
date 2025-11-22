
Want to contribute a bug fix or new feature to {{ formal_name }}? This guide will help you set up a development environment so you can implement and test changes to {{ formal_name }}.

## Prerequisites  { #dev-environment-prereqs }

You'll need to install the following prerequisites.

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

{% block macos_prerequisites %}

{{ formal_name }} requires Python {{ min_python_version }}+. You will also need a method for managing virtual environments (such as `venv`).

You can verify the version of Python that you have installed by running:

```console
$ python3 --version
```

If you have more than one version of Python installed, you may need to replace `python3` with a specific version number (e.g., `python{{ recent_python_version }}`)

{% endblock %}

{% if not config.extra.macos_only %}

///

/// tab | Linux

{% block linux_prerequisites %}

{{ formal_name }} requires Python {{ min_python_version }}+. You will also need a method for managing virtual environments (such as `venv`).

You can verify the version of Python that you have installed by running:

```console
$ python3 --version
```

If you have more than one version of Python installed, you may need to replace `python3` with a specific version number (e.g., `python{{ recent_python_version }}`)

{% endblock %}

///

/// tab | Windows

{% block windows_prerequisites %}

{{ formal_name }} requires Python {{ min_python_version }}+. You will also need a method for managing virtual environments (such as `venv`).

You can verify the version of Python that you have installed by running:

```doscon
C:\...>py -3 --version
```

If you have more than one version of Python installed, you may need to replace the `-3` with a specific version number (e.g., `-python{{ recent_python_version }}`)

We recommend avoiding recently released version of Python (i.e., versions that have a ".0" or ".1" micro version number, like e.g., 3.14.0). This is because the tools needed to support Python on Windows often lag usually aren't available for recently released stable Python versions.

{% endblock %}

///

{% endif %}

## <nospell>tl;dr</nospell> - Quick start { #dev-environment-tldr }

Create your dev environment by running:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
$ git clone https://github.com/beeware/{{ project_name }}.git
$ cd {{ project_name }}
$ python3 -m venv .venv
$ . .venv/bin/activate
(.venv) $ python -m pip install -Ue . --group dev
(.venv) $ pre-commit install
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
$ git clone https://github.com/beeware/{{ project_name }}.git
$ cd {{ project_name }}
$ python3 -m venv .venv
$ . .venv/bin/activate
(.venv) $ python -m pip install -Ue . --group dev
(.venv) $ pre-commit install
```

///

/// tab | Windows

```doscon
C:\...>git clone https://github.com/beeware/{{ project_name }}.git
C:\...>cd {{ project_name }}
C:\...>py -3 -m venv .venv
C:\...>.venv\Scripts\activate
(.venv) C:\...>python -m pip install -Ue . --group dev
(.venv) C:\...>pre-commit install
```

///

{% endif %}

Invoke checks and tests by running:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ tox p
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ tox p
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox p
```

///

{% endif %}

## Set up your development environment  { #setup-dev-environment }

The recommended way of setting up your development environment for {{ formal_name }} is to use a [virtual environment](https://docs.python.org/3/library/venv.html), and then install the development version of {{ formal_name }} and its dependencies.

### Clone the {{ formal_name }} repository

Next, go to the [{{ formal_name }} page on GitHub](https://github.com/beeware/{{ project_name }}), and, if you haven't already, [fork the repository](https://github.com/beeware/{{ project_name }}/fork) into your own account. Next, click on the "<> Code" button on your fork. If you have the GitHub desktop application installed on your computer, you can select "Open with GitHub Desktop"; otherwise, copy the HTTPS URL provided, and use it to clone the repository to your computer using the command line:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

Fork the {{ formal_name }} repository, and then:

```console
$ git clone https://github.com/<your username>/{{ project_name }}.git
```

(substituting your GitHub username)

{% if not config.extra.macos_only %}

///

/// tab | Linux

Fork the {{ formal_name }} repository, and then:

```console
$ git clone https://github.com/<your username>/{{ project_name }}.git
```

(substituting your GitHub username)

///

/// tab | Windows

Fork the {{ formal_name }} repository, and then:

```doscon
C:\...>git clone https://github.com/<your username>/{{ project_name }}.git
```

(substituting your GitHub username)

///

{% endif %}

### Create a virtual environment

To set up a virtual environment, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
$ cd {{ project_name }}
$ python3 -m venv .venv
$ source .venv/bin/activate
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
$ cd {{ project_name }}
$ python3 -m venv .venv
$ source .venv/bin/activate
```

///

/// tab | Windows

```doscon
C:\...>cd {{ project_name }}
C:\...>py -3 -m venv .venv
C:\...>.venv\Scripts\activate
```

///

{% endif %}

Your prompt should now have a `(.venv)` prefix in front of it.

### Install {{ formal_name }}

Now that you have the source code, you can do an [editable install](https://setuptools.pypa.io/en/latest/userguide/development_mode.html) of {{ formal_name }} into your development environment. Run the following command:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ python -m pip install -Ue . --group dev
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ python -m pip install -Ue . --group dev
```

///

/// tab | Windows

```doscon
(.venv) C:\...>python -m pip install -Ue . --group dev
```

///

{% endif %}

### Enable pre-commit

{{ formal_name }} uses a tool called [pre-commit](https://pre-commit.com) to identify simple issues and standardize code formatting. It does this by installing a git hook that automatically runs a series of code linters prior to finalizing any git commit. To enable pre-commit, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

///

/// tab | Windows

```doscon
(.venv) C:\...>pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

///

{% endif %}

Now you are ready to start hacking on {{ formal_name }}!

## Running tests {% if not config.extra.hide_coverage %}and coverage{% endif %} { #run-test-suite }

{{ formal_name }} uses [`tox`](https://tox.wiki/en/latest/) to manage the testing process and [`pytest`](https://docs.pytest.org/en/latest) for its own test suite.

The default `tox` command includes running:

- pre-commit hooks
- `towncrier` release note check
- documentation linting
- test suite for available Python versions
{% if not config.extra.hide_coverage %}
- code coverage reporting
{% endif %}

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

As with the full test suite, and the core, this should report [100% test coverage][code-coverage].

{% endif %}

## Running test variations

### Run tests for multiple versions of Python

By default, many of the `tox` commands will attempt to run the test suite multiple times, once for each Python version supported by {{ formal_name }}. To do this, though, each of the Python versions must be installed on your machine and available to `tox`'s Python [discovery](https://virtualenv.pypa.io/en/latest/user_guide.html#python-discovery) process. In general, if a version of Python is available via `PATH`, then `tox` should be able to find and use it.

### Run only the test suite

If you're rapidly iterating on a new feature, you don't need to run the full test suite; you can run *just* the unit tests. To do this, run:

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

### Run a subset of tests { #test-subset }

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

You'll still get a coverage report when running a part of the test suite -but the coverage results will only report the lines of code that were executed by the specific tests you ran.

### Run the test suite for a specific Python version { #test-py-version }

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

### Run the test suite without coverage (fast)

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

## Code coverage

{{ formal_name }} maintains 100% branch coverage in its codebase. When you add or modify code in the project, you must add test code to ensure coverage of any changes you make.

However, {{ formal_name }} targets multiple platforms, as well as multiple versions of Python, so full coverage cannot be verified on a single platform and Python version. To accommodate this, several conditional coverage rules are defined in the `tool.coverage.coverage_conditional_plugin.rules` section of `pyproject.toml` (e.g., `no-cover-if-is-windows` can be used to flag a block of code that won't be executed when running the test suite on Windows). These rules are used to identify sections of code that are only covered on particular platforms or Python versions.

Of note, coverage reporting across Python versions can be a bit quirky. For instance, if coverage files are produced using one version of Python but coverage reporting is done on another, the report may include false positives for missed branches. Because of this, coverage reporting should always use the oldest version Python used to produce the coverage files.

### Understanding coverage results

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

### Coverage report for host platform and Python version

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

### Coverage report for host platform

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

### Coverage reporting in HTML

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

## Submitting a pull request { #pr-housekeeping }

Before you submit a pull request, there's a few bits of housekeeping to do.

### Submit from a feature branch, not your `main` branch

Before you start working on your change, make sure you've created a branch. By default, when you clone your repository fork, you'll be checked out on your `main` branch. This is a direct copy of {{ formal_name }}'s `main` branch.

While you *can* submit a pull request from your `main` branch, it's preferable if you *don't* do this. If you submit a pull request that is *almost* right, the core team member who reviews your pull request may be able to make the necessary changes, rather than giving feedback asking for a minor change. However, if you submit your pull request from your `main` branch, reviewers are prevented from making modifications.

Instead, you should make your changes on a *feature branch*. A feature branch has a simple name to identify the change that you've made. For example, if you've found a bug that causes a display problem on Windows 11, you might create a feature branch `fix-win11-display`. If your bug relates to a specific issue that has been reported, it's also common to reference that issue number in the branch name (e.g., `fix-1234`).

To create a `fix-win11-display` feature branch, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ git switch -c fix-win11-display
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ git switch -c fix-win11-display
```

///

/// tab | Windows

```doscon
(.venv) C:\...>git switch -c fix-win11-display
```

///

{% endif %}

Commit your changes to this branch, then push to GitHub and create a pull request.

### Working with pre-commit

When you commit any change, pre-commit will run automatically. If there are any issues found with the commit, this will cause your commit to fail. Where possible, pre-commit will make the changes needed to correct the problems it has found:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ git add some/interesting_file.py
(.venv) $ git commit -m "Minor change"
check toml...............................................................Passed
check yaml...............................................................Passed
check for case conflicts.................................................Passed
check docstring is first.................................................Passed
fix end of files.........................................................Passed
trim trailing whitespace.................................................Passed
ruff format..............................................................Failed
- hook id: ruff-format
- files were modified by this hook

1 file reformatted, 488 files left unchanged

ruff check...............................................................Passed
codespell................................................................Passed
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ git add some/interesting_file.py
(.venv) $ git commit -m "Minor change"
check toml...............................................................Passed
check yaml...............................................................Passed
check for case conflicts.................................................Passed
check docstring is first.................................................Passed
fix end of files.........................................................Passed
trim trailing whitespace.................................................Passed
ruff format..............................................................Failed
- hook id: ruff-format
- files were modified by this hook

1 file reformatted, 488 files left unchanged

ruff check...............................................................Passed
codespell................................................................Passed
```

///

/// tab | Windows

```doscon
(.venv) C:\...>git add some/interesting_file.py
(.venv) C:\...>git commit -m "Minor change"
check toml...............................................................Passed
check yaml...............................................................Passed
check for case conflicts.................................................Passed
check docstring is first.................................................Passed
fix end of files.........................................................Passed
trim trailing whitespace.................................................Passed
ruff format..............................................................Failed
- hook id: ruff-format
- files were modified by this hook

1 file reformatted, 488 files left unchanged

ruff check...............................................................Passed
codespell................................................................Passed
```

///

{% endif %}

You can then re-add any files that were modified as a result of the pre-commit checks, and re-commit the change.

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ git add some/interesting_file.py
(.venv) $ git commit -m "Minor change"
check toml...............................................................Passed
check yaml...............................................................Passed
check for case conflicts.................................................Passed
check docstring is first.................................................Passed
fix end of files.........................................................Passed
trim trailing whitespace.................................................Passed
ruff format..............................................................Passed
ruff check...............................................................Passed
codespell................................................................Passed
[bugfix e3e0f73] Minor change
1 file changed, 4 insertions(+), 2 deletions(-)
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ git add some/interesting_file.py
(.venv) $ git commit -m "Minor change"
check toml...............................................................Passed
check yaml...............................................................Passed
check for case conflicts.................................................Passed
check docstring is first.................................................Passed
fix end of files.........................................................Passed
trim trailing whitespace.................................................Passed
ruff format..............................................................Passed
ruff check...............................................................Passed
codespell................................................................Passed
[bugfix e3e0f73] Minor change
1 file changed, 4 insertions(+), 2 deletions(-)
```

///

/// tab | Windows

```doscon
(.venv) C:\...>git add some\interesting_file.py
(.venv) C:\...>git commit -m "Minor change"
check toml...............................................................Passed
check yaml...............................................................Passed
check for case conflicts.................................................Passed
check docstring is first.................................................Passed
fix end of files.........................................................Passed
trim trailing whitespace.................................................Passed
ruff format..............................................................Passed
ruff check...............................................................Passed
codespell................................................................Passed
```

///

{% endif %}

Once everything passes, you're ready for the next steps.

### Add change information for release notes

When you submit this change as a pull request, you need to add a *change note*. {{ formal_name }} uses [`towncrier`](https://pypi.org/project/towncrier/) to automate building the release notes for each release. Every pull request must include at least one file in the `changes/` directory that provides a short description of the change implemented by the pull request.

The change note should be in Markdown format, in a file that has name of the format `<id>.<fragment type>.md`. If the change you are proposing will fix a bug or implement a feature for which there is an existing issue number, the ID will be the number of that ticket. If the change has no corresponding issue, the PR number can be used as the ID. You won't know this PR number until you push the pull request, so the first CI pass will fail the `towncrier` check; add the change note and push a PR update and CI should then pass.

There are five allowed fragment types:

- `feature`: The PR adds a new behavior or capability that wasn't previously possible (e.g., adding support for a new packaging format, or a new feature in an existing packaging format);
- `bugfix`: The PR fixes a bug in the existing implementation;
- `doc`: The PR is an significant improvement to documentation;
- `removal`; The PR represents a backwards incompatible change in the {{ formal_name }} API; or
- `misc`; A minor or administrative change (e.g., fixing a typo, a minor language clarification, or updating a dependency version) that doesn't need to be announced in the release notes.

This description in the change note should be a high level summary of the change from the perspective of the user, not a deep technical description or implementation detail. It is distinct from a commit message - a commit message describes what has been done so that future developers can follow the reasoning for a change; the change note is a "user facing" description. For example, if you fix a bug related to project naming, the commit message might read:

> Disallow project names that begin with a number.

The corresponding change note would read something like:

> Project names can no longer begin with a number.

Some PRs will introduce multiple features and fix multiple bugs, or introduce multiple backwards incompatible changes. In that case, the PR may have multiple change note files. If you need to associate two fragment types with the same ID, you can append a numerical suffix. For example, if PR 789 added a feature described by ticket 123, closed a bug described by ticket 234, and also made two backwards incompatible changes, you might have 4 change note files:

- `123.feature.md`
- `234.bugfix.md`
- `789.removal.1.md`
- `789.removal.2.md`

For more information about `towncrier` and fragment types see [News Fragments](https://towncrier.readthedocs.io/en/stable/tutorial.html#creating-news-fragments). You can also see existing examples of news fragments in the `changes` directory of the {{ formal_name }} repository. If this folder is empty, it's likely because {{ formal_name }} has recently published a new release; change note files are deleted and combined to update the [release notes]() with each release. You can look at that file to see the style of comment that is required; you can look at [recently merged PRs](https://github.com/beeware/briefcase/pulls?q=is%3Apr+is%3Amerged) to see how to format your change notes.

### It's not just about writing tests!

Although we ensure that we test all of our code, the task isn't *just* about maintaining that level of testing. Part of the task is to audit the code as you go. You could write a comprehensive set of tests for a concrete life jacket... but a concrete life jacket would still be useless for the purpose it was intended!

As you develop tests, you should be checking that the core module is internally **consistent** as well. If you notice any method names that aren't internally consistent (e.g., something called `on_select` in one module, but called `on_selected` in another), or where the data isn't being handled consistently, flag it and bring it to our attention by raising a ticket. Or, if you're confident that you know what needs to be done, create a pull request that fixes the problem you've found.

### Waiting for feedback

Once you've written your code, test, and change note, you can submit your changes as a pull request. One of the core team will review your work, and give feedback. If any changes are requested, you can make those changes, and update your pull request; eventually, the pull request will be accepted and merged. Congratulations, you're a contributor to {{ formal_name }}!

## What next?

Rinse and repeat! If you've improved testing for one method, go back and do it again for *another* method! If you've implemented a new feature, implement *another* feature!

Most importantly - have fun!
