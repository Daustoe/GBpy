import numbers

class Register(int):
    """
    Register class represents a physical register of the GB. (i.e. A, B, H, ...)
    numbers reference here:
    https://docs.python.org/3/library/numbers.html#module-numbers
    https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types
    http://stackoverflow.com/questions/2673651/inheritance-from-str-or-int
    """

    def __new__(cls, value=0, limit=0xff):
        i = int.__new__(cls, value)
        i._limit = limit
        return i
    
    def __str__(self):
        return hex(int(super(Register, self).__str__()))
    
    def __add__(self, other):
        return Register(int.__add__(self, other) & self._limit, limit=self._limit)
    
    def __and__(self, other):
        return Register(int.__and__(self, other) & self._limit, limit=self._limit)

    def __sub__(self, other):
        return Register(int.__sub__(self, other) & self._limit, limit=self._limit)

    def __lshift__(self, other):
        return Register(int.__lshift__(self, other) & self._limit, limit=self._limit)

    def __rshift__(self, other):
        return Register(int.__rshift__(self, other) & self._limit, limit=self._limit)

    def __xor__(self, other):
        return Register(int.__xor__(self, other) & self._limit, limit=self._limit)

    def __or__(self, other):
        return Register(int.__or__(self, other) & self._limit, limit=self._limit)

