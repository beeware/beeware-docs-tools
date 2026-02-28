Now that you've committed all your changes, you're ready to submit a pull request. To ensure you have a smooth review process, there are a number of steps you should take.

### Working with pre-commit

When you commit any change, pre-commit will run automatically. If there are any issues found with the commit, this will cause your commit to fail. Where possible, pre-commit will make the changes needed to correct the problems it has found. In the following example, a code formatting issue was found by the `ruff` check:

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

In this case, `ruff` automatically fixed the problem; so you can then re-add any files that were modified as a result of the pre-commit checks, and re-commit the change. However, some checks will require you to make manual modifications. Once you've made those changes, re-add any modified files, and re-commit.

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
[bugfix e3e0f73] Minor change
1 file changed, 4 insertions(+), 2 deletions(-)
```

///

{% endif %}

Once everything passes, you'll see a message indicating the commit has been finalized, and your git log will show your commit as the most recent addition. You're now ready to push to GitHub.

### Push your changes to GitHub and create your pull request

The first time you push to GitHub, you'll be provided a URL that takes you directly to the GitHub page to create a new pull request. Follow the URL and create your pull request.

The following shows an example of what to expect on `push`, with the URL highlighted.

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console {hl_lines="11"}
(.venv) $ git push
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
(.venv) $ git push
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
(.venv) C:\...>git push
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

If you've previously pushed the current branch to GitHub, you won't receive the URL again. However, there are other ways to get to the PR creation URL:

- Navigate to the upstream repository, click on "Pull Requests" followed by "New pull request", and choose the from which you want to submit your pull request.
- If you pushed recently, navigate to the upstream repository, locate the banner above the list of files that indicates the repo has "had recent pushes", and click the "Compare & pull request" button.
- Use the GitHub CLI `gh pr create` command, and fill out the prompts.
- Use the GitHub CLI `gh pr create --web` command to open a web browser to the PR creation page.

Any of these options will enable you to create your new pull request.

/// info | The GitHub CLI: `gh`

GitHub provides the [GitHub CLI](https://cli.github.com/), which gives you access to many of the features of GitHub from your terminal, through the `gh` command. The [GitHub CLI documentation](https://cli.github.com/manual/) covers all the features.

///

### Pull request content

A pull request title must be informative, clear, and concise. Try to keep it short if possible, but longer titles are acceptable, if needed. A good PR title should give a person without any context a reasonably solid idea of what bug or feature is implemented by your PR.

The PR description must clearly reflect the changes in the PR. A person without any context should be able to read your description, and gain a relatively complete understanding of why the change is being made. Avoid jokes, idioms, colloquialisms, and unnecessary formatting, such as using all caps or excessive punctuation; this is meant to be a straightforward explanation of what is happening in your PR, and avoiding those things makes the description more accessible to others.

If there are any reproduction cases, or any testing regimen that you used that are not already a part of the changes present in the PR, they should be explained and included in the PR. The explanation should include how to run them, and what to do to reproduce the desired outcome.

If your pull request will resolve issue #1234, you should include the text `Fixes #1234` in your pull request description. This will cause the issue to be automatically closed when the pull request is merged. You can refer to other discussions, issues or pull requests using the same `#1234` syntax. You can refer to an issue on a different repository by prefixing the number with - for example `python/cpython#1234` would refer to issue 1234 on the CPython repository.

### Continuous integration

*Continuous integration*, or *CI*, is the process of running automated checks on your pull request. This can include simple checks like ensuring code is correctly formatted; but it also includes running the test suite, and building documentation.

There are any number of changes that can result in CI failures. Broadly speaking, we won't review a PR that isn't passing CI. If you create a pull requests and CI fails, we won't begin your review until it is passing. If your changes result in a failure, it is your responsibility to look into the reason, and resolve the issue.

When CI fails, the failure links will show up at the bottom of the PR page, under the heading "Some checks were not successful". You'll see a list of failed checks, which, will show up at the top of the list of all checks if there are passing checks as well. If you click on the failure link, it will take you to the log. The log often provides all the information you need to figure out what caused the failure. Read through the log and try to figure out why the failure is occurring, and then do what's necessary to resolve it.

Occasionally, a CI check will fail for reasons that are unrelated to your changes. This could be due to an issue on the machine that runs the CI check; or because a CI check is unstable. If you see a failure, and you're fairly certain it's unrelated to your changes, add a comment to your PR to that effect, and we will look into it.

To trigger a new CI run, you need to push new changes to your branch.

If you find yourself in a situation where you need help getting CI to pass, leave a comment on the PR letting us know and we'll do what we can to help.

/// note | The `pre-commit` and `towncrier` checks

If either the `pre-commit` or `towncrier` checks fail, it will block most of the rest of the CI checks from running. You'll need to resolve the applicable issues before the full set of checks will run.

///

We have limited CI resources. It is important to understand that every time you push to the branch, CI will start. If you're going to make a number of changes, it's better to make those changes locally, push them all at once. CI will only run on the most recent commit in a batch, minimizing the load on our CI system.

The process of submitting your PR is not done until it's passing CI, or you can provide an explanation for why it's not.

{% block end_matter %}
{% endblock %}
