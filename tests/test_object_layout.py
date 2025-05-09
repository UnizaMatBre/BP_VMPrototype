import unittest

from source.vm_core import object_layout

class ObjectTestCase(unittest.TestCase):
    def test_slot_access(self):
        TEST_REAL_NAME = "testReal"
        TEST_FAKE_NAME = "testFake"
        TEST_FIRST_VALUE = 42
        TEST_SECOND_VALUE = 420

        testObject = object_layout.VM_Object()

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

    def test_slot_lookup(self):
        # name present in both parents
        TEST_SHARED_NAME = "shared"

        # name not present at all
        TEST_NONEXISTENT_NAME = "not_existing"

        # name present in one parent
        TEST_INPARENT_NAME = "in_parent"

        # name present in grandparent
        TEST_INGRANDPARENT_NAME = "in_grandparent"

        # name present in one parent and grandparent
        TEST_MULTIGEN_NAME = "multigen"

        # name that is in both children/receiver and both parents
        TEST_INPARENTCHILDREN_NAME = "both_generations"

        # name present in kid
        TEST_INCHILDREN_NAME = "in_children"

        # object setup
        grandParentObject   = object_layout.VM_Object()
        parentObject1       = object_layout.VM_Object()
        parentObject2       = object_layout.VM_Object()
        childrenObject      = object_layout.VM_Object()


        # setting up hierarchy
        childrenObject.add_slot("parent1", object_layout.SlotKind().toggleParent(), parentObject1)
        childrenObject.add_slot("parent2", object_layout.SlotKind().toggleParent(), parentObject2)

        parentObject1.add_slot("parent", object_layout.SlotKind().toggleParent(), grandParentObject)
        parentObject2.add_slot("parent", object_layout.SlotKind().toggleParent(), grandParentObject)

        # setting up target slots (values are not relevant)
        childrenObject.add_slot(TEST_INCHILDREN_NAME, object_layout.SlotKind(), 42)
        parentObject1.add_slot(TEST_INPARENT_NAME, object_layout.SlotKind(), 42)
        grandParentObject.add_slot(TEST_INGRANDPARENT_NAME, object_layout.SlotKind(), 42)

        parentObject1.add_slot(TEST_SHARED_NAME, object_layout.SlotKind(), 42)
        parentObject2.add_slot(TEST_SHARED_NAME, object_layout.SlotKind(), 42)

        parentObject2.add_slot(TEST_MULTIGEN_NAME, object_layout.SlotKind(), 42)
        grandParentObject.add_slot(TEST_MULTIGEN_NAME, object_layout.SlotKind(), 42)

        childrenObject.add_slot(TEST_INPARENTCHILDREN_NAME, object_layout.SlotKind(), 42)
        parentObject1.add_slot(TEST_INPARENTCHILDREN_NAME, object_layout.SlotKind(), 42)
        parentObject2.add_slot(TEST_INPARENTCHILDREN_NAME, object_layout.SlotKind(), 42)

        # asserts
        result = childrenObject.lookup_slot(TEST_INCHILDREN_NAME)
        self.assertTrue(
            result == (object_layout.SlotLookupStatus.FoundOne, childrenObject),
            "Lookup for in-children slot should found it in children object"
        )

        result = childrenObject.lookup_slot(TEST_NONEXISTENT_NAME)
        self.assertTrue(
            result[0] == object_layout.SlotLookupStatus.FoundNone,
            "Lookup for non-existing slot should be failure with 'FoundNone' status"
        )

        result = childrenObject.lookup_slot(TEST_INPARENT_NAME)
        self.assertTrue(
            result == (object_layout.SlotLookupStatus.FoundOne, parentObject1),
            "Lookup for in-parent slot should found it in parent object"
        )

        result = childrenObject.lookup_slot(TEST_INGRANDPARENT_NAME)
        self.assertTrue(
            result == (object_layout.SlotLookupStatus.FoundOne, grandParentObject),
            "Lookup for in-grandparent slot should found it in grandparent object"
        )

        result = childrenObject.lookup_slot(TEST_SHARED_NAME)
        self.assertTrue(
            result[0] == object_layout.SlotLookupStatus.FoundMany,
            "Lookup for shared slot should be failure with 'FoundSeveral' status"
        )

        result = childrenObject.lookup_slot(TEST_MULTIGEN_NAME)
        self.assertTrue(
            result[0] == object_layout.SlotLookupStatus.FoundMany,
            "Lookup for slot in multiple generations should be failure with 'FoundSeveral' status"
        )

        result = childrenObject.lookup_slot(TEST_INPARENTCHILDREN_NAME)
        self.assertTrue(
            result == (object_layout.SlotLookupStatus.FoundOne, childrenObject),
            "Lookup for slot that is present in both children and its parents should be found in children - lookup doesn't continue beyond successful find in receiver"
        )


if __name__ == '__main__':
    unittest.main()
