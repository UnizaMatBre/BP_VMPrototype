

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


class Object:
    def __init__(self):
        self._slots = {}

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

        # take all unvisited parent objects, mark them as visited and add them to search queue
        for slot in self._slots.values():
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
            for slot in viewed_object._slots.values():
                if slot[0].isParent() and slot[1] not in visited:
                    visited.add(slot[1])
                    queue.append(slot[1])

        # if we found slot, return object in which it was
        if slot_was_found:
            return (SlotLookupStatus.FoundOne, slot_was_found_in)

        # if we walked over all parents and found nothing, return FounNone
        return (SlotLookupStatus.FoundNone, None)
