import unittest

from source.vm_core.bytecode_parsing import *
from source.vm_core.object_kinds import VM_ByteArray, VM_Symbol


class UniverseMockup:
    def new_byte_array(self, byte_count):
        return VM_ByteArray(byte_count)

    def new_symbol(self, text, arity):
        return VM_Symbol(text, arity)

class BytearrayParsingTestCase(unittest.TestCase):
    def test_bytearray_correct(self):
        byte_content = [0x01, 0x02, 0x03, 0x04]
        byte_count = len(byte_content).to_bytes(8, byteorder="big", signed=True)
        byte_list = [LiteralTags.VM_BYTEARRAY] + list(byte_count) + byte_content

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        result = deserializer.parse_bytearray()

        self.assertTrue(
            isinstance(result, VM_ByteArray),
            "Byte array parsing must return VM_ByteArray"
        )

        self.assertTrue(
            result.get_byte_count() == 4,
            "VM_ByteArray created by byte array parsing must have exactly 4 bytes"
        )

        for index in range(len(byte_content)):
            self.assertTrue(
                result.byte_get_at(index) == byte_content[index],
                "VM_ByteArray created by byte array parsing must have correct bytes"
            )

    def test_bytearray_wrong_tag(self):
        byte_list = [0xFF]

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializerException, msg="Using byte array parsing, having wrong tag must fail"):
            result = deserializer.parse_bytearray()

    def test_bytearray_too_short_count(self):
        byte_count = (0).to_bytes(4, byteorder="big", signed=True)
        byte_list = [LiteralTags.VM_BYTEARRAY] + list(byte_count)

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializerException, msg="Using byte array parsing, having less than 8 bytes for size must fail"):
            result = deserializer.parse_bytearray()

    def test_bytearray_too_short_content(self):
        byte_content = [0x01, 0x02, 0x03, 0x04]
        byte_count = (8).to_bytes(8, byteorder="big", signed=True)
        byte_list = [LiteralTags.VM_BYTEARRAY] + list(byte_count) + byte_content

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializerException, msg="Using byte array parsing, having less content bytes than stated by size field must fail"):
            result = deserializer.parse_bytearray()


class SymbolParsingTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()