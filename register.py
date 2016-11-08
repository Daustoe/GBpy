import numbers

class Register(numbers.Integral):
    """
    Register class represents a physical register of the GB. (i.e. A, B, H, ...)
    numbers reference here:
    https://docs.python.org/3/library/numbers.html#module-numbers
    https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types
    http://stackoverflow.com/questions/2673651/inheritance-from-str-or-int
    """

    def __new__(cls, *args, **kwargs):
        print(args)
        return numbers.Integral.__new__(cls, *args, **kwargs)

    def __repr__(self):
        return hex(self.value)

    def __str__(self):
        return hex(self.value)

    def __add__(self, other):
        self.value += other
        self.value &= self.limit
        return self

    def __radd__(self, other):
        self.value += other
        self.value &= self.limit
        return self

    def __sub__(self, other):
        if type(other) is Register:
            self.value -= other.value
            self.value &= self.limit
            return self
        elif type(other) is int:
            self.value -= other
            self.value &= self.limit
            return self
        else:
            raise TypeError('unorderable types: Register - ' + type(other))