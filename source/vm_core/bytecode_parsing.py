from source.vm_core.object_kinds import VM_ByteArray


class LiteralTags:
    """Enumeration of tags that determine interpretation of following bytes"""
    VM_BYTEARRAY = 0x00

    VM_SYMBOL = 0x01

    VM_SMALL_INTEGER = 0x02

    VM_CODE = 0x03

    VM_OBJECT_ARRAY = 0x04

class DeserializerException(Exception):
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
            raise DeserializerException()

        old_index = self._index
        self._index += number

        return ( self._byte_list[local_index] for local_index in range(old_index, self._index) )

    def _move_by(self, distance):
        self._index += distance

    def _get_next_int64(self):
        return int.from_bytes(self._get_next_n_bytes(8), byteorder="big", signed=True)

    def _check_tag(self, expected_tag):
        if self._get_current() != expected_tag:
            raise DeserializerException()

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



    def parse_bytes(self):
        """Job of this is to pick correct parsing based on tag"""
        supposed_tag = self._get_current()
        self._move_by(1)

        match supposed_tag:
            case LiteralTags.VM_SYMBOL:
                return self.unchecked_parse_symbol()
            case LiteralTags.VM_SMALL_INTEGER:
                return self.unchecked_parse_byte_array()
            case LiteralTags.VM_BYTEARRAY:
                return self.unchecked_parse_byte_array()
            case _:
                raise DeserializerException()