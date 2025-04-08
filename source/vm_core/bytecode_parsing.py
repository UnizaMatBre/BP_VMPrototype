

class LiteralTags:
    """Enumeration of tags that determine interpretation of following bytes"""
    VM_BYTEARRAY = 0x00


class BytecodeDeserializer:
    def __init__(self, universe, byte_list):
        self._universe = universe
        self._byte_list = byte_list
        self._index = 0





