from source.vm_core.object_layout import VM_Object, SlotKind
from source.vm_core.object_kinds import *


class Universe:
    PARENT_KIND = SlotKind().toggleParent()
    NORMAL_KIND = SlotKind()

    def __init__(self):
        # root object of system
        self._lobby_object = None

        # name of slot linking object to trait
        self._parent_symbol = None

        # traits for other objects (object kinds + important objects)
        self._symbol_trait = None
        self._small_integer_trait = None
        self._byte_array_trait = None
        self._object_array_trait = None
        self._code_trait = None
        self._frame_trait = None
        self._process_trait = None
        self._true_object_trait = None
        self._false_object_trait = None
        self._none_object_trait = None

        # important objects
        self._true_object = None
        self._false_object = None
        self._none_object = None

    def init_clean_universe(self):
        self._symbol_trait = VM_Object()
        self._small_integer_trait = VM_Object()
        self._byte_array_trait = VM_Object()
        self._object_array_trait = VM_Object()
        self._code_trait = VM_Object()
        self._frame_trait = VM_Object()
        self._process_trait = VM_Object()

        self._true_object_trait = VM_Object()
        self._false_object_trait = VM_Object()
        self._none_object_trait = VM_Object()

        self._parent_symbol = VM_Symbol("parent", 0)
        self._parent_symbol.add_slot(self._parent_symbol, Universe.PARENT_KIND, self._symbol_trait)

        self._true_object = VM_Object()
        self._false_object = VM_Object()
        self._none_object = VM_Object()

        self._true_object.add_slot(self._parent_symbol, Universe.PARENT_KIND, self._true_object_trait)
        self._false_object.add_slot(self._parent_symbol, Universe.PARENT_KIND, self._false_object_trait)
        self._none_object.add_slot(self._parent_symbol, Universe.PARENT_KIND, self._none_object_trait)

        traits_object = VM_Object()

        def add_trait(name, trait_object):
            traits_object.add_slot(self.new_symbol(name, 0), Universe.NORMAL_KIND, trait_object)

        add_trait("Symbol", self._symbol_trait)
        add_trait("SmallInteger", self._small_integer_trait)
        add_trait("ByteArray", self._byte_array_trait)
        add_trait("ObjectArray", self._object_array_trait)
        add_trait("Code", self._code_trait)
        add_trait("Frame", self._frame_trait)
        add_trait("Process", self._process_trait)
        add_trait("True", self._true_object_trait)
        add_trait("False", self._false_object)
        add_trait("None", self._none_object)

        globals_object = VM_Object()

        globals_object.add_slot(self.new_symbol("True", 0), Universe.NORMAL_KIND, self._true_object)
        globals_object.add_slot(self.new_symbol("False", 0), Universe.NORMAL_KIND, self._false_object)
        globals_object.add_slot(self.new_symbol("None", 0), Universe.NORMAL_KIND, self._none_object)


        # initializing lobby
        self._lobby_object = VM_Object()
        self._lobby_object.add_slot(self.new_symbol("lobby", 0), Universe.NORMAL_KIND , self._lobby_object)
        self._lobby_object.add_slot(self.new_symbol("traits", 0), Universe.NORMAL_KIND, traits_object)
        self._lobby_object.add_slot(self.new_symbol("globals", 0), Universe.NORMAL_KIND, globals_object)



    def get_none_object(self):
        return self._none_object

    def get_true_object(self):
        return self._true_object

    def get_false_object(self):
        return self._false_object

    def _link_trait(self, child_object, trait):
        child_object.add_slot(self._parent_symbol, Universe.PARENT_KIND, trait)

    def new_symbol(self, text, arity):
        new_symbol = VM_Symbol(text, arity)
        self._link_trait(new_symbol, self._symbol_trait)

        return new_symbol

    def new_small_integer(self, value):
        new_small_integer = VM_SmallInteger(value)
        self._link_trait(new_small_integer, self._small_integer_trait)

        return new_small_integer

    def new_byte_array(self, byte_count):
        new_byte_array = VM_ByteArray(byte_count)
        self._link_trait(new_byte_array, self._byte_array_trait)

        return new_byte_array

    def new_object_array(self, item_count):
        new_object_array = VM_ObjectArray(item_count, self._none_object)
        self._link_trait(new_object_array, self._object_array_trait)

        return new_object_array

    def new_frame(self, stack, method_activation):
        new_frame = VM_Frame(self._none_object, stack, method_activation)
        self._link_trait(new_frame, self._frame_trait)

        return new_frame

    def new_frame_with_stack_size(self, stack_size, method_activation):
        new_stack = self.new_object_array(stack_size)
        new_frame = self.new_frame(new_stack, method_activation)

        return new_frame

    def new_process(self, root_frame):
        new_process = VM_Process(self._none_object, root_frame)
        self._link_trait(new_process, self._process_trait)

        return new_process