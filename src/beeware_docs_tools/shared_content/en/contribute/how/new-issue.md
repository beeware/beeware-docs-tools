Writing up a good issue or bug report can make all the difference in the ability to troubleshoot a problem. Here's how to submit a good bug report to {{ formal_name }}.

### Search for existing issues

Before submitting a new issue, search the index for existing issues that match your own. If there is an existing open issue that seems to match your problem, add a comment to that issue with any additional information about your experience. For example, if you're seeing the problem on a different Python version, or different operating system, that additional information can be helpful in determining the impact or cause of a problem.

If you find a *closed* issue that seems to match your problem, check how recently that issue was closed. If the issue was closed very recently, that likely means your bug has been fixed, and will be corrected in the next release. If the issue was closed more than 4 months ago, it's likely that what you're experiencing is a different problem - no matter how similar the error message might appear.

If you don't find an issue that matches what you are seeing, it might be appropriate to open a new issue.

### Start with a discussion

Before submitting an issue on GitHub, consider starting with a discussion to ask whether what you're experiencing is a actually a bug, or an issue with your setup or process. Unless you're seeing behavior that is directly contradicting documented behavior, it's likely worth asking a question before going straight to submitting a bug report. If it turns out you *have* found an issue, a discussion topic can be easily turned into an issue.

Starting a discussion can also help ensure you're reporting an issue in the best place. Although you might have experienced a problem while using {{ formal_name }}, the problem might be caused by a bug in a different project in the BeeWare ecosystem.

### Writing a good bug report

If a new issue *is* required, it's important to provide as much detail as possible. A good bug report includes all information potentially related to the bug, as well as the smallest possible reproduction example.

The reproduction example should be as short and concise as possible while still exhibiting the bug. Providing a massive example makes it significantly more difficult to troubleshoot, especially if it relies on other libraries, or requires extensive knowledge of the expected behavior or internal logic of the example.

We need as much detail as you can possibly provide. This includes, but is definitely not limited to:

- Your operating system version - down to the micro version (for example, macOS 15.7.2).
- Your Python version, also down to the micro version (for example, 3.14.1).
- How you installed Python. Did you download it from python.org? Did you use Homebrew? `uv`? `pyenv`? `conda`? Something else?
- The specific version of the BeeWare tools are you using (for example, Toga 0.5.3). If you're using a development version, what Git hash are you using? It's not enough to say "the current main branch", because that can change on a daily basis.
- The specific versions of other packages that must be installed to trigger the problem. You can include the results of running `python -m pip freeze` to provide this information.
- If a log file has been generated, the *entire* log file.
- If a stack trace has been generated, the *entire* stacktrace. Don't just provide the final error message - the full context of the stack trace is important. It's also best to provide this in *text* format, *not* as a screenshot.
- Anything else about your computer or network setup that may be having an effect on the issue. Is your computer older or slower? Is it a work machine that may have firewalls, virus checkers, or other restrictions in place? Is your network especially slow? Do you run your operating system with a unusual system defaults (such as a very large font or some other assistive technology enabled)?

Try to think outside the box, and include everything you can think of that might impact the problem you're experiencing. If you give us more than we need, we can easily ignore what we don't need. We can't come up with something you've left out.

#### A minimal example

The most important part of a bug report is a minimal reproduction case. It should be possible for a third party to read the instructions for your reproduction case, follow those instructions, and observe the same problem. This may mean providing a sample project that exhibits the problem - or, even better, using a pre-existing example (such as a tutorial or example project that is part of the existing code base).

Your full project **is not** a minimal reproduction case. A minimal reproduction case should contain no code that is not absolutely required to manufacture a problem. Be ruthless in composing your reproduction case - if a button isn't needed to manufacture the problem, don't include that button.

Quite often the process of developing this minimal reproduction case will reveal the source of the problem, because the act of creating the minimal example forces you to figure out exactly what is causing the issue, whether it's a bug in the code, or stemming from incorrect assumptions or API usage.

You should also be **explicit** in any reproduction instructions. Saying "Close the example app" could mean clicking the close button on the window, selecting "quit" from a menu, or typing Control-C in a terminal. Your report should leave no room for ambiguity in what needs to be done to reproduce the problem.

### Submitting the report

Navigate to the {% if config.extra.website %}project issues list{% else %}[{{ formal_name }} issues list](https://github.com/beeware/{{ project_name }}/issues){% endif %}, click the "New issue" button, and choose "Bug report" to begin the process.

**You must fill out *all the sections* in the issue template.** We provide the template as a prompt to help you provide the necessary information. Remember, you can (and should!) always provide more information than the template requires, but at the very minimum, we need all the information present in the template.

When including code, in the event that you can reproduce it with an existing example, such as the BeeWare tutorial, you can provide a link. Otherwise, provide the code in the report. It should be Markdown formatted; a codeblock needs three backticks (```) before and after it.

If you need to include a long block of text, you can make it collapsed content using the following syntax:

```html
<details>
<summary>Collapsed content title</summary>
Long block of text.
</details>
```

Once you've provided as much information as you can, click "Create" to submit the report.
