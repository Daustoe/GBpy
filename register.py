import numbers

class Register(numbers.Integral):
    """
    Register class represents a physical register of the GB. (i.e. A, B, H, ...)
    numbers reference here:
    https://docs.python.org/3/library/numbers.html#module-numbers
    """
    # TODO: Read up on https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types
    def __init__(self, value):
        self.value = value

    def value(self):
        return self.value

    def __int__(self):
        return self.value

    def __repr__(self):
        return hex(self.value)

    def __str__(self):
        return hex(self.value)

    def __setattr__(self, key, value):
        super().__setattr__('value', value)

    def __getattribute__(self, item):
        return object.__getattribute__(self, 'value')

    def __add__(self, other):
        self.value += other
        return self

    def __radd__(self, other):
        self.value += other
        return self

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __and__(self, other):
        return self.value & other

    def __sub__(self, other):
        if type(other) is Register:
            self.value -= other.value
            return self
        elif type(other) is int:
            self.value -= other
            return self
        else:
            raise TypeError('unorderable types: Register - ' + type(other))

    def __xor__(self, other):
        if type(other) is Register:
            return self.value ^ other.value
        elif type(other) is int:
            return self.value ^ other
        else:
            raise TypeError('unorderable types: Register < '+type(other))