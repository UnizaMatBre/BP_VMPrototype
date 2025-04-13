from source.vm_core.object_layout import VM_Object

class VM_Symbol(VM_Object):
    """
    Represents immutable name of slots and message selectors
    """

    def __init__(self, text, arity):
        super().__init__()

        self._text = text
        self._arity =  arity

    def copy(self):
        """
        Unlike other objects, symbols are unique and thus cannot be cloned.

        :return: self
        """

        return self

    def get_arity(self):
        return self._arity

    def __hash__(self):
        return hash((self._text, self._arity))

    def __eq__(self, other):
        if self is other:
            return True

        if not isinstance(other, VM_Symbol):
            return False

        return (self._text == other._text) and (self._arity == other._arity)


class VM_SmallInteger(VM_Object):
    """
    Represents signed integer
    """
    def __init__(self, value):
        super().__init__()

        self._value = value

    def copy(self):
        copy_object = VM_SmallInteger(self._value)

        self._copy_slots_into(copy_object)

        return copy_object

    def get_value(self):
        return self._value


class VM_ByteArray(VM_Object):
    """
    Represents sequence of bytes
    """
    def __init__(self, item_count):
        super().__init__()

        self._bytes = [0] * item_count

    def copy(self):
        copy_object = VM_ByteArray(self.get_byte_count())

        copy_object._bytes = self._bytes.copy()
        self._copy_slots_into(copy_object)

        return copy_object

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

    def copy(self):
        copy_object = VM_ObjectArray(self.get_item_count())

        copy_object._items = self._items.copy()
        self._copy_slots_into(copy_object)

        return copy_object

    def item_get_at(self, index):
        return self._items[index]

    def item_put_at(self, index, new_value):
        self._items[index] = new_value

    def get_item_count(self):
        return len(self._items)


class VM_String(VM_Object):
    """
    Represents UTF-8 string
    """
    def __init__(self, characters):
        assert isinstance(characters, str)

        super().__init__()

        self._characters = characters

    def copy(self):
        copy_object = VM_String(self._characters)

        self._copy_slots_into(copy_object)

        return copy_object

    def character_get_at(self, index):
        return self._characters[index]

    def character_put_at(self, index, new_value):
        self._characters[index] = new_value

    def get_character_count(self):
        return len(self._characters)


class VM_Assignment(VM_Object):
    """
    Represents assignment primitive
    """
    def __init__(self, target_slot_name):
        super().__init__()

        self._target_slot_name = target_slot_name

    def copy(self):
        copy_object = VM_Assignment(self._target_slot_name)

        self._copy_slots_into(copy_object)

        return copy_object

    def get_parameter_count(self):
        return 1

    def get_target_name(self):
        return self._target_slot_name




class VM_PrimitiveMethod(VM_Object):
    """
    Represents object which runs native code when evaluated
    """
    def __init__(self, parameter_count, native_function):
        assert parameter_count >= 0
        assert callable(native_function)

        super().__init__()

        self._parameter_count = parameter_count
        self._native_function = native_function

    def copy(self):
        return self

    def get_parameter_count(self):
        return self._parameter_count

    def native_call(self, interpreter, parameters):
        result = self._native_function(interpreter, parameters)

        assert isinstance(result, VM_Object)

        return result


class VM_Code(VM_Object):
    """
    Represents executable sequence of bytecode and list of literals referenced by it
    """

    def __init__(self, stack_usage, literals, bytecode):
        assert isinstance(literals, VM_ObjectArray)
        assert isinstance(bytecode, VM_ByteArray)
        assert isinstance(stack_usage, int)
        assert stack_usage >= 0
        assert bytecode.get_byte_count() % 2 == 0 # all instructions have size of 2 bytes, thus bytecode must have even bytes

        super().__init__()

        self._stack_usage = stack_usage
        self._literals = literals
        self._bytecode = bytecode

    def copy(self):
        copy_object = VM_Code(
            self._stack_usage,
            self._literals.copy(),
            self._bytecode.copy()
        )

        self._copy_slots_into(copy_object)

        return copy_object

    def get_stack_usage(self):
        return self._stack_usage

    def get_literals(self):
        return self._literals

    def get_bytecode(self):
        return self._bytecode

    def get_instruction_count(self):
        return self._bytecode.get_byte_count() // 2


class VM_Frame(VM_Object):
    """
    Represents runtime context of executed method (local values, selected instruction)
    """

    def __init__(self, none_object, stack, method_activation):
        super().__init__()

        assert isinstance(stack, VM_ObjectArray)
        assert method_activation.has_code()

        self._previous_frame = none_object

        self._local_stack = stack
        self._local_stack_index = 0

        self._method_activation = method_activation
        self._instruction_index = 0 # this will

    def copy(self):
        copy_object = VM_Frame(
            None,
            self._local_stack.copy(),
            self._method_activation.copy()
        )

        copy_object._previous_frame = self._previous_frame
        copy_object._local_stack_index = self._local_stack_index
        copy_object._instruction_index = self._instruction_index

        self._copy_slots_into(copy_object)

        return copy_object

    def get_method_activation(self):
        return self._method_activation

    def get_code(self):
        return self._method_activation.get_code()

    def push_item(self, item):
        self._local_stack.item_put_at(self._local_stack_index, item)

        self._local_stack_index += 1

    def pull_item(self, none_object):
        self._local_stack_index -= 1

        item_to_return = self._local_stack.item_get_at(self._local_stack_index)
        self._local_stack.item_put_at(self._local_stack_index, none_object)

        return item_to_return

    def can_stack_change_by(self, count):
        """
        Takes current stack index and checks if changing it by said number still produces valid stack position.
        + negative distance tells us if we can pull that many items from stack
        + positive distance tells us if we can push that many items into stack


        :param count: number of items from current index to check
        :return: True if resulting stack would be still valid, False otherwise
        """
        new_index = self._local_stack_index + count

        return 0 <= new_index <= self._local_stack.get_item_count()

    def is_stack_full(self):
        return self._local_stack_index >= self._local_stack.get_item_count()

    def is_stack_empty(self):
        return self._local_stack_index <= 0


    def get_current_instruction(self):
        bytecode_index = self._instruction_index * 2

        # TODO: maybe this should be refactored into its own object?
        return (
            self.get_code().get_bytecode().byte_get_at(bytecode_index),
            self.get_code().get_bytecode().byte_get_at(bytecode_index + 1)
        )

    def move_instruction_by(self, distance):
        self._instruction_index += distance

    def get_instruction_count(self):
        return self._method_activation.get_code().get_instruction_count()

    def has_finished(self):
        return self._instruction_index >= self.get_instruction_count()


    def get_previous_frame(self):
        return self._previous_frame

    def set_previous_frame(self, new_previous_frame):
        self._previous_frame = new_previous_frame


    def literal_get_at(self, index):
        if index >= self.get_code().get_literals().get_item_count():
            return (False, None)

        return (True, self.get_code().get_literals().item_get_at(index))


class VM_Process(VM_Object):
    def __init__(self, none_object, root_frame):
        super().__init__()

        self._active_frame = root_frame

        self._error_handler = none_object

        self._result = none_object

    def copy(self):
        copy_object = VM_Process(
            self._result,
            self._active_frame.copy()
        )

        self._copy_slots_into(copy_object)

        return copy_object

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


    def get_result(self):
        return self._result

    def set_result(self, new_result):
        self._result = new_result

    def has_finished(self, none_object):
        """Process is finished if either result is not none_object or there are no frames"""
        return self.get_result() != none_object or self.peek_frame() == none_object

    def get_error_handler(self):
        return self._error_handler

    def set_error_handler(self, new_handler):
        self._error_handler = new_handler