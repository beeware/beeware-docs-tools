{% if config.extra.website %}

Many BeeWare tools use [`towncrier`](https://pypi.org/project/towncrier/) to assist in building the release notes for each release. When you submit a pull request to one of the applicable tools, it will need to include a *change note* - this change note will become the entry in the release notes describing the change that has been made.

{% else %}

{{ formal_name }} uses [`towncrier`](https://pypi.org/project/towncrier/) to assist in building the release notes for each release. When you submit a pull request, it must include a *change note* - this change note will become the entry in the release notes describing the change that has been made.

{% endif %}

Every pull request must include at least one file in the `changes/` directory that provides a short description of the change implemented by the pull request. The change note should be in Markdown format, in a file that has name of the format `<id>.<fragment type>.md`. If the change you are proposing will fix a bug or implement a feature for which there is an existing issue number, the ID will be the number of that ticket. If the change has no corresponding issue, the PR number can be used as the ID. You won't know this PR number until you push the pull request, so the first CI pass will fail the `towncrier` check; add the change note and push a PR update and CI should then pass.

There are five fragment types:

- `feature`: The PR adds a new behavior or capability that wasn't previously possible (e.g., adding support for a new packaging format, or a new feature in an existing packaging format);
- `bugfix`: The PR fixes a bug in the existing implementation;
- `doc`: The PR is a significant improvement to documentation;
- `removal`; The PR represents a backwards incompatible change in the {{ formal_name }} API; or
- `misc`; A minor or administrative change (e.g., fixing a typo, a minor language clarification, or updating a dependency version) that doesn't need to be announced in the release notes.

This description in the change note should be a high level "marketing" summary of the change from the perspective of the user, not a deep technical description or implementation detail. It is distinct from a commit message - a commit message describes what has been done so that future developers can follow the reasoning for a change; the change note is a description for the benefit of users, who may not have knowledge of internals.

For example, if you fix a bug related to project naming, the commit message might read:

> Apply stronger regular expression check to disallow project names that begin with digits.

The corresponding change note would read something like:

> Project names can no longer begin with a number.

Some PRs will introduce multiple features and fix multiple bugs, or introduce multiple backwards incompatible changes. In that case, the PR may have multiple change note files. If you need to associate two fragment types with the same ID, you can append a numerical suffix. For example, if PR 789 added a feature described by ticket 123, closed a bug described by ticket 234, and also made two backwards incompatible changes, you might have 4 change note files:

- `123.feature.md`
- `234.bugfix.md`
- `789.removal.1.md`
- `789.removal.2.md`

For more information about `towncrier` and fragment types see [News Fragments](https://towncrier.readthedocs.io/en/stable/tutorial.html#creating-news-fragments). You can also see existing examples of news fragments in the `changes` directory of the {{ formal_name }} repository. If this folder is empty, it's likely because {{ formal_name }} has recently published a new release; change note files are deleted and combined to update the [release notes](https://github.com/beeware/{{ project_name }}/releases) with each release. You can look at that file to see the style of comment that is required; you can look at [recently merged PRs](https://github.com/beeware/{{ project_name }}/pulls?q=is%3Apr+is%3Amerged) to see how to format your change notes.
