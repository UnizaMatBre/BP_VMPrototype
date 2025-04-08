from source.vm_core.object_kinds import VM_ByteArray


class LiteralTags:
    """Enumeration of tags that determine interpretation of following bytes"""
    VM_BYTEARRAY = 0x00


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

    def _move_by(self, distance):
        self._index += distance

    def parse_bytearray(self):
        if self._get_current() != LiteralTags.VM_BYTEARRAY:
            raise DeserializerException()

        self._move_by(1)

        # read size (8-bits)
        # TODO: handle possible error of running out of the bytes to read
        byte_count_bytes = [self._get_current() for x in range(8)]

        byte_count = int.from_bytes(byte_count_bytes, byteorder="big", signed=False)

        # read values into array
        # TODO: handle possible error of running out of the bytes to read
        new_bytearray = self._universe.new_bytearray(byte_count)
        for index in range(byte_count):
            new_bytearray.byte_put_at(index, self._get_current())

        return new_bytearray


