import unittest

from source.vm_core import object_layout

class ObjectTestCase(unittest.TestCase):
    def test_slot_access(self):
        TEST_REAL_NAME = "testReal"
        TEST_FAKE_NAME = "testFake"
        TEST_FIRST_VALUE = 42
        TEST_SECOND_VALUE = 420

        testObject = object_layout.Object()

        # TODO: implement slot kind
        # TODO: should this be split into multiple test cases?

        # creating slots
        self.assertTrue(
            testObject.add_slot(TEST_REAL_NAME, None, TEST_FIRST_VALUE),
            "Adding slot with name not used in object must be successful"
        )

        self.assertFalse(
            testObject.add_slot(TEST_REAL_NAME, None, TEST_FIRST_VALUE),
            "Adding slot with name already used by another slot in object must be failure"
        )

        # access and assignment of real slots
        self.assertTrue(
            testObject.get_slot(TEST_REAL_NAME) == TEST_FIRST_VALUE,
            "Accessing slot that exists must return its correct value"
        )

        self.assertTrue(
            testObject.set_slot(TEST_REAL_NAME, TEST_SECOND_VALUE),
            "Storing value into existing slot must be successful"
        )

        self.assertTrue(
            testObject.get_slot(TEST_REAL_NAME) == TEST_SECOND_VALUE,
            "After changing value in slot, accessing it must return new value"
        )

        # access and assignment of fake slot
        self.assertIsNone(
            testObject.get_slot(TEST_FAKE_NAME),
            "Accessing slot that doesn't exist must be failure"
        )

        self.assertFalse(
            testObject.set_slot(TEST_FAKE_NAME, TEST_FIRST_VALUE),
            "Storing value into slot that doesn't exist must be failure"
        )

        # deletion of slot

        self.assertTrue(
            testObject.del_slot(TEST_REAL_NAME),
            "Deleting slot that exists in object must be successful"
        )

        self.assertFalse(
            testObject.del_slot(TEST_REAL_NAME),
            "Deleting slot that was already deleted must be failure"
        )

        self.assertFalse(
            testObject.del_slot(TEST_FAKE_NAME),
            "Deleting slot that never existed must be failure"
        )






if __name__ == '__main__':
    unittest.main()
