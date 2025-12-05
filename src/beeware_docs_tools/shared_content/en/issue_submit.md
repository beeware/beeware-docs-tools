TODO: intro sentence

### Start with a discussion

Before submitting an issue on GitHub, start with a discussion to ask whether what you're experiencing is a actually a bug, or an issue with your setup or process. Unless you're seeing behavior that is directly contradicting documented behavior, it's likely worth asking a question before going straight to submitting a bug report. Questions can always be turned into issues.

### Developing a good bug report

A good bug report includes all information potentially related to the bug, as well as the smallest possible reproduction example.

The reproduction example should be as short and concise as possible while still exhibiting the bug. Providing a massive example makes it significantly more difficult to troubleshoot, especially if it relies on other libraries, or requires extensive knowledge of the expected behavior or internal logic of the example.

We need as much detail as you can possibly provide. This includes, but is definitely not limited to:

- Your operating system version to the micro version (for example, macOS 15.7.2).
- Your Python version to the micro version (for example, 3.14.1).
- How you installed Python; for example, did you download it from python.org, use Homebrew, TODO: finish
- The specific version of the BeeWare tools are you using (for example, Toga 0.5.3).
- Other relevant packages; you can include the results of running `python -m pip freeze`.
- Logs wherever possible; if the tool generates log files, provide the entire log file.
- A stacktrace, if available; in this case, provide the *entire* stacktrace, not only the error message or the last couple of lines. If it is referencing code or documentation, the line numbers must match the example provided.
- Anything else about your computer or network setup that may be having an effect on the issue; is your computer older or slower, or is it a work machine that may have restrictions in place? In terms of your network, is it slow, or are you behind a firewall?

Try to think outside the box. Include everything you can think of. If you give us more than we need, we can easily ignore what we don't need. We can't come up with something you've left out.

Quite often the process of developing a good bug report will reveal the source of the problem, because the act of creating the minimal example forces you to figure out exactly what is causing the issue, whether it's a bug in the code, or stemming from incorrect assumptions or API usage.

### Submitting the report

Navigate to the [{{ formal_name }} issues list](https://github.com/beeware/{{ project_name }}/issues), click the "New issue" button, and choose "Bug report" to begin the process.

**You must fill out *all the sections* in the issue template.** We provide the template as a prompt to help you provide the necessary information. Remember, you can (and should!) always provide more information than the template requires, but at the very minimum, we need all the information present in the template.

When including code, in the event that you can reproduce it with an existing example, such as the BeeWare tutorial, you can provide a link. Otherwise, provide the code in the report. It should be Markdown formatted; a codeblock needs three backticks (```) before and after it.

If you need to include a long block of text, you can make it collapsed content using the following syntax:

```markdown
<details>
<summary>Collapsed content title</summary>
Long block of text.
</details>
```

Once you've provided as much information as you can, click "Create" to submit the report.
