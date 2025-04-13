from source.vm_core.object_kinds import VM_PrimitiveMethod
from source.vm_core.object_layout import SlotKind

from source.vm_core.primitives import primitives_debug
from source.vm_core.primitives import primitives_small_integer
from source.vm_core.primitives import primitives_string
from source.vm_core.primitives import primitives_byte_array
from source.vm_core.primitives import primitives_object_array


def add_primitives_into(universe, primitives_holder):
    """
    Adds all primitives in package into specified object

    :param universe: universe of object - needed to create symbols
    :param primitives_holder: object where we want to insert out primitives
    :return: None
    """

    def add_primitive(primitive_info):
        primitive_name, primitive_param_count, primitive_func = primitive_info

        symbol_name = universe.new_symbol(primitive_name, primitive_param_count)

        primitives_holder.add_slot(
            symbol_name,
            SlotKind(),
            VM_PrimitiveMethod(primitive_param_count, primitive_func)
        )

    def add_all_local(primitive_module):
        for one_primitive_info in primitive_module.LOCAL_PRIMITIVES:
            add_primitive(one_primitive_info)

    add_all_local(primitives_debug)
    add_all_local(primitives_small_integer)
    add_all_local(primitives_string)
    add_all_local(primitives_byte_array)
    add_all_local(primitives_object_array)

