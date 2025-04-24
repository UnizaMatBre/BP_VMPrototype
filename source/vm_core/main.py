import sys
from source.vm_core.bytecode_parsing import DeserializationError, BytecodeDeserializer, deserialize_module
from source.vm_core.interpreter import Interpreter
from source.vm_core.object_layout import VM_Object, SlotKind
from source.vm_core.universe import Universe

BOOTLOADER_MODULE_NAME = "bootloader"


def make_module_process(universe, module_bytes):
    # deserialize module bytecode
    try:
        module_code_object = deserialize_module(universe, list(module_bytes))
    except DeserializationError as e:
        print("[VM-Fatal]: Deserialization error: {}".format(str(e)))
        sys.exit(1)

    ## CONSTRUCT MODULE
    module_method_object = VM_Object()

    module_method_object.set_code(module_code_object)
    module_method_object.add_slot(
        universe.new_symbol("me", 0),
        SlotKind().toggleParent(),
        universe.get_lobby_object()
    )

    module_frame = universe.new_frame_with_code_stack_usage(module_method_object)
    module_process = universe.new_process(module_frame)

    return module_process


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[VM-Fatal] :: Pass exactly 1 argument - name of bytecode file.")
        sys.exit(1)

    universe = Universe()
    universe.init_clean_universe()

    try:
        with open(BOOTLOADER_MODULE_NAME, "rb") as bootloader_file_obj:
            module_bytes = bootloader_file_obj.read()
            bootstrap_process = make_module_process(universe, module_bytes)
            Interpreter(universe, bootstrap_process).execute_all()
    except FileNotFoundError:
        # bootloader doesn't exist, but that is not really a problem - bootloader just set up stdlib, it is not mandatory
        pass


    try:
        with open(sys.argv[1], "rb") as bootloader_file_obj:
            module_bytes = bootloader_file_obj.read()
            target_process = make_module_process(universe, module_bytes)
            Interpreter(universe, target_process).execute_all()
    except FileNotFoundError:
        # this one missing is actually a problem
        print("[VM-Fatal] :: code file '{}' doesn't exist".format(sys.argv[1]))
        sys.exit(1)
