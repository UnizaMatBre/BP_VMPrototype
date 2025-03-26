from object_layout import Object

class Symbol(Object):
    """
    Represents immutable name of slots and message selectors
    """

    def __init__(self, text, arity):
        super().__init__()

        self._text = text
        self._arity =  arity

    def __hash__(self):
        return hash((self._text, self._arity))

    def __eq__(self, other):
        if self is other:
            return True

        if not isinstance(other, Symbol):
            return False

        return (self._text == other._text) and (self._arity == other._arity)

class ByteArray(Object):
    def __init__(self, item_count):
        super().__init__()

        self._bytes = [0] * item_count

    def byte_get_at(self, index):
        return self._bytes[index]

    def item_put_at(self, index, byte):
        self._bytes[index] = byte

    def get_byte_count(self):
        return len(self._bytes)

