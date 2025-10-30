class DocsTest:
    def __init__(self, arg1: int, arg2: int = 42, **kwargs):
        """This is the test class.

        :param arg1: A value.
        :param arg2: A value with a default.
        :param kwargs: keyword arguments
        """
        pass

    @property
    def attribute(self) -> int:
        """This is a test attribute."""
        return 42

    def method(self, arg1: int, arg2: int = 42, **kwargs):
        """This is a test method.

        :param arg1: A value.
        :param arg2: A value with a default.
        :param kwargs: keyword arguments
        """
        pass
