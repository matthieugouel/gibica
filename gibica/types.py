"""Types module."""

from abc import ABC, abstractmethod
from gibica.exceptions import ObjectError, TypeError


class AbstractObject(ABC):
    """Abstract class for generic object."""

    # Raises a custom `ObjectError` if the attribute or method doesn't exist
    def _object_error(self):
        """Raise an `ObjectError`."""
        raise ObjectError("Unsupported method.")

    def __getattr__(self, name):
        """Handle methods and attributes fetching."""
        try:
            if callable(getattr(self, name)):
                # Requests a method
                return getattr(self, name)()
            else:
                # Requests an attribute
                return getattr(self, name)
        except AttributeError:
            self._object_error()


class AbstractType(AbstractObject, ABC):
    """Abstract class for generic type."""

    # Raises a custom `TypeError` if the operator is not overrided
    def _type_error(self):
        """Raise a `TypeError`."""
        raise TypeError("Unsupported operation.")

    # Triggers `_type_error` for all implemented operators
    for operator in (
        '__add__',
        '__sub__',
        '__mul__',
        '__truediv__',
        '__floordiv__',
        '__pos__',
        '__neg__',
        '__eq__',
        '__ne__',
        '__le__',
        '__ge__',
        '__lt__',
        '__gt__',
    ):
        locals()[operator] = lambda self, *args, **kwargs: self._type_error()

    def __bool__(self):
        """Handle the boolean value of the instance."""
        self._type_error()

    def __str__(self):
        """String representation of a boolean."""
        return str(self.value)

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class AbstractNumber(AbstractType, ABC):
    """Abstract class for generic number."""

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


class Bool(AbstractType):
    """Representation of a `Boolean`."""

    def __init__(self, value):
        """Initialization of `Bool` class."""
        self.value = bool(value)

    def __eq__(self, other):
        """Handle the `==` operator."""
        if isinstance(other.value, bool):
            return Bool(True) if self.value == other.value else Bool(False)
        else:
            raise self._type_error()

    def __ne__(self, other):
        """Handle the `!=` operator."""
        if isinstance(other.value, bool):
            return Bool(True) if self.value != other.value else Bool(False)
        else:
            raise self._type_error()

    def __bool__(self):
        """Handle the boolean value of the instance."""
        return True if self.value is True else False

    def __str__(self):
        """String representation of a boolean."""
        return 'true' if self.value is True else 'false'

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class Int(AbstractNumber):
    """Representation of an `Integer` number."""

    def _handle_type(self, other):
        """Helper to handle the return type."""
        if isinstance(other, Int):
            return Int
        elif isinstance(other, Float):
            return Float
        else:
            raise TypeError(
                f"Unsuported operation between `{type(self)}` and `{type(other)}`."
            )

    def __init__(self, value):
        """Initialization of `Int` class."""
        self.value = int(value)


class Float(AbstractNumber):
    """Representation of a `Float` number."""

    def _handle_type(self, other):
        """Helper to handle the return type."""
        if isinstance(other, Int):
            return Float
        elif isinstance(other, Float):
            return Float
        else:
            raise TypeError(
                f"Unsuported operation between `{type(self)}` and `{type(other)}`."
            )

    def __init__(self, value):
        """Initialization of `Float` class."""
        self.value = float(value)
