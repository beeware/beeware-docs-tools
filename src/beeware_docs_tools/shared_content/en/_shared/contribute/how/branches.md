Before you start working on your change, make sure you've created a branch. By default, when you clone your repository fork, you'll be checked out on your `main` branch. This is a direct copy of {{ formal_name }}'s `main` branch.

While you *can* submit a pull request from your `main` branch, it's preferable if you *don't* do this. If you submit a pull request that is *almost* right, the core team member who reviews your pull request may be able to make the necessary changes, rather than giving feedback asking for a minor change. However, if you submit your pull request from your `main` branch, reviewers are prevented from making modifications.

Working off your main branch also makes it difficult for *you* after you complete your first pull request. If you want to work on a second pull request, you will need to have a "clean" copy of the upstream project's main branch on which to base your second contribution; if you've made your first contribution from your `main` branch, you no longer have that clean version available.

Instead, you should make your changes on a *feature branch*. A feature branch has a simple name to identify the change that you've made. For example, if you're fixing a bug that causes build issues on Windows 11, you might create a feature branch `fix-win11-build`. If your bug relates to a specific issue that has been reported, it's also common to reference that issue number in the branch name (e.g., `fix-1234`).

To create a `fix-win11-build` feature branch, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ git switch -c fix-win11-build
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ git switch -c fix-win11-build
```

///

/// tab | Windows

```doscon
(.venv) C:\...>git switch -c fix-win11-build
```

///

{% endif %}
