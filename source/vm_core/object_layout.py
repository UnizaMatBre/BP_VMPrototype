

class Object:
    def get_slot(self, slot_name):
        """
        Retrieves value from slot of specified name

        :param slot_name: name of the slot
        :return: None if slot doesn't exist, value in slot otherwise
        """
        raise NotImplementedError()


    def set_slot(self, slot_name, new_value):
        """
        Stores value into slot of specified name

        :param slot_name: name of the slot
        :param new_value: value that will be stored in the slot
        :return: True if slot exists, False if otherwise
        """
        raise NotImplementedError()


    def add_slot(self, slot_name, slot_kind, slot_value):
        """
        Creates new slot and stores value in it

        :param slot_name: name of new slot
        :param slot_kind: kind of new slot
        :param slot_value: value in new slot
        :return: True if slot was creates successfully, False if slot with same name already exists
        """
        raise NotImplementedError()

    def del_slot(self, slot_name):
        """
        Removes existing slot

        :param slot_name: name of soon-to-be removed slot
        :return: True if slot was successfully removed, False if slot with this name doesn't exist
        """

        raise NotImplementedError()