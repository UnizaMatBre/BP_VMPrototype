from source.vm_core.object_kinds import VM_ByteArray, VM_SmallInteger, VM_ObjectArray


def primitive_object_array_item_get_at(interpreter, parameters):
    object_array_object, index_object = parameters

    assert isinstance(object_array_object, VM_ObjectArray)
    assert isinstance(index_object, VM_SmallInteger)
    assert 0 <= index_object.get_value() < object_array_object.get_item_count()

    return interpreter.get_universe().new_small_integer(
        object_array_object.item_get_at(index_object.get_value())
    )

def primitive_object_array_item_put_at(interpreter, parameters):
    object_array_object, index_object, item_object = parameters

    assert isinstance(object_array_object, VM_ObjectArray)
    assert isinstance(index_object, VM_SmallInteger)
    assert 0 <= index_object.get_value() < object_array_object.get_item_count()

    object_array_object.item_put_at(index_object.get_code(), item_object)

    return interpreter.get_universe().get_none_object()

def primitive_object_array_get_item_count(interpreter, parameters):
    object_array_object = parameters[0]

    assert isinstance(object_array_object, VM_ObjectArray)

    return interpreter.get_universe().new_small_integer(
        object_array_object.get_item_count()
    )


LOCAL_PRIMITIVES = (
    ("ObjectArray_GetAt", 2, primitive_object_array_item_get_at),
    ("ObjectArray_PutAt", 3, primitive_object_array_item_put_at),
    ("ObjectArray_ItemCount", 1, primitive_object_array_get_item_count)
)