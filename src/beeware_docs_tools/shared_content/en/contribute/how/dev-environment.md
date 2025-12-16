Contributing to {{ formal_name }} requires you to set up a development environment.

### Prerequisites  { #dev-environment-prereqs }

You'll need to install the following prerequisites.

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

{{ formal_name }} requires Python {{ min_python_version }}+. You will also need a method for managing virtual environments (such as `venv`).

You can verify the version of Python that you have installed by running:

```console
$ python3 --version
```

If you have more than one version of Python installed, you may need to replace `python3` with a specific version number (e.g., `python{{ recent_python_version }}`)

We recommend avoiding recently released version of Python (i.e., versions that have a ".0" or ".1" micro version number, like e.g., 3.14.0). This is because the tools needed to support Python on macOS often lag usually aren't available for recently released stable Python versions.

{% block prerequisites_macos %}
{% endblock %}

{% if not config.extra.macos_only %}

///

/// tab | Linux

{{ formal_name }} requires Python {{ min_python_version }}+. You will also need a method for managing virtual environments (such as `venv`).

You can verify the version of Python that you have installed by running:

```console
$ python3 --version
```

If you have more than one version of Python installed, you may need to replace `python3` with a specific version number (e.g., `python{{ recent_python_version }}`)

We recommend avoiding recently released version of Python (i.e., versions that have a ".0" or ".1" micro version number, like e.g., 3.14.0). This is because the tools needed to support Python on Linux often lag usually aren't available for recently released stable Python versions.

{% block prerequisites_linux %}
{% endblock %}

///

/// tab | Windows

{{ formal_name }} requires Python {{ min_python_version }}+. You will also need a method for managing virtual environments (such as `venv`).

You can verify the version of Python that you have installed by running:

```doscon
C:\...>py -3 --version
```

If you have more than one version of Python installed, you may need to replace the `-3` with a specific version number (e.g., `-python{{ recent_python_version }}`)

We recommend avoiding recently released version of Python (i.e., versions that have a ".0" or ".1" micro version number, like e.g., 3.14.0). This is because the tools needed to support Python on Windows often lag usually aren't available for recently released stable Python versions.

{% block prerequisites_windows %}
{% endblock %}

///

{% endif %}

### Set up your development environment  { #dev-environment-set-up }

The recommended way of setting up your development environment for {{ formal_name }} is to use a [virtual environment](https://docs.python.org/3/library/venv.html), and then install the development version of {{ formal_name }} and its dependencies.

#### Clone the {{ formal_name }} repository

Next, go to the [{{ formal_name }} page on GitHub](https://github.com/beeware/{{ project_name }}), and, if you haven't already, [fork the repository](https://github.com/beeware/{{ project_name }}/fork) into your own account. Next, click on the "<> Code" button on your fork. If you have the GitHub desktop application installed on your computer, you can select "Open with GitHub Desktop"; otherwise, copy the HTTPS URL provided, and use it to clone the repository to your computer using the command line:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

Fork the {{ formal_name }} repository, and then:

```console
$ git clone https://github.com/<your username>/{{ project_name }}.git
```

(substituting your GitHub username)

{% if not config.extra.macos_only %}

///

/// tab | Linux

Fork the {{ formal_name }} repository, and then:

```console
$ git clone https://github.com/<your username>/{{ project_name }}.git
```

(substituting your GitHub username)

///

/// tab | Windows

Fork the {{ formal_name }} repository, and then:

```doscon
C:\...>git clone https://github.com/<your username>/{{ project_name }}.git
```

(substituting your GitHub username)

///

{% endif %}

#### Create a virtual environment

To set up a virtual environment and upgrade `pip`, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
$ cd {{ project_name }}
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python -m pip install -U pip
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
$ cd {{ project_name }}
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python -m pip install -U pip
```

///

/// tab | Windows

```doscon
C:\...>cd {{ project_name }}
C:\...>py -3 -m venv .venv
C:\...>.venv\Scripts\activate
(.venv) $ python -m pip install -U pip
```

///

{% endif %}

Your prompt should now have a `(.venv)` prefix in front of it.

#### Install {{ formal_name }}

Now that you have the source code, you can do an [editable install](https://setuptools.pypa.io/en/latest/userguide/development_mode.html) of {{ formal_name }} into your development environment. Run the following command:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

{% block install_macos_tool %}

```console
(.venv) $ python -m pip install -U -e . --group dev
```

{% endblock %}

{% if not config.extra.macos_only %}

///

/// tab | Linux

{% block install_linux_tool %}

```console
(.venv) $ python -m pip install -U -e . --group dev
```

{% endblock %}

///

/// tab | Windows

{% block install_windows_tool %}

```doscon
(.venv) C:\...>python -m pip install -U -e . --group dev
```

{% endblock %}

///

{% endif %}

#### Enable pre-commit

{{ formal_name }} uses a tool called [pre-commit](https://pre-commit.com) to identify simple issues and standardize code formatting. It does this by installing a git hook that automatically runs a series of code linters prior to finalizing any git commit. To enable pre-commit, run:

{% if not config.extra.macos_only %}

/// tab | macOS

{% endif %}

```console
(.venv) $ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

{% if not config.extra.macos_only %}

///

/// tab | Linux

```console
(.venv) $ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

///

/// tab | Windows

```doscon
(.venv) C:\...>pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

///

{% endif %}

Now you are ready to start hacking on {{ formal_name }}!
