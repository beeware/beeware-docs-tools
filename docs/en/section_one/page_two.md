# BeeWare Docs Tools Demo section one: page two

## Footer and navigation links

Navigation should render at the bottom of the page; "BeeWare Docs Tools Demo Section One" should be on the left, "Section Two" should be on the right. The footer should be below the navigation links. This confirms the theme configuration has been applied.

## Class reference documentation

The following should show the reference documentation for the `DocsTest` class, located in `docs_test.py`, in the `src/beeware_docs_tools` directory. This verifies that the source code directory symlinking is working properly.

::: beeware_docs_tools.docs_test.DocsTest

## Macro functionality

The following should say 'Brutus says "Hello world!"'. This confirms that global variables and macros defined via MkDocs-Macros are available.

{{ mascot_name }} says "{{ say_hello() }}"
