"""Type module."""

from abc import ABC, abstractmethod


class Generic(ABC):
    """Generic abstract class for generic type."""

    @abstractmethod
    def _handle_type(self, other):
        """Helper to handle the return type."""
        pass

    def __add__(self, other):
        """Handle the `+` operator."""
        return self._handle_type(other)(self.value + other.value)

    def __sub__(self, other):
        """Handle the `-` operator."""
        return self._handle_type(other)(self.value - other.value)

    def __mul__(self, other):
        """Handle the `*` operator."""
        return self._handle_type(other)(self.value * other.value)

    def __truediv__(self, other):
        """Handle the `/` operator."""
        return Float(self.value / other.value)

    def __floordiv__(self, other):
        """Handle the `//` operator."""
        return self._handle_type(other)(self.value // other.value)

    def __pos__(self):
        """Handle the unary `+` operator."""
        return type(self)(+self.value)

    def __neg__(self):
        """Handle the unary `+` operator."""
        return type(self)(-self.value)

    def __eq__(self, other):
        """Handle the `==` operator."""
        return Bool(True) if self.value == other.value else Bool(False)

    def __ne__(self, other):
        """Handle the `!=` operator."""
        return Bool(True) if self.value != other.value else Bool(False)

    def __le__(self, other):
        """Handle the `<=` operator."""
        return Bool(True) if self.value <= other.value else Bool(False)

    def __ge__(self, other):
        """Handle the `>=` operator."""
        return Bool(True) if self.value >= other.value else Bool(False)

    def __lt__(self, other):
        """Handle the `<` operator."""
        return Bool(True) if self.value < other.value else Bool(False)

    def __gt__(self, other):
        """Handle the `>` operator."""
        return Bool(True) if self.value > other.value else Bool(False)

    def __str__(self):
        """String representation of a boolean."""
        return str(self.value)

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class Bool(object):
    """Representation of a Boolean."""

    def __init__(self, value):
        """Initialization of `Bool` class."""
        self.value = bool(value)

    def __eq__(self, other):
        """Handle the `==` operator."""
        return Bool(True) if self.value == other.value else Bool(False)

    def __ne__(self, other):
        """Handle the `!=` operator."""
        return Bool(True) if self.value != other.value else Bool(False)

    def __str__(self):
        """String representation of a boolean."""
        return 'true' if self.value is True else 'false'

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class Int(Generic):
    """Representation of a Integer."""

    def _handle_type(self, other):
        """Helper to handle the return type."""
        if isinstance(other, Int):
            return Int
        elif isinstance(other, Float):
            return Float
        else:
            raise Exception(
                (f'TYPE ERROR: '
                 f'Insuported {type(self)} {type(other)} evaluation.')
            )

    def __init__(self, value):
        """Initialization of `Int` class."""
        self.value = int(value)


class Float(Generic):
    """Representation of a Float."""

    def _handle_type(self, other):
        """Helper to handle the return type."""
        if isinstance(other, Int):
            return Float
        elif isinstance(other, Float):
            return Float
        else:
            raise Exception(
                (f'TYPE ERROR: '
                 f'Insuported {type(self)} {type(other)} evaluation.')
            )

    def __init__(self, value):
        """Initialization of `Float` class."""
        self.value = float(value)
