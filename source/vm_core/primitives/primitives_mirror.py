from ast import iter_child_nodes

from charset_normalizer.utils import is_arabic_isolated_form

from source.vm_core.bytecodes import SlotKindTags
from source.vm_core.object_kinds import VM_Mirror, VM_Symbol, VM_SmallInteger
from source.vm_core.object_layout import SlotKind


def primitive_mirror_mirror_on(interpreter, parameters):
    reflectee = parameters[0]

    return interpreter.get_universe().new_mirror(
        reflectee
    )

def primitive_mirror_add_slot(interpreter, parameters):
    mirror_object, slot_name_object, slot_kind_object, slot_content_object = parameters

    assert isinstance(mirror_object, VM_Mirror)
    assert isinstance(slot_name_object, VM_Symbol)
    assert isinstance(slot_kind_object, VM_SmallInteger)

    reflectee = mirror_object.get_reflectee()

    slot_kind_bytes = slot_kind_object.get_value()
    slot_kind = SlotKind()

    if slot_kind_bytes | SlotKindTags.PARAMETER_SLOT_TAG:
        slot_kind.toggleParameter()
    if slot_kind_bytes | SlotKindTags.PARENT_SLOT_TAG:
        slot_kind.toggleParent()



    result = reflectee.add_slot(
        slot_name_object,
        slot_kind,
        slot_content_object
    )

    assert result == True

    return interpreter.get_universe().get_none_object()






LOCAL_PRIMITIVES = (

)