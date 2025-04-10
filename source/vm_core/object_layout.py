

class SlotKind:
    """
    Represents possible combinations of slot kinds
    """
    def __init__(self):
        self._isParent = False
        self._isParameter = False

    def toggleParent(self):
        self._isParent = not self._isParent
        return self

    def toggleParameter(self):
        self._isParameter = not self._isParameter
        return self

    def isParent(self):
        return self._isParent

    def isParameter(self):
        return self._isParameter


class SlotLookupStatus:
    FoundNone = 0,
    FoundOne = 1,
    FoundMany = 2


class VM_Object:
    def __init__(self):
        self._slots = {}
        self._code = None

    def copy(self):
        """
        Creates copy of self object, with same slots and structure
        :return: newly created copy object
        """
        copy_object = VM_Object()

        self._copy_slots_into(copy_object)

        return copy_object

    def _copy_slots_into(self, copy_object):
        """
        Copies own slots into specified object

        :param copy_object: object into which slots will be copied
        :return: None
        """

        copy_object._slots = self._slots.copy()

    def get_parameter_count(self):
        """
        Returns number of parameters this object has (mainly used by object kinds that override it)

        :return: 0
        """

        return 0

    def get_slot(self, slot_name):
        """
        Retrieves value from slot of specified name

        :param slot_name: name of the slot
        :return: None if slot doesn't exist, value in slot otherwise
        """
        if slot_name not in self._slots:
            return None

        return self._slots[slot_name][1]


    def set_slot(self, slot_name, new_value):
        """
        Stores value into slot of specified name

        :param slot_name: name of the slot
        :param new_value: value that will be stored in the slot
        :return: True if slot exists, False if otherwise
        """

        if slot_name not in self._slots:
            return False

        self._slots[slot_name][1] = new_value
        return True


    def add_slot(self, slot_name, slot_kind, slot_value):
        """
        Creates new slot and stores value in it

        :param slot_name: name of new slot
        :param slot_kind: kind of new slot
        :param slot_value: value in new slot
        :return: True if slot was creates successfully, False if slot with same name already exists
        """

        if slot_name in self._slots:
            return False

        self._slots[slot_name] = [slot_kind, slot_value]
        return True

    def del_slot(self, slot_name):
        """
        Removes existing slot

        :param slot_name: name of soon-to-be removed slot
        :return: True if slot was successfully removed, False if slot with this name doesn't exist
        """

        if slot_name not in self._slots:
            return False

        del self._slots[slot_name]
        return True

    def select_slot_values(self, predicate):
        """
        Returns slot values that fit passed predicate

        :param predicate: function that determined which slots will be returned
        :return: generator containing all fitting slots
        """
        return (slot for slot in self._slots.values() if predicate(slot))

    def select_slots(self, predicate):
        """
        Returns slots that fit passed predicate

        :param predicate: function that determined which slots will be returned. Accepts 3 parameters, slot name, kind and content
        :return: generator containing all filing slots in form of tuple: (SlotName, SlotKind, SlotContent)
        """

        return (
            (slot_name, slot_kind, slot_content) for slot_name, slot_kind, slot_content in self._slots.items() if predicate(slot_name, slot_kind, slot_content)
        )

    def lookup_slot(self, slot_name):
        """
        Searches for slot in object. If not found, continues search in parent slots

        :param slot_name: name of slot we want
        :return: (SlotLookupStatus: status of lookup, Object: object containing slot or None)
        """

        # no need to look further if slot is here
        if slot_name in self._slots:
            return (SlotLookupStatus.FoundOne, self)

        visited = {self}
        queue = []

        def parent_predicate(slot_value):
            return slot_value[0].isParent() and slot_value[1] not in visited

        # take all unvisited parent objects, mark them as visited and add them to search queue
        for slot in self.select_slot_values(parent_predicate):
            if slot[0].isParent() and slot[1] not in visited:
                visited.add(slot[1])
                queue.append(slot[1])


        slot_was_found = False
        slot_was_found_in = None

        # loop while there are parents to look at
        while len(queue) > 0:

            # get object and mark it as viewed
            viewed_object = queue.pop(0)

            # is slot in currently viewed object
            if slot_name in viewed_object._slots:
                # if slot was already found, return FoundSeveral
                if slot_was_found:
                    return (SlotLookupStatus.FoundMany, None)

                # mark the object and skip - we don't search parents of object that has slot we want
                slot_was_found = True
                slot_was_found_in = viewed_object
                continue

            # in case slot is not in this object
            # take all unvisited parent objects, mark them as visited and add them to search queue
            for slot in viewed_object.select_slot_values(parent_predicate):
                visited.add(slot[1])
                queue.append(slot[1])

        # if we found slot, return object in which it was
        if slot_was_found:
            return (SlotLookupStatus.FoundOne, slot_was_found_in)

        # if we walked over all parents and found nothing, return FoundNone
        return (SlotLookupStatus.FoundNone, None)

    def get_code(self):
        return self._code

    def set_code(self, new_code):
        self._code = new_code

    def has_code(self):
        """TODO: Maybe replace this with none_object?"""
        return self._code is not None
