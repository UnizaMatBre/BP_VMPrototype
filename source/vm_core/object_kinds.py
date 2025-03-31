from object_layout import VM_Object

class VM_Symbol(VM_Object):
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

        if not isinstance(other, VM_Symbol):
            return False

        return (self._text == other._text) and (self._arity == other._arity)

class VM_ByteArray(VM_Object):
    """
    Represents sequence of bytes
    """
    def __init__(self, item_count):
        super().__init__()

        self._bytes = [0] * item_count

    def byte_get_at(self, index):
        return self._bytes[index]

    def byte_put_at(self, index, byte):
        self._bytes[index] = byte

    def get_byte_count(self):
        return len(self._bytes)


class VM_ObjectArray(VM_Object):
    """
    Represents sequence of objects
    """
    def __init__(self, item_count, none_object):
        super().__init__()

        self._items = [none_object] * item_count

    def item_get_at(self, index):
        return self._items[index]

    def item_put_at(self, index, new_value):
        self._items[index] = new_value

    def get_item_count(self):
        return len(self._items)


class VM_Method(VM_Object):
    """
    Represents object with custom evaluation
    """
    def __init__(self, literals, bytecode):
        super().__init__()

        assert isinstance(literals, VM_ObjectArray)
        assert isinstance(bytecode, VM_ByteArray)
        assert bytecode.get_byte_count() % 2 == 0 # all instructions have size of 2 bytes, thus bytecode must have even bytes

        self._literals = literals
        self._bytecode = bytecode

    def get_literals(self):
        return self._literals

    def get_bytecodes(self):
        return self._bytecode


class VM_Frame(VM_Object):
    """
    Represents runtime context of executed method (local values, selected instruction)
    """

    def __init__(self, none_object, stack, method_activation):
        super().__init__()

        assert isinstance(stack, VM_ObjectArray)
        assert isinstance(method_activation, VM_Method)

        self._previous_frame = none_object

        self._local_stack = stack
        self._local_stack_index = 0

        self._method_activation = method_activation
        self._instruction_index = 0 # this will

    def push_item(self, item):
        self._local_stack.item_put_at(self._local_stack_index, item)

    def pull_item(self, none_object):
        self._local_stack_index -= 1

        item_to_return = self._local_stack.item_get_at(self._local_stack_index)
        self._local_stack.item_put_at(self._local_stack_index, none_object)

        return item_to_return

    def get_current_instruction(self):
        bytecode_index = self._instruction_index * 2

        # TODO: maybe this should be refactored into its own object?
        return (
            self._method_activation.get_bytecodes().byte_get_at(bytecode_index),
            self._method_activation.get_bytecodes().byte_get_at(bytecode_index + 1)
        )

    def move_instruction_by(self, distance):
        self._instruction_index += distance

    def get_instruction_count(self):
        return self._method_activation.get_bytecodes().get_byte_count() / 2

    def is_instruction_finished(self):
        return self._instruction_index > self.get_instruction_count()


    def get_previous_frame(self):
        return self._previous_frame

    def set_previous_frame(self, new_previous_frame):
        self._previous_frame = new_previous_frame


class VM_Proces(VM_Object):
    def __init__(self, root_frame):
        super().__init__()

        self._active_frame = root_frame

    def push_frame(self, new_frame):
        assert isinstance(new_frame, VM_Frame)

        new_frame.set_previous_frame(self._active_frame)

        self._active_frame = new_frame

    def pull_frame(self, none_object):
        old_active_frame = self._active_frame
        self._active_frame = self._active_frame.get_previous_frame()

        old_active_frame.set_previous_frame(none_object)

        return old_active_frame

    def peek_frame(self):
        return self._active_frame
