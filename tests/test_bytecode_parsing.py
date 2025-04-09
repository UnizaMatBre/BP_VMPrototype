import unittest

from source.vm_core.bytecode_parsing import *
from source.vm_core.object_kinds import VM_ByteArray, VM_Symbol, VM_SmallInteger, VM_ObjectArray


class UniverseMockup:
    def new_byte_array(self, byte_count):
        return VM_ByteArray(byte_count)

    def new_object_array(self, item_count):
        return VM_ObjectArray(item_count=item_count, none_object=None)

    def new_symbol(self, text, arity):
        return VM_Symbol(text, arity)

    def new_small_integer(self, value):
        return VM_SmallInteger(value)


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
    def test_symbol_correct(self):
        arity_bytes = (10).to_bytes(8, byteorder="big", signed=True)
        text_bytes = "to_be_parsed".encode(encoding="ascii")
        text_bytes_count = len(text_bytes).to_bytes(8, byteorder="big", signed=True)

        byte_list = bytes([LiteralTags.VM_SYMBOL]) + arity_bytes + text_bytes_count + text_bytes

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        result = deserializer.parse_symbol()

        self.assertTrue(
            isinstance(result, VM_Symbol),
            "Symbol parsing must return VM_Symbol"
        )

        self.assertTrue(
            result.get_arity() == 10,
            "VM_Symbol created by parsing must have correct arity"
        )

        self.assertTrue(
            result._text == "to_be_parsed",
            "VM_Symbol created by parsing must have correct text"
        )

    def test_symbol_wrong_tag(self):
        byte_list = [0xFF]

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializerException, msg="Using symbol parsing, having wrong tag must fail"):
            result = deserializer.parse_symbol()

    def test_symbol_too_short_arity(self):
        arity_bytes = (10).to_bytes(4, byteorder="big", signed=True)
        byte_list = bytes([LiteralTags.VM_SYMBOL]) + arity_bytes

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializerException, msg="Using symbol parsing, having less than 8 bytes for arity must fail"):
            result = deserializer.parse_bytearray()

    def test_symbol_too_short_text_length(self):
        arity_bytes = (10).to_bytes(8, byteorder="big", signed=True)
        text_bytes_count = (8).to_bytes(4, byteorder="big", signed=True)

        byte_list = bytes([LiteralTags.VM_SYMBOL]) + arity_bytes + text_bytes_count

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializerException, msg="Using symbol parsing, having less text characters than stated by text length field must fail"):
            result = deserializer.parse_bytearray()

    def test_symbol_too_short_text(self):
        arity_bytes = (10).to_bytes(8, byteorder="big", signed=True)
        text_bytes = "to_be_parsed".encode(encoding="ascii")
        text_bytes_count = len(text_bytes * 20).to_bytes(8, byteorder="big", signed=True)

        byte_list = bytes([LiteralTags.VM_SYMBOL]) + arity_bytes + text_bytes_count + text_bytes

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializerException, msg="Using symbol parsing, having less than 8 bytes for text lenght must fail"):
            result = deserializer.parse_bytearray()


class SmallIntegerParsingTestCase(unittest.TestCase):
    def test_small_integer_correct(self):
        byte_list = bytes([LiteralTags.VM_SMALL_INTEGER]) + (-5).to_bytes(8, byteorder="big", signed=True)

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        result = deserializer.parse_small_integer()

        self.assertTrue(
            isinstance(result, VM_SmallInteger),
            "Small integer parsing must return VM_SmallInteger"
        )

        self.assertTrue(
            result.get_value() == -5,
            "VM_SmallInteger created by parsing must have correct value"
        )

    def test_small_integer_wrong_tag(self):
        byte_list = [0xFF]

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializerException, msg="Using small integer parsing, having wrong tag must fail"):
            result = deserializer.parse_small_integer()

    def test_small_integer_too_short_value(self):
        byte_list = [LiteralTags.VM_SMALL_INTEGER, 0x00, 0x00]

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializerException, msg="Using small integer parsing, having less than 8 bytes for value field must fail"):
            result = deserializer.parse_small_integer()

class ObjectArrayParsing(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()