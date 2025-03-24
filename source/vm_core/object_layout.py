

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