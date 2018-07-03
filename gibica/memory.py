"""Memory module."""


class Scope(dict):
    """Memory scope object."""
    pass


class Frame(list):
    """Frame of scopes objects."""

    def __init__(self, *args, **kwargs):
        """Initialization of `Frame` class."""
        super().__init__(*args, **kwargs)

    @property
    def current(self):
        """Get the current scope of the frame."""
        return self[-1]


class Stack(list):
    """Stack of frames objects."""

    def __init__(self, *args, **kwargs):
        """Initialization of `Stack` class."""
        super().__init__(*args, **kwargs)

    @property
    def current(self):
        """Get the current frame of the stack."""
        return self[-1]


class Memory(object):
    """Memory object representation."""

    def __init__(self, **kwags):
        """Initialization of `Memory` class."""
        self.stack = Stack([Frame([Scope(**kwags)])])

    def __getitem__(self, value):
        """Get a value from the current scope in the current frame."""
        return self.stack.current.current.get(value)

    def __setitem__(self, key, value):
        """Set a value from the current scope in the current frame."""
        self.stack.current.current[key] = value

    def __eq__(self, other):
        """Handle the `==` operator."""
        return self.stack == other.stack

    def __ne__(self, other):
        """Handle the `!=` operator."""
        return self.stack != other.stack

    def append_frame(self):
        """Create a new frame."""
        self.stack.append(Frame([Scope()]))

    def pop_frame(self):
        """Delete the current frame."""
        self.stack.pop()

    def append_scope(self):
        """Create a new scope in the current frame."""
        self.stack.current.append(Scope())

    def pop_scope(self):
        """Delete the current scope in the current scope."""
        self.stack.current.pop()

    def __str__(self):
        """String representation of a token."""
        return f"{str(self.stack)}"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()
