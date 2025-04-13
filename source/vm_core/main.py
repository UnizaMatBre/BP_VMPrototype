import sys
from source.vm_core.bytecode_parsing import DeserializationError, BytecodeDeserializer, deserialize_module
from source.vm_core.object_layout import VM_Object, SlotKind
from source.vm_core.universe import Universe

BOOTLOADER_MODULE_NAME = "bootloader"


def make_module_process(universe, module_bytes):
    # deserialize module bytecode
    try:
        module_code_object = deserialize_module(universe, list(module_bytes))
    except DeserializationError as e:
        print("[VM]: Error during deserialization of code object")
        sys.exit(1)

    ## CONSTRUCT MODULE
    module_method_object = VM_Object()

    module_method_object.set_code(module_code_object)
    module_method_object.add_slot(
        universe.new_symbol("me", 0),
        SlotKind().toggleParent(),
        universe.get_lobby_object()
    )

    module_frame = universe.



if __name__ == "__main__":


    universe = Universe()
    universe.init_clean_universe()

    try:
        with open(BOOTLOADER_MODULE_NAME, "rb") as bootloader_file_obj:
            module_bytes = bootloader_file_obj.read()
    except FileNotFoundError:
        pass #bootloader doesn't exist, that is not really a problem

    make_module_process(universe, module_bytes)