# Test/example module for Mkdocs macros. See
# https://mkdocs-macros-plugin.readthedocs.io/en/latest/macros/


def define_env(env):
    # This is a global variable, which should be available on any page.
    env.variables.mascot_name = "Brutus"

    # This is a global macro, which should be available on any page.
    @env.macro
    def say_hello():
        return "Hello world!"
