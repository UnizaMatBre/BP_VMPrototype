from vm_core.object_layout import Object

class Symbol(Object):
    """
    Represents immutable name of slots and message selectors
    """

    def __init__(self, text, arity):
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