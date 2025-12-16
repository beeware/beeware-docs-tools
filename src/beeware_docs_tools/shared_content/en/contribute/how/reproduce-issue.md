You can't fix a problem if you don't have the problem in the first place. Therefore, reproducing the issue is a prerequisite to fixing it. In software, problems are commonly referred to as ["bugs"](https://en.wikipedia.org/wiki/Software_bug), and issues are often called "bug reports".

Someone has provided a bug report. You need to validate that the steps the reporter describes are resulting in the bug being reported. Can you reproduce the same result by doing exactly what was described in the report? If you can't, you need to figure out why.

{% block front_matter %}
{% endblock %}

### Bugs in code

In an ideal situation, you will have the same setup as the person who reported the bug, you will follow the steps, and you will be able to reproduce the bug as described. In many cases, though, it won't be so straightforward. Many bug reports include only vague explanations, and a vague set of conditions. The problem is that many bugs vary based on the set of conditions involved, including how they're interacted with, various preconditions, operating system, operating system version, CPU architecture, or whether the user's machine is old and slow or new and fast. The more information we have about the situation surrounding the bug, the better. Try and reproduce the set of conditions that the reporter has provided. If you're unable to do so, your next step may need to be requesting more information from the person who reported the bug.

The best way to reproduce a bug is with the smallest possible example that still exhibits the issue. Most of the time reporters will not provide a minimum viable example; if they provide *any* example at all, it will be copied directly from their "real world" application. Your aim will be to reduce the report down to the simplest possible form that exhibits the issue. The best reproduction case is the smallest possible program. This reduction is itself helpful because it determines what the actual problem is. Anyone can take the minimal example, run it, and they will observe the bug that is described.

### Bugs in documentation

Bugs in documentation can manifest in different ways. There are problems with formatting that result in rendering issues. Sometimes it's not even a bug; the person may have misread the documentation, or made a genuine mistake. This doesn't necessarily mean there isn't an issue with the documentation. The content may be unclear or imprecise, leaving room for confusion or misinterpretation. It's possible that a concept that should be discussed isn't, because it is completely undocumented.

When a bug is filed for a documentation issue, you'll want to verify that the issue reported actually still exists. In the case of rendering issues, you'll need to build the documentation to see if you can reproduce the issue. Content issues are a matter of reading to verify that no one has submitted an update.

### Update the issue

The final step in the triage process is to document your findings by leaving a comment on the issue.

If you're able to reproduce the issue exactly as described, that's all you need to say. Leave a comment saying that you've confirmed that you're seeing the same problem, in the exact way the original reporter describes.

If you're able to provide any additional context, then include details of that context. This might include being able to reproduce the problem on a different operating system, or with a different version of some of the software involved, or anything else that varies from the original report.

If the original report was missing details that you needed to reproduce the report, include *those* details. This might include providing operating system or version details that the original report didn't make, more complete logs or stack traces, or clearer instructions on the exact sequence of operations needed to reproduce the problem. If you've developed a simpler way to reproduce the problem (or the original reporter didn't provide a reproduction case), you can include details of that reproduction methodology.

If you *can't* reproduce the issue, then you also leave a comment, detailing what you tried. Knowing where a problem *doesn't* exist is almost as important as knowing where it *does* exist, because that helps to narrow down a possible cause. If you have an theories about *why* you can't reproduce the problem - for example, if you think it's an error of usage, or that the problem has been resolved by a recent operating system update - include that speculation as part of your comment.

Lastly, you can provide any recommendations you may have to the core team. If you think the original report is in error, suggest that the issue should be closed; if you have a theory about the cause of the issue, you can suggest that as well. Your comments will help the core team work out how to progress the issue to the next step.

{% block end_matter %}
{% endblock %}
