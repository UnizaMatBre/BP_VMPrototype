from doctest import UnexpectedException

from source.vm_core.object_kinds import VM_ByteArray, VM_Code
from source.vm_core.object_layout import VM_Object, SlotKind


class LiteralTags:
    """Enumeration of tags that determine interpretation of following bytes"""
    VM_BYTEARRAY = 0x00

    VM_SYMBOL = 0x01

    VM_SMALL_INTEGER = 0x02

    VM_CODE = 0x03

    VM_OBJECT_ARRAY = 0x04

    VM_NONE = 0x05

    VM_OBJECT = 0x06



class DeserializationError(Exception):
    pass

class BytecodeDeserializer:
    def __init__(self, universe, byte_list):
        self._universe = universe
        self._byte_list = byte_list
        self._index = 0


    def _is_finished(self):
        return self._index >= len(self._byte_list)

    def _get_current(self):
        return self._byte_list[self._index]

    def _get_next_n_bytes(self, number):
        if self._index + number > len(self._byte_list):
            raise DeserializationError()

        old_index = self._index
        self._index += number

        return ( self._byte_list[local_index] for local_index in range(old_index, self._index) )

    def _move_by(self, distance):
        self._index += distance

    def _get_next_int64(self):
        return int.from_bytes(self._get_next_n_bytes(8), byteorder="big", signed=True)

    def _check_tag(self, expected_tag):
        if self._get_current() != expected_tag:
            raise DeserializationError()

        self._move_by(1)


    def unchecked_parse_symbol(self):
        arity = self._get_next_int64()
        character_count = self._get_next_int64()

        symbol_text = "".join(chr(ch) for ch in self._get_next_n_bytes(character_count))

        return self._universe.new_symbol(symbol_text, arity)

    def parse_symbol(self):
        self._check_tag(LiteralTags.VM_SYMBOL)
        return self.unchecked_parse_symbol()




    def unchecked_parse_small_integer(self):
        return self._universe.new_small_integer(self._get_next_int64())

    def parse_small_integer(self):
        self._check_tag(LiteralTags.VM_SMALL_INTEGER)
        return self.unchecked_parse_small_integer()


    def unchecked_parse_byte_array(self):
        # read size (8 bytes)
        byte_count = self._get_next_int64()

        # read values into array
        new_byte_array = self._universe.new_byte_array(byte_count)
        new_byte_array_content = self._get_next_n_bytes(byte_count)

        for index in range(byte_count):
            new_byte_array.byte_put_at(index, next(new_byte_array_content))

        return new_byte_array

    def parse_bytearray(self):
        self._check_tag(LiteralTags.VM_BYTEARRAY)
        return self.unchecked_parse_byte_array()




    def unchecked_parse_object_array(self):
        # read size (8 bytes)
        item_count = self._get_next_int64()

        # read values
        new_object_array = self._universe.new_object_array(item_count)

        for index in range(item_count):
            new_object_array.item_put_at(index, self.parse_bytes())

        return new_object_array

    def parse_object_array(self):
        self._check_tag(LiteralTags.VM_OBJECT_ARRAY)
        return self.unchecked_parse_object_array()


    def unchecked_parse_code(self):
        literals = self.parse_object_array()
        bytecode = self.parse_bytearray()

        return self._universe.new_code(literals, bytecode)

    def parse_code(self):
        self._check_tag(LiteralTags.VM_CODE)
        return self.unchecked_parse_code()

    def _parse_slot(self):
        slot_kind_bytes = self._get_current()
        self._move_by(1)

        slot_kind = SlotKind()
        if bool(slot_kind_bytes & 0b00000001):
            slot_kind.toggleParent()

        if bool(slot_kind_bytes & 0b00000010):
            slot_kind.toggleParameter()

        slot_name = self.parse_symbol()
        slot_content = self.parse_bytes()

        return (slot_name, slot_kind, slot_content)


    def unchecked_parse_slot_object(self):
        slot_count = self._get_next_int64()

        new_slot_object = VM_Object()

        for counter in range(slot_count):
            slot_name, slot_kind, slot_content = self._parse_slot()

            # raise error if slot already exists
            slot_created = new_slot_object.add_slot(slot_name, slot_kind, slot_content)
            if not slot_created:
                raise DeserializationError()

        if self._get_current() == LiteralTags.VM_CODE:
            self._move_by(1)
            new_slot_object.set_code(
                self.unchecked_parse_code()
            )


        return new_slot_object

    def parse_slot_object(self):
        self._check_tag(LiteralTags.VM_OBJECT)
        return self.unchecked_parse_slot_object()





    def parse_bytes(self):
        """Job of this is to pick correct parsing based on tag"""
        supposed_tag = self._get_current()
        self._move_by(1)

        match supposed_tag:
            case LiteralTags.VM_NONE:
                return self._universe.get_none_object()
            case LiteralTags.VM_SYMBOL:
                return self.unchecked_parse_symbol()
            case LiteralTags.VM_SMALL_INTEGER:
                return self.unchecked_parse_small_integer()
            case LiteralTags.VM_BYTEARRAY:
                return self.unchecked_parse_byte_array()
            case LiteralTags.VM_OBJECT_ARRAY:
                return self.unchecked_parse_object_array()
            case LiteralTags.VM_CODE:
                return self.unchecked_parse_code()
            case LiteralTags.VM_OBJECT:
                return self.unchecked_parse_slot_object()
            case _:
                raise DeserializationError()



REAL_MODULE_SIGNATURE = [ord(char) for char in "ORE"]

def deserialize_module(universe, byte_sequence):
    this_module_signature = [next(byte_sequence) for counter in range(len(REAL_MODULE_SIGNATURE))]

    if this_module_signature != REAL_MODULE_SIGNATURE:
        raise DeserializationError()

    return BytecodeDeserializer(universe, list(byte_sequence)).parse_code()