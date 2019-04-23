"""Memory module."""


class Scope(dict):
    """Memory scope object."""

    pass


class Frame(list):
    """Frame of `Scope` objects."""

    def __init__(self, *args, **kwargs):
        """Initialization of `Frame` class."""
        super().__init__(*args, **kwargs)

    @property
    def current(self):
        """Get the current scope of the frame."""
        return self[-1]

    @current.setter
    def current(self, value):
        """Set the current scope of the frame."""
        self[-1] = value


class Stack(list):
    """Stack of `Frame` objects."""

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

    def __iter__(self):
        """Iterate on the memory."""
        for key in self.stack.current.current:
            yield key

    def append_frame(self, **kwargs):
        """Create a new frame."""
        self.stack.append(Frame([Scope(**kwargs)]))

    def pop_frame(self):
        """Delete the current frame."""
        self.stack.pop()

    def append_scope(self):
        """Create a new scope in the current frame."""
        self.stack.current.append(Scope(self.stack.current.current))

    def pop_scope(self):
        """Delete the current scope in the current frame."""
        child_scope = self.stack.current.current.copy()
        self.stack.current.pop()
        parent_scope = self.stack.current.current.copy()
        self.stack.current.current = {
            key: child_scope[key] for key in child_scope if key in parent_scope
        }

    def __str__(self):
        """String representation of a token."""
        return str(self.stack)

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()  # pragma: no cover
