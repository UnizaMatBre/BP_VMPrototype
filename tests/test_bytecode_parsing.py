import unittest

from source.vm_core.bytecode_parsing import *
from source.vm_core.object_kinds import VM_ByteArray, VM_Symbol, VM_SmallInteger, VM_ObjectArray


class UniverseMockup:
    def get_none_object(self):
        return None

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

        with self.assertRaises(DeserializationError, msg="Using byte array parsing, having wrong tag must fail"):
            result = deserializer.parse_bytearray()

    def test_bytearray_too_short_count(self):
        byte_count = (0).to_bytes(4, byteorder="big", signed=True)
        byte_list = [LiteralTags.VM_BYTEARRAY] + list(byte_count)

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializationError, msg="Using byte array parsing, having less than 8 bytes for size must fail"):
            result = deserializer.parse_bytearray()

    def test_bytearray_too_short_content(self):
        byte_content = [0x01, 0x02, 0x03, 0x04]
        byte_count = (8).to_bytes(8, byteorder="big", signed=True)
        byte_list = [LiteralTags.VM_BYTEARRAY] + list(byte_count) + byte_content

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializationError, msg="Using byte array parsing, having less content bytes than stated by size field must fail"):
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

        with self.assertRaises(DeserializationError, msg="Using symbol parsing, having wrong tag must fail"):
            result = deserializer.parse_symbol()

    def test_symbol_too_short_arity(self):
        arity_bytes = (10).to_bytes(4, byteorder="big", signed=True)
        byte_list = bytes([LiteralTags.VM_SYMBOL]) + arity_bytes

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializationError, msg="Using symbol parsing, having less than 8 bytes for arity must fail"):
            result = deserializer.parse_bytearray()

    def test_symbol_too_short_text_length(self):
        arity_bytes = (10).to_bytes(8, byteorder="big", signed=True)
        text_bytes_count = (8).to_bytes(4, byteorder="big", signed=True)

        byte_list = bytes([LiteralTags.VM_SYMBOL]) + arity_bytes + text_bytes_count

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializationError, msg="Using symbol parsing, having less text characters than stated by text length field must fail"):
            result = deserializer.parse_bytearray()

    def test_symbol_too_short_text(self):
        arity_bytes = (10).to_bytes(8, byteorder="big", signed=True)
        text_bytes = "to_be_parsed".encode(encoding="ascii")
        text_bytes_count = len(text_bytes * 20).to_bytes(8, byteorder="big", signed=True)

        byte_list = bytes([LiteralTags.VM_SYMBOL]) + arity_bytes + text_bytes_count + text_bytes

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializationError, msg="Using symbol parsing, having less than 8 bytes for text lenght must fail"):
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

        with self.assertRaises(DeserializationError, msg="Using small integer parsing, having wrong tag must fail"):
            result = deserializer.parse_small_integer()

    def test_small_integer_too_short_value(self):
        byte_list = [LiteralTags.VM_SMALL_INTEGER, 0x00, 0x00]

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)

        with self.assertRaises(DeserializationError, msg="Using small integer parsing, having less than 8 bytes for value field must fail"):
            result = deserializer.parse_small_integer()

class ObjectArrayParsing(unittest.TestCase):
    def test_object_array_correct_same_types(self):
        item_1 = bytes([LiteralTags.VM_SMALL_INTEGER]) + (0).to_bytes(8, byteorder="big", signed=True)
        item_2 = bytes([LiteralTags.VM_SMALL_INTEGER]) + (1).to_bytes(8, byteorder="big", signed=True)

        item_count = (2).to_bytes(8, byteorder="big", signed=True)

        byte_list = [LiteralTags.VM_OBJECT_ARRAY] + list(item_count) + list(item_1) + list(item_2)

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)
        result = deserializer.parse_object_array()

        self.assertTrue(
            isinstance(result, VM_ObjectArray),
            "Object array parsing must return VM_ObjectArray"
        )

        self.assertTrue(
            result.get_item_count() == 2,
            "Equal-sized VM_ObjectArray created by parsing must have exactly 2 items"
        )

        for index in range(2):
            item = result.item_get_at(index)

            self.assertTrue(
                isinstance(item, VM_SmallInteger),
                "Equal-sized VM_ObjectArray created by parsing containing integer tags must have VM_SmallInteger items"
            )

            self.assertTrue(
                item.get_value() == index,
                "Equal-sized VM_ObjectArray created by parsing containing integer tags must have correct integer values"
            )

    def test_object_array_correct_heterogeneous(self):
        items = [
            [LiteralTags.VM_SMALL_INTEGER] + list((3).to_bytes(8, byteorder="big", signed=True)),
            [LiteralTags.VM_NONE],
            [LiteralTags.VM_BYTEARRAY] + list((2).to_bytes(8, byteorder="big", signed=True)) + [0x01, 0x02]
        ]

        item1, item2, item3 = items
        byte_list = [LiteralTags.VM_OBJECT_ARRAY] + list(len(items).to_bytes(8, byteorder="big", signed=True)) + item1 + item2 + item3

        deserializer = BytecodeDeserializer(universe=UniverseMockup(), byte_list=byte_list)
        result = deserializer.parse_object_array()

        self.assertTrue(
            result.get_item_count() == 3,
            "Heterogeneous VM_ObjectArray created by parsing must have exactly 3 items"
        )

        self.assertTrue(
            isinstance(result.item_get_at(0), VM_SmallInteger) and result.item_get_at(1) is None  and isinstance(result.item_get_at(2), VM_ByteArray),
            "Heterogeneous VM_ObjectArray created by parsing must have correct item types (SmallInteger, None, ByteArray)"
        )



if __name__ == '__main__':
    unittest.main()