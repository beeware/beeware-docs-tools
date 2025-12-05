Now that you've committed all your changes, there are a number of important steps to the process of submitting your PR.

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

Once everything passes, you're ready to push to GitHub.

### Push your changes to GitHub and create your pull request

The first time you push to GitHub, you'll be provided a URL that takes you directly to the GitHub page to create a new pull request. Follow the URL and create your pull request.

The following shows an example of what to expect on `push`, with the URL highlighted.

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console {hl_lines="11"}
(.venv) $ git push origin fix-win11-build
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 24 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (8/8), 689 bytes | 689.00 KiB/s, done.
Total 8 (delta 4), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
remote:
remote: Create a pull request for 'fix-win11-build' on GitHub by visiting:
remote:      https://github.com/<your GitHub username>/{{ formal_name }}/pull/new/fix-win11-build
remote:
To https://github.com/<your GitHub username>/{{ formal_name }}.git
 * [new branch]      fix-win11-build -> fix-win11-build
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console {hl_lines="11"}
(.venv) $ git push origin fix-win11-build
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 24 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (8/8), 689 bytes | 689.00 KiB/s, done.
Total 8 (delta 4), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
remote:
remote: Create a pull request for 'fix-win11-build' on GitHub by visiting:
remote:      https://github.com/<your GitHub username>/{{ formal_name }}/pull/new/fix-win11-build
remote:
To https://github.com/<your GitHub username>/{{ formal_name }}.git
 * [new branch]      fix-win11-build -> fix-win11-build
```

///

/// tab | Windows

```doscon {hl_lines="11"}
(.venv) C:\...>git push origin fix-win11-build
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 24 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (8/8), 689 bytes | 689.00 KiB/s, done.
Total 8 (delta 4), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
remote:
remote: Create a pull request for 'fix-win11-build' on GitHub by visiting:
remote:      https://github.com/<your GitHub username>/{{ formal_name }}/pull/new/fix-win11-build
remote:
To https://github.com/<your GitHub username>/{{ formal_name }}.git
 * [new branch]      fix-win11-build -> fix-win11-build
```

///

{% endif %}

If you've previously pushed the current branch to GitHub, you won't receive the URL again. However, you have options.

- Navigate to the upstream repository, click on "Pull Requests" followed by "New pull request", choose your branch, and verify everything is as you expect it.
- Navigate to the upstream repository, locate the banner above the list of files that indicates the repo has "had recent pushes", and click the "Compare & pull request" button.
- Use the GitHub CLI `gh pr create` command, and fill out the prompts.
- Use the GitHub CLI `gh pr create --web` command to open a web browser to the PR creation page.

Any of these options will enable you to create your new pull request.

TODO: Explain `gh`

### Pull request content

A pull request title must be applicable, clear, and concise; avoid TODO: finish.

The PR description must clearly reflect the changes in the PR. A person who doesn't have any context should be able to read your description and understand why the change is being made.

If there are any reproduction cases, or any testing regimen that you used that are not already a part of the changes present in the PR, they must be explained and included in the PR. The explanation should include how to run them, and what to do to reproduce the desired outcome.

### Continuous integration

*Continuous integration*, or *CI*, is what we use to run automated checks on your pull request, for example, checking formatting, running the test suite, and verifying the documentation builds. There are any number of changes that can result in CI failures. Broadly speaking, we won't review a PR that isn't passing CI; if you push and CI fails, we won't begin your review until it is passing. If your changes result in a failure, it is your responsibility to look into the reason, and resolve the issue.

If you click on the failure link in your PR, it will take you to the log. The log often provides all the information you need to figure out what caused the failure. TODO: finish.

If you find yourself in a situation where you need help getting CI to pass, you need to leave a comment on the PR letting us know.

/// note | The `pre-commit` and `towncrier` checks

If either the `pre-commit` or `towncrier` checks fail, it will block most of the rest of the CI checks from running. You'll need to resolve the applicable issues before the full set of checks will run.

///

The process of submitting your PR is not done until it's passing CI, or you can provide an explanation for why it's not.

If you see a failure, and you're certain it's unrelated to your changes, add a comment to your PR to that effect, and we will look into it.

We have limited CI resources. It is important to understand that every time you push to the branch, CI will start. If you're going to make a large number of changes, queue them up locally, and submit them together. This will minimize the load on the CI system.
