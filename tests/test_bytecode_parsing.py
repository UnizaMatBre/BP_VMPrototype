import unittest

from source.vm_core.object_kinds import VM_ByteArray

class UniverseMockup:
    def new_byte_array(self, byte_count):
        return VM_ByteArray(byte_count)


class BytearrayParsingTestCase(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()