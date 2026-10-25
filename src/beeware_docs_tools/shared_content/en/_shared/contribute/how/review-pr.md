Everyone is welcome to review any contribution to the BeeWare project. There are some important considerations to be aware of before getting started.

### THINK before you review

Before engaging in a review, THINK. As reviewers, we should consider whether the response we're about to send is:

* True. Always strive to provide accurate suggestions and information.
* Helpful. We are providing guidance on how to improve the submission; this guidance should clearly identify the source of a problem or an unconsidered use case, and ideally provides a path forward for what would resolve or satisfy the concern.
* Inspiring. It is up to us to inspire the author to want to work through our requested changes.
* Necessary. The expectation is that the author will read everything we post; we must respect their time and effort by only posting when necessary.
* Kind. There are multiple ways to present the same feedback; we need to ensure we are choosing to be kind, supportive, and constructive with our words.

It is entirely possible to THINK, while also providing an effective review. The concepts discussed above to not preclude pointing out any issues you find with a PR. Contributors won't have the opportunity to improve their contribution if they are unaware of areas needing improvement. The important thing is to remain aware of *how* you are presenting this feedback. Try to depersonalize your review. Instead of, "You made a mistake," you can say, "This code could be improved." Review the code, not the author.

It's important to remember to provide positive feedback in addition to identifying the areas needing improvement. If, for example, the changes are especially helpful, do something particularly clever, or you are introduced to an API that you didn't know about, let the author know! Never underestimate the effect of pointing out something someone has done correctly or well, in the middle of a situation where everything else you've pointed out are issues that need to be resolved.

### What is ready for review

The simplest way to find open pull requests is to go to the project's pull requests page: https://github.com/beeware/{{project_name}}/pulls

You can use the GitHub Search functionality to find any open pull requests for a project.

For example:

* [All open PRs, with passing tests for {{formal_name}}](https://github.com/search?q=org%3Abeeware+repo%3A{{project_name}}+is%3Apr+state%3Aopen+status%3Asuccess+draft%3Afalse+review%3Arequired&type=pullrequests&s=created&o=asc)
* [All open PRs, with passing tests for all projects](https://github.com/search?q=org%3Abeeware+is%3Apr+state%3Aopen+status%3Asuccess+draft%3Afalse+review%3Arequired&type=pullrequests&s=created&o=asc)
* [All open PRs across BeeWare](https://github.com/search?o=asc&q=org%3Abeeware+is%3Apr+is%3Aopen+draft%3Afalse+-author%3A%40me+archived%3Afalse&s=created&type=pullrequests)

Note: Not all BeeWare repos have CI tests, and not all open PRs were created when PRs had tests.

### GitHub review suggestions

The GitHub review interface has a mechanism for change suggestions, in which you can provide the exact change you are suggesting as a replacement for the existing content. Keep in mind that, until they are accepted and committed, these suggested changes won't be run through pre-commit and the linting checks. Therefore, this feature should be used for smaller changes, as the larger the suggested change is, the more likely it is to introduce issues.
