Your pull request has been submitted, and passing CI. It is now ready to be reviewed.

## <nospell>tl;dr</nospell> - The review process

The short version of the review process:

1. Wait for a review.
2. Respond to feedback.
3. If changes are requested:
   * Work through completing requested changes.
   * Submit all requested changes.
   * Re-request a review when all requested changes have been submitted.
   * Repeat section three until no further changes are needed.
4. Wait for your pull request to be approved and merged.

Congratulations! You've just made a contribution to {{ formal_name }}!

## I submitted my pull request, what's next?

After submitting your pull request, you'll need to wait for a review of your contribution. There are two sides to the review process: providing a review and receiving a review.

/// info | Review expectations

You should expect anyone reviewing your submissions to follow these guidelines, including reviews from members of the core team. You should also follow these guidelines when you are reviewing submissions from others.

If you feel your reviewer is straying from these expectations, and you feel comfortable raising the issue yourself on the pull request, you can do so. If you don't feel comfortable, please reach out to the [BeeWare Code of Conduct Response Team](https://beeware.org/bee/coc). We will review your report, and follow up with your reviewer. The follow-up will reflect the reported action; a minor transgression may result in a discussion, whereas a major violation may result in something more serious.

///

## Providing a review

Everyone is welcome to provide a review on any pull request. [These guidelines](../how/review-pr.md) describe our expectations of a review, regardless of whether it's provided by a core team member or a member of the community.

A core team member will always need to provide the final review; but reviews from community members can be a helpful way to streamline the process - ideally, the review from the core team would be a formality after community reviews have identified all the major problems.

## Receiving a review

Receiving a review involves three basic steps:

1. Initial feedback and questions.
2. Change requests.
3. Approval and merge.

Each step is detailed below. If at any point during the process you have questions, don't hesitate to ask! We are happy to help.

### Timeline and initial feedback

The core team aims to ensure that every pull requests receives a review within ten business days. However, with more complicated submissions, or when a pull request is submitted when parts of the team are on leave, that timeline may be extended.

We typically maintain continuity with reviewers on each pull request - that is, you'll likely work with the same reviewer for your entire review. This means your reviewer will have context throughout the process, and you'll be able to learn what to expect in terms of response cadence and review style. If your initial reviewer identifies that they don't have the necessary expertise to review your pull requests, or they know that will be unavailable for some reason, they may pass responsibility for your pull request to another team member.

You can expect us to respond to each exchange within a rolling ten business day time frame. Responding to feedback and questions is an essential part of the review process. We will expect a response from you before we move to the next step in the process.

### Change requests

Most of the time, your reviewer is going to request changes on your pull request. This isn't necessarily a reflection of your work, it's simply part of the process.

If the initial review reveals a significant number of problems, the first review may not be comprehensive. Instead, it will focus on providing high level direction on the work required to get the pull request into a mergeable state. The review process may include questions to clarify the purpose and scope of the work that has been attempted.

#### Work through requested changes

Your reviewer will post comments to your pull request. These comments can be general, on a specific file, or on a specific line or lines of code. They will sometimes include directly suggested changes that you can apply to your pull request through the GitHub UI. Typically, they will be questions, requests for clarification, or guidance on updates.

/// info | Marking a conversation as resolved

During the discussion part of the feedback process, you should never mark a conversation started by your reviewer as "resolved". Marking the conversation as resolved is the responsibility of the reviewer. It's up to them to determine whether the identified problem has been solved.

///

If the review reveals a systematic problem (e.g., a naming inconsistency that exists in the code), the reviewer may not highlight every instance of that problem. Instead, they may pick a couple of examples of the problem, and indicate that other instances should also be corrected. If a review highlights a problem in once place, and you think it might apply elsewhere, you should fix that problem wherever it occurs. If you're unsure, ask for clarification from your reviewer.

#### Submit all requested changes

Once you've worked through all the requested changes, you can push an update to your pull request. This will trigger a new CI run; once you have confirmed that CI is still passing, post a comment requesting an updated review and the core team will take another look at your pull request.

/// info | Push, don't force or rebase

When you're updating your pull request during a review, it is important to leave the commit history intact. It doesn't matter if there's a huge list of commits; they are all squashed when we merge the pull request. If you force push or rebase your pull request in the middle of a review, you may be removing important context needed by your reviewer.

///

#### Re-request a review

Once you have resolved all the requested changes in a given review, and CI is passing again, you can re-request a review from your reviewer. If an issue is particularly complicated, and fixing one will impact another thing, you can ask for a review on the specific piece you've updated. The assumption will be that any request for a review is a request for a *full* review. If you're not ready for a full review, be sure to specify exactly what you're looking for.

### Pull request approval and merge

Once you've responded to all the change requests are completed, the pull request will be approved. In most cases, once a pull request is approved, we will immediately merge it. In some cases, there may be extenuating circumstances, such as relying on another not-yet-merged pull request, that will lead to a delay. We'll communicate this in the comments, so you'll know the situation.
