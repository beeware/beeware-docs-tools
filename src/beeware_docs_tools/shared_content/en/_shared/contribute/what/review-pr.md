We're always happy to have reviews from contributors, regardless of their experience level.

### Why review contributions?

Every contribution that is submitted needs to be reviewed, regardless of whether it was submitted by a core team member or a first-time contributor. Everyone has the potential to miss something. The review process is in place to provide an extra safety net.

The purpose of the review process is to ensure all content, including code and documentation, is as bug-free and easy-to-maintain as possible. Anything you can do to further that goal is a welcome contribution. This could range from something as simple as correcting a typo, to finding edge cases in the API usage that aren't being caught. You could identify ways the testing regimen could be more robust, or make a suggestion of ways to structure the overall architecture of the changes so that they are easier to maintain or extend.

### Can I review?

Yes! You can offer a review on any pull request you see open on {{ formal_name }}.

As a first-time contributor, you should feel free to review any pull request you find, even if it was submitted by a core team member. If you're a novice, you might be missing some larger project context; but we aim to keep the codebase approachable regardless of your level of experience. If there's something in the code that doesn't make sense, that might indicate there's a need for more documentation (either in the code, or as standalone design documentation).


### What is ready for review

The simplest way to find open pull requests is to go to the project's pull requests page: https://github.com/beeware/{{project_name}}/pulls

You can use the GitHub Search functionality to find any open pull requests for a project.

For example:

* [All open PRs, with passing tests for {{formal_name}}](https://github.com/search?q=org%3Abeeware+repo%3A{{project_name}}+is%3Apr+state%3Aopen+status%3Asuccess+draft%3Afalse+review%3Arequired&type=pullrequests&s=created&o=asc)
* [All open PRs, with passing tests for all projects](https://github.com/search?q=org%3Abeeware+is%3Apr+state%3Aopen+status%3Asuccess+draft%3Afalse+review%3Arequired&type=pullrequests&s=created&o=asc)
* [All open PRs across BeeWare](https://github.com/search?o=asc&q=org%3Abeeware+is%3Apr+is%3Aopen+draft%3Afalse+-author%3A%40me+archived%3Afalse&s=created&type=pullrequests)

Note: Not all BeeWare repos have CI tests, and not all open PRs were created when PRs had tests.

## Contributing a pull request review

/// details-abstract | Providing a pull request review

{% include "how/review-pr.md" %}

///
